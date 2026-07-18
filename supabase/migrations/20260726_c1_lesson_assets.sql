-- ⚡ تخفيف الضغط على الخادم: أصول الدروس الثقيلة خارج ملف المعلمة
-- بيانات العروض التقديمية وملخصات الكتاب كانت تُخزَّن داخل
-- cycle1_profiles.data — وكل حفظ (حتى منح نجمة) يرفع الملف كاملاً.
-- هذا الجدول يعزل الأصول الثقيلة في صفوف مستقلة لكل درس، فيبقى ملف
-- المعلمة صغيراً وسريع الحفظ مهما ولّدت من عروض.

create table if not exists c1_lesson_assets (
  user_id uuid not null references auth.users(id) on delete cascade,
  lesson_id text not null,
  slides jsonb,
  book_summary text,
  updated_at timestamptz default now(),
  primary key (user_id, lesson_id)
);

alter table c1_lesson_assets enable row level security;

drop policy if exists "c1assets_own_select" on c1_lesson_assets;
create policy "c1assets_own_select" on c1_lesson_assets
  for select to authenticated using (user_id = auth.uid());

drop policy if exists "c1assets_own_insert" on c1_lesson_assets;
create policy "c1assets_own_insert" on c1_lesson_assets
  for insert to authenticated with check (user_id = auth.uid());

drop policy if exists "c1assets_own_update" on c1_lesson_assets;
create policy "c1assets_own_update" on c1_lesson_assets
  for update to authenticated
  using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists "c1assets_own_delete" on c1_lesson_assets;
create policy "c1assets_own_delete" on c1_lesson_assets
  for delete to authenticated using (user_id = auth.uid());
