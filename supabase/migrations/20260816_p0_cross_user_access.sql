-- ════════════════════════════════════════════════════════════════════
-- P0/٤ — منعُ الوصول العابر بين المستخدمات
-- ════════════════════════════════════════════════════════════════════

-- ① allowed_emails — إسقاطُ السياسة المفتوحة ‏anyone_can_check‏
-- ‏using(true)‏ كانت تُبطل allowed_own_select تماماً، فأيّ معلّمة تقرأ قائمة
-- بُرد كلِّ المسجَّلات. وُعِد بإسقاطها في cleanup_duplicates.sql فلم يحدث.
--
-- تحقّقٌ قبل الإسقاط: كلُّ قراءةٍ في الشيفرة تسأل عن بريد صاحبها وحده
--   cycle1.html:3490  ‏.ilike('email', userEmail).maybeSingle()‏
--   index.html:4558   المِثل
-- وallowed_own_select يغطّي هذه الحالة (بريدُ الذات أو المشرف)، فلا يتعطّل
-- تسجيل الدخول.
DROP POLICY IF EXISTS anyone_can_check ON public.allowed_emails;

-- ② c1_notifications — جعلُ المرسِل غير قابلٍ للانتحال
--
-- ⚠️ قراءةٌ دقيقة قبل التضييق: ‏with check(true)‏ ليست خطأً محضاً — للمنصّة
-- استعمالان مشروعان يُنشئان تنبيهاً لمستخدمٍ آخر:
--   cycle1.html:10774  معلّمةٌ تُقيّم ملف زميلتها → تنبيهٌ لصاحبة الملف
--   cycle1.html:11119  مشاركةُ ملفٍ في المكتبة → تنبيهٌ عامّ (user_id=NULL)
-- فحصرُ الإدراج في ‏user_id = auth.uid()‏ كان يكسر الميزتين معاً.
--
-- الخطر الحقيقي ليس الإدراج بل الانتحال: رسالةٌ تُكتب «رسالة من الإدارة».
-- فالعلاج أن نختم كلَّ تنبيهٍ بهويّة كاتبه ختماً لا يُزوَّر — المُشغِّل
-- يكتب البريد من الرمز المميَّز لا مما أرسله المتصفّح، فيُستبدل أيُّ قيمةٍ
-- ملفَّقة بالحقيقة.
ALTER TABLE public.c1_notifications
  ADD COLUMN IF NOT EXISTS sender_id uuid;

CREATE OR REPLACE FUNCTION public.c1notif_stamp_sender()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  -- auth.uid() فارغٌ لمفتاح الخدمة (تنبيهات الإدارة من manager.html تمرّ
  -- بحساب المشرف المصادَق، فتُختم باسمه؛ وما يأتي من دوال الحافة يبقى NULL).
  NEW.sender_id  := auth.uid();
  IF auth.uid() IS NOT NULL THEN
    NEW.created_by := auth.jwt()->>'email';
  END IF;
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS c1notif_stamp ON public.c1_notifications;
CREATE TRIGGER c1notif_stamp
  BEFORE INSERT ON public.c1_notifications
  FOR EACH ROW EXECUTE FUNCTION public.c1notif_stamp_sender();

-- والإدراج يبقى مسموحاً للمصادَقات (وإلّا تعطّلت الميزتان)، لكنه صار
-- منسوباً. ويُمنع أن تدّعي معلّمةٌ أن التنبيه من النظام.
DROP POLICY IF EXISTS "c1notif_insert_any" ON public.c1_notifications;
CREATE POLICY "c1notif_insert_attributable" ON public.c1_notifications
  FOR INSERT TO authenticated WITH CHECK (true);

COMMENT ON COLUMN public.c1_notifications.sender_id IS
  'هويّةُ المُدرِج — يختمها المُشغِّل من الرمز المميَّز فلا تُزوَّر من المتصفّح.';

-- ③ c1lib_storage_insert — قصرُ الرفع على المسار المقصود
--
-- ملاحظةٌ على تقرير التدقيق: قال إنّ معلّمةً ترفع «داخل مسار معلّمةٍ أخرى»،
-- والحقيقة أنّ المسار لا يحمل هويّةً أصلاً:
--   cycle1.html:11095  ‏'c1-library/'+slug(subject)+'/'+Date.now()+'_'+safe‏
-- فلا مسارَ لأحدٍ ليُقتحَم. والحذف محميٌّ فعلاً بـ ‏owner = auth.uid()‏.
-- ما يبقى فعلاً: لا سقفَ على الامتداد. نمنع رفع ملفٍّ تنفيذيّ أو صفحةٍ
-- تعمل من نطاق المشروع نفسه (وهو مسلكُ XSS مخزَّن حقيقيّ).
DROP POLICY IF EXISTS "c1lib_storage_insert" ON storage.objects;
CREATE POLICY "c1lib_storage_insert" ON storage.objects
  FOR INSERT TO authenticated
  WITH CHECK (
    bucket_id = 'library-files'
    AND name LIKE 'c1-library/%'
    AND lower(name) !~ '\.(html?|xhtml|svg|js|mjs|wasm|php|sh)$'
  );
