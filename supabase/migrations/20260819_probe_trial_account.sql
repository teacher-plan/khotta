DO $$
DECLARE v text;
DECLARE uid uuid;
BEGIN
  SELECT id INTO uid FROM public.cycle1_profiles WHERE lower(email)=lower('X@y.com');
  SELECT format(
    'uid=%s | allowed=%s | c1prof_updated=%s | banned=%s | gen_enabled=%s | usage=%s | last_cost=%s',
    uid::text,
    (SELECT format('email=%s cycle=%s added=%s expires=%s',email,cycle,added_at,expires_at) FROM public.allowed_emails WHERE lower(email)=lower('X@y.com')),
    (SELECT updated_at::text FROM public.cycle1_profiles WHERE id=uid),
    (SELECT EXISTS(SELECT 1 FROM public.banned_users WHERE user_id=uid))::text,
    (SELECT value FROM public.ai_settings WHERE key='generator_enabled'),
    (SELECT string_agg(kind||':'||count,', ') FROM public.ai_usage WHERE user_id=uid AND month=to_char(now(),'YYYY-MM')),
    (SELECT format('%s | %s | %s | model=%s | cost=%s',created_at,function_name,kind,model,cost_usd) FROM public.ai_cost_log WHERE user_id=uid ORDER BY created_at DESC LIMIT 1)
  ) INTO v;
  RAISE EXCEPTION 'PROBE | %', v;
END $$;
