-- عدّاد زياراتٍ داخلي لصفحة الترويج (بلا خدمة تحليلات خارجية): كل فتحٍ
-- للصفحة يسجّل صفاً واحداً — لا بيانات شخصية، فقط اسم الصفحة وكود
-- الإحالة (إن وُجد) وتوقيت الزيارة. يُستخدَم لحساب نسبة التحويل
-- (تسجيلات ÷ زيارات) في لوحة الإدارة.

CREATE TABLE IF NOT EXISTS public.page_views (
  id         bigserial   PRIMARY KEY,
  page       text        NOT NULL DEFAULT 'cycle1-landing',
  ref        text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_page_views_page_created ON public.page_views (page, created_at DESC);

ALTER TABLE public.page_views ENABLE ROW LEVEL SECURITY;

-- أي زائرٍ (anon) يستطيع تسجيل زيارته — لا يستطيع قراءة أي صفٍّ (لا سياسة
-- SELECT لغير المشرف)، فلا يكشف عدد الزيارات لغير الإدارة.
DROP POLICY IF EXISTS "pageviews_anon_insert" ON public.page_views;
CREATE POLICY "pageviews_anon_insert" ON public.page_views
  FOR INSERT TO anon, authenticated WITH CHECK (true);

DROP POLICY IF EXISTS "pageviews_admin_select" ON public.page_views;
CREATE POLICY "pageviews_admin_select" ON public.page_views
  FOR SELECT TO authenticated USING (is_app_admin());

COMMENT ON TABLE public.page_views IS
  'عدّاد زياراتٍ داخلي بسيط — لا بيانات شخصية، فقط page/ref/created_at. يُستخدم لحساب نسبة التحويل في لوحة الإدارة.';
