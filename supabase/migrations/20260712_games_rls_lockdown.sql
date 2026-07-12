-- 🔐 إحكام عزل الألعاب: كل معلم يرى ألعابه فقط
alter table games enable row level security;
drop policy if exists "games_own" on games;
create policy "games_own" on games for all to authenticated
  using (user_id = auth.uid()) with check (user_id = auth.uid());
-- تصحيح أي صفوف قديمة بلا مالك (لا يفترض وجودها، احتياط)
delete from games where user_id is null;
