DO $$
DECLARE v text;
BEGIN
  SELECT string_agg(format('%s: lessons=%s units=%s grades=%s',subject,lessons,units,grades), E'\n' ORDER BY lessons DESC)
  INTO v
  FROM (
    SELECT subject, count(*) lessons, count(DISTINCT unit) units,
      string_agg(DISTINCT grade::text, ',' ORDER BY grade::text) grades
    FROM public.curriculum
    WHERE grade BETWEEN 1 AND 4
    GROUP BY subject
  ) t;
  RAISE EXCEPTION 'PROBE | %', COALESCE(v,'NO_ROWS');
END $$;
