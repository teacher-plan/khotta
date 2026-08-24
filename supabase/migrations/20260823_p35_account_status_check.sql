-- بعد انتهاء صلاحية حسابٍ (allowed_emails.expires_at)، سياسة allowed_own_select
-- تُخفي الصفّ عن صاحبته عمداً (انظر 20260818_p24_account_expiry.sql) — فتُرفَض
-- بنفس رسالة «البريد غير مصرّح له بالدخول» التي تظهر لمن لم تُسجَّل قط. هذه
-- الدالّة تفتح استثناءً ضيّقاً جداً: تسمح للمعلّمة بمعرفة أن حسابها *كان*
-- موجوداً وانتهى تحديداً (لا أي تفصيلٍ آخر)، حتى تعرض لها الواجهة رسالةً
-- مفيدة بدل الرسالة العامة المُلبِسة.
--
-- SECURITY DEFINER يتجاوز RLS عمداً هنا — نفس نمط get_my_ai_budget() القائم.
-- الأمان: لا معامل إدخال إطلاقاً (تقرأ بريد المستدعي من جلسته فقط عبر
-- auth.jwt()، فلا تستطيع أي مستخدمة الاستعلام عن بريد غيرها)، والمُخرَج
-- محصورٌ بثلاث حالاتٍ مجرَّدة (not_found / active / expired) مع حالة الدفع
-- عند الانتهاء فقط — لا تسريب لأي عمودٍ آخر من الصفّ.
CREATE OR REPLACE FUNCTION public.check_my_account_status()
RETURNS jsonb
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_email text := lower(auth.jwt()->>'email');
  v_expires_at timestamptz;
  v_found boolean;
  v_payment text;
BEGIN
  IF v_email IS NULL OR v_email = '' THEN
    RETURN jsonb_build_object('status', 'not_found');
  END IF;

  SELECT true, expires_at INTO v_found, v_expires_at
  FROM public.allowed_emails
  WHERE lower(email) = v_email
  LIMIT 1;

  IF NOT FOUND THEN
    RETURN jsonb_build_object('status', 'not_found');
  END IF;

  IF v_expires_at IS NOT NULL AND v_expires_at <= now() THEN
    SELECT payment_status INTO v_payment
    FROM public.pre_registrations
    WHERE lower(email) = v_email
    ORDER BY created_at DESC
    LIMIT 1;

    RETURN jsonb_build_object('status', 'expired', 'payment_status', COALESCE(v_payment, 'pending'));
  END IF;

  RETURN jsonb_build_object('status', 'active');
END;
$$;

GRANT EXECUTE ON FUNCTION public.check_my_account_status() TO authenticated;

-- تحقّق: SELECT public.check_my_account_status(); -- بجلسة المشرف يُعيد not_found (لا صفّ للمشرف في allowed_emails)
