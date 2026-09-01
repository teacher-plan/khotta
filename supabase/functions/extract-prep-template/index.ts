// v2026.09.01 ════════════════════════════════════════════════════════════════
// Edge Function: extract-prep-template
// (للمشرف فقط) يقرأ القالب المعتمد المرفوع (Word أو PDF) ويستخرج نصّه
// كمرجع تنسيقٍ يُرسَل للذكاء الاصطناعي عند توليد كل تحضير — دون أي كتابةٍ
// يدوية. ملف Word يبقى محفوظاً كهيكلٍ حرفي (skeleton) يُستعمل لاحقاً في
// generate-lesson-prep-guided لحقن المحتوى داخله بنفس تنسيقه بالضبط.
//
// النشر: تلقائي عبر GitHub Actions
// الأسرار: OPENROUTER_API_KEY (لقالب PDF فقط — القراءة بالرؤية)
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { readDocxBytes, docxPlainText } from "../_shared/docx.ts";
import { orFetch, ensureVision, orErrCode } from "../_shared/ai.ts";

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

const ADMIN_EMAIL = "teacherplane2026project@gmail.com";

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
    if ((user.email || "").toLowerCase() !== ADMIN_EMAIL) return json({ error: "forbidden" }, 403);

    const b = await req.json().catch(() => ({}));
    const ext = String(b.ext || "").toLowerCase();
    if (ext !== "docx" && ext !== "pdf") return json({ error: "bad_ext" }, 400);

    let templateText = "";

    if (ext === "docx") {
      const { data: blob, error: dlErr } = await admin.storage.from("library-files").download("prep-template/template.docx");
      if (dlErr || !blob) return json({ error: "template_not_found" }, 404);
      const bytes = new Uint8Array(await blob.arrayBuffer());
      const { documentXml } = await readDocxBytes(bytes);
      templateText = docxPlainText(documentXml);
      if (!templateText.trim()) return json({ error: "empty_template" }, 400);
    } else {
      // PDF: صور صفحاته مرفوعة مسبقاً من العميل (نفس نمط دليل المعلم) تحت
      // prep-template/pN.jpg — نقرأها بالرؤية لاستخراج عناوين أقسامه بالترتيب.
      const pageCount = parseInt(b.page_count) || 0;
      if (!pageCount) return json({ error: "no_page_count" }, 400);

      const apiKey = Deno.env.get("OPENROUTER_API_KEY");
      if (!apiKey) return json({ error: "server_not_configured" }, 500);
      const { data: rows } = await admin.from("ai_settings").select("key,value");
      const st: Record<string, string> = {};
      (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
      const model = ensureVision(st.model_guide_index || st.vision_model || "google/gemini-2.5-flash", "google/gemini-2.5-flash");

      const images: string[] = [];
      for (let i = 1; i <= Math.min(pageCount, 20); i++) {
        images.push(admin.storage.from("library-files").getPublicUrl(`prep-template/p${i}.jpg`).data.publicUrl);
      }
      const system = [
        "أمامك صور صفحات قالب تحضير درسٍ معتمد (نموذج فارغ أو شبه فارغ للتنسيق الرسمي).",
        "استخرج نصّ عناوين أقسامه بترتيبها الفعلي كما تظهر في الصفحات (كل عنوان قسمٍ في سطر مستقل)، متجاهلاً أي بيانات تعبئة (تاريخ، اسم معلّم...) لا تخصّ محتوى الدرس نفسه.",
        "أعد النص فقط، سطراً لكل عنوان قسم، بلا أي شرحٍ إضافي.",
      ].join("\n");
      const userContent: unknown[] = [{ type: "text", text: "صور صفحات القالب:" }];
      for (const u of images) userContent.push({ type: "image_url", image_url: { url: u } });

      const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Template Extractor",
        },
        body: JSON.stringify({
          model,
          messages: [{ role: "system", content: system }, { role: "user", content: userContent }],
          temperature: 0.1,
          max_tokens: 1500,
        }),
      }, { st, task: "template_extract" });
      const j = await r.json();
      if (!r.ok) {
        const m = String(j?.error?.message || j?.message || "");
        console.error(`openrouter ${r.status} في extract-prep-template: ${m}`);
        return json({ error: orErrCode(r.status, m), detail: m.slice(0, 200) }, 502);
      }
      templateText = String(j?.choices?.[0]?.message?.content || "").trim();
      if (!templateText) return json({ error: "no_text_extracted" }, 502);
    }

    await admin.from("ai_settings").upsert([
      { key: "prep_template_text", value: templateText },
      { key: "prep_template_ext", value: ext },
    ], { onConflict: "key" });

    return json({ template_text: templateText, ext });
  } catch (e) {
    console.error("server_error:", String(e));
    return json({ error: "server_error" }, 500);
  }
});
