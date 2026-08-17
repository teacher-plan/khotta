// ═══ KHOTTA Autonomous Operations 2.0 — Phase 3: محرّك مطابقة Playbooks
// + الشروط المسبقة + تقييم Shadow Mode/Dry Run/Auto Mode (Controlled
// Self-Healing Engine) ═══
//
// أنبوبٌ ثابتٌ صريح (القسم 17 من المواصفة)، بلا تخطّي خطوة:
//   Incident → Diagnosis → Playbook Match → Preconditions → Risk Check →
//   Permission Check → Action Registry → Execute → Verify
// لا قفزة من Diagnosis إلى Execute مباشرةً أبداً. المطابقة هنا حتميّةٌ
// بالكامل — لا نداء LLM لاختيار Playbook أو تأليف repair_steps (القسم 2):
// النص الحر (رسائل الخطأ) يُستخدَم فقط كبياناتٍ للمقارنة الحرفية
// (نمط الحادثة/agent_id)، لا كتعليماتٍ تُوجِّه أي قرار (القسم 38).
//
// وضع AUTO مبنيٌّ هنا في الكود (تنفيذٌ فعلي عبر ACTIONS من
// opsActionRegistry.ts، بنفس بوّابات ops-actions:"execute" تماماً) لكنه
// لا يُستدعى فعلياً من أي مسارٍ حيّ في هذه المرحلة — كل صفٍّ في
// repair_playbooks يُدخَل بـmode='SHADOW' فقط (القسم 15)، والمسار الوحيد
// المُستدعى فعلياً من ops-actions هو evaluateShadow.
//
// deno-lint-ignore-file no-explicit-any
import { ACTIONS, isKnownAction } from "./opsActionRegistry.ts";

export interface PlaybookRow {
  playbook_id: string; name: string; incident_pattern: string;
  diagnosis_requirements: Record<string, unknown>; minimum_confidence: number;
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  allowed_agents: string[]; allowed_actions: string[]; preconditions: string[];
  repair_steps: { action_id: string; params_template: Record<string, unknown> }[];
  rollback_strategy: string; max_attempts: number; cooldown_minutes: number;
  circuit_breaker_threshold: number; circuit_breaker_window_minutes: number;
  affected_scope: string; mode: "SHADOW" | "AUTO" | "PAUSED" | "DISABLED";
  circuit_state: "CLOSED" | "OPEN"; requires_human_approval: boolean; enabled: boolean;
}

export interface PreconditionCheck { name: string; passed: boolean; detail: string }
export interface DecisionResult {
  status: string;             // repair_executions.status
  reason?: string;
  preconditions: PreconditionCheck[];
  blast_radius: { scope: string; target: string };
}

// القسم 3: أنماطٌ حصريةٌ تطابق حرفياً معرّفات ruleBasedDiagnose (opsDiagnosis.ts)
// — لا مطابقة نصّيةٍ ضبابية بالذكاء الاصطناعي، لا يُستنتَج النمط إلا من
// خواصّ الأدلّة البنيوية (failures/sameError/agent_id) لا من نص رسالة
// الخطأ نفسها كتعليمات.
export function matchIncidentPattern(evidence: { agent_id?: string; consecutive_failures?: number; distinct_errors?: string[] }): string | null {
  const failures = evidence.consecutive_failures || 0;
  const errors = evidence.distinct_errors || [];
  const sameError = errors.length === 1 && failures >= 2;
  if (failures >= 3 && sameError) {
    if (evidence.agent_id === "daily-summary") return "KNOWN_DAILY_SUMMARY_REPEATED_FAILURE";
    return "KNOWN_MONITOR_REPEATED_FAILURE";
  }
  return null;
}

