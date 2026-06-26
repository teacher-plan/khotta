# إعداد ربط Google Drive للتخزين (خطوات لوحة التحكم)

الكود جاهز في المستودع، لكن الميزة لا تعمل حتى تكمل الخطوات التالية من
لوحاتك (Supabase + Google Cloud). نفّذها بالترتيب.

## 1) قاعدة البيانات
- افتح Supabase → SQL Editor، والصق محتوى `supabase_drive_tokens_migration.sql` ثم Run.
- النتيجة: جدول `drive_tokens` مع سياسات RLS.

## 2) تفعيل الربط اليدوي للهويات (مهم)
- Supabase → Authentication → Sign In / Providers → بالأسفل قسم **"Allow manual linking"** → فعّله (On) → Save.
- بدونه ستفشل عملية `linkIdentity` التي يستخدمها زر الربط.

## 3) Google Cloud Console (نفس مشروع OAuth الحالي)
- تأكد أن **Authorized redirect URIs** لعميل OAuth تتضمن رابط Supabase:
  `https://mkdsnnfkkdwdkywnwnjh.supabase.co/auth/v1/callback`
- في **OAuth consent screen** تأكد أن النطاق (scope) `.../auth/drive.file` مضاف.
- انسخ **Client ID** و **Client Secret** (ستحتاجهما في الخطوة 5).

## 4) نشر الـ Edge Function
- ثبّت Supabase CLI ثم من جذر المشروع:
  - `supabase login`
  - `supabase link --project-ref mkdsnnfkkdwdkywnwnjh`
  - `supabase functions deploy drive-token`
- (الملف موجود في `supabase/functions/drive-token/index.ts`)

## 5) أسرار الـ Edge Function
- Supabase → Edge Functions → drive-token → Secrets (أو عبر CLI):
  - `GOOGLE_CLIENT_ID`     = معرّف العميل من الخطوة 3
  - `GOOGLE_CLIENT_SECRET` = السر من الخطوة 3
- (المتغيّران `SUPABASE_URL` و `SUPABASE_SERVICE_ROLE_KEY` متوفّران تلقائياً.)
- ⚠️ لا تضع `GOOGLE_CLIENT_SECRET` في أي ملف داخل المستودع — فقط في أسرار Supabase.

## 6) التجربة من طرف المعلم
- معلم بحساب بريد/كلمة مرور → افتح أي قسم فيه رفع ملف (درس / أرشيف / سيرة ذاتية) → اضغط رفع.
- ستظهر رسالة "اربط حساب Google الآن؟" → موافقة → نافذة جوجل (تظهر مرة واحدة) → عُد للموقع.
- أعد محاولة الرفع → يجب أن ينجح. وفي اليوم التالي (جلسة جديدة) يجب أن يستمر العمل
  تلقائياً عبر تجديد التوكن من الخادم بدون إعادة ربط.

## ملاحظات
- مستخدمو تسجيل الدخول بجوجل الحاليون: لا يتأثرون — يعملون كما هم، ويُحفظ لهم
  refresh_token تلقائياً ليستفيدوا أيضاً من التجديد بعد انتهاء الساعة الأولى.
- ملفات Drive القديمة تبقى قابلة للعرض (روابطها عامة) دون أي ترحيل.
- تحذير "التطبيق غير موثّق" من جوجل سيظهر **مرة واحدة فقط** عند الربط بدل كل دخول.
  لإزالته نهائياً تحتاج لإكمال توثيق التطبيق لدى Google (عملية منفصلة).
