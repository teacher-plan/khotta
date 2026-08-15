-- عمود متابعة الدفع لأمر /payment في بوت تلجرام — يشبه welcomed_at لكنّه
-- لا يُخفي المعلّمة نهائياً بعد التسجيل، بل يُنقلها لآخر طابور المتابعة.
ALTER TABLE pre_registrations
  ADD COLUMN IF NOT EXISTS payment_followup_at TIMESTAMPTZ;

COMMENT ON COLUMN pre_registrations.payment_followup_at IS
  'وقت آخر متابعةٍ للدفع عبر أمر /payment — NULL يعني لم تُتابَع قطّ';
