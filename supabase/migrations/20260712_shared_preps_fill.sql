-- 🧩 السماح لأي معلم بملء الأجزاء الناقصة في النسخة المشتركة
drop policy if exists "shared_preps_update" on shared_preps;
create policy "shared_preps_update" on shared_preps for update to authenticated
  using (true) with check (true);
