// طبقةُ تتبّعٍ موحَّدة لتشغيلات الوكلاء (agent_runs) — Phase 1.5.
//
// قاعدةُ أمانٍ صارمة: فشل التسجيل نفسه لا يجوز أن يُسقط وظيفة الوكيل
// الأساسية أبداً — الملاحظة (Observability) لا يجوز أن تصير سبباً لعطلٍ
// إنتاجي. كل دالّةٍ هنا تبتلع أخطاءها الخاصة وتُعيد null/تتجاهل بصمت
// مع console.error، ولا ترمي أبداً.
//
// deno-lint-ignore-file no-explicit-any

export interface RunHandle {
  runId: string | null;
  correlationId: string | null;
  startedAt: number;
}

// بدءُ تشغيلة — يُستدعى أول شيء في الدالّة. عند فشل الإدراج (RLS/شبكة/
// اسم وكيل غير مسجَّل في agent_registry) نُعيد مقبضاً فارغاً بصمت؛ الوكيل
// يتابع عمله الأساسي بلا تتبّع لهذه المرّة فقط.
export async function startRun(
  sb: any,
  agentId: string,
  trigger: "CRON" | "MANUAL" | "WEBHOOK" | "ON_DEMAND" = "CRON",
): Promise<RunHandle> {
  const startedAt = Date.now();
  try {
    const { data, error } = await sb.from("agent_runs").insert({
      agent_id: agentId, trigger, status: "RUNNING",
    }).select("run_id,correlation_id").maybeSingle();
    if (error) {
      console.error(`agent_runs: تعذّر بدء تشغيلة (${agentId}):`, error.message);
      return { runId: null, correlationId: null, startedAt };
    }
    return { runId: data?.run_id ?? null, correlationId: data?.correlation_id ?? null, startedAt };
  } catch (e) {
    console.error(`agent_runs: استثناءٌ أثناء بدء تشغيلة (${agentId}):`, String(e));
    return { runId: null, correlationId: null, startedAt };
  }
}

export interface FinishArgs {
  status: "SUCCESS" | "FAILED" | "PARTIAL" | "TIMEOUT" | "SKIPPED";
  resultSummary?: string;
  error?: string;
  recordsRead?: number;
  recordsWritten?: number;
  actionsTaken?: unknown[];
  extra?: Record<string, unknown>;
}

// إنهاءُ تشغيلة — لا يُستدعى إن كان runId فارغاً (لا صفّ لتحديثه أصلاً).
export async function finishRun(sb: any, handle: RunHandle, args: FinishArgs): Promise<void> {
  if (!handle.runId) return;
  try {
    await sb.from("agent_runs").update({
      status: args.status,
      completed_at: new Date().toISOString(),
      duration_ms: Date.now() - handle.startedAt,
      result_summary: args.resultSummary ?? null,
      error: args.error ?? null,
      records_read: args.recordsRead ?? null,
      records_written: args.recordsWritten ?? null,
      actions_taken: args.actionsTaken ?? [],
      extra: args.extra ?? null,
    }).eq("run_id", handle.runId);
  } catch (e) {
    console.error("agent_runs: تعذّر إنهاء التشغيلة:", String(e));
  }
}
