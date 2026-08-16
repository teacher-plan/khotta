DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'now', now(),
    'last_health_check_run', (SELECT max(r.end_time) FROM cron.job j JOIN cron.job_run_details r ON r.jobid=j.jobid WHERE j.jobname='agent-health-check'),
    'last_health_check_status', (SELECT (array_agg(r.status ORDER BY r.end_time DESC))[1] FROM cron.job j JOIN cron.job_run_details r ON r.jobid=j.jobid WHERE j.jobname='agent-health-check'),
    'runs_since_deploy', (SELECT count(*) FROM cron.job j JOIN cron.job_run_details r ON r.jobid=j.jobid WHERE j.jobname='agent-health-check' AND r.end_time > '2026-08-16T04:45:02+00:00'::timestamptz),
    'failed_runs_since_deploy', (SELECT count(*) FROM cron.job j JOIN cron.job_run_details r ON r.jobid=j.jobid WHERE j.jobname='agent-health-check' AND r.end_time > '2026-08-16T04:45:02+00:00'::timestamptz AND r.status <> 'succeeded'),
    'incident_count', (SELECT count(*) FROM public.ops_incidents),
    'incidents', (SELECT json_agg(json_build_object('component',component,'severity',severity,'status',status,'occurrence_count',occurrence_count)) FROM public.ops_incidents)
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
