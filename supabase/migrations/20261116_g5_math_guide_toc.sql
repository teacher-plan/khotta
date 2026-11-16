-- ربط كل درس من رياضيات الخامس ف١ بصفحة «النشاط الأساسي» الخاصة به في دليل المعلم (طبعة ٢٠٢١).
-- الأرقام هنا صفحات PDF مباشرةً، لذا الإزاحة ١. متعادلة.
update public.teacher_guides tg set offset_pages=1, status='indexed', indexed_at=now(), toc=(
  select jsonb_agg(jsonb_build_object('guide_unit',c.unit,'guide_lesson',c.lesson,'guide_page',v.p,'matched_curriculum_id',c.id,'confidence','high') order by c.sort)
  from public.curriculum c join (values (1,24),(2,26),(3,28),(4,34),(5,40),(6,48),(7,52),(8,56),(9,58),(10,64),(11,66),(12,68),(13,72),(14,76),(15,80),(16,88),(17,92),(18,100),(19,108),(20,112),(21,118),(22,122),(23,128),(24,132),(25,134),(26,142),(27,146),(28,148),(29,152),(30,158),(31,162),(32,166),(33,172)) v(s,p) on v.s=c.sort
  where c.semester='الفصل الأول' and c.grade=5 and c.subject='الرياضيات')
where tg.semester='الفصل الأول' and tg.grade=5 and tg.subject='الرياضيات';
