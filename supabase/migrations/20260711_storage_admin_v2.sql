-- 🔐 v2: سياسات مشرف التخزين بفحص البريد المباشر من التوكن
-- (بديل عن is_app_admin() التي قد لا تُقيَّم كما نتوقع في سياق storage)

drop policy if exists "libfiles admin insert" on storage.objects;
create policy "libfiles admin insert" on storage.objects
  for insert to authenticated
  with check (
    bucket_id = 'library-files'
    and lower(coalesce(auth.jwt() ->> 'email', '')) = 'teacherplane2026project@gmail.com'
  );

drop policy if exists "libfiles admin update" on storage.objects;
create policy "libfiles admin update" on storage.objects
  for update to authenticated
  using (
    bucket_id = 'library-files'
    and lower(coalesce(auth.jwt() ->> 'email', '')) = 'teacherplane2026project@gmail.com'
  )
  with check (
    bucket_id = 'library-files'
    and lower(coalesce(auth.jwt() ->> 'email', '')) = 'teacherplane2026project@gmail.com'
  );

drop policy if exists "libfiles admin delete" on storage.objects;
create policy "libfiles admin delete" on storage.objects
  for delete to authenticated
  using (
    bucket_id = 'library-files'
    and lower(coalesce(auth.jwt() ->> 'email', '')) = 'teacherplane2026project@gmail.com'
  );
