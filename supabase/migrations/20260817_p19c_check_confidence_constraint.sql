DO $$
DECLARE v_def text;
BEGIN
  SELECT pg_get_constraintdef(oid) INTO v_def FROM pg_constraint WHERE conname='ops_incidents_confidence_check';
  RAISE EXCEPTION 'P19C_CONFIDENCE_CHECK | def=%', v_def;
END $$;
