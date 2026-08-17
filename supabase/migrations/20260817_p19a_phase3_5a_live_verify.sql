DO $$
DECLARE
  v_tbl_exists boolean;
  v_fn1_exists boolean;
  v_fn2_exists boolean;
  v_idx_exists boolean;
  v_uniq_target boolean;
  v_status_check text;
  v_grants_incident_claims text;
  v_grants_repair_executions text;
  v_grants_repair_playbooks text;
  v_grants_self_healing_controls text;
  v_rpc_grants text;
  v_fn_secdef text;
  v_kill_switch boolean;
  v_disabled_agents jsonb;
  v_pb1_mode text;
  v_pb2_mode text;
BEGIN
  SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema='public' AND table_name='incident_claims') INTO v_tbl_exists;
  SELECT EXISTS (SELECT 1 FROM pg_proc WHERE proname='claim_incident_for_repair') INTO v_fn1_exists;
  SELECT EXISTS (SELECT 1 FROM pg_proc WHERE proname='release_incident_claim') INTO v_fn2_exists;
  SELECT EXISTS (SELECT 1 FROM pg_indexes WHERE indexname='uq_repair_executions_incident_playbook_attempt') INTO v_idx_exists;
  SELECT EXISTS (SELECT 1 FROM pg_constraint WHERE conname='incident_claims_unique_target') INTO v_uniq_target;

  SELECT pg_get_constraintdef(oid) INTO v_status_check FROM pg_constraint WHERE conname='repair_executions_status_check';

  SELECT string_agg(DISTINCT grantee||':'||privilege_type, ', ') INTO v_grants_incident_claims
    FROM information_schema.role_table_grants WHERE table_name='incident_claims' AND grantee IN ('anon','authenticated');
  SELECT string_agg(DISTINCT grantee||':'||privilege_type, ', ') INTO v_grants_repair_executions
    FROM information_schema.role_table_grants WHERE table_name='repair_executions' AND grantee IN ('anon','authenticated');
  SELECT string_agg(DISTINCT grantee||':'||privilege_type, ', ') INTO v_grants_repair_playbooks
    FROM information_schema.role_table_grants WHERE table_name='repair_playbooks' AND grantee IN ('anon','authenticated');
  SELECT string_agg(DISTINCT grantee||':'||privilege_type, ', ') INTO v_grants_self_healing_controls
    FROM information_schema.role_table_grants WHERE table_name='self_healing_controls' AND grantee IN ('anon','authenticated');

  SELECT string_agg(DISTINCT grantee||':'||routine_name||':'||privilege_type, ', ') INTO v_rpc_grants
    FROM information_schema.routine_privileges
    WHERE routine_name IN ('claim_incident_for_repair','release_incident_claim') AND grantee IN ('anon','authenticated');

  SELECT string_agg(proname||'(secdef='||prosecdef||',search_path='||COALESCE((SELECT option_value FROM unnest(proconfig) AS option_value WHERE option_value LIKE 'search_path%'),'NONE')||')', ' | ')
    INTO v_fn_secdef
    FROM pg_proc WHERE proname IN ('claim_incident_for_repair','release_incident_claim');

  SELECT self_healing_enabled, disabled_agents INTO v_kill_switch, v_disabled_agents FROM public.self_healing_controls WHERE control_id='global';
  SELECT mode INTO v_pb1_mode FROM public.repair_playbooks WHERE playbook_id='retry_monitor_known_timeout';
  SELECT mode INTO v_pb2_mode FROM public.repair_playbooks WHERE playbook_id='reschedule_known_daily_summary_failure';

  RAISE EXCEPTION 'P19A_VERIFY | table=% fn1=% fn2=% idx=% uniq_target=% | status_check=% | grants_incident_claims=[%] grants_repair_executions=[%] grants_repair_playbooks=[%] grants_self_healing_controls=[%] | rpc_grants=[%] | fn_secdef=[%] | kill_switch_enabled=% disabled_agents=% | pb1_mode=% pb2_mode=%',
    v_tbl_exists, v_fn1_exists, v_fn2_exists, v_idx_exists, v_uniq_target,
    v_status_check,
    COALESCE(v_grants_incident_claims,'NONE'), COALESCE(v_grants_repair_executions,'NONE'), COALESCE(v_grants_repair_playbooks,'NONE'), COALESCE(v_grants_self_healing_controls,'NONE'),
    COALESCE(v_rpc_grants,'NONE'),
    v_fn_secdef,
    v_kill_switch, v_disabled_agents,
    v_pb1_mode, v_pb2_mode;
END $$;
