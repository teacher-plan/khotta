-- تشخيص: لماذا لم تصل رسالة تلغرام؟ — نفّذي الاستعلامات الأربعة معاً

-- ١) ردّ الوكيل على نداء المُشغِّل  ← أهمّ سطر
SELECT id, status_code AS "الرمز", left(content, 300) AS "المحتوى",
       error_msg AS "خطأ الشبكة", created
FROM net._http_response ORDER BY id DESC LIMIT 3;

-- ٢) هل عُلِّم الحجز التجريبي مُرسَلاً؟
SELECT name, stage, notified_at, created_at
FROM pre_registrations
WHERE email = 'khotta.test.delete@gmail.com';

-- ٣) ماذا سجّل الوكيل عن نفسه؟ (يظهر فقط إن تجاوز الحارس)
SELECT action, status, error_message, data_collected, created_at
FROM agent_logs WHERE agent_name = 'registration-notifier'
ORDER BY created_at DESC LIMIT 5;

-- ٤) أي صيغةِ مفتاحٍ في الخزانة؟ (يُظهر البادئة والطول فقط، لا المفتاح)
SELECT left(decrypted_secret, 7) AS "البادئة",
       length(decrypted_secret)  AS "الطول",
       CASE WHEN decrypted_secret LIKE 'eyJ%' THEN '✅ الصيغة الصحيحة (JWT)'
            ELSE '❌ صيغة خاطئة — يلزم مفتاح eyJhbGci…' END AS "الحكم"
FROM vault.decrypted_secrets WHERE name = 'service_role_key';