// القسم 5: كل شرطٍ من preconditions تحقّقٌ حتميٌّ منفصل — فشل أيٍّ منها
// يمنع أي إصلاحٍ (حتى في وضع Shadow لا يُعلَّم WOULD_AUTO_HEAL).
export async function checkPreconditions(
  admin: any, pb: PlaybookRow,
  ctx: { agentId: string; consecutiveFailures: number; distinctErrors: string[]; lastSuccessAt: string | null; incidentComponent: string },
): Promise<PreconditionCheck[]> {
  const out: PreconditionCheck[] = [];

  out.push({
    name: "same_function_same_error_pattern",
    passed: ctx.distinctErrors.length === 1,
    detail: ctx.distinctErrors.length === 1 ? "رسالة خطأٍ واحدة ثابتة." : `${ctx.distinctErrors.length} رسالة خطأٍ مختلفة — لا نمطٌ ثابت.`,
  });

  const minFailures = Number((pb.diagnosis_requirements as any)?.min_consecutive_failures ?? 3);
  out.push({
    name: "failure_count_at_or_above_threshold",
    passed: ctx.consecutiveFailures >= minFailures,
    detail: `${ctx.consecutiveFailures} فشلاً متتالياً (الحدّ الأدنى ${minFailures}).`,
  });

  out.push({
    name: "last_known_success_exists",
    passed: !!ctx.lastSuccessAt,
    detail: ctx.lastSuccessAt ? `آخر نجاحٍ معروف: ${ctx.lastSuccessAt}` : "لا تشغيلة ناجحة معروفة سابقاً — لا يمكن التأكد أن الإصلاح يعيد حالةً سليمة معروفة.",
  });

  // لا حادثةٌ مشابهة مفتوحة/مُصعَّدة لنفس المكوّن آخر cooldown_minutes.
  //
  // إصلاحٌ (Phase 3.2): كان هذا الاستعلام يستعمل عمود created_at غير
  // الموجود إطلاقاً في ops_incidents (تحقّقٌ حيّ أثبت غيابه — انظر تقرير
  // Phase 3.1)، فيفشل بخطإٍ حقيقي عند التنفيذ الفعلي، لا بنتيجةٍ منطقية.
  // العمود الصحيح: first_seen_at — يُضبَط مرّةً واحدة فقط عند إدراج
  // الحادثة (DEFAULT now()، لا يُعاد كتابته أبداً؛ processIncidents في
  // system-health-check/index.ts يُحدِّث last_seen_at فقط عند التكرار) —
  // فهو المطابق فعلياً لدلالة "created_at" لا last_seen_at.
  //
  // كذلك كانت القيمة 'OPEN' مستعملةً في .in("status", …) رغم أنها لم
  // توجد إطلاقاً في أي نسخةٍ من قيد ops_incidents_status_check عبر كل
  // المهاجرات (القيم الفعلية: DETECTED/INVESTIGATING/IDENTIFIED/
  // RECOMMENDATION/RESOLVED/ESCALATED) — فكان هذا الشطر ميتاً بنيوياً
  // دوماً. الدلالة الصحيحة لـ"حادثةٍ لا تزال مفتوحة" في هذا المخطّط هي
  // status <> 'RESOLVED' (system-health-check يُدرِج status:'DETECTED'
  // ابتداءً، ولا حالة أخرى تعني إغلاقاً سوى RESOLVED).
  const since = new Date(Date.now() - pb.cooldown_minutes * 60 * 1000).toISOString();
  const { data: recentIncidents } = await admin.from("ops_incidents")
    .select("id,status").eq("component", ctx.incidentComponent).gte("first_seen_at", since)
    .neq("status", "RESOLVED");
  const similarOpenCount = (recentIncidents || []).length;
  out.push({
    name: "no_similar_incident_open_recently",
    passed: similarOpenCount <= 1,   // الحادثة الحالية نفسها ستظهر غالباً — سماحٌ لواحدة فقط
    detail: `${similarOpenCount} حادثةٍ مفتوحة/مُصعَّدة لنفس المكوّن آخر ${pb.cooldown_minutes} دقيقة.`,
  });

  // Phase 3.2: مصدر بياناتٍ حقيقيٌّ الآن (deployment_log، يكتبه
  // deploy-functions.yml بعد كل نشرٍ ناجح فعلياً). إن لم يوجد أي سجلٍّ
  // إطلاقاً، أو حدث نشرٌ ضمن نافذة cooldown_minutes نفسها، يُعتبَر الشرط
  // غير مُحقَّقٍ صراحةً — لا يُفترَض ناجحاً أبداً بلا دليل (القسم 4/38).
  const { data: lastDeploy } = await admin.from("deployment_log")
    .select("deployed_at").order("deployed_at", { ascending: false }).limit(1).maybeSingle();
  let deploymentPassed = false;
  let deploymentDetail: string;
  if (!lastDeploy) {
    deploymentDetail = "لا سجلّ نشرٍ متاحٌ بعد في deployment_log — لا يمكن التحقّق، فالشرط غير مُحقَّقٍ صراحةً (NOT_AVAILABLE)، لا افتراض نجاح.";
  } else {
    const minutesSinceDeploy = (Date.now() - new Date(lastDeploy.deployed_at).getTime()) / 60000;
    deploymentPassed = minutesSinceDeploy > pb.cooldown_minutes;
    deploymentDetail = deploymentPassed
      ? `آخر نشرٍ كان منذ ${Math.round(minutesSinceDeploy)} دقيقة — أقدم من نافذة cooldown (${pb.cooldown_minutes} دقيقة)، فالسياق مستقرّ.`
      : `آخر نشرٍ كان منذ ${Math.round(minutesSinceDeploy)} دقيقة فقط — ضمن نافذة cooldown (${pb.cooldown_minutes} دقيقة)، قد يكون السياق تغيَّر.`;
  }
  out.push({ name: "no_recent_deployment_change", passed: deploymentPassed, detail: deploymentDetail });

  out.push({
    name: "agent_permitted_for_playbook",
    passed: pb.allowed_agents.includes(ctx.agentId),
    detail: pb.allowed_agents.includes(ctx.agentId) ? `${ctx.agentId} ضمن allowed_agents.` : `${ctx.agentId} ليس ضمن allowed_agents لهذا الـPlaybook.`,
  });

  const actionId = pb.repair_steps[0]?.action_id;
  const actionKnown = !!actionId && isKnownAction(actionId) && pb.allowed_actions.includes(actionId);
  out.push({ name: "action_exists_in_registry", passed: actionKnown, detail: actionKnown ? `${actionId} معروفٌ في الكود ومسموحٌ به في هذا الـPlaybook.` : "الإجراء غير معروفٍ/غير مسموحٍ به." });

  let actionEnabled = false;
  if (actionId) {
    const { data: reg } = await admin.from("safe_action_registry").select("enabled,risk_level").eq("action_id", actionId).maybeSingle();
    actionEnabled = !!reg?.enabled;
  }
  out.push({ name: "action_enabled", passed: actionEnabled, detail: actionEnabled ? "مفعَّلٌ في safe_action_registry." : "غير مفعَّلٍ أو غير موجود في safe_action_registry." });

  return out;
}

