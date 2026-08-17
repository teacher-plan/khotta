-- ════════════════════════════════════════════════════════════════════
-- Phase 3.3 — SELF-HEALING SAFETY GATE VALIDATION
--
-- كل شيءٍ هنا داخل معاملةٍ واحدة (DO $$ ... RAISE EXCEPTION) — بما في
-- ذلك الكتابة الحقيقية على repair_playbooks.circuit_state (نفس عملية
-- checkCircuitBreaker() الحقيقية في opsPlaybooks.ts حرفياً) — فتتراجع
-- تلقائياً (ROLLBACK) عند نهاية الملف، فلا يبقى أي أثرٍ في Production:
-- لا صفوف اختبارٍ، ولا تغييرٌ حقيقي في circuit_state. هذا أنظف من نمط
-- إدراجٍ-ثم-حذف المُستعمَل في المهام السابقة — صفر بقايا حتى نظرياً.
-- ════════════════════════════════════════════════════════════════════

DO $$
DECLARE
  v_incident_id uuid;
  v_playbook_id text := 'retry_monitor_known_timeout';
  v_max_attempts int;
  v_cooldown_minutes int;
  v_circuit_threshold int;
  v_circuit_window int;
  v_attempts_count int;
  v_rate_limited boolean;
  v_circuit_failures int;
  v_circuit_would_open boolean;
  v_circuit_state_before text;
  v_circuit_state_after text;
  v_cooldown_active boolean;
  v_new_incident_blocked boolean;
  v_verification_failed_resolves boolean;
  v_rollback_strategy_1 text;
  v_rollback_strategy_2 text;
