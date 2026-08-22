// وكيل مراقبة صحة النظام (System Health Check)
// يفحص جميع المكونات كل 5 دقائق ويرسل تنبيهات طارئة عند المشاكل

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendTelegramOps as sendTelegram } from "../_shared/telegram.ts";
import { isServiceRoleRequest, unauthorized } from "../_shared/adminGuard.ts";
import { startRun, finishRun } from "../_shared/agentRun.ts";

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

// Telegram parse_mode HTML يفسّر < و > و & كوسوم — رسائل أخطاء Deno الحقيقية
// تحتوي غالباً "<anonymous>" أو مسارات بأقواس، فتكسر الرسالة كاملة بلا وصول.
function escHtml(s: string): string {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

interface HealthCheckResult {
  component: string;
  status: "healthy" | "warning" | "critical";
  responseTime?: number;
  error?: string;
  severity: number;
}

// ١. فحص وظائف Supabase
async function checkEdgeFunctions(
  sb: any,
  baseUrl: string,
  token: string
): Promise<HealthCheckResult[]> {
  const functions = [
    "daily-summary",
    "credit-monitor",
    "generate-lesson-plan",
    "generate-game-content",
    "generate-infographic",
  ];

  const results: HealthCheckResult[] = [];

  const ping = async (fn: string) => {
    const start = Date.now();
    const response = await fetch(
      `${baseUrl}/functions/v1/${fn}`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
        // ٥ ثوانٍ كانت أقصر من "البدء البارد" (cold start) الطبيعي لدوالّ
        // الحافة — فكانت دوالٌّ سليمةٌ تماماً تُبلَّغ كـ"حرجة" بـTimeoutError
        // كل بضع دورات. ٢٠ ثانية تتجاوز البدء البارد المعتاد عادةً، لكنها
        // لا تزال تُخطئ أحياناً على بدءٍ باردٍ نادرٍ أبطأ من المعتاد — رفعُ
        // الرقم مجدداً لن يحلّها للأبد (فُعل هذا مرّةً ولا يزال يتكرّر)،
        // فبدلاً منه أُضيفت محاولةٌ ثانية أدناه قبل إعلان العطل.
        signal: AbortSignal.timeout(20000),
      }
    );
    return { response, duration: Date.now() - start };
  };

  for (const fn of functions) {
    let last: { response: Response; duration: number } | null = null;
    let lastErr: unknown = null;
    // محاولتان قبل الحكم بعطلٍ حقيقي: بدءٌ باردٌ عابر يصيب أي دالّةٍ أحياناً،
    // والتشغيلات المجدولة الفعلية لهذه الدوالّ (عبر cron) مُثبَتٌ أنها تنجح
    // خلال ثوانٍ معدودة — فتكرار التنبيه على عطلٍ لم يتكرّر فعلياً هو الضجيج
    // الذي أراد المشرف إيقافه، لا حجب عطلٍ حقيقي (الذي يفشل في المحاولتين معاً).
    for (let attempt = 1; attempt <= 2; attempt++) {
      try {
        last = await ping(fn);
        lastErr = null;
        // 401 هنا متوقّع للدوال المحمية: نستدعيها بمفتاح anon بلا JWT مستخدم
        // حقيقي، فرفضها بـ401 يعني أنها تعمل وتتحقق من الهوية بشكل صحيح —
        // وليس عطلاً. العطل الحقيقي هو 5xx أو انقطاع الاتصال.
        if ([200, 201, 401].includes(last.response.status)) break;
        if (last.response.status < 500) break; // 4xx غير 401: لا تستحقّ إعادة محاولة
      } catch (error) {
        lastErr = error;
        last = null;
      }
    }

    if (last && [200, 201, 401].includes(last.response.status)) {
      results.push({ component: `function:${fn}`, status: "healthy", responseTime: last.duration, severity: 1 });
    } else if (last) {
      results.push({
        component: `function:${fn}`,
        status: last.response.status >= 500 ? "critical" : "warning",
        responseTime: last.duration,
        error: `HTTP ${last.response.status}`,
        severity: last.response.status >= 500 ? 4 : 2,
      });
    } else {
      results.push({ component: `function:${fn}`, status: "critical", error: String(lastErr), severity: 4 });
    }
  }

  return results;
}

