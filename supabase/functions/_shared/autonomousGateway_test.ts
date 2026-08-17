// ═══ اختبارات Phase 3.5-A لبوّابة التنفيذ الآلي — Deno.test بأدوات وهمية
// (Fake Supabase client)، لا اتصال حقيقي بقاعدة بيانات. لا اختبار Auto-
// Heal حقيقي ضد الإنتاج إطلاقاً — كل شيء هنا محاكاةٌ محلّية بحتة.
//
// تشغيلٌ محتمل: `deno test supabase/functions/_shared/autonomousGateway_test.ts`
// — لم يُنفَّذ فعلياً في هذه الجلسة (Deno غير مثبَّتٍ في هذه البيئة،
// تحقّقٌ حيّ: `which deno` أعاد لا نتيجة) — الاختبارات مُستنتَجةٌ من قراءة
// الكود بعناية فقط (STATIC REASONING)، لا DEPLOYMENT/LIVE VERIFIED.
//
// deno-lint-ignore-file no-explicit-any
import { assertEquals } from "https://deno.land/std@0.208.0/testing/asserts.ts";
import {
  gate0_incidentValid, gate1_diagnosisValid, gate2_playbookMatch, gate3_globalKillSwitch,
  gate4_playbookAutoMode, gate5_circuitBreaker, gate6_confidenceThreshold, gate7_riskLowOnly,
  gate8_rateLimitCooldown, gate9_preconditions, gate10_actionRegistryValidation,
  gate11_atomicClaim, gate12_idempotencyCheck, executeAutonomous,
} from "./autonomousGateway.ts";

// ─── محاكاة Supabase client: جدولٌ ثابتٌ من البيانات، سلسلة استعلامٍ ───
function makeFakeAdmin(tables: Record<string, any[]>, opts: { rpcResults?: Record<string, any>; insertCapture?: any[] } = {}) {
  const inserted = opts.insertCapture || [];
  function builder(tableName: string) {
    let rows = [...(tables[tableName] || [])];
    let single = false;
    let count = false;
    const state: any = { filters: [] as [string, string, any][] };
    const api: any = {
      select(_cols?: string, o?: any) { if (o?.count) count = true; return api; },
      eq(col: string, val: any) { rows = rows.filter((r) => r[col] === val); return api; },
      neq(col: string, val: any) { rows = rows.filter((r) => r[col] !== val); return api; },
      gte(col: string, val: any) { rows = rows.filter((r) => r[col] >= val); return api; },
      in(col: string, vals: any[]) { rows = rows.filter((r) => vals.includes(r[col])); return api; },
      order() { return api; },
      limit(n: number) { rows = rows.slice(0, n); return api; },
      maybeSingle() { single = true; return Promise.resolve({ data: rows[0] || null, error: null }); },
      then(resolve: any) { resolve({ data: rows, count: count ? rows.length : undefined, error: null }); },
      insert(payload: any) {
        const row = { ...payload, repair_id: crypto.randomUUID() };
        inserted.push(row);
        (tables[tableName] ||= []).push(row);
        return { select: () => ({ maybeSingle: () => Promise.resolve({ data: row, error: null }) }) };
      },
      update(_payload: any) { return { eq: () => ({ select: () => ({ maybeSingle: () => Promise.resolve({ data: null, error: null }) }) }) }; },
    };
    return api;
  }
  return {
    from: builder,
    rpc(fn: string, args: any) {
      const r = opts.rpcResults?.[fn];
      if (typeof r === "function") return Promise.resolve(r(args));
      return Promise.resolve(r ?? { data: null, error: null });
    },
    _inserted: inserted,
  };
}

