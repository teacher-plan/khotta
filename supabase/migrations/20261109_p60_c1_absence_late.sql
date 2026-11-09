-- ════════════════════════════════════════════════════════════════
-- P60 — التأخّر في لوحة الإدارة: يُضاف حقل absence_late (المتأخّرون لكل
-- شعبة ويوم وحصة) إلى ما تُرجعه c1_school_dashboard لإدارة المدرسة.
-- الدالّة نفسها بحقلٍ زائد فقط؛ الصلاحيات كما هي في p59.
-- متعادلة (idempotent).
-- ════════════════════════════════════════════════════════════════
create or replace function public.c1_school_dashboard()
returns json language plpgsql stable security definer set search_path = public as $$
declare sid uuid := c1_admin_school_id(); s c1_schools;
begin
  if sid is null then raise exception 'forbidden'; end if;
  select * into s from c1_schools where id = sid;
  return json_build_object(
    'school', json_build_object('id', s.id, 'name', s.name, 'code', s.code),
    'teachers', coalesce((
      select json_agg(json_build_object(
        'id', m.teacher_id,
        'joined_at', m.joined_at,
        'name', coalesce(p.data->>'display_name', p.email, ''),
        'gender', p.data->>'teacher_gender',
        'grades', coalesce(p.data->'grades', '[]'::jsonb),
        'absence', coalesce(p.data->'absence', '{}'::jsonb),
        'absence_late', coalesce(p.data->'absence_late', '{}'::jsonb),
        'beh_log', coalesce(p.data->'beh_log', '{}'::jsonb),
        'updated_at', p.updated_at
      ) order by coalesce(p.data->>'display_name', p.email, ''))
      from c1_school_members m
      left join cycle1_profiles p on p.id = m.teacher_id
      where m.school_id = sid), '[]'::json)
  );
end $$;
revoke execute on function public.c1_school_dashboard() from public, anon;
grant execute on function public.c1_school_dashboard() to authenticated;
