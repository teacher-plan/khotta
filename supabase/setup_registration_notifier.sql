-- ════════════════════════════════════════════════════════════════════
--  تفعيل وكيل تنبيه التسجيلات — الحلقة الأولى
--  يُنفَّذ مرّة واحدة من: لوحة Supabase ← SQL Editor
--
--  قبل التنفيذ: استبدلي «ضعي_مفتاح_الخدمة_هنا» في الجزء ٢ بمفتاح الخدمة
--  (Settings ← API ← service_role). لا تحفظي هذا الملف بالمفتاح داخله.
--
--  السكربت آمن التكرار: تنفيذه مرّتين لا يُحدث ضرراً ولا يُكرّر شيئاً.
-- ════════════════════════════════════════════════════════════════════


-- ═══ الجزء ١: علامة الإرسال ═══════════════════════════════════════
-- بدونها يعتمد الوكيل على الوقت في تمييز الجديد، والوقت خؤون: إعادة
-- تشغيلٍ واحدة تُعيد إرسال ما أُرسل، وتعطُّلٌ عابر يُسقط تسجيلاً بلا أن
-- يُلحظ. بعمودٍ صريح يصير السؤال «هل أُرسل؟» لا «متى كان آخر تشغيل؟».

ALTER TABLE pre_registrations
  ADD COLUMN IF NOT EXISTS notified_at TIMESTAMPTZ;

-- فهرسٌ جزئي على المنتظِرات وحدها: الصفوف المُرسَلة تخرج منه فلا ينمو
-- بنمو الجدول، ويبقى مسح المتأخّرات فورياً مهما بلغ عدد التسجيلات.
CREATE INDEX IF NOT EXISTS idx_pre_reg_unnotified
  ON pre_registrations (created_at)
  WHERE notified_at IS NULL;

-- ما سُجّل قبل اليوم ليس جديداً: تركُه بلا علامة يُطلق عند أول تشغيل
-- سيلاً من رسائل عن حجوزاتٍ قديمة. نَعُدّها مُبلَّغاً عنها من الآن.
UPDATE pre_registrations SET notified_at = NOW() WHERE notified_at IS NULL;

-- تسجيل الوكيل في جدول الوكلاء
INSERT INTO agent_schedules (agent_name, scheduled_hour, scheduled_minute, description)
VALUES ('registration-notifier', 0, 0,
        'تنبيه فوري عند حجز مقعد في صفحة الحلقة الأولى — ومسح احتياطيّ لما يفوت الخطّاف')
ON CONFLICT (agent_name) DO NOTHING;


-- ═══ الجزء ٢: إيداع مفتاح الخدمة في الخزانة ═══════════════════════
-- لوحة Supabase حين تُنشئ خطّافاً تدفن المفتاح نصّاً صريحاً داخل تعريف
-- المُشغِّل، فيظهر لكل من يقرأ بنية الجدول. الخزانة تحفظه مُعمّى ويُقرأ
-- عند النداء وحده — فلا يظهر في تعريفٍ ولا يدخل المستودع.

CREATE EXTENSION IF NOT EXISTS supabase_vault WITH SCHEMA vault;

DO $$
DECLARE
  v_key TEXT := 'ضعي_مفتاح_الخدمة_هنا';   -- ← استبدليه، ثم لا تحفظي الملف
BEGIN
  IF v_key = 'ضعي_' || 'مفتاح_الخدمة_هنا' THEN
    RAISE EXCEPTION 'لم يُستبدل مفتاح الخدمة في الجزء ٢ — استبدليه ثم أعيدي التنفيذ';
  END IF;

  -- تحديث الموجود بدل تكراره، ليبقى السكربت آمن التكرار.
  IF EXISTS (SELECT 1 FROM vault.secrets WHERE name = 'service_role_key') THEN
    PERFORM vault.update_secret(
      (SELECT id FROM vault.secrets WHERE name = 'service_role_key'),
      v_key, 'service_role_key', 'مفتاح الخدمة — تستعمله مُشغِّلات قاعدة البيانات');
  ELSE
    PERFORM vault.create_secret(
      v_key, 'service_role_key', 'مفتاح الخدمة — تستعمله مُشغِّلات قاعدة البيانات');
  END IF;
END $$;


-- ═══ الجزء ٣: المُشغِّل الفوري ════════════════════════════════════
-- pg_net يرسل الطلب لا متزامنٍ: يُودِعه طابوراً ويعود فوراً. وهذا مقصود —
-- تسجيل المعلّمة يجب ألّا ينتظر تلغرام. لو كان النداء متزامناً لصار بطء
-- تلغرام بطءاً في صفحة الحجز نفسها.

CREATE EXTENSION IF NOT EXISTS pg_net WITH SCHEMA extensions;

CREATE OR REPLACE FUNCTION notify_new_registration()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER               -- ليقرأ الخزانة، والقارئ العادي لا يملك ذلك
SET search_path = public, extensions, vault
AS $$
DECLARE
  v_key TEXT;
BEGIN
  SELECT decrypted_secret INTO v_key
    FROM vault.decrypted_secrets WHERE name = 'service_role_key';

  IF v_key IS NULL THEN
    RAISE WARNING 'notify_new_registration: مفتاح الخدمة غير موجود في الخزانة';
    RETURN NEW;
  END IF;

  PERFORM net.http_post(
    url     := 'https://mkdsnnfkkdwdkywnwnjh.supabase.co/functions/v1/registration-notifier',
    headers := jsonb_build_object(
                 'Content-Type',  'application/json',
                 'Authorization', 'Bearer ' || v_key),
    body    := jsonb_build_object('record', jsonb_build_object('id', NEW.id)),
    timeout_milliseconds := 5000
  );

  RETURN NEW;
EXCEPTION WHEN OTHERS THEN
  -- ⚠️ الأهمّ في هذا الملف: تنبيهٌ فاشل لا يجوز أن يُسقط حجزاً.
  -- بلا هذا الحاجز، عطلٌ في pg_net أو الخزانة يُفشل الـINSERT نفسه،
  -- فترى المعلّمة «تعذّر التسجيل» ويضيع الحجز. الحجز أثمن من التنبيه —
  -- والمسح الاحتياطيّ في الوكيل يلتقط ما فات على أي حال.
  RAISE WARNING 'notify_new_registration فشل: %', SQLERRM;
  RETURN NEW;
END $$;

DROP TRIGGER IF EXISTS trg_notify_new_registration ON pre_registrations;

CREATE TRIGGER trg_notify_new_registration
  AFTER INSERT ON pre_registrations
  FOR EACH ROW
  WHEN (NEW.stage = 'cycle1')     -- الحلقة الأولى وحدها
  EXECUTE FUNCTION notify_new_registration();


-- ═══ التحقق ══════════════════════════════════════════════════════
SELECT
  (SELECT count(*) FROM information_schema.columns
     WHERE table_name='pre_registrations' AND column_name='notified_at')  AS "عمود notified_at",
  (SELECT count(*) FROM vault.secrets WHERE name='service_role_key')      AS "المفتاح في الخزانة",
  (SELECT count(*) FROM pg_trigger WHERE tgname='trg_notify_new_registration') AS "المُشغِّل",
  (SELECT count(*) FROM pg_extension WHERE extname='pg_net')              AS "pg_net";
-- المطلوب: ١ في كل خانة.
