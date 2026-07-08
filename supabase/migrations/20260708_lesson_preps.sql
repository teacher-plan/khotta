-- مساعد التحضير اليومي: تخزين خطط الحصص المولّدة لكل معلم
create table if not exists lesson_preps (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  lesson_id text not null,
  grade int,
  subject text,
  unit text,
  lesson text,
  plan jsonb not null,
  edited boolean default false,
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  unique (user_id, lesson_id)
);

alter table lesson_preps enable row level security;

drop policy if exists "own_preps" on lesson_preps;
create policy "own_preps" on lesson_preps
  for all using (auth.uid() = user_id) with check (auth.uid() = user_id);
