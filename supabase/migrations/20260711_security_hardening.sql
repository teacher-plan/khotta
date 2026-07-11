-- 🔐 تحصين أمني: (١) حذف كلمات المرور النصية نهائياً (٢) حصص استخدام الذكاء على الخادم
alter table pre_registrations drop column if exists account_password;

create table if not exists ai_usage (
  user_id uuid not null,
  month text not null,          -- 'YYYY-MM'
  kind text not null,           -- 'text' | 'img'
  count int not null default 0,
  primary key (user_id, month, kind)
);
alter table ai_usage enable row level security;
-- المعلم يقرأ استهلاكه فقط؛ الكتابة عبر دوال الخادم (service role) حصراً
create policy "usage_read_own" on ai_usage for select to authenticated using (user_id = auth.uid());
