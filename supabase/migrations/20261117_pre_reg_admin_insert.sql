-- ════════════════════════════════════════════════════════════════════
-- إصلاح زرّ «إضافة معلّم» في صفحة «المعلّمون» (manager.html admTAddSave):
-- يُدرج المشرف طلب التسجيل في pre_registrations وهو مسجَّل الدخول (دور
-- authenticated)، والجدول ليس فيه سياسة إدراج إلا للزائر (anon، نموذج
-- التسجيل العام) — فيُرفض الإدراج بخطأ RLS ويظهر «تعذّرت الإضافة».
-- السياسة الجديدة للمشرف وحده (is_app_admin)، ولا تمسّ سياسة الزائر.
-- ════════════════════════════════════════════════════════════════════
drop policy if exists "pre_reg_admin_insert" on pre_registrations;
create policy "pre_reg_admin_insert" on pre_registrations
  for insert to authenticated
  with check (is_app_admin());
