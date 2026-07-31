-- قراءة المشرفة لاستهلاك الذكاء الاصطناعي
--
-- جدول ai_usage أُنشئ بسياسةٍ واحدة: كل معلّمة تقرأ صفّها فقط (usage_read_own).
-- وهي سياسةٌ صحيحة للمعلّمة لكنها تحجب الجدول عن المشرفة أيضاً، فلا ترى من
-- يستهلك الرصيد الذي خصّصته. هذه السياسة تفتحه للمشرفة وحدها.
--
-- تُنفَّذ مرّة واحدة من محرّر SQL في لوحة سوبابيز.

-- الجدول قد لا يكون موجوداً بعد: يُنشأ عند أول استخدامٍ للذكاء الاصطناعي
-- من داخل دالّة الحصص. ننشئه هنا بالشكل نفسه كي لا تفشل السياسة أدناه.
create table if not exists public.ai_usage (
  user_id uuid not null,
  month text not null,
  kind text not null,
  count int not null default 0,
  primary key (user_id, month, kind)
);

alter table public.ai_usage enable row level security;

drop policy if exists "usage_read_own" on public.ai_usage;
create policy "usage_read_own" on public.ai_usage
  for select to authenticated
  using (user_id = auth.uid() or is_app_admin());

-- لا سياسة كتابة عمداً: الكتابة تتمّ من دوالّ الحافة بمفتاح الخدمة الذي
-- يتجاوز RLS. فتح الكتابة للمتصفّح يعني أن أيّ معلّمة تستطيع تصفير عدّادها.
