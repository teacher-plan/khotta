-- اللغة العربية للحادي عشر ف١: وحدةٌ واحدة لكل فرع (طلب الأستاذ عيسى) بدل وحدةٍ لكل محور.
-- الدروس وترتيبها وصفحاتها كما هي؛ ويُحدَّث اسم الوحدة في فهرس دليل المعلم. متعادلة.
update public.curriculum set unit = case
    when unit like 'الأدب والنصوص%' then 'الأدب والنصوص'
    when unit like 'النقد الأدبي%' then 'النقد الأدبي'
    when unit like 'المطالعة%' then 'المطالعة'
    when unit = 'التعبير' then 'التعبير'
    when unit like 'المفيد: النحو والصرف' then 'النحو والصرف'
    when unit like 'المفيد: البلاغة' then 'البلاغة'
    when unit like 'المفيد: العروض' then 'العروض'
    when unit like 'المفيد: مراجعة' then 'مراجعة: نص تطبيقي'
    else unit end
where semester='الفصل الأول' and grade=11 and subject='اللغة العربية';
update public.teacher_guides tg set toc=(
  select jsonb_agg(e || jsonb_build_object('guide_unit',c.unit) order by c.sort)
  from jsonb_array_elements(tg.toc) e join public.curriculum c on c.id::text = e->>'matched_curriculum_id')
where tg.semester='الفصل الأول' and tg.grade=11 and tg.subject='اللغة العربية' and tg.toc is not null;
