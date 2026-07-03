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
    const headings: string[] = Array.isArray(b.headings) ? b.headings.map(String) : [];
    if (!lessons.length || !headings.length) return json({ error: "bad_input" }, 400);

    const system = [
      "أنت أداة دقيقة لمطابقة أسماء الدروس بعناوينها المستخرجة من كتاب مدرسي.",
      "لديك: (١) قائمة «عناوين» مرقّمة استُخرجت من الكتاب بالترتيب، (٢) قائمة «دروس» المنهج بالترتيب.",
      "لكل درس في قائمة الدروس، أعِد رقم العنوان الأقرب له معنىً من قائمة العناوين (الرقم كما هو مُعطى).",
      "طابق بالمعنى لا بالحروف: قد تختلف الصياغة قليلاً بين اسم الدرس وعنوانه في الكتاب.",
      "راعِ الترتيب: الدروس والعناوين مرتّبة عموماً بنفس التسلسل، فاستعن بذلك عند التشابه.",
      "لا تُكرّر تعيين نفس العنوان لأكثر من درس إن أمكن. إن لم يوجد عنوان مناسب لدرس، أعِد -1 له.",
      "أعد JSON فقط: {\"matches\":[رقم العنوان للدرس الأول, رقم العنوان للدرس الثاني, ...]} بنفس ترتيب قائمة الدروس وعددها.",
    ].join("\n");

    const userMsg =
      "قائمة العناوين المستخرجة (الرقم ثم العنوان):\n" +
      headings.map((h, i) => `${i}: ${h}`).join("\n") +
      "\n\nقائمة دروس المنهج بالترتيب:\n" +
      lessons.map((l, i) => `${i + 1}. ${l}`).join("\n") +
      "\n\nأعِد لكل درس رقم العنوان الأنسب من القائمة الأولى (JSON).";

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
