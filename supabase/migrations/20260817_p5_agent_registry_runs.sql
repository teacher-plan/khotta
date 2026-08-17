-- ════════════════════════════════════════════════════════════════════
-- KHOTTA Autonomous Operations 2.0 — Phase 1
-- سجلّ الوكلاء (Agent Registry) + دفتر التشغيلات (Agent Runs) +
-- توسيعٌ إضافيّ لِـ ops_incidents (نموذج حوادث موحَّد) + عمود correlation
-- في agent_logs (لربط سجلّات النشاط بتشغيلة واحدة).
--
-- نهجٌ إضافيّ بالكامل: لا حذف ولا إعادة تسمية لأي عمود/قيمة قائمة.
-- agent_schedules وagent_logs وagent_messages وops_incidents تبقى كما هي
-- تُكتَب إليها بلا أي تغيير — هذا الملف يُضيف بجانبها فقط.
-- ════════════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────────
-- 1) agent_registry — سجلّ مركزي لكل وكيلٍ حقيقي في المشروع (لا مفهوم
--    جديد يوازي agent_schedules؛ agent_schedules يبقى مصدر «الجدولة
--    القابلة للتعديل من تلغرام» كما هو، وagent_registry يضيف فوقه معلومات
--    الهوية/النوع/الصلاحيات/القدرة الذاتية اللازمة للوحة الإدارة وCopilot،
--    وهي معلوماتٌ لم يكن لها مكان في agent_schedules أصلاً).
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.agent_registry (
  agent_id          text        PRIMARY KEY,   -- يطابق اسم الدالة الحقيقي (function slug)
  display_name      text        NOT NULL,
  description       text        NOT NULL,
  agent_type        text        NOT NULL CHECK (agent_type IN ('MONITOR','NOTIFIER','AI_ANALYST','DISPATCHER','ORCHESTRATOR')),
  status            text        NOT NULL DEFAULT 'ACTIVE' CHECK (status IN ('ACTIVE','DISABLED','DEPRECATED')),
  version           text        NOT NULL DEFAULT '1.0.0',
  schedule_cron     text,        -- تعبير cron الفعلي إن كان مجدولاً، NULL إن كان عند-الطلب فقط
  trigger_kind      text        NOT NULL CHECK (trigger_kind IN ('CRON','DB_WEBHOOK','ON_DEMAND','LIVE_WEBHOOK')),
  autonomy_level    int         NOT NULL CHECK (autonomy_level BETWEEN 0 AND 5),
  permission_level  text        NOT NULL CHECK (permission_level IN
                      ('READ_ONLY','READ_ANALYZE','SAFE_ACTION','WRITE_LIMITED',
                       'WRITE_PRODUCTION','ADMIN_ACTION','AUTONOMOUS_REPAIR')),
  allowed_actions   jsonb       NOT NULL DEFAULT '[]'::jsonb, -- allowlist أسماء إجراءات صريحة
  notes             text,        -- فجوات/تحذيرات معروفة (مثال: بيانات وهمية، أزرار stub)
  created_at        timestamptz NOT NULL DEFAULT now(),
  updated_at        timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_agent_registry_type   ON public.agent_registry(agent_type);
CREATE INDEX IF NOT EXISTS idx_agent_registry_status  ON public.agent_registry(status);

ALTER TABLE public.agent_registry ENABLE ROW LEVEL SECURITY;
-- داخليٌّ — كنمط ops_incidents: لا سياسة مباشرة لـanon/authenticated؛
-- القراءة الإدارية حصراً عبر ops-analyze/ops-copilot (is_app_admin على الخادم).
REVOKE ALL ON public.agent_registry FROM anon, authenticated;

COMMENT ON TABLE public.agent_registry IS
  'سجلّ مركزي لكل الوكلاء الحقيقيين (Edge Functions المجدولة/شبه المستقلة) — الهوية والنوع والصلاحيات ومستوى الاستقلالية. داخليٌّ: service_role فقط، القراءة الإدارية عبر ops-analyze/ops-copilot.';

-- ─────────────────────────────────────────────────────────────────────
-- 2) agent_runs — دفترُ تشغيلاتٍ موحَّد لكل تشغيلة وكيل (جديد بالكامل —
--    لا مكافئ له في الجداول القائمة: agent_logs سجلٌّ نصّيٌّ بسيط بلا
--    started_at/completed_at/duration/trigger/records_*/cost موحَّدة).
--    الوكلاء القائمة تستمر بالكتابة في agent_logs/agent_messages كما هي؛
--    هذا الجدول يُضاف بجانبها (انظر تعليمات instrumentation في التقرير).
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.agent_runs (
  run_id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_id          text        NOT NULL REFERENCES public.agent_registry(agent_id),
  correlation_id    uuid        NOT NULL DEFAULT gen_random_uuid(),
  started_at        timestamptz NOT NULL DEFAULT now(),
  completed_at      timestamptz,
  duration_ms       int,
  status            text        NOT NULL DEFAULT 'RUNNING' CHECK (status IN ('RUNNING','SUCCESS','FAILED','PARTIAL')),
  trigger           text        NOT NULL DEFAULT 'CRON' CHECK (trigger IN ('CRON','MANUAL','WEBHOOK','ON_DEMAND')),
  result_summary    text,
  error             text,
  records_read      int,
  records_written   int,
  actions_taken     jsonb       DEFAULT '[]'::jsonb,
  cost_usd          numeric,
  extra             jsonb        -- بياناتٌ إضافية خاصة بالوكيل (مثال: حجم القاعدة لـdatabase-capacity-monitor)
);

