// v2026.07.09 ════════════════════════════════════════════════════════════════
// Edge Function: generate-lesson-plan
// مساعد التحضير اليومي — يولّد خطة حصة (45 دقيقة) منظمة لدرس محدد
// بنموذج نصي اقتصادي، وتُخزَّن في lesson_preps لإعادة الاستخدام.
//
// النشر:  supabase functions deploy generate-lesson-plan
// الأسرار: OPENROUTER_API_KEY
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { takeQuota, refundQuota, logAiCost } from "../_shared/quota.ts";
import { parseAiJson, requireArray } from "../_shared/aiJson.ts";
import { orFetch, ensureVision, orErrCode } from "../_shared/ai.ts";

/* ══ دليل المعلم ══
   صفحات الدرس نفسه من دليل المعلم الرسمي (المرفوع والمفهرس من لوحة المشرف)
   تُقرأ بالرؤية مرّةً واحدة لكل درس، ويُخزَّن ما استُخرج منها (JSON) في
   library-files/guide-summaries/ — فكل معلّمٍ بعد الأول يأخذه جاهزاً بلا تكلفة.
   أيّ عطلٍ هنا لا يُفشل التحضير: نكمل بالكتاب وحده كما كان. */
type Admin = ReturnType<typeof createClient>;
async function guideContextFor(admin: Admin, st: Record<string, string>, apiKey: string,
  grade: string, subject: string, unit: string, lesson: string, semester: string): Promise<string> {
  try {
    let q = admin.from("curriculum").select("id,semester,unit,lesson").eq("grade", grade).eq("subject", subject).eq("lesson", lesson);
    if (semester) q = q.eq("semester", semester);
    const { data: curs } = await q;
    const cur = (curs || []).find((c: { unit: string }) => !unit || c.unit === unit) || (curs || [])[0];
    if (!cur) return "";
    const { data: guide } = await admin.from("teacher_guides").select("id,base_path,page_count,offset_pages,toc")
      .eq("grade", parseInt(grade)).eq("subject", subject).eq("semester", cur.semester).maybeSingle();
    if (!guide || !guide.base_path || !Array.isArray(guide.toc)) return "";
    const cacheKey = `guide-summaries/${guide.id}-${cur.id}.json`;
    const cached = await admin.storage.from("library-files").download(cacheKey);
    if (!cached.error && cached.data) { const t = await cached.data.text(); if (t.length > 20) return t; }

    type E = { guide_page?: number; matched_curriculum_id?: number };
    const toc = (guide.toc as E[]).filter((x) => x.guide_page).sort((a, b) => (a.guide_page || 0) - (b.guide_page || 0));
    const e = toc.find((x) => x.matched_curriculum_id === cur.id);
    if (!e) return "";
    const start = e.guide_page!;
    let end = guide.page_count || start;
    for (const x of toc) if ((x.guide_page || 0) > start) { end = x.guide_page! - 1; break; }
    if (end < start) end = start;
    const off = guide.offset_pages || 1, images: string[] = [];
    for (let bp = start; bp <= end && images.length < 12; bp++) {
      const sheet = bp + off - 1; if (sheet < 1 || sheet > (guide.page_count || 9999)) continue;
      images.push(admin.storage.from("library-files").getPublicUrl(`${guide.base_path}/p${sheet}.jpg`).data.publicUrl);
    }
    if (!images.length) return "";

    const shape = JSON.stringify({
      learning_points: ["نقاط/أهداف التعلّم كما وردت"], vocabulary: [{ ar: "المصطلح", en: "term" }],
      prior_knowledge: "التعلّم القبلي المطلوب", resources: ["المواد والأدوات المطلوبة"],
      starter: "نشاط التهيئة/البداية المقترح في الدليل بتفاصيله", activities: [{ name: "اسم النشاط", detail: "خطواته كما في الدليل" }],
      misconceptions: [{ error: "الخطأ أو المفهوم الخاطئ الشائع", fix: "كيف يعالجه المعلم" }],
      differentiation: { support: "دعم المتعثرين", extension: "إثراء المتقدمين" },
      thinking: ["أسئلة التفكير/الاستقصاء المقترحة"], exercises: [{ ex: "رقم التمرين", note: "التعليق أو الإجابة أو التوجيه" }],
      assessment: "أفكار التقويم في الدليل", homework: "الواجب المقترح", cross_links: "الربط بالحياة أو المواد الأخرى", other: "أي توجيه آخر مهم",
    });
    const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta Guide Reader" },
      body: JSON.stringify({
        model: ensureVision(st.model_guided_prep || st.vision_model || "google/gemini-2.5-flash", "google/gemini-2.5-flash"),
        messages: [
          { role: "system", content: [
            "أنت تقرأ صفحات دليل المعلم الرسمي (سلطنة عُمان) لدرسٍ واحد وتستخرج كل ما فيه بأمانة ودقة، دون إضافة شيءٍ من عندك.",
            `الدرس المقصود: «${lesson}»${unit ? ` من وحدة «${unit}»` : ""}. قد تحوي الصفحات أجزاءً من دروسٍ مجاورة — تجاهلها.`,
            "انقل التفاصيل كما وردت: أرقام التمارين، أسماء الأنشطة، الأخطاء الشائعة، المفردات بالعربية والإنجليزية، والأزمنة إن ذُكرت.",
            "الحقل الذي لا يرد في الدليل اتركه فارغاً (\"\" أو []). الأرقام بالعربية-الهندية.",
            `أعد JSON فقط بهذا الشكل: ${shape}`,
          ].join("\n") },
          { role: "user", content: [{ type: "text", text: `صفحات دليل المعلم لدرس: ${lesson}` }, ...images.map((u) => ({ type: "image_url", image_url: { url: u } }))] },
        ],
        response_format: { type: "json_object" }, temperature: 0.1, max_tokens: 5000,
      }),
    }, { st, task: "guide_read" });
    if (!r.ok) return "";
    const j = await r.json();
    const pp = parseAiJson(j?.choices?.[0]?.message?.content || "");
    if (!pp.ok) return "";
    const txt = JSON.stringify(pp.value);
    await admin.storage.from("library-files").upload(cacheKey, new Blob([txt], { type: "application/json" }), { upsert: true, contentType: "application/json" });
    return txt;
  } catch (e) {
    console.error("guide_context_failed:", String(e));
    return "";
  }
}

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
    // تمييزٌ لازم: fail-closed يعني أنّ عطلاً في القاعدة يمنع التوليد أيضاً —
    // فلو قلنا «نفد رصيدك» لكذبنا على المعلّمة وأرسلناها تشكو رصيداً سليماً.
    if (!quota.ok) return quota.error === "quota_unavailable"
      ? json({ error: "quota_unavailable" }, 503)
      : json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);
    // كل مخرجٍ بخطأٍ بعد هذه النقطة يستردّ ما خُصم: المعلمة لا تُحاسَب
    // على توليدٍ لم تستلمه.
    const refund = async (body: Record<string, unknown>, status: number) => {
      await refundQuota(admin, user.id, user.email || "", "text");
      return json(body, status);
    };

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const unit = String(b.unit || "");
    const lesson = String(b.lesson || "");
    const images: string[] = Array.isArray(b.images) ? b.images.slice(0, 12) : [];
    // ملخص نصي جاهز من صفحات الكتاب (مُعَدّ مسبقاً بدالة summarize-lesson-pages) —
    // بديل أرخص عن إرفاق الصور نفسها في كل استدعاء توليد
    const bookContext = String(b.bookContext || "").slice(0, 4000);
    const semester = String(b.semester || "");
    if (!lesson) return json({ error: "no_lesson" }, 400);
    const guideContext = (await guideContextFor(admin, st, apiKey, grade, subject, unit, lesson, semester)).slice(0, 9000);

    // عند إرفاق صفحات الكتاب نحتاج نموذجاً يدعم الرؤية
    // مع صفحات الكتاب: نموذج رؤية مضمون (لا نمرّ بـ ai_model النصي)
    const model = images.length
      ? ensureVision(st.model_plan_vision || st.vision_model || "google/gemini-2.5-flash", "google/gemini-2.5-flash")
      : (st.model_plan || st.ai_model || "google/gemini-2.5-flash");

    // عمر الطلاب في عُمان: الصف الأول = ٧ سنوات (العمر = الصف + ٦)
    const gradeNum = parseInt(grade) || 0;
    const age = gradeNum ? gradeNum + 6 : 0;

    // هيكل التحضير المعتمد في منصة نور (سلطنة عُمان)
    const schema = JSON.stringify({
      outcomes: [{ level: "التذكر", text: "أنا أستطيع أن أذكر ..." }],
      strategies: ["استراتيجية تدريس مناسبة"],
      resources: ["مصدر أو وسيلة تعليمية"],
      concepts: ["مفهوم أساسي في الدرس"],
      warmup: "التهيئة والتمهيد والتعلم القبلي: نص تفصيلي — ماذا يفعل المعلم بالضبط وماذا يقول حرفياً بين قوسي اقتباس، وكيف يستدعي التعلم القبلي",
      procedures: [{ title: "الخطوة/النشاط", minutes: 10, detail: "سير مفصل: ما يفعله المعلم، ما يقوله حرفياً، ما يعمله الطلاب، وكيف ينتقل للتالي" }],
      formative: "التقويم التكويني أثناء الدرس: كيف يتحقق المعلم من الفهم لحظياً (أسئلة سريعة، ملاحظة، إشارات)",
      summative: [{ q: "سؤال ختامي يقيس مخرجاً محدداً", a: "الإجابة النموذجية", outcome: "المخرج الذي يقيسه" }],
      homework: "واجب منزلي قصير مناسب",
      tip: "نصيحة تربوية خاصة بهذا الدرس",
      // ── ما يتجاوز الترويسة المعتمدة: كل ما في دليل المعلم ──
      vocabulary: [{ ar: "المصطلح", en: "term" }],
      prior_knowledge: "التعلّم القبلي الذي يُبنى عليه الدرس",
      success_criteria: ["معيار نجاح يلاحظه المعلم"],
      misconceptions: [{ error: "خطأ شائع متوقّع في هذا الدرس", fix: "كيف يعالجه المعلم عملياً" }],
      differentiation: { support: "دعم المتعثرين بخطوات محددة", extension: "إثراء المتقدمين بمهمة محددة" },
      thinking: ["سؤال تفكير عليا أو استقصاء"],
      exercises: [{ ex: "رقم التمرين في الكتاب", note: "توجيه التنفيذ أو الإجابة أو التعليق" }],
      cross_links: "الربط بالحياة اليومية والمواد الأخرى",
      guide_notes: ["أي توجيه مهم آخر من دليل المعلم لم يرد في الحقول السابقة"],
    });

    const system = [
      "أنت خبير مناهج وطرائق تدريس متمرس في سلطنة عُمان، تعدّ تحضيراً رسمياً بهيكل منصة نور، مبنياً على أسس تربوية بحتة.",
      "المنهج المعتمد: منهج كامبردج (Cambridge) كما يطبَّق في مدارس سلطنة عُمان — راعِ فلسفته: الفهم العميق، الاستقصاء، وربط التعلم بالحياة.",
      guideContext
        ? `ما ورد في دليل المعلم الرسمي لهذا الدرس (JSON مستخرج من صفحاته) — هو المرجع التربوي الأول: خذ منه نقاط التعلّم والأنشطة المقترحة والأخطاء الشائعة والمفردات والتمايز والتعليق على التمارين والواجب، ولا تُسقط شيئاً منه:\n${guideContext}`
        : "",
      guideContext
        ? "المطلوب تحضيرٌ شاملٌ يغطّي كل ما في دليل المعلم، لا الاكتفاء بخانات الترويسة المعتمدة: املأ حقول الترويسة (المخرجات… الواجب) ثم الحقول الإضافية (المفردات، التعلّم القبلي، معايير النجاح، الأخطاء الشائعة، التمايز، أسئلة التفكير، التمارين، الربط، ملاحظات الدليل). ابنِ الإجراءات على أنشطة الدليل نفسها بأسمائها."
        : "إلى جانب خانات الترويسة املأ الحقول الإضافية (المفردات، التعلّم القبلي، معايير النجاح، الأخطاء الشائعة، التمايز، أسئلة التفكير، التمارين، الربط) بما يناسب محتوى الدرس، واترك guide_notes فارغة.",
      bookContext
        ? `ملخص فعلي لمحتوى هذا الدرس من كتاب الطالب المعتمد — استخدمه كمصدر أساسي حصري (لا من معرفة عامة):\n${bookContext}`
        : images.length
        ? "الصور المرفقة هي صفحات هذا الدرس من كتاب الطالب المعتمد. اقرأها بدقّة وابنِ التحضير من محتواها الفعلي حصراً (المفاهيم، الأمثلة، الأنشطة، الأرقام كما وردت) لا من معرفة عامة."
        : "لا صور مرفقة من الكتاب — بناءً على خبرتك بمنهج كامبردج المعتمد في سلطنة عُمان لهذا الصف والمادة، توقّع المحتوى الفعلي المرجّح لهذا الدرس تحديداً (لا محتوى عام) وابنِ التحضير عليه مباشرة بثقة.",
      age ? `أعمار الطلاب: ${age} سنوات تقريباً (الصف ${grade}) — كل الصياغات والأنشطة والأمثلة يجب أن تناسب هذا العمر النمائي بدقة.` : "",
      "المخرجات التعليمية (outcomes): 3-5 مخرجات بصيغة «أنا أستطيع أن …» موزعة على مستويات بلوم مختلفة، وحقل level يحدد المستوى (التذكر، الفهم، التطبيق، التحليل...).",
      "الاستراتيجيات (strategies): 2-3 استراتيجيات تدريس حقيقية مناسبة للدرس والعمر (التعلم التعاوني، لعب الأدوار، الاستقصاء...).",
      "المصادر (resources): مصادر ووسائل واقعية متاحة في الصف العماني.",
      "المفاهيم (concepts): المفاهيم الأساسية التي يبنى عليها الدرس.",
      "التهيئة (warmup): فقرة تفصيلية عملية — ماذا يفعل المعلم خطوة خطوة وماذا يقول حرفياً (ضع أقواله بين «») وكيف يستحضر التعلم القبلي المرتبط.",
      "الإجراءات (procedures): سير الدرس كاملاً من البداية للنهاية في 3-5 خطوات موقوتة (مجموعها ~45 دقيقة بعد التهيئة)، كل خطوة بتفصيل عملي: فعل المعلم، قوله الحرفي، عمل الطلاب.",
      "التقويم التكويني (formative): آليات تحقق لحظية أثناء الدرس.",
      "التقويم الختامي (summative): 3 أسئلة تقيس المخرجات تحديداً، كل سؤال مرتبط بمخرج (حقل outcome) مع إجابته النموذجية.",
      "صُغ بالعربية الفصحى بلغة تربوية رسمية دقيقة.",
      "الأرقام دائماً بالترقيم العربي-الهندي (٠١٢٣٤٥٦٧٨٩) لا اللاتيني، وأي معادلة أو عملية حسابية تُكتب من اليمين إلى اليسار متوافقة مع اتجاه النص العربي.",
      `أعد الناتج JSON فقط بهذا الشكل حصراً: ${schema}`,
    ].filter(Boolean).join("\n");

    const userMsg = [
      `الصف: ${grade} | المادة: ${subject}`,
      unit ? `الوحدة: ${unit}` : "",
      `الدرس: ${lesson}`,
    ].filter(Boolean).join("\n");

    // محتوى المستخدم: نص + صور صفحات الدرس إن وُجدت
    const userContent: unknown[] = [{ type: "text", text: userMsg }];
    for (const u of images) userContent.push({ type: "image_url", image_url: { url: u } });

    // الخطة هي أساس التحضير كله — لا نستسلم من أول محاولة:
    // (١) محاولة كاملة (بالصور إن وُجدت) → (٢) إعادة عند خروج غير سليم → (٣) تراجع نصي بلا صور
    const callOnce = async (withImages: boolean) => {
      const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Lesson Prep",
        },
        body: JSON.stringify({
          model: withImages ? model : (st.model_plan || st.ai_model || "google/gemini-2.5-flash"),
          messages: [
            { role: "system", content: system },
            { role: "user", content: withImages && images.length ? userContent : userMsg },
          ],
          response_format: { type: "json_object" },
          temperature: 0.4,
          max_tokens: 7000,
        }),
      }, { st, task: "plan" });
      const j = await r.json();
      // رمزُ الحالة يُمرَّر مع الفشل: بدونه يُبتلع نفادُ الرصيد داخل
      // «bad_output» فيُقرأ عطلاً في المحتوى لا في الحساب
      if (!r.ok) return { ok: false as const, detail: j, status: r.status, msg: String(j?.error?.message || j?.message || "") };
      const text = j?.choices?.[0]?.message?.content || "";
      // هذه وحدها كانت تحرس التحليلين معاً وتفحص الشكل — بقي أن نُبدّل
      // الـregex الجشع بمسحٍ متوازنٍ يحترم النصوص، فلا يُهزم بشرحٍ فيه قوس.
      const _pp = parseAiJson(text);
      const plan: unknown = _pp.ok ? _pp.value : null;
      const pl = plan as { procedures?: unknown[]; outcomes?: unknown[]; phases?: unknown[] } | null;
      if (!pl || !(pl.procedures || pl.phases)) return { ok: false as const, detail: text.slice(0, 300) };
      return { ok: true as const, plan, usage: j?.usage || null };
    };

    let attempt = await callOnce(images.length > 0);
    if (!attempt.ok) attempt = await callOnce(images.length > 0);          // إعادة مرة
    if (!attempt.ok && images.length) attempt = await callOnce(false);     // تراجع نصي
    if (!attempt.ok) {
      const st_ = (attempt as { status?: number }).status;
      const m_ = (attempt as { msg?: string }).msg || "";
      if (st_) {
        console.error(`openrouter ${st_} في generate-lesson-plan: ${m_}`);
        return refund({ error: orErrCode(st_, m_), detail: m_.slice(0, 200) }, 502);
      }
      return refund({ error: "bad_output", detail: attempt.detail }, 502);
    }
    await logAiCost(admin, user.id, "generate-lesson-plan", "text", model, attempt.usage);
    return json({ plan: { ...(attempt.plan as Record<string, unknown>), _guide: !!guideContext }, model, usage: attempt.usage });
  } catch (e) {
    // لا استرداد هنا: قد يقع الخطأ قبل تعريف refund أصلاً (وقبل خصم الحصّة)
    console.error("server_error:", String(e));
    return json({ error: "server_error" }, 500);
  }
});
