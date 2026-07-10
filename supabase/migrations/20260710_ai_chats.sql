-- 💬 محادثات المساعد الذكي — محفوظة لكل معلم
create table if not exists ai_chats (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid(),
  title text,
  messages jsonb not null default '[]'::jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
alter table ai_chats enable row level security;
create policy "chats_own" on ai_chats for all to authenticated
  using (user_id = auth.uid()) with check (user_id = auth.uid());
