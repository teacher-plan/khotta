-- ════════════════════════════════════════════════════════════════════
-- KHOTTA Autonomous Management — Phase 0: تسجيل تكلفة الذكاء الاصطناعي
--
-- كل دالّةٍ من الثمان التي تستهلك حصةً (generate-lesson-plan، generate-
-- chat، generate-exam، generate-exam-vision، generate-game-content،
-- generate-infographic، extract-roster، summarize-lesson-pages) تستلم
-- usage.cost حقيقياً من OpenRouter في كل استجابة، وتُرجعه للعميل — ولا
-- تحفظه في أي مكان. فلا سبيل اليوم لمعرفة: كم أنفقنا هذا الشهر؟ من أكثر
-- المعلّمات استهلاكاً؟ أي ميزةٍ أغلى؟ أي نموذجٍ أُخذ منه أكثر؟
--
-- هذه الهجرة تُنشئ جدول تسجيلٍ صرفاً (observability) — لا تمسّ take_quota
-- ولا refund_quota ولا check_ai_rate_limit ولا أي منطق حصةٍ أو تقييد
-- معدّل. مصدر cost_usd الوحيد هو usage.cost القادم من OpenRouter نفسه —
-- لا تقدير ولا جدول أسعار محليّ.
-- ════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.ai_cost_log (
  id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       uuid        REFERENCES auth.users(id) ON DELETE CASCADE,
  function_name text        NOT NULL,   -- اسم دالّة الحافة: 'generate-lesson-plan' إلخ
  kind          text        NOT NULL,   -- 'text' أو 'img' أو 'search' — نفس مفردات ai_usage.kind
  model         text,                   -- النموذج الفعليّ الذي نُفِّذ به الاستدعاء
  -- عشرة منازل عشرية: تكاليف OpenRouter الحقيقية المُلاحَظة تصل إلى
  -- ٠٫٠٠٠٢٥٥٥٩٨٢ للاستدعاء الواحد — تقريبٌ بأقل من ذلك يُفقِد الدقّة.
  -- NULL صراحةً لا صفر: صفرٌ مُخترَع يبدو استدعاءً بلا تكلفة، وNULL وحده
  -- يقول «لم نستطع القراءة» بصدق. لا قيد NOT NULL هنا لهذا السبب بالذات.
  cost_usd      numeric(14,10),
  created_at    timestamptz NOT NULL DEFAULT now()
);

-- فهارس مبنيّةٌ على الاستعمال المعروف مسبقاً فقط (Section 5 من طلب المرحلة):
--   • user_id      → GROUP BY user_id (أكثر المعلّمات استهلاكاً، تكلفة كل مستخدم)
--   • function_name → GROUP BY function_name (تكلفة كل ميزة/دالّة حافة)
--   • model         → GROUP BY model (تكلفة كل نموذج — طُلب صراحةً في القائمة)
--   • created_at DESC → WHERE created_at BETWEEN ... (تقارير يومية/شهرية،
--     والأحدث أولاً لأن التقارير تُقرأ من الأحدث إلى الأقدم غالباً)
-- لا فهرس على kind: أساساً كارديناليةٌ منخفضة (ثلاث قيمٍ فقط) ولن يُستَعلَم
-- عنه منفرداً — إضافته الآن تخمينٌ لا حاجة.
CREATE INDEX IF NOT EXISTS idx_ai_cost_log_user_id       ON public.ai_cost_log (user_id);
CREATE INDEX IF NOT EXISTS idx_ai_cost_log_function_name ON public.ai_cost_log (function_name);
CREATE INDEX IF NOT EXISTS idx_ai_cost_log_model          ON public.ai_cost_log (model);
CREATE INDEX IF NOT EXISTS idx_ai_cost_log_created_at     ON public.ai_cost_log (created_at DESC);

ALTER TABLE public.ai_cost_log ENABLE ROW LEVEL SECURITY;

-- جدولٌ داخليّ للعمليات صرفاً — بلا أي سياسة، تماماً كنمط الجداول الداخلية
-- الثلاثة عشر في 20260816_p0_rls_internal_tables.sql (health_checks،
-- error_logs، إلخ): service_role يتجاوز RLS بحكم تصميم Postgres، فالوكلاء
-- ودالّة التسجيل تعملان بلا تعديل؛ وanon وauthenticated بلا سياسة = صفر
-- صفوف. لا سياسة "اقرئي تكلفة طلباتك الخاصة" — لا يوجد لها نظيرٌ قائم في
-- المنصّة اليوم (ai_usage تكشف عدد الطلبات لا تكلفتها بالدولار)، فلا تُضاف
-- الآن دون سببٍ من الواجهة الفعلية.
REVOKE ALL ON public.ai_cost_log FROM anon, authenticated;

COMMENT ON TABLE public.ai_cost_log IS
  'سجلّ تكلفة كل نداء ذكاءٍ اصطناعي ناجح — قراءةٌ صرفة من usage.cost عند OpenRouter، لا تقدير. داخليٌّ بالكامل: service_role فقط، لا يُقرأ من المتصفح.';
COMMENT ON COLUMN public.ai_cost_log.cost_usd IS
  'usage.cost كما أعادته OpenRouter حرفياً. NULL يعني أن الاستجابة لم تتضمّن رقماً صالحاً — لا تُقدَّر قيمةٌ بديلة أبداً.';