const BASE_PB = {
  playbook_id: "retry_monitor_known_timeout", name: "x", incident_pattern: "KNOWN_MONITOR_REPEATED_FAILURE",
  diagnosis_requirements: { min_consecutive_failures: 3 }, minimum_confidence: 90, risk_level: "LOW",
  allowed_agents: ["system-health-check"], allowed_actions: ["rerun_monitor_agent"], preconditions: [],
  repair_steps: [{ action_id: "rerun_monitor_agent", params_template: {} }], rollback_strategy: "idempotent",
  max_attempts: 2, cooldown_minutes: 30, circuit_breaker_threshold: 3, circuit_breaker_window_minutes: 60,
  affected_scope: "ONE_AGENT", mode: "SHADOW", circuit_state: "CLOSED", requires_human_approval: false, enabled: true,
};

Deno.test("Gate 3: global self-healing OFF blocks", async () => {
  const admin = makeFakeAdmin({ self_healing_controls: [{ control_id: "global", self_healing_enabled: false, disabled_agents: [] }] });
  const r = await gate3_globalKillSwitch(admin, "system-health-check");
  assertEquals(r.passed, false);
  assertEquals(r.status, "DISABLED");
});

Deno.test("Gate 4: playbook mode SHADOW blocks (the actual disable mechanism)", () => {
  const r = gate4_playbookAutoMode(BASE_PB as any);
  assertEquals(r.passed, false);
  assertEquals(r.status, "DISABLED");
});

Deno.test("Gate 4: playbook disabled=false blocks even if mode were AUTO", () => {
  const r = gate4_playbookAutoMode({ ...BASE_PB, mode: "AUTO", enabled: false } as any);
  assertEquals(r.passed, false);
});

Deno.test("Gate 4: passes only when enabled=true AND mode==='AUTO'", () => {
  const r = gate4_playbookAutoMode({ ...BASE_PB, mode: "AUTO", enabled: true } as any);
  assertEquals(r.passed, true);
});

Deno.test("Gate 7: risk HIGH blocks", () => {
  const r = gate7_riskLowOnly({ ...BASE_PB, risk_level: "HIGH" } as any);
  assertEquals(r.passed, false);
  assertEquals(r.status, "RISK_BLOCKED");
});

Deno.test("Gate 6: confidence below minimum blocks", () => {
  const r = gate6_confidenceThreshold(BASE_PB as any, 50);
  assertEquals(r.passed, false);
  assertEquals(r.status, "ESCALATED");
});

Deno.test("Gate 6: confidence null treated as 0, blocks", () => {
  const r = gate6_confidenceThreshold(BASE_PB as any, null);
  assertEquals(r.passed, false);
});

Deno.test("Gate 5: circuit_state OPEN blocks without extra query", async () => {
  const admin = makeFakeAdmin({});
  const r = await gate5_circuitBreaker(admin, { ...BASE_PB, circuit_state: "OPEN" } as any);
  assertEquals(r.passed, false);
  assertEquals(r.status, "CIRCUIT_OPEN");
});

Deno.test("Gate 8: max_attempts reached blocks (RATE_LIMITED)", async () => {
  const admin = makeFakeAdmin({
    repair_executions: [{ repair_id: "1", incident_id: "inc1", playbook_id: BASE_PB.playbook_id, started_at: new Date().toISOString(), status: "SUCCEEDED" }],
  });
  const r = await gate8_rateLimitCooldown(admin, { ...BASE_PB, max_attempts: 1 } as any, "inc1");
  assertEquals(r.passed, false);
  assertEquals(r.status, "RATE_LIMITED");
});

Deno.test("Gate 8: cooldown active blocks", async () => {
  const admin = makeFakeAdmin({
    repair_executions: [{ repair_id: "1", incident_id: "incX", playbook_id: BASE_PB.playbook_id, started_at: new Date().toISOString(), status: "WOULD_AUTO_HEAL" }],
  });
  const r = await gate8_rateLimitCooldown(admin, BASE_PB as any, "inc1");
  assertEquals(r.passed, false);
  assertEquals(r.status, "COOLDOWN_ACTIVE");
});

