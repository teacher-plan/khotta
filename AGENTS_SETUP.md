# إعداد نظام الوكلاء الذكيين

## ١. حفظ البيانات السرية في Supabase

اذهب إلى لوحة تحكم Supabase → Settings → Secrets

أضف السريات التالية:

```
TELEGRAM_BOT_TOKEN = 8699789334:AAFxJ0o9YmUOpFBDEvkq00BwYz-bYlBHeEw
TELEGRAM_CHAT_ID = 863476544
```

## ٢. تطبيق ملف المهاجرة (Migration)

قم بتشغيل ملف المهاجرة:

```bash
supabase db push
```

هذا سينشئ الجداول:
- `agent_schedules` — جدولة الوكلاء
- `agent_messages` — سجل الرسائل
- `agent_logs` — سجلات التنفيذ
- `user_analytics` — بيانات تحليلية
- `user_surveys` — الاستبيانات
- `usage_tracking` — تتبع الاستخدام
- `analytics_insights` — الاقتراحات الذكية

## ٣. نشر الدوال

نشر الدوال الجديدة:

```bash
supabase functions deploy daily-summary
supabase functions deploy credit-monitor
supabase functions deploy telegram-webhook
```

بعد نشر `telegram-webhook`، اربطيه بالبوت (مرة واحدة فقط):
```bash
curl -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook" \
  -d "url=https://YOUR_PROJECT_ID.supabase.co/functions/v1/telegram-webhook"
```

## ٤. جدولة المهام (Cron)

قم بتشغيل هذا SQL في SQL Editor بلوحة Supabase (يتطلب تفعيل `pg_cron` و`pg_net` من Database → Extensions):

```sql
CREATE EXTENSION IF NOT EXISTS pg_cron;
CREATE EXTENSION IF NOT EXISTS pg_net;

-- جدولة الملخص اليومي الساعة 5 مساءً (17:00 بتوقيت UTC — عدّلي حسب فرق التوقيت)
SELECT cron.schedule('daily-summary-5pm', '0 17 * * *',
  $$SELECT net.http_post(
      url:='https://YOUR_PROJECT_ID.supabase.co/functions/v1/daily-summary',
      headers:='{"Authorization":"Bearer YOUR_ANON_KEY","Content-Type":"application/json"}'::jsonb
    )$$);
```

⚠️ ملاحظة: جدولة `pg_cron` تعمل بتوقيت UTC وليس توقيت الرياض. الساعة 5 مساءً بتوقيت الرياض (UTC+3) تعني `0 14 * * *` في تعبير cron.

## ٥. اختبار يدوي

لاختبار الوكيل يدوياً:

```bash
# شغّل daily-summary
curl -X POST https://YOUR_PROJECT_ID.supabase.co/functions/v1/daily-summary \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json"
```

## ٦. الأزرار التفاعلية

الوكلاء ترسل رسائل مع أزرار تفاعلية:
- `💰 رصيد` → تقرير مفصل عن استهلاك الرصيد
- `📚 مكتبة` → الملفات المرفوعة الجديدة
- `📈 أوقات` → تحليل أوقات الذروة
- `📋 استبيان` → إرسال استبيان جديد
- `🤖 تحليل` → الاقتراحات الذكية
- `⏰ إعادة جدولة` → تغيير وقت الملخص

## الخطوات التالية

بعد الإعداد الأساسي:

1. **وكيل مراقبة المكتبة** — يراقب الملفات المرفوعة
2. **وكيل أوقات الذروة** — يحلل أوقات الاستخدام
3. **وكيل جمع الآراء** — يرسل استبيانات دورية
4. **وكيل التحليل الذكي** — يجمع البيانات ويولد اقتراحات

## الملاحظات

- البيانات السرية محفوظة في Supabase Secrets فقط
- السجلات محفوظة في جداول قاعدة البيانات
- يمكن تعديل أوقات الجدولة من جدول `agent_schedules`
- كل وكيل مستقل ويمكن إيقافه بسهولة (عمود `enabled`)
