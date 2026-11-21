// وكيل مراقبة سعة قاعدة البيانات (Database Capacity Monitor)
// KHOTTA Autonomous Operations 2.0 — Phase 1
//
// قراءةٌ صرفة فقط: لا DELETE/UPDATE/DROP/TRUNCATE/ALTER/VACUUM ولا SQL
// حرّ — فقط RPCs جاهزة (database_size, database_top_tables) وSELECT على
// جدول تاريخ داخلي (db_capacity_history) كتبته هذه الدالة نفسها.
//
// يفرّق صراحةً بين: حجم قاعدة البيانات (Postgres) — هذا الملف فقط — وبين
// Supabase Storage (ملفات) وتكلفة الذكاء الاصطناعي (ai_cost_log)؛ لا خلط.
// مراقبة Supabase Storage نفسها خارج نطاق Phase 1 (انظر التقرير، القسم 28).
//
// النشر: supabase functions deploy database-capacity-monitor

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendTelegramOps as sendTelegram } from "../_shared/telegram.ts";
import { isServiceRoleRequest, unauthorized } from "../_shared/adminGuard.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

// ⚠️ الحدّ الأقصى لخطة Supabase الفعلية غير موجود في أي إعداد/سرّ مقروء في
// هذا المشروع (NOT VERIFIED). هذه القيمة الافتراضية أدناه NULL عمداً —
// لا تُخترَع. لضبطها لاحقاً: أضف سرّاً DB_PLAN_LIMIT_MB في متغيرات البيئة.
function getConfiguredLimitMb(): number | null {
  const raw = Deno.env.get("DB_PLAN_LIMIT_MB");
  const n = raw ? Number(raw) : NaN;
  return Number.isFinite(n) && n > 0 ? n : null;
}

