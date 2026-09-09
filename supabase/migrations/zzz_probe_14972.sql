DO $$
DECLARE d text;
BEGIN
  SELECT to_jsonb(t)::text INTO d FROM net._http_response t WHERE id = 14972;
  IF d IS NULL THEN d := 'still_no_row'; END IF;
  RAISE EXCEPTION 'DATA=%', left(d, 2000);
END $$;
