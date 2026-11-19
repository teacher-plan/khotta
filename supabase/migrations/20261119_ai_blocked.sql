-- ١٩ نوفمبر: حظر معلّمٍ بعينه من استهلاك رصيد الذكاء الاصطناعي (من صفحة الإدارة).
-- يقرؤه takeQuota في supabase/functions/_shared/quota.ts فيرفض كل نداءات التوليد.
-- الكتابة عبر سياسة allowed_admin_write القائمة (المدير فقط)؛ لا سياسة تحديث للمعلّم.
alter table public.allowed_emails add column if not exists ai_blocked boolean not null default false;
