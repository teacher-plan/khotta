-- ٢٧ نوفمبر: صيغة المخاطبة تُعرف من التسجيل. كانت رسائل ما قبل الدخول (الترحيب،
-- تلجرام، بريد التفعيل) مؤنّثةً ثابتاً فتصل المعلّمين الرجال بالمؤنّث. صار نموذج
-- التسجيل يسأل «معلّم/معلّمة» ويحفظه هنا، فتقرؤه الرسائل والمنصّة عند أول دخول.
alter table public.pre_registrations add column if not exists gender text
  check (gender in ('m','f'));

drop function if exists public.register_teacher(text,text,text,text,text);
create or replace function public.register_teacher(p_name text, p_phone text, p_email text, p_stage text,
  p_referred_by text default null, p_gender text default null)
returns void language plpgsql security definer set search_path to 'public' as $function$
declare v_email text := lower(trim(p_email));
        v_ref text := nullif(left(trim(coalesce(p_referred_by,'')), 60), '');
        v_g text := case when p_gender in ('m','f') then p_gender end;
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
  if v_ref is not null then
    v_ref := coalesce((select code from referrers where lower(code) = lower(v_ref) limit 1), v_ref);
  end if;
  insert into pre_registrations(name, phone, email, stage, referred_by, gender) values (p_name, p_phone, v_email, p_stage, v_ref, v_g);
end;
$function$;
grant execute on function public.register_teacher(text,text,text,text,text,text) to anon, authenticated;
