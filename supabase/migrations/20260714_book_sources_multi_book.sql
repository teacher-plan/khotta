-- استثناء الحلقة الأولى: كل مادة لها ٣ كتب في الفصل الواحد بدل كتاب واحد.
-- يضيف عمود book_no (رقم الكتاب: ١/٢/٣...) لجدولي book_sources وcurriculum
-- بقيمة افتراضية ١ — لا يغيّر أي سلوك حالي لصفوف الحلقة الثانية (كتاب واحد دائماً = ١).

alter table public.book_sources
  add column if not exists book_no integer not null default 1;

alter table public.curriculum
  add column if not exists book_no integer not null default 1;

-- استبدال قيد التفرّد القديم (grade, subject, semester) بقيد يشمل رقم الكتاب،
-- حتى يمكن رفع أكثر من كتاب لنفس المادة/الصف/الفصل دون أن يُستبدل أحدها الآخر.
do $$
declare
  con record;
begin
  for con in
    select tc.constraint_name
    from information_schema.table_constraints tc
    where tc.table_schema = 'public'
      and tc.table_name = 'book_sources'
      and tc.constraint_type = 'UNIQUE'
      and (
        select array_agg(kcu.column_name order by kcu.column_name)
        from information_schema.key_column_usage kcu
        where kcu.constraint_name = tc.constraint_name
          and kcu.table_schema = 'public'
      ) = array['grade','semester','subject']::text[]
  loop
    execute format('alter table public.book_sources drop constraint %I', con.constraint_name);
  end loop;
end $$;

alter table public.book_sources
  add constraint book_sources_grade_subject_semester_book_no_key
  unique (grade, subject, semester, book_no);
