-- 🔐 إغلاق الباب المفتوح في تخزين library-files
-- السياسة "library-files all access" كانت تسمح لأي شخص (حتى بلا دخول)
-- بالرفع والتعديل والحذف في المخزن كله — تُحذف نهائياً.
drop policy if exists "library-files all access" on storage.objects;

-- تعويض الجزء المشروع الوحيد منها: المشرف يستطيع التحديث/الاستبدال
-- (أصوات الألعاب، شخصية فهيم، الثيمات — كلها upsert من لوحة الإدارة)
drop policy if exists "libfiles admin update" on storage.objects;
create policy "libfiles admin update" on storage.objects
  for update to authenticated
  using (bucket_id = 'library-files' and is_app_admin())
  with check (bucket_id = 'library-files' and is_app_admin());
