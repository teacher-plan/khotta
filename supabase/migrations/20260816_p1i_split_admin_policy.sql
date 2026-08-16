-- محاولة عزل أخرى: استبدال سياسة FOR ALL بثلاث سياساتٍ منفصلة
-- (SELECT/UPDATE/DELETE) بدل ALL، تحسّباً لتعارضٍ بين FOR ALL وFOR INSERT
-- منفصلة على نفس الجدول.
DROP POLICY IF EXISTS pre_reg_admin_all ON public.pre_registrations;
CREATE POLICY pre_reg_admin_select ON public.pre_registrations
  FOR SELECT TO authenticated USING (public.is_app_admin());
CREATE POLICY pre_reg_admin_update ON public.pre_registrations
  FOR UPDATE TO authenticated USING (public.is_app_admin()) WITH CHECK (public.is_app_admin());
CREATE POLICY pre_reg_admin_delete ON public.pre_registrations
  FOR DELETE TO authenticated USING (public.is_app_admin());
