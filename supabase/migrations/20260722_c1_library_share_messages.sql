-- 📚 رسالة جماعية تلقائية لمعلمات المادة عند رفع ملف جديد في المكتبة
alter table c1_messages add column if not exists target_subject text;
alter table c1_messages add column if not exists item_id uuid references c1_library_items(id) on delete cascade;

alter table c1_messages drop constraint if exists c1_messages_kind_check;
alter table c1_messages add constraint c1_messages_kind_check check (kind in ('broadcast','private','library_share'));

-- أي معلمة (لا المشرف فقط) يمكنها الآن إدراج رسالة من نوع library_share حصراً
-- (رسالة جماعية بلا هدف فردي، مرتبطة بمادة محددة) — بقية الأنواع تبقى حكراً على المشرف
drop policy if exists "c1msg_insert_admin" on c1_messages;
drop policy if exists "c1msg_insert" on c1_messages;
create policy "c1msg_insert" on c1_messages
  for insert to authenticated with check (
    is_app_admin()
    or (kind = 'library_share' and target_user_id is null and target_subject is not null)
  );
