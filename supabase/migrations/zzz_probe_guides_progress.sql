-- فحصٌ للقراءة فقط، يتراجع عن نفسه: يرفع استثناءً يحمل النتيجة لأن سير
-- العمل لا يطبع مخرجات الاستعلام الناجح — يُحذف الملف بعد الاطّلاع.
do $$
declare n int; lst text;
begin
  select count(*) into n from public.teacher_guides;
  select string_agg(grade || '/' || subject || ' (' || coalesce(page_count,0) || 'ص)', ' | ' order by grade, subject)
    into lst from public.teacher_guides;
  raise exception 'GUIDES_COUNT=% :: %', n, coalesce(lst,'(لا صفوف)');
end $$;
