# إعداد نظام مراقبة صحة النظام

## 🚨 ما الجديد؟

أضيفنا **وكيلين ذكيين حرجين**:

### 1️⃣ **System Health Check** 🔍
**التشغيل:** كل 5 دقائق
**الوظيفة:** يفحص صحة كل مكونات النظام ويرسل تنبيهات فورية عند المشاكل

يفحص:
- ✅ حالة جميع Edge Functions
- ✅ أداء قاعدة البيانات
- ✅ سرعة الاستجابة
- ✅ حجم التخزين
- ✅ سجلات الأخطاء الأخيرة
- ✅ الملفات العالقة

### 2️⃣ **File Processor Monitor** 📁
**التشغيل:** كل ساعة
**الوظيفة:** يراقب معالجة الملفات والملفات العالقة

يراقب:
- 📊 الملفات قيد المعالجة
- 🚨 الملفات العالقة (>2 ساعات)
- ✅ الملفات المكتملة
- ❌ الملفات المفشلة

---

## 🔧 خطوات الإعداد

### الخطوة 1: تطبيق المهاجرات الجديدة

```bash
supabase db push
```

هذا سينشئ الجداول:
- `health_checks` — سجل فحوصات الصحة
- `emergency_alerts` — التنبيهات الطارئة
- `file_processing_status` — حالة معالجة الملفات
- `error_logs` — سجل الأخطاء
- `performance_metrics` — مقاييس الأداء
- `service_status` — حالة الخدمات

### الخطوة 2: نشر الدوال الجديدة

```bash
supabase functions deploy system-health-check
supabase functions deploy file-processor-monitor
```

### الخطوة 3: جدولة المهام

```sql
-- فحص الصحة كل 5 دقائق
SELECT cron.schedule('system-health-5min', '*/5 * * * *', 
  'SELECT http_post(''https://YOUR_PROJECT.supabase.co/functions/v1/system-health-check'')');

-- مراقبة الملفات كل ساعة
SELECT cron.schedule('file-monitor-hourly', '0 * * * *', 
  'SELECT http_post(''https://YOUR_PROJECT.supabase.co/functions/v1/file-processor-monitor'')');
```

### الخطوة 4: اختبار

```bash
# اختبر الفحص الصحي
curl -X POST https://YOUR_PROJECT.supabase.co/functions/v1/system-health-check \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json"

# اختبر مراقب الملفات
curl -X POST https://YOUR_PROJECT.supabase.co/functions/v1/file-processor-monitor \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json"
```

---

## 📊 مثال على الرسائل

### الفحص الصحي (كل 5 دقائق)

إذا كل شيء بخير:
```
✅ النظام سليم
📊 جميع الدوال تعمل
✅ قاعدة البيانات سريعة (120ms)
✅ التخزين: 2.3GB / 5GB
🟢 لا توجد أخطاء
```

إذا حدثت مشكلة:
```
🚨 تنبيه حرج من نظام الصحة
━━━━━━━━━━━━━━━━━━━━━━
المشكلة: function:generate-lesson-plan
الخطورة: 4/5
الخطأ: HTTP 500
الإجراء: قم بفحص logs الدالة وأعد تشغيلها إذا لزم الأمر

⏰ الوقت: 2026-08-09 15:30:45
```

### مراقب الملفات (كل ساعة)

```
📁 ملخص معالجة الملفات
━━━━━━━━━━━━━━━━━━━━━━

⏳ قيد المعالجة: 3 ملفات
   🚨 عالقة (>2 ساعات):
      • thesis.pdf (125 دقيقة)
   ⏳ قيد المعالجة (طبيعي): 2 ملف

✅ اكتملت الساعة الأخيرة: 5 ملفات

━━━━━━━━━━━━━━━━━━━━━━

[📊 تفاصيل] [🚨 الملفات العالقة] [❌ إعادة محاولة]
```

---

## 🚨 التنبيهات الطارئة (Emergency Alerts)

