// v2026.07.09 ════════════════════════════════════════════════════════════════
// Edge Function: generate-presentation
// يولّد شرائح عرض تقديمي (عنوان + نقاط) من محتوى المكتبة المعتمد.
// يقرأ صور صفحات الدرس (رؤية) إن توفّرت، وإلا يعتمد على أسماء الدروس فقط.
// المفتاح يبقى سرياً على الخادم.
//
// النشر:  supabase functions deploy generate-presentation
// الأسرار: OPENROUTER_API_KEY (نفس مفتاح generate-exam)
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { takeQuota } from "../_shared/quota.ts";

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

    // ⛔ حصة الاستخدام الشهرية — تُفرض على الخادم
    const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
    if (!quota.ok) return json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);
    // برومبت خاص للعروض التقديمية إن ضبطه المشرف، وإلا نرجع للعام
    const adminPrompt = st.ppt_system_prompt || st.system_prompt || "";

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const lessonNames: string[] = Array.isArray(b.lessonNames) ? b.lessonNames.map(String) : [];
    const images: string[] = Array.isArray(b.images) ? b.images.slice(0, 40) : [];
    const slideCount = Math.max(3, Math.min(20, parseInt(b.slideCount) || 8));
    const teacherPrompt = String(b.teacherPrompt || "").slice(0, 2000);
    if (!lessonNames.length) return json({ error: "no_lessons" }, 400);

    // النموذج الذي يختاره المشرف من لوحة التحكم (ارفع الجودة باختيار Claude Sonnet مثلاً).
    // عند إرفاق صور صفحات الكتاب نحتاج نموذجاً يدعم الرؤية، فنرجع لنموذج الرؤية إن كان المختار لا يدعمها.
    let model = st.ai_model || st.vision_model || "google/gemini-2.5-flash";
    if (images.length && /deepseek/i.test(model)) model = st.vision_model || "google/gemini-2.5-flash";

    const schema =
      '{"slides":[{"title":"عنوان الشريحة","bullets":["نقطة أولى","نقطة ثانية"],"notes":"ملاحظات شرح للمعلم لهذه الشريحة"}]}';

    const system = [
      "أنت معلّم خبير في إعداد عروض تقديمية تعليمية احترافية (PowerPoint) في سلطنة عُمان.",
      images.length
        ? "الصور المرفقة هي صفحات الدرس من كتاب الطالب. اقرأها بدقّة وابنِ الشرائح من محتواها حصراً."
        : "لا توجد صور مرفقة؛ اعتمد على اسم/أسماء الدرس المذكورة وابنِ شرائح تعليمية عالية الجودة حولها.",
      "ابنِ عرضاً متكاملاً بتسلسل تربوي: شريحة أهداف الدرس، ثم شرائح تشرح المفاهيم الرئيسية واحداً تلو الآخر بتدرّج، ثم شريحة مثال/تطبيق، ثم شريحة نشاط أو سؤال للطلاب، وأخيراً شريحة خلاصة ومراجعة.",
      "كل شريحة: عنوان واضح قصير + 3-5 نقاط مختصرة ومفيدة (لا فقرات طويلة، ولا حشو).",
      "لكل شريحة اكتب في حقل notes ملاحظات شرح موجزة للمعلم (ما يقوله أو يركّز عليه) — جملتان إلى ثلاث.",
      "صُغ بالعربية الفصحى وفق مستوى الصف، بلغة تعليمية جذّابة ودقيقة.",
      "أعد الناتج بصيغة JSON فقط دون أي نص خارجه.",
      adminPrompt,
    ].filter(Boolean).join("\n");

    const content: unknown[] = [
      { type: "text", text: [
        `الصف: ${grade} | المادة: ${subject}`,
        `الدرس/الدروس: ${lessonNames.join("، ")}`,
        `عدد الشرائح المطلوب تقريباً: ${slideCount}`,
        teacherPrompt ? `توجيهات المعلم: ${teacherPrompt}` : "",
        `أعد النتيجة بهذا الشكل حصراً (JSON): ${schema}`,
      ].filter(Boolean).join("\n") },
    ];
    for (const url of images) content.push({ type: "image_url", image_url: { url } });

    const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Presentation Generator",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content },
        ],
        response_format: { type: "json_object" },
        temperature: 0.5,
        max_tokens: 6000,
      }),
    });
    const or = await orResp.json();
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);

    const text = or?.choices?.[0]?.message?.content || "";
    let parsed: unknown;
    try { parsed = JSON.parse(text); }
    catch (_) { const m = text.match(/\{[\s\S]*\}/); parsed = m ? JSON.parse(m[0]) : { slides: [] }; }
    const slides = (parsed as { slides?: unknown[] })?.slides || [];
    return json({ slides, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
