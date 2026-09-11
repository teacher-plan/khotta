-- فحصٌ للقراءة فقط: آراء المشتركات المنشورة، لاستعمالها في فيديو الترويج.
-- يرفع استثناءً عمداً ليظهر الناتج في سجلّ التشغيل، ولا يكتب شيئاً.
-- يُحذف فور قراءة نتيجته.
DO $$
DECLARE
  v_pub  text;
  v_all  int;
  v_on   int;
BEGIN
  SELECT count(*) INTO v_all FROM public.testimonials;
  SELECT count(*) INTO v_on  FROM public.testimonials WHERE is_published IS TRUE;

  SELECT string_agg(teacher_name || ' ||| ' || quote, E'\n~~~\n'
                    ORDER BY sort_order NULLS LAST, created_at DESC)
    INTO v_pub
    FROM public.testimonials
   WHERE is_published IS TRUE;

  RAISE EXCEPTION E'TST_COUNTS all=% published=%\nTST_START\n%\nTST_END',
        v_all, v_on, COALESCE(v_pub, '(لا آراء منشورة)');
END $$;
