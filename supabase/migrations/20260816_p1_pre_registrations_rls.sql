-- ════════════════════════════════════════════════════════════════════
-- P1 — تفعيل RLS على pre_registrations
--
-- الجدول لم يظهر قط في أي هجرة متتبَّعة (لا CREATE TABLE ولا ALTER
-- ENABLE ROW LEVEL SECURITY ولا CREATE POLICY) — أُنشئ يدوياً قبل أن
-- تبدأ الهجرات تتبُّع المخطّط. وحالته الفعلية في الإنتاج غير معروفة من
-- الشيفرة وحدها.
--
-- ولجدول pre_registrations استعمالان من المتصفح مباشرةً (لا دالّة حافة):
--   • landing.html:456   INSERT بمفتاح anon (نموذج التسجيل العام، قبل
--     أي حساب) — name, phone, email, stage, referred_by فقط.
--   • manager.html       SELECT * / UPDATE / DELETE بحساب المشرف
--     المصادَق — وحارسها اليوم isAdmin() في المتصفح وحده، وهو تحقّقٌ
--     تجميلي لا أمني: أي تبديلٍ في أدوات المطوّر يتجاوزه.
--
-- فإن كان RLS معطَّلاً أو سياسته مفتوحة، فأي معلّمةٍ مصادَقة تقرأ/تُعدّل/
-- تحذف بيانات كل من سجّل اهتمامه بالاشتراك (اسمٌ وهاتفٌ وبريد) بحساب
-- تدريسها العادي عبر sb.from('pre_registrations') من نافذة المتصفح —
-- بلا حاجة لحساب المشرف.
--
-- كل دوالّ الحافة (activate-teacher، registration-notifier،
-- telegram-webhook) تعمل بمفتاح الخدمة فتتجاوز RLS، فلا تتأثر بهذه
-- الهجرة إطلاقاً.
-- ════════════════════════════════════════════════════════════════════

ALTER TABLE public.pre_registrations ENABLE ROW LEVEL SECURITY;

-- إسقاطُ أي سياساتٍ سابقة أياً كان اسمها، فلا تبقى سياسةٌ أوسع تعمل
-- بجوار ما سنُنشئه (RLS تتّحد بـ OR، فبقاء سياسةٍ مفتوحة يُبطل التضييق).
DO $$
DECLARE p RECORD;
BEGIN
  FOR p IN SELECT policyname FROM pg_policies
            WHERE schemaname='public' AND tablename='pre_registrations'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON public.pre_registrations', p.policyname);
  END LOOP;
END;
$$;

-- الجمهورُ العام (anon) يُدرج طلب اشتراكٍ جديداً فقط — لا قراءة ولا
-- تعديل ولا حذف. والشرط يمنع تلقيم أعمدة الحالة الداخلية (account_email
-- إلخ) بقيمةٍ عند الإنشاء، فلا يُزوَّر تسجيلٌ يبدو مفعَّلاً بالفعل.
CREATE POLICY pre_reg_public_insert ON public.pre_registrations
  FOR INSERT TO anon
  WITH CHECK (
    account_email IS NULL
    AND (payment_status IS NULL OR payment_status = 'pending')
    AND notified_at IS NULL
    AND welcomed_at IS NULL
  );

-- المشرف وحده يقرأ ويعدّل ويحذف — لوحة الإدارة (manager.html) تعمل
-- بحساب المشرف المصادَق، والحارسُ صار في القاعدة لا في واجهة العرض.
CREATE POLICY pre_reg_admin_all ON public.pre_registrations
  FOR ALL TO authenticated
  USING (public.is_app_admin()) WITH CHECK (public.is_app_admin());

COMMENT ON TABLE public.pre_registrations IS
  'طلبات الاشتراك قبل تفعيل الحساب — anon يُدرج فقط، والقراءة والتعديل للمشرف حصراً عبر RLS (لا اعتماد على تحقّق الواجهة).';
