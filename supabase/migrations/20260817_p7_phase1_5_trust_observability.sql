-- ════════════════════════════════════════════════════════════════════
-- KHOTTA Autonomous Operations 2.0 — Phase 1.5
-- تصليب الثقة والملاحظة (Trust & Observability Hardening)
--
-- إضافيٌّ بالكامل: لا حذف ولا إعادة تسمية لأي عمود/جدول/قيمة قائمة.
-- كل تعديل أدناه ALTER ... ADD COLUMN IF NOT EXISTS أو CREATE TABLE IF
-- NOT EXISTS أو تحديثاتٌ تراكمية على قيود CHECK فقط (توسيع، لا تضييق).
-- ════════════════════════════════════════════════════════════════════

-- ─────────────────────────────────────────────────────────────────────
-- 1) ai_cost_log: عمودا correlation_id/run_id — لربط تكلفة كل نداء AI
--    (ops-analyze/ops-copilot، kind='ops') بتشغيلة agent_runs محدَّدة،
--    فيصير Agent → Run → Model → Tokens → Cost قابلاً للتتبّع فعلاً
--    (القسم 8 من مواصفة Phase 1.5). NULL على كل الصفوف القديمة.
-- ─────────────────────────────────────────────────────────────────────
ALTER TABLE public.ai_cost_log ADD COLUMN IF NOT EXISTS correlation_id uuid;
ALTER TABLE public.ai_cost_log ADD COLUMN IF NOT EXISTS run_id uuid;
CREATE INDEX IF NOT EXISTS idx_ai_cost_log_run_id ON public.ai_cost_log(run_id);

COMMENT ON COLUMN public.ai_cost_log.run_id IS
  'يربط سطر التكلفة بتشغيلة agent_runs (ops-analyze/ops-copilot) — إضافيٌّ، NULL على السجلّات قبل Phase 1.5 وعلى تكلفة المعلّمات (kind != ops) التي لا agent_runs لها أصلاً.';

-- ─────────────────────────────────────────────────────────────────────
-- 2) agent_registry: تسجيل ops-analyze وops-copilot كوكيلي AI عند-الطلب
--    (كانا مسجَّلين مسبقاً في Phase 1 — هذا فقط تأكيدٌ لا استبدال بفضل
--    ON CONFLICT DO NOTHING؛ يبقى للتوثيق أن كل الوكلاء التسعة مسجَّلون).
--    لا صفوف جديدة هنا فعلياً؛ INSERT محميٌّ بـON CONFLICT فقط تحسّباً.
-- ─────────────────────────────────────────────────────────────────────
-- (تُرك فارغاً عمداً — كل الوكلاء التسعة موجودون في Phase 1، تحقّقنا
--  بالقراءة المباشرة لا بافتراض، انظر التقرير القسم 3.)

-- ─────────────────────────────────────────────────────────────────────
-- 3) agent_runs.status: توسيعٌ تراكمي للقيم المسموحة — إضافة TIMEOUT/
--    SKIPPED كحالتين جديدتين (القسم 1 من المواصفة: run states) بجانب
--    RUNNING/SUCCESS/FAILED/PARTIAL القائمة، بلا حذفٍ لأيٍّ منها.
-- ─────────────────────────────────────────────────────────────────────
ALTER TABLE public.agent_runs DROP CONSTRAINT IF EXISTS agent_runs_status_check;
ALTER TABLE public.agent_runs ADD CONSTRAINT agent_runs_status_check
  CHECK (status IN ('RUNNING','SUCCESS','FAILED','PARTIAL','TIMEOUT','SKIPPED'));

-- ─────────────────────────────────────────────────────────────────────
-- 4) agent_runs.trigger: لا تغيير مطلوب — CRON/MANUAL/WEBHOOK/ON_DEMAND
--    تغطّي كل أنواع المشغِّلات الفعلية المكتشفة في هذه المرحلة (القسم 3).
-- ─────────────────────────────────────────────────────────────────────

-- ─────────────────────────────────────────────────────────────────────
-- 5) تحديث agent_registry.notes ليعكس ما أُصلح فعلاً في Phase 1.5 — لا
--    يبقى النصّ القديم موحياً بمشاكل مُصلَحة بالفعل (UPDATE لا DELETE،
--    والسطر القديم مذكورٌ بالكامل في تقرير Phase 1.5 للمراجعة).
-- ─────────────────────────────────────────────────────────────────────
UPDATE public.agent_registry SET notes =
  'Phase 1.5: تحقّق X-Telegram-Bot-Api-Secret-Token مكتوبٌ في الكود لكنه BLOCKED حتى يضبط المدير TELEGRAM_WEBHOOK_SECRET (سرّاً في Supabase) ويسجّله في setWebhook — راجع تقرير Phase 1.5 قسم الأسرار للأوامر الدقيقة. أزرار summary:refresh/credit:reschedule أصبحت تُعيد تشغيلاً حقيقياً للوكيل بدل ادّعاء نجاحٍ فارغ. files:retry_failed أصبح يصرّح بعدم توفّر إعادة المعالجة التلقائية بدل ادّعاء نجاحٍ كاذب. لا تعقّبٌ في agent_runs بعد (عشرات مخارج return المبكرة تجعل الإغلاق الآمن لكل تشغيلة عملاً أكبر من نطاق هذه المرحلة) — يبقى agent_logs/agent_messages مصدر السجلّ.'
  WHERE agent_id = 'telegram-webhook';

UPDATE public.agent_registry SET notes =
  'Phase 1.5: getPeakHoursSummary وgetAnalyticsSummary لم تعودا تُعيدان نصّاً ثابتاً مختلَقاً — الآن "البيانات غير متوفرة حالياً" صراحةً (لا مصدر بياناتٍ حقيقي لهما بعد). avgScore=4.2 الثابت استُبدل بمتوسطٍ محسوبٍ فعلياً من user_surveys.responses.rating، أو "غير متوفرة" إن لم توجد تقييماتٌ رقمية. أصبح يكتب تشغيلةً في agent_runs (Phase 1.5 إضافة).'
  WHERE agent_id = 'daily-summary';

UPDATE public.agent_registry SET notes =
  'العمود الفقري لرصد الحوادث؛ لا يصلح شيئاً، اكتشاف وتنبيه فقط. Phase 1.5: أصبح يكتب تشغيلةً في agent_runs، وحوادث ops_incidents الناتجة منه تحمل الآن source_agent وcorrelation_id.'
  WHERE agent_id = 'system-health-check';

-- تحقّق يدوي بعد التطبيق:
--   SELECT conname, pg_get_constraintdef(oid) FROM pg_constraint WHERE conname='agent_runs_status_check';
--   SELECT column_name FROM information_schema.columns WHERE table_name='ai_cost_log' AND column_name IN ('run_id','correlation_id');
