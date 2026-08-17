-- ════════════════════════════════════════════════════════════════════
-- KHOTTA Autonomous Operations 2.0 — Phase 3.5-B: جدولة بوّابة التنفيذ
-- الآلي (Scheduler & Gateway Integration) — SHADOW فقط.
--
-- هذه الهجرة تُنشئ (1) جدول scheduler_runs لتسجيل كل دورة تشغيلٍ للجدولة
-- الجديدة، و(2) مهمّة pg_cron باسم agent-autonomous-scheduler تستدعي
-- الدالّة الجديدة autonomous-scheduler كل ٥ دقائق، بنفس آلية call_agent()
-- القائمة فعلياً منذ P0/٢ (20260816_p0_agent_cron_service_key.sql) —
-- لا آلية جديدة، لا مفتاحٌ ظاهرٌ في نصّ الجدولة، لا نقطة نهايةٍ عامّة جديدة.
--
-- ⚠️ لا تفعيلٌ لأي تنفيذٍ آليٍّ حقيقي هنا: كلا الـPlaybook يبقى mode=SHADOW
-- (لم يُلمَس)، وself_healing_controls.self_healing_enabled يبقى كما هو
-- (لم يُلمَس). الدالّة الجديدة تستدعي executeAutonomous() من
-- autonomousGateway.ts فقط، وGate 4 هناك يمنع بنيوياً أي تنفيذٍ فعلي ما لم
-- يكن mode='AUTO' — لا صفّ اليوم يحمل هذه القيمة.
-- ════════════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────────
-- 1) scheduler_runs — سجلّ تدقيقٍ لكل دورة تشغيلٍ للجدولة (لا يُكرَّر
--    داخله ما يُسجَّله repair_executions أصلاً — فقط عدّادات الدورة نفسها).
-- ─────────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS public.scheduler_runs (
  run_id              uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  started_at          timestamptz NOT NULL DEFAULT now(),
  completed_at        timestamptz,
  status              text        CHECK (status IN ('RUNNING', 'COMPLETED', 'FAILED')),
  incidents_scanned   int         DEFAULT 0,
  incidents_claimed   int         DEFAULT 0,
  incidents_evaluated int         DEFAULT 0,
  shadow_would_repair int         DEFAULT 0,
  escalated           int         DEFAULT 0,
  errors              int         DEFAULT 0,
  error_detail        jsonb,
  duration_ms         int
);

CREATE INDEX IF NOT EXISTS idx_scheduler_runs_started_at ON public.scheduler_runs(started_at DESC);

ALTER TABLE public.scheduler_runs ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.scheduler_runs FROM anon, authenticated;

COMMENT ON TABLE public.scheduler_runs IS
  'سجلّ تدقيقٍ لكل دورة تشغيلٍ لـautonomous-scheduler (Phase 3.5-B) — عدّادات الدورة (مسح/ادّعاء/تقييم/أخطاء)، لا تفاصيل كل حادثة (تلك في repair_executions أصلاً). لا كتابة إلا من autonomous-scheduler/index.ts بمفتاح الخدمة.';

-- ─────────────────────────────────────────────────────────────────────
-- 2) الجدولة: نفس نمط call_agent() القائم فعلياً — المفتاح من الخزانة،
--    لا يظهر في نصّ الجدولة، ونفس اسم الدالّة يُستخدَم لتوجيه net.http_post
--    إلى /functions/v1/<اسم الدالّة>. اسم مهمّة cron.job وفق الاصطلاح
--    القائم agent-* (system-health-check ⇒ agent-health-check، هنا
--    autonomous-scheduler ⇒ agent-autonomous-scheduler).
-- ─────────────────────────────────────────────────────────────────────
SELECT cron.schedule(
  'agent-autonomous-scheduler',
  '*/5 * * * *',
  $$SELECT public.call_agent('autonomous-scheduler')$$
);

-- تحقّق: SELECT jobname, schedule, command FROM cron.job WHERE jobname = 'agent-autonomous-scheduler';
--        يجب أن يظهر صفٌّ واحد، وألّا يحتوي command أي مفتاح.
