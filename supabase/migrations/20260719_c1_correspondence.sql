-- 📨 مراسلات الحلقة الأولى: رسائل جماعية + رسائل خاصة + استبيانات
-- يديرها المشرف من صفحة إدارة الحلقة الأولى (manager.html)، وتصل لمعلمات
-- الحلقة الأولى في قسم «المراسلات» الجديد داخل cycle1.html.

create table if not exists c1_messages (
  id uuid primary key default gen_random_uuid(),
  kind text not null check (kind in ('broadcast','private')),
  title text not null,
  body text not null,
  target_user_id uuid,          -- null = رسالة جماعية لكل معلمات الحلقة الأولى
  target_label text,            -- اسم/بريد المعلمة المستهدفة (لعرضها في قائمة المشرف دون جوين)
  created_by text,
  created_at timestamptz default now()
);
alter table c1_messages enable row level security;

drop policy if exists "c1msg_read" on c1_messages;
create policy "c1msg_read" on c1_messages
  for select to authenticated using (target_user_id is null or target_user_id = auth.uid() or is_app_admin());

drop policy if exists "c1msg_insert_admin" on c1_messages;
create policy "c1msg_insert_admin" on c1_messages
  for insert to authenticated with check (is_app_admin());

drop policy if exists "c1msg_delete_admin" on c1_messages;
create policy "c1msg_delete_admin" on c1_messages
  for delete to authenticated using (is_app_admin());

-- استبيانات (سؤال واحد + خيارات متعددة لكل استبيان)
create table if not exists c1_surveys (
  id uuid primary key default gen_random_uuid(),
  question text not null,
  options jsonb not null,       -- ["خيار ١","خيار ٢",...]
  closed boolean not null default false,
  created_by text,
  created_at timestamptz default now()
);
alter table c1_surveys enable row level security;

drop policy if exists "c1srv_read_all" on c1_surveys;
create policy "c1srv_read_all" on c1_surveys
  for select to authenticated using (true);

drop policy if exists "c1srv_insert_admin" on c1_surveys;
create policy "c1srv_insert_admin" on c1_surveys
  for insert to authenticated with check (is_app_admin());

drop policy if exists "c1srv_update_admin" on c1_surveys;
create policy "c1srv_update_admin" on c1_surveys
  for update to authenticated using (is_app_admin()) with check (is_app_admin());

drop policy if exists "c1srv_delete_admin" on c1_surveys;
create policy "c1srv_delete_admin" on c1_surveys
  for delete to authenticated using (is_app_admin());

create table if not exists c1_survey_responses (
  survey_id uuid not null references c1_surveys(id) on delete cascade,
  user_id uuid not null default auth.uid(),
  option_index int not null,
  created_at timestamptz default now(),
  primary key (survey_id, user_id)
);
alter table c1_survey_responses enable row level security;

drop policy if exists "c1srvr_read_all" on c1_survey_responses;
create policy "c1srvr_read_all" on c1_survey_responses
  for select to authenticated using (true);

drop policy if exists "c1srvr_insert_own" on c1_survey_responses;
create policy "c1srvr_insert_own" on c1_survey_responses
  for insert to authenticated with check (user_id = auth.uid());

drop policy if exists "c1srvr_update_own" on c1_survey_responses;
create policy "c1srvr_update_own" on c1_survey_responses
  for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
