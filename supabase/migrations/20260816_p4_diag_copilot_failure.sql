DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'now', now(),
    'ops_cost_log_rows', (SELECT count(*) FROM public.ai_cost_log WHERE kind='ops'),
    'ops_cost_log_by_function', (SELECT json_agg(json_build_object('function_name',function_name,'model',model,'created_at',created_at,'user_id',user_id)) FROM public.ai_cost_log WHERE kind='ops' ORDER BY created_at DESC LIMIT 20),
    'is_app_admin_exists', (SELECT count(*) FROM pg_proc WHERE proname='is_app_admin'),
    'is_app_admin_def', (SELECT prosrc FROM pg_proc WHERE proname='is_app_admin' LIMIT 1),
    'is_app_admin_grants', (SELECT json_agg(grantee || ':' || privilege_type) FROM information_schema.routine_privileges WHERE routine_name='is_app_admin'),
    'ops_copilot_function_deployed', (SELECT count(*) FROM pg_proc WHERE proname LIKE '%ops%'),
    'auth_users_admin_row', (SELECT json_build_object('exists', count(*)>0) FROM auth.users WHERE lower(email)='teacherplane2026project@gmail.com'),
    'ops_incidents_rls', (SELECT relrowsecurity FROM pg_class WHERE relname='ops_incidents'),
    'recent_error_logs_ops', (SELECT json_agg(json_build_object('function_name',function_name,'error_type',error_type,'occurred_at',occurred_at)) FROM public.error_logs WHERE function_name IN ('ops-copilot','ops-analyze') ORDER BY occurred_at DESC LIMIT 10)
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
