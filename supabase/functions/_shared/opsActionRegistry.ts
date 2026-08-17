// ═══ KHOTTA Autonomous Operations 2.0 — Phase 2: طبقة تنفيذ الإجراءات
// الآمنة + التحقّق (Action Execution + Verification Engine) ═══
//
// كل إجراءٍ هنا مطابقٌ 1:1 لصفٍّ في safe_action_registry (DB) — تحقّقٌ
// مزدوج: الصفّ يجب أن يكون enabled=true في القاعدة، والمعرّف يجب أن
// يكون معروفاً هنا في الكود. غياب أيٍّ منهما = رفضٌ فوري، لا تنفيذ.
//
// ممنوعٌ صراحةً أن يُضاف هنا أي إجراءٍ عام (execute_sql/execute_command/
// run_any_function/admin_override/ai_action) — القسم 6 من المواصفة.
//
// deno-lint-ignore-file no-explicit-any
import { get_recent_agent_runs, get_agent_schedule } from "./opsTools.ts";

const KNOWN_MONITOR_AGENTS = [
  "system-health-check", "credit-monitor", "database-capacity-monitor",
  "file-processor-monitor", "daily-summary",
] as const;

export interface ActionExecResult {
  ok: boolean;
  result?: Record<string, unknown>;
  error?: string;
}
export interface VerificationResult {
  status: "PASSED" | "FAILED" | "INCONCLUSIVE";
  detail: Record<string, unknown>;
}

// نفس نداء invokeAgentNow الحقيقي في telegram-webhook/index.ts (منطقٌ
// منسوخٌ حرفياً، لا نسخةٌ جديدة مختلفة السلوك) — نداء دالّة حافةٍ معروفة
// بمفتاح الخدمة نفسه.
async function invokeAgentNow(fnName: string): Promise<{ ok: boolean; status: number; error?: string }> {
  try {
    const r = await fetch(`${Deno.env.get("SUPABASE_URL")}/functions/v1/${fnName}`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({}),
    });
    return { ok: r.ok, status: r.status, error: r.ok ? undefined : `HTTP ${r.status}` };
  } catch (e) {
    return { ok: false, status: 0, error: String(e) };
  }
}

// كل إجراءٍ: execute(params) → ActionExecResult، verify(params, execResult) → VerificationResult.
// الاثنان منفصلان دوماً (القسم 11: لا اعتبار النجاح مجرّد نداءٍ ناجح).
export const ACTIONS: Record<string, {
  execute: (admin: any, params: Record<string, unknown>) => Promise<ActionExecResult>;
  verify: (admin: any, params: Record<string, unknown>, exec: ActionExecResult, startedAt: string) => Promise<VerificationResult>;
}> = {
  rerun_monitor_agent: {
    async execute(_admin, params) {
      const agentId = String(params.agent_id || "");
      if (!KNOWN_MONITOR_AGENTS.includes(agentId as any)) {
        return { ok: false, error: `agent_id غير مسموح: ${agentId}` };
      }
      const r = await invokeAgentNow(agentId);
      return { ok: r.ok, result: { invoked: r.ok, http_status: r.status }, error: r.error };
    },
    async verify(admin, params, exec, startedAt) {
      if (!exec.ok) return { status: "FAILED", detail: { reason: "نداء الدالّة نفسه فشل — لا داعي للتحقّق." } };
      const agentId = String(params.agent_id || "");
      // ننتظر لحظاتٍ قصيرة قبل التحقّق — تشغيلة agent_runs تُكتَب فور بدء
      // الدالّة المستهدَفة، لا حاجة لانتظارٍ طويل، لكن سباقٌ فوريٌّ ممكن.
      await new Promise((res) => setTimeout(res, 1500));
      const summary = await get_recent_agent_runs(admin, agentId, 5);
      const newRun = (summary.runs || []).find((r: any) => new Date(r.started_at).getTime() >= new Date(startedAt).getTime() - 2000);
      if (!newRun) return { status: "INCONCLUSIVE", detail: { reason: "لا تشغيلةٌ جديدة ظاهرة بعد في agent_runs — قد تحتاج وقتاً أطول." } };
      if (newRun.status === "SUCCESS") return { status: "PASSED", detail: { run_id: newRun.run_id, status: newRun.status } };
      if (newRun.status === "RUNNING") return { status: "INCONCLUSIVE", detail: { reason: "التشغيلة لا تزال جارية.", run_id: newRun.run_id } };
      return { status: "FAILED", detail: { run_id: newRun.run_id, status: newRun.status, error: newRun.error } };
    },
  },

  reschedule_daily_summary: {
    async execute(admin) {
      const now = new Date();
      const { data: before } = await admin.from("agent_schedules").select("scheduled_hour,scheduled_minute").eq("agent_name", "daily-summary").maybeSingle();
      const targetHour = now.getHours();
      const targetMinute = now.getMinutes();
      const { error } = await admin.from("agent_schedules").update({
        scheduled_hour: targetHour, scheduled_minute: targetMinute,
      }).eq("agent_name", "daily-summary");
      if (error) return { ok: false, error: error.message };
      return { ok: true, result: { scheduled_hour: targetHour, scheduled_minute: targetMinute, previous: before || null } };
    },
    async verify(admin, _params, exec) {
      if (!exec.ok || !exec.result) return { status: "FAILED", detail: { reason: "فشل التنفيذ." } };
      const after = await get_agent_schedule(admin, "daily-summary");
      const ok = after.found && after.schedule?.scheduled_hour === exec.result.scheduled_hour && after.schedule?.scheduled_minute === exec.result.scheduled_minute;
      return ok
        ? { status: "PASSED", detail: { schedule: after.schedule } }
        : { status: "FAILED", detail: { reason: "قيمة الجدول بعد الكتابة لا تطابق القيمة المطلوبة.", schedule: after.schedule } };
    },
  },
};

export function isKnownAction(actionId: string): boolean {
  return Object.prototype.hasOwnProperty.call(ACTIONS, actionId);
}
