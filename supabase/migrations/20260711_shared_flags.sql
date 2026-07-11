-- 🚩 بلاغات جودة «الخطة الذهبية»: بلاغ واحد لكل معلم لكل درس
-- عند ٣ بلاغات تُستبعد الحزمة من الاستيراد التلقائي حتى يراجعها المشرف
create table if not exists shared_prep_flags (
  lesson_id text not null,
  user_id uuid not null default auth.uid(),
  created_at timestamptz default now(),
  primary key (lesson_id, user_id)
);
alter table shared_prep_flags enable row level security;
create policy "flags_insert_own" on shared_prep_flags for insert to authenticated with check (user_id = auth.uid());
create policy "flags_read" on shared_prep_flags for select to authenticated using (true);
create policy "flags_admin_delete" on shared_prep_flags for delete to authenticated using (is_app_admin());
