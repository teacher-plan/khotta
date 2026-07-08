// ════════════════════════════════════════════════════════════════
// Edge Function: generate-lesson-plan
// مساعد التحضير اليومي — يولّد خطة حصة (45 دقيقة) منظمة لدرس محدد
// بنموذج نصي اقتصادي، وتُخزَّن في lesson_preps لإعادة الاستخدام.
//
// النشر:  supabase functions deploy generate-lesson-plan
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
    const unit = String(b.unit || "");
    const lesson = String(b.lesson || "");
    if (!lesson) return json({ error: "no_lesson" }, 400);

    const model = st.ai_model || "google/gemini-2.5-flash";

    const schema = JSON.stringify({
      objectives: ["هدف تعليمي قابل للقياس"],
      materials: ["وسيلة أو أداة"],
      phases: [{ name: "التمهيد", minutes: 5, detail: "وصف عملي دقيق لما يفعله المعلم والطلاب" }],
      quickQuestions: [{ q: "سؤال تقييم ختامي", a: "إجابته النموذجية" }],
      homework: "واجب منزلي قصير مناسب",
      tip: "نصيحة تربوية ذكية خاصة بهذا الدرس",
    });

    const system = [
      "أنت خبير تربوي عُماني متمرس في إعداد خطط الحصص وفق مناهج سلطنة عُمان.",
      "أعدّ خطة حصة واحدة (45 دقيقة) عملية وواقعية ينفذها المعلم مباشرة دون تعديل.",
      "المراحل الإلزامية بالترتيب: التمهيد (5د) — العرض والشرح (20د) — نشاط تطبيقي (10د) — التقويم (8د) — الغلق (2د). لكل مرحلة detail عملي محدد (ماذا يقول المعلم، ماذا يفعل الطلاب) لا عبارات عامة.",
      "3-4 أهداف قابلة للقياس تبدأ بفعل سلوكي (يميّز، يحسب، يستنتج...).",
      "3 أسئلة تقييم ختامية متدرجة الصعوبة مع إجاباتها النموذجية.",
      "نشاط تطبيقي تفاعلي مناسب للعمل الثنائي أو الجماعي بأدوات متاحة في أي صف عماني.",
      "صُغ بالعربية الفصحى وبمستوى الصف المحدد.",
      `أعد الناتج JSON فقط بهذا الشكل حصراً: ${schema}`,
      st.ppt_system_prompt ? "" : "",
    ].filter(Boolean).join("\n");

    const userMsg = [
      `الصف: ${grade} | المادة: ${subject}`,
      unit ? `الوحدة: ${unit}` : "",
      `الدرس: ${lesson}`,
    ].filter(Boolean).join("\n");

    const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Lesson Prep",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content: userMsg },
        ],
        response_format: { type: "json_object" },
        temperature: 0.4,
        max_tokens: 2500,
      }),
    });
    const or = await orResp.json();
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);

    const text = or?.choices?.[0]?.message?.content || "";
    let plan: unknown;
    try { plan = JSON.parse(text); }
    catch (_) { const m = text.match(/\{[\s\S]*\}/); plan = m ? JSON.parse(m[0]) : null; }
    if (!plan || !(plan as { phases?: unknown[] }).phases) {
      return json({ error: "bad_output", detail: text.slice(0, 300) }, 502);
    }
    return json({ plan, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
