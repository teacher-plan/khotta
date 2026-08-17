-- ════════════════════════════════════════════════════════════════════
-- Phase 3.2 FINAL — تحقّقٌ حيٌّ شامل: نتيجة اختبار Shadow النهائي +
-- REVOKE حقيقي عبر information_schema.role_table_grants (لا نصّ الملف
-- فقط) للأدوار anon/authenticated على الجداول الأربعة + تأكيد mode.
-- يفشل عمداً فيتراجع تلقائياً — لا أثر جانبي.
-- ════════════════════════════════════════════════════════════════════

DO $$
DECLARE
  v_shadow_result text;
  v_grants text;
  v_playbook_modes text;
BEGIN
  SELECT 'status=' || re.status || ',escalation_reason=' || coalesce(re.escalation_reason,'NULL')
    || ',preconditions=' || re.preconditions_result::text
  INTO v_shadow_result
  FROM public.repair_executions re
  JOIN public.ops_incidents oi ON oi.id = re.incident_id
  WHERE oi.dedup_key = '__phase3_2_final_test__credit-monitor'
  ORDER BY re.started_at DESC LIMIT 1;

  SELECT string_agg(table_name || '/' || grantee || '/' || privilege_type, ', ' ORDER BY table_name, grantee, privilege_type)
  INTO v_grants
  FROM information_schema.role_table_grants
  WHERE table_schema = 'public'
    AND table_name IN ('repair_playbooks','repair_executions','self_healing_controls','deployment_log')
    AND grantee IN ('anon','authenticated');

  SELECT string_agg(playbook_id || '=' || mode, ', ' ORDER BY playbook_id)
  INTO v_playbook_modes FROM public.repair_playbooks;

  RAISE EXCEPTION 'PHASE3_2_FINAL_EVIDENCE | SHADOW_RESULT: % | GRANTS_TO_anon_authenticated: % | PLAYBOOK_MODES: %',
    coalesce(v_shadow_result,'NOT FOUND'), coalesce(v_grants,'NONE — لا صلاحيات إطلاقاً'), coalesce(v_playbook_modes,'NONE');
END $$;