// القسم 9/10: سقف محاولاتٍ لكل Playbook × incident + cooldown مستقلّين
// عن preconditions أعلاه (preconditions تفحص شكل الحادثة نفسها، هذان
// يفحصان تاريخ محاولات الإصلاح الذاتي تحديداً).
export async function checkRateLimitAndCooldown(
  admin: any, pb: PlaybookRow, incidentId: string | null,
): Promise<{ rateLimited: boolean; attemptsSoFar: number; cooldownActive: boolean; cooldownUntil: string | null }> {
  if (!incidentId) return { rateLimited: false, attemptsSoFar: 0, cooldownActive: false, cooldownUntil: null };
  const { count } = await admin.from("repair_executions").select("repair_id", { count: "exact", head: true })
    .eq("incident_id", incidentId).eq("playbook_id", pb.playbook_id);
  const attemptsSoFar = count || 0;

  const since = new Date(Date.now() - pb.cooldown_minutes * 60 * 1000).toISOString();
  const { data: recentRuns } = await admin.from("repair_executions")
    .select("started_at").eq("playbook_id", pb.playbook_id).gte("started_at", since)
    .in("status", ["WOULD_AUTO_HEAL", "SUCCEEDED", "FAILED", "VERIFICATION_FAILED", "ESCALATED"])
    .order("started_at", { ascending: false }).limit(1);
  const cooldownActive = !!(recentRuns && recentRuns.length);
  const cooldownUntil = cooldownActive ? new Date(new Date(recentRuns[0].started_at).getTime() + pb.cooldown_minutes * 60 * 1000).toISOString() : null;

  return { rateLimited: attemptsSoFar >= pb.max_attempts, attemptsSoFar, cooldownActive, cooldownUntil };
}

