// ════════════════════════════════════════════════════════════════
// Edge Function: generate-slide-image
// يرسم شريحة عرض تقديمي واحدة (16:9) بالكامل بالذكاء الاصطناعي
// بأسلوب NotebookLM — تُستدعى مرة لكل شريحة من واجهة المولّد.
// النموذج: Gemini 3 Pro Image (Nano Banana Pro) عبر OpenRouter.
//
// النشر:  supabase functions deploy generate-slide-image
// الأسرار: OPENROUTER_API_KEY (نفس مفتاح بقية الدوال)
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
    if (st.generator_enabled === "0") return json({ error: "disabled" }, 403);

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const title = String(b.title || "").slice(0, 200);
    const bullets: string[] = (Array.isArray(b.bullets) ? b.bullets : []).map(String).slice(0, 8);
    const slideNo = Math.max(1, parseInt(b.slideNo) || 1);
    const slideTotal = Math.max(1, parseInt(b.slideTotal) || 1);
    const kind = ["cover", "content", "closing"].includes(b.kind) ? b.kind : "content";
    if (!title) return json({ error: "no_title" }, 400);

    // نموذج الرسم الموحّد — يُبدَّل من ai_settings (مفتاح slide_model) بدون نشر
    const model = st.slide_model || "google/gemini-2.5-flash-image";

    // نظام بصري موحّد لكل شرائح العرض الواحد — قابل للتخصيص من ai_settings
    const style = st.slide_style_prompt || [
      "أسلوب بصري موحّد: شريحة عرض تقديمي تعليمية عريضة (16:9) بأسلوب إنفوجرافيك مرح واحترافي.",
      "خلفية كريمية دافئة فاتحة مع مناطق باستيل ناعمة (أزرق فاتح، أصفر كريمي، أخضر نعناعي، وردي فاتح) بحدود منحنية انسيابية.",
      "رسوم كرتونية مسطحة لطيفة توضح المفاهيم (أشكال هندسية، أيقونات ملونة، شخصيات مبتسمة صغيرة).",
      "خط عربي عريض واضح جداً، عنوان كبير، ونقاط منظمة كل واحدة مع رسمة توضيحية صغيرة بجانبها.",
      "ترقيم الشريحة في زاوية سفلية داخل دائرة ملونة صغيرة.",
      "النص العربي يجب أن يكون دقيقاً إملائياً ومقروءاً تماماً — أهم شرط على الإطلاق.",
      "لا صور فوتوغرافية، ولا نص غير المطلوب حرفياً أدناه.",
    ].join(" ");

    const kindPrompt = kind === "cover"
      ? `هذه شريحة الغلاف الافتتاحية: اجعل العنوان ضخماً في المنتصف مع رسوم احتفالية مرحة حول الموضوع، وشارة ملونة تحمل «${subject}${grade ? " — الصف " + grade : ""}».`
      : kind === "closing"
        ? "هذه الشريحة الختامية: صمّمها كخلاصة/شكر بأسلوب دافئ مع رسمة معبّرة كبيرة."
        : "هذه شريحة محتوى: العنوان أعلى الشريحة، والنقاط موزّعة بتنظيم واضح كل نقطة مع رسمة توضيحية مناسبة لمعناها.";

    const userPrompt = [
      `ارسم شريحة عرض تقديمي تعليمية واحدة (الشريحة ${slideNo} من ${slideTotal}) لمادة ${subject}${grade ? " للصف " + grade : ""}.`,
      kindPrompt,
      `العنوان (اكتبه حرفياً): «${title}»`,
      bullets.length ? `النقاط (اكتبها حرفياً كما هي):\n${bullets.map((x, i) => `${i + 1}. ${x}`).join("\n")}` : "",
      style,
    ].filter(Boolean).join("\n");

    // إن رفض النموذج إعداد المقاس نعيد المحاولة بدونه بدل إفشال الشريحة
    const call = (cfg: Record<string, unknown> | null) =>
      fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Visual Slides",
        },
        body: JSON.stringify({
          model,
          messages: [{ role: "user", content: userPrompt }],
          modalities: ["image", "text"],
          ...(cfg ? { image_config: cfg } : {}),
        }),
      });
    let orResp = await call({ aspect_ratio: "16:9" });
    let or = await orResp.json();
    if (!orResp.ok) { orResp = await call(null); or = await orResp.json(); }
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);

    const msg = or?.choices?.[0]?.message;
    const img = msg?.images?.[0]?.image_url?.url || "";
    if (!img) return json({ error: "no_image", detail: msg?.content || null }, 502);

    return json({ image: img, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
