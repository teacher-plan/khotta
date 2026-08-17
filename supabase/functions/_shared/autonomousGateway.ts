// ═══ KHOTTA Autonomous Operations 2.0 — Phase 3.5-A: بوّابة التنفيذ
// الآلي (Autonomous Execution Gateway) — بنيةٌ تحتيةٌ فقط، غير مُفعَّلة.
//
// هذا الملف مسارٌ منفصلٌ تماماً عن التنفيذ البشري في
// ops-actions/index.ts (action:"execute") — لا يُعاد استخدام أي كودٍ من
// تلك الدالّة نفسها، فقط يُستورَد من opsActionRegistry.ts (ACTIONS نفسها
// المُسجَّلة والمُتحقَّق منها) وopsPlaybooks.ts (checkPreconditions/
// checkRateLimitAndCooldown/checkCircuitBreaker/computeBlastRadius) —
// نفس دوال الحساب المنطقي، لا إعادة اختراعٍ لها، لكن التركيب/التسلسل/نقطة
// الدخول هنا جديدةٌ بالكامل وحصرية لهذا المسار (المتطلَّب 1).
//
// ═══ لماذا يستحيل بنيوياً أن يُنفَّذ شيءٌ فعلي عبر هذا الملف اليوم ═══
//   Gate 3: self_healing_controls.self_healing_enabled يجب = true (هو
//           كذلك افتراضياً اليوم — لكن هذا وحده لا يكفي، انظر Gate 4).
//   Gate 4: pb.enabled === true AND pb.mode === 'AUTO' — كلا الصفّين
//           الوحيدين الموجودين اليوم في repair_playbooks (mode='SHADOW')
//           يفشلان هذا الشرط دوماً. هذه هي آلية التعطيل الفعلية، لا
//           تعليقاً نصّياً فقط — Gate 3 وGate 4 مستقلّان تماماً (المتطلَّب
//           6): تعطيل self_healing_enabled عامّاً لا يمسّ أي شيءٍ آخر
//           (مراقبة/تشخيص/تنبيهات/الكوبايلوت)، وحتى لو كان مفعَّلاً عامّاً
//           فلا Playbook بوضع AUTO ⇒ Gate 4 يوقف كل شيء دوماً اليوم.
//   ولا سبيل بشري لتفعيل mode='AUTO' اليوم أصلاً: set_playbook_mode في
//   ops-actions/index.ts يرفض صراحةً (403) أي طلب mode='AUTO' — لم
//   يُعدَّل في هذه المرحلة (المتطلَّب 9/10 من مواصفة المستخدم).
//   ولا مسار كودٍ حيّ (لا Edge Function، لا cron) يستدعي executeAutonomous
//   من هذا الملف اليوم — export جديدٌ غير مُستدعًى (المتطلَّب 10 من
//   مواصفة المستخدم/القسم 14 من هذه المهمّة).
//
// لا LLM هنا إطلاقاً: لا استيراد لـai.ts/aiJson.ts/orFetch — التشخيص
// (الذي قد يستخدم LLM) يحدث بالكامل قبل استدعاء هذه البوّابة؛ تستهلك
// البوّابة فقط حقولاً بنيويةً جاهزة (confidence/recommended_action_id/
// risk_level) من ops_diagnoses، لا نصّاً حرّاً من أي نموذج.
//
// لا SQL خام إطلاقاً: كل وصول للقاعدة عبر supabase-js query builder أو
// admin.rpc() لدوالّ Postgres مُعرَّفة صراحةً في الهجرة (claim_incident_
// for_repair/release_incident_claim) — لا template string SQL في أي مكان.
//
// deno-lint-ignore-file no-explicit-any
import { ACTIONS, isKnownAction } from "./opsActionRegistry.ts";
import {
  PlaybookRow,
  PreconditionCheck,
  checkPreconditions,
  checkRateLimitAndCooldown,
  checkCircuitBreaker,
  computeBlastRadius,
  matchIncidentPattern,
} from "./opsPlaybooks.ts";

// الفاعل الوحيد المسموح لهذا المسار — لا يظهر أبداً كفعلٍ بشري.
export const AUTONOMOUS_ACTOR = "autonomous_execution_gateway";

