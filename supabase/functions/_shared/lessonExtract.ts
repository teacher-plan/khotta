// ════════════════════════════════════════════════════════════════
// قراءة صفحات الدرس مرّة واحدة على مستوى المنصّة (اقتراح الأستاذ عيسى):
// عند التحضير تُقرأ صفحات كتاب الطالب للدرس بنموذج رؤية اقتصادي، ويُستخرج منها
//   • الملخّص النصّي المعتاد (للتحضير والألعاب والعروض)، و
//   • «مستخلص الاختبارات»: الأهداف، القواعد، الأمثلة المحلولة بأرقامها، والتمارين بنصّها —
//     ما يكفي لكتابة أسئلة اختبار دون إرسال الصور مرّة أخرى.
// يُخزَّن في library-files/book-extracts/{curriculum.id}.json، فيأخذه كل معلّمٍ بعد الأول
// جاهزاً بلا تكلفة، وتستعمله دالة exam-khotta نصّاً بدل ٢٠ صورة في كل اختبار.
// ════════════════════════════════════════════════════════════════
import { orFetch, ensureVision } from "./ai.ts";
import { parseAiJson } from "./aiJson.ts";
import { logAiCost } from "./quota.ts";

// deno-lint-ignore no-explicit-any
type Any = any;
export const EXTRACT_VERSION = 1;
export const guideKey = (guideId: number | string, curId: number | string) => `guide-summaries/${guideId}-${curId}.json`;
export const bookKey = (curId: number | string) => `book-extracts/${curId}.json`;

export async function curFor(admin: Any, grade: string | number, subject: string, unit: string, lesson: string, semester?: string) {
  let q = admin.from("curriculum").select("id,semester,unit,lesson,sort,page,book_no").eq("grade", Number(grade)).eq("subject", subject).eq("lesson", lesson);
  if (semester) q = q.eq("semester", semester);
  const { data } = await q;
  const rows: Any[] = data || [];
  return rows.find((c) => !unit || c.unit === unit) || rows[0] || null;
}

export async function readCache(admin: Any, key: string): Promise<Any | null> {
  try {
    const r = await admin.storage.from("library-files").download(key);
    if (r.error || !r.data) return null;
    const t = await r.data.text();
    const j = JSON.parse(t);
    return j && typeof j === "object" ? j : null;
  } catch { return null; }
}

const EXAM_SHAPE = {
  objectives: [{ code: "الرمز إن طُبع في الصفحة (مثل 9N1.2) وإلا \"\"", text: "نصّ الهدف/ما سوف تتعلّمه" }],
  vocabulary: [{ ar: "المصطلح", en: "term", def: "تعريفه كما ورد" }],
  rules: ["كل قاعدة/خاصية/تعريف/طريقة كما وردت حرفياً، مع رموزها"],
  worked_examples: [{ ref: "مثال ١ ص ٢٤", problem: "نصّ المثال بأعداده", steps: ["خطوات الحل كما في الكتاب"], answer: "الناتج" }],
  exercises: [{ ref: "تمرين ٣ ص ٢٥", text: "نصّ التمرين بأعداده كاملاً", parts: ["(أ) …", "(ب) …"], kind: "حسابي|كلامي|استدلال|إنشاء|قراءة شكل" }],
  figures: ["وصف دقيق لكل شكل/جدول/خط أعداد/شبكة مهمّ: ماذا يعرض وبأي قيم"],
  contexts: ["السياقات الحياتية المستعملة في الدرس (عُمانية أو غيرها)"],
  notation: "طريقة كتابة الرموز في الكتاب (الكسور، القوى، الجذور، الوحدات…)",
  pitfalls: ["تنبيهات أو أخطاء شائعة ذكرها الكتاب"],
};

