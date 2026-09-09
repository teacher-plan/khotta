DO $$
DECLARE d text;
BEGIN
  SELECT format('status=%s body=%s',
    coalesce(status_code::text,'(pending)'),
    left(coalesce((content::jsonb)::text, content, '(no response yet)'), 500)
  ) INTO d
  FROM net._http_response WHERE id = 14959;
  IF d IS NULL THEN d := 'NO_ROW_YET'; END IF;
  RAISE EXCEPTION 'DATA=%', d;
END $$;
