DO $$
DECLARE d text;
BEGIN
  SELECT string_agg(to_jsonb(t)::text, E'\n' ORDER BY t.id DESC)
  INTO d
  FROM (SELECT * FROM net._http_response ORDER BY id DESC LIMIT 5) t;
  IF d IS NULL THEN d := 'NO_ROWS_AT_ALL'; END IF;
  RAISE EXCEPTION 'DATA=%', left(d, 3000);
END $$;
