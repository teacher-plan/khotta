-- ════════════════════════════════════════════════════════════════════
-- تصحيح: الحصّة يجب أن تُحسب من تاريخ تفعيل كل حساب (allowed_emails.
-- added_at) إلى انتهائه (expires_at، خمسة أشهر) — لا من تاريخٍ عامٍّ واحد
-- لكل المعلّمات. القرار الصريح: "الرصيد يبقى من وقت تفعيل الحساب إلى خمس
-- أشهر قادمة ثم يتوقف بالحساب وينتهي الرصيد معه" — وانتهاء الحساب مضبوطٌ
-- أصلاً (20260818_p24_account_expiry.sql)، فلا حاجة لآلية إيقافٍ منفصلة؛
-- يكفي أن نقيس الاستهلاك من added_at بدل budget_period_start العامّ.
-- ════════════════════════════════════════════════════════════════════

CREATE OR REPLACE FUNCTION public.get_my_ai_budget()
RETURNS TABLE(used_usd numeric, budget_usd numeric, pct numeric)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_period date;
  v_budget_omr numeric;
  v_rate numeric;
  v_used numeric;
BEGIN
  IF auth.uid() IS NULL THEN
    RAISE EXCEPTION 'unauthenticated';
  END IF;

  -- تاريخ تفعيل حساب هذه المعلّمة تحديداً — لا تاريخٌ عامّ.
  SELECT ae.added_at::date INTO v_period
    FROM public.allowed_emails ae
    JOIN auth.users u ON lower(u.email) = lower(ae.email)
   WHERE u.id = auth.uid();

  -- سقوطٌ احترازي فقط: حسابٌ بلا صفٍّ في allowed_emails (حالةٌ غير متوقَّعة
  -- اليوم — الدخول أصلاً يمرّ عبرها) يرجع للتاريخ العامّ بدل خطأٍ صريح.
  IF v_period IS NULL THEN
    SELECT value::date INTO v_period FROM public.ai_settings WHERE key = 'budget_period_start';
    v_period := coalesce(v_period, '2026-01-01'::date);
  END IF;

  SELECT value::numeric INTO v_budget_omr FROM public.ai_settings WHERE key = 'budget_omr';
  SELECT value::numeric INTO v_rate FROM public.ai_settings WHERE key = 'usd_omr_rate';
  v_budget_omr := coalesce(v_budget_omr, 13);
  v_rate := coalesce(v_rate, 0.3845);

  SELECT coalesce(sum(cost_usd), 0) INTO v_used
    FROM public.ai_cost_log
   WHERE user_id = auth.uid() AND created_at >= v_period::timestamptz;

  budget_usd := round(v_budget_omr / v_rate, 4);
  used_usd := v_used;
  pct := CASE WHEN budget_usd > 0 THEN least(100, round(v_used / budget_usd * 100, 1)) ELSE 0 END;
  RETURN NEXT;
END;
$$;

COMMENT ON FUNCTION public.get_my_ai_budget() IS
  'رصيد المعلّمة الحالية فقط، محسوباً منذ تفعيل حسابها الخاص (allowed_emails.added_at) لا من تاريخٍ عام — يوافق مدّة اشتراكها (٥ أشهر) تماماً.';

-- تحقّق: select added_at from allowed_emails where lower(email)='<بريد اختبار>';
