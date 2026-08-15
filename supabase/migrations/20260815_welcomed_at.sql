-- عمود تسجيل الترحيب: إرسال واتساب يقع خارج المنصّة فلا سبيل إلى معرفته
-- إلا بإقرار المشرف. وبدونه تظل القائمة تعرض الخمس أنفسهنّ أبداً.
ALTER TABLE pre_registrations
  ADD COLUMN IF NOT EXISTS welcomed_at TIMESTAMPTZ;

COMMENT ON COLUMN pre_registrations.welcomed_at IS
  'وقت إرسال رسالة الترحيب — NULL يعني أنها لم تُرحَّب بها بعد';

-- فهرسٌ جزئي على المنتظِرات وحدهنّ، كنظيره في notified_at
CREATE INDEX IF NOT EXISTS idx_pre_reg_unwelcomed
  ON pre_registrations (created_at)
  WHERE welcomed_at IS NULL;
