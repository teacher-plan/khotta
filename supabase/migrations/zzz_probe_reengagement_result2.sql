DO $$
DECLARE d text;
BEGIN
  SELECT string_agg('id='||id||' status='||coalesce(status_code::text,'null')||' created='||created, E'\n' ORDER BY id DESC)
  INTO d
  FROM net._http_response
  ORDER BY id DESC LIMIT 5;
  IF d IS NULL THEN d := 'NO_ROWS_AT_ALL'; END IF;
  RAISE EXCEPTION 'DATA=%', d;
END $$;