// عتبات تنبيه تدرّجية — افتراضية بانتظار تأكيد حدّ الخطة الحقيقي.
const THRESHOLDS = [
  { pct: 98, tier: "CRITICAL" },
  { pct: 95, tier: "CRITICAL" },
  { pct: 90, tier: "HIGH" },
  { pct: 80, tier: "MEDIUM" },
  { pct: 70, tier: "LOW" },
] as const;

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  // 🔒 نفس نمط الحراسة في بقية وكلاء المراقبة (file-processor-monitor,
  // credit-monitor, system-health-check).
  if (!isServiceRoleRequest(req)) return unauthorized(cors);

  const startedAt = Date.now();
  const sb = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  let runId: string | null = null;
  try {
    // ═ 1) بدء تشغيلة في دفتر agent_runs (إضافي — لا يوقف الدالة إن فشل) ═
    const { data: runRow } = await sb.from("agent_runs").insert({
      agent_id: "database-capacity-monitor",
      trigger: "CRON",
      status: "RUNNING",
    }).select("run_id,correlation_id").maybeSingle();
    runId = runRow?.run_id ?? null;
    const correlationId = runRow?.correlation_id ?? null;

    console.log("💾 بدء فحص سعة قاعدة البيانات...");

    // ═ 2) حجم قاعدة البيانات الحقيقي (RPC موجود مسبقاً منذ Phase 0) ═
    const { data: sizeRows, error: sizeErr } = await sb.rpc("database_size");
    const sizeMb: number | null = sizeRows?.[0]?.database_size_mb ?? null;

    if (sizeErr || sizeMb === null) {
      await sb.from("agent_logs").insert({
        agent_name: "database-capacity-monitor", action: "measure_size", status: "error",
        error_message: sizeErr?.message || "database_size() returned no data", correlation_id: correlationId, run_id: runId,
      });
      if (runId) await sb.from("agent_runs").update({
        status: "FAILED", completed_at: new Date().toISOString(),
        duration_ms: Date.now() - startedAt, error: sizeErr?.message || "no size data",
      }).eq("run_id", runId);
      return json({ error: "failed_to_measure_database_size", detail: sizeErr?.message }, 500);
    }

    // ═ 3) أكبر الجداول تخزيناً — أسماءٌ حقيقية من كتالوج المشروع ═
    const { data: topTables } = await sb.rpc("database_top_tables", { p_limit: 10 });

    // ═ 4) الحدّ المعروف (إن وُجد) ونسبة الاستهلاك ═
    const limitMb = getConfiguredLimitMb();
    const usagePercent = limitMb ? Math.round((sizeMb / limitMb) * 1000) / 10 : null;

    // ═ 5) التاريخ: القراءة قبل الكتابة — لحساب النمو والتوقّع من نفس
    //     الجدول الذي ستكتب إليه هذه التشغيلة صفّاً جديداً بعد قليل ═
    const { data: history } = await sb
      .from("db_capacity_history")
      .select("measured_at,size_mb")
      .order("measured_at", { ascending: false })
      .limit(30);

    const points = (history || []).slice().reverse(); // الأقدم أولاً
    let growth: Record<string, unknown>;
    let forecast: Record<string, unknown>;

    if (points.length < 2) {
      growth = { status: "INSUFFICIENT_DATA", reason: `عدد القياسات التاريخية المتاحة: ${points.length} — يلزم قياسان على الأقل لحساب معدّل نمو.` };
      forecast = { status: "INSUFFICIENT_DATA", reason: "لا يمكن التوقّع بلا معدّل نمو موثوق." };
    } else {
      const first = points[0];
      const last = points[points.length - 1];
      const hoursSpan = (new Date(last.measured_at).getTime() - new Date(first.measured_at).getTime()) / 3_600_000;
      if (hoursSpan < 24 || points.length < 4) {
        // أقل من يوم واحد من التاريخ أو أقل من ٤ قياسات (أقل من يوم كامل
        // بمعدّل كل ٦ ساعات) — نافذة العيّنة قصيرة جداً لمعدّل نمو موثوق.
        growth = { status: "INSUFFICIENT_DATA", reason: `النافذة الزمنية المتاحة (${hoursSpan.toFixed(1)} ساعة، ${points.length} قياسات) قصيرة جداً لمعدّل نمو موثوق — يلزم عدة أيام.` };
        forecast = { status: "INSUFFICIENT_DATA", reason: "بانتظار تراكم تاريخٍ كافٍ (أيام قليلة على الأقل)." };
      } else {
        const deltaMb = last.size_mb - first.size_mb;
        const mbPerDay = (deltaMb / hoursSpan) * 24;
        growth = {
          status: "OK",
          window_hours: Math.round(hoursSpan * 10) / 10,
          samples: points.length,
          delta_mb: Math.round(deltaMb * 100) / 100,
          mb_per_day: Math.round(mbPerDay * 100) / 100,
        };
        if (limitMb && mbPerDay > 0) {
          const remainingMb = limitMb * 0.9 - sizeMb; // زمن الوصول لـ٩٠٪
          const daysTo90 = remainingMb > 0 ? Math.round((remainingMb / mbPerDay) * 10) / 10 : 0;
          forecast = {
            status: "OK",
            days_to_90_percent: daysTo90,
            basis: "معدّل نمو خطّي بسيط من العيّنات الأخيرة فقط — ليس نموذجاً إحصائياً متقدماً.",
          };
        } else if (!limitMb) {
          forecast = { status: "INSUFFICIENT_DATA", reason: "الحدّ الأقصى للخطة غير مؤكَّد (NOT VERIFIED) — لا يمكن حساب زمن الوصول لعتبة٪ بلا حدّ." };
        } else {
          forecast = { status: "OK", days_to_90_percent: null, note: "معدّل النمو صفرٌ أو سالب — لا خطر توسّعٍ قريب وفق العيّنات الحالية." };
        }
      }
    }

    // ═ 6) تصنيف تنبيه العتبة (إن وُجد حدّ فقط) ═
    let alertTier: string | null = null;
    if (usagePercent !== null) {
      for (const t of THRESHOLDS) if (usagePercent >= t.pct) { alertTier = t.tier; break; }
    }

    // ═ 7) كشف شذوذ بسيط: قفزة حجم غير معتادة بين آخر قياسين (يحتاج
    //     تاريخاً كافياً؛ يتدهور بأمان إلى INSUFFICIENT_DATA بلا اختلاق) ═
    let anomaly: Record<string, unknown>;
    if (points.length >= 2) {
      const prev = points[points.length - 1];
      const jumpMb = sizeMb - prev.size_mb;
      const jumpPct = prev.size_mb > 0 ? (jumpMb / prev.size_mb) * 100 : 0;
      anomaly = jumpPct > 15
        ? { status: "ANOMALY_DETECTED", jump_percent: Math.round(jumpPct * 10) / 10, note: "قفزة حجمٍ غير معتادة (>15%) منذ آخر قياس — يستحق مراجعة يدوية." }
        : { status: "NORMAL", jump_percent: Math.round(jumpPct * 10) / 10 };
    } else {
      anomaly = { status: "INSUFFICIENT_DATA" };
    }

    // ═ 8) تخزين القياس في تاريخ خفيف مخصَّص (db_capacity_history) ═
    await sb.from("db_capacity_history").insert({
      run_id: runId, size_mb: sizeMb, top_tables: topTables || null,
      limit_mb: limitMb, usage_percent: usagePercent,
    });

    // ═ 9) إشعار Telegram فقط عند تصعيد فعلي (MEDIUM فأعلى) — لا ضجيج
    //     لكل تشغيلة سليمة كل ٦ ساعات. يعيد استخدام نمط dedup الموجود في
    //     ops_incidents عبر processCapacityIncident أدناه لمنع تكرار
    //     التنبيه لنفس المستوى في تشغيلاتٍ متتالية. ═
    let escalated = false;
    if (alertTier && alertTier !== "LOW") {
      escalated = await processCapacityIncident(sb, {
        tier: alertTier, sizeMb, limitMb, usagePercent, correlationId, runId,
      });
    }

    const durationMs = Date.now() - startedAt;
    await sb.from("agent_logs").insert({
      agent_name: "database-capacity-monitor", action: "measured", status: "success",
      execution_time_ms: durationMs,
      data_collected: { size_mb: sizeMb, usage_percent: usagePercent, alert_tier: alertTier, growth, top_tables_count: (topTables || []).length },
      correlation_id: correlationId, run_id: runId,
    });

    if (runId) await sb.from("agent_runs").update({
      status: "SUCCESS", completed_at: new Date().toISOString(), duration_ms: durationMs,
      result_summary: `حجم القاعدة ${sizeMb} MB` + (usagePercent !== null ? ` (${usagePercent}% من الحدّ)` : " — الحدّ غير مؤكَّد"),
      records_read: (topTables || []).length + points.length,
      records_written: 1,
      actions_taken: escalated ? [{ action: "escalate_incident", tier: alertTier }] : [],
      extra: { size_mb: sizeMb, limit_mb: limitMb, usage_percent: usagePercent, growth, forecast, anomaly, top_tables: topTables },
    }).eq("run_id", runId);

    return json({
      ok: true,
      resource: "database_storage", // تمييزٌ صريح عن Supabase Storage/AI cost
      database_size_mb: sizeMb,
      limit_mb: limitMb,
      limit_source: limitMb ? "env:DB_PLAN_LIMIT_MB" : "NOT_VERIFIED",
      usage_percent: usagePercent ?? "NOT_AVAILABLE",
      alert_tier: alertTier,
      thresholds_note: "عتبات 70/80/90/95/98% افتراضية بانتظار تأكيد حدّ خطة Supabase الفعلي.",
      top_tables: topTables || [],
      growth,
      forecast,
      anomaly,
      run_id: runId,
      duration_ms: durationMs,
    });
  } catch (error) {
    console.error("❌ database-capacity-monitor error:", error);
    try {
      if (runId) await sb.from("agent_runs").update({
        status: "FAILED", completed_at: new Date().toISOString(),
        duration_ms: Date.now() - startedAt, error: String(error),
      }).eq("run_id", runId);
      await sb.from("agent_logs").insert({
        agent_name: "database-capacity-monitor", action: "run", status: "error", error_message: String(error), run_id: runId,
      });
    } catch { /* تسجيل الفشل نفسه فشل — لا نرفع استثناءً ثانياً */ }
    return json({ error: String(error) }, 500);
  }
});

