DO $$
DECLARE d text;
BEGIN
  SELECT format(
    'trial_total=%s | targets=%s | sample=%s',
    (SELECT count(*) FROM allowed_emails WHERE expires_at IS NOT NULL AND expires_at > now() AND expires_at <= now() + interval '2 days'),
    (SELECT count(*) FROM allowed_emails ae
       WHERE ae.expires_at IS NOT NULL AND ae.expires_at > now() AND ae.expires_at <= now() + interval '2 days'
         AND NOT EXISTS (
           SELECT 1 FROM auth.users u WHERE lower(u.email)=lower(ae.email)
             AND u.last_sign_in_at IS NOT NULL AND u.last_sign_in_at >= now() - interval '2 days'
         )),
    (SELECT string_agg(ae.email||'(last:'||coalesce(to_char(u.last_sign_in_at,'MM-DD'),'never')||', exp:'||to_char(ae.expires_at,'MM-DD HH24:MI')||')', E'\n' ORDER BY ae.email)
       FROM allowed_emails ae LEFT JOIN auth.users u ON lower(u.email)=lower(ae.email)
       WHERE ae.expires_at IS NOT NULL AND ae.expires_at > now() AND ae.expires_at <= now() + interval '2 days'
         AND (u.last_sign_in_at IS NULL OR u.last_sign_in_at < now() - interval '2 days'))
  ) INTO d;
  RAISE EXCEPTION 'DATA=%', d;
END $$;
