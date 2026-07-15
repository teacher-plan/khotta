-- 🔔 تمييز أنواع الإشعارات: استبيان/ملف جديد (قابلة للفتح) مقابل رسائل خاصة/جماعية (للقراءة فقط)
-- ودعم إشعار جماعي مرتبط بمادة (رفع ملف جديد) يُرسله معلم عادي لا المشرف فقط
alter table c1_notifications alter column user_id drop not null;
alter table c1_notifications add column if not exists kind text not null default 'info';
alter table c1_notifications add column if not exists subject text;

drop policy if exists "c1notif_read_own" on c1_notifications;
create policy "c1notif_read_own" on c1_notifications
  for select to authenticated using (user_id = auth.uid() or user_id is null);
