-- جدولٌ للاختبار وحده: هل الآلية نفسها (anon → RLS INSERT) تعمل على
-- القاعدة إطلاقاً، أم أن العطل خاصٌّ بجدول pre_registrations تحديداً؟
-- يُحذف فور انتهاء التشخيص.
CREATE TABLE IF NOT EXISTS public._audit_sanity (id serial primary key, note text);
ALTER TABLE public._audit_sanity ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS sanity_insert ON public._audit_sanity;
CREATE POLICY sanity_insert ON public._audit_sanity FOR INSERT TO anon WITH CHECK (true);
GRANT INSERT ON public._audit_sanity TO anon;
GRANT USAGE ON SEQUENCE public._audit_sanity_id_seq TO anon;
