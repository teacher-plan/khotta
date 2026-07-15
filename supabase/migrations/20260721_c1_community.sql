-- 💬 مجتمع معلمات الحلقة الأولى — رسائل مشتركة بين كل المعلمات (بلا منشورات/تعليقات، فقط تبادل رسائل)
create table if not exists c1_community_messages (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid(),
  user_label text,
  message text not null,
  created_at timestamptz default now()
);
alter table c1_community_messages enable row level security;

drop policy if exists "c1com_read_all" on c1_community_messages;
create policy "c1com_read_all" on c1_community_messages
  for select to authenticated using (true);

drop policy if exists "c1com_insert_own" on c1_community_messages;
create policy "c1com_insert_own" on c1_community_messages
  for insert to authenticated with check (user_id = auth.uid());

drop policy if exists "c1com_delete_own_or_admin" on c1_community_messages;
create policy "c1com_delete_own_or_admin" on c1_community_messages
  for delete to authenticated using (user_id = auth.uid() or is_app_admin());
