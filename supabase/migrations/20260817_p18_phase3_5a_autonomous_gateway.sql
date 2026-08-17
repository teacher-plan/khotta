-- ════════════════════════════════════════════════════════════════════
-- KHOTTA Autonomous Operations 2.0 — Phase 3.5-A: بنية تحتية لبوّابة
-- التنفيذ الآلي (Autonomous Execution Gateway) — القفل الذرّي + قيد
-- منع التكرار (Idempotency) + توسيعٌ إضافيٌّ (لا هدمي) لقائمة حالات
-- repair_executions.status.
--
-- لا تفعيلٌ لأي شيء هنا: لا صفّ في repair_playbooks يتغيّر mode، ولا
-- self_healing_controls.self_healing_enabled يتغيّر. هذه الهجرة بنيةٌ
-- بحتة (جداول/أعمدة/قيود/دوال SQL)، لا سلوك تنفيذٍ آلي جديد يصبح
-- قابلاً للوصول فعلياً بسببها — الكود الذي يستدعيها (autonomousGateway.ts)
-- غير مربوطٍ بأي مسار HTTP/cron حيّ في هذه المرحلة (انظر تقرير التنفيذ).
-- ════════════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────────
-- 1) incident_claims — القفل الذرّي (المتطلَّب 7). جدولٌ مخصّص بدل إضافة
--    claimed_by/claimed_at مباشرةً على ops_incidents: يفصل "من يحاول
--    الإصلاح الآن" عن سجلّ الحادثة نفسه (الذي تكتبه أيضاً مسارات أخرى
--    كـsystem-health-check)، ويسمح بتاريخ محاولات ادّعاءٍ متعدّدة دون
--    فقد أي منها عبر UPDATE-in-place. الذرّية مضمونةٌ بقيد UNIQUE على
--    (incident_id, playbook_id) + INSERT..ON CONFLICT DO UPDATE بشرطٍ
--    صريح (WHERE) — لا سباق SELECT-then-UPDATE إطلاقاً؛ عبارة SQL واحدة.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.incident_claims (
  claim_id     uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  incident_id  uuid        NOT NULL REFERENCES public.ops_incidents(id),
  playbook_id  text        NOT NULL REFERENCES public.repair_playbooks(playbook_id),
  claimed_by   text        NOT NULL,     -- دوماً 'autonomous_execution_gateway' من هذا الكود — لا فاعلٌ بشري
  claimed_at   timestamptz NOT NULL DEFAULT now(),
  released_at  timestamptz,
  CONSTRAINT incident_claims_unique_target UNIQUE (incident_id, playbook_id)
);

CREATE INDEX IF NOT EXISTS idx_incident_claims_incident ON public.incident_claims(incident_id);

ALTER TABLE public.incident_claims ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.incident_claims FROM anon, authenticated;

COMMENT ON TABLE public.incident_claims IS
  'قفلٌ ذرّي على (incident_id, playbook_id) لمنع تنفيذٍ آليٍّ متزامن مزدوج لنفس الحادثة+الخطة (Phase 3.5-A، Gate 11). لا كتابة إلا من autonomousGateway.ts بمفتاح الخدمة.';

-- دالّة الادّعاء الذرّي: عبارة SQL واحدة (INSERT..ON CONFLICT DO UPDATE
-- WHERE) — لا يمكن لطلبين متزامنين كلاهما أن ينجحا لنفس الهدف؛ Postgres
-- يسلسل الوصول لصفّ الفهرس الفريد نفسه. تُعيد claim_id عند النجاح، أو
-- NULL صراحةً عند فشل الادّعاء (ادّعاءٌ آخر نشطٌ وغير منتهي الصلاحية).
CREATE OR REPLACE FUNCTION public.claim_incident_for_repair(
  p_incident_id   uuid,
  p_playbook_id   text,
  p_claimed_by    text,
  p_stale_minutes int DEFAULT 15
) RETURNS uuid
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_claim_id uuid;
BEGIN
  INSERT INTO public.incident_claims (incident_id, playbook_id, claimed_by, claimed_at, released_at)
  VALUES (p_incident_id, p_playbook_id, p_claimed_by, now(), NULL)
  ON CONFLICT (incident_id, playbook_id) DO UPDATE
    SET claimed_by = EXCLUDED.claimed_by,
        claimed_at = now(),
        released_at = NULL
    WHERE public.incident_claims.released_at IS NOT NULL
       OR public.incident_claims.claimed_at < now() - (p_stale_minutes || ' minutes')::interval
  RETURNING claim_id INTO v_claim_id;

  RETURN v_claim_id;  -- NULL إن كان الادّعاء الحالي لا يزال نشطاً وغير منتهي الصلاحية
END;
$$;

REVOKE ALL ON FUNCTION public.claim_incident_for_repair(uuid, text, text, int) FROM anon, authenticated;

