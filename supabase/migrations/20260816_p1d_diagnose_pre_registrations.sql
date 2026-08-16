-- تشخيصٌ مقصود الفشل: الـworkflow يطبع resp.json فقط عند الفشل، فنستعمل
-- RAISE EXCEPTION لإخراج التشخيص كرسالة خطأ نقرؤها. لا يُغيّر أي شيء —
-- قراءةٌ صرفة ملفوفة في استثناء متعمَّد.
DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'has_insert_anon', has_table_privilege('anon', 'public.pre_registrations', 'INSERT'),
    'has_insert_authenticated', has_table_privilege('authenticated', 'public.pre_registrations', 'INSERT'),
    'has_select_authenticated', has_table_privilege('authenticated', 'public.pre_registrations', 'SELECT'),
    'relrowsecurity', (SELECT c.relrowsecurity FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relname='pre_registrations'),
    'relforcerowsecurity', (SELECT c.relforcerowsecurity FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relname='pre_registrations'),
    'policies', (SELECT json_agg(json_build_object('name',policyname,'cmd',cmd,'roles',roles,'with_check',with_check,'qual',qual)) FROM pg_policies WHERE tablename='pre_registrations'),
    'grants', (SELECT json_agg(json_build_object('grantee',grantee,'priv',privilege_type)) FROM information_schema.role_table_grants WHERE table_name='pre_registrations' AND table_schema='public')
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
