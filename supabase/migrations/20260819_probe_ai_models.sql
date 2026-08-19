DO $$
DECLARE v text;
BEGIN
  SELECT string_agg(key||'='||value, ', ' ORDER BY key)
  INTO v FROM public.ai_settings WHERE key LIKE 'model_%' OR key='ai_model';
  RAISE EXCEPTION 'PROBE | %', v;
END $$;
