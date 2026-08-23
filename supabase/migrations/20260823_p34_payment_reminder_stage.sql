-- تتبّع مرحلة تذكير الدفع لكل تسجيل: يميّز أي تذكيرٍ (الأول/الثاني/الثالث)
-- وصل للمعلّمة حتى الآن، فلا يُعاد إرسال نفس التذكير مرّتين، ويظهر لكل
-- معلّمة تذكيرها التالي فقط عبر أوامر /دفع، /دفع2، /دفع3 في بوت تلغرام.
ALTER TABLE pre_registrations
  ADD COLUMN IF NOT EXISTS payment_reminder_stage INTEGER NOT NULL DEFAULT 0;

COMMENT ON COLUMN pre_registrations.payment_reminder_stage IS
  '0 = لم يصلها أي تذكير بعد. 1/2/3 = وصلها التذكير الأول/الثاني/الثالث — يحدّد أيّ أمرٍ (/دفع، /دفع2، /دفع3) يعرضها تالياً.';

-- المرحلة التي كانت عليها المعلّمة لحظة تفعيل دفعها فعلياً — يعطي تقرير
-- إسنادٍ حقيقي: كم دفعت من التذكير الأول مقابل الثاني والثالث. NULL يعني
-- دفعت قبل وجود هذا النظام أو دون المرور بأي تذكير.
ALTER TABLE pre_registrations
  ADD COLUMN IF NOT EXISTS paid_at_reminder_stage INTEGER;

COMMENT ON COLUMN pre_registrations.paid_at_reminder_stage IS
  'قيمة payment_reminder_stage وقت تأكيد الدفع فعلياً — لتقرير أي تذكيرٍ حوّلها.';
