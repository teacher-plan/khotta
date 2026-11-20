// ════════════════════════════════════════════════════════════════
// خرائط المفاهيم الطبقية «الذكاء يرسم، والمنصّة تكتب» (٢٠ نوفمبر — تجريبي لحساب المطوّر)
//
// نموذجٌ نصّي رخيص يبني «هيكل» الخريطة JSON من مستخلص صفحات الدرس بحسب نوعها
// (مفاهيم، شعاعية، شجرية، تدفّق، مقارنة، سبب ونتيجة، دورة)، والمتصفّح يرسم الصناديق
// والأسهم والنصوص بدقّة. نموذج الصور يرسم خلفيةً مزخرفة بلا كتابة بالنمط المختار،
// تُحفظ للوحدة والنمط والمقاس فتُعاد بلا تكلفة. بلا رسوم ← بلا نداء صور إطلاقاً.
// ════════════════════════════════════════════════════════════════
import { refundQuota, logAiCost } from "../_shared/quota.ts";
import { orFetch, orErrCode } from "../_shared/ai.ts";
import { parseAiJson } from "../_shared/aiJson.ts";
import { curFor, bookExtract } from "../_shared/lessonExtract.ts";

// deno-lint-ignore no-explicit-any
type Any = any;
const S = (v: unknown, n = 120) => String(v ?? "").replace(/\s+/g, " ").trim().slice(0, n);
const A = (v: unknown) => (Array.isArray(v) ? v : []);
const L = (v: unknown, n: number, m = 60) => A(v).slice(0, n).map((x) => S(x, m)).filter(Boolean);
function hash(s: string): string { let h = 5381; for (const ch of s) h = ((h * 33) ^ ch.charCodeAt(0)) >>> 0; return h.toString(36); }

export const CM_TYPES = ["concept", "radial", "tree", "flow", "compare", "cause", "cycle"] as const;
const N: Record<string, [number, number, number]> = { "1": [3, 2, 2], "2": [5, 3, 3], "3": [7, 4, 4] }; // [فروع/مراحل، عناصر لكل فرع، أسباب/نتائج]

function shapeFor(type: string, d: string): string {
  const [b, it, ce] = N[d] || N["2"];
  switch (type) {
    case "concept": return `{"title":"المفهوم الأشمل (عنوان الدرس)","nodes":[{"id":"n1","label":"مفهوم (١–٣ كلمات)","level":1,"icon":"إيموجي"}],"links":[{"from":"root","to":"n1","label":"عبارة ربط قصيرة (يتكوّن من، يؤدّي إلى، من أنواعه، يُستخدم في…)"}]} — المفهوم الأشمل معرّفه "root"؛ ${b}–${b + 3} مفاهيم في المستويين ١ و٢ (level)، وكل مفهوم يصله سهمٌ واحد على الأقل، ويجوز وصلة عرضية واحدة بين فرعين إن وُجدت العلاقة في الدرس`;
    case "radial": return `{"center":"عنوان الدرس مختصراً","branches":[{"label":"فكرة رئيسية (١–٣ كلمات)","icon":"إيموجي","items":["تفصيل قصير (٢–٦ كلمات)"]}]} — ${b} فروع، ولكلٍّ ${it} تفاصيل على الأكثر`;
    case "tree": return `{"root":"عنوان التصنيف","children":[{"label":"فئة","icon":"إيموجي","items":["عنصر أو مثال"]}]} — ${Math.min(b, 5)} فئات من الدرس، ولكلٍّ ${it + 1} عناصر على الأكثر`;
    case "flow": return `{"title":"عنوان الإجراء أو العملية","steps":[{"label":"الخطوة (١–٤ كلمات)","icon":"إيموجي","note":"توضيح قصير اختياري"}]} — ${b}–${b + 2} خطوات بترتيبها في الدرس`;
    case "compare": return `{"a":"الشيء الأول","b":"الشيء الثاني","same":["وجه شبه"],"onlyA":["ما ينفرد به الأول"],"onlyB":["ما ينفرد به الثاني"]} — ${ce} عناصر على الأكثر في كل قائمة`;
    case "cause": return `{"event":"الحدث أو الظاهرة","causes":["سبب"],"effects":["نتيجة"]} — ${ce} أسباب و${ce} نتائج على الأكثر`;
    case "cycle": return `{"title":"اسم الدورة","stages":[{"label":"المرحلة (١–٣ كلمات)","icon":"إيموجي","note":"توضيح قصير اختياري"}]} — ${Math.max(3, b - 1)}–${b + 1} مراحل بترتيبها`;
  }
  return "";
}

