DO $$
DECLARE d text;
BEGIN
  SELECT format('count=%s | rows=%s',
    (SELECT count(*) FROM trial_reengagement_log),
    (SELECT string_agg(email||':'||status, ', ' ORDER BY sent_at DESC) FROM trial_reengagement_log)
  ) INTO d;
  RAISE EXCEPTION 'DATA=%', left(d, 2500);
END $$;
