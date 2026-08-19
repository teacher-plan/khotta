DO $$
DECLARE v text;
BEGIN
  SELECT format('quota_text=%s | quota_img=%s | quota_search=%s',
    (SELECT value FROM public.ai_settings WHERE key='quota_text'),
    (SELECT value FROM public.ai_settings WHERE key='quota_img'),
    (SELECT value FROM public.ai_settings WHERE key='quota_search'))
  INTO v;
  RAISE EXCEPTION 'PROBE | %', v;
END $$;
