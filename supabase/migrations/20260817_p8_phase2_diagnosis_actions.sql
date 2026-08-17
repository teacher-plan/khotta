-- ════════════════════════════════════════════════════════════════════
-- KHOTTA AUTONOMOUS OPERATIONS 2.0 — PHASE 2
-- تشخيصٌ وإجراءاتٌ آمنة (Diagnosis & Safe Actions)
--
-- إضافيٌّ بالكامل — لا حذف ولا إعادة تسمية لأي عمود/جدول/قيمة قائمة من
-- Phase 1/1.5/1.75. أربعة جداول جديدة + تمديد قيمة CHECK واحدة على
-- ops_incidents (تراكمياً، إضافةً لا استبدالاً).
--
-- المبدأ الجوهري لهذه المرحلة: لا تنفيذ تلقائي عام. كل إجراءٍ يمرّ عبر
-- سجلّ إجراءاتٍ آمنة (safe_action_registry) محدَّد سلفاً — لا SQL حرّ ولا
-- إجراءات مُختَرَعة وقت التشغيل. القراءة الإدارية لكل الجداول أدناه حصراً
-- عبر Edge Functions (is_app_admin على الخادم) — لا سياسة RLS مباشرة
-- لـanon/authenticated، بنفس نمط ops_incidents/agent_registry القائم.
-- ════════════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────────
-- 1) safe_action_registry — قبل أي شيءٍ آخر: هذا هو الحارس. كل إجراءٍ
--    قابلٍ للتنفيذ (آلياً أو بموافقة مشرف) يجب أن يكون صفاً هنا أولاً —
--    لا تنفيذ لإجراءٍ غير مسجَّل، ولا استثناء.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.safe_action_registry (
  action_id               text        PRIMARY KEY,   -- معرّفٌ ثابت، يطابق مفتاحاً في كود opsActionRegistry.ts (لا تنفيذ لمعرّفٍ غير معروفٍ في الكود أيضاً — تحقّقٌ مزدوج DB×code)
  name                     text        NOT NULL,
  description              text        NOT NULL,
  category                 text        NOT NULL CHECK (category IN ('RERUN_MONITOR','RESCHEDULE','NOTIFY_ONLY')),
  risk_level               text        NOT NULL CHECK (risk_level IN ('LOW','MEDIUM','HIGH','CRITICAL')),
  allowed_agents           jsonb       NOT NULL DEFAULT '[]'::jsonb,  -- agent_id المسموح لهم بطلب هذا الإجراء (نادراً LLM، غالباً المشرف عبر اللوحة/الكوبايلوت)
  required_permission      text        NOT NULL,       -- يطابق permission_level في agent_registry
  input_schema             jsonb       NOT NULL DEFAULT '{}'::jsonb,
  output_schema            jsonb       NOT NULL DEFAULT '{}'::jsonb,
  reversible               boolean     NOT NULL,
  rollback_strategy        text        NOT NULL,       -- نصٌّ إلزامي — لا صفَّ بلا استراتيجية توثَّق حتى لو كانت "لا حاجة، العملية مثاليّة" (idempotent)
  verification_strategy    text        NOT NULL,       -- كيف يُتحقَّق من نجاح الإجراء فعلياً بعد التنفيذ — إلزامي
  requires_human_approval  boolean     NOT NULL DEFAULT true,
  enabled                  boolean     NOT NULL DEFAULT true,
  created_at               timestamptz NOT NULL DEFAULT now(),
  updated_at               timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE public.safe_action_registry ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.safe_action_registry FROM anon, authenticated;

COMMENT ON TABLE public.safe_action_registry IS
  'سجلّ الإجراءات الآمنة المسموح تنفيذها — كل إجراءٍ محدَّد سلفاً، لا تنفيذٌ لأي إجراءٍ غير مسجَّل هنا. ممنوعٌ صراحةً تسجيل execute_sql/execute_command/run_any_function/admin_override/ai_action أو أي مكافئٍ عام.';

-- قيدٌ إضافي دفاعي: يرفض أي محاولة تسجيل اسمٍ من الأسماء العامة الممنوعة
-- صراحةً في المواصفة، حتى لو غفل مراجعٌ بشري عن القاعدة أعلاه لاحقاً.
ALTER TABLE public.safe_action_registry
  ADD CONSTRAINT safe_action_registry_no_generic_ids
  CHECK (action_id NOT IN ('execute_sql','execute_command','run_any_function','admin_override','ai_action'));

-- ─────────────────────────────────────────────────────────────────────
-- 2) ops_diagnoses — تشخيصٌ واحد لكل دورة تحليل، مرتبطٌ بحادثةٍ في
--    ops_incidents. لا يُعلَّم COMPLETED إلا حين ينتهي التحليل فعلاً —
--    الحالات الأخرى (LOW_CONFIDENCE/FAILED) صريحة، لا صمتٌ عن الفشل.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.ops_diagnoses (
  diagnosis_id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  incident_id              uuid        NOT NULL REFERENCES public.ops_incidents(id),
  agent_id                 text        REFERENCES public.agent_registry(agent_id),  -- من طلب التشخيص (ops-analyze غالباً)، NULL إن كان المشرف مباشرةً
  correlation_id            uuid        NOT NULL DEFAULT gen_random_uuid(),
  created_at                timestamptz NOT NULL DEFAULT now(),
  completed_at              timestamptz,
  diagnosis_status          text        NOT NULL DEFAULT 'PENDING'
                                CHECK (diagnosis_status IN ('PENDING','COLLECTING_EVIDENCE','ANALYZING','COMPLETED','LOW_CONFIDENCE','FAILED')),
  suspected_root_cause      text,        -- NULL إن كانت الأدلة غير كافية (INSUFFICIENT EVIDENCE) — لا سببٌ مُختلَق أبداً
  confidence                int         CHECK (confidence IS NULL OR (confidence BETWEEN 0 AND 100)),
  confidence_reasoning      text,        -- تفسيرٌ صريح لرقم الثقة (القسم 4 من المواصفة)
  evidence                  jsonb       NOT NULL DEFAULT '[]'::jsonb,   -- كل بند: {source,timestamp,type,value,reliability}
  contributing_factors      jsonb       NOT NULL DEFAULT '[]'::jsonb,
  recommended_action_id     text        REFERENCES public.safe_action_registry(action_id),  -- NULL إن لم يوجد إجراءٌ آمن مطابق
  risk_level                text        CHECK (risk_level IS NULL OR risk_level IN ('LOW','MEDIUM','HIGH','CRITICAL')),
  risk_factors              jsonb       NOT NULL DEFAULT '{}'::jsonb,   -- {data_modification,user_impact,financial_impact,reversibility,blast_radius,production_impact,security_impact}
  requires_human            boolean     NOT NULL DEFAULT true,
  model_used                text,
  token_usage                jsonb,
  cost_usd                   numeric,
  error                       text
);

