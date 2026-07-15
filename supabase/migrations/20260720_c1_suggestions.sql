-- 💌 صندوق اقتراحات المعلمات لإدارة منصة «خطتي» (تطوير المنصة نفسها)
create table if not exists c1_suggestions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid(),
  user_label text,
  message text not null,
  created_at timestamptz default now()
);
alter table c1_suggestions enable row level security;

drop policy if exists "c1sug_insert_own" on c1_suggestions;
create policy "c1sug_insert_own" on c1_suggestions
  for insert to authenticated with check (user_id = auth.uid());

drop policy if exists "c1sug_read_admin" on c1_suggestions;
create policy "c1sug_read_admin" on c1_suggestions
  for select to authenticated using (is_app_admin());

drop policy if exists "c1sug_delete_admin" on c1_suggestions;
create policy "c1sug_delete_admin" on c1_suggestions
  for delete to authenticated using (is_app_admin());
