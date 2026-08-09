# تطبيق نظام الوكلاء الذكيين ✅

## ما تم إنشاؤه

### 1. قاعدة البيانات 📊
**ملف:** `supabase/migrations/20260809_agents_system.sql`

جداول جديدة:
- `agent_schedules` — جدولة تشغيل الوكلاء
- `agent_messages` — سجل الرسائل المرسلة
- `agent_logs` — سجلات التنفيذ والأخطاء
- `user_analytics` — بيانات تحليلية لكل معلمة
- `user_surveys` — الاستبيانات والآراء
- `usage_tracking` — تتبع نشاط المستخدمين
- `analytics_insights` — الاقتراحات والتنبيهات الذكية

### 2. دوال Supabase Edge Functions 🚀

#### `_shared/telegram.ts`
دالة مساعدة مركزية لإرسال الرسائل:
```typescript
sendTelegram(message, { inline_keyboard: [...] })
editTelegram(messageId, message, options)
```

#### `daily-summary/index.ts`
**الوظيفة الرئيسية** — ملخص يومي واحد يحتوي على:
- 💰 ملخص الرصيد (أعداد الحالات الحرجة والتحذيرات)
- 📚 آخر المكتبة (عدد الملفات الجديدة)
- 📈 أوقات الذروة (أكثر ساعات النشاط)
- 📋 آراء المستخدمين (الاستبيانات الأسبوعية)
- 🤖 التحليلات الذكية (الاقتراحات)

مع **أزرار تفاعلية**:
```
[💰 رصيد] [📚 مكتبة] [📈 أوقات]
[📋 استبيان] [🤖 تحليل]
[⏰ إعادة جدولة] [🔄 تحديث الآن]
```

#### `credit-monitor/index.ts`
**وكيل مراقبة الرصيد** — يراقب استهلاك الذكاء الاصطناعي:
- تصنيف المعلمات: 🔴 حرجة (>80%) | 🟡 تحذير (50-80%) | 🟢 سليمة (<50%)
- يرسل تنبيهات فورية عند الوصول للحدود

#### `telegram-webhook/index.ts`
**استقبال التفاعلات** — يستقبل ضغطات الأزرار والرسائل:
- معالجة الأزرار التفاعلية
- حفظ آراء المستخدمين
- إعادة جدولة الوكلاء

### 3. التكوين والإعدادات 🔧
**ملف:** `AGENTS_SETUP.md`

خطوات الإعداد:
1. حفظ Telegram Token و Chat ID في Supabase Secrets
2. تشغيل ملف المهاجرة (Migration)
3. نشر الدوال (Deploy)
4. جدولة المهام (Cron)
5. اختبار يدوي

---

## البنية المعمارية

```
Telegram User
    ↓
[Khotah_agent_bot] 🤖
    ↓
Telegram API
    ↓
┌─────────────────────────────────┐
│   Supabase Edge Functions       │
├─────────────────────────────────┤
│                                 │
│  daily-summary (الملخص المركزي)  │
│  ├─ credit-monitor              │
│  ├─ library-monitor (قريباً)     │
│  ├─ peak-hours-monitor (قريباً)  │
│  ├─ feedback-collector (قريباً)  │
│  └─ analytics-agent (قريباً)     │
│                                 │
│  telegram-webhook (استقبال)     │
│  ↓                              │
│  معالجات الأزرار والأوامر      │
│                                 │
└─────────────────────────────────┘
    ↓
┌──────────────────────────────┐
│   Supabase Database          │
├──────────────────────────────┤
│ agent_schedules              │
│ agent_messages               │
│ agent_logs                   │
│ user_analytics               │
│ user_surveys                 │
│ usage_tracking               │
│ analytics_insights           │
└──────────────────────────────┘
```

---

## الجدولة الزمنية

تشغيل تلقائي **يومياً الساعة 5:00 مساءً (17:00)**:

```sql
SELECT cron.schedule('daily-summary-5pm', '0 17 * * *', 
  'SELECT http_post(''https://your-project.supabase.co/functions/v1/daily-summary'')');
```

يمكن تغيير الوقت من جدول `agent_schedules`:
```sql
UPDATE agent_schedules 
SET scheduled_hour = 18  -- الساعة 6 مساءً
WHERE agent_name = 'daily-summary';
```

---

## الخطوات التالية 🎯

### الأسبوع الأول:
1. ✅ إعداد Telegram و Supabase Secrets
2. ✅ نشر daily-summary و credit-monitor
3. ✅ تفعيل الجدولة
4. **اختبار يدوي لمدة يوم**

### الأسبوع الثاني:
5. إضافة **library-monitor** — مراقبة الملفات الجديدة
6. إضافة **peak-hours-monitor** — تحليل أوقات الذروة
7. إضافة معالجات أزرار مفصلة

### الأسبوع الثالث:
8. إضافة **feedback-collector** — استبيانات دورية
9. إضافة **analytics-agent** — تحليل ذكي واقتراحات
10. تحسين الواجهة والأزرار

---

## ملاحظات مهمة ⚠️

1. **البيانات السرية** محفوظة في Supabase Secrets فقط
2. **لا تضع التوكن** في الكود أو في مستودع Git
3. كل وكيل **مستقل** ويمكن إيقافه بـ `enabled = FALSE`
4. السجلات **محفوظة في قاعدة البيانات** للتتبع والتدقيق
5. الرسائل **قابلة للتحديث** عبر `editTelegram()`

---

## الأوامر السريعة

```bash
# عرض السجلات
SELECT * FROM agent_logs ORDER BY created_at DESC LIMIT 10;

# عرض الرسائل المرسلة
SELECT * FROM agent_messages ORDER BY sent_at DESC LIMIT 5;

# تعطيل وكيل مؤقتاً
UPDATE agent_schedules SET enabled = FALSE WHERE agent_name = 'credit-monitor';

# تفعيل الوكيل مرة أخرى
UPDATE agent_schedules SET enabled = TRUE WHERE agent_name = 'credit-monitor';

# تشغيل يدوي فوري
SELECT http_post('https://YOUR_PROJECT.supabase.co/functions/v1/daily-summary');
```

---

## المساعدة والمشاكل

- **الرسالة لم تصل:** تحقق من `TELEGRAM_BOT_TOKEN` و `TELEGRAM_CHAT_ID` في Secrets
- **خطأ في الدالة:** تفحص `agent_logs` للتفاصيل
- **الجدولة لم تعمل:** تأكد من تفعيل `pg_cron` extension
- **أزرار لا تعمل:** تحقق من `telegram-webhook` logs

---

## التطوير المستقبلي

- [ ] Dashboard مرئي لتتبع البيانات
- [ ] رسائل صوتية من Telegram
- [ ] تصدير التقارير PDF
- [ ] إشعارات عبر البريد الإلكتروني أيضاً
- [ ] تنبيهات فورية (real-time) للحالات الحرجة
