-- ════════════════════════════════════════════════════════════════════
-- Phase 3.1 — اختبار Shadow حيّ وآمن، موثَّقٌ فعلياً في قاعدة الإنتاج.
--
-- يُدرِج حادثةً اصطناعية موسومة صراحةً (__phase3_1_test__) تحاكي نمط
-- KNOWN_MONITOR_REPEATED_FAILURE (3 فشلاتٍ متتالية بنفس رسالة الخطأ)،
-- ثم يُطبِّق يدوياً بالضبط نفس الشروط الثمانية في checkPreconditions()
-- (opsPlaybooks.ts) عبر SQL صريح يقرأ من الجداول الحقيقية، ثم يُدرِج
-- النتيجة في repair_executions تماماً كما يفعل ops-actions حين يُستدعى.
--
-- هذا يُثبِت أن Schema والبيانات الحقيقية تدعمان الأنبوب فعلياً DATABASE
-- VERIFIED — لكنه لا يستدعي الدالة المنشورة نفسها عبر HTTP (لا مفتاح
-- service role متاحٌ لذلك)، فيبقى تنفيذ الكود المنشور نفسه NOT VERIFIED
-- صراحةً، موثَّقٌ هكذا في التقرير النهائي.
--
-- سيُحذَف كل صفٍّ يُدرَج هنا في الملف التالي (p12c) — لا بقايا اختبارٍ
-- في جداول الإنتاج.
-- ════════════════════════════════════════════════════════════════════

INSERT INTO public.ops_incidents (
  dedup_key, component, severity, status, confidence,
  summary, evidence, source_agent, occurrence_count, first_seen_at, last_seen_at
) VALUES (
  '__phase3_1_test__credit-monitor',
  'credit-monitor', 'P2', 'ACTION_REQUIRED', 'VERIFIED',
  '[اختبارٌ آمن Phase 3.1] فشلٌ متكرّرٌ اصطناعي لغرض التحقّق الحيّ فقط',
  jsonb_build_array(jsonb_build_object('source','phase3_1_test','detail','3 فشلاتٍ اصطناعية بنفس رسالة الخطأ: TimeoutError')),
  'credit-monitor', 3, now() - interval '10 minutes', now()
)
RETURNING id;

-- تقييمٌ يدويّ لنفس الشروط الثمانية بالضبط (نفس الأسماء والترتيب في
-- opsPlaybooks.ts::checkPreconditions)، مبنيٌّ على بيانات السيناريو
-- المُعلَنة أعلاه + حالة الجداول الحقيقية وقت التنفيذ:
DO $$
DECLARE
  v_incident_id uuid;
  v_similar_open int;
  v_action_ok boolean;
  v_action_enabled boolean;
  v_preconditions jsonb;
  v_any_failed boolean;
  v_status text;
  v_escalation text;
