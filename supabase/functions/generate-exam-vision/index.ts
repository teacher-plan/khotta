// v2026.07.09 ════════════════════════════════════════════════════════════════
// Edge Function: generate-exam-vision
// يولّد أسئلة اختبار من صور صفحات الدرس (رؤية) — الذكاء يقرأ الصفحات
// مباشرةً فيتجاوز مشكلة الخطوط المشوّهة ويفهم المعادلات والأشكال.
// المعلم لا يحمّل شيئاً؛ نمرّر روابط الصور العامة ويجلبها المزوّد.
//
// النشر:  supabase functions deploy generate-exam-vision
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

const TYPE_LABELS: Record<string, string> = {
  mcq: "اختيار من متعدد (مع 4 خيارات في options)",
  essay: "مقالي",
  tf: "صح وخطأ",
  fill: "إكمال الفراغ",
  match: "توصيل (colA و colB مصفوفتان متساويتان)",
};

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
    const model = st.vision_model || "google/gemini-2.5-flash";
    const maxQ = parseInt(st.max_questions || "30") || 30;
    const allowedTypes = (st.allowed_types || "mcq,essay,tf,fill,match").split(",");
    const adminPrompt = st.system_prompt || "";

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const lessonNames: string[] = Array.isArray(b.lessonNames) ? b.lessonNames.map(String) : [];
    const images: string[] = Array.isArray(b.images) ? b.images.slice(0, 40) : [];
    let types = (Array.isArray(b.types) ? b.types : []).filter((t: string) => allowedTypes.includes(t));
    if (!types.length) types = ["mcq"];
    const count = Math.max(1, Math.min(maxQ, parseInt(b.count) || 10));
    const total = Math.max(1, Math.min(100, parseInt(b.total) || 20));
    const teacherPrompt = String(b.teacherPrompt || "").slice(0, 2000);
    if (!images.length) return json({ error: "no_images" }, 400);

    const typesList = types.map((t: string) => TYPE_LABELS[t] || t).join("، ");
    const schema =
      '{"questions":[{"type":"mcq|essay|tf|fill|match","question":"نص السؤال",' +
      '"options":["خيار أ","خيار ب","خيار ج","خيار د"],"colA":["..."],"colB":["..."]}]}';

    const system = [
      "أنت معلّم خبير في إعداد الاختبارات المدرسية في سلطنة عُمان.",
      "الصور المرفقة هي صفحات الدرس من كتاب الطالب. اقرأها بدقّة (نصّاً ومعادلاتٍ وأشكالاً) وابنِ الأسئلة من محتواها حصراً.",
      "لا تسأل عن شيء غير موجود في هذه الصفحات. صُغ بالعربية الفصحى وفق مستوى الصف.",
      "أعد الناتج بصيغة JSON فقط دون أي نص خارجه.",
      adminPrompt,
    ].filter(Boolean).join("\n");

    const content: unknown[] = [
      { type: "text", text: [
        `الصف: ${grade} | المادة: ${subject}`,
        lessonNames.length ? `الدرس: ${lessonNames.join("، ")}` : "",
        `أنواع الأسئلة: ${typesList} | العدد: ${count} | الدرجة الكلية: ${total}`,
        teacherPrompt ? `توجيهات المعلم: ${teacherPrompt}` : "",
        `اقرأ صفحات الدرس التالية وأعد النتيجة بهذا الشكل حصراً (JSON): ${schema}`,
        "options لأسئلة mcq فقط. colA/colB لأسئلة match فقط.",
      ].filter(Boolean).join("\n") },
    ];
    for (const url of images) content.push({ type: "image_url", image_url: { url } });

    const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Exam Generator (Vision)",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content },
        ],
        response_format: { type: "json_object" },
        temperature: 0.5,
        max_tokens: 8000,
      }),
    });
    const or = await orResp.json();
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);

    const text = or?.choices?.[0]?.message?.content || "";
    let parsed: unknown;
    try { parsed = JSON.parse(text); }
    catch (_) { const m = text.match(/\{[\s\S]*\}/); parsed = m ? JSON.parse(m[0]) : { questions: [] }; }
    const questions = (parsed as { questions?: unknown[] })?.questions || [];
    return json({ questions, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
