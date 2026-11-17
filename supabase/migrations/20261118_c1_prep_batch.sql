-- تحضير وحدةٍ كاملة بضغطة (c1-prep-job action=unit): طابورٌ على الخادم يُعِدّ الدروس
-- واحداً بعد الآخر (حدّ السرعة ثانيتان لكل معلّم يمنع التوازي)، مع إعادة تلقائية. متعادلة.
do $$
declare c text;
begin
  for c in select conname from pg_constraint
           where conrelid = 'public.c1_prep_jobs'::regclass and contype = 'c'
             and pg_get_constraintdef(oid) ilike '%status%'
  loop
    execute format('alter table public.c1_prep_jobs drop constraint %I', c);
  end loop;
end $$;
alter table public.c1_prep_jobs
  add constraint c1_prep_jobs_status_check check (status in ('queued','running','done','error'));
alter table public.c1_prep_jobs add column if not exists batch_id uuid;
alter table public.c1_prep_jobs add column if not exists attempts int not null default 0;
alter table public.c1_prep_jobs add column if not exists payload jsonb;
alter table public.c1_prep_jobs add column if not exists started_at timestamptz;
create index if not exists c1_prep_jobs_batch_idx on public.c1_prep_jobs (batch_id, status) where batch_id is not null;
