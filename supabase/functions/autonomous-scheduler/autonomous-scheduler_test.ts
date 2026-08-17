// ═══ اختبارات Phase 3.5-B لجدولة بوّابة التنفيذ الآلي — Deno.test بأدوات
// وهمية (Fake Supabase client)، لا اتصال حقيقي بقاعدة بيانات ولا شبكة
// حقيقية (fetch الخاص بـgetOrCreateDiagnosis يُتفادى بتوفير تشخيصٍ مكتملٍ
// موجودٍ سلفاً في كل الحالات — لا اختبار هنا يعتمد على استدعاء ops-actions
// شبكياً فعلياً). نفس أسلوب autonomousGateway_test.ts تماماً.
//
// تشغيلٌ: `deno test --no-check --allow-net supabase/functions/autonomous-scheduler/autonomous-scheduler_test.ts`
//
// deno-lint-ignore-file no-explicit-any
import { assertEquals, assert } from "https://deno.land/std@0.208.0/testing/asserts.ts";
import { runSchedulerCycle, BATCH_LIMIT } from "./index.ts";

// ─── محاكاة Supabase client — نفس نمط autonomousGateway_test.ts، مع دعم
// order/limit إضافيّين يستخدمهما هذا الملف. ───
function makeFakeAdmin(tables: Record<string, any[]>, opts: { rpcResults?: Record<string, any>; insertCapture?: any[] } = {}) {
  const inserted = opts.insertCapture || [];
  function builder(tableName: string) {
    let rows = [...(tables[tableName] || [])];
    let count = false;
    const api: any = {
      select(_cols?: string, o?: any) { if (o?.count) count = true; return api; },
      eq(col: string, val: any) { rows = rows.filter((r) => r[col] === val); return api; },
      neq(col: string, val: any) { rows = rows.filter((r) => r[col] !== val); return api; },
      gte(col: string, val: any) { rows = rows.filter((r) => r[col] >= val); return api; },
      in(col: string, vals: any[]) { rows = rows.filter((r) => vals.includes(r[col])); return api; },
      order() { return api; },
      limit(n: number) { rows = rows.slice(0, n); return api; },
      maybeSingle() { return Promise.resolve({ data: rows[0] || null, error: null }); },
      then(resolve: any) { resolve({ data: rows, count: count ? rows.length : undefined, error: null }); },
      insert(payload: any) {
        const row = { ...payload, repair_id: crypto.randomUUID(), run_id: crypto.randomUUID() };
        inserted.push(row);
        (tables[tableName] ||= []).push(row);
        return {
          select: () => ({ maybeSingle: () => Promise.resolve({ data: row, error: null }) }),
        };
      },
      update(payload: any) {
        return {
          eq: (col: string, val: any) => {
            (tables[tableName] || []).forEach((r) => { if (r[col] === val) Object.assign(r, payload); });
            return { select: () => ({ maybeSingle: () => Promise.resolve({ data: null, error: null }) }) };
          },
        };
      },
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
    _tables: tables,
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

const GLOBAL_ENABLED = { control_id: "global", self_healing_enabled: true, disabled_agents: [] };
const GLOBAL_DISABLED = { control_id: "global", self_healing_enabled: false, disabled_agents: [], disabled_reason: "test" };

function makeIncident(id: string, component = "monitor-x") {
  return { id, status: "DETECTED", component, last_seen_at: new Date().toISOString(), first_seen_at: new Date().toISOString() };
}

function makeDiagnosis(id: string, incidentId: string, agentId = "system-health-check", failures = 5) {
  return {
    diagnosis_id: id, incident_id: incidentId, diagnosis_status: "COMPLETED", confidence: 95,
    completed_at: new Date().toISOString(),
    evidence: [{ source: "get_recent_agent_runs", value: { agent_id: agentId, consecutive_failures: failures, distinct_errors: ["timeout"], last_success_at: new Date().toISOString() } }],
  };
}

// ─── (A) لا حوادث مؤهَّلة → خروجٌ آمن، سجلّ scheduler_runs بعدّادات صفرية، لا نداء بوّابة ───
Deno.test("(A) no eligible incidents: exits safely, logs zero-count scheduler_runs row, no gateway call", async () => {
  const admin = makeFakeAdmin({
    self_healing_controls: [GLOBAL_ENABLED],
    ops_incidents: [], // لا حوادث إطلاقاً
  });
  const result = await runSchedulerCycle(admin, "https://example.test", "svc-key");
  assertEquals(result.ok, true);
  assertEquals(result.incidents_scanned, 0);
  assertEquals(result.incidents_claimed, 0);
  assertEquals(result.incidents_evaluated, 0);
  const runsRow = admin._tables.scheduler_runs[0];
  assertEquals(runsRow.status, "COMPLETED");
  assertEquals(runsRow.incidents_claimed, 0);
  // لا صفوف repair_executions (البوّابة لم تُستدعَ إطلاقاً)
  assertEquals((admin._tables.repair_executions || []).length, 0);
});

// ─── (B) حادثةٌ مؤهَّلةٌ واحدة → ادّعاءٌ ناجح → البوّابة تُستدعى → نتيجة
//     SHADOW مسجَّلة → لا تنفيذٍ فعلي (mode='SHADOW' يوقف عند Gate 4) ───
Deno.test("(B) one eligible incident: claim succeeds, gateway called, SHADOW outcome recorded, no real execution", async () => {
  const diag = makeDiagnosis("d1", "i1");
  const admin = makeFakeAdmin({
    self_healing_controls: [GLOBAL_ENABLED],
    ops_incidents: [makeIncident("i1")],
    ops_diagnoses: [diag],
    repair_playbooks: [BASE_PB],
  }, { rpcResults: { claim_incident_for_repair: { data: "claim-1", error: null } } });

  const result = await runSchedulerCycle(admin, "https://example.test", "svc-key");
  assertEquals(result.ok, true);
  assertEquals(result.incidents_claimed, 1);
  assertEquals(result.incidents_evaluated, 1);
  // executeAutonomous يتوقّف عند Gate 4 (mode='SHADOW') ⇒ status DISABLED،
  // لا SUCCEEDED ولا استدعاء ACTIONS[...] فعلي إطلاقاً.
  const exec = admin._tables.repair_executions.find((r: any) => r.incident_id === "i1");
  assert(exec, "يجب تسجيل تنفيذٍ واحدٍ على الأقل لهذه الحادثة");
  assertEquals(exec.status, "DISABLED");
  assertEquals(exec.actor, "autonomous_execution_gateway");
  assert(exec.status !== "SUCCEEDED", "لا يجوز أبداً أن ينجح تنفيذٌ فعلي في هذه المرحلة");
});

// ─── (C) محاكاة تشغيلتين متزامنتين تحاولان ادّعاء نفس الحادثة — فقط
//     واحدةٌ تنجح؛ نُحاكي هذا بجعل claim_incident_for_repair يُعيد قيمةً
//     مرّةً ثم null، ونتحقّق أن الجدولة تتخطّى بصمتٍ دون إعادة محاولة. ───
Deno.test("(C) two concurrent claim attempts on the same incident: only one succeeds, the other is skipped", async () => {
  const diag = makeDiagnosis("d1", "i1");
  let calls = 0;
  const admin = makeFakeAdmin({
    self_healing_controls: [GLOBAL_ENABLED],
    ops_incidents: [makeIncident("i1")],
    ops_diagnoses: [diag],
    repair_playbooks: [BASE_PB],
  }, {
    rpcResults: {
      claim_incident_for_repair: () => {
        calls += 1;
        return calls === 1 ? { data: "claim-first", error: null } : { data: null, error: null };
      },
    },
  });

  const first = await runSchedulerCycle(admin, "https://example.test", "svc-key");
  assertEquals(first.incidents_claimed, 1);

  const second = await runSchedulerCycle(admin, "https://example.test", "svc-key");
  assertEquals(second.incidents_claimed, 0); // الادّعاء الثاني فشل (null) ⇒ تخطٍّ فوري، لا إعادة محاولة
});

// ─── (D) المفتاح العام مُعطَّل → SKIPPED_GLOBAL_DISABLED، لا ادّعاء ولا بوّابة ───
Deno.test("(D) global self_healing_enabled=false: logs SKIPPED_GLOBAL_DISABLED, no claim/gateway attempted", async () => {
  let claimCalled = false;
  const admin = makeFakeAdmin({
    self_healing_controls: [GLOBAL_DISABLED],
    ops_incidents: [makeIncident("i1")],
    ops_diagnoses: [makeDiagnosis("d1", "i1")],
    repair_playbooks: [BASE_PB],
  }, { rpcResults: { claim_incident_for_repair: () => { claimCalled = true; return { data: "x", error: null }; } } });

  const result = await runSchedulerCycle(admin, "https://example.test", "svc-key");
  assertEquals(result.skipped, "SKIPPED_GLOBAL_DISABLED");
  assertEquals(claimCalled, false);
  assertEquals((admin._tables.repair_executions || []).length, 0);
  const runsRow = admin._tables.scheduler_runs[0];
  assertEquals(runsRow.error_detail?.skipped, "SKIPPED_GLOBAL_DISABLED");
});

// ─── (E) mode='SHADOW' ⇒ WOULD_AUTO_HEAL نتيجةٌ منطقيةٌ ممكنة نظرياً (من
//     evaluateShadow لا executeAutonomous)، لكن executeAutonomous تحديداً
//     تتوقّف عند Gate 4 بحالة DISABLED — نُثبِت هنا أن لا مسار تنفيذٍ
//     فعلي يُؤخَذ مهما كانت النتيجة: execution_result يبقى غائباً. ───
Deno.test("(E) playbook mode=SHADOW: no real execution path taken (no execution_result on the recorded row)", async () => {
  const admin = makeFakeAdmin({
    self_healing_controls: [GLOBAL_ENABLED],
    ops_incidents: [makeIncident("i1")],
    ops_diagnoses: [makeDiagnosis("d1", "i1")],
    repair_playbooks: [BASE_PB], // mode: 'SHADOW'
  }, { rpcResults: { claim_incident_for_repair: { data: "claim-1", error: null } } });

  await runSchedulerCycle(admin, "https://example.test", "svc-key");
  const exec = admin._tables.repair_executions[0];
  assertEquals(exec.status, "DISABLED");
  assertEquals(exec.execution_result, undefined);
});

// ─── (F) البوّابة تُلقي استثناءً لحادثةٍ واحدة → الدورة تكتمل، عدّاد errors يزداد ───
Deno.test("(F) gateway throws for one incident: run still completes, errors counter incremented", async () => {
  const admin = makeFakeAdmin({
    self_healing_controls: [GLOBAL_ENABLED],
    ops_incidents: [makeIncident("i1")],
    ops_diagnoses: [makeDiagnosis("d1", "i1")],
    repair_playbooks: [BASE_PB],
  }, { rpcResults: { claim_incident_for_repair: { data: "claim-1", error: null } } });

  // الأهلية تجتاز طبيعياً (تستخدم incident الجاهز من المرشّحين، بلا إعادة
  // استعلامٍ عن ops_incidents). الاستدعاء الأول لِـ.from("ops_incidents")
  // هو جلب المرشّحين (يجب أن ينجح)؛ الاستدعاء الثاني يقع داخل
  // gate0_incidentValid ضمن executeAutonomous نفسها — هناك نُحاكي استثناءً
  // حقيقياً غير مُلتقَط داخل البوّابة، ليلتقطه try/catch حلقة المعالجة.
  let call = 0;
  const originalFrom = admin.from;
  admin.from = (t: string) => {
    if (t === "ops_incidents") {
      call += 1;
      if (call === 2) throw new Error("simulated_gateway_failure");
    }
    return originalFrom(t);
  };

  const result = await runSchedulerCycle(admin, "https://example.test", "svc-key");
  assertEquals(result.ok, true); // الدورة نفسها تكتمل بنجاح رغم فشل حادثةٍ واحدة
  assertEquals(result.errors, 1);
  assertEquals(result.incidents_claimed, 1); // الادّعاء نجح قبل أن يرمي gate0 داخل البوّابة
});

// ─── (G) حادثةٌ واحدة تفشل أثناء تجهيز الأهلية (استثناء) → الحوادث
//     التالية في نفس الدفعة تُعالَج رغم ذلك ───
Deno.test("(G) one incident's eligibility check throws: subsequent incidents in the same batch are still processed", async () => {
  const diagGood = makeDiagnosis("d2", "i2");
  const admin = makeFakeAdmin({
    self_healing_controls: [GLOBAL_ENABLED],
    ops_incidents: [makeIncident("i1"), makeIncident("i2")],
    ops_diagnoses: [diagGood], // i1 عمداً بلا تشخيصٍ صالح لإثارة مسارٍ مختلف
    repair_playbooks: [BASE_PB],
  }, { rpcResults: { claim_incident_for_repair: { data: "claim-x", error: null } } });

  // اجعل .from("ops_diagnoses") يرمي فقط عند البحث عن تشخيص i1 تحديداً
  // (نُحاكي عبر عدّاد استدعاءات) — الاستدعاء الأول (لِـi1) يرمي، الثاني (لِـi2) يعمل طبيعياً.
  let call = 0;
  const originalFrom = admin.from;
  admin.from = (t: string) => {
    if (t === "ops_diagnoses") {
      call += 1;
      if (call === 1) throw new Error("simulated_failure_for_i1_only");
    }
    return originalFrom(t);
  };

  const result = await runSchedulerCycle(admin, "https://example.test", "svc-key");
  assertEquals(result.ok, true);
  // i1 فشل تقييم أهليّته (استثناءٌ داخل حلقة الأهلية، يُلتقَط ويُتجاوَز) —
  // i2 وصلت وتمّت معالجتها فعلياً (ادّعاءٌ + بوّابة).
  assertEquals(result.incidents_claimed, 1);
  assertEquals(result.incidents_evaluated, 1);
});

// ─── (H) أكثر من ٥ حوادث مؤهَّلة → BATCH_LIMIT فقط تُعالَج هذه الدورة ───
Deno.test("(H) more than BATCH_LIMIT eligible incidents exist: only BATCH_LIMIT are processed per cycle", async () => {
  const N = 8;
  assert(N > BATCH_LIMIT);
  const incidents = Array.from({ length: N }, (_, i) => makeIncident(`i${i}`));
  const diagnoses = incidents.map((inc, i) => makeDiagnosis(`d${i}`, inc.id));
  let claimCalls = 0;
  const admin = makeFakeAdmin({
    self_healing_controls: [GLOBAL_ENABLED],
    ops_incidents: incidents,
    ops_diagnoses: diagnoses,
    repair_playbooks: [BASE_PB],
  }, {
    rpcResults: {
      claim_incident_for_repair: () => { claimCalls += 1; return { data: `claim-${claimCalls}`, error: null }; },
    },
  });

  const result = await runSchedulerCycle(admin, "https://example.test", "svc-key");
  assertEquals(result.incidents_scanned, N);
  assertEquals(result.incidents_claimed, BATCH_LIMIT);
  assertEquals(result.incidents_evaluated, BATCH_LIMIT);
  assertEquals(claimCalls, BATCH_LIMIT);
});
