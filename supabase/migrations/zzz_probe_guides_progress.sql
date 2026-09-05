-- فحصٌ للقراءة فقط، يتراجع عن نفسه (يُحذف بعد الاطّلاع).
do $$
declare n int; lst text;
begin
  select count(*) into n from public.teacher_guides;
  select string_agg(grade || '/' || subject || '(' || coalesce(page_count,0) || ')', ' | ' order by grade, subject)
    into lst from public.teacher_guides;
  raise exception 'GUIDES=% :: %', n, coalesce(lst,'(لا صفوف)');
end $$;
