// v2026.09.06 ════════════════════════════════════════════════════════════════
// Edge Function: generate-lesson-prep-guided
// (للمشرف فقط) يولّد تحضير درسٍ واحد من صفحاته في الكتاب المدرسي + دليل
// المعلم معاً (بعد مطابقة الفهرس عبر index-teacher-guide)، بهيكل التحضير
// المعتمد في منصة نور (سبعة أقسامٍ ثابتة — انظر NOOR_SECTIONS أدناه)، لا
// بقالب Word مرفوع (أُلغي هذا المسار: التسليم الفعلي في نور نفسه، فالمعلمة
// تنسخ كل قسمٍ من معاينة الشاشة إلى حقل نور المقابل مباشرة). يُخزَّن الناتج
// في lesson_prep_generations كمسودة تنتظر اعتماد المشرف.
//
// النشر: تلقائي عبر GitHub Actions
// الأسرار: OPENROUTER_API_KEY
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { parseAiJson } from "../_shared/aiJson.ts";
import { orFetch, ensureVision, orErrCode } from "../_shared/ai.ts";
import { buildGenericDocx } from "../_shared/docx.ts";

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

// هيكل التحضير المعتمد في منصة نور — ثابتٌ لكل درسٍ ومادة، لا يتغيّر بتغيّر
// قالبٍ مرفوع. استُخرج من نموذج تحضيرٍ فعلي اعتمده الأستاذ عيسى (تحضير
// «سورة الحشر» — تربية إسلامية، صف عاشر) وأكّد أن هذا هو العمق والتفصيل
// المطلوبان فعلياً لكل درس، وليسا مبالغةً في مثالٍ واحد.
const NOOR_SECTIONS = [
  {
    heading: "المخرجات التعليمية والمستوى التعليمي",
    guidance: "٣-٥ مخرجات، كل واحدٍ بصيغة «أن يفعل الطالب...» (قراءة/فهم/تطبيق/تقويم حسب طبيعة الدرس)، مبنية حصراً على محتوى الكتاب ودليل المعلم لهذا الدرس. اختم بسطر «المستوى التعليمي: ...» يسمّي مستويات بلوم التي تغطيها المخرجات مجتمعة.",
  },
  {
    heading: "الاستراتيجيات والمصادر التعليمية والمفاهيم",
    guidance: "بنودٌ فرعية بعناوين صريحة كلٌّ في سطره: «الاستراتيجيات:»، «المصادر والوسائل:»، «المفاهيم:»، «المفردات:»، «المهارات:»، وإن اقتضت طبيعة المادة (كأحكام تلاوة أو مواضع وقف في التربية الإسلامية، أو قواعد سلامة في العلوم) أضف «الضبط المنهجي:» — احذفه إن لم يكن للدرس ما يستدعيه.",
  },
  {
    heading: "التهيئة / التعلم القبلي",
    guidance: "فقرة سردية تصف موقفاً أو سؤالاً افتتاحياً يربط الدرس بمعرفة الطلاب السابقة، ثم سطر منفصل يبدأ بـ«التحقق من التعلم القبلي:» يصف كيف يتأكد المعلم من جاهزية الطلاب قبل الدخول في الدرس.",
  },
  {
    heading: "إجراءات سير الدرس والأنشطة",
    guidance: "القسم الأكبر والأهم — سلسلة خطواتٍ مرقّمة متتابعة، عددها يتبع طبيعة الدرس نفسه ولا يلتزم رقماً ثابتاً (درسٌ غنيٌّ بالأنشطة يحتاج خطواتٍ أكثر من درسٍ قصير) — المطلوب تغطية ما يحتاجه هذا الدرس فعلاً بعمقٍ عملي، لا بلوغ عددٍ معيّن ولا اختصارٌ مخلّ. تغطّي بالترتيب ما يناسب الدرس من: تثبيت هدف الحصة، الأنشطة الرئيسية للدرس بالتفصيل العملي (ماذا يفعل المعلم بالضبط وماذا يقول، وماذا يفعل الطلاب)، أسئلة المعلم المتدرجة (اذكرها كقائمة أسئلة فعلية مبنية على محتوى الدرس)، نشاط تطبيقي مركب، دعم المتعثرين، إثراء المتقدمين، تغذية راجعة منظمة، مؤشرات الأداء التي يلاحظها المعلم، معالجة الخطأ المتوقع الشائع لهذا الدرس تحديداً، تنظيم المشاركة والوقت، مهمة فردية تثبت الفهم، مراجعة بالأقران، إعادة تعليم فورية للمتعثرين، وتوثيق أثر التعلم استعداداً للغلق. كل خطوة رقمٌ متسلسل يبدأ بعنوان قصير ثم شرح تفصيلي عملي — لا عناوين عامة بلا تفصيل.",
  },
  {
    heading: "التقويم التكويني",
    guidance: "فقرة تصف آلية المتابعة أثناء الحصة (أسئلة شفهية بعد كل خطوة، اختيار طلاب متفاوتي المستوى...)، ثم سطر يبدأ بـ«معيار النجاح أثناء الحصة:» يحدد ما يُعتبر أداءً مقبولاً.",
  },
  {
    heading: "التقويم الختامي / غلق الدرس",
    guidance: "أداة تقويم ختامي محددة (بطاقة خروج، سؤال ختامي، أو ما يناسب طبيعة الدرس) بتفاصيلها، ثم فقرة «غلق الدرس:» تلخّص الدرس وتوجّه الطلاب لموضع المراجعة في الكتاب أو التدريب المقرر — بلا أي واجب أو معلومة غير واردة في المصدر.",
  },
];

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

    const model = ensureVision(st.model_guided_prep || st.vision_model || "google/gemini-2.5-flash", "google/gemini-2.5-flash");

    const gradeNum = parseInt(String(cur.grade)) || 0;
    const age = gradeNum ? gradeNum + 6 : 0;

    const sectionsSpec = NOOR_SECTIONS.map((s, i) => `${i + 1}. «${s.heading}» — ${s.guidance}`).join("\n");

    const system = [
      "أنت خبير مناهج وطرائق تدريس متمرس في سلطنة عُمان، تُعِدّ تحضيراً رسمياً بهيكل منصة نور المعتمد وزارياً.",
      "معك مصدران للصور: (أ) صفحات الدرس من كتاب الطالب المعتمد، (ب) صفحات نفس الدرس من دليل المعلم الرسمي (توجيهات تدريسية وأنشطة مقترحة من الوزارة).",
      "اقرأهما معاً بدقّة، وابنِ تحضيراً كاملاً لهذا الدرس اعتماداً على محتواهما الفعلي حصراً (لا من معرفة عامة) — استعمل توجيهات دليل المعلم تحديداً لتحديد الاستراتيجيات والأنشطة والتوقيت، واستعمل الكتاب لتحديد المحتوى والأمثلة والأسئلة.",
      "هيكل التحضير ثابتٌ دائماً بهذه الأقسام السبعة بالضبط وبهذا الترتيب — لا تُسقط قسماً ولا تُضف قسماً غير مذكور:",
      sectionsSpec,
      age ? `أعمار الطلاب: ${age} سنوات تقريباً (الصف ${cur.grade}) — راعِ ذلك في الصياغة والأنشطة ومستوى الأسئلة.` : "",
      "صُغ بالعربية الفصحى بلغة تربوية رسمية دقيقة، والأرقام بالترقيم العربي-الهندي (٠١٢٣٤٥٦٧٨٩).",
      "قسم «إجراءات سير الدرس والأنشطة» يجب أن يكون مفصلاً وعملياً بعمق مماثل للنموذج المعتمد (خطواتٌ مرقّمة، كل خطوة بشرحٍ تنفيذي لا عنوانٍ مجرّد) — أما عددُ الخطوات فيتبع طبيعة الدرس ومحتواه، فلا تُطِل بحشوٍ لبلوغ عددٍ معيّن ولا تختصر ما يحتاجه الدرس فعلاً.",
      'أعد الناتج JSON فقط بهذا الشكل: {"title":"عنوان التحضير","sections":[{"heading":"عنوان القسم كما هو أعلاه حرفياً","body":"المحتوى التفصيلي لهذا القسم"}]}',
      "اجعل sections سبعة عناصر بالضبط، بنفس ترتيب الأقسام أعلاه وعناوينها الحرفية.",
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
          max_tokens: 6000,
        }),
      }, { st, task: "guided_prep" });
      const j = await r.json();
      if (!r.ok) return { ok: false as const, status: r.status, msg: String(j?.error?.message || j?.message || "") };
      const text = j?.choices?.[0]?.message?.content || "";
      const pp = parseAiJson<{ title?: string; sections?: unknown[] }>(text);
      const val = pp.ok ? pp.value : null;
      if (!val || !Array.isArray(val.sections) || val.sections.length < NOOR_SECTIONS.length) {
        return { ok: false as const, detail: text.slice(0, 300) };
      }
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

    // ملف Word بسيط اختياري (تنزيلٌ إضافي مريح) — لا يقلّد أي قالبٍ ورقي؛
    // المصدر الأساسي للتسليم هو نسخ كل قسمٍ من معاينة الشاشة إلى نور مباشرة.
    const sections = (attempt.content.sections || []) as { heading?: string; body?: string }[];
    const cleanSections = sections.map((s) => ({ heading: String(s.heading || ""), body: String(s.body || "") }));
    let docxUrl: string | null = null;
    try {
      const docxBytes = await buildGenericDocx(String(attempt.content.title || cur.lesson), cleanSections);
      const docxPath = `generated-preps/${curriculumId}.docx`;
      const { error: docxUpErr } = await admin.storage.from("library-files").upload(docxPath, docxBytes, {
        contentType: "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        upsert: true,
      });
      if (docxUpErr) console.error("docx_upload_failed:", docxUpErr.message);
      else docxUrl = admin.storage.from("library-files").getPublicUrl(docxPath).data.publicUrl;
    } catch (e) {
      console.error("docx_build_failed:", String(e));
    }

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