CREATE INDEX IF NOT EXISTS idx_ops_diagnoses_incident ON public.ops_diagnoses(incident_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_ops_diagnoses_status    ON public.ops_diagnoses(diagnosis_status);
CREATE INDEX IF NOT EXISTS idx_ops_diagnoses_correlation ON public.ops_diagnoses(correlation_id);

ALTER TABLE public.ops_diagnoses ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.ops_diagnoses FROM anon, authenticated;

COMMENT ON TABLE public.ops_diagnoses IS
  'تشخيصٌ مرتبطٌ بحادثة ops_incidents — سبب مُرجَّح + ثقة + إجراءٌ موصى به من safe_action_registry حصراً (أو NULL إن لم يوجد). لا تنفيذ من هذا الجدول نفسه.';

-- ─────────────────────────────────────────────────────────────────────
-- 3) action_approvals — كل تنفيذٍ يتطلّب موافقة (بحسب requires_human_
--    approval في السجلّ) يمرّ عبر صفٍّ هنا أولاً، بانتهاء صلاحيةٍ صريح.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.action_approvals (
  approval_id      uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  action_id         text        NOT NULL REFERENCES public.safe_action_registry(action_id),
  incident_id        uuid        REFERENCES public.ops_incidents(id),
  diagnosis_id        uuid        REFERENCES public.ops_diagnoses(diagnosis_id),
  input_params         jsonb       NOT NULL DEFAULT '{}'::jsonb,
  requested_by          text        NOT NULL,   -- 'system' (اقتراح تلقائي) أو user_id/email المشرف
  requested_at           timestamptz NOT NULL DEFAULT now(),
  expires_at              timestamptz NOT NULL,   -- إلزامي — لا موافقة بلا انتهاء صلاحية (القسم 8)
  approved_by              text,
  approved_at               timestamptz,
  status                     text        NOT NULL DEFAULT 'PENDING'
                                CHECK (status IN ('PENDING','APPROVED','REJECTED','EXPIRED'))
);

CREATE INDEX IF NOT EXISTS idx_action_approvals_status ON public.action_approvals(status, expires_at);
CREATE INDEX IF NOT EXISTS idx_action_approvals_incident ON public.action_approvals(incident_id);

ALTER TABLE public.action_approvals ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.action_approvals FROM anon, authenticated;

COMMENT ON TABLE public.action_approvals IS
  'طلبات موافقةٍ بشرية على إجراءٍ من safe_action_registry — تنتهي صلاحيتها. لا تنفيذ لإجراءٍ requires_human_approval=true بلا صفٍّ APPROVED هنا لم تنقضِ صلاحيته.';

