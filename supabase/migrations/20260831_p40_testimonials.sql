-- آراء المشتركين (شهادات المعلّمات) — تُعرض في قسم «آراء المشتركين» بصفحة
-- الترويج (cycle1-landing.html)، وتُدار من قسم «الترويج» الجديد في لوحة
-- الإدارة. is_published يسمح بإخفاء رأيٍ دون حذفه (مثلاً أثناء المراجعة).

CREATE TABLE IF NOT EXISTS public.testimonials (
  id           bigserial   PRIMARY KEY,
  teacher_name text        NOT NULL,
  quote        text        NOT NULL,
  is_published boolean     NOT NULL DEFAULT true,
  sort_order   int         NOT NULL DEFAULT 0,
  created_at   timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_testimonials_published_sort
  ON public.testimonials (is_published, sort_order, created_at DESC);

ALTER TABLE public.testimonials ENABLE ROW LEVEL SECURITY;

-- أي زائرٍ (anon) يقرأ الآراء المنشورة فقط — صفحة الترويج عامّة وبلا تسجيل دخول.
DROP POLICY IF EXISTS "testimonials_public_select" ON public.testimonials;
CREATE POLICY "testimonials_public_select" ON public.testimonials
  FOR SELECT TO anon, authenticated USING (is_published = true);

-- الإضافة والتعديل والحذف للمشرف فقط (لوحة الإدارة، قسم «الترويج»).
DROP POLICY IF EXISTS "testimonials_admin_insert" ON public.testimonials;
CREATE POLICY "testimonials_admin_insert" ON public.testimonials
  FOR INSERT TO authenticated WITH CHECK (is_app_admin());

DROP POLICY IF EXISTS "testimonials_admin_update" ON public.testimonials;
CREATE POLICY "testimonials_admin_update" ON public.testimonials
  FOR UPDATE TO authenticated USING (is_app_admin()) WITH CHECK (is_app_admin());

DROP POLICY IF EXISTS "testimonials_admin_delete" ON public.testimonials;
CREATE POLICY "testimonials_admin_delete" ON public.testimonials
  FOR DELETE TO authenticated USING (is_app_admin());

DROP POLICY IF EXISTS "testimonials_admin_select_all" ON public.testimonials;
CREATE POLICY "testimonials_admin_select_all" ON public.testimonials
  FOR SELECT TO authenticated USING (is_app_admin());

COMMENT ON TABLE public.testimonials IS
  'آراء المشتركين (شهادات المعلّمات) — تُعرض في صفحة الترويج، وتُدار من قسم «الترويج» بلوحة الإدارة.';

-- شهادتان حقيقيتان لبدء القسم بمحتوىً لا فراغ.
INSERT INTO public.testimonials (teacher_name, quote, sort_order)
SELECT * FROM (VALUES
  ('أ. مريم الحارثية', 'وفّرت عليّ «خُطّة» ساعاتٍ كل مساء — التحضير والألعاب تُولَّد من درسي نفسه، وما بقي عليّ إلا المراجعة.', 1),
  ('أ. سالمة البلوشية', 'أحسن ما فيها متابعة سلوك الطالبات: نجمةٌ بلمسة، وسجلٌّ كامل لكل طالبة أرجع إليه وقت الحاجة.', 2)
) AS v(teacher_name, quote, sort_order)
WHERE NOT EXISTS (SELECT 1 FROM public.testimonials);
