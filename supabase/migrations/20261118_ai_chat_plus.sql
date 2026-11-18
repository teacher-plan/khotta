-- تطوير «خُطّة AI» (١٨ نوفمبر): تثبيت المحادثات، والبحث فيها، وتقييم الردود (👍/👎) لتراها الإدارة. متعادلة.
alter table public.ai_chats add column if not exists pinned boolean not null default false;

-- البحث في عناوين المحادثات ونصوصها — لصاحبها فقط
create or replace function public.search_ai_chats(p_q text)
returns table(id uuid, title text, updated_at timestamptz, pinned boolean)
language sql stable security invoker set search_path = public as $$
  select c.id, c.title, c.updated_at, c.pinned
  from ai_chats c
  where c.user_id = auth.uid()
    and length(trim(coalesce(p_q,''))) >= 2
    and (c.title ilike '%' || trim(p_q) || '%' or c.messages::text ilike '%' || trim(p_q) || '%')
  order by c.pinned desc, c.updated_at desc
  limit 30;
$$;
revoke all on function public.search_ai_chats(text) from public, anon;
grant execute on function public.search_ai_chats(text) to authenticated;

create table if not exists public.ai_chat_feedback (
  id bigserial primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  chat_id uuid,
  rating smallint not null check (rating in (-1, 1)),
  question text,
  reply text,
  model text,
  created_at timestamptz not null default now()
);
create index if not exists ai_chat_feedback_created on public.ai_chat_feedback (created_at desc);
alter table public.ai_chat_feedback enable row level security;
drop policy if exists ai_fb_insert_own on public.ai_chat_feedback;
create policy ai_fb_insert_own on public.ai_chat_feedback for insert to authenticated with check (user_id = auth.uid());
drop policy if exists ai_fb_admin_read on public.ai_chat_feedback;
create policy ai_fb_admin_read on public.ai_chat_feedback for select to authenticated using (is_app_admin());
revoke all on public.ai_chat_feedback from anon;
grant insert, select on public.ai_chat_feedback to authenticated;
grant usage, select on sequence public.ai_chat_feedback_id_seq to authenticated;
