DO $$
DECLARE v_key text; v_req bigint; v_status int; v_content text; v_tries int := 0;
BEGIN
  SELECT decrypted_secret INTO v_key FROM vault.decrypted_secrets WHERE name = 'service_role_key';
  IF v_key IS NULL THEN RAISE EXCEPTION 'NO_KEY'; END IF;

  SELECT net.http_post(
    url := 'https://mkdsnnfkkdwdkywnwnjh.supabase.co/functions/v1/trial-reengagement-email',
    headers := jsonb_build_object('Content-Type','application/json','Authorization','Bearer '||v_key),
    body := '{}'::jsonb,
    timeout_milliseconds := 15000
  ) INTO v_req;

  LOOP
    v_tries := v_tries + 1;
    SELECT status_code, content INTO v_status, v_content FROM net._http_response WHERE id = v_req;
    EXIT WHEN v_status IS NOT NULL OR v_tries > 30;
    PERFORM pg_sleep(0.5);
  END LOOP;

  IF v_status IS NULL THEN
    RAISE EXCEPTION 'REQ_ID=% still pending after % tries', v_req, v_tries;
  END IF;
  RAISE EXCEPTION 'REQ_ID=% STATUS=% BODY=%', v_req, v_status, left(v_content, 800);
END $$;
