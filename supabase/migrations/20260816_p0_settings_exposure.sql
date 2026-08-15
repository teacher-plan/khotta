-- ════════════════════════════════════════════════════════════════════
-- P0 (مُكتشَفٌ بالفحص الحيّ لا بقراءة الهجرات) — قصرُ ai_settings على
-- المفاتيح التي تحتاجها الواجهة فعلاً.
--
-- ثبت بالتجربة على الإنتاج، بالمفتاح العامّ وحده (المنسوخ من مصدر الصفحة):
--     GET /rest/v1/ai_settings?select=key  →  200، ستةٌ وثلاثون مفتاحاً
-- وفيها ما لا يخصّ المتصفّح:
--   • per_teacher_usd و teacher_count — أرقامُ عملٍ تجاريّ (كلفةُ المعلّمة
--     وعددُ المشتركات) يقرؤها أيُّ زائر.
--   • ppt_system_prompt — موجِّهُ النظام، وهو ملكيّةٌ فكريّة.
--   • model_* و slide_model — أيُّ النماذج تُستعمل وأين.
--
-- ولا يجوز إقفالُ الجدول كلَّه: صفحة المعلّمة تقرأ منه أربعةَ مفاتيح عبر
-- ‏c1Setting()‏ (cycle1.html:4051) وهي: quota_text و quota_img و
-- c1_tt_defaults و game_cfg — تحقّقٌ بمسحٍ شاملٍ للملف، ولا مسلكَ آخر.
-- فالقصرُ على قائمةٍ بيضاء لا الإقفال.
-- ════════════════════════════════════════════════════════════════════

ALTER TABLE public.ai_settings ENABLE ROW LEVEL SECURITY;

-- السياساتُ القديمة المفتوحة — أياً كان اسمها — تُسقَط أولاً، وإلّا بقيت
-- الأوسعُ منها تعمل بجوار الجديدة فلا يتغيّر شيء (سياسات RLS تتّحد بـ OR).
DO $$
DECLARE p RECORD;
BEGIN
  FOR p IN SELECT policyname FROM pg_policies
            WHERE schemaname='public' AND tablename='ai_settings'
  LOOP
    EXECUTE format('DROP POLICY IF EXISTS %I ON public.ai_settings', p.policyname);
  END LOOP;
END;
$$;

-- ما تحتاجه صفحة المعلّمة، وهذا كلُّه.
CREATE POLICY ai_settings_client_read ON public.ai_settings
  FOR SELECT TO anon, authenticated
  USING (key IN ('quota_text','quota_img','quota_search','c1_tt_defaults','game_cfg'));

-- المشرف يقرأ ويكتب كلَّ شيء (لوحة الإدارة تقرأ منه ثلاثاً وعشرين مرّة).
CREATE POLICY ai_settings_admin_all ON public.ai_settings
  FOR ALL TO authenticated
  USING (public.is_app_admin()) WITH CHECK (public.is_app_admin());

-- دوالُّ الحافة تعمل بمفتاح الخدمة فتتجاوز RLS — فقراءتها لـ model_* و
-- ppt_system_prompt تبقى كما هي بلا تعديلِ حرف.

COMMENT ON TABLE public.ai_settings IS
  'إعداداتُ الذكاء الاصطناعي — المتصفّح يقرأ الحصص وافتراضيات الجدول فقط؛ النماذج والموجّهات وأرقام العمل لخدمة الخادم والمشرف.';
