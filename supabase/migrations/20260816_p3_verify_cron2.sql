DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'now', now(),
    'recent_runs', (SELECT json_agg(json_build_object('end_time',r.end_time,'status',r.status) ORDER BY r.end_time DESC) FROM cron.job j JOIN cron.job_run_details r ON r.jobid=j.jobid WHERE j.jobname='agent-health-check' AND r.end_time > now() - interval '10 minutes'),
    'incident_count', (SELECT count(*) FROM public.ops_incidents)
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
