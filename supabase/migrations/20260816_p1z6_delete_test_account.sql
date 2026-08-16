-- حذف حساب الاختبار الذي أُنشئ أثناء التحقّق الحيّ من RLS وتقييد معدّل
-- الذكاء الاصطناعي — لا صلاحية خاصة له ولا تأثير على بيانات حقيقية،
-- لكن حذفه أنظف من تركه.
DELETE FROM auth.users WHERE email = 'khotta.audit.test+dbcheck@gmail.com';
