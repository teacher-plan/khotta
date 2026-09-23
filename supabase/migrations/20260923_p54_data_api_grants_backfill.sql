-- ════════════════════════════════════════════════════════════════════
-- P54 — تقنينُ صلاحيات الوصول عبر Data API (backfill).
--
-- الخلفية: من ٣٠ أكتوبر ٢٠٢٦ يتوقّف سوبابيس عن منح صلاحية Data API تلقائياً
-- للجداول الجديدة في public. الجداول الحيّة الحالية لا تتأثّر، لكنّ ملفات
-- الهجرة عندنا كانت تعتمد على المنح التلقائي، فلو أُعيد بناء القاعدة من الصفر
-- (مشروعٌ جديد، فرع معاينة preview، أو supabase db reset) لصارت أغلب الجداول
-- غير قابلةٍ للوصول عبر الـAPI. هذه الهجرة تُقنّن الصلاحيات الحالية كما هي
-- بالضبط (قُرئت من information_schema.role_table_grants على القاعدة الحيّة)
-- فتُعيد مجموعةُ الهجرات البناءَ نظيفةً على أي نسخة.
--
-- آمنةٌ على الإنتاج: المنح مُطابقٌ للموجود فعلاً (فلا أثر)، ومتخطٍّ لأي جدولٍ
-- غير موجود (to_regclass) فلا يفشل على نسخةٍ ناقصة. الجداول الداخلية
-- (سجلّات العمليات/الوكلاء/التدقيق) لا تُذكر هنا عمداً — تبقى بعيدةً عن
-- الـAPI كما هي الآن (خدمةٌ فقط).
-- ════════════════════════════════════════════════════════════════════

do $$
declare
  t text;
  -- جداولٌ تمنح anon وauthenticated الصلاحيات الكاملة (= GRANT ALL)، مضبوطةٌ
  -- بسياسات RLS. هذا هو الوضع الحيّ الحالي لكلٍّ منها.
  full_tables text[] := array[
    'ai_chats','ai_settings','allowed_emails','announcements','app_settings',
    'banned_users','book_sources','c1_community_messages','c1_golden_reuses',
    'c1_lesson_assets','c1_library_items','c1_library_ratings','c1_messages',
    'c1_notifications','c1_shared_assets','c1_suggestions','c1_survey_responses',
    'c1_surveys','curriculum','cycle1_profiles','drive_tokens','game_themes',
    'games','grade_templates','invites','lesson_prep_generations','lesson_preps',
    'lesson_texts','library_files','library_items','library_links','page_views',
    'pre_registrations','private_messages','profiles','push_subscriptions',
    'referrers','shared_prep_ratings','shared_preps','subjects','survey_responses',
    'surveys','teacher_guides','testimonials','trial_reengagement_log',
    'user_files','user_preps','user_storage_limits','violation_types','violations'
  ];
begin
  foreach t in array full_tables loop
    if to_regclass('public.'||quote_ident(t)) is not null then
      execute format('grant all on public.%I to anon, authenticated', t);
    end if;
  end loop;

  -- ── الحالات الخاصة (مطابقةٌ للوضع الحيّ لا GRANT ALL) ──
  -- ai_usage: قراءةٌ فقط للطرفين (بلا إدراج/تعديل/حذف).
  if to_regclass('public.ai_usage') is not null then
    execute 'grant references, select, trigger, truncate on public.ai_usage to anon, authenticated';
  end if;
  -- schools: authenticated بلا SELECT (القراءة للـanon فقط في الوضع الحالي).
  if to_regclass('public.schools') is not null then
    execute 'grant all on public.schools to anon';
    execute 'grant delete, insert, references, trigger, truncate, update on public.schools to authenticated';
  end if;
  -- usage_tracking: authenticated فقط، إدراجٌ وقراءة.
  if to_regclass('public.usage_tracking') is not null then
    execute 'grant insert, select on public.usage_tracking to authenticated';
  end if;
end $$;

-- تسلسلاتٌ (sequences): إدراجُ صفٍّ بمفتاحٍ تسلسليّ يحتاج USAGE على تسلسله.
-- المنح التلقائي كان يشملها؛ نُقنّنها ليعمل الإدراج على أي نسخةٍ معاد بناؤها.
grant usage, select on all sequences in schema public to anon, authenticated;
