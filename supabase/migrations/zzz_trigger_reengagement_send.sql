DO $$
DECLARE v_key text; v_req bigint;
BEGIN
  SELECT decrypted_secret INTO v_key FROM vault.decrypted_secrets WHERE name = 'service_role_key';
  IF v_key IS NULL THEN
    RAISE EXCEPTION 'NO_KEY';
  END IF;
  SELECT net.http_post(
    url := 'https://mkdsnnfkkdwdkywnwnjh.supabase.co/functions/v1/trial-reengagement-email',
    headers := jsonb_build_object('Content-Type','application/json','Authorization','Bearer '||v_key),
    body := '{}'::jsonb,
    timeout_milliseconds := 120000
  ) INTO v_req;
  RAISE EXCEPTION 'REQ_ID=%', v_req;
END $$;