// القسم 11: القاطع (Circuit Breaker) — N فشلاً ضمن نافذة زمنية ⇒
// SELF_HEALING_PAUSED لهذا الـPlaybook حتى يستأنفه إنسان (لا مسار آلي
// لإعادة الإغلاق هنا إطلاقاً).
export async function checkCircuitBreaker(admin: any, pb: PlaybookRow): Promise<{ open: boolean; failuresInWindow: number }> {
  if (pb.circuit_state === "OPEN") return { open: true, failuresInWindow: -1 };
  const since = new Date(Date.now() - pb.circuit_breaker_window_minutes * 60 * 1000).toISOString();
  const { count } = await admin.from("repair_executions").select("repair_id", { count: "exact", head: true })
    .eq("playbook_id", pb.playbook_id).gte("started_at", since)
    .in("status", ["FAILED", "VERIFICATION_FAILED"]);
  const failures = count || 0;
  if (failures >= pb.circuit_breaker_threshold) {
    await admin.from("repair_playbooks").update({ circuit_state: "OPEN", circuit_opened_at: new Date().toISOString() }).eq("playbook_id", pb.playbook_id);
    return { open: true, failuresInWindow: failures };
  }
  return { open: false, failuresInWindow: failures };
}

// القسم 8: نطاق التأثير — محدودٌ صراحةً بواحدٍ من ثلاثة، وإلا تصعيدٌ فوري.
export function computeBlastRadius(pb: PlaybookRow, agentId: string): { scope: string; target: string; allowed: boolean } {
  const forbidden = new Set(["ALL_USERS", "ALL_DATABASE", "ALL_TEACHERS", "FINANCE", "AUTHENTICATION"]);
  const allowed = ["ONE_FUNCTION", "ONE_AGENT", "ONE_JOB"].includes(pb.affected_scope) && !forbidden.has(pb.affected_scope);
  return { scope: pb.affected_scope, target: agentId, allowed };
}

// القسم 12: بوّابة الإيقاف الطارئ — عامّ، أو Playbook بعينه، أو وكيلٌ بعينه.
export async function isSelfHealingBlocked(admin: any, pb: PlaybookRow, agentId: string): Promise<{ blocked: boolean; reason: string | null }> {
  if (!pb.enabled || pb.mode === "DISABLED") return { blocked: true, reason: "الـPlaybook معطَّلٌ (enabled=false أو mode=DISABLED)." };
  if (pb.mode === "PAUSED") return { blocked: true, reason: "الـPlaybook متوقّفٌ يدوياً (PAUSED)." };
  const { data: ctl } = await admin.from("self_healing_controls").select("*").eq("control_id", "global").maybeSingle();
  if (ctl && ctl.self_healing_enabled === false) return { blocked: true, reason: `الإصلاح الذاتي مُعطَّلٌ عامّاً: ${ctl.disabled_reason || "بلا سببٍ مذكور"}.` };
  const disabledAgents: string[] = (ctl?.disabled_agents || []) as string[];
  if (disabledAgents.includes(agentId)) return { blocked: true, reason: `الإصلاح الذاتي معطَّلٌ تحديداً للوكيل ${agentId}.` };
  return { blocked: false, reason: null };
}

