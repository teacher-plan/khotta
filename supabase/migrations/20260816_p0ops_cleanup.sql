-- تنظيف بيانات الاختبار الحيّ لتسجيل التكلفة (Phase 0) — حساب الاختبار
-- ومدخلاته في ai_cost_log وai_usage. لا صفوف حقيقية لمعلماتٍ فعليات تُمسّ.
DELETE FROM public.ai_cost_log WHERE user_id = '1618acc4-1b30-4c5c-b8d1-e581bf1ca479';
DELETE FROM public.ai_usage    WHERE user_id = '1618acc4-1b30-4c5c-b8d1-e581bf1ca479';
DELETE FROM auth.users         WHERE email = 'khotta.audit.test+phase0@gmail.com';
