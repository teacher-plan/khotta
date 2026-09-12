-- القالب المعتمد صار يُرفع كملفٍّ حقيقي (PDF أو Word) لا نصاً مُلصَقاً، وناتج
-- التوليد صار ملفّ Word فعلياً بنفس تنسيق القالب (لا معاينة HTML فقط) —
-- يحتاج عمود رابط الملف الناتج.
alter table public.lesson_prep_generations
  add column if not exists docx_url text;

-- تحقّق: select docx_url from lesson_prep_generations limit 1; -- NULL لأي صفٍّ سابق (طبيعي، لم يُولَّد بعد بهذا المسار)