// ═══ نقطة الدخول الوحيدة الحيّة فعلياً في هذه المرحلة: تقييم Shadow Mode.
// Detect → Diagnose (مُنجَزٌ سلفاً قبل هذا النداء) → Match Playbook →
// Decide، بلا أي تنفيذٍ فعلي مهما كانت النتيجة (القسم 14). ═══
export async function evaluateShadow(
  admin: any,
  diag: { diagnosis_id: string; incident_id: string; confidence: number | null; recommended_action_id: string | null; risk_level: string | null },
  incident: { component: string; source_agent?: string | null },
  runsSummary: { agent_id: string; consecutive_failures: number; distinct_errors: string[]; last_success_at: string | null },
): Promise<DecisionResult & { playbook_id: string | null; execution_id?: string }> {
  const pattern = matchIncidentPattern({ agent_id: runsSummary.agent_id, consecutive_failures: runsSummary.consecutive_failures, distinct_errors: runsSummary.distinct_errors });
  const blastEmpty = { scope: "NONE", target: runsSummary.agent_id };
  if (!pattern) {
    return { status: "NO_PLAYBOOK_MATCH", preconditions: [], blast_radius: blastEmpty, playbook_id: null, reason: "لا نمط حادثةٍ معروف يطابق أدلّة هذا التشخيص." };
  }

  const { data: pb } = await admin.from("repair_playbooks").select("*").eq("incident_pattern", pattern).eq("enabled", true).maybeSingle();
  if (!pb) {
    return { status: "NO_PLAYBOOK_MATCH", preconditions: [], blast_radius: blastEmpty, playbook_id: null, reason: `نمطٌ معروف (${pattern}) لكن لا Playbook مسجَّلٌ ومفعَّلٌ يطابقه.` };
  }

  const blast = computeBlastRadius(pb, runsSummary.agent_id);
  if (!blast.allowed) {
    return { status: "RISK_BLOCKED", preconditions: [], blast_radius: blast, playbook_id: pb.playbook_id, reason: `نطاق تأثيرٍ ممنوعٌ للإصلاح الآلي: ${blast.scope}.` };
  }

  // القسم 12: الإيقاف الطارئ أولاً — قبل أي فحصٍ آخر مكلف.
  const blocked = await isSelfHealingBlocked(admin, pb, runsSummary.agent_id);
  if (blocked.blocked) {
    return { status: "DISABLED", preconditions: [], blast_radius: blast, playbook_id: pb.playbook_id, reason: blocked.reason || undefined };
  }

  // القسم 11: القاطع.
  const circuit = await checkCircuitBreaker(admin, pb);
  if (circuit.open) {
    return { status: "CIRCUIT_OPEN", preconditions: [], blast_radius: blast, playbook_id: pb.playbook_id, reason: `القاطع مفتوحٌ لهذا الـPlaybook (${circuit.failuresInWindow >= 0 ? circuit.failuresInWindow + " فشلاً ضمن النافذة" : "مفتوحٌ سلفاً"}) — لا إصلاحٌ آليٌّ حتى يستأنفه مشرف.` };
  }

  // القسم 6: عتبة الثقة الخاصّة بالـPlaybook (LOW=90+ هنا دوماً بحكم القسم 7).
  const confidence = diag.confidence ?? 0;
  if (confidence < pb.minimum_confidence) {
    return { status: "ESCALATED", preconditions: [], blast_radius: blast, playbook_id: pb.playbook_id, reason: `الثقة ${confidence}% أقل من الحدّ الأدنى ${pb.minimum_confidence}% لهذا الـPlaybook.` };
  }

  // القسم 7: Phase 3 لا يُصلِح آلياً غير LOW إطلاقاً — بلا استثناء مهما
  // كانت الثقة، حتى لو كان mode='AUTO' نظرياً (لا يوجد اليوم أصلاً).
  if (pb.risk_level !== "LOW") {
    return { status: "RISK_BLOCKED", preconditions: [], blast_radius: blast, playbook_id: pb.playbook_id, reason: `خطورة الـPlaybook ${pb.risk_level} — Phase 3 لا يُصلِح آلياً إلا LOW، يتطلّب موافقةً بشرية عبر مسار Phase 2 القائم.` };
  }

  // القسم 9/10: السقف والـcooldown.
  const rl = await checkRateLimitAndCooldown(admin, pb, diag.incident_id);
  if (rl.rateLimited) {
    return { status: "RATE_LIMITED", preconditions: [], blast_radius: blast, playbook_id: pb.playbook_id, reason: `تجاوز سقف ${pb.max_attempts} محاولاتٍ لهذه الحادثة على هذا الـPlaybook.` };
  }
  if (rl.cooldownActive) {
    return { status: "COOLDOWN_ACTIVE", preconditions: [], blast_radius: blast, playbook_id: pb.playbook_id, reason: `نفس نمط الفشل تكرَّر ضمن نافذة التهدئة (${pb.cooldown_minutes} دقيقة) — لا إعادة إصلاحٍ، تصعيدٌ بدلاً منه حتى ${rl.cooldownUntil}.` };
  }

  // القسم 5: الشروط المسبقة — إن فشل أيٌّ منها، لا إصلاح مهما كانت الثقة عالية.
  const preconditions = await checkPreconditions(admin, pb, {
    agentId: runsSummary.agent_id, consecutiveFailures: runsSummary.consecutive_failures,
    distinctErrors: runsSummary.distinct_errors, lastSuccessAt: runsSummary.last_success_at,
    incidentComponent: incident.component,
  });
  const failedPre = preconditions.filter((p) => !p.passed);
  if (failedPre.length) {
    return {
      status: "PRECONDITION_FAILED", preconditions, blast_radius: blast, playbook_id: pb.playbook_id,
      reason: `شروطٌ مسبقة لم تتحقّق: ${failedPre.map((p) => p.name).join("، ")}.`,
    };
  }

  // كل البوّابات اجتِيزت — في وضع SHADOW (وهو الوضع الوحيد الحيّ اليوم على
  // أي Playbook): "كان سيُصلِح لو AUTO" فقط، بلا أي تنفيذٍ فعلي (القسم 14/15).
  if (pb.mode === "SHADOW") {
    return { status: "WOULD_AUTO_HEAL", preconditions, blast_radius: blast, playbook_id: pb.playbook_id, reason: `كل الشروط اجتِيزت — كان سيُنفَّذ ${pb.repair_steps[0]?.action_id} لو كان الـPlaybook في وضع AUTO.` };
  }

  // pb.mode === 'AUTO': لا صفٍّ اليوم يحمل هذه القيمة (كل الـPlaybooks
  // تُدخَل SHADOW في الهجرة) — الفرع موجودٌ للاكتمال البنيوي والاختبار
  // المستقبلي فقط، غير مُفعَّلٍ إنتاجياً في هذه المرحلة إطلاقاً.
  return { status: "AUTO_MODE_NOT_ACTIVATED_IN_PHASE3", preconditions, blast_radius: blast, playbook_id: pb.playbook_id, reason: "القسم 15: لا Playbook يُفعَّل بوضع AUTO ضمن Phase 3 — هذا الفرع غير قابلٍ للوصول عملياً اليوم." };
}