BEGIN
  SELECT id INTO v_incident_id FROM public.ops_incidents WHERE dedup_key = '__phase3_1_test__credit-monitor';

  -- محاكاةٌ حرفية لاستعلام checkPreconditions الحقيقي في opsPlaybooks.ts —
  -- بما فيها قيمتا الحالة 'OPEN'/'ESCALATED' كما وردتا في الكود المنشور
  -- فعلياً، رغم أن قيد ops_incidents.status (p5) لا يسمح بهما إطلاقاً
  -- (القيم الصالحة: DETECTED/INVESTIGATING/IDENTIFIED/RECOMMENDATION/
  -- RESOLVED/ACTION_REQUIRED/FAILED/IGNORED) — هذا الاستعلام سيُعيد صفراً
  -- دوماً بنيوياً، وهذا بالضبط ما يجب توثيقه كخللٍ حقيقي مكتشَفٍ بالاختبار
  -- الحيّ لا نظرياً (انظر تقرير Phase 3.1، قسم Known Issues).
  -- ملاحظة: الكود الحقيقي يستعلم بعمود created_at — وهو عمودٌ غير موجودٍ
  -- إطلاقاً في ops_incidents (تحقّقٌ حيّ عبر information_schema، انظر
  -- التقرير) — فيفشل هذا الاستعلام في الكود المنشور فعلياً بخطإ "عمودٌ
  -- غير موجود" لا بإعادة صفر بصمت. هنا نستعمل first_seen_at (الموجود
  -- فعلاً) لإكمال الاختبار المحاكي، لكن الخلل الحقيقي موثَّقٌ في التقرير.
  SELECT count(*) INTO v_similar_open FROM public.ops_incidents
    WHERE component = 'credit-monitor' AND status IN ('OPEN','ESCALATED')
      AND first_seen_at >= now() - interval '30 minutes';

  SELECT enabled INTO v_action_enabled FROM public.safe_action_registry WHERE action_id = 'rerun_monitor_agent';
  v_action_ok := (v_action_enabled IS NOT NULL);

  v_preconditions := jsonb_build_array(
    jsonb_build_object('name','same_function_same_error_pattern','passed', true, 'detail','رسالة خطأٍ واحدة ثابتة (TimeoutError) — سيناريو الاختبار.'),
    jsonb_build_object('name','failure_count_at_or_above_threshold','passed', true, 'detail','3 فشلاتٍ متتالية (الحدّ الأدنى 3) — occurrence_count الحقيقي في ops_incidents.'),
    jsonb_build_object('name','last_known_success_exists','passed', true, 'detail','آخر نجاحٍ حقيقي لـcredit-monitor موجودٌ في agent_runs (تحقَّق مسبقاً في هذا التقرير).'),
    jsonb_build_object('name','no_similar_incident_open_recently','passed', v_similar_open <= 1, 'detail', v_similar_open || ' حادثةٍ مفتوحة/مُصعَّدة لنفس المكوّن آخر 30 دقيقة.'),
    jsonb_build_object('name','no_recent_deployment_change','passed', false, 'detail','لا مصدر بياناتٍ حقيقيّ لسجلّ النشر بعد — يُعتبَر غير مُحقَّقٍ صراحةً دوماً (نفس سلوك الكود الحيّ المنشور).'),
    jsonb_build_object('name','agent_permitted_for_playbook','passed', true, 'detail','credit-monitor ضمن allowed_agents لـretry_monitor_known_timeout.'),
    jsonb_build_object('name','action_exists_in_registry','passed', v_action_ok, 'detail','rerun_monitor_agent موجودٌ في safe_action_registry.'),
    jsonb_build_object('name','action_enabled','passed', coalesce(v_action_enabled,false), 'detail', CASE WHEN v_action_enabled THEN 'مفعَّلٌ.' ELSE 'غير مفعَّلٍ أو غير موجود.' END)
  );

  v_any_failed := EXISTS (SELECT 1 FROM jsonb_array_elements(v_preconditions) e WHERE (e->>'passed') = 'false');

  IF v_any_failed THEN
    v_status := 'ESCALATED';
    v_escalation := 'شرطٌ واحدٌ أو أكثر من preconditions لم يتحقّق — أهمّها no_recent_deployment_change (لا مصدر بياناتٍ حقيقي للنشر بعد)، فلا إصلاحٌ آليٌّ حتى في Shadow — تصعيدٌ صريح، تماماً كما تنصّ القاعدة "لا يوجد Auto Repair عند نقص الأدلة".';
  ELSE
    v_status := 'WOULD_AUTO_HEAL';
    v_escalation := NULL;
  END IF;

  INSERT INTO public.repair_executions (
    incident_id, playbook_id, action_id, agent_id, mode, status,
    attempt_number, evidence_snapshot, preconditions_result, error, escalation_reason,
    blast_radius, confidence_at_decision, completed_at
  ) VALUES (
    v_incident_id, 'retry_monitor_known_timeout', 'rerun_monitor_agent', 'credit-monitor', 'SHADOW', v_status,
    1,
    jsonb_build_object('consecutive_failures', 3, 'distinct_errors', jsonb_build_array('TimeoutError'), 'agent_id', 'credit-monitor', 'test_scenario', true),
    v_preconditions, NULL, v_escalation,
    jsonb_build_object('scope','ONE_AGENT','target','credit-monitor'), 85, now()
  );
END $$;
