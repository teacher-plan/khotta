DO $$
DECLARE d text;
BEGIN
  SELECT format(
    'rls_pv=%s pols_pv=%s | rls_pr=%s pols_pr=%s | exec_anon_register=%s | pv_total=%s pv_7d=%s pv_by_page=%s | pr_total=%s pr_stage_cycle1=%s pr_last=%s',
    (SELECT relrowsecurity FROM pg_class WHERE relname='page_views'),
    (SELECT string_agg(policyname||':'||cmd||':'||roles::text, ', ') FROM pg_policies WHERE tablename='page_views'),
    (SELECT relrowsecurity FROM pg_class WHERE relname='pre_registrations'),
    (SELECT string_agg(policyname||':'||cmd||':'||roles::text, ', ') FROM pg_policies WHERE tablename='pre_registrations'),
    (SELECT has_function_privilege('anon', 'public.register_teacher(text,text,text,text,text)', 'EXECUTE')),
    (SELECT count(*) FROM page_views),
    (SELECT count(*) FROM page_views WHERE created_at > now() - interval '14 days'),
    (SELECT string_agg(page||':'||c::text,', ') FROM (SELECT page, count(*) c FROM page_views GROUP BY page) x),
    (SELECT count(*) FROM pre_registrations),
    (SELECT count(*) FROM pre_registrations WHERE stage='cycle1'),
    (SELECT max(created_at) FROM pre_registrations)
  ) INTO d;
  RAISE EXCEPTION 'DATA=%', d;
END $$;
