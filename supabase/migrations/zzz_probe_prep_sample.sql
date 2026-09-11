-- فحصٌ للقراءة فقط: عيّنة من تحضيرٍ حقيقي مولَّد، لعرضه في فيديو الترويج
-- بدل محاكاةٍ مرسومة. يرفع استثناءً عمداً ليظهر الناتج في سجلّ التشغيل،
-- ولا يكتب شيئاً. يُحذف فور قراءة نتيجته.
DO $$
DECLARE
  v_n     int;
  v_meta  text;
  v_body  text;
BEGIN
  SELECT count(*) INTO v_n FROM public.lesson_prep_generations;

  SELECT g.grade || ' | ' || g.subject || ' | ' || g.unit || ' | ' || g.lesson
    INTO v_meta
    FROM public.lesson_prep_generations g
   ORDER BY g.created_at DESC
   LIMIT 1;

  -- أوّل ٢٠٠ حرفٍ من كل قسمٍ تكفي لعرضٍ أمين في الفيديو
  SELECT string_agg(kv.key || ' >>> ' || left(regexp_replace(kv.value::text, E'[\\n\\r]+', ' ', 'g'), 200),
                    E'\n---\n' ORDER BY kv.key)
    INTO v_body
    FROM (
      SELECT g.content FROM public.lesson_prep_generations g
       ORDER BY g.created_at DESC LIMIT 1
    ) t, jsonb_each(t.content) AS kv;

  RAISE EXCEPTION E'PREP_N=%\nPREP_META=%\nPREP_START\n%\nPREP_END',
        v_n, COALESCE(v_meta, '(لا تحاضير)'), COALESCE(v_body, '(لا محتوى)');
END $$;
