-- ════════════════════════════════════════════════════════════════════
-- P2 — فهارس لأعمدةٍ تُستعمَل في كل بحثٍ ولا فهرس لها.
--
-- كلُّ فهرس هنا مقابله موضعٌ حقيقي في الشيفرة يُصفّي أو يُرتّب على هذا
-- العمود بالضبط — لا فهرسة تخمينية. وكل أمرٍ محروسٌ بفحص وجود الجدول
-- والعمود أولاً (to_regclass / information_schema)، لأن بعض الجداول هنا
-- (profiles، private_messages) غير موجودةٍ في أي هجرةٍ متتبَّعة، فقد لا
-- تطابق أسماء أعمدتها ما هو مفترَض — والفشلُ الصامت هنا أسلم من فشل
-- الهجرة كاملةً على جدولٍ غير موجود.
-- ════════════════════════════════════════════════════════════════════

DO $$
BEGIN
  -- curriculum(grade,subject,semester) — يُصفَّى عليها في: manager.html
  -- (تحميل دروس الإدارة)، cycle1.html (c1Curriculum لكل معلّمة عند فتح
  -- الخطة/الاستوديو/تحضير الحصة) — أكثر الجداول قراءةً في المنصّة كلّها.
  IF to_regclass('public.curriculum') IS NOT NULL THEN
    CREATE INDEX IF NOT EXISTS idx_curriculum_gsse
      ON public.curriculum (grade, subject, semester);
  END IF;

  -- games(user_id, created_at) — gmLoadMyGames (الآن مرئيةٌ فعلاً بعد
  -- إصلاحٍ سابق) وlوحة الإدارة تُرتّبان عليه معاً.
  IF to_regclass('public.games') IS NOT NULL
     AND EXISTS (SELECT 1 FROM information_schema.columns
                  WHERE table_schema='public' AND table_name='games' AND column_name='user_id')
  THEN
    CREATE INDEX IF NOT EXISTS idx_games_user_created
      ON public.games (user_id, created_at DESC);
  END IF;

  -- library_files(grade, subject) — قائمة مكتبة المادة، تُفتح من كل
  -- معلّمة عند دخول قسم المكتبة.
  IF to_regclass('public.library_files') IS NOT NULL
     AND EXISTS (SELECT 1 FROM information_schema.columns
                  WHERE table_schema='public' AND table_name='library_files' AND column_name='grade')
  THEN
    CREATE INDEX IF NOT EXISTS idx_library_files_grade_subject
      ON public.library_files (grade, subject);
  END IF;

  -- violation_types(cycle) — تُقرأ عند فتح قسم «طلابي» لكل معلّمة.
  IF to_regclass('public.violation_types') IS NOT NULL
     AND EXISTS (SELECT 1 FROM information_schema.columns
                  WHERE table_schema='public' AND table_name='violation_types' AND column_name='cycle')
  THEN
    CREATE INDEX IF NOT EXISTS idx_violation_types_cycle
      ON public.violation_types (cycle);
  END IF;

  -- survey_responses(survey_id) — لوحة نتائج الاستبيانات في الإدارة.
  IF to_regclass('public.survey_responses') IS NOT NULL
     AND EXISTS (SELECT 1 FROM information_schema.columns
                  WHERE table_schema='public' AND table_name='survey_responses' AND column_name='survey_id')
  THEN
    CREATE INDEX IF NOT EXISTS idx_survey_responses_survey
      ON public.survey_responses (survey_id);
  END IF;

  -- profiles(updated_at) — قائمة «المستخدمون» في لوحة الإدارة تُرتّب
  -- عليه؛ الجدول موجودٌ فعلاً (يُقرأ منه في manager.html) لكن غير متتبَّع
  -- في الهجرات، فنتحقّق من العمود بدل افتراضه.
  IF to_regclass('public.profiles') IS NOT NULL
     AND EXISTS (SELECT 1 FROM information_schema.columns
                  WHERE table_schema='public' AND table_name='profiles' AND column_name='updated_at')
  THEN
    CREATE INDEX IF NOT EXISTS idx_profiles_updated_at
      ON public.profiles (updated_at DESC);
  END IF;

  -- private_messages(to_user_id) — الرسائل الخاصة من الإدارة.
  IF to_regclass('public.private_messages') IS NOT NULL
     AND EXISTS (SELECT 1 FROM information_schema.columns
                  WHERE table_schema='public' AND table_name='private_messages' AND column_name='to_user_id')
  THEN
    CREATE INDEX IF NOT EXISTS idx_private_messages_to_user
      ON public.private_messages (to_user_id);
  END IF;
END;
$$;
