// ════════════════════════════════════════════════════════════════
// Edge Function: ops-copilot
// KHOTTA Autonomous Management — Phase 4 (Admin Copilot)
//
// سؤالٌ حرّ بالعربية عن حالة المنصّة → تصنيفٌ بالكلمات المفتاحية لتحديد
// الأدوات اللازمة (لا استدعاء الكلّ دائماً — كلفةٌ وسياقٌ محدودان) →
// نداءٌ واحدٌ للذكاء الاصطناعي على الأدلّة المجموعة → إجابة.
//
// لا حلقة أدواتٍ (agentic loop): جمعٌ واحد، نداءٌ واحد، إجابةٌ واحدة —
// يمنع الحلقات وسقف التكلفة يبقى معروفاً مسبقاً لكل سؤال.
//
// القراءة فقط: لا أداة كتابة إطلاقاً هنا. المشرف حصراً (authorizeOps
// وليس مفتاح الخدمة — هذا الطريق للبشر لا للوكلاء المجدولة).
//
// النشر: supabase functions deploy ops-copilot
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { authorizeOps, unauthorized } from "../_shared/adminGuard.ts";
import { orFetch } from "../_shared/ai.ts";
import { logAiCost } from "../_shared/quota.ts";
import {
  get_system_health, get_recent_errors, get_emergency_alerts,
  get_ai_usage, get_ai_cost, get_quota_status, get_database_health,
  get_edge_function_health, get_recent_deployments, get_recent_incidents,
  get_database_capacity, get_agent_registry, get_agent_runs_summary,
} from "../_shared/opsTools.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
}

