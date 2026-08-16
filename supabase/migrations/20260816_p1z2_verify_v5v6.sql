DO $$
DECLARE d json;
BEGIN
  SELECT json_agg(json_build_object('name',name,'payment_status',payment_status,'deleted','no-still-here'))
    INTO d
  FROM public.pre_registrations
  WHERE name IN ('__AUDIT_TEST_DO_NOT_ACTIVATE__','__AUDIT_TEST_ATTACK__');
  RAISE EXCEPTION '%', COALESCE(d::text, 'NULL-no-rows-found');
END;
$$;
