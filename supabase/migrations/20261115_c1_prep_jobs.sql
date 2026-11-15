-- إعداد التحضير في الخلفية (c1-prep-job): مهمةٌ لكل طلب، يقرؤها المتصفح ويدمج خطتها
-- في plan_state ثم يعلّمها «مستهلكة». الكتابة من الخادم وحده (مفتاح الخدمة). متعادلة.
create table if not exists public.c1_prep_jobs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  lesson_id text not null,
  lesson_name text,
  meta jsonb not null default '{}'::jsonb,
  status text not null default 'running' check (status in ('running','done','error')),
  plan jsonb,
  summary text,
  error text,
  consumed boolean not null default false,
  created_at timestamptz not null default now(),
  finished_at timestamptz
);
create index if not exists c1_prep_jobs_user_idx on public.c1_prep_jobs (user_id, consumed);
alter table public.c1_prep_jobs enable row level security;
drop policy if exists c1_prep_jobs_read_own on public.c1_prep_jobs;
create policy c1_prep_jobs_read_own on public.c1_prep_jobs for select to authenticated using (user_id = auth.uid());
drop policy if exists c1_prep_jobs_consume_own on public.c1_prep_jobs;
create policy c1_prep_jobs_consume_own on public.c1_prep_jobs for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
revoke all on public.c1_prep_jobs from anon;
grant select, update (consumed) on public.c1_prep_jobs to authenticated;

-- إشعار «التحضير جاهز» يُرسَل إلى الهاتف فوراً كرسائل الإدارة
create or replace function public.c1_notif_push_trg()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if new.user_id is not null and (new.kind in ('survey','prep') or (coalesce(new.kind,'info') = 'info' and new.item_id is null)) then
    perform public.c1_push_call('notif', jsonb_build_object('id', new.id));
  end if;
  return new;
end;
$$;
revoke all on function public.c1_notif_push_trg() from public, anon, authenticated;
