// ════════════════════════════════════════════════════════════════
// Edge Function: generate-exam
// تولّد أسئلة اختبار عبر OpenRouter من محتوى الدروس المحدّدة.
// مفتاح OpenRouter يبقى سرياً على الخادم ولا يصل أبداً لكود المتصفح.
// تُفرض حدود المشرف (التفعيل/أقصى أسئلة/الأنواع/النموذج) على الخادم.
//
// النشر:  supabase functions deploy generate-exam
// الأسرار المطلوبة (Supabase → Edge Functions → Secrets):
//   OPENROUTER_API_KEY = مفتاح OpenRouter (sk-or-v1-...)
//   (SUPABASE_URL و SUPABASE_SERVICE_ROLE_KEY متوفّران تلقائياً)
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

const TYPE_LABELS: Record<string, string> = {
  mcq: "اختيار من متعدد (مع 4 خيارات في options)",
  essay: "مقالي",
  tf: "صح وخطأ",
  fill: "إكمال الفراغ",
  match: "توصيل (عمودان: colA و colB مصفوفتان متساويتان)",
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

    // مصادقة المعلم
    const jwt = authHeader.replace("Bearer ", "");
    const { data: { user }, error: userErr } = await admin.auth.getUser(jwt);
    if (userErr || !user) return json({ error: "unauthorized" }, 401);

    const apiKey = Deno.env.get("OPENROUTER_API_KEY");
    if (!apiKey) return json({ error: "server_not_configured" }, 500);

    // إعدادات المولّد التي يضبطها المشرف (تُفرض على الخادم)
    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });

    if (st.generator_enabled === "0") return json({ error: "disabled" }, 403);

    const model = st.ai_model || "deepseek/deepseek-chat";
    const maxQ = parseInt(st.max_questions || "30") || 30;
    const allowedTypes = (st.allowed_types || "mcq,essay,tf,fill,match").split(",");
    const adminPrompt = st.system_prompt || "";

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const lessons = Array.isArray(b.lessons) ? b.lessons : [];
    let types = (Array.isArray(b.types) ? b.types : []).filter((t: string) => allowedTypes.includes(t));
    if (!types.length) types = ["mcq"];
    const count = Math.max(1, Math.min(maxQ, parseInt(b.count) || 10));
    const teacherPrompt = String(b.teacherPrompt || "").slice(0, 2000);
    // مرفقات المعلم: مرجع لتوليد دقيق من المحتوى، ونموذج لمحاكاة الأسلوب والتنسيق
    const referenceText = String(b.referenceText || "").slice(0, 60000);
    const sampleExam = String(b.sampleExam || "").slice(0, 30000);

    if (!lessons.length) return json({ error: "no_lessons" }, 400);

    // بناء سياق الدروس: النص الفعلي إن توفّر، وإلا الاسم فقط
    const lessonCtx = lessons.map((l: { name?: string; text?: string }, i: number) => {
      const name = l.name || `درس ${i + 1}`;
      const text = (l.text || "").slice(0, 12000);
      return text ? `### ${name}\n${text}` : `### ${name}`;
    }).join("\n\n");

    const typesList = types.map((t: string) => TYPE_LABELS[t] || t).join("، ");

    const system = [
      "أنت معلّم خبير في إعداد الاختبارات المدرسية في سلطنة عُمان.",
      "صُغ الأسئلة باللغة العربية الفصحى السليمة، وفق مستوى الصف الدراسي المحدد.",
      referenceText
        ? "استند حصراً إلى «المرجع» المُرفق لصياغة الأسئلة؛ لا تختلق معلومات خارجه. إن لم يغطِّ المرجع نقطة، فتجاهلها."
        : "استند إلى محتوى الدروس المُعطى. إن لم يتوفّر نص كافٍ، استعمل الموضوع المعروف للدرس بحذر.",
      sampleExam
        ? "حاكِ أسلوب «النموذج» المُرفق وتنسيقه وصياغته وتوزيع درجاته قدر الإمكان، دون نسخ أسئلته حرفياً."
        : "",
      "أعِد الناتج بصيغة JSON فقط دون أي نص خارج JSON.",
      adminPrompt,
    ].filter(Boolean).join("\n");

    const schema =
      '{"questions":[{"type":"mcq|essay|tf|fill|match","question":"نص السؤال",' +
      '"options":["خيار أ","خيار ب","خيار ج","خيار د"],' +
      '"colA":["..."],"colB":["..."]}]}';

    const userMsg = [
      `الصف: ${grade} | المادة: ${subject}`,
      `أنواع الأسئلة المطلوبة: ${typesList}`,
      `العدد الإجمالي للأسئلة: ${count}`,
      teacherPrompt ? `توجيهات المعلم: ${teacherPrompt}` : "",
      "",
      "محتوى الدروس:",
      lessonCtx,
      referenceText ? `\n=== المرجع (استند إليه حصراً) ===\n${referenceText}` : "",
      sampleExam ? `\n=== نموذج للاختبار (حاكِ أسلوبه وتنسيقه فقط) ===\n${sampleExam}` : "",
      "",
      `أعد النتيجة بهذا الشكل حصراً (JSON): ${schema}`,
      "options تُملأ فقط لأسئلة mcq. colA/colB فقط لأسئلة match. وزّع الأنواع المطلوبة على العدد الإجمالي.",
    ].filter(Boolean).join("\n");

    const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Exam Generator",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content: userMsg },
        ],
        response_format: { type: "json_object" },
        temperature: 0.6,
        max_tokens: 8000,
      }),
    });

    const or = await orResp.json();
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);

    const content = or?.choices?.[0]?.message?.content || "";
    let parsed: unknown;
    try {
      parsed = JSON.parse(content);
    } catch (_) {
      // بعض النماذج تحيط JSON بنص — نحاول استخراج أول كائن
      const m = content.match(/\{[\s\S]*\}/);
      parsed = m ? JSON.parse(m[0]) : { questions: [] };
    }

    const questions = (parsed as { questions?: unknown[] })?.questions || [];
    return json({ questions, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
