DO $$
DECLARE v text;
BEGIN
  SELECT string_agg(conname||':'||contype::text, ', ') INTO v
  FROM pg_constraint WHERE conrelid = 'public.ai_settings'::regclass;
  RAISE EXCEPTION 'PROBE_AI_SETTINGS_CONSTRAINTS | %', coalesce(v,'NONE');
END $$;