// تصعيدٌ إلى ops_incidents بنفس نمط dedup المثبَت في system-health-check
// (dedup_key + occurrence_count) — يمنع تنبيهاً مكرّراً لكل تشغيلة طالما
// الحادثة مفتوحة بنفس المستوى، ويُرسل Telegram فقط عند إنشاء حادثة جديدة
// أو تصعيدها (لا عند كل تكرار). severity: HIGH/CRITICAL → P1، MEDIUM → P2.
async function processCapacityIncident(
  // deno-lint-ignore no-explicit-any
  sb: any,
  args: { tier: string; sizeMb: number; limitMb: number | null; usagePercent: number | null; correlationId: string | null; runId: string | null },
): Promise<boolean> {
  const dedupKey = "database-capacity";
  const severity = args.tier === "CRITICAL" ? "P1" : args.tier === "HIGH" ? "P1" : "P2";
  const requiresHuman = args.tier === "CRITICAL";

  const { data: existing } = await sb
    .from("ops_incidents")
    .select("id,occurrence_count,severity")
    .eq("dedup_key", dedupKey)
    .neq("status", "RESOLVED")
    .order("last_seen_at", { ascending: false })
    .limit(1)
    .maybeSingle();

  const summary = `استهلاك قاعدة البيانات ${args.usagePercent}% (${args.sizeMb} MB${args.limitMb ? ` من ${args.limitMb} MB` : ""}) — مستوى ${args.tier}`;

  if (existing) {
    const escalating = severity === "P1" && existing.severity === "P2";
    await sb.from("ops_incidents").update({
      occurrence_count: (existing.occurrence_count || 1) + 1,
      last_seen_at: new Date().toISOString(),
      severity, // قد يتصاعد من P2 إلى P1
      summary,
      requires_human_attention: requiresHuman,
    }).eq("id", existing.id);
    if (!escalating) return false; // تكرارٌ بنفس المستوى — لا تنبيه Telegram جديد
  } else {
    await sb.from("ops_incidents").insert({
      dedup_key: dedupKey, severity, status: args.tier === "CRITICAL" ? "ACTION_REQUIRED" : "DETECTED",
      component: "database_storage", summary,
      evidence: [{ source: "database-capacity-monitor", data: args }],
      confidence: "VERIFIED",
      source_agent: "database-capacity-monitor",
      correlation_id: args.correlationId,
      related_run_id: args.runId,
      suggested_action: args.tier === "CRITICAL"
        ? "راجع أكبر الجداول استهلاكاً وفكّر بترقية خطة Supabase فوراً."
        : "راقب النمو خلال الأيام القادمة، وفكّر بترقية الخطة إن استمر الاتجاه.",
      requires_human_attention: requiresHuman,
    });
  }

  // HIGH و CRITICAL فقط تُرسِل Telegram (سياسة التصعيد: MEDIUM → لوحة فقط،
  // HIGH/CRITICAL → لوحة + Telegram، CRITICAL أيضاً يرفع requires_human_attention).
  const msg = `${args.tier === "CRITICAL" ? "🚨" : "⚠️"} <b>تنبيه سعة قاعدة البيانات</b>\n━━━━━━━━━━━━━━━━━━━━━━\nالمستوى: ${args.tier}\nالحجم: ${args.sizeMb} MB${args.limitMb ? ` من ${args.limitMb} MB (${args.usagePercent}%)` : " (الحدّ الأقصى للخطة غير مؤكَّد)"}\n━━━━━━━━━━━━━━━━━━━━━━`;
  await sendTelegram(msg);
  return true;
}
