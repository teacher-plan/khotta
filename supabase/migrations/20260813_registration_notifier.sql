-- وكيل تنبيه التسجيلات — الحلقة الأولى
-- يرسل رسالة تلغرام فور حجز معلّمة مقعدها في صفحة الترويج.

-- ═ علامة الإرسال ═
-- بدونها يعتمد الوكيل على الوقت في تمييز الجديد، والوقت خؤون: إعادة تشغيلٍ
-- واحدة تُعيد إرسال ما أُرسل، وتعطُّلٌ عابر يُسقط تسجيلاً بلا أن يُلحظ.
-- بعمودٍ صريح يصير السؤال «هل أُرسل؟» لا «متى كان آخر تشغيل؟».
ALTER TABLE pre_registrations
  ADD COLUMN IF NOT EXISTS notified_at TIMESTAMPTZ;

-- فهرسٌ جزئي على المنتظِرات وحدها: الصفوف المُرسَلة تخرج من الفهرس فلا ينمو
-- بنمو الجدول، ويبقى مسح المتأخّرات فورياً مهما بلغ عدد التسجيلات.
CREATE INDEX IF NOT EXISTS idx_pre_reg_unnotified
  ON pre_registrations (created_at)
  WHERE notified_at IS NULL;

-- ═ التسجيلات السابقة ═
-- ما سُجّل قبل اليوم لا يُعدّ جديداً: تركُه بلا علامة يُطلق عند أول تشغيل
-- سيلاً من رسائل عن حجوزاتٍ قديمة. نَعُدّها مُبلَّغاً عنها من الآن.
UPDATE pre_registrations
   SET notified_at = NOW()
 WHERE notified_at IS NULL;

-- ═ تسجيل الوكيل ═
-- الساعة صفر لأنه لا يعمل بموعد: يُستدعى فور الحجز عبر خطّاف قاعدة البيانات،
-- والجدولة هنا لمسحٍ احتياطيّ يلتقط ما فات الخطّاف.
INSERT INTO agent_schedules (agent_name, scheduled_hour, scheduled_minute, description)
VALUES ('registration-notifier', 0, 0,
        'تنبيه فوري عند حجز مقعد في صفحة الحلقة الأولى — ومسح احتياطيّ لما يفوت الخطّاف')
ON CONFLICT (agent_name) DO NOTHING;

COMMENT ON COLUMN pre_registrations.notified_at IS
  'وقت إرسال تنبيه تلغرام عن هذا الحجز — NULL يعني أنه لم يُبلَّغ عنه بعد';
