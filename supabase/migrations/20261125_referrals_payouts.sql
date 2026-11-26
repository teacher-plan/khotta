-- نظام الإحالات: دفعات العمولة في القاعدة بدل localStorage، ومبلغ الاشتراك
-- لحظة الدفع، وتوحيد كود الإحالة عند التسجيل.

-- ١) مبلغ الاشتراك وتاريخ الدفع لكل تسجيل: العمولة تُحسب على ما دُفع فعلاً،
--    فلا يغيّر تعديلُ السعر لاحقاً عمولاتٍ سابقة.
alter table public.pre_registrations
  add column if not exists paid_amount numeric,
  add column if not exists paid_at timestamptz;

-- ٢) دفعات العمولة للأصدقاء: سجلٌّ دائم مشترك بين أجهزة المشرف.
create table if not exists public.referral_payouts (
  id bigint generated always as identity primary key,
  referrer_code text not null,
  amount numeric not null check (amount > 0),
  note text,
  paid_at timestamptz not null default now(),
  created_by uuid default auth.uid()
);
create index if not exists referral_payouts_code_idx on public.referral_payouts (referrer_code);
alter table public.referral_payouts enable row level security;
drop policy if exists ref_payouts_admin_all on public.referral_payouts;
create policy ref_payouts_admin_all on public.referral_payouts
  for all to authenticated using (is_app_admin()) with check (is_app_admin());
grant select, insert, update, delete on public.referral_payouts to authenticated;

-- ٣) التسجيل: يُوحَّد كود الإحالة (مسافات، حالة الأحرف) إلى كود الصديق
--    المسجَّل، فلا تضيع إحالةٌ لأن الرابط كُتب ?ref=Hala بدل hala.
--    الكود المجهول يُحفظ كما هو (يظهر في الجدول للمراجعة).
create or replace function public.register_teacher(p_name text, p_phone text, p_email text, p_stage text, p_referred_by text default null::text)
 returns void
 language plpgsql
 security definer
 set search_path to 'public'
as $function$
declare v_email text := lower(trim(p_email));
        v_ref text := nullif(left(trim(coalesce(p_referred_by,'')), 60), '');
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
  insert into pre_registrations(name, phone, email, stage, referred_by) values (p_name, p_phone, v_email, p_stage, v_ref);
end;
$function$;

-- ٤) ترحيل: التسجيلات المدفوعة سابقاً تأخذ السعر الحالي مبلغاً لها.
update public.pre_registrations
   set paid_amount = (select value::numeric from app_settings where key='subscription_price'),
       paid_at = coalesce(paid_at, created_at)
 where payment_status='paid' and paid_amount is null;

-- ٥) (٢٥ نوفمبر — طلب الأستاذ عيسى) عمولة بمبلغ ثابت لكل صديق بدل النسبة:
--    commission_amount ر.ع لكل مشترك يدفع عبر رابطه، ويُثبَّت المبلغ على
--    التسجيل لحظة تأكيد الدفع (referral_commission) فلا يغيّره تعديلٌ لاحق.
--    الأصدقاء الحاليون: المبلغ = نسبتهم × السعر الحالي.
alter table public.referrers add column if not exists commission_amount numeric check (commission_amount >= 0);
update public.referrers set commission_amount = round(coalesce(commission_rate,20)/100.0 * (select value::numeric from app_settings where key='subscription_price'), 2) where commission_amount is null;
alter table public.pre_registrations add column if not exists referral_commission numeric;
update public.pre_registrations p set referral_commission = f.commission_amount
  from public.referrers f where p.referred_by = f.code and p.payment_status='paid' and p.referral_commission is null;
