DO $$
DECLARE d text;
BEGIN
  SELECT format(
    'total_users=%s | total_pre_reg_cycle1=%s | ' ||
    'signed_up_no_trial_request=%s | ' ||
    'trial_requested_never_logged_in=%s | ' ||
    'logged_in_never_since=%s | ' ||
    'sample_no_trial=%s | ' ||
    'sample_no_login=%s | ' ||
    'sample_stale=%s',
    (SELECT count(*) FROM auth.users),
    (SELECT count(*) FROM pre_registrations WHERE stage='cycle1'),
    (SELECT count(*) FROM auth.users u
       WHERE NOT EXISTS (SELECT 1 FROM pre_registrations p WHERE lower(p.email)=lower(u.email))),
    (SELECT count(*) FROM pre_registrations p
       WHERE p.stage='cycle1' AND NOT EXISTS (SELECT 1 FROM auth.users u WHERE lower(u.email)=lower(p.email))),
    (SELECT count(*) FROM auth.users WHERE last_sign_in_at IS NOT NULL AND last_sign_in_at < now() - interval '7 days'),
    (SELECT string_agg(email||'('||to_char(created_at,'MM-DD')||')', ', ')
       FROM (SELECT email, created_at FROM auth.users u
             WHERE NOT EXISTS (SELECT 1 FROM pre_registrations p WHERE lower(p.email)=lower(u.email))
             ORDER BY created_at DESC LIMIT 8) x),
    (SELECT string_agg(email||'('||to_char(created_at,'MM-DD')||')', ', ')
       FROM (SELECT email, created_at FROM pre_registrations p
             WHERE p.stage='cycle1' AND NOT EXISTS (SELECT 1 FROM auth.users u WHERE lower(u.email)=lower(p.email))
             ORDER BY created_at DESC LIMIT 8) x),
    (SELECT string_agg(email||'(last:'||to_char(last_sign_in_at,'MM-DD')||')', ', ')
       FROM (SELECT email, last_sign_in_at FROM auth.users
             WHERE last_sign_in_at IS NOT NULL AND last_sign_in_at < now() - interval '7 days'
             ORDER BY last_sign_in_at DESC LIMIT 8) x)
  ) INTO d;
  RAISE EXCEPTION 'DATA=%', d;
END $$;
