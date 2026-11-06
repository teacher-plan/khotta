-- ════════════════════════════════════════════════════════════════
-- P59 — مدارس منصّة الحلقة الأولى (cycle1): رمز مدرسة، وانضمام المعلّم،
-- وحساب إدارة مشترك يرى غياب معلّمي مدرسته وسلوك طلابهم.
--
-- التصميم:
--   • c1_schools: المدرسة واسمها ورمز الانضمام وبريد حساب الإدارة المشترك.
--   • c1_school_members: معلّمٌ ← مدرسةٌ واحدة (المفتاح هو المعلّم).
--   • لا قراءة مباشرة لأيٍّ منهما من المتصفح: RLS مفعّلة بلا سياسات للمستخدمين،
--     وكل شيءٍ يمرّ عبر دوالّ SECURITY DEFINER تتحقّق من الهوية بنفسها.
--   • الإدارة لا تقرأ ملفات المعلّمين: c1_school_dashboard يُرجع لها حقولاً
--     محدّدة فقط (الاسم، الشعب وطلابها، الغياب، سجلّ السلوك) ولمعلّمي مدرستها فقط.
--   • حساب الإدارة يُعرَّف في allowed_emails بالحلقة 'school'، فيفتح التطبيق
--     نفسه على واجهة الإدارة بدل واجهة المعلّم.
-- متعادلة (idempotent): إعادة تشغيلها لا تضرّ.
-- ════════════════════════════════════════════════════════════════

create table if not exists public.c1_schools (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  code        text not null unique,
  admin_email text not null unique,
  created_at  timestamptz not null default now()
);

create table if not exists public.c1_school_members (
  teacher_id uuid primary key references auth.users(id) on delete cascade,
  school_id  uuid not null references public.c1_schools(id) on delete cascade,
  joined_at  timestamptz not null default now()
);
create index if not exists c1_school_members_school on public.c1_school_members(school_id);

alter table public.c1_schools enable row level security;
alter table public.c1_school_members enable row level security;
revoke all on public.c1_schools from anon, authenticated;
revoke all on public.c1_school_members from anon, authenticated;

-- رمزٌ قصير سهل الإملاء: ٦ أحرف بلا الحروف المتشابهة (0/O، 1/I/L)
create or replace function public.c1_gen_school_code()
returns text language plpgsql set search_path = public as $$
declare a text := 'ABCDEFGHJKMNPQRSTUVWXYZ23456789'; c text; i int;
begin
  loop
    c := '';
    for i in 1..6 loop c := c || substr(a, 1 + floor(random() * length(a))::int, 1); end loop;
    exit when not exists (select 1 from c1_schools where code = c);
  end loop;
  return c;
end $$;

-- المدرسة التي يديرها المستخدم الحالي (بريد حساب الإدارة)
create or replace function public.c1_admin_school_id()
returns uuid language sql stable security definer set search_path = public as $$
  select id from c1_schools where lower(admin_email) = lower(coalesce(auth.jwt()->>'email',''));
$$;

-- ═══ مشرف خُطّة: إنشاء مدرسة وقائمة المدارس ═══
create or replace function public.c1_admin_create_school(p_name text, p_admin_email text)
returns json language plpgsql security definer set search_path = public as $$
declare s c1_schools;
begin
  if not is_app_admin() then raise exception 'forbidden'; end if;
  if coalesce(trim(p_name),'') = '' or coalesce(trim(p_admin_email),'') = '' then raise exception 'missing'; end if;
  insert into c1_schools(name, code, admin_email)
    values (trim(p_name), c1_gen_school_code(), lower(trim(p_admin_email)))
    returning * into s;
  return json_build_object('id', s.id, 'name', s.name, 'code', s.code, 'admin_email', s.admin_email);
end $$;

create or replace function public.c1_admin_list_schools()
returns json language plpgsql stable security definer set search_path = public as $$
begin
  if not is_app_admin() then raise exception 'forbidden'; end if;
  return coalesce((select json_agg(json_build_object(
      'id', s.id, 'name', s.name, 'code', s.code, 'admin_email', s.admin_email, 'created_at', s.created_at,
      'teachers', (select count(*) from c1_school_members m where m.school_id = s.id))
    order by s.created_at desc) from c1_schools s), '[]'::json);
