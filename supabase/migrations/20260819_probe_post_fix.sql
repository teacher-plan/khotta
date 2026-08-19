DO $$
DECLARE v text;
DECLARE uid uuid;
BEGIN
  SELECT id INTO uid FROM public.cycle1_profiles WHERE lower(email)=lower('X@y.com');
  SELECT format(
    'usage_now=%s | her_last_cost=%s | any_recent_cost_5min=%s | recent_cost_sample=%s',
    (SELECT string_agg(kind||':'||count,', ') FROM public.ai_usage WHERE user_id=uid AND month=to_char(now(),'YYYY-MM')),
    (SELECT format('%s|%s|%s|model=%s|cost=%s',created_at,function_name,kind,model,cost_usd) FROM public.ai_cost_log WHERE user_id=uid ORDER BY created_at DESC LIMIT 1),
    (SELECT count(*) FROM public.ai_cost_log WHERE created_at > now() - interval '30 minutes')::text,
    (SELECT string_agg(format('[%s] %s %s cost=%s',created_at,function_name,kind,cost_usd),E'\n' ORDER BY created_at DESC) FROM (SELECT * FROM public.ai_cost_log ORDER BY created_at DESC LIMIT 8) t)
  ) INTO v;
  RAISE EXCEPTION 'PROBE | %', v;
END $$;
