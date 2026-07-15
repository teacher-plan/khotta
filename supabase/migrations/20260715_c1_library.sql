-- 📚 مكتبة الحلقة الأولى التشاركية: تُوحَّد حسب المادة لا الصف —
-- محتوى معلمة رياضيات الصف الأول يظهر لمعلمة رياضيات الصف الرابع وهكذا.
-- كل معلمات المادة الواحدة (بغض النظر عن الصف) يشتركن في نفس المساحة.

create table if not exists c1_library_items (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid(),
  subject text not null,
  title text not null,
  description text,
  file_url text,
  file_name text,
  uploader_name text,
  created_at timestamptz default now()
);
alter table c1_library_items enable row level security;

drop policy if exists "c1lib_read_all" on c1_library_items;
create policy "c1lib_read_all" on c1_library_items
  for select to authenticated using (true);

drop policy if exists "c1lib_insert_own" on c1_library_items;
create policy "c1lib_insert_own" on c1_library_items
  for insert to authenticated with check (user_id = auth.uid());

drop policy if exists "c1lib_delete_own" on c1_library_items;
create policy "c1lib_delete_own" on c1_library_items
  for delete to authenticated using (user_id = auth.uid());

-- الملفات المرفقة تُحفظ داخل مخزن library-files الموجود، تحت مسار مخصص
-- c1-library/ — بلا أي أثر على سياسات المخزن الأخرى (أصوات الألعاب، الكتب، شخصية فهيم).
drop policy if exists "c1lib_storage_insert" on storage.objects;
create policy "c1lib_storage_insert" on storage.objects
  for insert to authenticated
  with check (bucket_id = 'library-files' and name like 'c1-library/%');

drop policy if exists "c1lib_storage_delete_own" on storage.objects;
create policy "c1lib_storage_delete_own" on storage.objects
  for delete to authenticated
  using (bucket_id = 'library-files' and name like 'c1-library/%' and owner = auth.uid());
