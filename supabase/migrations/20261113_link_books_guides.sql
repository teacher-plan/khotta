-- ربط كتب الطالب بأدلّة المعلّم لستّة مناهج (ف١): إزاحة الصفحات + فهرس الدليل مطابَقاً لدروس curriculum. متعادلة.
update public.book_sources set offset_pages=3, updated_at=now() where semester='الفصل الأول' and grade='8' and subject='العلوم';
update public.book_sources set offset_pages=3, updated_at=now() where semester='الفصل الأول' and grade='7' and subject='التربية الإسلامية';
update public.book_sources set offset_pages=3, updated_at=now() where semester='الفصل الأول' and grade='7' and subject='اللغة العربية';
update public.book_sources set offset_pages=3, updated_at=now() where semester='الفصل الأول' and grade='5' and subject='التربية الإسلامية';
update public.book_sources set offset_pages=2, updated_at=now() where semester='الفصل الأول' and grade='9' and subject='الرياضيات';
update public.book_sources set offset_pages=1, updated_at=now() where semester='الفصل الأول' and grade='8' and subject='التربية الإسلامية';
update public.teacher_guides tg set offset_pages=2, status='indexed', indexed_at=now(), toc=(
  select jsonb_agg(jsonb_build_object('guide_unit',c.unit,'guide_lesson',c.lesson,'guide_page',v.p,'matched_curriculum_id',c.id,'confidence','high') order by c.sort)
  from public.curriculum c join (values (1,38),(2,40),(3,43),(4,46),(5,50),(6,51),(7,53),(8,56),(9,81),(10,83),(11,84),(12,87),(13,91),(14,96),(15,98),(16,100),(17,103),(18,106),(19,129),(20,132),(21,136),(22,139),(23,142),(24,144),(25,154),(26,158),(27,159),(28,162),(29,164),(30,180),(31,182),(32,185),(33,187),(34,192),(35,193),(36,197),(37,205),(38,220),(39,222),(40,223),(41,225),(42,228),(43,231),(44,233),(45,235)) v(s,p) on v.s=c.sort
  where c.semester='الفصل الأول' and c.grade=8 and c.subject='العلوم')
where tg.semester='الفصل الأول' and tg.grade=8 and tg.subject='العلوم';
update public.teacher_guides tg set offset_pages=2, status='indexed', indexed_at=now(), toc=(
  select jsonb_agg(jsonb_build_object('guide_unit',c.unit,'guide_lesson',c.lesson,'guide_page',v.p,'matched_curriculum_id',c.id,'confidence','high') order by c.sort)
  from public.curriculum c join (values (1,29),(2,34),(3,42),(4,48),(5,52),(6,57),(7,63),(8,69),(9,74),(10,80),(11,86),(12,91),(13,96),(14,102),(15,109),(16,114),(17,120),(18,126),(19,131),(20,136),(21,143),(22,150),(23,155),(24,160),(25,165),(26,169),(27,173)) v(s,p) on v.s=c.sort
  where c.semester='الفصل الأول' and c.grade=7 and c.subject='التربية الإسلامية')
where tg.semester='الفصل الأول' and tg.grade=7 and tg.subject='التربية الإسلامية';
update public.teacher_guides tg set offset_pages=2, status='indexed', indexed_at=now(), toc=(
  select jsonb_agg(jsonb_build_object('guide_unit',c.unit,'guide_lesson',c.lesson,'guide_page',v.p,'matched_curriculum_id',c.id,'confidence','high') order by c.sort)
  from public.curriculum c join (values (1,26),(2,32),(3,37),(4,72),(5,76),(6,81),(7,89),(8,120),(9,126),(10,132),(11,158),(12,162),(13,167),(14,172),(15,46),(16,52),(17,56),(18,60),(19,63),(20,68),(21,96),(22,100),(23,105),(24,110),(25,112),(26,116),(27,140),(28,143),(29,147),(30,150),(31,152),(32,155),(33,180),(34,185),(35,189),(36,192),(37,194),(38,198)) v(s,p) on v.s=c.sort
  where c.semester='الفصل الأول' and c.grade=7 and c.subject='اللغة العربية')
where tg.semester='الفصل الأول' and tg.grade=7 and tg.subject='اللغة العربية';
update public.teacher_guides tg set offset_pages=2, status='indexed', indexed_at=now(), toc=(
  select jsonb_agg(jsonb_build_object('guide_unit',c.unit,'guide_lesson',c.lesson,'guide_page',v.p,'matched_curriculum_id',c.id,'confidence','high') order by c.sort)
  from public.curriculum c join (values (1,28),(2,34),(3,41),(4,47),(5,52),(6,57),(7,65),(8,72),(9,77),(10,84),(11,90),(12,94),(13,98),(14,102),(15,108),(16,113),(17,123),(18,129),(19,133),(20,141),(21,146),(22,152),(23,157),(24,162),(25,168),(26,172),(27,177)) v(s,p) on v.s=c.sort
  where c.semester='الفصل الأول' and c.grade=5 and c.subject='التربية الإسلامية')
where tg.semester='الفصل الأول' and tg.grade=5 and tg.subject='التربية الإسلامية';
update public.teacher_guides tg set offset_pages=2, status='indexed', indexed_at=now(), toc=(
  select jsonb_agg(jsonb_build_object('guide_unit',c.unit,'guide_lesson',c.lesson,'guide_page',v.p,'matched_curriculum_id',c.id,'confidence','low') order by c.sort)
  from public.curriculum c join (values (1,21),(2,21),(3,21),(4,21),(5,21),(6,41),(7,41),(8,41),(9,41),(10,41),(11,41),(12,63),(13,63),(14,63),(15,63),(16,63),(17,81),(18,81),(19,81),(20,81),(21,81),(22,81),(23,103),(24,103),(25,103),(26,123),(27,123),(28,123),(29,123),(30,123),(31,123),(32,123),(33,167),(34,167),(35,187),(36,187),(37,187),(38,187),(39,209),(40,209)) v(s,p) on v.s=c.sort
  where c.semester='الفصل الأول' and c.grade=9 and c.subject='الرياضيات')
where tg.semester='الفصل الأول' and tg.grade=9 and tg.subject='الرياضيات';