CREATE INDEX IF NOT EXISTS idx_agent_runs_agent_started ON public.agent_runs(agent_id, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_agent_runs_status        ON public.agent_runs(status);
CREATE INDEX IF NOT EXISTS idx_agent_runs_correlation    ON public.agent_runs(correlation_id);

ALTER TABLE public.agent_runs ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.agent_runs FROM anon, authenticated;

COMMENT ON TABLE public.agent_runs IS
  'دفتر تشغيلاتٍ موحَّد لكل الوكلاء — بداية/نهاية/حالة/نتيجة/تكلفة كل تشغيلة. إضافيّ بجانب agent_logs، لا بديل عنه.';

-- ─────────────────────────────────────────────────────────────────────
-- 3) agent_logs: عمود correlation_id إضافي — لربط سجلّات agent_logs
--    القائمة (النصّية) بتشغيلة agent_runs محدَّدة، فيصير بالإمكان بناء
--    خط-زمن (timeline) لكل تشغيلة. NULL افتراضياً فلا يكسر أي كتابة قائمة.
-- ─────────────────────────────────────────────────────────────────────
ALTER TABLE public.agent_logs ADD COLUMN IF NOT EXISTS correlation_id uuid;
ALTER TABLE public.agent_logs ADD COLUMN IF NOT EXISTS run_id uuid;
CREATE INDEX IF NOT EXISTS idx_agent_logs_correlation ON public.agent_logs(correlation_id);

COMMENT ON COLUMN public.agent_logs.correlation_id IS
  'يربط سجلّ agent_logs بتشغيلة agent_runs (correlation_id) — إضافيٌّ، NULL على السجلّات القديمة والوكلاء غير المُحدَّثة بعد.';

-- ─────────────────────────────────────────────────────────────────────
-- 4) ops_incidents — توسيعٌ إضافي (لا جدول جديد): الحقول الناقصة من
--    مواصفة النموذج الموحَّد + قيم status جديدة تُضاف لا تستبدل القديمة.
-- ─────────────────────────────────────────────────────────────────────
ALTER TABLE public.ops_incidents ADD COLUMN IF NOT EXISTS source_agent text;
ALTER TABLE public.ops_incidents ADD COLUMN IF NOT EXISTS related_run_id uuid;
ALTER TABLE public.ops_incidents ADD COLUMN IF NOT EXISTS correlation_id uuid;
ALTER TABLE public.ops_incidents ADD COLUMN IF NOT EXISTS suggested_action text;
ALTER TABLE public.ops_incidents ADD COLUMN IF NOT EXISTS action_taken text;
ALTER TABLE public.ops_incidents ADD COLUMN IF NOT EXISTS resolution text;
ALTER TABLE public.ops_incidents ADD COLUMN IF NOT EXISTS requires_human_attention boolean NOT NULL DEFAULT false;