// القسم 13: Dry Run — يعرض الخطوة المُتوقَّعة بلا أي تنفيذٍ فعلي، بصرف
// النظر عن mode الحالي للـPlaybook (أداة تفتيشٍ يدوية للمشرف).
export function dryRun(pb: PlaybookRow): { would_execute: string[]; rollback_strategy: string; verification_steps: unknown } {
  return {
    would_execute: pb.repair_steps.map((s) => `${s.action_id}(${JSON.stringify(s.params_template)})`),
    rollback_strategy: pb.rollback_strategy,
    verification_steps: (pb as any).verification_steps,
  };
}

// القسم 16: بوّابة الانتقال إلى AUTO — تُوثَّق هنا كدالّة فحصٍ حقيقية
// (لا ملاحظة نصّية فقط)، تُستخدَم من واجهة الإدارة كقائمة تحقّقٍ للقراءة،
// لا لتفعيل أي شيءٍ تلقائياً. لا مسار كودٍ يستدعيها لتغيير mode فعلياً.
export interface AutoModeGateCheck { criterion: string; met: boolean; detail: string }
export async function autoModeGateStatus(admin: any, playbookId: string): Promise<AutoModeGateCheck[]> {
  const { data: pb } = await admin.from("repair_playbooks").select("*").eq("playbook_id", playbookId).maybeSingle();
  if (!pb) return [{ criterion: "playbook_exists", met: false, detail: "الـPlaybook غير موجود." }];
  const { data: shadowRuns } = await admin.from("repair_executions").select("status").eq("playbook_id", playbookId);
  const shadowSuccesses = (shadowRuns || []).filter((r: any) => r.status === "WOULD_AUTO_HEAL").length;
  const shadowFailures = (shadowRuns || []).filter((r: any) => ["PRECONDITION_FAILED", "RISK_BLOCKED", "COOLDOWN_ACTIVE", "RATE_LIMITED", "CIRCUIT_OPEN"].includes(r.status)).length;
  return [
    { criterion: "playbook_succeeded_in_shadow_mode", met: shadowSuccesses >= 5, detail: `${shadowSuccesses} حالة WOULD_AUTO_HEAL مسجَّلة (المطلوب: ٥ على الأقل قبل الاعتبار جاهزاً — رقمٌ استرشاديٌّ، القرار النهائي بشري).` },
    { criterion: "high_diagnosis_confidence", met: pb.minimum_confidence >= 90, detail: `الحدّ الأدنى المُعدّ: ${pb.minimum_confidence}%.` },
    { criterion: "preconditions_working", met: (shadowRuns || []).length > 0, detail: (shadowRuns || []).length ? "شروطٌ مسبقة نُفِّذت فعلياً في تنفيذاتٍ حقيقية." : "لا تنفيذاتٍ Shadow بعد لإثبات عمل الشروط المسبقة." },
    { criterion: "verification_defined", met: !!pb.repair_steps?.length, detail: "verify() معرَّفةٌ في opsActionRegistry.ts لكل إجراءٍ ضمن repair_steps." },
    { criterion: "rollback_known", met: !!pb.rollback_strategy, detail: pb.rollback_strategy },
    { criterion: "max_attempts_set", met: pb.max_attempts >= 1, detail: `max_attempts=${pb.max_attempts}` },
    { criterion: "cooldown_set", met: pb.cooldown_minutes >= 0, detail: `cooldown_minutes=${pb.cooldown_minutes}` },
    { criterion: "circuit_breaker_working", met: pb.circuit_breaker_threshold >= 1, detail: `threshold=${pb.circuit_breaker_threshold} ضمن ${pb.circuit_breaker_window_minutes} دقيقة، مع ${shadowFailures} حالة فشلٍ/تصعيدٍ مسجَّلة تاريخياً لاختبار المسار.` },
    { criterion: "audit_logging_working", met: true, detail: "كل تقييمٍ يُسجَّل في repair_executions (evidence_snapshot/preconditions_result/blast_radius) بصرف النظر عن النتيجة." },
  ];
}

