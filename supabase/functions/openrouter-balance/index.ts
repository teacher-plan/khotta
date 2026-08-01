// v2026.07.09 ════════════════════════════════════════════════════════════════
// Edge Function: openrouter-balance
// يعيد رصيد حساب OpenRouter الفعلي (للمشرف فقط) لعرضه في تبويب الميزانية.
//
// النشر:  supabase functions deploy openrouter-balance
// الأسرار: OPENROUTER_API_KEY
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { orKeys } from "../_shared/ai.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
};
function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) return json({ error: "unauthorized" }, 401);

    // عميل بهوية المستخدم نفسه للتحقق أنه مشرف المنصة عبر is_app_admin()
    const userClient = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
      { global: { headers: { Authorization: authHeader } } },
    );
    const { data: { user } } = await userClient.auth.getUser();
    if (!user) return json({ error: "unauthorized" }, 401);
    const { data: isAdmin } = await userClient.rpc("is_app_admin");
    if (!isAdmin) return json({ error: "forbidden" }, 403);

    const keys = orKeys();
    if (!keys.length) return json({ error: "server_not_configured" }, 500);

    // رصيد كل مفتاح على حدة: المجموع وحده يُخفي أن أحدها على وشك النفاد،
    // وهو ما يوقف المهامّ المسندة إليه وإن بقي في غيره رصيد وفير.
    const per = await Promise.all(keys.map(async (k, i) => {
      try {
        const r = await fetch("https://openrouter.ai/api/v1/credits", {
          headers: { "Authorization": "Bearer " + k },
        });
        const j = await r.json();
        if (!r.ok) return { key: i + 1, ok: false, error: String(j?.error?.message || r.status) };
        const total = Number(j?.data?.total_credits ?? 0);
        const used = Number(j?.data?.total_usage ?? 0);
        return { key: i + 1, ok: true, total, used, remaining: Math.max(0, total - used) };
      } catch (e) {
        return { key: i + 1, ok: false, error: String(e) };
      }
    }));

    const live = per.filter((p) => p.ok) as { total: number; used: number; remaining: number }[];
    const total = live.reduce((s, p) => s + p.total, 0);
    const used = live.reduce((s, p) => s + p.used, 0);
    // total/used/remaining تبقى كما كانت: شاشات قديمة تقرؤها ولا تعرف keys
    return json({ total, used, remaining: Math.max(0, total - used), keys: per });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
