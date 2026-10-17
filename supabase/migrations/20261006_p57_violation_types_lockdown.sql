-- 🔒 violation_types كانت بسياسة ALL للدور public (حتى غير المسجّل) بـ true:
-- أيّ زائرٍ يملك المفتاح العام يستطيع حذف أنواع المخالفات أو تعديلها لكل المدارس.
-- القراءة تبقى لكل حسابٍ مسجّل، والكتابة للمشرف وحده (كما في بقية جداول الإدارة).
drop policy if exists "violation_types_all" on public.violation_types;
drop policy if exists "violation_types_read" on public.violation_types;
drop policy if exists "violation_types_admin_write" on public.violation_types;
create policy "violation_types_read" on public.violation_types for select to authenticated using (true);
create policy "violation_types_admin_write" on public.violation_types for all to authenticated
  using (lower(coalesce(auth.jwt() ->> 'email', '')) = 'teacherplane2026project@gmail.com')
  with check (lower(coalesce(auth.jwt() ->> 'email', '')) = 'teacherplane2026project@gmail.com');
