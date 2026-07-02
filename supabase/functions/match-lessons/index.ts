// ════════════════════════════════════════════════════════════════
// Edge Function: match-lessons
// مطابقة دلالية: تتلقّى نصّ كتاب + قائمة أسماء دروس (بالترتيب)،
// وتعيد لكل درس «مقتطفاً حرفياً» من الموضع الذي يبدأ فيه في النصّ —
// ليحدّد المتصفّح مكانه بدقّة ويقطّع، حتى لو اختلفت صياغة العنوان.
//
// النشر:  supabase functions deploy match-lessons
// الأسرار: OPENROUTER_API_KEY (نفس مفتاح generate-exam)
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

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

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) return json({ error: "unauthorized" }, 401);
    const admin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );
    const jwt = authHeader.replace("Bearer ", "");
    const { data: { user }, error: userErr } = await admin.auth.getUser(jwt);
    if (userErr || !user) return json({ error: "unauthorized" }, 401);

    const apiKey = Deno.env.get("OPENROUTER_API_KEY");
    if (!apiKey) return json({ error: "server_not_configured" }, 500);

    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
    const model = st.ai_model || "deepseek/deepseek-chat";

    const b = await req.json().catch(() => ({}));
    const lessons: string[] = Array.isArray(b.lessons) ? b.lessons.map(String) : [];
    const text = String(b.text || "").slice(0, 220000);
    if (!lessons.length || !text) return json({ error: "bad_input" }, 400);

    const system = [
      "أنت أداة دقيقة لتحديد مواضع بدء الدروس داخل نصّ كتاب مدرسي.",
      "لكل درس في القائمة (بالترتيب)، جد الموضع الذي يبدأ فيه ذلك الدرس في النصّ، وانسخ حرفياً أول 6 إلى 10 كلمات متتالية من ذلك الموضع كما وردت في النصّ تماماً (لا تعدّلها ولا تترجمها).",
      "طابق بالمعنى لا بالحروف: قد تختلف صياغة العنوان في القائمة عن النصّ.",
      "إن لم تجد الدرس في النصّ، اجعل قيمته سلسلة فارغة.",
      "أعد JSON فقط بهذا الشكل: {\"matches\":[\"مقتطف الدرس الأول\",\"مقتطف الدرس الثاني\"]} بنفس ترتيب القائمة وعددها.",
    ].join("\n");

    const userMsg = "قائمة الدروس بالترتيب:\n" +
      lessons.map((l, i) => `${i + 1}. ${l}`).join("\n") +
      "\n\n=== نصّ الكتاب ===\n" + text;

    const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Match Lessons",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content: userMsg },
        ],
        response_format: { type: "json_object" },
        temperature: 0,
        max_tokens: 6000,
      }),
    });
    const or = await orResp.json();
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);

    const content = or?.choices?.[0]?.message?.content || "";
    let parsed: unknown;
    try { parsed = JSON.parse(content); }
    catch (_) { const m = content.match(/\{[\s\S]*\}/); parsed = m ? JSON.parse(m[0]) : { matches: [] }; }
    const matches = (parsed as { matches?: unknown[] })?.matches || [];
    return json({ matches, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