COMMENT ON FUNCTION public.claim_incident_for_repair IS
  'ادّعاءٌ ذرّي لحق تنفيذ إصلاحٍ آليٍّ على (incident_id, playbook_id) — عبارة SQL واحدة، لا سباق. يُستدعى فقط من autonomousGateway.ts (Gate 11) بمفتاح الخدمة.';

-- دالّة تحرير الادّعاء الصريح بعد انتهاء المحاولة (نجاحاً أو فشلاً) —
-- تسمح بادّعاءٍ لاحق فوري (مثلاً محاولةٌ ثانية إن attempt_number < max_attempts)
-- دون انتظار انتهاء stale window.
CREATE OR REPLACE FUNCTION public.release_incident_claim(p_claim_id uuid)
RETURNS void
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
  UPDATE public.incident_claims SET released_at = now() WHERE claim_id = p_claim_id;
$$;

REVOKE ALL ON FUNCTION public.release_incident_claim(uuid) FROM anon, authenticated;

-- ─────────────────────────────────────────────────────────────────────
-- 2) قيد منع التكرار على مستوى القاعدة (المتطلَّب 8): فهرسٌ فريدٌ جزئي
--    على (incident_id, playbook_id, attempt_number) — يُطبَّق فقط عندما
--    incident_id غير NULL (تنفيذات evaluateShadow المستقلّة عن حادثةٍ
--    محدَّدة، إن وُجدت، تبقى خارج هذا القيد كما كانت). يجعل إدراج نفس
--    (حادثة، خطة، رقم محاولة) مرّتين مستحيلاً بنيوياً حتى تحت تزامنٍ
--    حقيقي — لا فحص تطبيقي فقط.
-- ─────────────────────────────────────────────────────────────────────
CREATE UNIQUE INDEX IF NOT EXISTS uq_repair_executions_incident_playbook_attempt
  ON public.repair_executions (incident_id, playbook_id, attempt_number)
  WHERE incident_id IS NOT NULL;

COMMENT ON INDEX public.uq_repair_executions_incident_playbook_attempt IS
  'منع تكرارٍ على مستوى القاعدة (Phase 3.5-A، Gate 12): لا إدراج مزدوج لنفس (incident_id, playbook_id, attempt_number) — يفشل INSERT الثاني بخطإٍ حقيقي من Postgres، لا بفحصٍ تطبيقي قابلٍ للتفويت تحت تزامن.';

-- ─────────────────────────────────────────────────────────────────────
-- 3) توسيعٌ إضافي (لا هدمي) لقيد repair_executions.status — حالاتٌ
--    جديدة تخصّ رفض بوّابات البوّابة الآلية الجديدة (Gate 0/1/2/10/11/12)
--    غير الموجودة أصلاً في قائمة evaluateShadow (القسم 15). لا حالةٌ
--    قديمة تُحذَف أو تُعاد تسميتها.
-- ─────────────────────────────────────────────────────────────────────
ALTER TABLE public.repair_executions DROP CONSTRAINT IF EXISTS repair_executions_status_check;
ALTER TABLE public.repair_executions ADD CONSTRAINT repair_executions_status_check
  CHECK (status IN (
    'EVALUATING', 'WOULD_AUTO_HEAL', 'DRY_RUN_LOGGED', 'PRECONDITION_FAILED',
    'RISK_BLOCKED', 'RATE_LIMITED', 'COOLDOWN_ACTIVE', 'CIRCUIT_OPEN', 'DISABLED',
    'RUNNING', 'SUCCEEDED', 'FAILED', 'VERIFICATION_FAILED', 'ESCALATED',
    -- ═══ Phase 3.5-A — بوّابات جديدة خاصّة بمسار autonomousGateway.ts فقط ═══
    'INVALID_INCIDENT',            -- Gate 0: incident_id غير موجود/غير صالح
    'INVALID_DIAGNOSIS',           -- Gate 1: diagnosis_id غير موجود/غير مكتمل
    'NO_PLAYBOOK_MATCH',           -- Gate 2: لا نمط حادثةٍ معروف يطابق
    'CLAIM_FAILED',                -- Gate 11: فشل الادّعاء الذرّي (محاولةٌ أخرى نشطة)
    'DUPLICATE_EXECUTION_BLOCKED', -- Gate 12: مفتاح idempotency مُستخدَمٌ سلفاً
    'ACTION_VALIDATION_FAILED'     -- Gate 10: الإجراء غير معروف/غير مفعَّل/خارج allowed_actions/لا استراتيجية تحقّق
  ));

COMMENT ON CONSTRAINT repair_executions_status_check ON public.repair_executions IS
  'Phase 3.5-A: توسيعٌ إضافيٌّ فقط — كل قيمةٍ من Phase 3 (evaluateShadow) بقيت كما هي، أُضيفت 6 قيمٍ جديدة لبوّابات autonomousGateway.ts (Gate 0/1/2/10/11/12) حصراً.';
