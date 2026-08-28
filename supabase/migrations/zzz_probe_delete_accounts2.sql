DO $$
DECLARE v1 jsonb; v2 jsonb; v3 jsonb;
BEGIN
  SELECT jsonb_agg(jsonb_build_object('email',email,'cycle',cycle,'added_at',added_at,'expires_at',expires_at))
  INTO v1
  FROM public.allowed_emails
  WHERE lower(email) IN ('c1@khotati.app','x@y.com','iphon90z8@yahoo.com','tv8888tvvv@gmail.com');

  SELECT jsonb_agg(jsonb_build_object('id',id,'email',email,'data',data,'created_at',created_at))
  INTO v2
  FROM public.cycle1_profiles
  WHERE lower(email) IN ('c1@khotati.app','x@y.com','iphon90z8@yahoo.com','tv8888tvvv@gmail.com');

  SELECT jsonb_agg(jsonb_build_object('id',id,'email',email))
  INTO v3
  FROM auth.users
  WHERE lower(email) IN ('c1@khotati.app','x@y.com','iphon90z8@yahoo.com','tv8888tvvv@gmail.com');

  RAISE EXCEPTION 'PROBE_DEL2 | allowed=% | profiles=% | users=%', COALESCE(v1::text,'NULL'), COALESCE(v2::text,'NULL'), COALESCE(v3::text,'NULL');
END $$;
