-- ════════════════════════════════════════════════════════════════════
-- حصّةٌ موحّدة بالريال العماني بدل ثلاث حصصٍ منفصلة (صور/نصّ/بحث)
--
-- القرار (نقاشٌ مع الإدارة): ١٣ ر.ع لكل معلّمة طوال الفصل الدراسي، تُستهلك
-- بحرّية عبر أي مزيجٍ من الصور/النصوص/البحث — لا حدودٌ منفصلة تُجبر توزيعاً
-- افتراضياً لا يطابق كيف تستعمل كل معلّمة المنصّة فعلياً. الفحص عند كل نداء:
-- «هل التراكم قبل هذا النداء بلغ الحدّ؟» — إن لا، يُسمح ويُكمَل النداء كاملاً
-- حتى لو تجاوز الحدّ بقليل (لا حجب في المنتصف)؛ فقط النداء التالي يُرفض.
-- ════════════════════════════════════════════════════════════════════

insert into public.ai_settings (key, value, updated_at) values
  ('budget_omr',          '13',         now()),
  ('usd_omr_rate',        '0.3845',     now()),  -- سعر الصرف الثابت الرسمي (لا يتقلّب)
  ('budget_period_start', current_date::text, now())
on conflict (key) do update set value = excluded.value, updated_at = excluded.updated_at;

-- من نُبِّهت فعلاً عند بلوغ ٨٠٪ — مرّةً واحدة لكل فترة (budget_period_start)،
-- لا رسالةً في كل تشغيلة cron بعد تجاوز الحدّ.
CREATE TABLE IF NOT EXISTS public.budget_alerts (
  user_id       uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  period_start  date NOT NULL,
  alert_80_sent_at timestamptz,
  updated_at    timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.budget_alerts ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.budget_alerts FROM anon, authenticated;  -- داخليٌّ: service_role فقط

COMMENT ON TABLE public.budget_alerts IS
  'يمنع تكرار بريد تجاوز ٨٠٪ لنفس المعلّمة في نفس الفصل — صفٌّ واحد لكل معلّمة، يُعاد تصفيره ضمنياً عند تغيّر budget_period_start.';

-- قراءة المعلّمة رصيدها الخاص فقط — بلا كشف ai_cost_log نفسه (يبقى داخلياً
-- بالكامل كما صُمِّم). SECURITY DEFINER يتجاوز REVOKE على ai_cost_log لكنه
-- لا يُرجع سوى مجموعٍ واحد محسوبٍ لمستخدم الجلسة الحالي — لا صفوف خام.
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

  SELECT value::date INTO v_period FROM public.ai_settings WHERE key = 'budget_period_start';
  SELECT value::numeric INTO v_budget_omr FROM public.ai_settings WHERE key = 'budget_omr';
  SELECT value::numeric INTO v_rate FROM public.ai_settings WHERE key = 'usd_omr_rate';
  v_budget_omr := coalesce(v_budget_omr, 13);
  v_rate := coalesce(v_rate, 0.3845);
  v_period := coalesce(v_period, '2026-01-01'::date);

  SELECT coalesce(sum(cost_usd), 0) INTO v_used
    FROM public.ai_cost_log
   WHERE user_id = auth.uid() AND created_at >= v_period::timestamptz;

  budget_usd := round(v_budget_omr / v_rate, 4);
  used_usd := v_used;
  pct := CASE WHEN budget_usd > 0 THEN least(100, round(v_used / budget_usd * 100, 1)) ELSE 0 END;
  RETURN NEXT;
END;
$$;

REVOKE ALL ON FUNCTION public.get_my_ai_budget() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION public.get_my_ai_budget() TO authenticated;

COMMENT ON FUNCTION public.get_my_ai_budget() IS
  'رصيد المعلّمة الحالية فقط (auth.uid())، ملخَّصاً كنسبةٍ مئوية — لا كشفَ لسجلّ التكلفة الخام.';

-- جدولة تنبيه ٨٠٪ عبر نفس آلية call_agent() القائمة — كل ٦ ساعات (نمط
-- credit-monitor)، والدالّة نفسها لا تُرسل إلا لمن عبرت ٨٠٪ ولم تُنبَّه بعد.
SELECT cron.schedule(
  'agent-budget-alert-check',
  '0 */6 * * *',
  $$SELECT public.call_agent('budget-alert-check')$$
);

-- تحقّق:
-- select key,value from ai_settings where key in ('budget_omr','usd_omr_rate','budget_period_start');
-- select proname from pg_proc where proname='get_my_ai_budget';
-- select jobname, schedule from cron.job where jobname='agent-budget-alert-check';
