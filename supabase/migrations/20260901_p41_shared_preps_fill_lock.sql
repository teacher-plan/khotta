-- إصلاح أمني: سياسة shared_preps_update كانت using(true) with check(true) —
-- أي معلّم مسجّل يستطيع استبدال exam_html/plan/slides لأي درسٍ موجود بالكامل
-- بمحتوى عشوائي (بما فيه HTML/JS)، لا فقط "ملء الناقص" كما كان القصد الأصلي
-- من عنوان الهجرة 20260712 (راجع تقرير الفحص الأمني: نتيجة عالية الخطورة).
--
-- الإصلاح: نُبقي السياسة مفتوحة (لأن أي معلم يجب أن يقدر يملأ حقلاً ناقصاً
-- لأي درس، لا درسه فقط — هذا هو التصميم المقصود لتجمّع "الخطة الذهبية")،
-- لكن نضيف Trigger يمنع تغيير أي عمود له قيمة غير فارغة مسبقاً — فتصبح كل
-- الأعمدة قابلة للملء مرة واحدة فقط، لا للاستبدال بعد ذلك.
create or replace function public.shared_preps_lock_filled()
returns trigger
language plpgsql
as $$
begin
  if old.plan is not null then new.plan := old.plan; end if;
  if old.slides is not null then new.slides := old.slides; end if;
  if old.exam_html is not null then new.exam_html := old.exam_html; end if;
  if old.info_b64 is not null then new.info_b64 := old.info_b64; end if;
  if old.slide_imgs is not null then new.slide_imgs := old.slide_imgs; end if;
  -- الأعمدة الوصفية (grade/subject/unit/lesson/created_by/created_at) لا تُغيَّر أبداً بعد الإنشاء
  new.grade := old.grade;
  new.subject := old.subject;
  new.unit := old.unit;
  new.lesson := old.lesson;
  new.created_by := old.created_by;
  new.created_at := old.created_at;
  return new;
end;
$$;

drop trigger if exists shared_preps_lock_filled_trg on public.shared_preps;
create trigger shared_preps_lock_filled_trg
  before update on public.shared_preps
  for each row
  execute function public.shared_preps_lock_filled();

-- تحقّق: بعد هذه الهجرة، UPDATE على عمودٍ مملوءٍ مسبقاً يُنفَّذ بلا خطأ لكن
-- بلا أثر (القيمة القديمة تبقى) — فتُغلَق ثغرة الاستبدال دون كسر ميزة "ملء الناقص".