// ٢. فحص أداء قاعدة البيانات
async function checkDatabaseHealth(sb: any): Promise<HealthCheckResult[]> {
  const results: HealthCheckResult[] = [];

  try {
    // قياس سرعة الاتصال
    const start = Date.now();
    const { count, error } = await sb
      .from("profiles")
      .select("count", { count: "exact" });
    const duration = Date.now() - start;

    if (error) {
      results.push({
        component: "database:connection",
        status: "critical",
        responseTime: duration,
        error: error.message,
        severity: 4,
      });
    } else {
      const status = duration > 2000 ? "warning" : "healthy";
      results.push({
        component: "database:response_time",
        status,
        responseTime: duration,
        severity: duration > 2000 ? 2 : 1,
      });
    }

    // التحقق من حجم التخزين — دالة RPC تُرجع مصفوفة صف واحد
    const { data: statsRows } = await sb.rpc("database_size");
    const sizeMb = statsRows?.[0]?.database_size_mb;
    if (sizeMb != null && sizeMb > 4500) {
      results.push({
        component: "database:storage",
        status: "warning",
        error: `Storage: ${sizeMb}MB / 5000MB`,
        severity: 2,
      });
    } else {
      results.push({
        component: "database:storage",
        status: "healthy",
        severity: 1,
      });
    }
  } catch (error) {
    results.push({
      component: "database:health",
      status: "critical",
      error: String(error),
      severity: 4,
    });
  }

  return results;
}

// ٣. فحص سجلات الأخطاء الأخيرة
async function checkRecentErrors(sb: any): Promise<HealthCheckResult[]> {
  try {
    const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000).toISOString();

    const { data: errors } = await sb
      .from("error_logs")
      .select("*")
      .gte("occurred_at", oneHourAgo);

    const errorCount = errors?.length || 0;
    const criticalErrors = errors?.filter((e: any) => e.error_type === "function_error")
      .length || 0;

    return [
      {
        component: "error_tracking:count",
        status:
          criticalErrors > 5
            ? "critical"
            : errorCount > 10
              ? "warning"
              : "healthy",
        error:
          errorCount > 0 ? `${errorCount} errors (${criticalErrors} critical)` : undefined,
        severity: criticalErrors > 5 ? 4 : errorCount > 10 ? 2 : 1,
      },
    ];
  } catch (error) {
    return [
      {
        component: "error_tracking:health",
        status: "warning",
        error: String(error),
        severity: 2,
      },
    ];
  }
}

// ٤. فحص الملفات العالقة
async function checkStuckFiles(sb: any): Promise<HealthCheckResult[]> {
  try {
    const twoHoursAgo = new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString();

    const { data: stuckFiles } = await sb
      .from("file_processing_status")
      .select("*")
      .eq("status", "processing")
      .lt("updated_at", twoHoursAgo);

    const stuckCount = stuckFiles?.length || 0;

    return [
      {
        component: "file_processing:stuck_files",
        status: stuckCount > 0 ? "critical" : "healthy",
        error: stuckCount > 0 ? `${stuckCount} stuck files (>2 hours)` : undefined,
        severity: stuckCount > 0 ? 4 : 1,
      },
    ];
  } catch (error) {
    return [
      {
        component: "file_processing:health",
        status: "warning",
        error: String(error),
        severity: 2,
      },
    ];
  }
}

// ٥. تجميع النتائج وإرسال التنبيهات
async function processHealthResults(
  results: HealthCheckResult[],
  sb: any
): Promise<void> {
  // حفظ النتائج في قاعدة البيانات
  for (const result of results) {
    await sb.from("health_checks").insert({
      component_name: result.component,
      check_type: result.component.split(":")[0],
      status: result.status,
      response_time_ms: result.responseTime,
      error_message: result.error,
      severity: result.severity,
    });
  }

  // البحث عن المشاكل الحرجة
  const criticalIssues = results.filter((r) => r.status === "critical");
  const warnings = results.filter((r) => r.status === "warning");

  // إرسال تنبيهات طارئة فقط
  if (criticalIssues.length > 0) {
    for (const issue of criticalIssues) {
      // منع التكرار — مبنيٌّ على الزمن لا على حالة الحادثة. المحاولة
      // السابقة (فحص ops_incidents المفتوحة) لم تكفِ لأن العطل المتقطّع
      // (timeout ثم تعافٍ ثم timeout) يجعل الحادثة تُغلَق تلقائياً بين
      // كل ظهورٍ وآخر، فيُعَدّ كلُّ ظهورٍ "جديداً" ويُرسَل تنبيهٌ من جديد.
      // القاعدة الآن: تنبيهٌ واحدٌ لكل مكوّنٍ خلال ساعة، مهما تذبذب.
      const alertCooldownSince = new Date(Date.now() - 60 * 60 * 1000).toISOString();
      const { data: recentAlert } = await sb
        .from("emergency_alerts")
        .select("alert_id")
        .eq("affected_component", issue.component)
        .gte("created_at", alertCooldownSince)
        .limit(1)
        .maybeSingle();

      // السجلّ يُكتَب دوماً (أثرٌ تدقيقيٌّ كامل)، والإرسال وحده هو المحكوم
      // بفترة التهدئة — فلا نفقد أي معلومةٍ من تاريخ الأعطال.
      await sb.from("emergency_alerts").insert({
        alert_type: issue.component.split(":")[1],
        severity: issue.severity,
        title: `🚨 مشكلة حرجة: ${issue.component}`,
        description: issue.error,
        affected_component: issue.component,
        action_required: getActionForComponent(issue.component, issue.error),
      });

      if (recentAlert) continue; // نُبِّه عن هذا المكوّن خلال الساعة الماضية

      // إرسال تنبيه فوري عبر Telegram
      const alertMessage = `
🚨 <b>تنبيه حرج من نظام الصحة</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>المشكلة:</b> ${escHtml(issue.component)}
<b>الخطورة:</b> ${issue.severity}/5
<b>الخطأ:</b> ${escHtml(issue.error || "غير معروف")}
<b>الإجراء:</b> ${escHtml(getActionForComponent(issue.component, issue.error))}

⏰ الوقت: ${new Date().toLocaleString("ar-SA")}
      `.trim();

      await sendTelegram(alertMessage, {
        parse_mode: "HTML",
      });
    }
  }

  // حفظ ملخص الحالة
  const allHealthy = criticalIssues.length === 0 && warnings.length === 0;
  console.log(
    `📊 Health Check: ${allHealthy ? "✅ Healthy" : `⚠️ ${warnings.length} warnings, 🚨 ${criticalIssues.length} critical`}`
  );
}

