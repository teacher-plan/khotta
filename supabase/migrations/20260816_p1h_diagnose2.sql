DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'policies', (SELECT json_agg(json_build_object('name',polname,'permissive',polpermissive,'cmd',polcmd,'roles',(SELECT array_agg(rolname) FROM pg_roles WHERE oid = ANY(polroles)),'with_check',pg_get_expr(polwithcheck, polrelid),'qual',pg_get_expr(polqual, polrelid))) FROM pg_policy WHERE polrelid = 'public.pre_registrations'::regclass),
    'anon_is_member_of_authenticated', pg_has_role('anon','authenticated','MEMBER'),
    'anon_role_attrs', (SELECT json_build_object('rolbypassrls',rolbypassrls,'rolsuper',rolsuper,'rolinherit',rolinherit) FROM pg_roles WHERE rolname='anon'),
    'current_setting_row_security', current_setting('row_security', true),
    'table_owner', (SELECT pg_get_userbyid(relowner) FROM pg_class WHERE oid='public.pre_registrations'::regclass)
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
