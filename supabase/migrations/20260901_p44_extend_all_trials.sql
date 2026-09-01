-- تمديد كل الحسابات التجريبية (allowed_emails.expires_at IS NOT NULL — صفٌّ
-- بلا expires_at يعني حساباً دائماً/مدفوعاً ولا يُمسّ هنا) إلى ١٠/٩/٢٠٢٦،
-- بما فيها الحسابات المنتهية بالفعل — تُعاد صلاحيتها بنفس الحركة (تحديث
-- expires_at وحده يكفي: سياسة allowed_own_select تُخفي الصفَّ عن صاحبته
-- فقط حين expires_at <= now()، فتمديده يعيد ظهوره فوراً بلا أي تعديلٍ آخر).
update public.allowed_emails
set expires_at = '2026-09-10 23:59:59+04'::timestamptz
where expires_at is not null;

-- تحقّق: select email, expires_at from public.allowed_emails where expires_at is not null order by email;
--        يجب أن تكون كل الصفوف الآن ٢٠٢٦-٠٩-١٠ ٢٣:٥٩:٥٩+٠٤ بلا استثناء.
