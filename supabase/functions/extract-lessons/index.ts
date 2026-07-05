// ════════════════════════════════════════════════════════════════
// Edge Function: extract-lessons
// يقرأ صورة «فهرس» كتاب مدرسي عبر نموذج رؤية (Gemini) ويعيد
// قائمة الوحدات والدروس مرتّبة — ليعتمدها المشرف في المنهج.
// المفتاح يبقى سرياً على الخادم.
//
// النشر:  supabase functions deploy extract-lessons
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

    // نموذج رؤية (Gemini يدعم الصور والعربية). قابل للضبط من ai_settings.vision_model
    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
    const model = st.vision_model || "google/gemini-2.5-flash";

    const b = await req.json().catch(() => ({}));
    const images: string[] = Array.isArray(b.images) ? b.images : (b.image ? [b.image] : []);
    if (!images.length) return json({ error: "no_image" }, 400);

    const schema =
      '{"units":[{"unit":"اسم الوحدة","lessons":[{"name":"اسم الدرس","page":12}]}]}';

    const system = [
      "أنت مساعد يستخرج فهرس محتويات كتاب مدرسي عُماني من صورة.",
      "استخرج أسماء الوحدات، وتحت كل وحدة أسماء الدروس بالترتيب كما تظهر، ومع كل درس رقم صفحة بدايته المذكور أمامه في الفهرس.",
      "page = رقم الصفحة كما هو مكتوب في الفهرس أمام الدرس (رقم صحيح). إن لم يظهر رقم لدرس، اجعل page = 0.",
      "لا تختلق أي درس غير موجود في الصورة. تجاهل العناوين العامة (مقدمة/فهرس/تمهيد).",
      "إن لم توجد وحدات صريحة، اجعل الدروس تحت وحدة باسم «عام».",
      "أعد JSON فقط دون أي نص خارجه.",
    ].join("\n");

    const content: unknown[] = [
      { type: "text", text: `استخرج الوحدات والدروس وأرقام صفحاتها بهذا الشكل حصراً (JSON): ${schema}` },
    ];
    for (const img of images.slice(0, 6)) {
      content.push({ type: "image_url", image_url: { url: img } });
    }

    const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Lessons Extractor",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content },
        ],
        response_format: { type: "json_object" },
        temperature: 0.1,
        max_tokens: 4000,
      }),
    });

    const or = await orResp.json();
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);

    const text = or?.choices?.[0]?.message?.content || "";
    let parsed: unknown;
    try {
      parsed = JSON.parse(text);
    } catch (_) {
      const m = text.match(/\{[\s\S]*\}/);
      parsed = m ? JSON.parse(m[0]) : { units: [] };
    }

    const units = (parsed as { units?: unknown[] })?.units || [];
    return json({ units, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
