-- ════════════════════════════════════════════════════════════════════
-- P1 — تقييدُ معدّل نداءات الذكاء الاصطناعي لكل مستخدمة (دفاعٌ إضافي)
--
-- الحصةُ الشهرية (take_quota) تمنع تجاوز السقف، لكنها لا تمنع معلّمةً
-- واحدة من إطلاق عشرة نداءاتٍ في اللحظة نفسها (كلّها ضمن حصتها) —
-- فتضرب OpenRouter بذروةٍ لحظية تُكلف أكثر مما تستحقّ الفائدة. هذه
-- طبقةٌ إضافية لا بديلة: تمنع النداء الثاني قبل مرور مهلةٍ قصيرة من
-- الأول، بصرف النظر عن الحصة المتبقية.
-- ════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.ai_rate_limit (
  user_id uuid PRIMARY KEY,
  last_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.ai_rate_limit ENABLE ROW LEVEL SECURITY;

-- لا سياسةَ قراءةٍ ولا كتابة: يُستدعى عبر الدالة أدناه بامتياز المُعرِّف
-- وحده — معلّمةٌ لا تستطيع تصفير مهلتها من المتصفح مباشرة.
REVOKE ALL ON public.ai_rate_limit FROM anon, authenticated;

-- يُرجع true إن سُمح بالنداء (ومُهلة الحماية بدأت الآن من جديد)، وfalse
-- إن كان النداء السابق أقرب من الحدّ. العبارة عبارةٌ ذرّيّة واحدة، كما
-- في take_quota تماماً: Postgres يقفل الصفّ فلا يتسابق نداءان متزامنان.
CREATE OR REPLACE FUNCTION public.check_ai_rate_limit(p_user uuid, p_min_ms int)
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_touched timestamptz;
  v_now timestamptz := clock_timestamp();
BEGIN
  INSERT INTO public.ai_rate_limit (user_id, last_at)
  VALUES (p_user, v_now)
  ON CONFLICT (user_id) DO UPDATE
    SET last_at = v_now
    WHERE public.ai_rate_limit.last_at <= v_now - make_interval(secs => p_min_ms / 1000.0)
  RETURNING last_at INTO v_touched;

  RETURN v_touched IS NOT NULL;
END;
$$;

REVOKE ALL ON FUNCTION public.check_ai_rate_limit(uuid, int) FROM PUBLIC, anon, authenticated;

COMMENT ON FUNCTION public.check_ai_rate_limit IS
  'حماية معدّل النداء لكل مستخدمة — طبقةٌ إضافية فوق الحصة الشهرية، لا بديلة عنها.';
