-- ════════════════════════════════════════════════════════════════════
-- KHOTTA Autonomous Operations 2.0 — Phase 2
-- تسجيل ops-actions في agent_registry — القسم 16: مستوى استقلالٍ صريح.
-- SAFE_ACTION/Level 3 فقط لأن كل تنفيذٍ فعلي يمرّ عبر بوّابة موافقةٍ/سقف
-- محاولةٍ في الكود (opsActionRegistry.ts) — لا Level 4/5 في هذه المرحلة.
-- ════════════════════════════════════════════════════════════════════
INSERT INTO public.agent_registry
  (agent_id, display_name, description, agent_type, status, version,
   schedule_cron, trigger_kind, autonomy_level, permission_level, allowed_actions, notes)
VALUES
  ('ops-actions', 'محرّك التشخيص والإجراءات الآمنة', 'تشخيصٌ حتميّ/LLM لحوادث ops_incidents، تقييم خطورة، وتنفيذ إجراءاتٍ من safe_action_registry حصراً بموافقة مشرفٍ عند الحاجة — لا SQL حرّ ولا تنفيذ خارج السجلّ.',
   'AI_ANALYST', 'ACTIVE', '2.0.0', NULL, 'ON_DEMAND', 3, 'SAFE_ACTION',
   '["diagnose_incident","request_safe_action","execute_registered_action","verify_action_result"]'::jsonb,
   'Phase 2: أول وكيلٍ يصل Level 3 (SAFE_ACTION) في المشروع — إجراءاته الاثنان الوحيدان المسجَّلان (rerun_monitor_agent، reschedule_daily_summary) كلاهما LOW risk، بلا موافقةٍ مطلوبة بحسب السجلّ حالياً، وبسقف محاولةٍ آليةٍ واحدة لكل حادثة. لا Level 4/5 في هذه المرحلة — ممنوعٌ صراحةً بالمواصفة.')
ON CONFLICT (agent_id) DO NOTHING;
