DO $$
DECLARE d text;
BEGIN
  SELECT to_jsonb(t)::text INTO d FROM net._http_response t WHERE id = 14959;
  IF d IS NULL THEN
    SELECT 'no_response_row; queue_exists=' || (EXISTS(SELECT 1 FROM net.http_request_queue WHERE id=14959))::text
    INTO d;
  END IF;
  RAISE EXCEPTION 'DATA=%', left(d, 3000);
END $$;