export interface GateResult {
  gate: string;
  passed: boolean;
  status: string;   // قيمةٌ من repair_executions.status عند الرفض
  reason: string;
}

export interface GatewayContext {
  incidentId: string;
  diagnosisId: string;
  agentId: string;
  consecutiveFailures: number;
  distinctErrors: string[];
  lastSuccessAt: string | null;
}

// ─────────────────────────────────────────────────────────────────────
// Gate 0: صلاحية الحادثة — موجودةٌ فعلاً، لم تُحلّ سابقاً.
// ─────────────────────────────────────────────────────────────────────
export async function gate0_incidentValid(admin: any, incidentId: string): Promise<GateResult & { incident?: any }> {
  const { data: incident } = await admin.from("ops_incidents").select("*").eq("id", incidentId).maybeSingle();
  if (!incident) {
    return { gate: "gate0_incident_valid", passed: false, status: "INVALID_INCIDENT", reason: `لا حادثة بهذا المعرّف: ${incidentId}.` };
  }
  if (incident.status === "RESOLVED") {
    return { gate: "gate0_incident_valid", passed: false, status: "INVALID_INCIDENT", reason: "الحادثة مُغلَقةٌ سلفاً (RESOLVED) — لا داعي لإصلاح." };
  }
  return { gate: "gate0_incident_valid", passed: true, status: "EVALUATING", reason: "الحادثة موجودةٌ ومفتوحة.", incident };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 1: صلاحية التشخيص — يجب أن يكون مكتملاً (COMPLETED) ومرتبطاً
// بنفس الحادثة، لا تشخيصاً معلَّقاً أو فاشلاً أو من حادثةٍ أخرى.
// ─────────────────────────────────────────────────────────────────────
export async function gate1_diagnosisValid(admin: any, diagnosisId: string, incidentId: string): Promise<GateResult & { diagnosis?: any }> {
  const { data: diag } = await admin.from("ops_diagnoses").select("*").eq("diagnosis_id", diagnosisId).maybeSingle();
  if (!diag) {
    return { gate: "gate1_diagnosis_valid", passed: false, status: "INVALID_DIAGNOSIS", reason: `لا تشخيص بهذا المعرّف: ${diagnosisId}.` };
  }
  if (diag.incident_id !== incidentId) {
    return { gate: "gate1_diagnosis_valid", passed: false, status: "INVALID_DIAGNOSIS", reason: "التشخيص لا يخصّ الحادثة المُعطاة." };
  }
  if (diag.diagnosis_status !== "COMPLETED") {
    return { gate: "gate1_diagnosis_valid", passed: false, status: "INVALID_DIAGNOSIS", reason: `حالة التشخيص ${diag.diagnosis_status} — يجب COMPLETED.` };
  }
  return { gate: "gate1_diagnosis_valid", passed: true, status: "EVALUATING", reason: "التشخيص مكتملٌ ويخصّ الحادثة.", diagnosis: diag };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 2: تطابق نمط حادثةٍ معروف + وجود Playbook مفعَّل يطابقه — نفس
// matchIncidentPattern الحتمية في opsPlaybooks.ts، لا استنتاج LLM.
// ─────────────────────────────────────────────────────────────────────
export async function gate2_playbookMatch(
  admin: any, evidence: { agent_id?: string; consecutive_failures?: number; distinct_errors?: string[] },
): Promise<GateResult & { playbook?: PlaybookRow }> {
  const pattern = matchIncidentPattern(evidence);
  if (!pattern) {
    return { gate: "gate2_playbook_match", passed: false, status: "NO_PLAYBOOK_MATCH", reason: "لا نمط حادثةٍ معروف يطابق الأدلّة." };
  }
  const { data: pb } = await admin.from("repair_playbooks").select("*").eq("incident_pattern", pattern).maybeSingle();
  if (!pb) {
    return { gate: "gate2_playbook_match", passed: false, status: "NO_PLAYBOOK_MATCH", reason: `نمطٌ معروف (${pattern}) لكن لا Playbook مسجَّل يطابقه.` };
  }
  return { gate: "gate2_playbook_match", passed: true, status: "EVALUATING", reason: `طابق ${pattern} ⇒ ${pb.playbook_id}.`, playbook: pb as PlaybookRow };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 3: مفتاح الإيقاف الطارئ العام — مستقلٌّ تماماً عن Gate 4 (مود
// الـPlaybook). تعطيل هذا لا يمسّ المراقبة/التشخيص/التنبيهات/الكوبايلوت
// إطلاقاً — فقط يمنع هذه البوّابة تحديداً من المتابعة.
// ─────────────────────────────────────────────────────────────────────
export async function gate3_globalKillSwitch(admin: any, agentId: string): Promise<GateResult> {
  const { data: ctl } = await admin.from("self_healing_controls").select("*").eq("control_id", "global").maybeSingle();
  if (!ctl) {
    return { gate: "gate3_global_kill_switch", passed: false, status: "DISABLED", reason: "لا صفّ self_healing_controls('global') — يُعامَل كمُعطَّلٍ افتراضياً (لا يُفترَض تفعيلٌ بلا دليل)." };
  }
  if (ctl.self_healing_enabled === false) {
    return { gate: "gate3_global_kill_switch", passed: false, status: "DISABLED", reason: `الإصلاح الذاتي مُعطَّلٌ عامّاً: ${ctl.disabled_reason || "بلا سببٍ مذكور"}.` };
  }
  const disabledAgents: string[] = (ctl.disabled_agents || []) as string[];
  if (disabledAgents.includes(agentId)) {
    return { gate: "gate3_global_kill_switch", passed: false, status: "DISABLED", reason: `الإصلاح الذاتي معطَّلٌ تحديداً للوكيل ${agentId}.` };
  }
  return { gate: "gate3_global_kill_switch", passed: true, status: "EVALUATING", reason: "المفتاح العام مفعَّل، الوكيل غير مستثنى." };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 4: mode==='AUTO' تحديداً + enabled=true — آلية التعطيل الفعلية
// لكل تنفيذٍ آلي حقيقي. اليوم: كل صفّ في repair_playbooks بوضع SHADOW
// ⇒ هذا الشرط يفشل دوماً بصرف النظر عن Gate 3.
// ─────────────────────────────────────────────────────────────────────
export function gate4_playbookAutoMode(pb: PlaybookRow): GateResult {
  if (!pb.enabled) {
    return { gate: "gate4_playbook_auto_mode", passed: false, status: "DISABLED", reason: `الـPlaybook ${pb.playbook_id} معطَّلٌ (enabled=false).` };
  }
  if (pb.mode !== "AUTO") {
    return { gate: "gate4_playbook_auto_mode", passed: false, status: "DISABLED", reason: `الـPlaybook ${pb.playbook_id} بوضع ${pb.mode} لا AUTO — لا تنفيذ آلي ممكن. Phase 3.5-A لا تُفعِّل AUTO لأي Playbook.` };
  }
  return { gate: "gate4_playbook_auto_mode", passed: true, status: "EVALUATING", reason: `الـPlaybook مفعَّلٌ وبوضع AUTO.` };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 5: القاطع (Circuit Breaker) — إعادة استخدام checkCircuitBreaker.
// ─────────────────────────────────────────────────────────────────────
export async function gate5_circuitBreaker(admin: any, pb: PlaybookRow): Promise<GateResult> {
  const circuit = await checkCircuitBreaker(admin, pb);
  if (circuit.open) {
    return { gate: "gate5_circuit_breaker", passed: false, status: "CIRCUIT_OPEN", reason: `القاطع مفتوحٌ (${circuit.failuresInWindow >= 0 ? circuit.failuresInWindow + " فشلاً ضمن النافذة" : "مفتوحٌ سلفاً"}).` };
  }
  return { gate: "gate5_circuit_breaker", passed: true, status: "EVALUATING", reason: "القاطع مغلق." };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 6: عتبة الثقة — pb.minimum_confidence.
// ─────────────────────────────────────────────────────────────────────
export function gate6_confidenceThreshold(pb: PlaybookRow, confidence: number | null): GateResult {
  const c = confidence ?? 0;
  if (c < pb.minimum_confidence) {
    return { gate: "gate6_confidence_threshold", passed: false, status: "ESCALATED", reason: `الثقة ${c}% أقل من الحدّ الأدنى ${pb.minimum_confidence}%.` };
  }
  return { gate: "gate6_confidence_threshold", passed: true, status: "EVALUATING", reason: `الثقة ${c}% >= ${pb.minimum_confidence}%.` };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 7: خطورة LOW فقط — لا استثناء، لا مسار MEDIUM/HIGH/CRITICAL في
// هذه المرحلة مهما كانت الثقة.
// ─────────────────────────────────────────────────────────────────────
export function gate7_riskLowOnly(pb: PlaybookRow): GateResult {
  if (pb.risk_level !== "LOW") {
    return { gate: "gate7_risk_low_only", passed: false, status: "RISK_BLOCKED", reason: `خطورة الـPlaybook ${pb.risk_level} — البوّابة الآلية لا تنفّذ إلا LOW.` };
  }
  return { gate: "gate7_risk_low_only", passed: true, status: "EVALUATING", reason: "الخطورة LOW." };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 8: السقف + cooldown — إعادة استخدام checkRateLimitAndCooldown.
// ─────────────────────────────────────────────────────────────────────
export async function gate8_rateLimitCooldown(admin: any, pb: PlaybookRow, incidentId: string): Promise<GateResult & { attemptsSoFar?: number }> {
  const rl = await checkRateLimitAndCooldown(admin, pb, incidentId);
  if (rl.rateLimited) {
    return { gate: "gate8_rate_limit_cooldown", passed: false, status: "RATE_LIMITED", reason: `تجاوز سقف ${pb.max_attempts} محاولاتٍ.`, attemptsSoFar: rl.attemptsSoFar };
  }
  if (rl.cooldownActive) {
    return { gate: "gate8_rate_limit_cooldown", passed: false, status: "COOLDOWN_ACTIVE", reason: `نافذة تهدئةٍ نشطة حتى ${rl.cooldownUntil}.`, attemptsSoFar: rl.attemptsSoFar };
  }
  return { gate: "gate8_rate_limit_cooldown", passed: true, status: "EVALUATING", reason: "لا سقفٌ ولا تهدئة نشطة.", attemptsSoFar: rl.attemptsSoFar };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 9: كل الشروط المسبقة الثمانية — إعادة استخدام checkPreconditions
// (النسخة المُصلَحة في Phase 3.2: first_seen_at/status<>'RESOLVED'/
// deployment_log الحقيقي).
// ─────────────────────────────────────────────────────────────────────
export async function gate9_preconditions(
  admin: any, pb: PlaybookRow, ctx: GatewayContext & { incidentComponent: string },
): Promise<GateResult & { preconditions: PreconditionCheck[] }> {
  const preconditions = await checkPreconditions(admin, pb, {
    agentId: ctx.agentId, consecutiveFailures: ctx.consecutiveFailures,
    distinctErrors: ctx.distinctErrors, lastSuccessAt: ctx.lastSuccessAt,
    incidentComponent: ctx.incidentComponent,
  });
  const failed = preconditions.filter((p) => !p.passed);
  if (failed.length) {
    return {
      gate: "gate9_preconditions", passed: false, status: "PRECONDITION_FAILED",
      reason: `شروطٌ مسبقة لم تتحقّق: ${failed.map((p) => p.name).join("، ")}.`, preconditions,
    };
  }
  return { gate: "gate9_preconditions", passed: true, status: "EVALUATING", reason: "كل الشروط المسبقة تحقّقت.", preconditions };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 10: تحقّقٌ كاملٌ من سجلّ الإجراءات قبل أي محاولة تنفيذ — معروفٌ
// في الكود (isKnownAction) + مفعَّلٌ في القاعدة + خطورةٌ LOW + ضمن
// allowed_actions للـPlaybook + مخطّط مُدخَلاتٍ (إن كان له معنى فعلي —
// انظر الملاحظة أدناه) + نطاق تأثيرٍ مسموح + استراتيجية تحقّقٍ موجودة.
// ─────────────────────────────────────────────────────────────────────
export async function gate10_actionRegistryValidation(
  admin: any, pb: PlaybookRow, actionId: string, params: Record<string, unknown>, agentId: string,
): Promise<GateResult & { registryRow?: any }> {
  if (!actionId || !isKnownAction(actionId)) {
    return { gate: "gate10_action_registry_validation", passed: false, status: "ACTION_VALIDATION_FAILED", reason: `الإجراء غير معروفٍ في الكود: ${actionId}.` };
  }
  if (!pb.allowed_actions.includes(actionId)) {
    return { gate: "gate10_action_registry_validation", passed: false, status: "ACTION_VALIDATION_FAILED", reason: `${actionId} ليس ضمن allowed_actions للـPlaybook ${pb.playbook_id}.` };
  }
  const { data: reg } = await admin.from("safe_action_registry").select("*").eq("action_id", actionId).maybeSingle();
  if (!reg) {
    return { gate: "gate10_action_registry_validation", passed: false, status: "ACTION_VALIDATION_FAILED", reason: `لا صفّ safe_action_registry لـ${actionId}.` };
  }
  if (!reg.enabled) {
    return { gate: "gate10_action_registry_validation", passed: false, status: "ACTION_VALIDATION_FAILED", reason: `${actionId} غير مفعَّلٍ في safe_action_registry.` };
  }
  if (reg.risk_level !== "LOW") {
    return { gate: "gate10_action_registry_validation", passed: false, status: "ACTION_VALIDATION_FAILED", reason: `خطورة الإجراء ${reg.risk_level} — البوّابة الآلية تسمح فقط بـLOW.` };
  }
  const allowedAgents: string[] = (reg.allowed_agents || []) as string[];
  if (allowedAgents.length && !allowedAgents.includes(agentId)) {
    return { gate: "gate10_action_registry_validation", passed: false, status: "ACTION_VALIDATION_FAILED", reason: `${agentId} ليس ضمن allowed_agents للإجراء ${actionId}.` };
  }
  // مخطّط المُدخَلات: تحقّقٌ سطحيٌّ (وجود المفاتيح المطلوبة إن ذُكرت في
  // input_schema.required) — ملاحظةٌ صريحة: كلا الإجراءين الحاليين
  // (rerun_monitor_agent وreschedule_daily_summary) لهما input_schema
  // فارغٌ أو بلا required فعلي في الهجرات الحالية، فهذا التحقّق اليوم
  // no-op عملياً (لا مُدخلاتٍ إلزامية مُعرَّفة بعد) — مُوثَّقٌ في التقرير،
  // لا يُدَّعى أنه تحقّقٌ عميقٌ لمخطّطٍ غير موجود.
  const required: string[] = (reg.input_schema?.required || []) as string[];
  const missing = required.filter((k) => !(k in params));
  if (missing.length) {
    return { gate: "gate10_action_registry_validation", passed: false, status: "ACTION_VALIDATION_FAILED", reason: `مُدخَلاتٌ إلزاميةٌ ناقصة: ${missing.join("، ")}.` };
  }
  const blast = computeBlastRadius(pb, agentId);
  if (!blast.allowed) {
    return { gate: "gate10_action_registry_validation", passed: false, status: "ACTION_VALIDATION_FAILED", reason: `نطاق تأثيرٍ ممنوع: ${blast.scope}.` };
  }
  if (!reg.verification_strategy) {
    return { gate: "gate10_action_registry_validation", passed: false, status: "ACTION_VALIDATION_FAILED", reason: "لا استراتيجية تحقّقٍ موثَّقة لهذا الإجراء." };
  }
  return { gate: "gate10_action_registry_validation", passed: true, status: "EVALUATING", reason: `${actionId} معروفٌ، مفعَّلٌ، LOW، مسموحٌ للـPlaybook والوكيل، ولديه استراتيجية تحقّق.`, registryRow: reg };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 11: القفل الذرّي — استدعاء دالّة Postgres claim_incident_for_repair
// (عبارة SQL واحدة، لا سباق SELECT-then-UPDATE). فشل الادّعاء = محاولةٌ
// أخرى (متزامنة أو حديثة) نشطة على نفس (incident_id, playbook_id).
// ─────────────────────────────────────────────────────────────────────
export async function gate11_atomicClaim(admin: any, incidentId: string, playbookId: string): Promise<GateResult & { claimId?: string }> {
  const { data: claimId, error } = await admin.rpc("claim_incident_for_repair", {
    p_incident_id: incidentId, p_playbook_id: playbookId, p_claimed_by: AUTONOMOUS_ACTOR, p_stale_minutes: 15,
  });
  if (error) {
    return { gate: "gate11_atomic_claim", passed: false, status: "CLAIM_FAILED", reason: `خطأ استدعاء claim_incident_for_repair: ${error.message}` };
  }
  if (!claimId) {
    return { gate: "gate11_atomic_claim", passed: false, status: "CLAIM_FAILED", reason: "ادّعاءٌ نشطٌ آخر موجودٌ سلفاً على نفس (incident_id, playbook_id) — لا تنفيذٌ متزامنٌ مزدوج." };
  }
  return { gate: "gate11_atomic_claim", passed: true, status: "EVALUATING", reason: "تمّ الادّعاء الذرّي بنجاح.", claimId: String(claimId) };
}

// ─────────────────────────────────────────────────────────────────────
// Gate 12: التحقّق من عدم وجود مفتاح idempotency مُستخدَمٍ سلفاً — تحقّقٌ
// تطبيقيٌّ استباقي (تجربة UX أفضل: رفضٌ برسالةٍ واضحة)، لكن الحارس
// الحقيقي غير القابل للتفويت هو UNIQUE INDEX في القاعدة (الهجرة)
// الذي يفشل INSERT الفعلي حتى لو مرّ هذا الفحص تحت تزامنٍ حقيقي.
// ─────────────────────────────────────────────────────────────────────
export async function gate12_idempotencyCheck(
  admin: any, incidentId: string, playbookId: string, attemptNumber: number,
): Promise<GateResult> {
  const { data: existing } = await admin.from("repair_executions").select("repair_id")
    .eq("incident_id", incidentId).eq("playbook_id", playbookId).eq("attempt_number", attemptNumber).maybeSingle();
  if (existing) {
    return { gate: "gate12_idempotency_check", passed: false, status: "DUPLICATE_EXECUTION_BLOCKED", reason: `تنفيذٌ سابقٌ موجودٌ بالفعل لـ(${incidentId}, ${playbookId}, محاولة ${attemptNumber}) — repair_id=${existing.repair_id}.` };
  }
  return { gate: "gate12_idempotency_check", passed: true, status: "EVALUATING", reason: "لا تكرار — مفتاح idempotency جديد." };
}

// ═══════════════════════════════════════════════════════════════════
// executeAutonomous — التركيب الكامل لكل البوّابات بالترتيب، قطعٌ فوري
// (short-circuit) عند أول فشل. كل استدعاءٍ — بما فيه كل رفضٍ مبكر —
// يُسجَّل صفاً في repair_executions (المتطلَّب 11).
//
// ⚠️ غير مُستدعاةٍ من أي مسار HTTP/cron حيّ في هذه المرحلة. export جديدٌ
// فقط، جاهزٌ للاختبار والمراجعة، لا للتشغيل الفعلي (القسم 14/17 من
// مواصفة المستخدم).
// ═══════════════════════════════════════════════════════════════════
export async function executeAutonomous(
  admin: any,
  input: {
    incidentId: string;
    diagnosisId: string;
    agentId: string;
    consecutiveFailures: number;
    distinctErrors: string[];
    lastSuccessAt: string | null;
  },
): Promise<{ status: string; reason: string; gates: GateResult[]; repair_id?: string; execution_result?: unknown; verification_result?: unknown }> {
  const gates: GateResult[] = [];
  const correlationId = crypto.randomUUID();

  async function recordAndReturn(g: GateResult, extra: Record<string, unknown> = {}) {
    gates.push(g);
    const { data: row } = await admin.from("repair_executions").insert({
      incident_id: input.incidentId,
      diagnosis_id: input.diagnosisId,
      playbook_id: (extra.playbook_id as string) || null,
      action_id: (extra.action_id as string) || null,
      agent_id: input.agentId,
      correlation_id: correlationId,
      mode: "AUTO",
      status: g.status,
      attempt_number: (extra.attempt_number as number) || 1,
      evidence_snapshot: { consecutive_failures: input.consecutiveFailures, distinct_errors: input.distinctErrors, last_success_at: input.lastSuccessAt },
      preconditions_result: (extra.preconditions as unknown) || [],
      blast_radius: (extra.blast_radius as unknown) || { scope: "NONE", target: input.agentId },
      escalation_reason: g.passed ? null : g.reason,
      actor: AUTONOMOUS_ACTOR,
    }).select("repair_id").maybeSingle();
    return { status: g.status, reason: g.reason, gates, repair_id: row?.repair_id };
  }

  // Gate 0
  const g0 = await gate0_incidentValid(admin, input.incidentId);
  if (!g0.passed) return recordAndReturn(g0);
  gates.push(g0);

  // Gate 1
  const g1 = await gate1_diagnosisValid(admin, input.diagnosisId, input.incidentId);
  if (!g1.passed) return recordAndReturn(g1);
  gates.push(g1);
  const diag = g1.diagnosis;

  // Gate 2
  const g2 = await gate2_playbookMatch(admin, {
    agent_id: input.agentId, consecutive_failures: input.consecutiveFailures, distinct_errors: input.distinctErrors,
  });
  if (!g2.passed) return recordAndReturn(g2);
  gates.push(g2);
  const pb = g2.playbook!;

  // Gate 3 (مستقلٌّ عن Gate 4 — المتطلَّب 6)
  const g3 = await gate3_globalKillSwitch(admin, input.agentId);
  if (!g3.passed) return recordAndReturn(g3, { playbook_id: pb.playbook_id });
  gates.push(g3);

  // Gate 4 — آلية التعطيل الفعلية: mode!=='AUTO' يوقف كل شيء اليوم.
  const g4 = gate4_playbookAutoMode(pb);
  if (!g4.passed) return recordAndReturn(g4, { playbook_id: pb.playbook_id });
  gates.push(g4);

  // Gate 5
  const g5 = await gate5_circuitBreaker(admin, pb);
  if (!g5.passed) return recordAndReturn(g5, { playbook_id: pb.playbook_id });
  gates.push(g5);

  // Gate 6
  const g6 = gate6_confidenceThreshold(pb, diag.confidence);
  if (!g6.passed) return recordAndReturn(g6, { playbook_id: pb.playbook_id });
  gates.push(g6);

  // Gate 7
  const g7 = gate7_riskLowOnly(pb);
  if (!g7.passed) return recordAndReturn(g7, { playbook_id: pb.playbook_id });
  gates.push(g7);

  // Gate 8
  const g8 = await gate8_rateLimitCooldown(admin, pb, input.incidentId);
  if (!g8.passed) return recordAndReturn(g8, { playbook_id: pb.playbook_id });
  gates.push(g8);
  const attemptNumber = (g8.attemptsSoFar || 0) + 1;

  // Gate 9
  const g9 = await gate9_preconditions(admin, pb, {
    ...input, incidentComponent: g0.incident.component,
  });
  if (!g9.passed) return recordAndReturn(g9, { playbook_id: pb.playbook_id, preconditions: g9.preconditions, attempt_number: attemptNumber });
  gates.push(g9);

  const step = pb.repair_steps[0];
  const actionId = step?.action_id || "";
  const params = { ...(step?.params_template || {}), agent_id: input.agentId };
  const blast = computeBlastRadius(pb, input.agentId);

  // Gate 10
  const g10 = await gate10_actionRegistryValidation(admin, pb, actionId, params, input.agentId);
  if (!g10.passed) return recordAndReturn(g10, { playbook_id: pb.playbook_id, action_id: actionId, preconditions: g9.preconditions, blast_radius: blast, attempt_number: attemptNumber });
  gates.push(g10);

  // Gate 11 — القفل الذرّي
  const g11 = await gate11_atomicClaim(admin, input.incidentId, pb.playbook_id);
  if (!g11.passed) return recordAndReturn(g11, { playbook_id: pb.playbook_id, action_id: actionId, preconditions: g9.preconditions, blast_radius: blast, attempt_number: attemptNumber });
  gates.push(g11);
  const claimId = g11.claimId!;

  // Gate 12 — منع التكرار (تطبيقيٌّ استباقي؛ الحارس الحقيقي هو UNIQUE INDEX)
  const g12 = await gate12_idempotencyCheck(admin, input.incidentId, pb.playbook_id, attemptNumber);
  if (!g12.passed) {
    await admin.rpc("release_incident_claim", { p_claim_id: claimId });
    return recordAndReturn(g12, { playbook_id: pb.playbook_id, action_id: actionId, preconditions: g9.preconditions, blast_radius: blast, attempt_number: attemptNumber });
  }
  gates.push(g12);

  // ═══ كل البوّابات اجتِيزت — لن يصل الكود إلى هنا اليوم إطلاقاً لأن
  // Gate 4 يفشل دوماً على كلا الصفّين الوحيدين الحاليَّين (mode=SHADOW).
  // القسم أدناه مبنيٌّ للاكتمال البنيوي وللاختبار المستقبلي فقط. ═══
  const startedAt = new Date().toISOString();
  const impl = ACTIONS[actionId];
  let execResult;
  try {
    execResult = await impl.execute(admin, params);
  } catch (e) {
    execResult = { ok: false, error: String(e) };
  }

  if (!execResult.ok) {
    await admin.rpc("release_incident_claim", { p_claim_id: claimId });
    const failGate: GateResult = { gate: "execute", passed: false, status: "FAILED", reason: `فشل التنفيذ: ${execResult.error}` };
    if (attemptNumber < pb.max_attempts) {
      // المتطلَّب 13: إعادة محاولةٍ محدودة بنفس الإجراء ضمن نفس الـPlaybook
      // فقط — لا استبدال إجراءٍ آخر أبداً. هذا الاستدعاء الحالي ينتهي هنا
      // بحالة FAILED؛ استئنافٌ لاحقٌ (خارج استدعاءٍ واحد) هو ما يزيد
      // attempt_number عبر استدعاءٍ جديدٍ لـexecuteAutonomous، لا حلقةً
      // داخلية هنا.
    }
    if (g0.incident) await admin.from("ops_incidents").update({ status: "ESCALATED", requires_human_attention: true }).eq("id", input.incidentId);
    return recordAndReturn(failGate, {
      playbook_id: pb.playbook_id, action_id: actionId, preconditions: g9.preconditions, blast_radius: blast, attempt_number: attemptNumber,
    });
  }

  let verification;
  try {
    verification = await impl.verify(admin, params, execResult, startedAt);
  } catch (e) {
    verification = { status: "INCONCLUSIVE", detail: { reason: String(e) } };
  }

  await admin.rpc("release_incident_claim", { p_claim_id: claimId });

  // المتطلَّب 12/13: verification.passed !== true (بما فيها INCONCLUSIVE)
  // ⇒ لا SUCCEEDED أبداً، لا حلّ الحادثة أبداً — تصعيدٌ دوماً.
  const passed = verification.status === "PASSED";
  const finalGate: GateResult = passed
    ? { gate: "verify", passed: true, status: "SUCCEEDED", reason: "التنفيذ نجح والتحقّق PASSED." }
    : { gate: "verify", passed: false, status: "VERIFICATION_FAILED", reason: `التحقّق ${verification.status} — لا اعتبار الإصلاح ناجحاً.` };

  if (passed) {
    await admin.from("ops_incidents").update({ status: "RESOLVED", resolved_at: new Date().toISOString() }).eq("id", input.incidentId);
  } else {
    await admin.from("ops_incidents").update({ status: "ESCALATED", requires_human_attention: true }).eq("id", input.incidentId);
  }

  gates.push(finalGate);
  const { data: row } = await admin.from("repair_executions").insert({
    incident_id: input.incidentId, diagnosis_id: input.diagnosisId, playbook_id: pb.playbook_id,
    action_id: actionId, agent_id: input.agentId, correlation_id: correlationId, mode: "AUTO",
    status: finalGate.status, attempt_number: attemptNumber,
    evidence_snapshot: { consecutive_failures: input.consecutiveFailures, distinct_errors: input.distinctErrors, last_success_at: input.lastSuccessAt },
    preconditions_result: g9.preconditions, execution_result: execResult, verification_result: verification,
    blast_radius: blast, confidence_at_decision: diag.confidence, escalation_reason: passed ? null : finalGate.reason,
    actor: AUTONOMOUS_ACTOR, completed_at: new Date().toISOString(),
  }).select("repair_id").maybeSingle();

  return { status: finalGate.status, reason: finalGate.reason, gates, repair_id: row?.repair_id, execution_result: execResult, verification_result: verification };
}