// ═══ KHOTTA Autonomous Management — Phase 3: تجميع الحوادث ═══
// إضافةٌ بعد processHealthResults بلا تعديل حرفٍ فيها — نفس النتائج التي
// كانت تُكتب في health_checks وemergency_alerts وتلجرام كما هي تماماً،
// وفوقها الآن تجميعٌ في ops_incidents: تكرار عطل المكوّن نفسه ضمن نافذةٍ
// مفتوحة يزيد occurrence_count بدل صفٍّ وتنبيهٍ جديدين لكل فحصٍ فاشل.
// P0/P1 فقط يُرسِل تلجرام هنا (المُشكِلات الحرجة) — P2 (تحذيرات) تُسجَّل
// دون تنبيهٍ جديد، فلا ازدواج مع تنبيه processHealthResults الحرج أعلاه،
// ولا ضجيجٌ لكل تحذيرٍ عابر؛ تبقى مرئيةً عبر ops-analyze/الـcopilot.
async function processIncidents(
  results: HealthCheckResult[],
  sb: any,
  correlationId: string | null = null, // Phase 1.5: لربط الحادثة بتشغيلتها
): Promise<void> {
  try {
    const critical = results.filter((r) => r.status === "critical");
    const warning = results.filter((r) => r.status === "warning");
    const problematic = new Set([...critical, ...warning].map((r) => r.component));

    for (const issue of [...critical, ...warning]) {
      const severity = issue.status === "critical" ? "P1" : "P2";
      const { data: existing } = await sb
        .from("ops_incidents")
        .select("id,occurrence_count")
        .eq("dedup_key", issue.component)
        .neq("status", "RESOLVED")
        .order("last_seen_at", { ascending: false })
        .limit(1)
        .maybeSingle();

      if (existing) {
        await sb.from("ops_incidents").update({
          occurrence_count: (existing.occurrence_count || 1) + 1,
          last_seen_at: new Date().toISOString(),
        }).eq("id", existing.id);
        continue; // تكرارٌ لحادثةٍ مفتوحة — لا صفّ جديد ولا تنبيهٌ جديد
      }

      const { data: created } = await sb.from("ops_incidents").insert({
        dedup_key: issue.component,
        severity,
        status: "DETECTED",
        component: issue.component,
        summary: `${issue.component}: ${issue.error || issue.status}`,
        evidence: [{ source: "system-health-check", data: issue }],
        confidence: "VERIFIED", // من فحصٍ حيّ مباشر، لا استنتاج
        source_agent: "system-health-check",
        correlation_id: correlationId,
      }).select("id").maybeSingle();

      // P1 فقط يُنبَّه فوراً (P0 يتطلّب إشارةً أمنية/بياناتٍ لا يُصدرها هذا
      // الفحص — لا تُدَّعى بلا دليل). processHealthResults أرسل تنبيهاً
      // مسبقاً لهذا الفحص الحرج نفسه (منطقٌ منفصل غير مُعدَّل)؛ هذا سجلٌّ
      // تراكميّ إضافي في ops_incidents لا تنبيهاً ثانياً مكرَّراً.
      if (severity === "P1" && created) {
        console.log(`ops_incidents: حادثةٌ جديدة #${created.id} (${issue.component})`);
      }
    }

    // إغلاقٌ تلقائي: حادثةٌ مفتوحة لمكوّنٍ عاد سليماً الآن.
    const healthyNow = results.filter((r) => r.status === "healthy" && !problematic.has(r.component));
    for (const ok of healthyNow) {
      await sb.from("ops_incidents")
        .update({ status: "RESOLVED", resolved_at: new Date().toISOString() })
        .eq("dedup_key", ok.component)
        .neq("status", "RESOLVED");
    }
  } catch (e) {
    // تراكم الحوادث تحليليٌّ إضافي — فشله لا يُسقط الفحص الصحّي نفسه
    // ولا التنبيهات الحرجة القائمة (processHealthResults أعلاه مستقل تماماً).
    console.error("ops_incidents: فشل التجميع:", String(e));
  }
}

