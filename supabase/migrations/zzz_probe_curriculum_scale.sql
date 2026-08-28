DO $$
DECLARE v jsonb;
BEGIN
  SELECT jsonb_agg(row_to_json(t)) INTO v FROM (
    SELECT grade, subject, count(*) AS lessons, count(DISTINCT unit) AS units
    FROM public.curriculum
    WHERE semester = 'الفصل الأول' AND grade IN (1,2,3,4)
    GROUP BY grade, subject
    ORDER BY grade, subject
  ) t;
  RAISE EXCEPTION 'PROBE_CURR_SCALE | %', COALESCE(v::text,'NULL');
END $$;
