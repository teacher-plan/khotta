-- حذف ثلاثة حسابات معلمين تجريبية/غير مستخدَمة من الحلقة الأولى:
--   c1@khotati.app        (لا يوجد لها ملف cycle1_profiles)
--   iphon90z8@yahoo.com   ("Honda" — ملف بلا محتوى تحاضير مُولَّد)
--   tv8888tvvv@gmail.com  ("تجريبي" — محتوى تحاضيرها الـ24 موجود مسبقاً
--                          ومنشور في c1_shared_assets فلن يُفقد بحذف الحساب)
-- حساب نورة السعدية (x@y.com) مستثنى صراحةً ولا يُلمس.

DO $$
DECLARE
  target_emails text[] := ARRAY['c1@khotati.app','iphon90z8@yahoo.com','tv8888tvvv@gmail.com'];
  uid uuid;
BEGIN
  FOR uid IN
    SELECT id FROM auth.users WHERE email = ANY(target_emails)
  LOOP
    DELETE FROM public.cycle1_profiles WHERE id = uid;
    DELETE FROM public.allowed_emails WHERE email IN (
      SELECT email FROM auth.users WHERE id = uid
    );
    DELETE FROM auth.users WHERE id = uid;
  END LOOP;

  -- تأمين إضافي: حذف أي صفوف allowed_emails متبقية بهذه العناوين
  -- (لو لم يوجد لها حساب auth.users من الأساس).
  DELETE FROM public.allowed_emails WHERE email = ANY(target_emails);
END $$;