// ═══ مسار AUTO المبنيّ في الكود — القسم 17/18/19/22 (البناء داخل نطاق
// هذه المرحلة، التفعيل خارجه). لا يُستدعى من أي مسار ops-actions حيّ
// اليوم؛ موجودٌ فقط ليكون جاهزاً حرفياً للمراجعة والاختبار البشري لاحقاً
// دون كتابة كودٍ إضافي وقت تفعيل AUTO. ينفّذ فقط repair_steps[0] —
// Playbook بخطوةٍ واحدة حصراً في هذه المرحلة (لا سلسلة خطواتٍ متعددة). ═══
export async function executeAutoRepair_NOT_ACTIVATED_IN_PHASE3(
  admin: any, pb: PlaybookRow, evidence: Record<string, unknown>,
): Promise<{ status: string; execution_result: unknown; verification_result: unknown }> {
  const step = pb.repair_steps[0];
  if (!step || !isKnownAction(step.action_id)) {
    return { status: "FAILED", execution_result: null, verification_result: { reason: "خطوةٌ غير معروفة — لا تنفيذ." } };
  }
  const impl = ACTIONS[step.action_id];
  const params = { ...step.params_template, agent_id: (evidence as any).agent_id };
  const startedAt = new Date().toISOString();
  let execResult;
  try { execResult = await impl.execute(admin, params); } catch (e) { execResult = { ok: false, error: String(e) }; }
  if (!execResult.ok) return { status: "FAILED", execution_result: execResult, verification_result: null };
  let verification;
  try { verification = await impl.verify(admin, params, execResult, startedAt); } catch (e) { verification = { status: "INCONCLUSIVE", detail: { reason: String(e) } }; }
  const status = verification.status === "PASSED" ? "SUCCEEDED" : "VERIFICATION_FAILED";
  return { status, execution_result: execResult, verification_result: verification };
}