// تصنيفٌ بالكلمات المفتاحية — لا LLM يختار الأدوات (يمنع حلقة اختيارٍ
// إضافية ويُبقي التكلفة والزمن متوقَّعين). كلماتٌ متعدّدة قد تُفعِّل أكثر
// من فئة لنفس السؤال، وهذا مقصود — أفضل من إغفال دليلٍ ذي صلة.
function classify(q: string) {
  const s = q.toLowerCase();
  return {
    health: /صحة|مشكل|حال|يعمل|عطل|خطأ|status|health|error/.test(s),
    cost: /تكلف|صرف|فلوس|دولار|cost|\$|مال/.test(s),
    incidents: /حادث|incident|مشكل|خلل/.test(s),
    users: /مستخدم|معلم|user|استهلاك/.test(s),
    deploy: /نشر|deploy|تحديث|آخر تغيير/.test(s),
    capacity: /حجم|سعة|تخزين|قاعدة البيانات|capacity|storage|database size|مساحة|نمو/.test(s),
    agents: /وكيل|وكلاء|agent|جدولة|autonomy|استقلال/.test(s),
  };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const auth = await authorizeOps(req);
    // الـcopilot للمشرف البشري حصراً — لا مفتاح الخدمة، ولا مستخدمٍ غير مشرف.
    if (!auth.ok || auth.isService) return unauthorized(cors);

    const admin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    const b = await req.json().catch(() => ({}));
    const question = String(b.question || "").trim().slice(0, 500);
    if (!question) return json({ error: "no_question" }, 400);

    const cat = classify(question);
    // حزمةٌ ثابتة صغيرة دائماً (حالة النظام) + ما صنّفه السؤال فقط.
    const jobs: Record<string, Promise<unknown>> = {
      health: get_system_health(admin),
      dbHealth: get_database_health(admin),
    };
    if (cat.health) jobs.errors = get_recent_errors(admin, 24);
    if (cat.health) jobs.alerts = get_emergency_alerts(admin);
    if (cat.health) jobs.fnHealth = get_edge_function_health(admin);
    if (cat.cost || cat.users) jobs.aiCost = get_ai_cost(admin);
    if (cat.cost) jobs.aiUsage = get_ai_usage(admin);
    if (cat.cost) jobs.quota = get_quota_status(admin);
    if (cat.incidents) jobs.incidents = get_recent_incidents(admin, 15);
    if (cat.deploy) jobs.deployments = get_recent_deployments();
    if (cat.capacity) jobs.databaseCapacity = get_database_capacity(admin);
    if (cat.agents) jobs.agentRegistry = get_agent_registry(admin);
    if (cat.agents) jobs.agentRuns = get_agent_runs_summary(admin, 24);

    // تشخيصٌ مؤقّت: نفصل جمع الأدلّة عن نداء الذكاء الاصطناعي بخطأٍ بنيوي
    // مسمّى — فلو رمت أداةٌ استثناءً نعرف أيّها بالضبط، لا رسالةً عامة تُشبه
    // فشل الصلاحية أو فشل المزوّد. لا تغييرٌ في التفويض أو المزوّد أو الحصص.
    const keys = Object.keys(jobs);
    const settled = await Promise.allSettled(Object.values(jobs));
    const failedTools = keys.filter((_, i) => settled[i].status === "rejected");
    if (failedTools.length) {
      const detail = failedTools
        .map((k) => `${k}: ${String((settled[keys.indexOf(k)] as PromiseRejectedResult).reason)}`)
        .join(" | ");
      return json({ error: "tool_failed", tool: failedTools.join(","), detail }, 500);
    }
    const evidence: Record<string, unknown> = {};
    keys.forEach((k, i) => { evidence[k] = (settled[i] as PromiseFulfilledResult<unknown>).value; });

    const system = [
      "أنت مساعد عمليات KHOTTA — تجيب مدير المنصّة (غير تقنيّ بالضرورة) بالعربية الفصحى.",
      "قاعدةٌ صارمة: لا تُجب من معرفةٍ عامة، أجب من الأدلّة المُعطاة فقط.",
      "إن لم تكفِ الأدلّة للإجابة، قل حرفياً: «لا أملك بيانات كافية للإجابة على هذا السؤال».",
      "إن كانت الأدلّة جزئية، ابدأ بـ«بناءً على البيانات المتاحة…».",
      "إن كان استنتاجك احتمالياً لا مؤكَّداً من الأدلّة صراحةً، قل «السبب المحتمل…» ولا تقل «السبب هو» أبداً إلا مع دليلٍ قاطع.",
      "أسئلة سعة قاعدة البيانات (الحجم/النسبة/النمو/التوقّع): إن كانت البيانات في الأدلّة \"INSUFFICIENT_DATA\" أو \"NOT_AVAILABLE\" فقل ذلك حرفياً، ولا تحسب أو تقدّر رقماً غير موجود في الأدلّة إطلاقاً.",
      "لا تقترح أي إجراءٍ تنفيذي تلقائي — توصيةٌ للمشرف يقرّرها هو، لا تنفيذ.",
      "لا تخترع أسماء مستخدمين أو أرقاماً أو تواريخ غير موجودة في الأدلّة.",
      "أعد الناتج JSON فقط بالشكل التالي:",
      JSON.stringify({
        manager_summary: "جملةٌ أو جملتان بلغةٍ إدارية بسيطة، بلا مصطلحاتٍ تقنية",
        technical_details: "تفاصيل تقنية عند الحاجة، أو نصٌّ فارغ إن لم تلزم",
        confidence: "VERIFIED|LIKELY|UNKNOWN|INSUFFICIENT_DATA",
      }),
    ].join("\n");

    const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + (Deno.env.get("OPENROUTER_API_KEY") || ""),
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Ops Copilot",
      },
      body: JSON.stringify({
        model: "deepseek/deepseek-chat",
        messages: [
          { role: "system", content: system },
          { role: "user", content: `السؤال: ${question}\n\nالأدلّة (JSON):\n${JSON.stringify(evidence).slice(0, 10000)}` },
        ],
        response_format: { type: "json_object" },
        temperature: 0.2,
        max_tokens: 700, // سقفٌ صريح — إجابةٌ واحدة موجزة، لا مقالة
      }),
    }, { task: "ops" });

    const or = await r.json();
    await logAiCost(admin, auth.userId || null, "ops-copilot", "ops", "deepseek/deepseek-chat", or?.usage);

    if (!r.ok) return json({ manager_summary: "تعذّر الوصول إلى مساعد التحليل الآن.", technical_details: null, confidence: "INSUFFICIENT_DATA" });

    const text = or?.choices?.[0]?.message?.content || "";
    let parsed: Record<string, unknown> | null = null;
    try { parsed = JSON.parse(text); } catch { /* يبقى null */ }

    if (!parsed || typeof parsed.manager_summary !== "string") {
      return json({ manager_summary: "لا أملك بيانات كافية للإجابة على هذا السؤال.", technical_details: null, confidence: "INSUFFICIENT_DATA" });
    }
    return json({
      manager_summary: parsed.manager_summary,
      technical_details: parsed.technical_details || null,
      confidence: parsed.confidence || "UNKNOWN",
      evidence_categories_used: keys,
    });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
