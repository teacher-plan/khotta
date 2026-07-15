-- 🔔 إشعارات داخل تطبيق الحلقة الأولى (بلا Push حقيقي) — تُستخدم أولاً لتنبيه
-- صاحبة الملف عند تقييم إحدى زميلاتها له في المكتبة المشتركة.
create table if not exists c1_notifications (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null,            -- صاحبة الإشعار (المستلمة)
  message text not null,
  item_id uuid references c1_library_items(id) on delete cascade,
  read boolean not null default false,
  created_at timestamptz default now()
);
alter table c1_notifications enable row level security;

drop policy if exists "c1notif_read_own" on c1_notifications;
create policy "c1notif_read_own" on c1_notifications
  for select to authenticated using (user_id = auth.uid());

drop policy if exists "c1notif_insert_any" on c1_notifications;
create policy "c1notif_insert_any" on c1_notifications
  for insert to authenticated with check (true);

drop policy if exists "c1notif_update_own" on c1_notifications;
create policy "c1notif_update_own" on c1_notifications
  for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
