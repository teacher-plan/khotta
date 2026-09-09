DO $$
DECLARE d text;
BEGIN
  SELECT format('count=%s | rows=%s',
    (SELECT count(*) FROM trial_reengagement_log),
    (SELECT string_agg(email||':'||status||coalesce(' ('||left(reason,60)||')',''), E'\n' ORDER BY sent_at DESC)
       FROM trial_reengagement_log)
  ) INTO d;
  RAISE EXCEPTION 'DATA=%', left(d, 3000);
END $$;
