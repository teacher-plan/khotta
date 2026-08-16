-- عزلٌ مؤقّت: هل السبب شرط WITH CHECK نفسه أم شيءٌ بنيويّ آخر؟
-- تعطيل الشرط مؤقتاً (true) للاختبار فقط — سنُعيده فوراً بعد التشخيص.
DROP POLICY IF EXISTS pre_reg_public_insert ON public.pre_registrations;
CREATE POLICY pre_reg_public_insert ON public.pre_registrations
  FOR INSERT TO anon
  WITH CHECK (true);
