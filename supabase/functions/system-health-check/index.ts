// وكيل مراقبة صحة النظام (System Health Check)
// يفحص جميع المكونات كل 5 دقائق ويرسل تنبيهات طارئة عند المشاكل

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendTelegram } from "../_shared/telegram.ts";

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

  for (const fn of functions) {
    try {
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
          signal: AbortSignal.timeout(5000), // timeout بـ 5 ثوانٍ
        }
      );
      const duration = Date.now() - start;

      if (response.status === 200 || response.status === 201) {
        results.push({
          component: `function:${fn}`,
          status: "healthy",
          responseTime: duration,
          severity: 1,
        });
      } else {
        results.push({
          component: `function:${fn}`,
          status: response.status >= 500 ? "critical" : "warning",
          responseTime: duration,
          error: `HTTP ${response.status}`,
          severity: response.status >= 500 ? 4 : 2,
        });
      }
    } catch (error) {
      results.push({
        component: `function:${fn}`,
        status: "critical",
        error: String(error),
        severity: 4,
      });
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

    // التحقق من حجم التخزين
    const { data: stats } = await sb.rpc("database_size");
    if (stats && stats.database_size_mb > 4500) {
      results.push({
        component: "database:storage",
        status: "warning",
        error: `Storage: ${stats.database_size_mb}MB / 5000MB`,
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
      await sb.from("emergency_alerts").insert({
        alert_type: issue.component.split(":")[1],
        severity: issue.severity,
        title: `🚨 مشكلة حرجة: ${issue.component}`,
        description: issue.error,
        affected_component: issue.component,
        action_required: getActionForComponent(issue.component, issue.error),
      });

      // إرسال تنبيه فوري عبر Telegram
      const alertMessage = `
🚨 <b>تنبيه حرج من نظام الصحة</b>
━━━━━━━━━━━━━━━━━━━━━━
<b>المشكلة:</b> ${issue.component}
<b>الخطورة:</b> ${issue.severity}/5
<b>الخطأ:</b> ${issue.error || "غير معروف"}
<b>الإجراء:</b> ${getActionForComponent(issue.component, issue.error)}

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

  try {
    const sb = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    const baseUrl = Deno.env.get("SUPABASE_URL")!;
    const anonKey = Deno.env.get("SUPABASE_ANON_KEY")!;

    console.log("🔍 بدء فحص صحة النظام...");

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

    // معالجة النتائج وإرسال التنبيهات
    await processHealthResults(allResults, sb);

    return json({
      ok: true,
      timestamp: new Date().toISOString(),
      totalChecks: allResults.length,
      healthy: allResults.filter((r) => r.status === "healthy").length,
      warnings: allResults.filter((r) => r.status === "warning").length,
      critical: allResults.filter((r) => r.status === "critical").length,
      results: allResults,
    });
  } catch (error) {
    console.error("❌ Health check error:", error);
    return json({ error: String(error) }, 500);
  }
});
