do $$ begin
  if exists (select 1 from public.curriculum where grade=6 and subject='التربية الإسلامية' and semester='الفصل الأول') then raise exception 'curriculum rows already exist'; end if;
  if not exists (select 1 from public.book_sources where grade='6' and subject='التربية الإسلامية' and semester='الفصل الأول' and page_count=182) then raise exception 'new book not imported yet'; end if;
end $$;
create temp table _t(sort int, unit text, lesson text, page int, gpage int);
insert into _t values
(1,'الوحدة الأولى','مخارج الحروف',22,29),
(2,'الوحدة الأولى','سورة البقرة (183–185) تلاوة وفهم',29,36),
(3,'الوحدة الأولى','ثواب العمل الصالح (حديث شريف)',35,44),
(4,'الوحدة الأولى','من دلائل وحدانية الله تعالى',40,50),
(5,'الوحدة الأولى','أنواع الصيام',45,56),
(6,'الوحدة الأولى','التخطيط للهجرة النبوية',50,61),
(7,'الوحدة الأولى','من آداب الأسواق',56,68),
(8,'الوحدة الثانية','مقدمة في أحكام النون الساكنة والتنوين',64,76),
(9,'الوحدة الثانية','سورة المدثر (11–27) تلاوة وفهم',69,82),
(10,'الوحدة الثانية','اترك ما لا يعنيني (حديث شريف)',73,88),
(11,'الوحدة الثانية','معجزات الرسل عليهم السلام',79,94),
(12,'الوحدة الثانية','زكاة الفطر',83,100),
(13,'الوحدة الثانية','الهجرة المباركة',89,107),
(14,'الوحدة الثانية','الاعتدال منهجي في الحياة',95,112),
(15,'الوحدة الثالثة','الإظهار الحلقي في النون الساكنة والتنوين',102,119),
(16,'الوحدة الثالثة','سورة الحجرات (10–13) تلاوة وفهم',107,124),
(17,'الوحدة الثالثة','من فضائل الأعمال (حديث شريف)',114,130),
(18,'الوحدة الثالثة','الله الحليم',120,135),
(19,'الوحدة الثالثة','من أحكام صلاة الجمعة',125,140),
(20,'الوحدة الثالثة','بناء المسجد',131,146),
(21,'الوحدة الثالثة','التزم الحق',137,151),
(22,'الوحدة الرابعة','الإدغام في النون الساكنة والتنوين',144,157),
(23,'الوحدة الرابعة','سورة المزمل الآية (20) تلاوة وفهم',149,163),
(24,'الوحدة الرابعة','هجر المسلم حرام (حديث شريف)',157,168),
(25,'الوحدة الرابعة','القرآن الكريم معجزة خالدة',164,174),
(26,'الوحدة الرابعة','الاستدراك في الصلاة',170,179),
(27,'الوحدة الرابعة','الصحابي عبدالله بن عمر رضي الله عنهما',175,185);
insert into public.curriculum (semester,grade,subject,unit,lesson,sort,page,book_no)
  select 'الفصل الأول',6,'التربية الإسلامية',unit,lesson,sort,page,1 from _t order by sort;
update public.book_sources set offset_pages=2, updated_at=now() where grade='6' and subject='التربية الإسلامية' and semester='الفصل الأول' and book_no=1;
update public.teacher_guides set
  toc=(select jsonb_agg(jsonb_build_object('guide_unit',a.unit,'guide_lesson',a.lesson,'guide_page',a.gpage,'matched_curriculum_id',c.id,'confidence','high') order by a.sort)
       from _t a join public.curriculum c on c.grade=6 and c.subject='التربية الإسلامية' and c.semester='الفصل الأول' and c.sort=a.sort),
  offset_pages=1, status='indexed', indexed_at=now(), updated_at=now()
  where grade=6 and subject='التربية الإسلامية' and semester='الفصل الأول';
select (select count(*) from public.curriculum where grade=6 and subject='التربية الإسلامية' and semester='الفصل الأول') cur_rows,
       (select offset_pages||'/'||page_count from public.book_sources where grade='6' and subject='التربية الإسلامية' and semester='الفصل الأول') book,
       (select jsonb_array_length(toc)||' / '||status||' / off '||offset_pages||' / '||page_count from public.teacher_guides where grade=6 and subject='التربية الإسلامية' and semester='الفصل الأول') guide;
