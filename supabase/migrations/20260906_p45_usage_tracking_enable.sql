-- تفعيل تتبّع الاستخدام: كم مرّةً دخلت المعلّمة في اليوم، وأي الأقسام فتحت.
--
-- الجدول usage_tracking موجودٌ منذ 20260809_agents_system.sql بالشكل الصحيح
-- تماماً (event_type/feature_name/timestamp) لكنه بقي فارغاً: هجرة
-- 20260816_p0 فعّلت RLS بلا سياسات وسحبت الامتيازات من authenticated —
-- فلا المتصفّح يكتب فيه ولا أحدٌ يقرؤه. هذه الهجرة تفتح المسارين بحدّهما
-- الأدنى الضروري لا أكثر.
--
-- ⚠️ الحدّ الأدنى المقصود:
--   • المعلّمة تكتب صفوفها هي فقط (user_id = auth.uid() في WITH CHECK)،
--     ولا تملك SELECT إطلاقاً — فلا ترى نشاط غيرها ولا نشاطها نفسه.
--   • المشرف يقرأ الكل ولا يكتب شيئاً (لا سياسة INSERT له: البيانات تُولَّد
--     من الاستخدام الفعلي، وكتابةُ المشرف فيها تُفسد صدقها).
--   • لا UPDATE ولا DELETE لأحد: سجلٌّ أحداثٍ لا يُعدَّل بأثرٍ رجعي.

-- ① الكتابة: المعلّمة تسجّل حدثها هي وحدها
DROP POLICY IF EXISTS usage_insert_own ON public.usage_tracking;
CREATE POLICY usage_insert_own ON public.usage_tracking
  FOR INSERT TO authenticated
  WITH CHECK (user_id = auth.uid());

-- ② القراءة: المشرف فقط
DROP POLICY IF EXISTS usage_admin_select ON public.usage_tracking;
CREATE POLICY usage_admin_select ON public.usage_tracking
  FOR SELECT TO authenticated
  USING (is_app_admin());

-- ③ الامتيازات: INSERT فقط لـauthenticated (السياسة تحصره في صفوفها)،
--    وSELECT كذلك (سياسة المشرف وحدها هي التي تسمح بالقراءة فعلياً).
GRANT INSERT, SELECT ON public.usage_tracking TO authenticated;

-- ④ نطاقُ القيم: event_type حرٌّ اليوم فيقبل أي نصٍّ يُرسله المتصفّح.
--    نحصره في الأنواع الثلاثة المستعملة فعلاً حتى لا يتلوّث السجلّ بقيمٍ
--    عشوائية تُفسد التجميع لاحقاً (والقيدُ لا يكسر صفوفاً قائمة: الجدول فارغ).
ALTER TABLE public.usage_tracking DROP CONSTRAINT IF EXISTS usage_tracking_event_type_chk;
ALTER TABLE public.usage_tracking ADD CONSTRAINT usage_tracking_event_type_chk
  CHECK (event_type IN ('login', 'feature_used', 'content_viewed'));

-- ⑤ فهرسٌ مركّب للاستعلام الفعلي («نشاط معلّمةٍ بعينها في مدًى زمني»).
--    الفهرسان القائمان مفردان (user_id وحده، timestamp وحده) فلا يخدمان
--    الشرطين معاً بكفاءة.
CREATE INDEX IF NOT EXISTS idx_usage_tracking_user_time
  ON public.usage_tracking (user_id, timestamp DESC);

-- ⑥ حدُّ الاحتفاظ: دالّةٌ تحذف ما مضى عليه أكثر من ٩٠ يوماً. تُستدعى من
--    وكيلٍ مجدول لاحقاً (أو يدوياً)؛ بدونها ينمو الجدول بلا سقفٍ لأن كل
--    فتح قسمٍ يُنتج صفاً.
CREATE OR REPLACE FUNCTION public.prune_usage_tracking()
RETURNS integer
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE n integer;
BEGIN
  DELETE FROM public.usage_tracking WHERE timestamp < now() - interval '90 days';
  GET DIAGNOSTICS n = ROW_COUNT;
  RETURN n;
END;
$$;

COMMENT ON TABLE public.usage_tracking IS
  'سجلّ أحداث استخدام المعلّمات (دخول/فتح قسم). تكتب المعلّمة صفوفها هي فقط ولا تقرأ شيئاً؛ المشرف يقرأ الكل. يُقلَّم إلى ٩٠ يوماً عبر prune_usage_tracking().';

-- تحقّق: select policyname, cmd from pg_policies where tablename='usage_tracking';
--        يجب أن يظهر usage_insert_own (INSERT) وusage_admin_select (SELECT) فقط.
