-- سجلٌّ صغير لمنع إرسال رسالة تذكير التجربة مرّتين لنفس المعلّمة، لو
-- استُدعيت الدالّة أكثر من مرّة (كما حدث فعلياً: النداء الأول انقطعت
-- متابعته بسبب عطلٍ في قراءة استجابة pg_net، فلا يجوز التأكّد بإعادة
-- النداء بلا ضمان عدم التكرار).
CREATE TABLE IF NOT EXISTS public.trial_reengagement_log (
  email      text PRIMARY KEY,
  status     text NOT NULL,        -- sent | failed
  reason     text,
  sent_at    timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.trial_reengagement_log ENABLE ROW LEVEL SECURITY;
-- لا سياسة لأحد: تُقرأ وتُكتب بمفتاح الخدمة من الدالّة نفسها فقط.

COMMENT ON TABLE public.trial_reengagement_log IS
  'سجلّ إرسال رسالة تذكير التجربة المجانية — يمنع إرسالاً مكرَّراً لنفس البريد عند إعادة استدعاء trial-reengagement-email.';
