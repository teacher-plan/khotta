DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'now', now(),
    'ops_cost_log_rows', (SELECT count(*) FROM public.ai_cost_log WHERE kind='ops'),
    'ops_cost_log_by_function', (
      SELECT json_agg(t) FROM (
        SELECT function_name, model, created_at, user_id
        FROM public.ai_cost_log WHERE kind='ops'
        ORDER BY created_at DESC LIMIT 20
      ) t
    ),
    'is_app_admin_exists', (SELECT count(*) FROM pg_proc WHERE proname='is_app_admin'),
    'is_app_admin_def', (SELECT prosrc FROM pg_proc WHERE proname='is_app_admin' LIMIT 1),
    'is_app_admin_grants', (SELECT json_agg(grantee || ':' || privilege_type) FROM information_schema.routine_privileges WHERE routine_name='is_app_admin'),
    'ops_functions_in_pg_proc', (SELECT json_agg(proname) FROM pg_proc WHERE proname LIKE '%ops%'),
    'auth_users_admin_row_exists', (SELECT count(*)>0 FROM auth.users WHERE lower(email)='teacherplane2026project@gmail.com'),
    'ops_incidents_rls', (SELECT relrowsecurity FROM pg_class WHERE relname='ops_incidents'),
    'recent_error_logs_ops', (
      SELECT json_agg(t) FROM (
        SELECT function_name, error_type, occurred_at
        FROM public.error_logs WHERE function_name IN ('ops-copilot','ops-analyze')
        ORDER BY occurred_at DESC LIMIT 10
      ) t
    )
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
