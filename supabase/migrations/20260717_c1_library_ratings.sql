-- ⭐ تقييم ملفات مكتبة الحلقة الأولى من نجمة إلى خمس (تقييم واحد لكل معلمة لكل ملف)
create table if not exists c1_library_ratings (
  item_id uuid not null references c1_library_items(id) on delete cascade,
  user_id uuid not null default auth.uid(),
  rating int not null check (rating between 1 and 5),
  created_at timestamptz default now(),
  primary key (item_id, user_id)
);
alter table c1_library_ratings enable row level security;

drop policy if exists "c1libr_read_all" on c1_library_ratings;
create policy "c1libr_read_all" on c1_library_ratings
  for select to authenticated using (true);

drop policy if exists "c1libr_insert_own" on c1_library_ratings;
create policy "c1libr_insert_own" on c1_library_ratings
  for insert to authenticated with check (user_id = auth.uid());

drop policy if exists "c1libr_update_own" on c1_library_ratings;
create policy "c1libr_update_own" on c1_library_ratings
  for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists "c1libr_delete_own" on c1_library_ratings;
create policy "c1libr_delete_own" on c1_library_ratings
  for delete to authenticated using (user_id = auth.uid());