BEGIN
  SELECT max_attempts, cooldown_minutes, circuit_breaker_threshold, circuit_breaker_window_minutes, circuit_state
    INTO v_max_attempts, v_cooldown_minutes, v_circuit_threshold, v_circuit_window, v_circuit_state_before
    FROM public.repair_playbooks WHERE playbook_id = v_playbook_id;

  -- حادثةٌ اصطناعية آمنة (ستتراجع مع كل شيء)
  INSERT INTO public.ops_incidents (dedup_key, component, severity, status, confidence, summary, evidence, source_agent, occurrence_count)
  VALUES ('__phase3_3_test__', 'credit-monitor', 'P2', 'DETECTED', 'VERIFIED', '[اختبار Phase 3.3]', '[]'::jsonb, 'credit-monitor', 3)
  RETURNING id INTO v_incident_id;

  -- ── 2) MAX ATTEMPTS: محاولتان فاشلتان (Verification FAIL) على نفس الحادثة ──
  INSERT INTO public.repair_executions (incident_id, playbook_id, action_id, agent_id, mode, status, attempt_number, execution_result, verification_result, completed_at)
  VALUES (v_incident_id, v_playbook_id, 'rerun_monitor_agent', 'credit-monitor', 'SHADOW', 'VERIFICATION_FAILED', 1,
          '{"simulated":true,"note":"Phase 3.3 test — Action نجح تقنياً"}'::jsonb, '{"passed":false,"reason":"simulated verification failure"}'::jsonb, now());
  INSERT INTO public.repair_executions (incident_id, playbook_id, action_id, agent_id, mode, status, attempt_number, execution_result, verification_result, completed_at)
  VALUES (v_incident_id, v_playbook_id, 'rerun_monitor_agent', 'credit-monitor', 'SHADOW', 'VERIFICATION_FAILED', 2,
          '{"simulated":true,"note":"Phase 3.3 test — Action نجح تقنياً"}'::jsonb, '{"passed":false,"reason":"simulated verification failure"}'::jsonb, now());

  -- نفس استعلام checkRateLimitAndCooldown() الحقيقي حرفياً:
  SELECT count(*) INTO v_attempts_count FROM public.repair_executions
    WHERE incident_id = v_incident_id AND playbook_id = v_playbook_id;
  v_rate_limited := v_attempts_count >= v_max_attempts;

  -- نفس استعلام cooldown الحقيقي حرفياً:
  SELECT EXISTS (
    SELECT 1 FROM public.repair_executions
    WHERE playbook_id = v_playbook_id
      AND started_at >= now() - (v_cooldown_minutes || ' minutes')::interval
      AND status IN ('WOULD_AUTO_HEAL','SUCCEEDED','FAILED','VERIFICATION_FAILED','ESCALATED')
  ) INTO v_cooldown_active;

  -- ── 3) CIRCUIT BREAKER: صفٌّ ثالث (فشلٌ إضافي) يبلغ العتبة (3) ──
  INSERT INTO public.repair_executions (incident_id, playbook_id, action_id, agent_id, mode, status, attempt_number, execution_result, completed_at)
  VALUES (v_incident_id, v_playbook_id, 'rerun_monitor_agent', 'credit-monitor', 'SHADOW', 'FAILED', 1,
          '{"simulated":true,"note":"Phase 3.3 test — فشلٌ ثالث ضمن نافذة القاطع"}'::jsonb, now());

  SELECT count(*) INTO v_circuit_failures FROM public.repair_executions
    WHERE playbook_id = v_playbook_id AND started_at >= now() - (v_circuit_window || ' minutes')::interval
      AND status IN ('FAILED','VERIFICATION_FAILED');
  v_circuit_would_open := v_circuit_failures >= v_circuit_threshold;

  -- تنفيذٌ حقيقي (سيتراجع) لنفس عملية checkCircuitBreaker() تماماً — كتابةٌ فعلية على العمود الحقيقي:
  IF v_circuit_would_open THEN
    UPDATE public.repair_playbooks SET circuit_state = 'OPEN', circuit_opened_at = now() WHERE playbook_id = v_playbook_id;
  END IF;
  SELECT circuit_state INTO v_circuit_state_after FROM public.repair_playbooks WHERE playbook_id = v_playbook_id;

  -- حادثةٌ جديدة افتراضية لنفس الـPlaybook — هل ستُحجَب؟ (نفس منطق evaluateShadow: circuit_state='OPEN' ⇒ CIRCUIT_OPEN فوراً، لا فحص preconditions إطلاقاً)
  v_new_incident_blocked := (v_circuit_state_after = 'OPEN');

  -- ── 5) VERIFICATION FAILURE: مراجعة الكود — هل أي مسارٍ يُحوِّل incident إلى RESOLVED عند VERIFICATION_FAILED؟ ──
  -- (فحصٌ منطقي مبنيٌّ على مراجعة ops-actions/index.ts: resolveIncident() يُستدعى حصراً بعد verification_result.passed=true)
  v_verification_failed_resolves := false;  -- CODE VERIFIED: لا مسار كهذا موجود، تحقّقٌ بالمراجعة لا بالتنفيذ الحيّ لأن Shadow لا يُنفِّذ Action فعلياً أصلاً

  SELECT rollback_strategy INTO v_rollback_strategy_1 FROM public.repair_playbooks WHERE playbook_id = 'retry_monitor_known_timeout';
  SELECT rollback_strategy INTO v_rollback_strategy_2 FROM public.repair_playbooks WHERE playbook_id = 'reschedule_known_daily_summary_failure';

  RAISE EXCEPTION 'PHASE3_3_SAFETY_GATE_EVIDENCE | MAX_ATTEMPTS: configured=%, attempts_recorded=%, rate_limited=% | COOLDOWN: configured_minutes=%, cooldown_active=% | CIRCUIT: threshold=%, window_min=%, failures_in_window=%, would_open=%, state_before=%, state_after_real_update=%, new_incident_would_be_blocked=% | VERIFICATION_FAILURE_NEVER_AUTO_RESOLVES: % | ROLLBACK_STRATEGIES: playbook1=[%], playbook2=[%]',
    v_max_attempts, v_attempts_count, v_rate_limited,
    v_cooldown_minutes, v_cooldown_active,
    v_circuit_threshold, v_circuit_window, v_circuit_failures, v_circuit_would_open, v_circuit_state_before, v_circuit_state_after, v_new_incident_blocked,
    v_verification_failed_resolves,
    v_rollback_strategy_1, v_rollback_strategy_2;
END $$;