التنبيهات الحرجة تُرسل **فوراً** بدل الانتظار للملخص اليومي:

### أنواع التنبيهات:
- 🔴 **Function Down** — دالة معطلة (HTTP 500)
- 🟠 **Database Slow** — قاعدة البيانات بطيئة (>2 ثانية)
- 🟡 **Storage Full** — التخزين ممتلئ (>90%)
- 🔴 **Stuck Files** — ملفات عالقة (>2 ساعات)
- 🟠 **High Error Rate** — معدل أخطاء عالي (>5 أخطاء/ساعة)

---

## 📈 عرض البيانات

### جميع فحوصات الصحة:
```sql
SELECT * FROM health_checks 
ORDER BY checked_at DESC 
LIMIT 50;
```

### التنبيهات الحرجة غير المحلولة:
```sql
SELECT * FROM emergency_alerts 
WHERE resolved = FALSE 
ORDER BY created_at DESC;
```

### حالة الملفات المعلقة:
```sql
SELECT * FROM file_processing_status 
WHERE status = 'processing' 
AND updated_at < NOW() - INTERVAL '2 hours'
ORDER BY updated_at DESC;
```

### سجل الأخطاء الأخيرة:
```sql
SELECT * FROM error_logs 
ORDER BY occurred_at DESC 
LIMIT 20;
```

---

## ⚙️ تعديل الحدود (Thresholds)

تعديل الحدود في `system-health-check/index.ts`:

```typescript
// تعديل timeout الدوال
signal: AbortSignal.timeout(5000), // من 5 ثانٍ إلى أقل

// تعديل حد سرعة قاعدة البيانات
if (duration > 2000) // من 2 ثانية إلى حد آخر

// تعديل حد التخزين
if (stats && stats.database_size_mb > 4500) // من 90% إلى نسبة أخرى

// تعديل عدد الأخطاء المقبول
if (criticalErrors > 5) // من 5 أخطاء إلى عدد آخر
```

---

## 📝 ملاحظات مهمة

1. **التنبيهات الطارئة تُرسل فوراً** — لا تنتظر الملخص اليومي
2. **السجلات محفوظة للتتبع** — يمكنك تحليل الأخطاء لاحقاً
3. **الأداء مراقب بشكل مستمر** — اكتشف البطء مبكراً
4. **الملفات العالقة تُكتشف آلياً** — يمكن حذفها أو إعادة معالجتها

---

## 🆘 عند حدوث مشكلة

### إذا دخلت تنبيهات كثيرة:
1. فتّش `health_checks` لمعرفة المشكلة
2. فتّش `error_logs` للتفاصيل
3. افحص `emergency_alerts` غير المحلولة

### إذا كانت ملفات عالقة:
```sql
-- حذف الملف العالق
DELETE FROM file_processing_status 
WHERE file_id = 'YOUR_FILE_ID';

-- أو تحديث حالته يدوياً
UPDATE file_processing_status 
SET status = 'failed', error_message = 'Manual cancellation'
WHERE file_id = 'YOUR_FILE_ID';
```

---

## الخطوة التالية

بعد تفعيل هذين الوكيلين، سنضيف:
- **User Engagement Monitor** — معرفة المعلمات المفقودات
- **Advanced Analytics Agent** — تحليل ذكي واقتراحات

---

## الأوامر السريعة

```bash
# شغّل الفحص الصحي يدوياً
curl -X POST https://YOUR_PROJECT.supabase.co/functions/v1/system-health-check \
  -H "Authorization: Bearer YOUR_KEY"

# شغّل مراقب الملفات يدوياً
curl -X POST https://YOUR_PROJECT.supabase.co/functions/v1/file-processor-monitor \
  -H "Authorization: Bearer YOUR_KEY"

# عرض آخر 10 فحوصات
SELECT * FROM health_checks ORDER BY checked_at DESC LIMIT 10;

# عرض جميع التنبيهات الحرجة غير المحلولة
SELECT * FROM emergency_alerts WHERE resolved = FALSE;
```
