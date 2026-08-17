-- ════════════════════════════════════════════════════════════════════
-- KHOTTA Autonomous Operations 2.0 — Phase 3.2
-- deployment_log: سجلٌّ بسيطٌ لعمليات نشر الدوال، يكتبه deploy-functions.yml
-- نفسه بعد نجاح النشر فعلياً، عبر Management API — نفس آلية
-- apply-migrations.yml بالضبط، ونفس السرّ الموجود أصلاً (SUPABASE_ACCESS_TOKEN)،
-- بلا أي سرٍّ أو صلاحيةٍ جديدة (القسم 4 من مواصفة Phase 3.2).
--
-- ملاحظة صادقة: `supabase functions deploy` (بلا اسم) ينشر كل الدوال دفعةً
-- واحدة، فلا معنى حقيقي لتسجيل اسم دالّةٍ بعينها لكل عملية — function_name
-- يُسجَّل 'ALL' دوماً، موثَّقٌ صراحةً بدل الادّعاء بدقّةٍ لا تتوفّر.
-- ════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.deployment_log (
  id             bigserial   PRIMARY KEY,
  function_name  text        NOT NULL DEFAULT 'ALL',
  commit_sha     text        NOT NULL,
  workflow_run_id text,
  deployed_at    timestamptz NOT NULL DEFAULT now(),
  created_at     timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_deployment_log_deployed_at ON public.deployment_log (deployed_at DESC);

ALTER TABLE public.deployment_log ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.deployment_log FROM anon, authenticated;

COMMENT ON TABLE public.deployment_log IS
  'سجلّ نشر الدوال — يكتبه GitHub Actions (deploy-functions.yml) عبر Management API فقط، لا PostgREST. يُستعمَل في checkPreconditions (opsPlaybooks.ts) لشرط no_recent_deployment_change الحقيقي بدل الافتراض الدائم بعدم التوفّر.';
