DO $$
DECLARE v_pb record; v_action record;
BEGIN
  SELECT * INTO v_pb FROM public.repair_playbooks WHERE playbook_id='retry_monitor_known_timeout';
  SELECT * INTO v_action FROM public.safe_action_registry WHERE action_id = (v_pb.repair_steps->0->>'action_id');
  RAISE EXCEPTION 'PHASE3_4_PREFLIGHT | exists=% enabled=% mode=% risk=% min_conf=% max_attempts=% cooldown=% circuit_threshold=% circuit_state=% affected_scope=% requires_approval=% | action_id=% action_enabled=% action_reversible=%',
    (v_pb.playbook_id IS NOT NULL), v_pb.enabled, v_pb.mode, v_pb.risk_level, v_pb.minimum_confidence, v_pb.max_attempts, v_pb.cooldown_minutes, v_pb.circuit_breaker_threshold, v_pb.circuit_state, v_pb.affected_scope, v_pb.requires_human_approval,
    v_action.action_id, v_action.enabled, v_action.reversible;
END $$;
