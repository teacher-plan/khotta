-- ════════════════════════════════════════════════════════════════════
-- KHOTTA AUTONOMOUS OPERATIONS 2.0 — PHASE 3
-- الإصلاح الذاتي المُتحكَّم به (Controlled Self-Healing)
--
-- إضافيٌّ بالكامل — لا حذف ولا إعادة تسمية لأي عمود/جدول/قيمة قائمة من
-- Phase 1/1.5/1.75/2. جدولان جديدان (repair_playbooks، repair_executions)
-- + جدول تحكّمٍ عامّ واحد (self_healing_controls) للإيقاف الطارئ.
--
-- المبدأ الجوهري: LEVEL 4 (الإصلاح الذاتي) خاصٌّ بـPlaybook محدَّد، لا
-- بوكيلٍ كامل — لا يُرفَع أي صفٍّ في agent_registry إلى LEVEL 4 هنا ولا
-- في أي مكانٍ آخر. المستوى يعيش على الـplaybook/التنفيذ فقط.
--
-- كل الـPlaybooks تُنشأ هنا enabled=true لكنها mode='SHADOW' حصراً —
-- لا Playbook واحد يُفعَّل بوضع AUTO ضمن هذه الهجرة (القسم 15). تفعيل
-- AUTO قرارٌ بشريٌّ لاحقٌ صريح، خارج نطاق هذه المرحلة تماماً.
-- ════════════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────────
-- 1) self_healing_controls — التحكّم الطارئ العام (القسم 12): تعطيل
--    الإصلاح الذاتي كلياً، أو لوكيلٍ بعينه، مستقلٌّ تماماً عن مراقبة
--    الحالة (المراقبة تستمر دوماً بلا علاقة بهذا الجدول). صفٌّ واحدٌ ثابت
--    (singleton) بمعرّفٍ ثابت 'global'.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.self_healing_controls (
  control_id            text        PRIMARY KEY DEFAULT 'global' CHECK (control_id = 'global'),
  self_healing_enabled  boolean     NOT NULL DEFAULT true,   -- إيقافٌ عامٌّ فوري لكل Playbook — المراقبة تستمر
  disabled_agents        jsonb       NOT NULL DEFAULT '[]'::jsonb,  -- قائمة agent_id مُعطَّلةٌ إصلاحها الذاتي تحديداً
  disabled_reason          text,
  updated_by                 text,
  updated_at                  timestamptz NOT NULL DEFAULT now()
);
INSERT INTO public.self_healing_controls (control_id, self_healing_enabled)
  VALUES ('global', true) ON CONFLICT (control_id) DO NOTHING;

ALTER TABLE public.self_healing_controls ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.self_healing_controls FROM anon, authenticated;

COMMENT ON TABLE public.self_healing_controls IS
  'مفتاح الإيقاف الطارئ العام للإصلاح الذاتي (Phase 3، القسم 12) — صفٌّ واحدٌ ثابت. المراقبة (Monitoring) تستمر دوماً بصرف النظر عن قيمته.';

