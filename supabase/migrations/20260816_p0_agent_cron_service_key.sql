-- ════════════════════════════════════════════════════════════════════
-- P0/٢ (مُكمِّلٌ لازم) — تحويل جدولة الوكلاء إلى مفتاح الخدمة
--
-- أُقفلت أربع دوالٍّ إدارية على service_role (credit-monitor و
-- daily-summary و file-processor-monitor و system-health-check).
-- لكنّ الوثائق (AGENTS_SETUP.md:56) تجدولها بـ ANON_KEY — فبلا هذا الملف
-- سيُقفَل الباب على الوكلاء أنفسهم وتتوقّف المراقبة بصمت.
--
-- الحلُّ يعيد استعمال نمط المشروع نفسه لا نظاماً جديداً: المفتاح يُقرأ من
-- الخزانة (vault) كما في notify_new_registration، فلا يظهر في تعريف
-- الجدولة ولا في cron.job حيث يقرأه أيُّ من يملك اطّلاعاً على القاعدة.
--
-- ⚠️ يتطلّب أن يكون سرّ 'service_role_key' موجوداً في الخزانة — وهو
--    موجودٌ أصلاً منذ إعداد registration-notifier.
-- ════════════════════════════════════════════════════════════════════

CREATE EXTENSION IF NOT EXISTS pg_cron;
CREATE EXTENSION IF NOT EXISTS pg_net;

-- نداءٌ موحَّد لأي وكيل: اسمُ الدالة وحده، والمفتاح يأتي من الخزانة.
CREATE OR REPLACE FUNCTION public.call_agent(p_agent TEXT)
RETURNS void
LANGUAGE plpgsql
SECURITY DEFINER               -- ليقرأ الخزانة، والقارئ العادي لا يملك ذلك
SET search_path = public, extensions, vault
AS $$
DECLARE
  v_key TEXT;
BEGIN
  SELECT decrypted_secret INTO v_key
    FROM vault.decrypted_secrets WHERE name = 'service_role_key';

  IF v_key IS NULL THEN
    RAISE WARNING 'call_agent(%): مفتاح الخدمة غير موجود في الخزانة', p_agent;
    RETURN;
  END IF;

  PERFORM net.http_post(
    url     := 'https://mkdsnnfkkdwdkywnwnjh.supabase.co/functions/v1/' || p_agent,
    headers := jsonb_build_object(
                 'Content-Type',  'application/json',
                 'Authorization', 'Bearer ' || v_key),
    body    := '{}'::jsonb,
    timeout_milliseconds := 10000
  );
EXCEPTION WHEN OTHERS THEN
  -- عطلُ وكيلٍ لا يجوز أن يُفشل مهمّة cron كاملةً ويوقف بقيّة الجدولة.
  RAISE WARNING 'call_agent(%) فشل: %', p_agent, SQLERRM;
END;
$$;

-- الدالة تقرأ الخزانة، فلا تُترك مستدعاةً من المتصفّح.
REVOKE ALL ON FUNCTION public.call_agent(TEXT) FROM PUBLIC, anon, authenticated;

-- إعادة الجدولة: تُلغى القديمة (التي تحمل ANON_KEY) ثم تُنشأ بالنداء الجديد.
-- الأسماء هي المذكورة في AGENTS_SETUP.md؛ ما لم يكن موجوداً يُتجاوز بلا خطأ.
DO $$
DECLARE
  j RECORD;
BEGIN
  FOR j IN
    SELECT jobname FROM cron.job
     WHERE command ILIKE '%functions/v1/daily-summary%'
        OR command ILIKE '%functions/v1/credit-monitor%'
        OR command ILIKE '%functions/v1/file-processor-monitor%'
        OR command ILIKE '%functions/v1/system-health-check%'
  LOOP
    PERFORM cron.unschedule(j.jobname);
    RAISE NOTICE 'أُلغيت الجدولة القديمة: %', j.jobname;
  END LOOP;
END;
$$;

-- الجدولة بتوقيت UTC. مسقط = UTC+4 بلا توقيت صيفي.
SELECT cron.schedule('agent-daily-summary',   '0 13 * * *',  $$SELECT public.call_agent('daily-summary')$$);          -- ٥ مساءً مسقط
SELECT cron.schedule('agent-credit-monitor',  '0 */6 * * *', $$SELECT public.call_agent('credit-monitor')$$);
SELECT cron.schedule('agent-file-processor',  '*/30 * * * *',$$SELECT public.call_agent('file-processor-monitor')$$);
SELECT cron.schedule('agent-health-check',    '*/5 * * * *', $$SELECT public.call_agent('system-health-check')$$);

-- تحقّق: يجب أن تظهر أربع مهامّ، وألّا يحتوي أيُّ أمرٍ منها على مفتاح.
-- SELECT jobname, schedule, command FROM cron.job WHERE jobname LIKE 'agent-%';