-- ─────────────────────────────────────────────────────────────────────
-- 4) action_executions — كل محاولة تنفيذٍ فعلية (سواءٌ آلية لإجراءٍ لا
--    يتطلّب موافقة، أو بعد موافقةٍ بشرية) + التحقّق (Verification) بعدها.
--    سقفُ محاولةٍ آليةٍ واحدة لكل (incident_id, action_id) — القسم 15:
--    لا حلقة إجراءاتٍ (enforced في الكود، موثَّقٌ هنا أيضاً بالتعليق).
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.action_executions (
  execution_id       uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  action_id            text        NOT NULL REFERENCES public.safe_action_registry(action_id),
  incident_id           uuid        REFERENCES public.ops_incidents(id),
  diagnosis_id           uuid        REFERENCES public.ops_diagnoses(diagnosis_id),
  approval_id             uuid        REFERENCES public.action_approvals(approval_id),  -- NULL إن كان الإجراء لا يتطلّب موافقة
  correlation_id            uuid        NOT NULL DEFAULT gen_random_uuid(),
  input_params                jsonb       NOT NULL DEFAULT '{}'::jsonb,
  executed_by                  text        NOT NULL,  -- 'system_auto' أو user_id/email المشرف الذي ضغط "تنفيذ"
  attempt_number                 int         NOT NULL DEFAULT 1,  -- ≤1 للتنفيذ الآلي بلا موافقة (القسم 15) — يُنفَّذ في الكود
  started_at                       timestamptz NOT NULL DEFAULT now(),
  completed_at                       timestamptz,
  execution_status                     text        NOT NULL DEFAULT 'RUNNING'
                                        CHECK (execution_status IN ('RUNNING','SUCCEEDED','FAILED')),
  execution_result                       jsonb,
  execution_error                          text,
  verification_status                        text        NOT NULL DEFAULT 'PENDING'
                                        CHECK (verification_status IN ('PENDING','RUNNING','PASSED','FAILED','INCONCLUSIVE')),
  verification_detail                          jsonb,
  verified_at                                    timestamptz,
  incident_resolved                                boolean     NOT NULL DEFAULT false,  -- true فقط إن نجح التنفيذ ونجح التحقّق معاً (القسم 12)
  escalated                                          boolean     NOT NULL DEFAULT false,
  escalation_reason                                    text
);

CREATE INDEX IF NOT EXISTS idx_action_executions_incident ON public.action_executions(incident_id, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_action_executions_correlation ON public.action_executions(correlation_id);

ALTER TABLE public.action_executions ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.action_executions FROM anon, authenticated;

COMMENT ON TABLE public.action_executions IS
  'كل محاولة تنفيذ إجراءٍ آمن + نتيجة التحقّق التالية. incident_resolved=true فقط إن نجح التنفيذ والتحقّق معاً — لا إغلاق حادثةٍ لمجرّد نجاح نداء الدالّة (القسم 12). سقف محاولةٍ آليةٍ واحدة يُطبَّق في الكود (opsActionRegistry.ts)، لا تكراراً تلقائياً بإجراءٍ آخر عند الفشل (القسم 15).';

-- ─────────────────────────────────────────────────────────────────────
-- 5) internal_agent_requests — أي حاجةٍ بين-وكلاء تُنمذَج صراحةً هنا، لا
--    نداءٌ حرٌّ مباشر بين دالّتي حافة (القسم 19).
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.internal_agent_requests (
  request_id     uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  source          text        NOT NULL,   -- agent_id الطالب
  target           text        NOT NULL,   -- agent_id/الدالّة المطلوب منها
  purpose           text        NOT NULL,
  correlation_id      uuid        NOT NULL DEFAULT gen_random_uuid(),
  requested_at          timestamptz NOT NULL DEFAULT now(),
  completed_at            timestamptz,
  status                    text        NOT NULL DEFAULT 'PENDING' CHECK (status IN ('PENDING','RUNNING','SUCCEEDED','FAILED')),
  result                     jsonb
);

CREATE INDEX IF NOT EXISTS idx_internal_agent_requests_status ON public.internal_agent_requests(status);

ALTER TABLE public.internal_agent_requests ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.internal_agent_requests FROM anon, authenticated;

COMMENT ON TABLE public.internal_agent_requests IS
  'نمذجةٌ صريحة لأي طلبٍ بين-وكلاء (مثال: ops-actions يطلب من رصيد التشغيل الفعلي لإجراءٍ آمن) — لا نداءٌ حرٌّ غير موثَّق بين دوالّ الحافة.';