-- توسيع enum الحالة إضافياً: القيم الجديدة تُضاف، والقديمة (DETECTED,
-- INVESTIGATING مذكورةٌ أصلاً, IDENTIFIED, RECOMMENDATION, RESOLVED) تبقى
-- صالحة بلا أي إعادة تسمية أو حذف — تحديثٌ تراكمي على القيد فقط.
ALTER TABLE public.ops_incidents DROP CONSTRAINT IF EXISTS ops_incidents_status_check;
ALTER TABLE public.ops_incidents ADD CONSTRAINT ops_incidents_status_check
  CHECK (status IN (
    'DETECTED','INVESTIGATING','IDENTIFIED','RECOMMENDATION','RESOLVED',
    'ACTION_REQUIRED','FAILED','IGNORED'
  ));

COMMENT ON COLUMN public.ops_incidents.source_agent IS 'agent_id (يطابق agent_registry) الذي اكتشف الحادثة — إضافي، NULL على الحوادث القديمة قبل هذا الحقل.';
COMMENT ON COLUMN public.ops_incidents.requires_human_attention IS 'علمٌ صريح: هل تتطلب هذه الحادثة تدخّلاً بشرياً؟ يُستعمل في سياسة التصعيد (Escalation)، لا يُشغِّل أي إجراءٍ آلي.';

-- ─────────────────────────────────────────────────────────────────────
-- 5) db_capacity_history — تاريخٌ خفيف مخصَّص لقياسات حجم القاعدة، منفصلٌ
--    عن agent_runs.extra (الذي يبقى بياناتٍ عامة لكل تشغيلة) لأن استعلامات
--    معدّل النمو/التوقّع تحتاج فرزاً وفلترةً زمنية متكرّرة على قياس رقمي
--    واحد فقط — تخزينه في عمودٍ عددي مخصَّص أبسط وأسرع من نبش jsonb عام
--    في كل استعلام. كل تشغيلة لِـ database-capacity-monitor تُدرج صفاً هنا.
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.db_capacity_history (
  id              uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id          uuid        REFERENCES public.agent_runs(run_id),
  measured_at     timestamptz NOT NULL DEFAULT now(),
  size_mb         numeric     NOT NULL,
  top_tables      jsonb,       -- لقطة أكبر ١٠ جداول وقت القياس
  limit_mb        numeric,     -- NULL إن كان الحدّ غير مؤكَّد (NOT VERIFIED)
  usage_percent   numeric      -- NULL إن تعذّر الحساب (الحدّ غير معروف)
);

CREATE INDEX IF NOT EXISTS idx_db_capacity_history_measured_at ON public.db_capacity_history(measured_at DESC);

ALTER TABLE public.db_capacity_history ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.db_capacity_history FROM anon, authenticated;

COMMENT ON TABLE public.db_capacity_history IS
  'تاريخٌ خفيف لقياسات حجم قاعدة البيانات — يُغذّى من تشغيلات database-capacity-monitor فقط. المصدر الوحيد لحساب معدّل النمو والتوقّع؛ فارغٌ أو قليل الصفوف أول أيام التشغيل → INSUFFICIENT DATA، لا رقم مُختلَق.';

