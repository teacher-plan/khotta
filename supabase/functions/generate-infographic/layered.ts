// ════════════════════════════════════════════════════════════════
// الإنفوجرافيك الطبقي «الذكاء يرسم، والمنصّة تكتب» (٢٠ نوفمبر — تجريبي لحساب المطوّر)
//
// بدل صورةٍ واحدة يكتب فيها نموذج الصور النصّ العربي (فيُخطئ إملاءً ويكرّر ويقلب
// القوانين)، نفصل العمل:
//   ١) نموذج نصّي رخيص يكتب المحتوى JSON من «مستخلص صفحات الدرس» حرفياً.
//   ٢) نموذج الصور يرسم الرسوم فقط — بلا أي كتابة — بدقة 1K (أرخص من 2K).
//   ٣) المتصفّح يكتب النصّ فوق الرسم بقالبٍ ثابت ثم يصوّره، فتعديل النصّ مجاني.
// قالبان:
//   cols — أربعة أعمدة، في أسفل كلٍّ رسمٌ يشرح فكرته (العلوم والدراسات)؛
//   bg   — خلفية بشخصيتين وزخارف ومساحة فارغة للمحتوى (اللغات والرياضيات والتربية
//          الإسلامية…)، وتُحفظ لكل وحدة فتُعاد بلا تكلفة رسمٍ لبقية دروسها.
// ════════════════════════════════════════════════════════════════
import { refundQuota, logAiCost } from "../_shared/quota.ts";
import { orFetch, orErrCode } from "../_shared/ai.ts";
import { parseAiJson } from "../_shared/aiJson.ts";
import { curFor, bookExtract } from "../_shared/lessonExtract.ts";

// deno-lint-ignore no-explicit-any
type Any = any;
export const LAYERED_VERSION = 1;

