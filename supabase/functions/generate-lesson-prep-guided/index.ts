// v2026.09.01 ════════════════════════════════════════════════════════════════
// Edge Function: generate-lesson-prep-guided
// (للمشرف فقط) يولّد تحضير درسٍ واحد من صفحاته في الكتاب المدرسي + دليل
// المعلم معاً (بعد مطابقة الفهرس عبر index-teacher-guide)، بتنسيقٍ يقلّد
// القالب المعتمد المخزَّن في ai_settings (prep_template_text). يُخزَّن
// الناتج في lesson_prep_generations كمسودة تنتظر اعتماد المشرف.
//
// النشر: تلقائي عبر GitHub Actions
// الأسرار: OPENROUTER_API_KEY
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { parseAiJson } from "../_shared/aiJson.ts";
import { orFetch, ensureVision, orErrCode } from "../_shared/ai.ts";
import { readDocxBytes, fillDocxTemplate, appendUnmatchedSections, writeDocxBytes, buildGenericDocx } from "../_shared/docx.ts";

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

    const apiKey = Deno.env.get("OPENROUTER_API_KEY");
    if (!apiKey) return json({ error: "server_not_configured" }, 500);

    const b = await req.json().catch(() => ({}));
    const curriculumId = parseInt(b.curriculum_id);
    const teacherGuideId = parseInt(b.teacher_guide_id);
    if (!curriculumId) return json({ error: "no_curriculum_id" }, 400);

    const { data: cur, error: cErr } = await admin.from("curriculum").select("*").eq("id", curriculumId).maybeSingle();
    if (cErr || !cur) return json({ error: "lesson_not_found" }, 404);

    const bookImages: string[] = Array.isArray(b.book_images) ? b.book_images.slice(0, 15) : [];
    const guideImages: string[] = Array.isArray(b.guide_images) ? b.guide_images.slice(0, 15) : [];
    if (!bookImages.length && !guideImages.length) return json({ error: "no_source_pages" }, 400);

    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
    const template = String(st.prep_template_text || "").slice(0, 6000);
    if (!template) return json({ error: "no_template" }, 400);

    const model = ensureVision(st.model_guided_prep || st.vision_model || "google/gemini-2.5-flash", "google/gemini-2.5-flash");

    const gradeNum = parseInt(String(cur.grade)) || 0;
    const age = gradeNum ? gradeNum + 6 : 0;

    const system = [
      "أنت خبير مناهج وطرائق تدريس متمرس في سلطنة عُمان.",
      "معك مصدران للصور: (أ) صفحات الدرس من كتاب الطالب المعتمد، (ب) صفحات نفس الدرس من دليل المعلم الرسمي (يحوي توجيهات تدريسية وأنشطة مقترحة من الوزارة).",
      "اقرأهما معاً بدقّة، وابنِ تحضيراً كاملاً لهذا الدرس اعتماداً على محتواهما الفعلي حصراً (لا من معرفة عامة) — استعمل توجيهات دليل المعلم تحديداً لتحديد الاستراتيجيات والأنشطة والتوقيت، واستعمل الكتاب لتحديد المحتوى والأمثلة والأسئلة.",
      "القالب المعتمد التالي هو مرجع التنسيق الرسمي المطلوب — اتبع هيكله وعناوين أقسامه وترتيبها بدقة (لا تخترع أقساماً غير موجودة فيه، ولا تُسقط قسماً منه):",
      "── بداية القالب ──",
      template,
      "── نهاية القالب ──",
      age ? `أعمار الطلاب: ${age} سنوات تقريباً (الصف ${cur.grade}) — راعِ ذلك في الصياغة والأنشطة.` : "",
      "صُغ بالعربية الفصحى بلغة تربوية رسمية دقيقة، والأرقام بالترقيم العربي-الهندي (٠١٢٣٤٥٦٧٨٩).",
      'أعد الناتج JSON فقط بهذا الشكل: {"title":"عنوان التحضير","sections":[{"heading":"عنوان القسم كما في القالب","body":"المحتوى التفصيلي لهذا القسم"}]}',
      "اجعل sections مطابقة تماماً لعدد وترتيب أقسام القالب أعلاه.",
    ].filter(Boolean).join("\n");

    const userMsg = [
      `الصف: ${cur.grade} | المادة: ${cur.subject}`,
      `الوحدة: ${cur.unit}`,
      `الدرس: ${cur.lesson}`,
    ].join("\n");

    const userContent: unknown[] = [{ type: "text", text: userMsg }];
    if (bookImages.length) {
      userContent.push({ type: "text", text: "── صفحات الكتاب المدرسي ──" });
      for (const u of bookImages) userContent.push({ type: "image_url", image_url: { url: u } });
    }
    if (guideImages.length) {
      userContent.push({ type: "text", text: "── صفحات دليل المعلم ──" });
      for (const u of guideImages) userContent.push({ type: "image_url", image_url: { url: u } });
    }

    const callOnce = async () => {
      const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Guided Prep Generator",
        },
        body: JSON.stringify({
          model,
          messages: [
            { role: "system", content: system },
            { role: "user", content: userContent },
          ],
          response_format: { type: "json_object" },
          temperature: 0.4,
          max_tokens: 4000,
        }),
      }, { st, task: "guided_prep" });
      const j = await r.json();
      if (!r.ok) return { ok: false as const, status: r.status, msg: String(j?.error?.message || j?.message || "") };
      const text = j?.choices?.[0]?.message?.content || "";
      const pp = parseAiJson<{ title?: string; sections?: unknown[] }>(text);
      const val = pp.ok ? pp.value : null;
      if (!val || !Array.isArray(val.sections) || !val.sections.length) return { ok: false as const, detail: text.slice(0, 300) };
      return { ok: true as const, content: val, usage: j?.usage || null };
    };

    let attempt = await callOnce();
    if (!attempt.ok) attempt = await callOnce();
    if (!attempt.ok) {
      const st_ = (attempt as { status?: number }).status;
      const m_ = (attempt as { msg?: string }).msg || "";
      if (st_) {
        console.error(`openrouter ${st_} في generate-lesson-prep-guided: ${m_}`);
        return json({ error: orErrCode(st_, m_), detail: m_.slice(0, 200) }, 502);
      }
      return json({ error: "bad_output", detail: (attempt as { detail?: string }).detail }, 502);
    }

    // بناء ملف Word الفعلي: إن كان القالب المعتمد مرفوعاً كـWord، نحقن كل
    // قسمٍ مولَّد داخل نسخةٍ من ملف القالب نفسه (بعد فقرة عنوانه المطابقة)
    // فيخرج التحضير بنفس تنسيق القالب حرفياً. غياب قالب Word (قالبٌ من PDF
    // فقط، أو لم يُرفع بعد) يُنتج مستنداً عاماً بسيطاً بدلاً منه.
    const sections = (attempt.content.sections || []) as { heading?: string; body?: string }[];
    const cleanSections = sections.map((s) => ({ heading: String(s.heading || ""), body: String(s.body || "") }));
    let docxBytes: Uint8Array;
    try {
      if (st.prep_template_ext === "docx") {
        const { data: tplBlob, error: tplErr } = await admin.storage.from("library-files").download("prep-template/template.docx");
        if (tplErr || !tplBlob) throw new Error("template_missing");
        const tplBytes = new Uint8Array(await tplBlob.arrayBuffer());
        const { zip, documentXml } = await readDocxBytes(tplBytes);
        const filled = fillDocxTemplate(documentXml, cleanSections);
        const withExtras = appendUnmatchedSections(filled.xml, cleanSections, filled.unmatched);
        docxBytes = await writeDocxBytes(zip, withExtras);
      } else {
        docxBytes = await buildGenericDocx(String(attempt.content.title || cur.lesson), cleanSections);
      }
    } catch (e) {
      console.error("docx_build_failed:", String(e));
      docxBytes = await buildGenericDocx(String(attempt.content.title || cur.lesson), cleanSections);
    }

    const docxPath = `generated-preps/${curriculumId}.docx`;
    const { error: docxUpErr } = await admin.storage.from("library-files").upload(docxPath, docxBytes, {
      contentType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      upsert: true,
    });
    let docxUrl: string | null = null;
    if (docxUpErr) console.error("docx_upload_failed:", docxUpErr.message);
    else docxUrl = admin.storage.from("library-files").getPublicUrl(docxPath).data.publicUrl;

    const { data: saved, error: upErr } = await admin.from("lesson_prep_generations").upsert({
      curriculum_id: curriculumId,
      teacher_guide_id: teacherGuideId || null,
      semester: cur.semester,
      grade: cur.grade,
      subject: cur.subject,
      unit: cur.unit,
      lesson: cur.lesson,
      content: attempt.content,
      docx_url: docxUrl,
      status: "draft",
      model,
      created_by: user.id,
    }, { onConflict: "curriculum_id" }).select().single();
    if (upErr) { console.error("db_error:", upErr.message); return json({ error: "db_error" }, 500); }

    return json({ generation: saved, model, usage: attempt.usage });
  } catch (e) {
    console.error("server_error:", String(e));
    return json({ error: "server_error" }, 500);
  }
});
