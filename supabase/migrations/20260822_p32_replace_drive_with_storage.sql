-- ════════════════════════════════════════════════════════════════════
-- P32 — استبدال Google Drive بتخزين Supabase الخاص، حصّةٌ صامتة لكل معلّمة
--
-- السبب: تأخّر ملحوظ في رفع/جلب ملفات Drive (تجديد توكن ← بحث/إنشاء مجلد
-- ← رفع فعلي، ثلاث رحلات شبكية على الأقل)، وملفاتٌ محمية تفشل بصمت أحياناً،
-- وتشتيت المعلّمة بطلب صلاحية Google إضافية. لا ملفات مرفوعة على Drive
-- حالياً (تحقّقٌ مباشر) — لا حاجة لأي هجرة بيانات.
--
-- الحصّة تُفرَض من الخادم عبر can_upload_file() فقط — لا اعتماد على فحصٍ
-- بالواجهة وحده، ولا كشفٌ لرقم الحصّة أو المستهلَك للمعلّمة (صريح الطلب:
-- "لا تبين للمستخدم أن هناك مساحة مقدّرة مخصّصة له"). user_storage_limits
-- بلا أي سياسة قراءةٍ لغير المشرف عمداً — لا مسار كودي واحد يستطيع كشفها
-- لصاحبة الحساب حتى لو أراد مطوّرٌ لاحقاً ذلك بالخطأ.
-- ════════════════════════════════════════════════════════════════════

-- ① الباكِت — عامّ للقراءة (كنمط library-files القائم أصلاً: رابطٌ غير
--    قابلٍ للتخمين بدل توقيع URL مؤقّت، أبسط وأثبت مع نفس مستوى الحماية
--    العملي)، والكتابة/الحذف مقصوران على صاحبة الملف عبر مسارها الخاص.
insert into storage.buckets (id, name, public)
values ('user-files', 'user-files', true)
on conflict (id) do nothing;

drop policy if exists "userfiles_own_insert" on storage.objects;
create policy "userfiles_own_insert" on storage.objects
  for insert to authenticated
  with check (
    bucket_id = 'user-files'
    and (storage.foldername(name))[1] = auth.uid()::text
    and lower(name) !~ '\.(html?|xhtml|svg|js|mjs|wasm|php|sh)$'
  );

drop policy if exists "userfiles_own_delete" on storage.objects;
create policy "userfiles_own_delete" on storage.objects
  for delete to authenticated
  using (
    bucket_id = 'user-files'
    and (storage.foldername(name))[1] = auth.uid()::text
  );

-- ② سجلّ الملفات — مصدر الحقيقة الوحيد لحساب المستهلَك (مجموع size_bytes)،
--    بدل استعراض الباكِت حيّاً في كل فحص حصّة أو كل تحميل لصفحة المراقبة.
create table if not exists public.user_files (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  bucket text not null default 'user-files',
  path text not null,
  size_bytes bigint not null check (size_bytes >= 0),
  kind text not null check (kind in ('lesson_attachment','achievement_attachment','profile_photo')),
  file_name text,
  created_at timestamptz not null default now()
);
create index if not exists user_files_user_idx on public.user_files(user_id);

alter table public.user_files enable row level security;
drop policy if exists "userfiles_row_own_select" on public.user_files;
create policy "userfiles_row_own_select" on public.user_files
  for select to authenticated using (user_id = auth.uid());
drop policy if exists "userfiles_row_own_insert" on public.user_files;
create policy "userfiles_row_own_insert" on public.user_files
  for insert to authenticated with check (user_id = auth.uid());
drop policy if exists "userfiles_row_own_delete" on public.user_files;
create policy "userfiles_row_own_delete" on public.user_files
  for delete to authenticated using (user_id = auth.uid());
-- المشرف يقرأ الكل (قسم "مراقبة التخزين" في لوحة الإدارة) — لا كتابة له
-- هنا؛ حجم الملفات لا يُعدَّل يدوياً، هو نتيجة رفعٍ/حذفٍ فعلي فقط.
drop policy if exists "userfiles_row_admin_select" on public.user_files;
create policy "userfiles_row_admin_select" on public.user_files
  for select to authenticated using (is_app_admin());

-- ③ الحصّة الفردية — افتراضياً ١ جيجابايت، قابلةٌ للتوسيع لكل معلّمة على
--    حدة من لوحة الإدارة. بلا صفٍّ = الافتراضي (لا حاجة لإدراج صفٍّ لكل
--    معلّمة عند التسجيل).
create table if not exists public.user_storage_limits (
  user_id uuid primary key references auth.users(id) on delete cascade,
  limit_bytes bigint not null default 1073741824,
  updated_at timestamptz not null default now(),
  updated_by text
);

alter table public.user_storage_limits enable row level security;
-- عمداً: لا سياسة قراءةٍ لغير المشرف — صاحبة الحساب لا تستطيع الاطّلاع على
-- حصّتها من هذا الجدول مباشرةً بأي مسار (RLS تمنع حتى قبل وصول أي كودٍ).
drop policy if exists "storagelimits_admin_all" on public.user_storage_limits;
create policy "storagelimits_admin_all" on public.user_storage_limits
  for all to authenticated using (is_app_admin()) with check (is_app_admin());

-- ④ فحص الحصّة — دالّةٌ تُعيد true/false فقط، لا رقماً. صاحبة الحساب
--    تستطيع استدعاءها (لازمةٌ لمنع الرفع الزائد فعلياً) لكن لا تستطيع
--    استنتاج رقم حصّتها منها إلا بتجربة قيمٍ متعددة يدوياً — عبءٌ يفوق أي
--    فائدة عملية، ومطابقٌ لروح "بلا إشعارٍ بالمساحة المتاحة".
create or replace function public.can_upload_file(add_bytes bigint)
returns boolean
language sql
security definer
set search_path = public
as $$
  select coalesce(
    (select sum(size_bytes) from public.user_files where user_id = auth.uid()), 0
  ) + greatest(add_bytes, 0)
  <=
  coalesce(
    (select limit_bytes from public.user_storage_limits where user_id = auth.uid()),
    1073741824
  );
$$;
grant execute on function public.can_upload_file(bigint) to authenticated;
