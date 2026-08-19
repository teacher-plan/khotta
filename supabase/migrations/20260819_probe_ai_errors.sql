DO $$
DECLARE v text;
BEGIN
  SELECT string_agg(format('[%s] %s | %s | %s',occurred_at,function_name,error_type,error_code),E'\n' ORDER BY occurred_at DESC)
  INTO v
  FROM (
    SELECT * FROM public.error_logs
    ORDER BY occurred_at DESC LIMIT 15
  ) t;
  RAISE EXCEPTION 'PROBE | %', COALESCE(v,'NO_ROWS');
END $$;
