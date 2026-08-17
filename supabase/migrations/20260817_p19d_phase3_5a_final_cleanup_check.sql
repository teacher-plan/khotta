DO $$
DECLARE
  v_leftover_incidents int;
  v_leftover_executions int;
  v_leftover_claims int;
BEGIN
  SELECT count(*) INTO v_leftover_incidents FROM public.ops_incidents WHERE dedup_key = 'PHASE3_5A_IDEMPOTENCY_TEST_TEMP';
  SELECT count(*) INTO v_leftover_executions FROM public.repair_executions WHERE actor = 'phase3_5a_validation';
  SELECT count(*) INTO v_leftover_claims FROM public.incident_claims WHERE claimed_by IN ('phase3_5a_validation_actor1','phase3_5a_validation_actor2');

  RAISE EXCEPTION 'P19D_FINAL_CLEANUP_CHECK | leftover_incidents=% leftover_executions=% leftover_claims=%',
    v_leftover_incidents, v_leftover_executions, v_leftover_claims;
END $$;
