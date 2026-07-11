-- 🔐 استكمال إغلاق التخزين: المشرف يملك صلاحيات كاملة على library-files
-- (السياسات القديمة "admin upload..." كانت محدودة بمسارات معينة، والمسارات
--  الجديدة game-sfx/ و assistant/ و game-themes/ كانت تمر عبر السياسة
--  المفتوحة المحذوفة — هذه تعوّضها للمشرف حصراً)

drop policy if exists "libfiles admin insert" on storage.objects;
create policy "libfiles admin insert" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'library-files' and is_app_admin());

drop policy if exists "libfiles admin delete" on storage.objects;
create policy "libfiles admin delete" on storage.objects
  for delete to authenticated
  using (bucket_id = 'library-files' and is_app_admin());