-- ─────────────────────────────────────────────────────────────────────
-- 2) repair_playbooks — سجلّ خطط الإصلاح المعروفة (القسم 1). كل Playbook
--    حتميٌّ بالكامل: repair_steps تشير حصراً لمعرّفات action_id موجودة
--    فعلاً في safe_action_registry — لا خطوةٍ حرّة يخترعها LLM وقت
--    التنفيذ (القسم 2).
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.repair_playbooks (
  playbook_id               text        PRIMARY KEY,   -- معرّفٌ ثابت، يطابق مفتاحاً في كود opsPlaybooks.ts (تحقّقٌ مزدوج DB×code كنمط safe_action_registry)
  name                       text        NOT NULL,
  description                text        NOT NULL,
  incident_pattern             text        NOT NULL,   -- معرّف نمطٍ حتميٌّ من ruleBasedDiagnose (مثال: KNOWN_MONITOR_REPEATED_FAILURE)
  diagnosis_requirements        jsonb       NOT NULL DEFAULT '{}'::jsonb,  -- {min_consecutive_failures, same_error_required, ...}
  minimum_confidence            int         NOT NULL CHECK (minimum_confidence BETWEEN 0 AND 100),
  risk_level                     text        NOT NULL CHECK (risk_level IN ('LOW','MEDIUM','HIGH','CRITICAL')),
  allowed_agents                  jsonb       NOT NULL DEFAULT '[]'::jsonb,  -- agent_id المسموح تشغيلها ضمن هذا الـPlaybook حصراً (نطاق ضيّق — القسم Level 4 خاصٌّ بالـPlaybook لا بالوكيل)
  allowed_actions                  jsonb       NOT NULL,  -- مصفوفة action_id من safe_action_registry حصراً — لا يمكن أن تكون فارغة
  preconditions                     jsonb       NOT NULL DEFAULT '[]'::jsonb,  -- قائمة أسماء شروطٍ حتمية يتحقّقها الكود (القسم 5)
  repair_steps                       jsonb       NOT NULL,  -- [{action_id, params_template}] — action_id يجب أن يطابق allowed_actions
  verification_steps                   jsonb       NOT NULL,  -- وصفٌ نصّي/بنيويّ لما تتحقّقه verify() في opsActionRegistry.ts لكل خطوة
  rollback_strategy                     text        NOT NULL,  -- إلزاميّ دوماً — نصٌّ معروفٌ سلفاً (القسم 21)، لا اختراع وقت التنفيذ
  max_attempts                           int         NOT NULL DEFAULT 2 CHECK (max_attempts BETWEEN 1 AND 5),
  cooldown_minutes                        int         NOT NULL DEFAULT 30 CHECK (cooldown_minutes >= 0),
  circuit_breaker_threshold                 int         NOT NULL DEFAULT 3 CHECK (circuit_breaker_threshold >= 1),
  circuit_breaker_window_minutes              int         NOT NULL DEFAULT 60,
  affected_scope                                text        NOT NULL,  -- 'ONE_FUNCTION'|'ONE_AGENT'|'ONE_JOB' — القسم 8، ممنوعٌ غير ذلك لأي Playbook auto-heal
  mode                                             text        NOT NULL DEFAULT 'SHADOW' CHECK (mode IN ('SHADOW','AUTO','PAUSED','DISABLED')),
  circuit_state                                     text        NOT NULL DEFAULT 'CLOSED' CHECK (circuit_state IN ('CLOSED','OPEN')),
  circuit_opened_at                                   timestamptz,
  requires_human_approval                               boolean     NOT NULL DEFAULT true,  -- MEDIUM/HIGH/CRITICAL دوماً true (القسم 7) — يُنفَّذ في الكود أيضاً كبوّابةٍ مزدوجة
  enabled                                                 boolean     NOT NULL DEFAULT true,
  created_at                                               timestamptz NOT NULL DEFAULT now(),
  updated_at                                                 timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT repair_playbooks_scope_valid CHECK (affected_scope IN ('ONE_FUNCTION','ONE_AGENT','ONE_JOB')),
  -- القسم 7: Phase 3 لا يُنفّذ آلياً غير LOW — أي Playbook MEDIUM/HIGH/CRITICAL
  -- يجب requires_human_approval=true إلزامياً، ولا يجوز أن يكون mode='AUTO'
  -- بلا موافقةٍ بشرية لكل تنفيذٍ فعليٍّ رغم mode (يُنفَّذ في الكود أيضاً).
  CONSTRAINT repair_playbooks_risk_approval_gate CHECK (risk_level = 'LOW' OR requires_human_approval = true)
);

CREATE INDEX IF NOT EXISTS idx_repair_playbooks_pattern ON public.repair_playbooks(incident_pattern);
CREATE INDEX IF NOT EXISTS idx_repair_playbooks_mode     ON public.repair_playbooks(mode);

ALTER TABLE public.repair_playbooks ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.repair_playbooks FROM anon, authenticated;

COMMENT ON TABLE public.repair_playbooks IS
  'سجلّ خطط الإصلاح الذاتي (Phase 3) — repair_steps يشير حصراً لإجراءاتٍ من safe_action_registry، لا خطوةً حرّة. كل الصفوف تُدخَل هنا بوضع mode=SHADOW — تفعيل AUTO فعلٌ بشريٌّ لاحقٌ صريح غير موجودٍ في هذه الهجرة.';

