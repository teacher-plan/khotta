-- ════════════════════════════════════════════════════════════════════
-- إصلاح خطأين حقيقيّين متكرّرين، مكتشفين من سجلّات Postgres الحقيقية
-- (اللوحة أظهرت ٧٨ خطأً؛ التحقيق ميّز الحقيقي من ضجيج تحقيقاتنا نفسها).
--
-- ١) budget-alert-check لم يُسجَّل في agent_registry عند بنائه أمس —
--    فكل استدعاء startRun() يفشل بقيد foreign key على agent_runs.agent_id.
--    الوكيل نفسه يعمل غالباً (فشل التسجيل لا يمنع منطقه)، لكن بلا أثرٍ في
--    agent_runs. هذه الهجرة تسجّله فقط؛ الكود لم يتغيّر.
-- ٢) خطأ "column emergency_alerts.id does not exist" أُصلح في الكود
--    (system-health-check/index.ts) — العمود الحقيقي هو alert_id، لا id.
--    هذه الهجرة توثيقٌ فقط، لا تعديل قاعدة بيانات يلزمه.
-- ════════════════════════════════════════════════════════════════════

INSERT INTO public.agent_registry
  (agent_id, display_name, description, agent_type, status, version,
   schedule_cron, trigger_kind, autonomy_level, permission_level, allowed_actions, notes)
VALUES
  ('budget-alert-check', 'تنبيه حصّة الذكاء الاصطناعي', 'يفحص كل 6 ساعات من عبرت ٨٠٪ من حصّتها الفصلية (١٣ ر.ع من تفعيل حسابها) ويرسل بريد تنبيهٍ مرّةً واحدة لكل فترة.',
   'MONITOR', 'ACTIVE', '1.0.0', '0 */6 * * *', 'CRON', 1, 'WRITE_LIMITED',
   '["read_ai_cost_log","read_allowed_emails","send_email","write_budget_alerts"]'::jsonb,
   'قراءةٌ وتنبيهٌ بالبريد فقط؛ لا يعدّل رصيد أي معلّمة ولا يحجب توليداً.')
ON CONFLICT (agent_id) DO NOTHING;

-- تحقّق: select agent_id from agent_registry where agent_id='budget-alert-check';