// يقرأ صفحات الكتاب للدرس (مرّة واحدة لكل درس على المنصّة) ويعيد {summary, exam}.
export async function bookExtract(admin: Any, st: Record<string, string>, apiKey: string, cur: Any,
  images: string[], meta: { grade: string | number; subject: string; userId?: string }): Promise<Any | null> {
  const key = bookKey(cur.id);
  const cached = await readCache(admin, key);
  if (cached && cached.v === EXTRACT_VERSION && cached.summary) return cached;
  if (!images.length) return null;
  const model = ensureVision(st.model_book_extract || st.model_summary || st.vision_model || "google/gemini-2.5-flash", "google/gemini-2.5-flash");
  const system = [
    "أنت مساعد بحث تربوي دقيق. أمامك صفحات درس واحد من كتاب طالب معتمد في سلطنة عُمان (منهج كامبردج).",
    `الدرس المقصود: «${cur.lesson}» من «${cur.unit}». قد تظهر في الصفحات أجزاء من دروس مجاورة — تجاهلها.`,
    "اقرأ الصفحات بدقّة تامّة، ولا تُضف أي معلومة من عندك ولا من معرفة عامة. انقل الأعداد والرموز كما وردت حرفياً.",
    "أعد JSON فقط بحقلين:",
    "١) summary: ملخّص نصّي متصل بالعربية الفصحى (٢٥٠–٤٥٠ كلمة): المفاهيم بالترتيب، والأمثلة والأرقام والقواعد كما وردت، والأنشطة والتمارين، والمصطلحات — فقرات قصيرة بلا عناوين ولا حشو.",
    "٢) exam: مستخلص مفصّل يكفي معلّماً لكتابة أسئلة اختبار من هذا الدرس دون رؤية الصفحات — انقل كل الأمثلة المحلولة بخطواتها، وكل التمارين بنصّها وأعدادها وأجزائها، وصِف الأشكال والجداول بقيمها. لا تختصر التمارين.",
    "الحقل الذي لا يرد في الصفحات اتركه فارغاً (\"\" أو []).",
    `شكل exam: ${JSON.stringify(EXAM_SHAPE)}`,
  ].join("\n");
  const content: Any[] = [{ type: "text", text: `الصف: ${meta.grade} | المادة: ${meta.subject} | الوحدة: ${cur.unit} | الدرس: ${cur.lesson}` }];
  for (const u of images.slice(0, 20)) content.push({ type: "image_url", image_url: { url: u } });
  const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta Lesson Page Extractor" },
    body: JSON.stringify({
      model, messages: [{ role: "system", content: system }, { role: "user", content }],
      temperature: 0.1, max_tokens: 12000, response_format: { type: "json_object" }, reasoning: { max_tokens: 1024 },
    }),
  }, { st, task: "summary" });
  const j = await r.json().catch(() => ({}));
  if (!r.ok) { console.error("book_extract", r.status, String(j?.error?.message || "").slice(0, 200)); return null; }
  if (meta.userId) await logAiCost(admin, meta.userId, "book-extract", "text", model, j?.usage);
  const p = parseAiJson(String(j?.choices?.[0]?.message?.content || ""));
  if (!p.ok || !p.value || typeof p.value.summary !== "string" || !p.value.summary.trim()) return null;
  const out = { v: EXTRACT_VERSION, lesson: cur.lesson, unit: cur.unit, summary: p.value.summary.trim(), exam: p.value.exam || {}, model, at: new Date().toISOString(), pages: images.length };
  await admin.storage.from("library-files").upload(key, new Blob([JSON.stringify(out)], { type: "application/json" }), { upsert: true, contentType: "application/json" });
  return out;
}

// صور صفحات الدرس من كتاب الطالب (الصيغة نفسها في الواجهة: الورقة = الصفحة + الإزاحة − ١)
export async function lessonBookImages(admin: Any, cur: Any, grade: string | number, subject: string, max = 20): Promise<string[]> {
  const bookNo = cur.book_no || 1;
  const { data: rows } = await admin.from("curriculum").select("id,sort,page,book_no").eq("grade", Number(grade)).eq("subject", subject).eq("semester", cur.semester).order("sort");
  const sorted = (rows || []).filter((r: Any) => (r.book_no || 1) === bookNo);
  const i = sorted.findIndex((r: Any) => r.id === cur.id);
  const start = parseInt(cur.page) || 0;
  if (!start || i < 0) return [];
  const { data: bs } = await admin.from("book_sources").select("base_path,page_count,offset_pages").eq("grade", String(grade)).eq("subject", subject).eq("semester", cur.semester).eq("book_no", bookNo).maybeSingle();
  if (!bs?.base_path) return [];
  let end = bs.page_count || start;
  for (let j = i + 1; j < sorted.length; j++) { const np = parseInt(sorted[j].page); if (np && np > start) { end = np - 1; break; } }
  if (end < start) end = start;
  const off = bs.offset_pages || 1, out: string[] = [];
  for (let p = start; p <= end && out.length < max; p++) {
    const sh = p + off - 1; if (sh < 1 || sh > (bs.page_count || 9999)) continue;
    out.push(admin.storage.from("library-files").getPublicUrl(`${bs.base_path}/p${sh}.jpg`).data.publicUrl);
  }
  return out;
}

// ── دليل المعلم: قراءة صفحات الدرس من الدليل مرّة واحدة (مخزَّنة في guide-summaries/) — منقولة من generate-lesson-plan ──
export async function guideContextFor(admin: Any, st: Record<string, string>, apiKey: string,
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
    const cacheKey = guideKey(guide.id, cur.id);
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
      objectives: [{ code: "رمز الهدف كما طُبع في الدليل (مثل 7Ni.03) وإلا \"\"", text: "نصّ الهدف" }], learning_points: ["نقاط/أهداف التعلّم كما وردت"], vocabulary: [{ ar: "المصطلح", en: "term" }],
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
            "انقل رموز الأهداف التعليمية حرفياً كما طُبعت (لا تخترع رمزاً). انقل التفاصيل كما وردت: أرقام التمارين، أسماء الأنشطة، الأخطاء الشائعة، المفردات بالعربية والإنجليزية، والأزمنة إن ذُكرت.",
            "الحقل الذي لا يرد في الدليل اتركه فارغاً (\"\" أو []). الأرقام بالعربية-الهندية.",
            `أعد JSON فقط بهذا الشكل: ${shape}`,
          ].join("\n") },
          { role: "user", content: [{ type: "text", text: `صفحات دليل المعلم لدرس: ${lesson}` }, ...images.map((u) => ({ type: "image_url", image_url: { url: u } }))] },
        ],
        response_format: { type: "json_object" }, temperature: 0.1, max_tokens: 12000, reasoning: { max_tokens: 1024 },
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