-- ─────────────────────────────────────────────────────────────────────
-- 6) ops_incidents.status — توسيعٌ تراكمي بقيمة ESCALATED (القسم 14):
--    حادثةٌ صعدت لعناية المشرف البشري صراحةً (ثقةٌ منخفضة/تحقّقٌ فاشل/
--    فشل إجراء/نتيجةٌ غير متوقّعة) — منفصلةٌ عن RESOLVED وعن أي حالةٍ
--    سابقة، بلا حذفٍ لأيّ قيمةٍ قائمة.
-- ─────────────────────────────────────────────────────────────────────
ALTER TABLE public.ops_incidents DROP CONSTRAINT IF EXISTS ops_incidents_status_check;
ALTER TABLE public.ops_incidents ADD CONSTRAINT ops_incidents_status_check
  CHECK (status IN ('DETECTED','INVESTIGATING','IDENTIFIED','RECOMMENDATION','RESOLVED','ESCALATED'));

-- ─────────────────────────────────────────────────────────────────────
-- 7) تعبئة safe_action_registry — أول إجراءات Phase 2، القسم 7: مُختارةٌ
--    من عملياتٍ حقيقية موجودة فعلاً في الكود (invokeAgentNow في
--    telegram-webhook، وكتابة agent_schedules في نفس الملف) — لا اختراع.
-- ─────────────────────────────────────────────────────────────────────
INSERT INTO public.safe_action_registry
  (action_id, name, description, category, risk_level, allowed_agents, required_permission,
   input_schema, output_schema, reversible, rollback_strategy, verification_strategy,
   requires_human_approval, enabled)
VALUES
  ('rerun_monitor_agent',
   'إعادة تشغيل وكيل مراقبة',
   'نداءٌ فوري لدالّة وكيل مراقبةٍ معروفة (system-health-check/credit-monitor/database-capacity-monitor/file-processor-monitor/daily-summary) — نفس نداء زرّ "إعادة الآن/تحديث" الحقيقي في تلغرام (telegram-webhook: invokeAgentNow) بلا أي تعديل على منطقه. الوكلاء المسموحة كلّها MONITOR/NOTIFIER بلا كتابةٍ على بياناتٍ حسّاسة — قراءةٌ أو تنبيهٌ فقط.',
   'RERUN_MONITOR', 'LOW', '["ops-analyze"]'::jsonb, 'SAFE_ACTION',
   '{"agent_id":{"type":"string","enum":["system-health-check","credit-monitor","database-capacity-monitor","file-processor-monitor","daily-summary"]}}'::jsonb,
   '{"invoked":"boolean","http_status":"number"}'::jsonb,
   true,
   'لا حاجة لتراجعٍ فعلي: العملية مثاليّة (idempotent) — إعادة تشغيل وكيل مراقبةٍ لا تُغيّر بيانات مستخدمين ولا تُصدر أي أثرٍ لا يمكن تكراره بأمان؛ يمكن إيقافه بعدم استدعائه مجدداً فقط.',
   'التحقّق من ظهور صفٍّ جديد في agent_runs لنفس agent_id بعد وقت بدء التنفيذ (started_at)، وأن status انتهى SUCCESS خلال مهلة 60 ثانية — PASSED فقط عند تحقّق الشرطين معاً، وإلا FAILED/INCONCLUSIVE.',
   false, true),

  ('reschedule_daily_summary',
   'إعادة جدولة الملخّص اليومي',
   'تحديث agent_schedules.scheduled_hour/scheduled_minute للوكيل daily-summary إلى الوقت الحالي — نفس الكتابة الحقيقية القائمة أصلاً خلف زرّ "إعادة جدولة" في تلغرام (summary:reschedule)، بلا تعديلٍ على منطقها. لا صلة لها ببيانات مستخدمين/بيانات مالية/بيانات أكاديمية أو مخطط قاعدة البيانات — سطر جدولة تشغيلي بحت.',
   'RESCHEDULE', 'LOW', '["ops-analyze"]'::jsonb, 'SAFE_ACTION',
   '{}'::jsonb,
   '{"scheduled_hour":"number","scheduled_minute":"number"}'::jsonb,
   true,
   'رجعيٌّ بالكامل: كتابة قيمتي scheduled_hour/scheduled_minute السابقتين (تُقرأان وتُحفَظان في input_params قبل التنفيذ) تُعيد الحالة كما كانت — لا حذف ولا فقدان بيانات.',
   'قراءة agent_schedules بعد التنفيذ والتأكّد أن scheduled_hour/scheduled_minute تطابقان القيمة المطلوبة فعلاً (لا افتراض نجاح UPDATE من عدد الصفوف المتأثرة وحده).',
   false, true)
ON CONFLICT (action_id) DO NOTHING;

-- تحقّق يدوي بعد التطبيق:
--   SELECT action_id, risk_level, reversible, requires_human_approval FROM public.safe_action_registry;
--   SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conname IN ('ops_incidents_status_check','safe_action_registry_no_generic_ids');
