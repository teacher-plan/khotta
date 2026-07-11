-- ⭐ تقييم «الخطة الذهبية» بخمس نجوم — تقييم واحد لكل معلم لكل تحضير (قابل للتعديل)
create table if not exists shared_prep_ratings (
  lesson_id text not null,
  user_id uuid not null default auth.uid(),
  stars int not null check (stars between 1 and 5),
  created_at timestamptz default now(),
  primary key (lesson_id, user_id)
);
alter table shared_prep_ratings enable row level security;
create policy "ratings_upsert_own" on shared_prep_ratings for insert to authenticated with check (user_id = auth.uid());
create policy "ratings_update_own" on shared_prep_ratings for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
create policy "ratings_read" on shared_prep_ratings for select to authenticated using (true);
create policy "ratings_admin_delete" on shared_prep_ratings for delete to authenticated using (is_app_admin());