Deno.test("Gate 9: failed precondition blocks (no last success)", async () => {
  const admin = makeFakeAdmin({ ops_incidents: [], deployment_log: [{ deployed_at: new Date(Date.now() - 100 * 24 * 3600 * 1000).toISOString() }] });
  const r = await gate9_preconditions(admin, BASE_PB as any, {
    incidentId: "i1", diagnosisId: "d1", agentId: "system-health-check",
    consecutiveFailures: 5, distinctErrors: ["timeout"], lastSuccessAt: null, incidentComponent: "monitor-x",
  });
  assertEquals(r.passed, false);
  assertEquals(r.status, "PRECONDITION_FAILED");
});

Deno.test("Gate 10: unknown action rejected", async () => {
  const admin = makeFakeAdmin({});
  const r = await gate10_actionRegistryValidation(admin, BASE_PB as any, "not_a_real_action", {}, "system-health-check");
  assertEquals(r.passed, false);
  assertEquals(r.status, "ACTION_VALIDATION_FAILED");
});

Deno.test("Gate 10: action not in playbook allowed_actions rejected", async () => {
  const admin = makeFakeAdmin({});
  const r = await gate10_actionRegistryValidation(admin, { ...BASE_PB, allowed_actions: [] } as any, "rerun_monitor_agent", {}, "system-health-check");
  assertEquals(r.passed, false);
});

Deno.test("Gate 10: action disabled in safe_action_registry rejected", async () => {
  const admin = makeFakeAdmin({ safe_action_registry: [{ action_id: "rerun_monitor_agent", enabled: false, risk_level: "LOW", allowed_agents: [], input_schema: {}, verification_strategy: "x" }] });
  const r = await gate10_actionRegistryValidation(admin, BASE_PB as any, "rerun_monitor_agent", {}, "system-health-check");
  assertEquals(r.passed, false);
});

Deno.test("Gate 10: unauthorized agent (not in action's allowed_agents) rejected", async () => {
  const admin = makeFakeAdmin({ safe_action_registry: [{ action_id: "rerun_monitor_agent", enabled: true, risk_level: "LOW", allowed_agents: ["other-agent"], input_schema: {}, verification_strategy: "x" }] });
  const r = await gate10_actionRegistryValidation(admin, BASE_PB as any, "rerun_monitor_agent", {}, "system-health-check");
  assertEquals(r.passed, false);
});

Deno.test("Gate 10: passes with matching enabled LOW-risk registry row", async () => {
  const admin = makeFakeAdmin({ safe_action_registry: [{ action_id: "rerun_monitor_agent", enabled: true, risk_level: "LOW", allowed_agents: [], input_schema: {}, verification_strategy: "checks agent_runs" }] });
  const r = await gate10_actionRegistryValidation(admin, BASE_PB as any, "rerun_monitor_agent", {}, "system-health-check");
  assertEquals(r.passed, true);
});

Deno.test("Gate 11: duplicate claim attempt fails (rpc returns null)", async () => {
  const admin = makeFakeAdmin({}, { rpcResults: { claim_incident_for_repair: { data: null, error: null } } });
  const r = await gate11_atomicClaim(admin, "inc1", BASE_PB.playbook_id);
  assertEquals(r.passed, false);
  assertEquals(r.status, "CLAIM_FAILED");
});

Deno.test("Gate 11: successful claim returns claimId", async () => {
  const admin = makeFakeAdmin({}, { rpcResults: { claim_incident_for_repair: { data: "claim-abc", error: null } } });
  const r = await gate11_atomicClaim(admin, "inc1", BASE_PB.playbook_id);
  assertEquals(r.passed, true);
  assertEquals(r.claimId, "claim-abc");
});

