-- تنظيف حساب اختبار Phase 2 (رفض غير المشرف فقط — لم يُستدعَ أي أداة كتابة)
DELETE FROM auth.users WHERE email = 'khotta.audit.test+ops@gmail.com';

-- تشخيصٌ للقراءة فقط: حالة ops_incidents الحقيقية بعد النشر.
DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'relrowsecurity', (SELECT c.relrowsecurity FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND c.relname='ops_incidents'),
    'policies', (SELECT json_agg(policyname) FROM pg_policies WHERE tablename='ops_incidents'),
    'grants_anon', (SELECT json_agg(privilege_type) FROM information_schema.role_table_grants WHERE table_name='ops_incidents' AND grantee='anon'),
    'grants_authenticated', (SELECT json_agg(privilege_type) FROM information_schema.role_table_grants WHERE table_name='ops_incidents' AND grantee='authenticated'),
    'incident_count', (SELECT count(*) FROM public.ops_incidents),
    'ai_cost_log_kind_ops_count', (SELECT count(*) FROM public.ai_cost_log WHERE kind='ops'),
    'last_health_check_cron', (SELECT max(r.end_time) FROM cron.job j JOIN cron.job_run_details r ON r.jobid=j.jobid WHERE j.jobname='agent-health-check'),
    'last_health_check_status', (SELECT (array_agg(r.status ORDER BY r.end_time DESC))[1] FROM cron.job j JOIN cron.job_run_details r ON r.jobid=j.jobid WHERE j.jobname='agent-health-check')
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
