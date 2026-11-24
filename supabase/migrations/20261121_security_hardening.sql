-- تقوية أمنية (فحص ٢١ نوفمبر). متعادلة: تُعاد بأمان.

-- ١) الإشعارات: كان أيّ معلّمٍ مسجّل يُدرج إشعاراً بأي نصٍّ لأي معلّم (أو للجميع)،
--    فيصل إلى الهاتف بعنوان «رسالة من الإدارة». الآن: الإدارة وحدها تُرسل الرسائل
--    العامة؛ والمعلّم يُدرج فقط إشعارَي المكتبة المرتبطين بملفٍّ (تقييم، ومشاركة)،
--    وهذان لا يُرسَلان إلى الهاتف أصلاً (مشغّل الدفع يتجاهل ما له item_id).
drop policy if exists "c1notif_insert_attributable" on public.c1_notifications;
create policy "c1notif_insert_attributable" on public.c1_notifications
  for insert to authenticated
  with check (
    public.is_app_admin()
    or (
      item_id is not null
      and char_length(coalesce(message, '')) <= 600
      and ((kind = 'info' and user_id is not null) or (kind = 'library_share' and user_id is null))
    )
  );

-- ٢) مجلد exams/ في المخزن العام: سياسة رفعٍ مفتوحة لأي معلّم بلا قيدٍ على النوع
--    أو الصاحب، ولا تستعملها المنصّة الحالية. تُحذف.
drop policy if exists "teachers upload exam files" on storage.objects;

-- ٣) جدول المدارس القديم كان مقروءاً لأي زائر بلا تسجيل (ومعه كلمات المرور المشفّرة).
--    القراءة الآن للإدارة فقط؛ تسجيل دخول المدرسة يمرّ بالدوال الآمنة كما هو.
drop policy if exists "schools_read" on public.schools;
create policy "schools_read" on public.schools for select to authenticated using (public.is_app_admin());

-- ٤) دخول المدارس: حدٌّ للمحاولات الفاشلة (١٠ كل ١٥ دقيقة لكل اسم مستخدم).
create table if not exists public.school_login_fails (
  username text not null,
  at timestamptz not null default now()
);
create index if not exists school_login_fails_idx on public.school_login_fails (username, at);
alter table public.school_login_fails enable row level security;
revoke all on public.school_login_fails from anon, authenticated;

create or replace function public.school_login(p_username text, p_password text)
returns table(id bigint, name text, username text, structure jsonb, token uuid)
language plpgsql security definer set search_path to 'public', 'extensions'
as $function$
declare v_row schools%rowtype; v_token uuid; v_user text := lower(coalesce(p_username, ''));
begin
  if (select count(*) from school_login_fails f where f.username = v_user and f.at > now() - interval '15 minutes') >= 10 then
    return;
  end if;
  select * into v_row from schools s where lower(s.username) = v_user limit 1;
  if v_row.id is null or v_row.password_hash is null or crypt(p_password, v_row.password_hash) <> v_row.password_hash then
    insert into school_login_fails(username) values (v_user);
    delete from school_login_fails where at < now() - interval '1 day';
    return;
  end if;
  insert into school_sessions(school_id) values (v_row.id) returning school_sessions.token into v_token;
  return query select v_row.id, v_row.name, v_row.username, v_row.structure, v_token;
end;
$function$;

-- ٥) التسجيل العام: سقفٌ عامّ يمنع الإغراق بتسجيلاتٍ وهمية (وبرسائل تلغرام تتبعها).
create or replace function public.register_teacher(p_name text, p_phone text, p_email text, p_stage text, p_referred_by text default null::text)
returns void
language plpgsql security definer set search_path to 'public'
as $function$
declare v_email text := lower(trim(p_email));
begin
  if (select count(*) from pre_registrations where created_at > now() - interval '10 minutes') >= 20 then
    raise exception 'rate_limited';
  end if;
  if char_length(coalesce(p_name, '')) > 120 or char_length(coalesce(p_phone, '')) > 30 or char_length(coalesce(v_email, '')) > 200 then
    raise exception 'invalid_input';
  end if;
  if v_email !~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$' then
    raise exception 'invalid_email_domain';
  end if;
  if exists (select 1 from pre_registrations where stage = p_stage and (phone = p_phone or lower(email) = v_email)) then
    raise exception 'already_registered';
  end if;
  insert into pre_registrations(name, phone, email, stage, referred_by) values (p_name, p_phone, v_email, p_stage, p_referred_by);
end;
$function$;
