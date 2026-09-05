-- فحصٌ نهائي للقراءة فقط، يتراجع عن نفسه (يُحذف بعد الاطّلاع).
do $$
declare n int; miss text; tot bigint;
begin
  select count(*), sum(page_count) into n, tot from public.teacher_guides;
  -- أي تركيبة (صف × مادة) ناقصة من المتوقَّع؟
  select string_agg(g || '/' || s, ' | ')
    into miss
  from (select g, s from unnest(array[1,2,3,4]) g
        cross join unnest(array['الهوية والمواطنة','ديني حياتي','أحب لغتي','اللغة الإنجليزية','الرياضيات','العلوم','عالمي الرقمي']) s) x
  where not exists (select 1 from public.teacher_guides t
                    where t.grade=x.g and t.subject=x.s and t.semester='الفصل الأول');
  raise exception 'TOTAL=% PAGES=% MISSING=%', n, tot, coalesce(miss,'(لا شيء ناقص)');
end $$;
