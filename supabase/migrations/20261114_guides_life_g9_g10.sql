-- دليلا المعلم للمهارات الحياتية (التاسع والعاشر ف١): إزاحة الصفحات وفهرسٌ بمستوى الوحدة
-- (كل درسٍ يشير إلى بداية وحدته في الدليل؛ الدليلان لا يفصّلان صفحات الدروس في فهرسهما). متعادلة.
update public.teacher_guides tg set offset_pages=1, status='indexed', indexed_at=now(), toc=(
  select jsonb_agg(jsonb_build_object('guide_unit',c.unit,'guide_lesson',c.lesson,'guide_page',v.p,'matched_curriculum_id',c.id,'confidence','low') order by c.sort)
  from public.curriculum c join (values (1,18),(2,18),(3,27),(4,27),(5,27),(6,37),(7,37),(8,43),(9,43)) v(s,p) on v.s=c.sort
  where c.semester='الفصل الأول' and c.grade=9 and c.subject='المهارات الحياتية')
where tg.semester='الفصل الأول' and tg.grade=9 and tg.subject='المهارات الحياتية';
update public.teacher_guides tg set offset_pages=2, status='indexed', indexed_at=now(), toc=(
  select jsonb_agg(jsonb_build_object('guide_unit',c.unit,'guide_lesson',c.lesson,'guide_page',v.p,'matched_curriculum_id',c.id,'confidence','low') order by c.sort)
  from public.curriculum c join (values (1,21),(2,21),(3,47),(4,47),(5,65),(6,65),(7,95),(8,95)) v(s,p) on v.s=c.sort
  where c.semester='الفصل الأول' and c.grade=10 and c.subject='المهارات الحياتية')
where tg.semester='الفصل الأول' and tg.grade=10 and tg.subject='المهارات الحياتية';
