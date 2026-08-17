-- ════════════════════════════════════════════════════════════════════
-- تحقّقٌ حيٌّ لمرحلة Phase 2 — بلا أي أثرٍ جانبي.
--
-- هذا الملف يتعمّد الفشل (RAISE EXCEPTION) لكي يُعيد سطر الخطأ نتيجة
-- الاستعلامات الحقيقية داخل جسم الرسالة، فتظهر في سجلّ GitHub Actions.
-- بما أن الاستثناء يُلغي المعاملة بالكامل (ROLLBACK تلقائي)، فلا تعديل
-- حقيقي يحدث على القاعدة — بما في ذلك محاولة إدخال action_id محظور،
-- التي يُفترض أن يرفضها قيد CHECK قبل أن تصل أصلاً إلى نقطة RAISE.
-- ════════════════════════════════════════════════════════════════════

DO $$
DECLARE
  v_tables text;
  v_rls text;
  v_seed text;
  v_check_test text;
BEGIN
  -- 1) وجود الجداول الخمسة بأعمدتها الأساسية
  SELECT string_agg(table_name || '(' || column_count || ' cols)', ', ' ORDER BY table_name)
  INTO v_tables
  FROM (
    SELECT table_name, count(*) AS column_count
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name IN ('ops_diagnoses','safe_action_registry','action_approvals','action_executions','internal_agent_requests')
    GROUP BY table_name
  ) t;

  -- 2) تفعيل RLS على الجداول الخمسة
  SELECT string_agg(relname || '=' || relrowsecurity, ', ' ORDER BY relname)
  INTO v_rls
  FROM pg_class
  WHERE relname IN ('ops_diagnoses','safe_action_registry','action_approvals','action_executions','internal_agent_requests')
    AND relnamespace = 'public'::regnamespace;

  -- 3) بيانات البذر الفعلية في سجلّ الإجراءات
  SELECT string_agg(
    action_id || '[risk=' || risk_level || ',approval=' || requires_human_approval || ',reversible=' || reversible || ']',
    ', ' ORDER BY action_id
  )
  INTO v_seed
  FROM public.safe_action_registry;

  -- 4) محاولة فعلية لإدخال action_id محظور — يجب أن يفشل بقيد CHECK
  BEGIN
    INSERT INTO public.safe_action_registry
      (action_id, name, description, category, risk_level, allowed_agents, required_permission,
       input_schema, output_schema, reversible, rollback_strategy, verification_strategy,
       requires_human_approval, enabled)
    VALUES
      ('execute_sql', 'محاولة اختبار', 'يجب أن تُرفض', 'NOTIFY_ONLY', 'CRITICAL', '["test"]'::jsonb, 'ADMIN_ACTION',
       '{}'::jsonb, '{}'::jsonb, false, 'n/a', 'n/a', true, false);
    v_check_test := 'FAIL — تم الإدخال رغم أنه محظور!';
  EXCEPTION WHEN check_violation THEN
    v_check_test := 'PASS — قيد CHECK رفض إدخال execute_sql فعلياً: ' || SQLERRM;
  END;

  RAISE EXCEPTION 'PHASE2_LIVE_EVIDENCE | TABLES: % | RLS: % | SEED: % | CHECK_TEST: %',
    coalesce(v_tables,'NONE'), coalesce(v_rls,'NONE'), coalesce(v_seed,'NONE'), v_check_test;
END $$;
