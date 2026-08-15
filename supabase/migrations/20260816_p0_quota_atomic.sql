-- ════════════════════════════════════════════════════════════════════
-- P0/٥ — جعلُ خصم الحصص ذرّيّاً (atomic)
--
-- كان takeQuota يقرأ العدّاد ثم يكتبه في خطوتين منفصلتين:
--     SELECT count …            ← الطلبان يقرآن ٦٤ معاً
--     if (used >= limit) …      ← كلاهما يمرّ
--     UPDATE count = used + 1   ← كلاهما يكتب ٦٥
-- فعشرة طلباتٍ متزامنة على آخر نقطةٍ في الرصيد تمرّ كلُّها، والعدّاد يزيد
-- واحداً فقط — أي توليدٌ مدفوعٌ بلا حدٍّ عند الحافّة تماماً.
--
-- العلاج: عبارةُ UPDATE واحدة يحرسها الشرط داخلها. Postgres يقفل الصفّ
-- طوال العبارة، فالطلب الثاني ينتظر ثم يقرأ القيمة المحدَّثة لا القديمة.
-- ON CONFLICT DO UPDATE يجعل أول طلبٍ في الشهر ذرّيّاً كذلك، فلا يتسابق
-- طلبان على INSERT فيفشل أحدهما بخرق المفتاح.
-- ════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.ai_usage (
  user_id uuid  NOT NULL,
  month   text  NOT NULL,
  kind    text  NOT NULL,
  count   int   NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, month, kind)
);
ALTER TABLE public.ai_usage ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "usage_read_own" ON public.ai_usage;
CREATE POLICY "usage_read_own" ON public.ai_usage
  FOR SELECT TO authenticated USING (user_id = auth.uid());

-- لا سياسةَ كتابةٍ إطلاقاً: الخصم يمرّ عبر الدالة أدناه بمفتاح الخدمة وحده،
-- فلا تستطيع معلّمةٌ أن تُصفّر عدّادها بـ UPDATE مباشر من المتصفّح.
REVOKE INSERT, UPDATE, DELETE ON public.ai_usage FROM anon, authenticated;

-- ── الخصم الذرّي ─────────────────────────────────────────────────────
-- يُرجع صفّاً واحداً: allowed (هل سُمح؟) و used (بعد الخصم) و lim.
CREATE OR REPLACE FUNCTION public.take_quota(
  p_user  uuid,
  p_month text,
  p_kind  text,
  p_limit int
)
RETURNS TABLE(allowed boolean, used int, lim int)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_new int;
BEGIN
  -- محاولةُ الخصم: تنجح فقط إن بقي متّسع. الشرط داخل العبارة نفسها،
  -- فالقراءة والقرار والكتابة لحظةٌ واحدة لا ثلاث.
  INSERT INTO public.ai_usage (user_id, month, kind, count)
  VALUES (p_user, p_month, p_kind, 1)
  ON CONFLICT (user_id, month, kind) DO UPDATE
    SET count = public.ai_usage.count + 1
    WHERE public.ai_usage.count < p_limit
  RETURNING count INTO v_new;

  IF v_new IS NOT NULL THEN
    RETURN QUERY SELECT true, v_new, p_limit;
    RETURN;
  END IF;

  -- لم يُرجَع صفّ = شرطُ WHERE سقط = الحدُّ مستنفَد. نقرأ الرصيد للعرض.
  SELECT c.count INTO v_new FROM public.ai_usage c
   WHERE c.user_id = p_user AND c.month = p_month AND c.kind = p_kind;
  RETURN QUERY SELECT false, COALESCE(v_new, p_limit), p_limit;
END;
$$;

-- ── الاسترجاع الذرّي ────────────────────────────────────────────────
-- GREATEST يمنع النزول تحت الصفر مهما تزامنت الاستدعاءات، فلا يصنع
-- استرجاعٌ متكرّرٌ رصيداً من العدم.
CREATE OR REPLACE FUNCTION public.refund_quota(
  p_user  uuid,
  p_month text,
  p_kind  text
)
RETURNS void
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
  UPDATE public.ai_usage
     SET count = GREATEST(count - 1, 0)
   WHERE user_id = p_user AND month = p_month AND kind = p_kind;
$$;

-- الدالّتان تعملان بامتياز المُعرِّف، فلا تُتركان مستدعاتين من المتصفّح.
REVOKE ALL ON FUNCTION public.take_quota(uuid, text, text, int)  FROM PUBLIC, anon, authenticated;
REVOKE ALL ON FUNCTION public.refund_quota(uuid, text, text)     FROM PUBLIC, anon, authenticated;

COMMENT ON FUNCTION public.take_quota IS
  'خصمٌ ذرّيّ لحصّة الذكاء الاصطناعي — عبارةٌ واحدة يحرسها count < limit داخلها.';
