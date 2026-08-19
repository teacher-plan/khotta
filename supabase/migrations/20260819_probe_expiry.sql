DO $$
DECLARE v text;
BEGIN
  SELECT format('total=%s, with_expiry=%s, col_exists=%s',
    count(*), count(expires_at),
    (SELECT count(*) FROM information_schema.columns
      WHERE table_name='allowed_emails' AND column_name='expires_at'))
  INTO v FROM public.allowed_emails;
  RAISE EXCEPTION 'PROBE | %', v;
END $$;
