-- ربط دليل التربية الإسلامية للصف الثامن (الطبعة الحالية) بدروس الكتاب. متعادلة.
update public.teacher_guides tg set offset_pages=2, status='indexed', indexed_at=now(), toc=(
  select jsonb_agg(jsonb_build_object('guide_unit',c.unit,'guide_lesson',c.lesson,'guide_page',v.p,'matched_curriculum_id',c.id,'confidence','high') order by c.sort)
  from public.curriculum c join (values (1,27),(2,33),(3,38),(4,43),(5,48),(6,53),(7,59),(8,67),(9,74),(10,80),(11,88),(12,94),(13,99),(14,104),(15,110),(16,115),(17,120),(18,126),(19,130),(20,136),(21,141),(22,147),(23,152),(24,158),(25,163),(26,171),(27,176)) v(s,p) on v.s=c.sort
  where c.semester='الفصل الأول' and c.grade=8 and c.subject='التربية الإسلامية')
where tg.semester='الفصل الأول' and tg.grade=8 and tg.subject='التربية الإسلامية';
