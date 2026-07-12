-- ☁️ نسخة كل معلم من تحضيراته — تُفتح من أي جهاز
create table if not exists user_preps (
  user_id uuid not null default auth.uid(),
  lesson_id text not null,
  grade text, subject text, unit text, lesson text,
  data jsonb not null,
  updated_at timestamptz default now(),
  primary key (user_id, lesson_id)
);
alter table user_preps enable row level security;
drop policy if exists "user_preps_own" on user_preps;
create policy "user_preps_own" on user_preps for all to authenticated
  using (user_id = auth.uid()) with check (user_id = auth.uid());
