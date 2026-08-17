-- تحقّقٌ حيٌّ بلا أثرٍ جانبي: وقت آخر نشرٍ حقيقي وعدد الدقائق المتبقية
-- حتى تنتهي نافذة cooldown (30 دقيقة) لكلا الـPlaybook.
DO $$
DECLARE
  v_last timestamptz;
  v_minutes numeric;
BEGIN
  SELECT deployed_at INTO v_last FROM public.deployment_log ORDER BY deployed_at DESC LIMIT 1;
  v_minutes := extract(epoch FROM (now() - v_last)) / 60;
  RAISE EXCEPTION 'DEPLOY_TIME_CHECK | last_deploy_at: % | now: % | minutes_elapsed: % | minutes_remaining_for_30min_cooldown: %',
    v_last, now(), round(v_minutes,2), greatest(0, round(30 - v_minutes,2));
END $$;
