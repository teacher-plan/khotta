-- ════════════════════════════════════════════════════════════════════
-- KHOTTA Autonomous Operations 2.0 — Phase 1
-- جدولة database-capacity-monitor عبر نفس آلية call_agent() القائمة
-- (20260816_p0_agent_cron_service_key.sql) — لا نظام جديد.
--
-- التكرار: كل 6 ساعات (كنمط credit-monitor). حجم قاعدة بيانات تعليمية
-- بهذا الحجم لا يتغيّر بما يبرر تكراراً أعلى (كـ*/5 دقائق لصحة النظام)،
-- لكن كل 6 ساعات كافٍ لبناء تاريخٍ ذي دلالة لحساب معدّل النمو خلال أيامٍ
-- قليلة، بكلفة SQL بحتة زهيدة (لا نداء LLM ولا API خارجي).
-- ════════════════════════════════════════════════════════════════════

SELECT cron.schedule(
  'agent-database-capacity-monitor',
  '0 */6 * * *',
  $$SELECT public.call_agent('database-capacity-monitor')$$
);

-- تحقّق: SELECT jobname, schedule, command FROM cron.job WHERE jobname = 'agent-database-capacity-monitor';