-- ─────────────────────────────────────────────────────────────────────
-- 6) RPC: database_top_tables — أكبر الجداول تخزيناً (بيانات + فهارس)،
--    قراءةٌ صرفة من كتالوج postgres (pg_class/pg_namespace)، لا SQL حرّ.
-- ─────────────────────────────────────────────────────────────────────
CREATE OR REPLACE FUNCTION public.database_top_tables(p_limit int DEFAULT 10)
RETURNS TABLE (table_name text, total_size_bytes bigint, total_size_mb numeric, row_estimate bigint)
LANGUAGE sql
SECURITY DEFINER
SET search_path = public, pg_catalog
AS $$
  SELECT
    c.relname::text AS table_name,
    pg_total_relation_size(c.oid) AS total_size_bytes,
    ROUND(pg_total_relation_size(c.oid) / 1024.0 / 1024.0, 2) AS total_size_mb,
    GREATEST(c.reltuples, 0)::bigint AS row_estimate
  FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE c.relkind = 'r' AND n.nspname = 'public'
  ORDER BY pg_total_relation_size(c.oid) DESC
  LIMIT GREATEST(LEAST(p_limit, 50), 1);
$$;

COMMENT ON FUNCTION public.database_top_tables(int) IS
  'أكبر جداول public تخزيناً (بيانات+فهارس) عبر pg_class — قراءةٌ صرفة، لا SQL حرّ. تُستخدم من database-capacity-monitor.';

REVOKE ALL ON FUNCTION public.database_top_tables(int) FROM PUBLIC;
REVOKE ALL ON FUNCTION public.database_top_tables(int) FROM anon;
REVOKE ALL ON FUNCTION public.database_top_tables(int) FROM authenticated;
GRANT EXECUTE ON FUNCTION public.database_top_tables(int) TO service_role;

-- ─────────────────────────────────────────────────────────────────────
-- 7) تعبئة agent_registry بصفوف الوكلاء الحقيقيين — القيم مبنيّةٌ على
--    القراءة الفعلية للكود (raw_evidence: التقرير المرافق، القسم 3).
--    autonomy/permission = الحد الأدنى الذي يثبته الكود فعلاً، بلا هامشٍ
--    لمراحل قادمة.
-- ─────────────────────────────────────────────────────────────────────
INSERT INTO public.agent_registry
  (agent_id, display_name, description, agent_type, status, version,
   schedule_cron, trigger_kind, autonomy_level, permission_level, allowed_actions, notes)