function clean(type: string, r: Any): Any | null {
  if (!r || typeof r !== "object") return null;
  const ic = (v: unknown) => S(v, 8);
  switch (type) {
    case "concept": {
      const nodes = A(r.nodes).slice(0, 12).map((n: Any, i: number) => ({ id: S(n?.id, 12) || "n" + (i + 1), label: S(n?.label, 40), level: Math.min(3, Math.max(1, Number(n?.level) || 1)), icon: ic(n?.icon) })).filter((n: Any) => n.label && n.id !== "root");
      const ids = new Set(["root", ...nodes.map((n: Any) => n.id)]);
      const links = A(r.links).slice(0, 20).map((l: Any) => ({ from: S(l?.from, 12), to: S(l?.to, 12), label: S(l?.label, 30) })).filter((l: Any) => ids.has(l.from) && ids.has(l.to) && l.from !== l.to);
      return nodes.length >= 2 ? { title: S(r.title, 50), nodes, links } : null;
    }
    case "radial": {
      const branches = A(r.branches).slice(0, 8).map((b: Any) => ({ label: S(b?.label, 40), icon: ic(b?.icon), items: L(b?.items, 5, 60) })).filter((b: Any) => b.label);
      return branches.length >= 2 ? { center: S(r.center, 50), branches } : null;
    }
    case "tree": {
      const children = A(r.children).slice(0, 5).map((b: Any) => ({ label: S(b?.label, 40), icon: ic(b?.icon), items: L(b?.items, 6, 60) })).filter((b: Any) => b.label);
      return children.length >= 2 ? { root: S(r.root, 60), children } : null;
    }
    case "flow": case "cycle": {
      const k = type === "flow" ? "steps" : "stages";
      const arr = A(r[k]).slice(0, 9).map((s: Any) => ({ label: S(s?.label, 40), icon: ic(s?.icon), note: S(s?.note, 70) })).filter((s: Any) => s.label);
      return arr.length >= 3 ? { title: S(r.title, 60), [k]: arr } : null;
    }
    case "compare": {
      const o = { a: S(r.a, 40), b: S(r.b, 40), same: L(r.same, 5), onlyA: L(r.onlyA, 5), onlyB: L(r.onlyB, 5) };
      return o.a && o.b && (o.same.length + o.onlyA.length + o.onlyB.length) >= 3 ? o : null;
    }
    case "cause": {
      const o = { event: S(r.event, 50), causes: L(r.causes, 5, 70), effects: L(r.effects, 5, 70) };
      return o.event && o.causes.length + o.effects.length >= 2 ? o : null;
    }
  }
  return null;
}

const STYLE: Record<string, string> = {
  cartoon: "cute flat cartoon style with soft pastel colors",
  flat: "clean modern flat vector style, few harmonious colors, lots of white space, thin line icons",
  hand: "hand-drawn sketchnote style with colored pencils on white paper, slightly wobbly lines",
  chalk: "dark green chalkboard with colorful chalk drawings and real chalk texture",
  clay: "soft glossy 3D claymorphism elements with gentle shadows on a light background",
};
function bgDecor(subject: string): string {
  if (/رياض/.test(subject)) return "rulers, set squares, protractors, colorful geometric shapes, stars";
  if (/علوم|أحياء|كيمياء|فيزياء/.test(subject)) return "leaves, plants, a microscope, test tubes, atoms shapes, a magnifying glass, stars";
  if (/عربية|لغة|أدب/.test(subject)) return "open books, a quill and inkwell, a lightbulb, empty speech bubbles, subtle arabesque patterns";
  if (/إسلام|اسلام|قرآن/.test(subject)) return "a lantern, crescent and stars, an open book on a wooden stand, subtle Islamic geometric patterns";
  if (/دراسات|جغراف|تاريخ/.test(subject)) return "a globe, a compass, a folded map, palm trees, a falaj water channel, Omani fort silhouette";
  return "books, pencils, a lightbulb, stars and sparkles";
}
function bgPrompt(subject: string, unit: string, style: string, aspect: string): string {
  return [
    `A ${aspect === "16:9" ? "wide 16:9" : aspect === "1:1" ? "square" : "portrait 3:4"} decorative BACKGROUND for a school concept-map poster about the unit «${unit}».`,
    `Style: ${STYLE[style] || STYLE.cartoon}.`,
    `Small wordless decorations only along the outer edges and corners: ${bgDecor(subject)}.`,
    "The large central area (about 84% of the width and 84% of the height) must be a clean, plain, light, EMPTY area with nothing drawn in it — a concept map will be placed there later.",
    "ABSOLUTELY NO text of any kind: no letters, no Arabic or Latin words, no numbers or digits, no symbols, no labels, no writing on books or signs.",
  ].join(" ");
}

