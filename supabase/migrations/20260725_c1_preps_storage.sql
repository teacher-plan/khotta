-- 🖼️ ملخصات الدروس (إنفوجرافيك بطاقة الدرس / بطاقة اليوم) — الحلقة الأولى
-- المعلمات يرفعن ملخص الدرس المولّد إلى مسار c1-preps/<user_id>/... داخل
-- مخزن library-files، وكانت سياسات التخزين تسمح فقط بمسار c1-library/
-- فيفشل الحفظ بصمت. هذه السياسات تفتح المسار الجديد لكل معلمة على
-- مجلدها الخاص فقط (القراءة عامة أصلاً لأن المخزن public).

drop policy if exists "c1preps_storage_insert" on storage.objects;
create policy "c1preps_storage_insert" on storage.objects
  for insert to authenticated
  with check (
    bucket_id = 'library-files'
    and name like 'c1-preps/' || auth.uid() || '/%'
  );

-- التوليد المتكرر لنفس الدرس يستبدل الصورة (upsert = update عند الوجود)
drop policy if exists "c1preps_storage_update" on storage.objects;
create policy "c1preps_storage_update" on storage.objects
  for update to authenticated
  using (
    bucket_id = 'library-files'
    and name like 'c1-preps/' || auth.uid() || '/%'
  )
  with check (
    bucket_id = 'library-files'
    and name like 'c1-preps/' || auth.uid() || '/%'
  );

drop policy if exists "c1preps_storage_delete" on storage.objects;
create policy "c1preps_storage_delete" on storage.objects
  for delete to authenticated
  using (
    bucket_id = 'library-files'
    and name like 'c1-preps/' || auth.uid() || '/%'
  );
