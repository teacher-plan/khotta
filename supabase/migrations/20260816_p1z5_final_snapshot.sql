DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'relrowsecurity', (SELECT c.relrowsecurity FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relname='pre_registrations'),
    'policies', (SELECT json_agg(json_build_object('name',policyname,'cmd',cmd,'roles',roles)) FROM pg_policies WHERE tablename='pre_registrations'),
    'ai_rate_limit_exists', (SELECT to_regclass('public.ai_rate_limit') IS NOT NULL),
    'check_ai_rate_limit_exists', (SELECT count(*)>0 FROM pg_proc WHERE proname='check_ai_rate_limit'),
    'sanity_table_gone', (SELECT to_regclass('public._audit_sanity') IS NULL),
    'test_rows_remaining', (SELECT count(*) FROM public.pre_registrations WHERE name LIKE '__AUDIT_TEST%')
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
