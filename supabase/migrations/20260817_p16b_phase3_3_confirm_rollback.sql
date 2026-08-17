DO $$
DECLARE v_state text; v_mode text; v_leftover_rows int;
BEGIN
  SELECT circuit_state, mode INTO v_state, v_mode FROM public.repair_playbooks WHERE playbook_id='retry_monitor_known_timeout';
  SELECT count(*) INTO v_leftover_rows FROM public.ops_incidents WHERE dedup_key='__phase3_3_test__';
  RAISE EXCEPTION 'PHASE3_3_ROLLBACK_CONFIRM | circuit_state_now: % | mode_now: % | leftover_test_incidents: %', v_state, v_mode, v_leftover_rows;
END $$;