const S = (v: unknown, n = 200) => String(v ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const A = (v: unknown) => (Array.isArray(v) ? v : []);

// قالب المادة: العلوم والدراسات رسومٌ تشرح، والباقي نصٌّ على خلفية
export function layoutFor(subject: string): "cols" | "bg" {
  return /علوم|أحياء|احياء|كيمياء|فيزياء|دراسات|جغرافيا|تاريخ|بيئ|الأرض/.test(subject) ? "cols" : "bg";
}
// زخارف الخلفية بحسب المادة (بلا حروف ولا أرقام — النموذج يرسمها مشوّهة)
function bgDecor(subject: string): string {
  if (/رياض/.test(subject)) return "playful math decorations: a set square, a ruler, a protractor, colorful geometric shapes (triangles, circles, cubes), stars and sparkles";
  if (/عربية|لغة|أدب|نحو|بلاغ/.test(subject)) return "an open book, a quill and inkwell, a lightbulb, an empty speech bubble, subtle Arabic geometric arabesque patterns in the corners";
  if (/إسلام|اسلام|قرآن|دين/.test(subject)) return "a softly drawn mosque silhouette, a Ramadan-style lantern, an open book on a wooden stand, crescent and stars, subtle Islamic geometric patterns in the corners";
  if (/انجليز|إنجليز|English/i.test(subject)) return "colorful books, a globe, a pencil, an empty speech bubble, a lightbulb, stars";
  if (/فن|موسيق/.test(subject)) return "paint brushes, a palette with colors, musical notes shapes without letters, stars";
  return "books, pencils, a lightbulb, a globe, stars and sparkles";
}

const STYLE = "Flat, cute educational cartoon style, soft pastel colors (mint, cream, light blue, blush pink, butter yellow), clean outlines, warm and friendly, suitable for Omani school students. Any people are Omani: boys in a white dishdasha and embroidered kumma cap, girls and women in a modest hijab; characters never touch each other.";
const NO_TEXT = "ABSOLUTELY NO text of any kind anywhere in the image: no letters, no Arabic or Latin words, no numbers or digits, no math symbols, no chemical formulas, no labels, no calligraphy, no writing on books, boards or signs.";

function artPrompt(layout: "cols" | "bg", c: Any, subject: string, unit: string): string {
  if (layout === "cols") {
    const cards = A(c.cards).slice(0, 4);
    const cols = cards.map((k: Any, i: number) => `Column ${i + 1}${i === 0 ? " (rightmost)" : i === 3 ? " (leftmost)" : ""}: ${S(k.art, 300) || "a simple illustration of the idea"}.`).join(" ");
    return [
      "Wide 16:9 educational poster illustration.", STYLE,
      "Soft cream background with a gentle Omani landscape strip (palm trees, distant mountains) along the very top edge.",
      "The image is divided into FOUR equal vertical columns, ordered from right to left. The TOP HALF of every column must be completely empty plain cream space (text will be added there later). In the BOTTOM HALF of each column draw exactly one clear illustration:",
      cols, NO_TEXT,
    ].join(" ");
  }
  return [
    `Wide 16:9 educational poster BACKGROUND illustration for a school lesson unit «${unit}».`, STYLE,
    `Decorations placed only around the edges and corners: ${bgDecor(subject)}.`,
    "On the far right edge: a thoughtful Omani student (boy in a white dishdasha and kumma cap). On the far left edge: a smiling Omani female teacher in a modest abaya and hijab holding an open book. The two characters are far apart.",
    "The large central area (about 76% of the width and 80% of the height) must be a clean, plain, soft cream EMPTY space with nothing drawn in it, reserved for content added later.",
    NO_TEXT,
  ].join(" ");
}

function contentPrompt(layout: "cols" | "bg", cur: Any, grade: string, subject: string, teacher: string): string {
  const shape = layout === "cols"
    ? `{"title":"عنوان الدرس كما هو","cards":[{"h":"عنوان قصير (٢–٤ كلمات)","points":["جملة قصيرة من الدرس","..."],"formula":"معادلة أو قاعدة قصيرة إن وُجدت في الدرس وإلا فارغ","art":"English description of ONE wordless illustration that explains this card's idea (objects only, no text)"}]}  — أربع بطاقات بالضبط`
    : `{"title":"عنوان الدرس كما هو","cards":[{"h":"عنوان قصير (١–٣ كلمات)","points":["جملة قصيرة من الدرس","..."]}],"example":{"label":"مثال وتحليله / مثال محلول","lines":["سطر المثال كما ورد (بيت شعر: شطران في سطرين؛ مسألة: نصّها)"],"head":["عنوان العمود","..."],"row":["قيمة","..."],"note":"خلاصة أو تحويل أو ناتج في جملة واحدة"}}  — ثلاث بطاقات بالضبط، والمثال واحد من أمثلة الدرس نفسها (الجدول من ٢–٣ أعمدة، ويجوز تركه فارغاً إن لم يناسب)`;
  return [
    "أنت مصمّم تعليمي عُماني. اكتب محتوى إنفوجرافيك لدرسٍ واحد من مستخلص صفحات الكتاب المرفق وحده.",
    `الدرس: «${cur.lesson}» — ${cur.unit} — ${subject} — الصف ${grade}.`,
    "الشروط: عربية فصحى سليمة إملائياً؛ انقل التعريفات والقواعد والمصطلحات والأرقام كما وردت حرفياً؛ لا تُضف معلومة ليست في المستخلص؛ لا أسئلة ولا تمارين؛ جُمل قصيرة (٨–١٨ كلمة)، ونقطتان أو ثلاث لكل بطاقة على الأكثر؛ الأرقام بالأرقام العربية (٠١٢٣٤٥٦٧٨٩) ما لم ترد بغيرها؛ المصطلح الإنجليزي (إن ورد في الكتاب) بين قوسين فقط.",
    "رتّب البطاقات بترتيب أفكار الدرس. في الرياضيات اكتب القانون في formula بالرموز العربية كما في الكتاب (مثل: م = ل × ض).",
    teacher ? `توجيهات المعلّم (لها الأولوية ما لم تخالف الشروط): ${teacher}` : "",
    `أعد JSON فقط بهذا الشكل: ${shape}`,
  ].filter(Boolean).join("\n");
}

function cleanContent(layout: "cols" | "bg", raw: Any, cur: Any): Any | null {
  if (!raw || typeof raw !== "object") return null;
  const n = layout === "cols" ? 4 : 3;
  const cards = A(raw.cards).slice(0, n).map((k: Any) => ({
    h: S(k?.h, 40), points: A(k?.points).slice(0, 3).map((p) => S(p, 160)).filter(Boolean),
    formula: S(k?.formula, 80), art: S(k?.art, 320),
  })).filter((k: Any) => k.h && k.points.length);
  if (cards.length < n) return null;
  const out: Any = { title: S(raw.title, 60) || S(cur.lesson, 60), cards };
  if (layout === "bg" && raw.example && typeof raw.example === "object") {
    const e = raw.example;
    const head = A(e.head).slice(0, 3).map((x) => S(x, 30)), row = A(e.row).slice(0, 3).map((x) => S(x, 70));
    out.example = {
      label: S(e.label, 30) || "مثال", lines: A(e.lines).slice(0, 3).map((x) => S(x, 90)).filter(Boolean),
      head: head.length === row.length && head.length >= 2 ? head : [], row: head.length === row.length && head.length >= 2 ? row : [],
      note: S(e.note, 160),
    };
    if (!out.example.lines.length && !out.example.row.length && !out.example.note) delete out.example;
  }
  return out;
}

async function storageUrl(admin: Any, key: string): Promise<string> {
  const { data } = await admin.storage.from("library-files").list(key.split("/").slice(0, -1).join("/"), { search: key.split("/").pop() });
  if (!A(data).some((o: Any) => o.name === key.split("/").pop())) return "";
  return admin.storage.from("library-files").getPublicUrl(key).data.publicUrl;
}
function hash(s: string): string { let h = 5381; for (const ch of s) h = ((h * 33) ^ ch.charCodeAt(0)) >>> 0; return h.toString(36); }

// يُستدعى بعد takeQuota(img). أي خروجٍ بخطأ يستردّ الحصّة.
export async function layeredInfographic(admin: Any, user: Any, st: Record<string, string>, apiKey: string, b: Any, json: (x: unknown, s?: number) => Response): Promise<Response> {
  const refund = async (body: Record<string, unknown>, status: number) => { await refundQuota(admin, user.id, user.email || "", "img"); return json(body, status); };
  const grade = String(b.grade || ""), subject = String(b.subject || ""), unit = String(b.unit || "");
  const lesson = String((A(b.lessonNames)[0]) || b.lesson || "");
  if (!grade || !subject || !lesson) return await refund({ error: "no_lessons" }, 400);
  const cur = await curFor(admin, grade, subject, unit, lesson).catch(() => null);
  if (!cur) return await refund({ error: "no_lesson", message: "الدرس غير موجود في المنهج." }, 404);
  const images: string[] = A(b.images).slice(0, 8).map(String);
  const ex = await bookExtract(admin, st, apiKey, cur, images, { grade, subject, userId: user.id }).catch(() => null);
  if (!ex || !ex.summary) return await refund({ error: "no_extract", message: "تعذّرت قراءة صفحات الدرس من الكتاب." }, 409);
  const layout: "cols" | "bg" = b.layout === "cols" || b.layout === "bg" ? b.layout : layoutFor(subject);

  // ١) المحتوى — أو محتوى جاهز من المعلّم عند «إعادة رسم الرسوم» فقط
  let content: Any = b.content && typeof b.content === "object" ? cleanContent(layout, b.content, cur) : null;
  if (!content) {
    const e = ex.exam || {};
    const src = [
      "ملخّص صفحات الدرس:\n" + String(ex.summary).slice(0, 6000),
      e.rules?.length ? "القواعد والتعريفات كما وردت:\n- " + e.rules.slice(0, 14).join("\n- ") : "",
      e.vocabulary?.length ? "المصطلحات:\n- " + e.vocabulary.slice(0, 14).map((v: Any) => v.ar + (v.def ? ": " + v.def : "")).join("\n- ") : "",
      e.worked_examples?.length ? "أمثلة الدرس:\n- " + e.worked_examples.slice(0, 5).map((w: Any) => `${w.problem} ← ${w.answer}`).join("\n- ") : "",
    ].filter(Boolean).join("\n\n");
    const model = st.model_info_text || st.model_summary || "google/gemini-2.5-flash";
    const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta Layered Infographic" },
      body: JSON.stringify({ model, temperature: 0.2, max_tokens: 3000, response_format: { type: "json_object" },
        messages: [{ role: "system", content: contentPrompt(layout, cur, grade, subject, S(b.teacherPrompt, 800)) }, { role: "user", content: src }] }),
    }, { st, task: "summary" });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) return await refund({ error: "provider_error", detail: String(j?.error?.message || "").slice(0, 200) }, 502);
    await logAiCost(admin, user.id, "generate-infographic", "text", model, j?.usage);
    const p = parseAiJson(String(j?.choices?.[0]?.message?.content || ""));
    content = p.ok ? cleanContent(layout, p.value, cur) : null;
    if (!content) return await refund({ error: "bad_output" }, 502);
  }

  // ٢) الرسم — الخلفية تُعاد لكل دروس الوحدة نفسها (القالب bg) ما لم يُطلب رسمٌ جديد
  const bgKey = `info-bg/v${LAYERED_VERSION}-${hash(`${grade}|${subject}|${cur.unit}`)}.jpg`;
  if (layout === "bg" && !b.redraw) {
    const url = await storageUrl(admin, bgKey);
    if (url) { await refundQuota(admin, user.id, user.email || "", "img"); return json({ layered: true, layout, content, art: url, cached: true, cur_id: cur.id }); }
  }
  let model = st.model_infographic || st.slide_model || "google/gemini-3.1-flash-image-preview";
  if (!model.startsWith("google/")) model = "google/gemini-3.1-flash-image-preview";
  const prompt = artPrompt(layout, content, subject, cur.unit);
  let img = "", usage: unknown = null, lastErr = "";
  for (const cfg of [{ aspect_ratio: "16:9", image_size: "1K" }, { aspect_ratio: "16:9" }]) {
    const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta Layered Infographic" },
      body: JSON.stringify({ model, messages: [{ role: "user", content: prompt }], modalities: ["image", "text"], image_config: cfg }),
    }, { st, task: "infographic" });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) { lastErr = String(j?.error?.message || j?.message || r.status); if (r.status === 402) break; continue; }
    img = j?.choices?.[0]?.message?.images?.[0]?.image_url?.url || "";
    usage = j?.usage || null;
    if (img) break;
  }
  if (!img) return await refund({ error: lastErr ? orErrCode(502, lastErr) : "no_image", detail: lastErr.slice(0, 200) }, 502);
  await logAiCost(admin, user.id, "generate-infographic", "img", model, usage);

  // الخلفية تُحفظ لتُعاد لبقية دروس الوحدة؛ رسوم الأعمدة خاصة بالدرس فتعود مباشرة
  if (layout === "bg") {
    try {
      const b64 = img.split(",")[1] || "";
      const bin = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
      const ct = (img.match(/^data:([^;]+)/) || [])[1] || "image/png";
      await admin.storage.from("library-files").upload(bgKey, new Blob([bin], { type: ct }), { upsert: true, contentType: ct, cacheControl: "31536000" });
    } catch (e) { console.error("layered bg cache", String(e)); }
  }
  return json({ layered: true, layout, content, art: img, cached: false, cur_id: cur.id });
}
