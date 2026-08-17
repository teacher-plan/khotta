// ════════════════════════════════════════════════════════════════════
// Edge Function: autonomous-scheduler
// KHOTTA Autonomous Operations 2.0 — Phase 3.5-B: جدولة بوّابة التنفيذ
// الآلي (Scheduler & Gateway Integration) — SHADOW فقط، بلا LLM جديد هنا.
//
// تُستدعى كل ٥ دقائق عبر pg_cron ⇒ public.call_agent('autonomous-scheduler')
// (نفس آلية agent-health-check/agent-daily-summary القائمة فعلياً —
// انظر 20260816_p0_agent_cron_service_key.sql وهجرة هذه المرحلة).
//
// ═══ لماذا يستحيل بنيوياً أن تُنفَّذ هذه الدالّة أي إجراءٍ فعلي اليوم ═══
// المسار الوحيد للتنفيذ الفعلي هنا هو executeAutonomous() من
// autonomousGateway.ts (Phase 3.5-A) — لا استدعاء مباشر لـACTIONS[...] في
// هذا الملف إطلاقاً. وGate 4 داخل تلك الدالّة يتوقّف دوماً اليوم لأن كلا
// الـPlaybook الحيّين mode='SHADOW' (لا AUTO) — هذه الدالّة لا تُغيّر ولا
// تقرأ mode لتقرّر شيئاً، هي فقط تستدعي البوّابة وتُسجِّل ما تُعيده.
//
// deno-lint-ignore-file no-explicit-any
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { isServiceRoleRequest, unauthorized } from "../_shared/adminGuard.ts";
import { executeAutonomous } from "../_shared/autonomousGateway.ts";
import { matchIncidentPattern, checkRateLimitAndCooldown } from "../_shared/opsPlaybooks.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
}

// ═══ ثوابتٌ مسمّاة — سهلة التعديل لاحقاً، لا أرقامٌ سحرية مبعثرة ═══
export const BATCH_LIMIT = 5;                 // سقف عدد الحوادث المُقيَّمة (ادّعاء+بوّابة) لكل دورة
export const CANDIDATE_SCAN_LIMIT = 50;        // سقف عدد الحوادث المفحوصة أوّلياً قبل تصفية المطابقة
export const CLAIM_STALE_MINUTES = 15;         // نفس قيمة claim_incident_for_repair الافتراضية (Gate 11)
export const TIME_BUDGET_MS = 4 * 60 * 1000;   // ميزانية زمنٍ ناعمة (٤ دقائق) — الجدولة كل ٥ دقائق
export const DIAGNOSE_FETCH_TIMEOUT_MS = 30000;

interface RunCounters {
  incidents_scanned: number;
  incidents_claimed: number;
  incidents_evaluated: number;
  shadow_would_repair: number;
  escalated: number;
  errors: number;
}

function freshCounters(): RunCounters {
  return { incidents_scanned: 0, incidents_claimed: 0, incidents_evaluated: 0, shadow_would_repair: 0, escalated: 0, errors: 0 };
}

// ─────────────────────────────────────────────────────────────────────
// الحصول على تشخيصٍ صالحٍ للحادثة — يفضّل تشخيصاً مكتملاً موجوداً سلفاً؛
// لا يُنشئ تشخيصاً جديداً إلا عند غيابه فعلياً، وحتى حينها لا نداء LLM
// جديد يُضاف هنا: الاستدعاء يمرّ عبر نفس مسار action:"diagnose" في
// ops-actions/index.ts (قاعدةٌ حتمية أولاً، LLM فقط عند عدم تطابق قاعدة —
// نفس المنطق القائم بالضبط، لا تكرارٌ له ولا نداءٌ جديد يُضيفه هذا الملف)،
// مُستدعًى بنفس نمط المصادقة الخدمية-إلى-خدمية القائم فعلاً (مفتاح
// الخدمة، كما يستدعي system-health-check دوالَّ أخرى بمفتاح anon/الخدمة).
// ─────────────────────────────────────────────────────────────────────
async function getOrCreateDiagnosis(
  admin: any, incidentId: string, supabaseUrl: string, serviceKey: string,
): Promise<any | null> {
  const { data: existing } = await admin
    .from("ops_diagnoses")
    .select("*")
    .eq("incident_id", incidentId)
    .eq("diagnosis_status", "COMPLETED")
    .order("completed_at", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (existing) return existing;

  try {
    const resp = await fetch(`${supabaseUrl}/functions/v1/ops-actions`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "Authorization": `Bearer ${serviceKey}` },
      body: JSON.stringify({ action: "diagnose", incident_id: incidentId }),
      signal: AbortSignal.timeout(DIAGNOSE_FETCH_TIMEOUT_MS),
    });
    if (!resp.ok) return null;
    const body = await resp.json().catch(() => null);
    const diag = body?.diagnosis ?? null;
    if (!diag || diag.diagnosis_status !== "COMPLETED") return null;
    return diag;
  } catch {
    return null;
  }
}