async function publicIfExists(admin: Any, key: string): Promise<string> {
  const dir = key.split("/").slice(0, -1).join("/"), name = key.split("/").pop();
  const { data } = await admin.storage.from("library-files").list(dir, { search: name });
  return A(data).some((o: Any) => o.name === name) ? admin.storage.from("library-files").getPublicUrl(key).data.publicUrl : "";
}

// يُستدعى بعد takeQuota(img). كل خروجٍ بخطأ يستردّ الحصّة.
export async function layeredConcept(admin: Any, user: Any, st: Record<string, string>, apiKey: string, b: Any, json: (x: unknown, s?: number) => Response): Promise<Response> {
  const refund = async (body: Record<string, unknown>, status: number) => { await refundQuota(admin, user.id, user.email || "", "img"); return json(body, status); };
  const o = b.concept && typeof b.concept === "object" ? b.concept : {};
  const type = (CM_TYPES as readonly string[]).includes(o.type) ? o.type : "concept";
  const detail = ["1", "2", "3"].includes(String(o.detail)) ? String(o.detail) : "2";
  const style = STYLE[o.style] ? o.style : "cartoon";
  const aspect = ["3:4", "16:9", "1:1"].includes(o.aspect) ? o.aspect : "3:4";
  const grade = String(b.grade || ""), subject = String(b.subject || ""), unit = String(b.unit || "");
  const lesson = String(A(b.lessonNames)[0] || "");
  const cur = await curFor(admin, grade, subject, unit, lesson).catch(() => null);
  if (!cur) return await refund({ error: "no_lesson" }, 404);
  const ex = await bookExtract(admin, st, apiKey, cur, A(b.images).slice(0, 8).map(String), { grade, subject, userId: user.id }).catch(() => null);
  if (!ex || !ex.summary) return await refund({ error: "no_extract", message: "تعذّرت قراءة صفحات الدرس من الكتاب." }, 409);

  // ١) الهيكل — أو هيكل المعلّم نفسه عند «خلفية جديدة» فقط
  let map: Any = b.map && typeof b.map === "object" ? clean(type, b.map) : null;
  if (!map) {
    const e = ex.exam || {};
    const src = [
      "ملخّص صفحات الدرس:\n" + String(ex.summary).slice(0, 6000),
      e.rules?.length ? "القواعد والتعريفات:\n- " + e.rules.slice(0, 14).join("\n- ") : "",
      e.vocabulary?.length ? "المصطلحات:\n- " + e.vocabulary.slice(0, 14).map((v: Any) => v.ar + (v.def ? ": " + v.def : "")).join("\n- ") : "",
      e.figures?.length ? "الأشكال والأنشطة:\n- " + e.figures.slice(0, 8).join("\n- ") : "",
    ].filter(Boolean).join("\n\n");
    const young = Number(grade) <= 4;
    const sys = [
      "أنت مصمّم تعليمي خبير في المنظِّمات البصرية (خرائط المفاهيم لنوفاك، والخرائط الذهنية لبوزان، وخرائط التفكير لهيرل). ابنِ خريطة لدرسٍ واحد من مستخلص صفحات الكتاب المرفق وحده.",
      `الدرس: «${cur.lesson}» — ${cur.unit} — ${subject} — الصف ${grade}.`,
      "الشروط: كلمات مفتاحية قصيرة لا جُمل طويلة؛ عربية فصحى سليمة إملائياً؛ انقل المصطلحات والأرقام كما وردت؛ لا تُضف معلومة ليست في المستخلص؛ رتّب العناصر بترتيب الدرس؛ لكل عقدة رئيسية إيموجي واحد يدلّ على معناه (لا تكرّره).",
      type === "compare" || type === "cause" || type === "cycle" || type === "flow"
        ? "إن لم يكن في الدرس ما يناسب هذا النوع تماماً، فابنِه من أقرب ما في الدرس (مثلاً: مقارنة بين مفهومين من الدرس، أو مراحل عملية وردت فيه) ولا تختلق محتوى."
        : "",
      young ? "الطلاب صغار (الصفوف ١–٤): كلمات قليلة سهلة." : "",
      S(o.extra, 600) ? `توجيهات المعلّم (لها الأولوية ما لم تخالف الشروط): ${S(o.extra, 600)}` : "",
      `أعد JSON فقط بهذا الشكل: ${shapeFor(type, detail)}`,
    ].filter(Boolean).join("\n");
    const model = st.model_mindmap || st.model_summary || "google/gemini-2.5-flash";
    const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta Layered Concept Map" },
      body: JSON.stringify({ model, temperature: 0.25, max_tokens: 3000, response_format: { type: "json_object" }, messages: [{ role: "system", content: sys }, { role: "user", content: src }] }),
    }, { st, task: "summary" });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) return await refund({ error: "provider_error", detail: String(j?.error?.message || "").slice(0, 200) }, 502);
    await logAiCost(admin, user.id, "generate-infographic", "text", model, j?.usage);
    const p = parseAiJson(String(j?.choices?.[0]?.message?.content || ""));
    map = p.ok ? clean(type, p.value) : null;
    if (!map) return await refund({ error: "bad_output" }, 502);
  }

  // ٢) الخلفية — «نصّ فقط» بلا رسم؛ وإلا خلفية الوحدة والنمط والمقاس (محفوظة)
  if (o.art === "none") { await refundQuota(admin, user.id, user.email || "", "img"); return json({ cmLayered: true, type, map, art: "", cached: true }); }
  const key = `info-bg/cm1-${hash(`${grade}|${subject}|${cur.unit}|${style}|${aspect}`)}.img`;
  if (!b.redraw) {
    const url = await publicIfExists(admin, key);
    if (url) { await refundQuota(admin, user.id, user.email || "", "img"); return json({ cmLayered: true, type, map, art: url, cached: true }); }
  }
  let model = st.model_infographic || st.slide_model || "google/gemini-3.1-flash-image-preview";
  if (!model.startsWith("google/")) model = "google/gemini-3.1-flash-image-preview";
  let img = "", usage: unknown = null, lastErr = "";
  for (const cfg of [{ aspect_ratio: aspect, image_size: "1K" }, { aspect_ratio: aspect }]) {
    const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta Layered Concept Map" },
      body: JSON.stringify({ model, messages: [{ role: "user", content: bgPrompt(subject, cur.unit, style, aspect) }], modalities: ["image", "text"], image_config: cfg }),
    }, { st, task: "infographic" });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) { lastErr = String(j?.error?.message || j?.message || r.status); if (r.status === 402) break; continue; }
    img = j?.choices?.[0]?.message?.images?.[0]?.image_url?.url || ""; usage = j?.usage || null;
    if (img) break;
  }
  // الخلفية زينة: إن تعذّر رسمها تُرسم الخريطة على خلفيةٍ سادة بدل أن تفشل كلها
  if (!img) { await refundQuota(admin, user.id, user.email || "", "img"); return json({ cmLayered: true, type, map, art: "", cached: false, art_error: lastErr ? orErrCode(502, lastErr) : "no_image" }); }
  await logAiCost(admin, user.id, "generate-infographic", "img", model, usage);
  try {
    const bin = Uint8Array.from(atob(img.split(",")[1] || ""), (c) => c.charCodeAt(0));
    const ct = (img.match(/^data:([^;]+)/) || [])[1] || "image/png";
    await admin.storage.from("library-files").upload(key, new Blob([bin], { type: ct }), { upsert: true, contentType: ct, cacheControl: "31536000" });
  } catch (e) { console.error("cm bg cache", String(e)); }
  return json({ cmLayered: true, type, map, art: img, cached: false });
}
