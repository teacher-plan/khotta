DO $$
DECLARE v text;
BEGIN
  SELECT pg_get_functiondef(oid) INTO v
  FROM pg_proc
  WHERE proname = 'register_teacher'
  LIMIT 1;
  RAISE EXCEPTION 'PROBE_FN | %', COALESCE(v, 'NOT_FOUND');
END $$;
