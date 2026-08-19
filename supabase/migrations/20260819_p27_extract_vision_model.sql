-- model_extract كان فارغاً، فيتّبع الإعداد العام (اليوم: DeepSeek — نصّيٌّ
-- لا يقرأ الصور). "استخراج الدروس" مهمّةٌ بصرية (تقرأ صفحات الكتاب)، فكان
-- يعمل فعلياً بمعرفة النموذج العامة بدل الكتاب المعتمد، بلا أي خطأٍ ظاهر.
--
-- ضُبط على نفس نموذج شقيقتيه البصريّتين (model_segment وmodel_summary):
-- Gemini 2.5 Flash — لا اختيارٌ جديد، بل توحيدٌ مع نمطٍ قائم فعلاً.
insert into public.ai_settings (key, value, updated_at)
values ('model_extract', 'google/gemini-2.5-flash', now())
on conflict (key) do update set value = excluded.value, updated_at = excluded.updated_at;