VALUES
  ('system-health-check', 'فحص صحة النظام', 'يفحص مكوّنات النظام كل 5 دقائق، ويكتشف الحوادث ويُزيل تكرارها في ops_incidents (P0–P3).',
   'MONITOR', 'ACTIVE', '1.0.0', '*/5 * * * *', 'CRON', 1, 'READ_ANALYZE',
   '["read_health_metrics","write_ops_incidents","send_telegram_alert"]'::jsonb,
   'العمود الفقري لرصد الحوادث؛ لا يصلح شيئاً، اكتشاف وتنبيه فقط.'),

  ('credit-monitor', 'مراقب رصيد الذكاء الاصطناعي', 'يفحص رصيد OpenRouter كل 6 ساعات وينبّه عبر تلغرام عند اقترابه من النفاد.',
   'MONITOR', 'ACTIVE', '1.0.0', '0 */6 * * *', 'CRON', 1, 'READ_ONLY',
   '["read_credit_balance","send_telegram_alert"]'::jsonb,
   'قراءة وتنبيه فقط؛ لا يشتري رصيداً ولا يبدّل مزوّداً.'),

  ('file-processor-monitor', 'مراقب معالجة الملفات', 'يفحص كل 30 دقيقة الملفات العالقة/الفاشلة في المعالجة وينبّه عبر تلغرام.',
   'MONITOR', 'ACTIVE', '1.0.0', '*/30 * * * *', 'CRON', 1, 'READ_ONLY',
   '["read_file_processing_status","send_telegram_alert"]'::jsonb,
   'زر "إعادة محاولة" في تلغرام PRESENT BUT NOT ACTIVE — لا تنفيذ فعلي خلفه (لم يُصلَح هنا، خارج نطاق Phase 1).'),

  ('daily-summary', 'الملخص اليومي', 'يرسل ملخصاً يومياً للمدير عبر تلغرام (تسجيلات/ملفات/تحليلات).',
   'NOTIFIER', 'ACTIVE', '1.0.0', '0 13 * * *', 'CRON', 1, 'READ_ONLY',
   '["read_summary_data","send_telegram_summary","update_own_schedule"]'::jsonb,
   'تحذير معروف: يتضمّن حقولاً تحليلية ثابتة (peak hours/avg score) غير حقيقية — لم يُصلَح هنا، خارج نطاق Phase 1، مذكورٌ في التقرير.'),

  ('registration-notifier', 'مُنبّه التسجيل', 'يُشعر المدير فوراً بحجز معلّمة جديدة عبر تلغرام (بوت التسجيل) مع رابط واتساب جاهز.',
   'NOTIFIER', 'ACTIVE', '1.0.0', NULL, 'DB_WEBHOOK', 1, 'WRITE_LIMITED',
   '["read_pre_registrations","mark_notified","send_telegram_message"]'::jsonb,
   'مسار الفوري (Webhook) مؤكَّد؛ مسار المسح الاحتياطي (sweep) لا جدولة pg_cron مؤكَّدة له — NOT VERIFIED، لم يُغيَّر هنا.'),

  ('ops-analyze', 'محلّل العمليات', 'تحليلٌ آنيّ (نداء LLM واحد أو قواعد حتمية) لحالة النظام/التكلفة عند طلب المدير من لوحة الإدارة.',
   'AI_ANALYST', 'ACTIVE', '1.0.0', NULL, 'ON_DEMAND', 1, 'READ_ANALYZE',
   '["read_ops_tools","call_llm_once","log_ai_cost"]'::jsonb,
   'توصية فقط، لا تنفيذ — موثَّق صراحةً في system prompt الكود. لا حلقة agentic.'),

  ('ops-copilot', 'مساعد Copilot', 'واجهة أسئلة حرة للمدير عن حالة المنصة، مبنية على نفس أدوات القراءة.',
   'AI_ANALYST', 'ACTIVE', '1.0.0', NULL, 'ON_DEMAND', 1, 'READ_ANALYZE',
   '["read_ops_tools","call_llm_once","log_ai_cost"]'::jsonb,
   'يرفض صراحةً مفتاح الخدمة — جلسة مدير بشري فقط. بلا كتابة إطلاقاً عدا ai_cost_log.'),

  ('telegram-webhook', 'موزّع أزرار تلغرام', 'يستقبل ضغطات أزرار Telegram من كلا البوتين وينفّذ الإجراء المطابق إن وُجد.',
   'DISPATCHER', 'ACTIVE', '1.0.0', NULL, 'LIVE_WEBHOOK', 0, 'WRITE_LIMITED',
   '["update_agent_schedule","mark_welcomed","mark_payment_followup"]'::jsonb,
   'أغلب الأزرار PRESENT BUT NOT ACTIVE (ردود وهمية/stub). ⚠️ لا تحقّق X-Telegram-Bot-Api-Secret-Token — SECURITY BLOCKER موثَّق في التقرير، لم يُعدَّل هنا.'),

  ('database-capacity-monitor', 'مراقب سعة قاعدة البيانات', 'قياسٌ دوري لحجم قاعدة البيانات وأكبر الجداول استهلاكاً، بلا ذكاء اصطناعي — SQL صرف للقراءة فقط.',
   'MONITOR', 'ACTIVE', '1.0.0', '0 */6 * * *', 'CRON', 1, 'READ_ONLY',
   '["read_database_size","read_top_tables","write_capacity_history","send_telegram_alert"]'::jsonb,
   'جديد في Phase 1. الحدّ الأقصى للخطة (plan limit) NOT VERIFIED — لا رقم مُختلَق؛ عتبات 70/80/90/95/98% افتراضية بانتظار تأكيد الحدّ الفعلي.')
ON CONFLICT (agent_id) DO NOTHING;
