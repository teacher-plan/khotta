-- توقيت المدرسة (أوقات الطابور والحصص والفسحة) يرفعه حساب إدارة المدرسة، فيصير أوقاتَ
-- حصص كل معلّمٍ منضمّ إليها، ويصل كلَّ معلّمٍ إشعارٌ إلزاميّ قبل كل حصةٍ من حصصه بخمس دقائق.
-- متعادلة (idempotent).
alter table public.c1_schools add column if not exists timing jsonb;
alter table public.c1_schools add column if not exists timing_at timestamptz;

-- التوقيت لصاحب الطلب: حساب الإدارة ← مدرسته، والمعلّم ← المدرسة التي انضمّ إليها
create or replace function public.c1_school_timing()
returns json language plpgsql stable security definer set search_path = public as $$
declare s c1_schools; v_admin boolean := false;
begin
  select * into s from c1_schools where id = c1_admin_school_id();
  if found then v_admin := true;
  else
    select sc.* into s from c1_schools sc join c1_school_members m on m.school_id = sc.id where m.teacher_id = auth.uid();
    if not found then return null; end if;
  end if;
  return json_build_object('school', s.name, 'timing', s.timing, 'timing_at', s.timing_at, 'is_admin', v_admin);
end $$;
revoke all on function public.c1_school_timing() from public, anon;
grant execute on function public.c1_school_timing() to authenticated;

-- الحفظ لحساب الإدارة وحده، مع تحقّقٍ من الشكل: periods مصفوفة أزواج «HH:MM»
create or replace function public.c1_school_set_timing(p_timing jsonb)
returns void language plpgsql security definer set search_path = public as $$
declare v_id uuid := c1_admin_school_id(); e jsonb;
begin
  if v_id is null then raise exception 'forbidden'; end if;
  if p_timing is not null then
    if jsonb_typeof(p_timing->'periods') <> 'array' or jsonb_array_length(p_timing->'periods') not between 1 and 12 then raise exception 'bad_timing'; end if;
    for e in select * from jsonb_array_elements(p_timing->'periods') loop
      if not (e->>0 ~ '^\d\d:\d\d$' and e->>1 ~ '^\d\d:\d\d$') then raise exception 'bad_timing'; end if;
    end loop;
  end if;
  update c1_schools set timing = p_timing, timing_at = case when p_timing is null then null else now() end where id = v_id;
end $$;
revoke all on function public.c1_school_set_timing(jsonb) from public, anon;
grant execute on function public.c1_school_set_timing(jsonb) to authenticated;

-- كل دقيقةٍ في ساعات الدوام: هل تبدأ حصةٌ في مدرسةٍ ما بعد خمس دقائق؟ إن نعم نادِ c1-push.
-- الفحص في القاعدة لا في الدالّة: نداءٌ للدالّة فقط حين يوجد ما يُرسَل.
create or replace function public.c1_period_tick()
returns void language plpgsql security definer set search_path = public as $$
declare t text := to_char((now() at time zone 'Asia/Muscat') + interval '5 minutes', 'HH24:MI'); r record;
begin
  if extract(dow from (now() at time zone 'Asia/Muscat')) not in (0,1,2,3,4) then return; end if;
  for r in
    select s.id, (x.i - 1)::int as p
    from c1_schools s, jsonb_array_elements(s.timing->'periods') with ordinality as x(v, i)
    where s.timing is not null and x.v->>0 = t
  loop
    perform c1_push_call('period', jsonb_build_object('school_id', r.id, 'p', r.p));
  end loop;
end $$;
revoke all on function public.c1_period_tick() from public, anon, authenticated;

do $$ begin
  perform cron.unschedule(jobname) from cron.job where jobname = 'c1-push-period';
end $$;
-- ٦:٠٠ص – ٢:٥٩م بتوقيت مسقط (UTC+4)، الأحد – الخميس
select cron.schedule('c1-push-period', '* 2-10 * * 0-4', $$select public.c1_period_tick()$$);
