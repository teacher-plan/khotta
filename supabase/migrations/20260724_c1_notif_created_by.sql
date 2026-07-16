-- 🔕 استبعاد إشعار «ملف جديد» عن المعلمة التي رفعته هي نفسها
alter table c1_notifications add column if not exists created_by text;
