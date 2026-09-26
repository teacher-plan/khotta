-- ════════════════════════════════════════════════════════════════════
-- P56 — تخفيف تردّد وكلاء المراقبة الذاتية.
--
-- الخلفية: استعداداً للانتقال إلى الخطة المجانية (حوسبةٌ مشتركة محدودة)،
-- وبطلب الأستاذ عيسى: مع ١٢ مستخدماً فقط، ستُبلَّغ الإدارة بأي عطلٍ من
-- المستخدمين مباشرة، فلا حاجة لفحصٍ آليٍّ كل ٥ دقائق على مدار الساعة.
--
-- ما يُخفَّف (فحصٌ/مراقبةٌ بحتة، لا وظيفة مستخدمٍ مباشرة):
--   • agent-health-check:            كل ٥ دقائق  → كل ساعة
--   • agent-autonomous-scheduler:    كل ٥ دقائق  → كل ساعة
--   • agent-database-capacity-monitor: كل ٦ ساعات → مرّتين يومياً (كل ١٢ساعة)
--
-- ما يبقى بلا تغيير عمداً:
--   • agent-file-processor (كل ٣٠ دقيقة): اسمها 'file-processor-monitor'
--     لكنها تتابع معالجة ملفاتٍ فعلية يرفعها المستخدمون (لا مراقبةً صرفة) —
--     تخفيفها قد يؤخّر ظهور نتائج معالجةٍ حقيقية للمعلّمات.
--   • agent-budget-alert-check وagent-credit-monitor (كل ٦ ساعات): شبكة أمانٍ
--     مالية (تنبيه تجاوز ميزانية/نفاد رصيد) — قيمتها في اكتشاف مشكلةٍ ماليةٍ
--     قبل أن يكتشفها أحد، فالإبقاء عليها كما هي أنسب من تخفيفها.
--   • agent-daily-summary (يومياً): تقريرٌ واحدٌ في اليوم أصلاً، لا داعي لمسّه.
-- ════════════════════════════════════════════════════════════════════

select cron.alter_job(job_id, schedule := '0 * * * *')
  from cron.job where jobname = 'agent-health-check';

select cron.alter_job(job_id, schedule := '0 * * * *')
  from cron.job where jobname = 'agent-autonomous-scheduler';

select cron.alter_job(job_id, schedule := '0 */12 * * *')
  from cron.job where jobname = 'agent-database-capacity-monitor';
