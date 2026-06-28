-- ════════════════════════════════════════════════════════════════
-- جدول توكنات Google Drive المرتبطة بكل معلم
-- يخزّن "refresh token" الخاص بجوجل لكل مستخدم بعد ربط حسابه مرة واحدة،
-- ليستطيع Edge Function تجديد توكن الوصول تلقائياً عند الحاجة.
-- ════════════════════════════════════════════════════════════════

create table if not exists public.drive_tokens (
  user_id uuid primary key references auth.users(id) on delete cascade,
  refresh_token text not null,
  google_email text,
  updated_at timestamptz not null default now()
);

alter table public.drive_tokens enable row level security;

-- المستخدم يقرأ/يكتب صف توكنه فقط (RLS)
drop policy if exists dt_select_own on public.drive_tokens;
create policy dt_select_own on public.drive_tokens
  for select using (auth.uid() = user_id);

drop policy if exists dt_insert_own on public.drive_tokens;
create policy dt_insert_own on public.drive_tokens
  for insert with check (auth.uid() = user_id);

drop policy if exists dt_update_own on public.drive_tokens;
create policy dt_update_own on public.drive_tokens
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

drop policy if exists dt_delete_own on public.drive_tokens;
create policy dt_delete_own on public.drive_tokens
  for delete using (auth.uid() = user_id);

-- ملاحظة: Edge Function يستخدم مفتاح service_role الذي يتجاوز RLS،
-- فيستطيع قراءة refresh_token لأي مستخدم لتجديد توكنه بأمان من الخادم.
