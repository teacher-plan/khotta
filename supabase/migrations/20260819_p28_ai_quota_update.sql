-- تحديث حصّة الذكاء الاصطناعي الشهرية لكل معلّمة إلى الاتفاق الحالي:
-- ٢٥٠ صورة (كانت ٦٥ — قديمة، تسبّبت في حجب توليد الصور فعلياً لمن
-- تجاوزتها) و١٠٠٠ استعمالٍ نصّي (كانت ٦٠٠).
insert into public.ai_settings (key, value, updated_at) values
  ('quota_img',  '250',  now()),
  ('quota_text', '1000', now())
on conflict (key) do update set value = excluded.value, updated_at = excluded.updated_at;
