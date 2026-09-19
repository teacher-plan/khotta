-- ════════════════════════════════════════════════════════════════════
-- P51 — إصلاح ثلاثة أخطاءٍ ظهرت فعلياً في سجلّات Postgres (٧٢ ساعة):
--
-- ١) games.theme_id / c1_shared_assets.theme_id من نوع uuid بمفتاحٍ
--    أجنبيّ إلى game_themes(id)، لكن الثيمات المرسومة محلياً في الواجهة
--    (GM_SCENES في cycle1.html: 'sc-fort', 'sc-books'...) معرّفاتها
--    نصّيةٌ لا تُخزَّن في game_themes أصلاً — فحفظ أي لعبةٍ بثيمٍ مدمج
--    يفشل بخطأ "invalid input syntax for type uuid". العمود يتحوّل إلى
--    text بلا قيدٍ أجنبي؛ التحقّق من صحّة معرّف ثيمٍ من الخادم يبقى
--    مسؤولية الواجهة (تقرأ القائمة من game_themes أصلاً قبل العرض).
--
-- ٢) permission denied for function get_my_ai_budget: المنحة مُنحت في
--    ٢٠٢٦٠٨١٩_p29 لكن ٢٠٢٦٠٨١٩_p30 أعاد تعريف الدالّة (CREATE OR REPLACE)
--    بلا إعادة المنحة صراحةً بعده. تُعاد هنا بصرف النظر عن حالتها الحالية.
--
-- ٣) لا إصلاح لـ"column c1_survey_responses.id does not exist": الجدول
--    لا يملك عمود id أصلاً (مفتاحه survey_id+user_id) — هذا استعلامٌ
--    خاطئ في manager.html لا خللٌ في قاعدة البيانات، فيُصلَح هناك.
--
-- ملاحظة: نصائح المدقّق الأمنية (rls_enabled_no_policy على الجداول
-- الداخلية الخمسة) والأدائية (unindexed_foreign_keys) مقصودةٌ ومُوثَّقة —
-- ليست أخطاءً. انظر 20260816_p0_rls_internal_tables.sql: RLS مفعّلة بلا
-- سياسة = صفر وصولٍ من anon/authenticated عمداً، وservice_role يتجاوزها
-- بحكم تصميم Postgres. إضافة سياسةٍ هنا كانت ستُضعف الإقفال لا تُصلحه.
-- الفهارس الناقصة على action_approvals/action_executions تُضاف أدناه
-- بلا ضررٍ لأنها مجّانية على جداولٍ صغيرة، لا لأن غيابها كان عطلاً.
-- ════════════════════════════════════════════════════════════════════

-- ── ١) theme_id: uuid → text، بلا قيدٍ أجنبي ──
ALTER TABLE public.games
  DROP CONSTRAINT IF EXISTS games_theme_id_fkey;
ALTER TABLE public.games
  ALTER COLUMN theme_id TYPE text USING theme_id::text;

ALTER TABLE public.c1_shared_assets
  DROP CONSTRAINT IF EXISTS c1_shared_assets_theme_id_fkey;
ALTER TABLE public.c1_shared_assets
  ALTER COLUMN theme_id TYPE text USING theme_id::text;

COMMENT ON COLUMN public.games.theme_id IS
  'معرّف ثيمٍ مدمجٍ نصّيّ (sc-*، مرسومٌ في الواجهة) أو uuid نصّيّ من game_themes — لا قيد أجنبي، فالثيمات المدمجة لا تُخزَّن في الجدول.';
COMMENT ON COLUMN public.c1_shared_assets.theme_id IS
  'نفس معنى games.theme_id — انظر تعليقها.';

-- ── ٢) إعادة منح تنفيذ get_my_ai_budget صراحةً ──
REVOKE ALL ON FUNCTION public.get_my_ai_budget() FROM PUBLIC, anon;
GRANT EXECUTE ON FUNCTION public.get_my_ai_budget() TO authenticated;

-- ── فهارس مجانية لمفاتيحَ أجنبيةٍ غير مفهرسة (نصائح أداء INFO) ──
CREATE INDEX IF NOT EXISTS idx_action_approvals_action_id
  ON public.action_approvals(action_id);
CREATE INDEX IF NOT EXISTS idx_action_approvals_diagnosis_id
  ON public.action_approvals(diagnosis_id);
CREATE INDEX IF NOT EXISTS idx_action_executions_action_id
  ON public.action_executions(action_id);
CREATE INDEX IF NOT EXISTS idx_action_executions_approval_id
  ON public.action_executions(approval_id);
