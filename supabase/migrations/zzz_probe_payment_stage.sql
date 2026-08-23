DO $$
DECLARE v text;
BEGIN
  SELECT string_agg(payment_status || '|' || payment_reminder_stage || '=' || cnt::text, ', ')
  INTO v
  FROM (
    SELECT payment_status, payment_reminder_stage, count(*) cnt
    FROM pre_registrations
    WHERE stage='cycle1'
    GROUP BY 1,2
    ORDER BY 1,2
  ) t;
  RAISE EXCEPTION 'PROBE_STAGE | %', v;
END $$;
