-- ════════════════════════════════════════════════════════════════════
-- Phase 3.2 — إعادة اختبار Shadow حيّ بعد إصلاح الخللين (عمود
-- ops_incidents الخاطئ + قيمة الحالة 'OPEN' غير الموجودة)، ووعي النشر
-- الحقيقي الجديد (deployment_log). حادثةٌ اصطناعية آمنة موسومة، محفوظةٌ
-- فعلياً ثم مُنظَّفة (p14c) — نفس نمط p12a المُثبَت في Phase 3.1.
-- ════════════════════════════════════════════════════════════════════

INSERT INTO public.ops_incidents (
  dedup_key, component, severity, status, confidence,
  summary, evidence, source_agent, occurrence_count, first_seen_at, last_seen_at
) VALUES (
  '__phase3_2_test__credit-monitor',
  'credit-monitor', 'P2', 'DETECTED', 'VERIFIED',
  '[اختبارٌ آمن Phase 3.2] فشلٌ متكرّرٌ اصطناعي لغرض التحقّق الحيّ بعد الإصلاح',
  jsonb_build_array(jsonb_build_object('source','phase3_2_test','detail','3 فشلاتٍ اصطناعية بنفس رسالة الخطأ: TimeoutError')),
  'credit-monitor', 3, now() - interval '10 minutes', now()
)
RETURNING id;

DO $$
DECLARE
  v_incident_id uuid;
  v_similar_count int;
  v_action_enabled boolean;
  v_last_deploy timestamptz;
  v_minutes_since_deploy numeric;
  v_deploy_passed boolean;
  v_deploy_detail text;
  v_preconditions jsonb;
  v_any_failed boolean;
  v_status text;
  v_escalation text;
BEGIN
  SELECT id INTO v_incident_id FROM public.ops_incidents WHERE dedup_key = '__phase3_2_test__credit-monitor';

  -- الشرط المُصلَح: first_seen_at (لا created_at) + status <> 'RESOLVED' (لا IN ('OPEN','ESCALATED'))
  SELECT count(*) INTO v_similar_count FROM public.ops_incidents
    WHERE component = 'credit-monitor' AND status <> 'RESOLVED'
      AND first_seen_at >= now() - interval '30 minutes';

  SELECT enabled INTO v_action_enabled FROM public.safe_action_registry WHERE action_id = 'rerun_monitor_agent';

  -- الشرط المُصلَح: قراءةٌ حقيقية من deployment_log (لا passed=false ثابتة)
  SELECT deployed_at INTO v_last_deploy FROM public.deployment_log ORDER BY deployed_at DESC LIMIT 1;
  IF v_last_deploy IS NULL THEN
    v_deploy_passed := false;
    v_deploy_detail := 'لا سجلّ نشرٍ متاحٌ بعد في deployment_log — NOT_AVAILABLE، لا افتراض نجاح.';
  ELSE
    v_minutes_since_deploy := extract(epoch FROM (now() - v_last_deploy)) / 60;
    v_deploy_passed := v_minutes_since_deploy > 30;
    v_deploy_detail := format('آخر نشرٍ كان منذ %s دقيقة (cooldown=30) — %s', round(v_minutes_since_deploy,1),
      CASE WHEN v_deploy_passed THEN 'أقدم من النافذة، السياق مستقرّ.' ELSE 'ضمن النافذة، قد يكون السياق تغيَّر — هذا نشرٌ حقيقيٌّ حصل الآن فعلياً أثناء Phase 3.2 نفسها.' END);
  END IF;

  v_preconditions := jsonb_build_array(
    jsonb_build_object('name','same_function_same_error_pattern','passed', true, 'detail','رسالة خطأٍ واحدة ثابتة (TimeoutError) — سيناريو الاختبار.'),
    jsonb_build_object('name','failure_count_at_or_above_threshold','passed', true, 'detail','3 فشلاتٍ متتالية (الحدّ الأدنى 3).'),
    jsonb_build_object('name','last_known_success_exists','passed', true, 'detail','آخر نجاحٍ حقيقي لـcredit-monitor موجودٌ في agent_runs.'),
    jsonb_build_object('name','no_similar_incident_open_recently','passed', v_similar_count <= 1, 'detail', v_similar_count || ' حادثةٍ غير محلولة لنفس المكوّن آخر 30 دقيقة (بعد الإصلاح: first_seen_at + status<>RESOLVED).'),
    jsonb_build_object('name','no_recent_deployment_change','passed', v_deploy_passed, 'detail', v_deploy_detail),
    jsonb_build_object('name','agent_permitted_for_playbook','passed', true, 'detail','credit-monitor ضمن allowed_agents لـretry_monitor_known_timeout.'),
    jsonb_build_object('name','action_exists_in_registry','passed', (v_action_enabled IS NOT NULL), 'detail','rerun_monitor_agent موجودٌ في safe_action_registry.'),
    jsonb_build_object('name','action_enabled','passed', coalesce(v_action_enabled,false), 'detail', CASE WHEN v_action_enabled THEN 'مفعَّلٌ.' ELSE 'غير مفعَّلٍ أو غير موجود.' END)
  );

  v_any_failed := EXISTS (SELECT 1 FROM jsonb_array_elements(v_preconditions) e WHERE (e->>'passed') = 'false');

  IF v_any_failed THEN
    v_status := 'ESCALATED';
    SELECT string_agg(e->>'name','|') INTO v_escalation FROM jsonb_array_elements(v_preconditions) e WHERE (e->>'passed')='false';
    v_escalation := 'شرطٌ فشل: ' || v_escalation;
  ELSE
    v_status := 'WOULD_AUTO_HEAL';
    v_escalation := NULL;
  END IF;

  INSERT INTO public.repair_executions (
    incident_id, playbook_id, action_id, agent_id, mode, status,
    attempt_number, evidence_snapshot, preconditions_result, error, escalation_reason,
    blast_radius, confidence_at_decision, completed_at
  ) VALUES (
    v_incident_id, 'retry_monitor_known_timeout', 'rerun_monitor_agent', 'credit-monitor', 'SHADOW', v_status,
    1,
    jsonb_build_object('consecutive_failures', 3, 'distinct_errors', jsonb_build_array('TimeoutError'), 'agent_id', 'credit-monitor', 'test_scenario', true, 'phase', '3.2'),
    v_preconditions, NULL, v_escalation,
    jsonb_build_object('scope','ONE_AGENT','target','credit-monitor'), 85, now()
  );
END $$;
