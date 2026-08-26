DO $$
DECLARE
  v_allowed jsonb;
  v_user jsonb;
  v_prereg jsonb;
  v_secrets jsonb;
  v_errlogs jsonb;
BEGIN
  SELECT to_jsonb(ae) INTO v_allowed
  FROM public.allowed_emails ae
  WHERE lower(email) = 'hebaa3918@gmail.com';

  SELECT jsonb_build_object('id', u.id, 'email', u.email, 'created_at', u.created_at,
    'confirmed_at', u.confirmed_at, 'last_sign_in_at', u.last_sign_in_at)
  INTO v_user
  FROM auth.users u
  WHERE lower(u.email) = 'hebaa3918@gmail.com';

  SELECT to_jsonb(pr) INTO v_prereg
  FROM public.pre_registrations pr
  WHERE lower(email) = 'hebaa3918@gmail.com'
  ORDER BY created_at DESC LIMIT 1;

  SELECT jsonb_agg(jsonb_build_object('name', name, 'is_set', (decrypted_secret IS NOT NULL AND decrypted_secret <> '')))
  INTO v_secrets
  FROM vault.decrypted_secrets
  WHERE name IN ('RESEND_API_KEY', 'MAIL_FROM');

  SELECT jsonb_agg(jsonb_build_object('occurred_at', occurred_at, 'function_name', function_name, 'message', left(message,200)))
  INTO v_errlogs
  FROM (
    SELECT * FROM public.error_logs
    WHERE (function_name ILIKE '%activate%' OR message ILIKE '%hebaa%' OR message ILIKE '%resend%')
    ORDER BY occurred_at DESC LIMIT 10
  ) x;

  RAISE EXCEPTION 'PROBE_HEBAA | allowed=% | user=% | prereg=% | secrets=% | errlogs=%',
    COALESCE(v_allowed::text,'NULL'), COALESCE(v_user::text,'NULL'), COALESCE(v_prereg::text,'NULL'),
    COALESCE(v_secrets::text,'NULL'), COALESCE(v_errlogs::text,'NULL');
END $$;