// ─────────────────────────────────────────────────────────────────────
// استخلاص ملخّص التشغيلات (agent_id/consecutive_failures/distinct_errors/
// last_success_at) من evidence المخزَّنة في التشخيص — نفس البنية التي
// يكتبها collectEvidence في opsDiagnosis.ts (source: "get_recent_agent_runs")،
// لا استنتاجٌ جديد.
// ─────────────────────────────────────────────────────────────────────
function extractRunsSummary(diag: any): { agent_id: string; consecutive_failures: number; distinct_errors: string[]; last_success_at: string | null } | null {
  const evidence = diag?.evidence;
  if (!Array.isArray(evidence)) return null;
  const item = evidence.find((e: any) => e?.source === "get_recent_agent_runs")?.value;
  if (!item || !item.agent_id) return null;
  return {
    agent_id: item.agent_id,
    consecutive_failures: item.consecutive_failures || 0,
    distinct_errors: item.distinct_errors || [],
    last_success_at: item.last_success_at || null,
  };
}

// ═══════════════════════════════════════════════════════════════════
// runSchedulerCycle — كل منطق الدورة معزولٌ في دالّةٍ مُصدَّرة (export)
// مستقلّة عن Deno.serve كي يُختبَر مباشرةً بـclient وهمي (fake admin) بلا
// تشغيل خادمٍ حقيقي — نفس أسلوب اختبار autonomousGateway_test.ts.
// ═══════════════════════════════════════════════════════════════════
export async function runSchedulerCycle(
  admin: any, supabaseUrl: string, serviceKey: string,
): Promise<{ ok: boolean; run_id: string | null; skipped?: string; error?: string } & Partial<RunCounters>> {
  const cycleStart = Date.now();
  let runId: string | null = null;

  try {
    const { data: runRow } = await admin.from("scheduler_runs").insert({ status: "RUNNING" }).select("run_id").maybeSingle();
    runId = runRow?.run_id ?? null;

    const counters = freshCounters();

    // ═══ Gate 3 المكافئ على مستوى الجدولة: المفتاح العام أوّلاً — إن كان
    // مُعطَّلاً لا ادّعاء ولا بوّابة إطلاقاً هذه الدورة (المتطلَّب 4و). ═══
    const { data: ctl } = await admin.from("self_healing_controls").select("*").eq("control_id", "global").maybeSingle();
    const globalEnabled = !!ctl && ctl.self_healing_enabled !== false;

    if (!globalEnabled) {
      await finishSchedulerRun(admin, runId, "COMPLETED", counters, cycleStart, { skipped: "SKIPPED_GLOBAL_DISABLED" });
      return { ok: true, run_id: runId, skipped: "SKIPPED_GLOBAL_DISABLED", ...counters };
    }

    // ═══ استعلام الأهلية: حوادث غير مُغلَقة، مُرتَّبةٌ بآخر ظهور. المطابقة
    // نفسها (matchIncidentPattern) وفحص cooldown (checkRateLimitAndCooldown)
    // مستوردان حرفياً من opsPlaybooks.ts — لا إعادة اختراعٍ لمنطقهما. عدم
    // الادّعاء يُفحَص فعلياً عبر claim_incident_for_repair نفسها أدناه (نفس
    // منطق التقادم — لا تكرارٌ له هنا). ═══
    const { data: candidates } = await admin
      .from("ops_incidents")
      .select("*")
      .neq("status", "RESOLVED")
      .order("last_seen_at", { ascending: false })
      .limit(CANDIDATE_SCAN_LIMIT);

    counters.incidents_scanned = (candidates || []).length;

    const eligible: { incident: any; diagnosis: any; playbook: any; runsSummary: ReturnType<typeof extractRunsSummary> }[] = [];

    for (const incident of candidates || []) {
      if (Date.now() - cycleStart > TIME_BUDGET_MS) break;
      if (eligible.length >= BATCH_LIMIT) break;
      try {
        const diagnosis = await getOrCreateDiagnosis(admin, incident.id, supabaseUrl, serviceKey);
        if (!diagnosis) continue;
        const runsSummary = extractRunsSummary(diagnosis);
        if (!runsSummary) continue;

        const pattern = matchIncidentPattern(runsSummary);
        if (!pattern) continue;

        const { data: playbook } = await admin.from("repair_playbooks").select("*").eq("incident_pattern", pattern).eq("enabled", true).maybeSingle();
        if (!playbook) continue;

        // فحصٌ إضافيٌّ رخيص (المتطلَّب 8): خطورةٌ عالية أو قاطعٌ مفتوح ⇒
        // لا داعي لادّعاءٍ أو استدعاء بوّابةٍ عبثاً — الاثنان اليوم دوماً
        // LOW/CLOSED لكن الفحص صادقٌ لا مُعلَّقاً بافتراض.
        if (playbook.risk_level === "HIGH" || playbook.risk_level === "CRITICAL") continue;
        if (playbook.circuit_state === "OPEN") continue;

        const rl = await checkRateLimitAndCooldown(admin, playbook, incident.id);
        if (rl.rateLimited || rl.cooldownActive) continue;

        eligible.push({ incident, diagnosis, playbook, runsSummary });
      } catch {
        // فشل تقييم مرشّحٍ واحد لا يُسقط بقيّة المسح — يُتجاوَز فقط.
        continue;
      }
    }

    if (!eligible.length) {
      await finishSchedulerRun(admin, runId, "COMPLETED", counters, cycleStart);
      return { ok: true, run_id: runId, ...counters };
    }

    // ═══ المعالجة: لكل حادثةٍ مؤهَّلة — ادّعاءٌ ذرّي ثم البوّابة فقط.
    // (المتطلَّب 4/7): try/catch مستقلٌّ لكل حادثة، فشل واحدةٍ لا يوقف البقيّة.
    // ═══
    for (const item of eligible) {
      if (Date.now() - cycleStart > TIME_BUDGET_MS) break;

      let claimId: string | null = null;
      try {
        const { data: claim, error: claimErr } = await admin.rpc("claim_incident_for_repair", {
          p_incident_id: item.incident.id,
          p_playbook_id: item.playbook.playbook_id,
          p_claimed_by: "autonomous_scheduler",
          p_stale_minutes: CLAIM_STALE_MINUTES,
        });
        if (claimErr || !claim) continue; // ادّعاءٌ فاشل — تخطٍّ فوري، لا إعادة محاولة ضمن نفس الدورة
        claimId = String(claim);
        counters.incidents_claimed += 1;

        // المسار الوحيد للتنفيذ الفعلي: executeAutonomous من autonomousGateway.ts.
        // لا استدعاء مباشر لـACTIONS[...] هنا إطلاقاً.
        const result = await executeAutonomous(admin, {
          incidentId: item.incident.id,
          diagnosisId: item.diagnosis.diagnosis_id,
          agentId: item.runsSummary!.agent_id,
          consecutiveFailures: item.runsSummary!.consecutive_failures,
          distinctErrors: item.runsSummary!.distinct_errors,
          lastSuccessAt: item.runsSummary!.last_success_at,
        });
        counters.incidents_evaluated += 1;
        if (result.status === "WOULD_AUTO_HEAL") counters.shadow_would_repair += 1;
        if (result.status === "ESCALATED") counters.escalated += 1;
      } catch {
        counters.errors += 1;
      } finally {
        // تحريرٌ دوماً بعد اكتمال المحاولة (نجاحاً أو فشلاً) — لا إعادة
        // محاولةٍ ضمن نفس الدورة (المتطلَّب 4د).
        if (claimId) {
          try {
            await admin.rpc("release_incident_claim", { p_claim_id: claimId });
          } catch {
            // تحريرٌ فاشل لا يُسقط الدورة — القفل سينتهي صلاحيته تلقائياً
            // بعد CLAIM_STALE_MINUTES على أي حال.
          }
        }
      }
    }

    await finishSchedulerRun(admin, runId, "COMPLETED", counters, cycleStart);
    return { ok: true, run_id: runId, ...counters };
  } catch (error) {
    // ═══ فشل الدورة كاملةً: تُسجَّل FAILED مع التفاصيل، ورَدٌّ نظيفٌ —
    // لا رميٌ يُغري بعاصفة إعادة محاولاتٍ؛ pg_cron سيُحاول تلقائياً في
    // الدورة التالية بصرف النظر عن رمز الحالة هنا. ═══
    console.error("autonomous-scheduler: فشلٌ في الدورة:", String(error));
    if (runId) {
      try {
        await admin.from("scheduler_runs").update({
          status: "FAILED",
          completed_at: new Date().toISOString(),
          duration_ms: Date.now() - cycleStart,
          error_detail: { error: String(error) },
        }).eq("run_id", runId);
      } catch {
        // لا شيءٌ إضافي يمكن فعله — الدورة فشلت والتسجيل نفسه فشل.
      }
    }
    return { ok: false, run_id: runId, error: String(error) };
  }
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  // 🔒 نفس نمط الحراسة القائم لكل الوكلاء المجدولة (system-health-check
  // إلخ): يسبر request بمفتاح الخدمة فقط — لا نقطة نهايةٍ عامّة جديدة.
  if (!isServiceRoleRequest(req)) return unauthorized(cors);

  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
  const serviceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
  const admin = createClient(supabaseUrl, serviceKey);

  const result = await runSchedulerCycle(admin, supabaseUrl, serviceKey);
  return json(result, result.ok ? 200 : 200);
});

async function finishSchedulerRun(
  admin: any, runId: string | null, status: "COMPLETED" | "FAILED", counters: RunCounters, cycleStart: number, extra: Record<string, unknown> = {},
): Promise<void> {
  if (!runId) return;
  try {
    await admin.from("scheduler_runs").update({
      status,
      completed_at: new Date().toISOString(),
      duration_ms: Date.now() - cycleStart,
      incidents_scanned: counters.incidents_scanned,
      incidents_claimed: counters.incidents_claimed,
      incidents_evaluated: counters.incidents_evaluated,
      shadow_would_repair: counters.shadow_would_repair,
      escalated: counters.escalated,
      errors: counters.errors,
      error_detail: Object.keys(extra).length ? extra : null,
    }).eq("run_id", runId);
  } catch (e) {
    console.error("scheduler_runs: تعذّر تحديث سجلّ الدورة:", String(e));
  }
}
