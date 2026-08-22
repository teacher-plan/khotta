DO $$
DECLARE v text;
BEGIN
  SELECT string_agg(
    format('policy=%s cmd=%s qual=%s check=%s', policyname, cmd, qual, with_check), E'\n'
  ) INTO v
  FROM pg_policies WHERE schemaname='storage' AND tablename='objects' AND policyname LIKE 'userfiles%';
  RAISE EXCEPTION 'PROBE_POLICIES | %', coalesce(v,'NONE');
END $$;