end $$;

create or replace function public.c1_admin_delete_school(p_id uuid)
returns void language plpgsql security definer set search_path = public as $$
begin
  if not is_app_admin() then raise exception 'forbidden'; end if;
  delete from c1_schools where id = p_id;
end $$;

-- ═══ المعلّم: الانضمام بالرمز، ومدرستي، والمغادرة ═══
create or replace function public.c1_join_school(p_code text)
returns json language plpgsql security definer set search_path = public as $$
declare s c1_schools;
begin
  if auth.uid() is null then raise exception 'unauthorized'; end if;
  select * into s from c1_schools where code = upper(trim(coalesce(p_code,'')));
  if s.id is null then return json_build_object('ok', false, 'error', 'bad_code'); end if;
  insert into c1_school_members(teacher_id, school_id) values (auth.uid(), s.id)
    on conflict (teacher_id) do update set school_id = excluded.school_id, joined_at = now();
  return json_build_object('ok', true, 'id', s.id, 'name', s.name);
end $$;

create or replace function public.c1_my_school()
returns json language sql stable security definer set search_path = public as $$
  select json_build_object('id', s.id, 'name', s.name)
  from c1_school_members m join c1_schools s on s.id = m.school_id
  where m.teacher_id = auth.uid();
$$;

create or replace function public.c1_leave_school()
returns void language sql security definer set search_path = public as $$
  delete from c1_school_members where teacher_id = auth.uid();
$$;

-- ═══ حساب الإدارة ═══
-- بيانات اللوحة: لكل معلّمٍ في المدرسة حقولٌ محدّدة فقط من ملفّه
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
        'beh_log', coalesce(p.data->'beh_log', '{}'::jsonb),
        'updated_at', p.updated_at
      ) order by coalesce(p.data->>'display_name', p.email, ''))
      from c1_school_members m
      left join cycle1_profiles p on p.id = m.teacher_id
      where m.school_id = sid), '[]'::json)
  );
end $$;

create or replace function public.c1_school_remove_teacher(p_teacher uuid)
returns void language plpgsql security definer set search_path = public as $$
declare sid uuid := c1_admin_school_id();
begin
  if sid is null then raise exception 'forbidden'; end if;
  delete from c1_school_members where teacher_id = p_teacher and school_id = sid;
end $$;

create or replace function public.c1_school_regen_code()
returns text language plpgsql security definer set search_path = public as $$
declare sid uuid := c1_admin_school_id(); c text;
begin
  if sid is null then raise exception 'forbidden'; end if;
  c := c1_gen_school_code();
  update c1_schools set code = c where id = sid;
  return c;
end $$;

revoke all on function public.c1_gen_school_code() from public, anon, authenticated;
revoke execute on function public.c1_admin_school_id() from public, anon;
revoke execute on function public.c1_admin_create_school(text, text) from public, anon;
revoke execute on function public.c1_admin_list_schools() from public, anon;
revoke execute on function public.c1_admin_delete_school(uuid) from public, anon;
revoke execute on function public.c1_join_school(text) from public, anon;
revoke execute on function public.c1_my_school() from public, anon;
revoke execute on function public.c1_leave_school() from public, anon;
revoke execute on function public.c1_school_dashboard() from public, anon;
revoke execute on function public.c1_school_remove_teacher(uuid) from public, anon;
revoke execute on function public.c1_school_regen_code() from public, anon;
grant execute on function public.c1_admin_school_id() to authenticated;
grant execute on function public.c1_admin_create_school(text, text) to authenticated;
grant execute on function public.c1_admin_list_schools() to authenticated;
grant execute on function public.c1_admin_delete_school(uuid) to authenticated;
grant execute on function public.c1_join_school(text) to authenticated;
grant execute on function public.c1_my_school() to authenticated;
grant execute on function public.c1_leave_school() to authenticated;
grant execute on function public.c1_school_dashboard() to authenticated;
grant execute on function public.c1_school_remove_teacher(uuid) to authenticated;
grant execute on function public.c1_school_regen_code() to authenticated;
