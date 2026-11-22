do $$ declare r text; begin
  select 'lessons='||(select count(*) from curriculum where semester='الفصل الأول' and grade=5 and subject='اللغة العربية')
   ||' book_offset='||coalesce((select offset_pages::text||' pages='||page_count from book_sources where semester='الفصل الأول' and grade='5' and subject='اللغة العربية' limit 1),'none')
   ||' guide_toc='||coalesce((select jsonb_array_length(toc)::text||' status='||status||' offset='||offset_pages from teacher_guides where semester='الفصل الأول' and grade=5 and subject='اللغة العربية' limit 1),'none') into r;
  raise exception 'PROBE %', r; end $$;
