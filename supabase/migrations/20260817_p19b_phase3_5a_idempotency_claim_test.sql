DO $$
DECLARE
  v_incident_id uuid;
  v_first_insert_ok boolean := false;
  v_second_insert_sqlstate text := 'NONE';
  v_second_insert_sqlerrm text := 'NONE';
  v_claim1 uuid;
  v_claim2 uuid;
BEGIN
  -- إدراج حادثة اختبارية مؤقتة (كل هذا الـDO سيتراجع بالكامل في النهاية)
  INSERT INTO public.ops_incidents (
    dedup_key, severity, status, component, summary, evidence,
    confidence, first_seen_at, last_seen_at, detected_at, source_agent
  ) VALUES (
    'PHASE3_5A_IDEMPOTENCY_TEST_TEMP', 'LOW', 'DETECTED', 'test-component',
    'PHASE3_5A test incident (self-rollback, never persisted)', '{}'::jsonb,
    90, now(), now(), now(), 'phase3_5a_validation'
  ) RETURNING id INTO v_incident_id;

  -- الإدراج الأول: يجب أن ينجح
  INSERT INTO public.repair_executions (
    incident_id, playbook_id, action_id, mode, status, attempt_number, started_at, actor
  ) VALUES (
    v_incident_id, 'retry_monitor_known_timeout', 'rerun_monitor_agent', 'SHADOW', 'EVALUATING', 1, now(), 'phase3_5a_validation'
  );
  v_first_insert_ok := true;

  -- الإدراج الثاني: نفس (incident_id, playbook_id, attempt_number) — يجب أن يفشل بقيد الفريد
  BEGIN
    INSERT INTO public.repair_executions (
      incident_id, playbook_id, action_id, mode, status, attempt_number, started_at, actor
    ) VALUES (
      v_incident_id, 'retry_monitor_known_timeout', 'rerun_monitor_agent', 'SHADOW', 'EVALUATING', 1, now(), 'phase3_5a_validation'
    );
  EXCEPTION WHEN unique_violation THEN
    v_second_insert_sqlstate := SQLSTATE;
    v_second_insert_sqlerrm := SQLERRM;
  END;

  -- اختبار الادّعاء الذرّي: استدعاءان متتاليان (تسلسليّان، لا متزامنان حقاً)
  SELECT public.claim_incident_for_repair(v_incident_id, 'retry_monitor_known_timeout', 'phase3_5a_validation_actor1', 15) INTO v_claim1;
  SELECT public.claim_incident_for_repair(v_incident_id, 'retry_monitor_known_timeout', 'phase3_5a_validation_actor2', 15) INTO v_claim2;

  RAISE EXCEPTION 'P19B_IDEMPOTENCY_CLAIM_TEST | first_insert_ok=% | second_insert_sqlstate=% second_insert_sqlerrm=% | claim1=% claim2=% claim1_succeeded=% claim2_correctly_blocked=%',
    v_first_insert_ok, v_second_insert_sqlstate, v_second_insert_sqlerrm,
    v_claim1, v_claim2, (v_claim1 IS NOT NULL), (v_claim2 IS NULL);
END $$;