-- ─────────────────────────────────────────────────────────────────────
-- 3) repair_executions — كل محاولة تقييم/تنفيذ Playbook، سواءٌ في وضع
--    SHADOW (تسجيلٌ فقط، بلا تنفيذٍ فعلي) أو AUTO (تنفيذٌ فعلي مستقبلي).
--    القسم 18/19: التحقّق دوماً خطوةٌ منفصلة عن نجاح النداء.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.repair_executions (
  repair_id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  incident_id               uuid        REFERENCES public.ops_incidents(id),
  diagnosis_id               uuid        REFERENCES public.ops_diagnoses(diagnosis_id),
  playbook_id                 text        NOT NULL REFERENCES public.repair_playbooks(playbook_id),
  action_id                     text        REFERENCES public.safe_action_registry(action_id),
  agent_id                       text        REFERENCES public.agent_registry(agent_id),
  correlation_id                   uuid        NOT NULL DEFAULT gen_random_uuid(),
  started_at                         timestamptz NOT NULL DEFAULT now(),
  completed_at                         timestamptz,
  mode                                   text        NOT NULL CHECK (mode IN ('SHADOW','AUTO','DRY_RUN')),
  status                                   text        NOT NULL DEFAULT 'EVALUATING'
                                    CHECK (status IN (
                                      'EVALUATING',            -- بدأ التقييم
                                      'WOULD_AUTO_HEAL',        -- Shadow Mode: كان سيُصلِح لو AUTO — لا تنفيذ فعلي
                                      'DRY_RUN_LOGGED',          -- Dry Run صريح: عرض الخطوة بلا تنفيذ
                                      'PRECONDITION_FAILED',      -- شرطٌ من preconditions لم يتحقّق ⇒ تصعيد
                                      'RISK_BLOCKED',               -- خطورة > LOW بلا موافقةٍ بشرية سارية ⇒ تصعيد لمسار الموافقة القائم
                                      'RATE_LIMITED',                -- تجاوز max_attempts ⇒ تصعيد
                                      'COOLDOWN_ACTIVE',               -- نفس الخطأ ضمن نافذة cooldown ⇒ تصعيد
                                      'CIRCUIT_OPEN',                    -- القاطع مفتوحٌ لهذا الـPlaybook ⇒ تصعيد
                                      'DISABLED',                          -- Playbook/الوكيل/عامّاً معطَّل ⇒ تصعيد
                                      'RUNNING',                             -- AUTO فقط (لا يوجد حالياً — الكود المبني غير مُفعَّل)
                                      'SUCCEEDED',                             -- AUTO فقط
                                      'FAILED',                                 -- فشل التنفيذ نفسه
                                      'VERIFICATION_FAILED',                     -- التنفيذ نجح لكن التحقّق فشل/غير حاسم (القسم 20)
                                      'ESCALATED'                                  -- الحالة النهائية لكل ما سبق عدا WOULD_AUTO_HEAL/SUCCEEDED/DRY_RUN_LOGGED
                                    )),
  attempt_number                           int         NOT NULL DEFAULT 1,
  evidence_snapshot                          jsonb       NOT NULL DEFAULT '{}'::jsonb,   -- نسخةٌ من أدلّة ops_diagnoses وقت اتخاذ القرار (تدقيقٌ لاحق مستقل عن تغيّر الجدول الأصلي)
  preconditions_result                         jsonb       NOT NULL DEFAULT '[]'::jsonb,   -- [{name, passed, detail}]
  execution_result                               jsonb,
  verification_result                              jsonb,
  rollback_result                                    jsonb,
  error                                                 text,
  escalation_reason                                       text,
  blast_radius                                              jsonb       NOT NULL DEFAULT '{}'::jsonb,  -- {scope, target} — القسم 8، يُحسَب قبل أي قرار
  confidence_at_decision                                     int,
  actor                                                        text        NOT NULL DEFAULT 'system_self_healing_engine'  -- يُميَّز دوماً AUTOMATED ACTION في العرض — لا يظهر أبداً كأنه فعلٌ بشري
);

