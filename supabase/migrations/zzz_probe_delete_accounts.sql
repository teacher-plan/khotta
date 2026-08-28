DO $$
DECLARE v jsonb;
BEGIN
  SELECT jsonb_agg(jsonb_build_object('id',id,'name',name,'email',email,'phone',phone,'stage',stage,
    'account_email',account_email,'payment_status',payment_status,'created_at',created_at))
  INTO v
  FROM public.pre_registrations
  WHERE lower(email) IN ('c1@khotati.app','x@y.com','iphon90z8@yahoo.com','tv8888tvvv@gmail.com')
     OR lower(email) LIKE '%khotati.app';
  RAISE EXCEPTION 'PROBE_DEL | %', COALESCE(v::text,'NULL');
END $$;
