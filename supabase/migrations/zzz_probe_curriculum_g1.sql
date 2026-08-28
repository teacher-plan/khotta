DO $$
DECLARE v text;
BEGIN
  SELECT string_agg(subject || '~' || unit || '~' || lesson, E'\n' ORDER BY subject, sort)
  INTO v
  FROM public.curriculum
  WHERE semester = 'الفصل الأول' AND grade = 1;
  RAISE EXCEPTION 'PROBE_CURR_G1|%', COALESCE(v,'NULL');
END $$;
