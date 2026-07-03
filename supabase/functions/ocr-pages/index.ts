// ════════════════════════════════════════════════════════════════
// Edge Function: ocr-pages
// يقرأ صور صفحات كتاب مدرسي عبر نموذج رؤية (Gemini) ويعيد نصّ كل صفحة
// كما هو — لتجاوز مشكلة الخطوط المشوّهة في استخراج نصّ الـ PDF.
//
// النشر:  supabase functions deploy ocr-pages
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
    const model = st.vision_model || "google/gemini-2.5-flash";

    const b = await req.json().catch(() => ({}));
    const images: string[] = Array.isArray(b.images) ? b.images : [];
    if (!images.length) return json({ error: "no_images" }, 400);
    if (images.length > 8) return json({ error: "too_many_images" }, 400);

    const schema = '{"pages":["نص الصفحة ١","نص الصفحة ٢"]}';
    const system = [
      "أنت أداة OCR دقيقة لكتب مدرسية عربية.",
      "استخرج كل النصّ العربي المقروء من كل صورة صفحة كما هو، بالترتيب الصحيح للقراءة (يمين إلى يسار).",
      "لا تلخّص ولا تشرح ولا تضف شيئاً. انسخ العناوين والفقرات والأسئلة كما تظهر.",
      "مهم جداً — تعليم عناوين الدروس فقط: عنوان الدرس الرئيسي يظهر في أعلى الصفحة بأكبر خطّ في الصفحة، ويفتتح درساً كاملاً يمتدّ عدة صفحات. ضع قبله فقط العلامة «§§ » في سطر مستقل ثم العنوان.",
      "كن متحفّظاً جداً: عناوين الدروس قليلة (لا يوجد عنوان درس في كل صفحة). لا تضع §§ إلا للعنوان الرئيسي الأكبر الذي يبدأ درساً جديداً.",
      "ممنوع منعاً باتاً وضع §§ لأيٍّ مما يلي: العناوين الفرعية داخل الدرس، وكلمات مثل (نشاط، تجربة، تحقّق من فهمك، أسئلة، تمارين، تقويم، مراجعة، إثراء، مفردات، أهداف)، وعناوين الصور والجداول والأشكال، وترويسة/تذييل الصفحة، وصفحة الفهرس/المحتويات.",
      "القاعدة الحاسمة: §§ فقط للعنوان الذي تجده مطابقاً لاسم درس في فهرس الكتاب. عند الشكّ، لا تضع العلامة.",
      "تجاهل أرقام الصفحات والزخارف. صف المعادلات بصياغة نصّية بسيطة إن وُجدت.",
      "أعد JSON فقط: مصفوفة pages نصّ كل صفحة بنفس ترتيب الصور المُعطاة.",
    ].join("\n");

    const content: unknown[] = [
      { type: "text", text: `اقرأ الصفحات التالية (بالترتيب) وأعد نصّ كل صفحة بهذا الشكل حصراً (JSON): ${schema}` },
    ];
    for (const img of images) content.push({ type: "image_url", image_url: { url: img } });

    const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta OCR Pages",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content },
        ],
        response_format: { type: "json_object" },
        temperature: 0,
        max_tokens: 8000,
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
      parsed = m ? JSON.parse(m[0]) : { pages: [] };
    }
    const pages = (parsed as { pages?: unknown[] })?.pages || [];
    return json({ pages, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