Deno.test("Gate 12: duplicate idempotency key blocked", async () => {
  const admin = makeFakeAdmin({ repair_executions: [{ repair_id: "existing", incident_id: "inc1", playbook_id: BASE_PB.playbook_id, attempt_number: 1 }] });
  const r = await gate12_idempotencyCheck(admin, "inc1", BASE_PB.playbook_id, 1);
  assertEquals(r.passed, false);
  assertEquals(r.status, "DUPLICATE_EXECUTION_BLOCKED");
});

Deno.test("Gate 12: fresh key passes", async () => {
  const admin = makeFakeAdmin({ repair_executions: [] });
  const r = await gate12_idempotencyCheck(admin, "inc1", BASE_PB.playbook_id, 1);
  assertEquals(r.passed, true);
});

Deno.test("Gate 0: unknown incident_id rejected", async () => {
  const admin = makeFakeAdmin({ ops_incidents: [] });
  const r = await gate0_incidentValid(admin, "does-not-exist");
  assertEquals(r.passed, false);
  assertEquals(r.status, "INVALID_INCIDENT");
});

Deno.test("Gate 0: RESOLVED incident rejected", async () => {
  const admin = makeFakeAdmin({ ops_incidents: [{ id: "i1", status: "RESOLVED", component: "x" }] });
  const r = await gate0_incidentValid(admin, "i1");
  assertEquals(r.passed, false);
});

Deno.test("Gate 1: diagnosis not COMPLETED rejected", async () => {
  const admin = makeFakeAdmin({ ops_diagnoses: [{ diagnosis_id: "d1", incident_id: "i1", diagnosis_status: "ANALYZING" }] });
  const r = await gate1_diagnosisValid(admin, "d1", "i1");
  assertEquals(r.passed, false);
  assertEquals(r.status, "INVALID_DIAGNOSIS");
});

Deno.test("Gate 1: diagnosis for a different incident rejected", async () => {
  const admin = makeFakeAdmin({ ops_diagnoses: [{ diagnosis_id: "d1", incident_id: "OTHER", diagnosis_status: "COMPLETED" }] });
  const r = await gate1_diagnosisValid(admin, "d1", "i1");
  assertEquals(r.passed, false);
});

Deno.test("Gate 2: no known pattern -> NO_PLAYBOOK_MATCH", async () => {
  const admin = makeFakeAdmin({});
  const r = await gate2_playbookMatch(admin, { agent_id: "x", consecutive_failures: 1, distinct_errors: ["a", "b"] });
  assertEquals(r.passed, false);
  assertEquals(r.status, "NO_PLAYBOOK_MATCH");
});

// ─── اختبار end-to-end: executeAutonomous يتوقّف دوماً عند Gate 4 لأن كل
// Playbook حيّ اليوم mode='SHADOW' — هذا هو الدليل المُبرمَج على أن AUTO
// المستحيل بنيوياً، لا افتراضٌ فقط. ───
Deno.test("executeAutonomous: full pipeline stops at Gate 4 for a real SHADOW playbook (proves AUTO cannot fire today)", async () => {
  const inserted: any[] = [];
  const admin = makeFakeAdmin({
    ops_incidents: [{ id: "i1", status: "DETECTED", component: "monitor-x" }],
    ops_diagnoses: [{ diagnosis_id: "d1", incident_id: "i1", diagnosis_status: "COMPLETED", confidence: 95 }],
    repair_playbooks: [BASE_PB],   // mode: 'SHADOW' — كما في الإنتاج فعلياً
    self_healing_controls: [{ control_id: "global", self_healing_enabled: true, disabled_agents: [] }],
  }, { insertCapture: inserted });

  const result = await executeAutonomous(admin, {
    incidentId: "i1", diagnosisId: "d1", agentId: "system-health-check",
    consecutiveFailures: 5, distinctErrors: ["timeout"], lastSuccessAt: new Date().toISOString(),
  });

  assertEquals(result.status, "DISABLED");
  assertEquals(inserted.length, 1);
  assertEquals(inserted[0].status, "DISABLED");
  assertEquals(inserted[0].actor, "autonomous_execution_gateway");
});
