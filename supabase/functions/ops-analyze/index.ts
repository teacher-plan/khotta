// ════════════════════════════════════════════════════════════════
// Edge Function: ops-analyze
// KHOTTA Autonomous Management — Phase 2 (Ops Intelligence) +
// المحرّك المستعمَل من Phase 3 (Incident Intelligence) للتحليل الإثرائي.
//
// action:"health"  — لقطةٌ حتمية بلا ذكاء اصطناعي إطلاقاً (قواعد/SQL فقط).
// action:"analyze" — يُستدعى فقط عند شذوذٍ فعليّ (حادثةٌ من system-health-
//                    check، أو طلب مشرفٍ صريح) — يجمع أدلّةً من الأدوات
//                    الثابتة ثم نداءٌ واحدٌ للذكاء الاصطناعي، لا حلقة.
//
// الاستدعاء: مفتاح الخدمة (الوكلاء المجدولة) أو جلسة مشرفٍ مصادَقة
// (authorizeOps — يتحقّق من is_app_admin() على الخادم، لا في الواجهة).
//
// النشر: supabase functions deploy ops-analyze
// الأسرار: OPENROUTER_API_KEY (يُعاد استعمالها — لا سرٌّ جديد)
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { authorizeOps, unauthorized } from "../_shared/adminGuard.ts";
import { orFetch } from "../_shared/ai.ts";
import { logAiCost } from "../_shared/quota.ts";
import { parseAiJson } from "../_shared/aiJson.ts";
import {
  get_system_health, get_recent_errors, get_emergency_alerts,
  get_ai_usage, get_ai_cost, get_quota_status, get_database_health,
  get_edge_function_health, get_recent_deployments, get_recent_incidents,
} from "../_shared/opsTools.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const auth = await authorizeOps(req);
    if (!auth.ok) return unauthorized(cors);

    const admin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    const b = await req.json().catch(() => ({}));
    const action = String(b.action || "health");

    // ═ action:"health" — بلا ذكاء اصطناعي، قواعدٌ حتمية فقط ═
    if (action === "health") {
      const [health, errors, alerts, dbHealth, fnHealth, incidents] = await Promise.all([
        get_system_health(admin),
        get_recent_errors(admin, 1),
        get_emergency_alerts(admin),
        get_database_health(admin),
        get_edge_function_health(admin),
        get_recent_incidents(admin, 5),
      ]);

      const severity =
        health.critical > 0 || dbHealth.status === "critical" ? "P1"
        : health.warning > 0 || dbHealth.status === "warning" ? "P2"
        : "P3";
      const status = severity === "P1" ? "incident" : severity === "P2" ? "degraded" : "healthy";

      return json({
        status,
        severity,
        summary: status === "healthy"
          ? "كل المكوّنات المفحوصة سليمة."
          : `${health.critical} مكوّناً حرجاً و${health.warning} تحذيراً في آخر ١٥ دقيقة.`,
        evidence: [
          { source: "get_system_health", data: health, confidence: "VERIFIED" },
          { source: "get_database_health", data: dbHealth, confidence: "VERIFIED" },
          { source: "get_recent_errors", data: errors, confidence: "VERIFIED" },
          { source: "get_emergency_alerts", data: alerts, confidence: "VERIFIED" },
          { source: "get_edge_function_health", data: fnHealth, confidence: "VERIFIED" },
        ],
        likely_causes: [],   // حتميّ فقط — لا استنتاج بلا استدعاء analyze صريح
        confidence: 1,
        affected_components: health.components.filter((c: { status: string }) => c.status !== "healthy").map((c: { component_name: string }) => c.component_name),
        affected_users: null,
        recommendations: status === "healthy" ? [] : ["استدعِ action:\"analyze\" لتحليلٍ أعمق بالذكاء الاصطناعي إن استمرّت المشكلة."],
        open_incidents: incidents.incidents,
        generated_at: new Date().toISOString(),
      });
    }

    // ═ action:"cost" — بلا ذكاء اصطناعي أيضاً: ملخّص تكلفةٍ مباشر ═
    if (action === "cost") {
      const cost = await get_ai_cost(admin);
      return json({ cost, generated_at: new Date().toISOString() });
    }

    // ═ action:"analyze" — شذوذٌ فعليّ فقط: جمع أدلّة ثم نداءٌ واحد ═
    if (action === "analyze") {
      const component = String(b.component || "").slice(0, 100);
      const hint = String(b.hint || "").slice(0, 500);

      const [health, errors, alerts, dbHealth, fnHealth, aiCost, quota] = await Promise.all([
        get_system_health(admin),
        get_recent_errors(admin, 3),
        get_emergency_alerts(admin),
        get_database_health(admin),
        get_edge_function_health(admin),
        get_ai_cost(admin),
        get_quota_status(admin),
      ]);
      const deployments = get_recent_deployments();

      const evidence = { health, errors, alerts, dbHealth, fnHealth, aiCost, quota, deployments };
      const schema = JSON.stringify({
        status: "healthy|degraded|incident",
        severity: "P0|P1|P2|P3",
        summary: "جملةٌ أو جملتان بالعربية الفصحى، بلا مصطلحاتٍ تقنية غير مشروحة",
        evidence: ["إشارة كل دليلٍ استُند إليه من البيانات المُعطاة فقط"],
        likely_causes: [{ cause: "...", confidence: "VERIFIED|LIKELY|UNKNOWN" }],
        confidence: 0,
        affected_components: ["..."],
        affected_users: null,
        recommendations: ["إجراءٌ مقترح — توصيةٌ لا تنفيذ"],
      });

      const system = [
        "أنت محلّل عمليات (Ops) لمنصّة KHOTTA التعليمية. تحصل على أدلّةٍ حقيقية من قواعد بيانات المنصّة فقط.",
        "قاعدةٌ صارمة: لا تذكر سبباً كحقيقةٍ مؤكَّدة (VERIFIED) إلا إذا كان مذكوراً حرفياً في الأدلّة المُعطاة. أي استنتاجٍ غير مؤكَّدٍ من الأدلّة صراحةً فصنّفه LIKELY، وما لا دليل عليه إطلاقاً فاتركه أو صنّفه UNKNOWN.",
        "لا تخترع أرقاماً ولا أسماء مستخدمين ولا تواريخ غير موجودة في الأدلّة.",
        "أنت للتوصية لا للتنفيذ: لا تقترح تنفيذاً تلقائياً، فقط توصيةً يقرّرها المشرف البشري.",
        component ? `المكوّن المتأثّر: ${component}` : "",
        hint ? `سياقٌ إضافي: ${hint}` : "",
        `أعد الناتج JSON فقط بهذا الشكل حصراً: ${schema}`,
      ].filter(Boolean).join("\n");

      const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + (Deno.env.get("OPENROUTER_API_KEY") || ""),
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Ops Analyze",
        },
        body: JSON.stringify({
          model: "deepseek/deepseek-chat",
          messages: [
            { role: "system", content: system },
            { role: "user", content: "الأدلّة (JSON):\n" + JSON.stringify(evidence).slice(0, 12000) },
          ],
          response_format: { type: "json_object" },
          temperature: 0.2,
          max_tokens: 1200,
        }),
      }, { task: "ops" });

      const or = await r.json();
      // تكلفة العمليات تُسجَّل بمعزلٍ عن تكلفة المستخدمين (kind='ops')،
      // ولا تُخصَم من حصة أي معلّمة — لا نداء takeQuota هنا إطلاقاً.
      await logAiCost(admin, auth.userId || null, "ops-analyze", "ops", "deepseek/deepseek-chat", or?.usage);

      if (!r.ok) {
        return json({ status: "unknown", severity: "P3", summary: "تعذّر تحليل الذكاء الاصطناعي — الأدلّة الخام متاحة دون تفسير.",
          evidence: [{ source: "raw", data: evidence, confidence: "VERIFIED" }], likely_causes: [], confidence: 0,
          affected_components: [], affected_users: null, recommendations: [], llm_error: true }, 200);
      }
      const text = or?.choices?.[0]?.message?.content || "";
      const parsed = parseAiJson(text);
      if (!parsed.ok) {
        return json({ status: "unknown", severity: "P3", summary: "تعذّر تفسير مخرجات الذكاء الاصطناعي.",
          evidence: [{ source: "raw", data: evidence, confidence: "VERIFIED" }], likely_causes: [], confidence: 0,
          affected_components: [], affected_users: null, recommendations: [], llm_error: true }, 200);
      }
      return json({ ...(parsed.value as Record<string, unknown>), raw_evidence: evidence, generated_at: new Date().toISOString() });
    }

    return json({ error: "unknown_action" }, 400);
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
