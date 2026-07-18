// v2026.07.25 ════════════════════════════════════════════════════════════════
// Edge Function: summarize-lesson-pages
// تقرأ صفحات الكتاب المصوّرة لدرس واحد (نصاً وصوراً) مرة واحدة، وتنتج
// ملخصاً نصياً دقيقاً بمحتواه الفعلي — يُعاد استخدام هذا الملخص في كل
// عمليات التوليد اللاحقة للدرس نفسه (تحضير، أسئلة لعبة، إنفوجرافيك،
// عرض تقديمي) بدل إرفاق الصور الخام في كل استدعاء على حدة (أرخص وأسرع).
//
// النشر: تلقائي عبر GitHub Actions
// الأسرار: OPENROUTER_API_KEY
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

    // حصة اقتصادية (نص) رغم أن المدخل صور — المخرج نص قصير فقط
    const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
    if (!quota.ok) return json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const unit = String(b.unit || "");
    const lesson = String(b.lesson || "");
    const images: string[] = Array.isArray(b.images) ? b.images.slice(0, 16) : [];
    if (!images.length) return json({ error: "no_images" }, 400);

    const model = st.vision_model || "google/gemini-2.5-flash";

    const system = [
      "أنت مساعد بحث تربوي دقيق. أمامك صفحات درس واحد من كتاب طالب معتمد في سلطنة عُمان (منهج كامبردج).",
      "اقرأ الصفحات بدقّة تامة واستخرج ملخصاً نصياً كثيفاً بمحتواها الفعلي حصراً — لا تُضف أي معلومة من عندك ولا من معرفة عامة.",
      "اكتب: المفاهيم الأساسية بالترتيب، الأمثلة والأرقام والقواعد كما وردت حرفياً، الأنشطة أو التمارين الموجودة في الصفحات، وأي مصطلحات أو تعريفات نصّت عليها الصفحات.",
      "الملخص نصّ متصل بالعربية الفصحى بلا عناوين JSON — فقرات قصيرة مباشرة، بلا حشو ولا تعليق، ~250-450 كلمة.",
    ].join("\n");

    const userMsg = `الصف: ${grade} | المادة: ${subject}${unit ? " | الوحدة: " + unit : ""} | الدرس: ${lesson}`;
    const userContent: unknown[] = [{ type: "text", text: userMsg }];
    for (const u of images) userContent.push({ type: "image_url", image_url: { url: u } });

    const r = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Lesson Page Summarizer",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content: userContent },
        ],
        temperature: 0.2,
        max_tokens: 1200,
      }),
    });
    const or = await r.json();
    if (!r.ok) return json({ error: "provider_error", detail: or }, 502);
    const summary = (or?.choices?.[0]?.message?.content || "").trim();
    if (!summary) return json({ error: "no_summary" }, 502);
    return json({ summary, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