CREATE INDEX IF NOT EXISTS idx_repair_executions_playbook  ON public.repair_executions(playbook_id, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_repair_executions_incident  ON public.repair_executions(incident_id);
CREATE INDEX IF NOT EXISTS idx_repair_executions_status    ON public.repair_executions(status);
CREATE INDEX IF NOT EXISTS idx_repair_executions_correlation ON public.repair_executions(correlation_id);

ALTER TABLE public.repair_executions ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.repair_executions FROM anon, authenticated;

COMMENT ON TABLE public.repair_executions IS
  'كل محاولة تقييم/تنفيذ Playbook (Phase 3) — سجلّ تدقيقٍ كامل (القسم 27): WHO/WHAT/WHY/WHEN/EVIDENCE/PLAYBOOK/ACTION/RISK/RESULT/VERIFICATION/ROLLBACK. actor يبقى مُعلَّماً AUTOMATED ACTION دوماً في الواجهة، لا يظهر أبداً كفعلٍ بشري.';

-- ─────────────────────────────────────────────────────────────────────
-- 4) الـPlaybooks الأولى — 2 فقط، ليس 3 (القسم 3 من المواصفة).
--    السجلّ الحالي لا يحمل سوى إجراءين آمنين حيّين: rerun_monitor_agent
--    وreschedule_daily_summary. مثالٌ ثالثٌ ("إعادة محاولة معالجةٍ
--    حتمية") يستلزم إجراءً آمناً غير موجودٍ اليوم في safe_action_registry
--    — بناؤه هنا يعني اختراع إجراءٍ جديدٍ غير آمنٍ مُثبَتٍ فعلياً، وهذا
--    ممنوعٌ صراحةً بنصّ المواصفة. لذا: Playbook واحدٌ لكل إجراءٍ آمنٍ
--    قائم، بنمط حادثةٍ مختلف — أمينٌ بالعدد كما طُلب حرفياً.
-- ─────────────────────────────────────────────────────────────────────

-- Playbook 1: فشلٌ متكرّرٌ لوكيل مراقبةٍ بنفس رسالة الخطأ (يطابق نمط
-- ruleBasedDiagnose رقم ١ في opsDiagnosis.ts حرفياً) ⇒ إعادة تشغيل الوكيل
-- عبر rerun_monitor_agent (الإجراء الآمن القائم فعلياً منذ Phase 2).
INSERT INTO public.repair_playbooks (
  playbook_id, name, description, incident_pattern, diagnosis_requirements,
  minimum_confidence, risk_level, allowed_agents, allowed_actions, preconditions,
  repair_steps, verification_steps, rollback_strategy, max_attempts, cooldown_minutes,
  circuit_breaker_threshold, circuit_breaker_window_minutes, affected_scope, mode,
  requires_human_approval, enabled
) VALUES (
  'retry_monitor_known_timeout',
  'إعادة تشغيل وكيل مراقبةٍ عند فشلٍ متكرّرٍ معروف',
  'حين يفشل أحد وكلاء المراقبة (credit-monitor / database-capacity-monitor / file-processor-monitor / system-health-check) ٣ مرّاتٍ متتاليةً على الأقل بنفس رسالة الخطأ حرفياً — نمطٌ مطابقٌ لِـruleBasedDiagnose النمط رقم ١ — يُعاد تشغيل نفس الوكيل عبر rerun_monitor_agent فقط، ثم يُتحقَّق أن تشغيلةً جديدةً نجحت فعلاً.',
  'KNOWN_MONITOR_REPEATED_FAILURE',
  jsonb_build_object(
    'min_consecutive_failures', 3,
    'same_error_message_required', true,
    'agent_type_required', 'MONITOR'
  ),
  90, 'LOW',
  jsonb_build_array('credit-monitor','database-capacity-monitor','file-processor-monitor','system-health-check'),
  jsonb_build_array('rerun_monitor_agent'),
  jsonb_build_array(
    'same_function_same_error_pattern',
    'failure_count_at_or_above_threshold',
    'last_known_success_exists',
    'no_similar_incident_open_recently',
    'no_recent_deployment_change',
    'agent_permitted_for_playbook',
    'action_exists_in_registry',
    'action_enabled'
  ),
  jsonb_build_array(jsonb_build_object('action_id','rerun_monitor_agent','params_template', jsonb_build_object('agent_id','{{evidence.agent_id}}'))),
  jsonb_build_array('agent_runs الجديدة بعد إعادة التشغيل تحمل status=SUCCESS — نفس منطق verify() في rerun_monitor_agent (opsActionRegistry.ts)، لا اعتبار نجاح نداء HTTP وحده كافياً'),
  'لا حاجة لتراجعٍ فعلي — rerun_monitor_agent عمليةٌ مثاليةٌ (idempotent): إعادة تشغيل وكيل مراقبةٍ لا تُعدِّل بياناتٍ ولا تُغيِّر حالة نظامٍ دائمة، بنفس rollback_strategy المسجَّلة أصلاً على الإجراء في safe_action_registry.',
  2, 30, 3, 60, 'ONE_AGENT', 'SHADOW', false, true
) ON CONFLICT (playbook_id) DO NOTHING;

-- Playbook 2: فشل جدولة/إرسال الملخّص اليومي المعروف (نفس مسار reschedule
-- الحيّ منذ Phase 2) ⇒ إعادة جدولته للحظةٍ قريبة عبر reschedule_daily_summary.
INSERT INTO public.repair_playbooks (
  playbook_id, name, description, incident_pattern, diagnosis_requirements,
  minimum_confidence, risk_level, allowed_agents, allowed_actions, preconditions,
  repair_steps, verification_steps, rollback_strategy, max_attempts, cooldown_minutes,
  circuit_breaker_threshold, circuit_breaker_window_minutes, affected_scope, mode,
  requires_human_approval, enabled
) VALUES (
  'reschedule_known_daily_summary_failure',
  'إعادة جدولة الملخّص اليومي عند فشلٍ معروفٍ متكرّر',
  'حين يفشل daily-summary ٣ مرّاتٍ متتاليةً على الأقل بنفس رسالة الخطأ (نمطٌ مطابقٌ لِـruleBasedDiagnose النمط رقم ١، مقصورٌ على agent_id=daily-summary فقط) — يُعاد جدولته للحظةٍ قريبة عبر reschedule_daily_summary (الإجراء الآمن القائم فعلياً منذ Phase 2)، لا إعادة تشغيلٍ فورية (daily-summary ليس في KNOWN_MONITOR_AGENTS ضمن rerun_monitor_agent).',
  'KNOWN_DAILY_SUMMARY_REPEATED_FAILURE',
  jsonb_build_object(
    'min_consecutive_failures', 3,
    'same_error_message_required', true,
    'agent_id_required', 'daily-summary'
  ),
  90, 'LOW',
  jsonb_build_array('daily-summary'),
  jsonb_build_array('reschedule_daily_summary'),
  jsonb_build_array(
    'same_function_same_error_pattern',
    'failure_count_at_or_above_threshold',
    'last_known_success_exists',
    'no_similar_incident_open_recently',
    'no_recent_deployment_change',
    'agent_permitted_for_playbook',
    'action_exists_in_registry',
    'action_enabled'
  ),
  jsonb_build_array(jsonb_build_object('action_id','reschedule_daily_summary','params_template', jsonb_build_object())),
  jsonb_build_array('قيمة agent_schedules بعد الكتابة تطابق القيمة المطلوبة حرفياً — نفس منطق verify() في reschedule_daily_summary (opsActionRegistry.ts)'),
  'قابلٌ للتراجع الكامل: القيمة السابقة لِـ(scheduled_hour, scheduled_minute) تُحفَظ في execution_result.previous وقت تنفيذ reschedule_daily_summary (opsActionRegistry.ts) — يمكن للمشرف إعادة كتابتها يدوياً من لوحة التشغيل عند الحاجة.',
  2, 30, 3, 60, 'ONE_JOB', 'SHADOW', false, true
) ON CONFLICT (playbook_id) DO NOTHING;

-- ─────────────────────────────────────────────────────────────────────
-- 5) توسيع agent_registry.permission_level المرجعي: لا تعديل على أي صفّ
--    قائم هنا (القسم "أهم قاعدة": لا يُرفَع أي وكيلٍ إلى LEVEL 4 كاملاً).
--    الملاحظة موثَّقةٌ في تعليق الجدول فقط، لا تنفيذٌ لأي UPDATE.
-- ─────────────────────────────────────────────────────────────────────
COMMENT ON COLUMN public.agent_registry.autonomy_level IS
  'مستوى استقلالية الوكيل العام (Phase 1). Phase 3 لا يرفع أي صفٍّ هنا إلى LEVEL 4 — LEVEL 4 (الإصلاح الذاتي) خاصٌّ بـPlaybook محدَّد في repair_playbooks، لا بوكيلٍ كامل. agent_id الظاهر في repair_playbooks.allowed_agents لا يعني تغييراً في هذا العمود.';