function getActionForComponent(component: string, error?: string): string {
  if (component.includes("function:")) {
    return "قم بفحص logs الدالة وأعد تشغيلها إذا لزم الأمر";
  }
  if (component.includes("database")) {
    return "قم بفحص اتصال قاعدة البيانات وأعد تشغيل الخادم";
  }
  if (component.includes("stuck_files")) {
    return "قم بحذف الملفات العالقة أو إعادة معالجتها يدوياً";
  }
  if (component.includes("storage")) {
    return "قم بتنظيف التخزين أو ترقية الخطة";
  }
  return "اتصل بدعم Supabase";
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  // 🔒 وكيلٌ إداريّ: يسبر دوالَّ أخرى ويكتب في تلجرام نيابةً عن المشرف.
  // ملاحظة: سبرُه للدوال يبقى بمفتاح anon، و401 عنده = صحّة (سطر ٧١)،
  // فإقفالُ daily-summary وcredit-monitor لا يجعلهما «معطوبتين» عنده.
  if (!isServiceRoleRequest(req)) return unauthorized(cors);

  const sb = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );
  // Phase 1.5: مُعرَّفةٌ خارج try كي يستطيع catch إغلاق التشغيلة بـFAILED
  // عند استثناءٍ غير مُلتقَط، لا فقط عند اكتمال الفحص بنجاح.
  let run = { runId: null as string | null, correlationId: null as string | null, startedAt: Date.now() };

  try {
    const baseUrl = Deno.env.get("SUPABASE_URL")!;
    const anonKey = Deno.env.get("SUPABASE_ANON_KEY")!;

    console.log("🔍 بدء فحص صحة النظام...");

    // Phase 1.5: بدء تشغيلة تتبّع (إضافي — لا يوقف الفحص إن فشل التسجيل)
    run = await startRun(sb, "system-health-check", "CRON");

    // تشغيل جميع الفحوصات بالتوازي
    const [
      functionChecks,
      dbChecks,
      errorChecks,
      fileChecks,
    ] = await Promise.all([
      checkEdgeFunctions(sb, baseUrl, anonKey),
      checkDatabaseHealth(sb),
      checkRecentErrors(sb),
      checkStuckFiles(sb),
    ]);

    const allResults = [
      ...functionChecks,
      ...dbChecks,
      ...errorChecks,
      ...fileChecks,
    ];

    // معالجة النتائج وإرسال التنبيهات — بلا تعديل
    await processHealthResults(allResults, sb);
    // Phase 3: تجميع الحوادث فوق النتائج نفسها — إضافةٌ لا تُغيّر ما سبق
    // Phase 1.5: يمرَّر run.correlationId فتُصبح الحوادث الناتجة قابلةً
    // للتتبّع إلى تشغيلتها (القسم 9: Incident → Source Agent → Run).
    await processIncidents(allResults, sb, run.correlationId);

    const critical = allResults.filter((r) => r.status === "critical").length;
    const warnings = allResults.filter((r) => r.status === "warning").length;
    // SUCCESS فقط إن لم يفشل جزءٌ جوهري من الفحص نفسه (استثناءٌ غير
    // ملتقَط) — وجود مكوّناتٍ حرجة/تحذيرية هو نتيجة فحصٍ ناجح لا فشلاً
    // في الوكيل نفسه، فيبقى SUCCESS مع تفاصيل النتيجة في result_summary.
    await finishRun(sb, run, {
      status: "SUCCESS",
      resultSummary: `${allResults.length} فحصاً — ${critical} حرج، ${warnings} تحذير`,
      recordsRead: allResults.length,
      recordsWritten: allResults.length,
    });

    return json({
      ok: true,
      timestamp: new Date().toISOString(),
      totalChecks: allResults.length,
      healthy: allResults.filter((r) => r.status === "healthy").length,
      warnings,
      critical,
      results: allResults,
      run_id: run.runId,
    });
  } catch (error) {
    console.error("❌ Health check error:", error);
    await finishRun(sb, run, { status: "FAILED", error: String(error) });
    return json({ error: String(error) }, 500);
  }
});
