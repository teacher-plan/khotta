-- نقل بيانات استهلاك الرصيد إلى نفس جدول مراقبة التخزين في لوحة الإدارة:
-- عمودٌ لتوسعة رصيد معلّمةٍ بعينها ($٥ في كل ضغطة، فوق الميزانية العامة
-- المشتركة budget_omr)، ودالّة مشرفٍ تُرجع استهلاك كل معلّمة الفعلي
-- بالدولار مقارنةً بميزانيتها (العامة + أي توسعةٍ خاصة).

ALTER TABLE public.user_storage_limits
  ADD COLUMN IF NOT EXISTS extra_budget_usd numeric NOT NULL DEFAULT 0;

COMMENT ON COLUMN public.user_storage_limits.extra_budget_usd IS
  'مبلغٌ إضافي بالدولار يُضاف فوق ميزانية الذكاء الاصطناعي العامة (budget_omr) لهذه المعلّمة تحديداً — يُزاد ٥$ في كل ضغطة "توسعة الرصيد" من لوحة الإدارة.';

CREATE OR REPLACE FUNCTION public.admin_get_ai_budget_usage()
RETURNS TABLE(user_id uuid, used_usd numeric, budget_usd numeric, pct numeric)
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_budget_omr numeric;
  v_rate numeric;
  v_base_budget numeric;
BEGIN
  IF NOT public.is_app_admin() THEN
    RAISE EXCEPTION 'not_authorized';
  END IF;

  SELECT value::numeric INTO v_budget_omr FROM public.ai_settings WHERE key = 'budget_omr';
  SELECT value::numeric INTO v_rate FROM public.ai_settings WHERE key = 'usd_omr_rate';
  v_budget_omr := coalesce(v_budget_omr, 13);
  v_rate := coalesce(v_rate, 0.3845);
  v_base_budget := round(v_budget_omr / v_rate, 4);

  RETURN QUERY
  SELECT
    u.id,
    coalesce(sum(acl.cost_usd) FILTER (WHERE acl.created_at >= ae.added_at::timestamptz), 0) AS used_usd,
    v_base_budget + coalesce(usl.extra_budget_usd, 0) AS budget_usd,
    CASE WHEN (v_base_budget + coalesce(usl.extra_budget_usd, 0)) > 0
      THEN least(100, round(
        coalesce(sum(acl.cost_usd) FILTER (WHERE acl.created_at >= ae.added_at::timestamptz), 0)
        / (v_base_budget + coalesce(usl.extra_budget_usd, 0)) * 100, 1))
      ELSE 0
    END AS pct
  FROM public.allowed_emails ae
  JOIN auth.users u ON lower(u.email) = lower(ae.email)
  LEFT JOIN public.user_storage_limits usl ON usl.user_id = u.id
  LEFT JOIN public.ai_cost_log acl ON acl.user_id = u.id
  WHERE ae.cycle = 'cycle1'
  GROUP BY u.id, ae.added_at, usl.extra_budget_usd;
END;
$$;

REVOKE ALL ON FUNCTION public.admin_get_ai_budget_usage() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION public.admin_get_ai_budget_usage() TO authenticated;

COMMENT ON FUNCTION public.admin_get_ai_budget_usage() IS
  'استهلاك كل معلّمة الفعلي بالدولار من ai_cost_log مقابل ميزانيتها (budget_omr العامة محوّلة للدولار + أي توسعةٍ خاصة usl.extra_budget_usd) — للمشرف فقط، تُستدعى من لوحة الإدارة (جدول مراقبة التخزين واستهلاك الرصيد).';
