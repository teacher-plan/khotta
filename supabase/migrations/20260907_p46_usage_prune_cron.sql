-- جدولة تقليم سجلّ الاستخدام (٩٠ يوماً) — يومياً.
--
-- الدالّة prune_usage_tracking() أُنشئت في p45 ولم تُجدوَل، فبقي التقليم
-- نظرياً: جدولٌ ينمو بصفٍّ لكل فتح قسمٍ لكل معلّمة يتضخّم بلا سقف إن لم
-- يُقلَّم فعلاً.
--
-- لماذا cron.schedule مباشرةً لا call_agent: الوكلاء الآخرون يستدعون دوالّ
-- حافةٍ عبر HTTP (تحتاج مفتاحاً وشبكة)، أمّا هذه فدالّة SQL خالصة داخل
-- القاعدة نفسها — فاستدعاؤها مباشرةً أبسط وأقلّ عرضةً للعطل، ولا يحتاج
-- تسجيلاً في agent_registry (وغيابُه منه كان سيُفشل كل تشغيلةٍ بقيد
-- foreign key، كما وقع فعلاً مع budget-alert-check سابقاً).
--
-- التوقيت: ٢:٣٠ فجراً بتوقيت مسقط (22:30 UTC) — خارج ساعات عمل المعلّمات
-- تماماً، فحذفُ آلاف الصفوف لا يزاحم استخدامهنّ.

SELECT cron.unschedule('prune-usage-tracking')
WHERE EXISTS (SELECT 1 FROM cron.job WHERE jobname = 'prune-usage-tracking');

SELECT cron.schedule(
  'prune-usage-tracking',
  '30 22 * * *',
  $$SELECT public.prune_usage_tracking()$$
);

-- تحقّق:
-- select jobname, schedule, command from cron.job where jobname='prune-usage-tracking';
-- select public.prune_usage_tracking();  -- يُعيد عدد الصفوف المحذوفة (٠ الآن، الجدول حديث)
