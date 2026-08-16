-- عزلٌ حاسم: تعطيل RLS كلياً مؤقتاً لمعرفة هل السبب RLS أصلاً أم شيءٌ آخر.
-- سنُعيد تفعيله فوراً بعد الاختبار — هذه الخطوة لثوانٍ معدودة فقط.
ALTER TABLE public.pre_registrations DISABLE ROW LEVEL SECURITY;
