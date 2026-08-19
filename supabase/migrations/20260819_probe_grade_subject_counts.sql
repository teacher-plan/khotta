-- probe: عدد الدروس لكل مادة داخل كل صفٍّ على حدة (١-٤) — يتراجع عن نفسه
do $$
declare v text;
begin
  select string_agg(grade || ' | ' || subject || ' | lessons=' || cnt || ' | pages=' || pages, e'\n' order by grade, cnt desc)
  into v
  from (
    select grade, subject, count(*) cnt, count(distinct page) pages
    from public.curriculum
    where grade in ('1','2','3','4')
    group by grade, subject
  ) t;
  raise exception 'PROBE | %', v;
end $$;
