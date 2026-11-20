-- ════════════════════════════════════════════════════════════════════
-- ٢٠ نوفمبر — شعار المدرسة في الشهادات.
-- حساب إدارة المدرسة يرفع صورةً فيها الشعار، ويحدّد نموذج رؤيةٍ مكانه فقط،
-- ويُقصّ من الصورة الأصلية في المتصفّح، ثم يُحفظ عبر الدالّة c1-school-logo
-- (بمفتاح الخدمة، بعد التحقّق أن المستدعي إدارة هذه المدرسة). هنا العمود وقراءته.
-- الشعار يظهر في شهادات كل معلّمٍ:
--   • منضمٍّ إلى المدرسة برمزها، أو
--   • كتب اسمها بيده في ملفّه — بمطابقةٍ بعد تطبيع الاسم (بلا مسافات ولا تشكيل
--     ولا «مدرسة»، والهمزات ألفاً والتاء المربوطة هاءً).
-- متعادلة: إعادة تشغيلها لا تضرّ.
-- ════════════════════════════════════════════════════════════════════
alter table public.c1_schools add column if not exists logo_url text;
alter table public.c1_schools add column if not exists logo_at timestamptz;

create or replace function public.c1_norm_school(t text)
returns text language sql immutable set search_path = public as $$
  select replace(replace(
    regexp_replace(translate(coalesce(t,''), 'أإآة', 'اااه'), '[ً-ْـ[:space:]]', '', 'g'),
    'مدرسه', ''), 'باابي', 'بنابي');
$$;

-- الشعار المناسب للمستخدم الحالي: مدرسته الإدارية، أو مدرسته المنضمّ إليها، أو مطابقة اسم ملفّه
create or replace function public.c1_school_logo(p_name text default null)
returns json language plpgsql stable security definer set search_path = public as $$
declare s c1_schools; n text := c1_norm_school(p_name);
begin
  if auth.uid() is null then return null; end if;
  select * into s from c1_schools where id = c1_admin_school_id();
  if s.id is null then
    select c.* into s from c1_school_members m join c1_schools c on c.id = m.school_id where m.teacher_id = auth.uid();
  end if;
  if (s.id is null or s.logo_url is null) and length(n) >= 6 then
    select c.* into s from c1_schools c
      where c.logo_url is not null and length(c1_norm_school(c.name)) >= 6 and position(c1_norm_school(c.name) in n) > 0
      order by length(c1_norm_school(c.name)) desc limit 1;
  end if;
  if s.id is null then return null; end if;
  return json_build_object('school', s.name, 'logo_url', s.logo_url, 'logo_at', s.logo_at);
end $$;

revoke all on function public.c1_school_logo(text) from public, anon;
grant execute on function public.c1_school_logo(text) to authenticated;
revoke all on function public.c1_norm_school(text) from public, anon;
grant execute on function public.c1_norm_school(text) to authenticated;
