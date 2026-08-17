-- ════════════════════════════════════════════════════════════════════
-- Phase 3.1 — تحقّقٌ حيٌّ شامل (Schema + RLS + Seed + بوّابة المخاطر +
-- نتيجة اختبار Shadow المُدرَج في p12a). يفشل عمداً (RAISE EXCEPTION)
-- لإعادة نتائج الاستعلامات الحقيقية داخل رسالة الخطأ، ثم يتراجع تلقائياً
-- (ROLLBACK) — لا أثر جانبي من هذا الملف تحديداً (محاولة قيد risk gate
-- تُرفَض كما في اختبار Phase 2 المماثل).
-- ════════════════════════════════════════════════════════════════════

DO $$
DECLARE
  v_tables text;
  v_rls text;
  v_playbooks text;
  v_controls text;
  v_gate_test text;
  v_shadow_result text;
BEGIN
  SELECT string_agg(table_name || '(' || column_count || ' cols)', ', ' ORDER BY table_name)
  INTO v_tables
  FROM (
    SELECT table_name, count(*) AS column_count FROM information_schema.columns
    WHERE table_schema = 'public' AND table_name IN ('repair_playbooks','repair_executions','self_healing_controls')
    GROUP BY table_name
  ) t;

  SELECT string_agg(relname || '=' || relrowsecurity, ', ' ORDER BY relname)
  INTO v_rls FROM pg_class
  WHERE relname IN ('repair_playbooks','repair_executions','self_healing_controls') AND relnamespace = 'public'::regnamespace;

  SELECT string_agg(
    playbook_id || '[mode=' || mode || ',risk=' || risk_level || ',min_conf=' || minimum_confidence
      || ',approval=' || requires_human_approval || ',max_attempts=' || max_attempts
      || ',cooldown=' || cooldown_minutes || ',scope=' || affected_scope || ',circuit=' || circuit_state || ']',
    ', ' ORDER BY playbook_id)
  INTO v_playbooks FROM public.repair_playbooks;

  SELECT 'self_healing_enabled=' || self_healing_enabled || ',disabled_agents=' || disabled_agents::text
  INTO v_controls FROM public.self_healing_controls WHERE control_id = 'global';

  -- بوّابة المخاطر الحقيقية: risk_level<>'LOW' يستلزم requires_human_approval=true
  -- (قيد repair_playbooks_risk_approval_gate) — محاولة إدخال Playbook
  -- MEDIUM بموافقةٍ معطَّلة يجب أن تُرفَض فعلياً.
  BEGIN
    INSERT INTO public.repair_playbooks (
      playbook_id, name, description, incident_pattern, minimum_confidence, risk_level,
      allowed_actions, repair_steps, verification_steps, rollback_strategy, affected_scope,
      requires_human_approval
    ) VALUES (
      '__test_should_fail__', 'اختبار', 'اختبار', 'X', 90, 'MEDIUM',
      '["rerun_monitor_agent"]'::jsonb, '[]'::jsonb, '[]'::jsonb, 'n/a', 'ONE_AGENT', false
    );
    v_gate_test := 'FAIL — تم الإدخال رغم مخالفة بوّابة المخاطر!';
  EXCEPTION WHEN check_violation THEN
    v_gate_test := 'PASS — قيد repair_playbooks_risk_approval_gate رفض Playbook متوسط الخطورة بلا موافقةٍ إلزامية: ' || SQLERRM;
  END;

  -- نتيجة اختبار Shadow الحقيقي المُدرَج في p12a (لا يزال موجوداً هنا،
  -- سيُحذَف في p12c التالي):
  SELECT 'status=' || re.status || ',escalation_reason=' || coalesce(re.escalation_reason,'NULL')
    || ',preconditions_failed=' || (
      SELECT string_agg(e->>'name', '|') FROM jsonb_array_elements(re.preconditions_result) e WHERE (e->>'passed')='false'
    )
  INTO v_shadow_result
  FROM public.repair_executions re
  JOIN public.ops_incidents oi ON oi.id = re.incident_id
  WHERE oi.dedup_key = '__phase3_1_test__credit-monitor'
  ORDER BY re.started_at DESC LIMIT 1;

  RAISE EXCEPTION 'PHASE3_1_LIVE_EVIDENCE | TABLES: % | RLS: % | PLAYBOOKS: % | CONTROLS: % | RISK_GATE_TEST: % | SHADOW_TEST_RESULT: %',
    coalesce(v_tables,'NONE'), coalesce(v_rls,'NONE'), coalesce(v_playbooks,'NONE'),
    coalesce(v_controls,'NONE'), v_gate_test, coalesce(v_shadow_result,'NOT FOUND');
END $$;
