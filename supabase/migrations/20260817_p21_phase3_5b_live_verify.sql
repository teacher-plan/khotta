DO $$
DECLARE
  v_tbl_exists boolean;
  v_cron_schedule text;
  v_cron_command text;
  v_grants text;
  v_kill_switch boolean;
  v_pb1_mode text;
  v_pb2_mode text;
BEGIN
  SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='scheduler_runs') INTO v_tbl_exists;
  SELECT schedule, command INTO v_cron_schedule, v_cron_command FROM cron.job WHERE jobname='agent-autonomous-scheduler';
  SELECT string_agg(DISTINCT grantee||':'||privilege_type, ', ') INTO v_grants
    FROM information_schema.role_table_grants WHERE table_name='scheduler_runs' AND grantee IN ('anon','authenticated');
  SELECT self_healing_enabled INTO v_kill_switch FROM public.self_healing_controls WHERE control_id='global';
  SELECT mode INTO v_pb1_mode FROM public.repair_playbooks WHERE playbook_id='retry_monitor_known_timeout';
  SELECT mode INTO v_pb2_mode FROM public.repair_playbooks WHERE playbook_id='reschedule_known_daily_summary_failure';

  RAISE EXCEPTION 'P21_VERIFY | scheduler_runs_exists=% | cron_schedule=% cron_command=% | grants_scheduler_runs=[%] | self_healing_enabled=% pb1_mode=% pb2_mode=%',
    v_tbl_exists, v_cron_schedule, v_cron_command, COALESCE(v_grants,'NONE'), v_kill_switch, v_pb1_mode, v_pb2_mode;
END $$;
