// ════════════════════════════════════════════════════════════════
// Edge Function: generate-infographic
// يولّد إنفوجرافيك تعليمي مرسوم (بأسلوب NotebookLM) لدرس محدد
// عبر نموذج توليد الصور Gemini 3 Pro Image (Nano Banana Pro) من OpenRouter.
// المفتاح يبقى سرياً على الخادم — نفس مفتاح generate-exam.
//
// النشر:  supabase functions deploy generate-infographic
// الأسرار: OPENROUTER_API_KEY
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
    const lessonNames: string[] = Array.isArray(b.lessonNames) ? b.lessonNames.map(String) : [];
    const teacherPrompt = String(b.teacherPrompt || "").slice(0, 1500);
    const size = ["1K", "2K", "4K"].includes(b.size) ? b.size : "2K";
    const aspect = ["9:16", "3:4", "1:1", "16:9", "21:9", "2:3", "4:3"].includes(b.aspect) ? b.aspect : "9:16";
    if (!lessonNames.length) return json({ error: "no_lessons" }, 400);

    // نموذج الصور — موحّد مع مولّد الشرائح (مفتاح slide_model في ai_settings)
    const model = st.slide_model || st.info_model || "google/gemini-2.5-flash-image";

    // نمط بصري ثابت مستوحى من إنفوجرافيك NotebookLM (باستيل + رسوم كرتونية تعليمية)
    const stylePrompt = st.info_style_prompt || [
      "أسلوب بصري: إنفوجرافيك تعليمي عمودي (portrait poster) بأسلوب مرح واحترافي في آن واحد.",
      "خلفية مقسمة لمناطق بألوان باستيل ناعمة متمايزة (أزرق فاتح، أصفر كريمي، وردي فاتح، أخضر نعناعي) بحدود منحنية انسيابية.",
      "رسوم كرتونية مسطحة لطيفة توضح كل مفهوم (أشكال هندسية مقسمة للكسور، نرد، مسطرة، شخصيات مبتسمة، أيقونات ملونة).",
      "عنوان رئيسي ضخم أعلى الملصق بالعربية بخط عريض واضح.",
      "كل قسم له عنوان فرعي داخل شارة (badge) ملونة، ومحتوى مختصر بنقاط قصيرة.",
      "أرقام وأمثلة رياضية مكتوبة بوضوح تام وخط كبير.",
      "النص العربي يجب أن يكون دقيقاً إملائياً ومقروءاً بوضوح — هذا أهم شرط.",
      "لا صور فوتوغرافية، لا نص إنجليزي إلا للمصطلحات بين قوسين.",
    ].join(" ");

    const userPrompt = [
      `أنشئ إنفوجرافيك تعليمياً واحداً متكاملاً بالعربية الفصحى لطلاب ${grade ? "الصف " + grade : "المدرسة"} في مادة ${subject}.`,
      `موضوع الدرس/الدروس: ${lessonNames.join("، ")}.`,
      "لخّص أهم المفاهيم والقواعد والأمثلة في أقسام واضحة مرقّمة (أولاً، ثانياً، ثالثاً...) مع تمثيل بصري مرسوم لكل مفهوم.",
      teacherPrompt ? `توجيهات المعلم: ${teacherPrompt}` : "",
      stylePrompt,
      `توجه التصميم: ${["16:9", "21:9"].includes(aspect) ? "أفقي عريض — وزّع الأقسام جنباً إلى جنب" : aspect === "1:1" ? "مربع متوازن" : "عمودي طولي — الأقسام فوق بعضها"}.`,
    ].filter(Boolean).join("\n");

    // بعض النماذج لا تقبل كل إعدادات المقاس/الجودة — نحاول كاملة ثم نتدرّج تلقائياً
    const call = (cfg: Record<string, unknown> | null) =>
      fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Infographic Generator",
        },
        body: JSON.stringify({
          model,
          messages: [{ role: "user", content: userPrompt }],
          modalities: ["image", "text"],
          ...(cfg ? { image_config: cfg } : {}),
        }),
      });
    // النماذج غير جوجل (مثل Seedream) تعمل عبر واجهة الصور الموحدة /v1/images فقط
    const callImagesApi = async () => {
      const r = await fetch("https://openrouter.ai/api/v1/images", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Infographic Generator",
        },
        body: JSON.stringify({ model, prompt: userPrompt, resolution: size, aspect_ratio: aspect }),
      });
      const j = await r.json();
      if (!r.ok) return { ok: false, detail: j, img: "" };
      const d = j?.data?.[0] || {};
      const img = d.b64_json ? "data:image/png;base64," + d.b64_json : (d.url || "");
      return { ok: !!img, detail: j, img };
    };

    let img = "";
    let usage: unknown = null;
    if (model.startsWith("google/")) {
      let orResp = await call({ aspect_ratio: aspect, image_size: size });
      let or = await orResp.json();
      if (!orResp.ok) { orResp = await call({ aspect_ratio: aspect }); or = await orResp.json(); }
      if (!orResp.ok) { orResp = await call(null); or = await orResp.json(); }
      if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);
      const msg = or?.choices?.[0]?.message;
      img = msg?.images?.[0]?.image_url?.url || "";
      usage = or?.usage || null;
      if (!img) return json({ error: "no_image", detail: msg?.content || null }, 502);
    } else {
      const r = await callImagesApi();
      if (!r.ok) return json({ error: "provider_error", detail: r.detail }, 502);
      img = r.img;
    }

    return json({ image: img, model, usage });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
