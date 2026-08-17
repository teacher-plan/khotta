DO $$
DECLARE v_row record;
BEGIN
  SELECT * INTO v_row FROM public.scheduler_runs ORDER BY started_at DESC LIMIT 1;
  RAISE EXCEPTION 'P22_REAL_RUN_CHECK | run_id=% status=% started_at=% completed_at=% duration_ms=% scanned=% claimed=% evaluated=% would_repair=% escalated=% errors=% error_detail=%',
    v_row.run_id, v_row.status, v_row.started_at, v_row.completed_at, v_row.duration_ms,
    v_row.incidents_scanned, v_row.incidents_claimed, v_row.incidents_evaluated,
    v_row.shadow_would_repair, v_row.escalated, v_row.errors, v_row.error_detail;
END $$;
