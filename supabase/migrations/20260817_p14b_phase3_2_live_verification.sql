-- ════════════════════════════════════════════════════════════════════
-- Phase 3.2 — تحقّقٌ حيٌّ نهائي: schema الجدول الجديد، حالة الـPlaybooks
-- (لا تزال SHADOW)، نتيجة اختبار Shadow المُصلَح (p14a)، وتأكيدٌ إضافي
-- أن بوّابة المخاطر (المُثبَتة في Phase 3.1) لم تتأثّر بأي تعديل.
-- يفشل عمداً (RAISE EXCEPTION) فيتراجع تلقائياً — لا أثر جانبي.
-- ════════════════════════════════════════════════════════════════════

DO $$
DECLARE
  v_deploy_log_cols text;
  v_deploy_rows int;
  v_playbook_modes text;
  v_shadow_result text;
  v_gate_still_works text;
BEGIN
  SELECT count(*) INTO v_deploy_log_cols FROM information_schema.columns
    WHERE table_schema='public' AND table_name='deployment_log';

  SELECT count(*) INTO v_deploy_rows FROM public.deployment_log;

  SELECT string_agg(playbook_id || '=' || mode, ', ' ORDER BY playbook_id)
  INTO v_playbook_modes FROM public.repair_playbooks;

  SELECT 'status=' || re.status || ',escalation_reason=' || coalesce(re.escalation_reason,'NULL')
  INTO v_shadow_result
  FROM public.repair_executions re
  JOIN public.ops_incidents oi ON oi.id = re.incident_id
  WHERE oi.dedup_key = '__phase3_2_test__credit-monitor'
  ORDER BY re.started_at DESC LIMIT 1;

  BEGIN
    INSERT INTO public.repair_playbooks (
      playbook_id, name, description, incident_pattern, minimum_confidence, risk_level,
      allowed_actions, repair_steps, verification_steps, rollback_strategy, affected_scope, requires_human_approval
    ) VALUES ('__test2_should_fail__','اختبار','اختبار','X',90,'HIGH','["rerun_monitor_agent"]'::jsonb,'[]'::jsonb,'[]'::jsonb,'n/a','ONE_AGENT', false);
    v_gate_still_works := 'FAIL — لا يزال القيد يجب أن يرفض!';
  EXCEPTION WHEN check_violation THEN
    v_gate_still_works := 'PASS — بوّابة المخاطر لا تزال تعمل بعد تعديلات Phase 3.2.';
  END;

  RAISE EXCEPTION 'PHASE3_2_LIVE_EVIDENCE | DEPLOYMENT_LOG_COLS: % | DEPLOYMENT_LOG_ROWS: % | PLAYBOOK_MODES: % | SHADOW_TEST_RESULT: % | RISK_GATE_STILL_WORKS: %',
    v_deploy_log_cols, v_deploy_rows, coalesce(v_playbook_modes,'NONE'), coalesce(v_shadow_result,'NOT FOUND'), v_gate_still_works;
END $$;
