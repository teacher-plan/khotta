// ════════════════════════════════════════════════════════════════
// Edge Function: generate-mindmap (١٩ نوفمبر — تجريبيّ لحساب المطوّر)
// يبني محتوى الخرائط الذهنية للدرس من «مستخلص صفحات الدرس» الذي يُنتجه التحضير
// (book-extracts/{curriculum.id}.json) — نصّاً لا صوراً، فالتكلفة زهيدة.
// المخرج JSON يرسمه المتصفّح (لا نموذج صور: العربية تبقى صحيحة):
//   الشعاعية دائماً + نوعٌ أو نوعان يلائمان طبيعة الدرس (شجرية للتصنيف، تدفّق للإجراءات).
// يُخزَّن في library-files/mindmaps/{curriculum.id}.json فيأخذه كل معلّمٍ بعده جاهزاً.
// ════════════════════════════════════════════════════════════════
import { withSubject, isEnglishSubject } from "../_shared/subjectProfile.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { takeQuota, refundQuota, logAiCost } from "../_shared/quota.ts";
import { orFetch } from "../_shared/ai.ts";
import { parseAiJson } from "../_shared/aiJson.ts";
import { curFor, readCache, bookKey } from "../_shared/lessonExtract.ts";

// deno-lint-ignore no-explicit-any
type Any = any;
const LAB_EMAILS = ["xx@y.com", "teacherplane2026project@gmail.com", "abdulrahman.demo@khotati.com"];
const MM_VERSION = 1;
const mmVersion = (subject: string) => (isEnglishSubject(subject) ? 2 : MM_VERSION);
const mmKey = (curId: number | string) => `mindmaps/${curId}.json`;
const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { ...cors, "Content-Type": "application/json" } });

const SHAPE = {
  icon: "إيموجي واحد يرمز للدرس كله",
  maps: [
    { type: "radial", center: "عنوان الدرس مختصراً (٢–٥ كلمات)", branches: [{ label: "فكرة رئيسية (١–٣ كلمات)", icon: "إيموجي", items: ["تفصيل قصير (٢–٦ كلمات)"] }] },
    { type: "tree", root: "سؤال أو عنوان التصنيف", children: [{ label: "فئة", icon: "إيموجي", items: ["عنصر"] }] },
    { type: "flow", title: "عنوان الإجراء", steps: [{ label: "الخطوة (١–٤ كلمات)", icon: "إيموجي", note: "توضيح قصير اختياري" }] },
  ],
};

function clean(m: Any): Any | null {
  const s = (v: unknown, n = 80) => String(v ?? "").replace(/\s+/g, " ").trim().slice(0, n);
  const arr = (v: unknown) => (Array.isArray(v) ? v : []);
  if (!m || typeof m !== "object") return null;
  if (m.type === "radial") {
    const branches = arr(m.branches).slice(0, 8).map((b: Any) => ({ label: s(b?.label, 40), icon: s(b?.icon, 8), items: arr(b?.items).slice(0, 5).map((x) => s(x, 60)).filter(Boolean) })).filter((b) => b.label);
    return branches.length >= 2 ? { type: "radial", center: s(m.center, 50), branches } : null;
  }
  if (m.type === "tree") {
    const children = arr(m.children).slice(0, 5).map((b: Any) => ({ label: s(b?.label, 40), icon: s(b?.icon, 8), items: arr(b?.items).slice(0, 6).map((x) => s(x, 70)).filter(Boolean) })).filter((b) => b.label);
    return children.length >= 2 ? { type: "tree", root: s(m.root, 60), children } : null;
  }
  if (m.type === "flow") {
    const steps = arr(m.steps).slice(0, 8).map((b: Any) => ({ label: s(b?.label, 40), icon: s(b?.icon, 8), note: s(b?.note, 60) })).filter((b) => b.label);
    return steps.length >= 3 ? { type: "flow", title: s(m.title, 60), steps } : null;
  }
  return null;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const auth = req.headers.get("Authorization");
    if (!auth) return json({ error: "unauthorized" }, 401);
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const { data: { user } } = await admin.auth.getUser(auth.replace("Bearer ", ""));
    if (!user) return json({ error: "unauthorized" }, 401);
    if (!LAB_EMAILS.includes((user.email || "").toLowerCase())) return json({ error: "forbidden" }, 403);

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || ""), subject = String(b.subject || ""), unit = String(b.unit || ""), lesson = String(b.lesson || "");
    if (!grade || !subject || !lesson) return json({ error: "bad_input" }, 400);
    const cur = await curFor(admin, grade, subject, unit, lesson).catch(() => null);
    if (!cur) return json({ error: "no_lesson", message: "الدرس غير موجود في المنهج." }, 404);

    if (!b.force) {
      const c = await readCache(admin, mmKey(cur.id));
      if (c && c.v === mmVersion(subject) && Array.isArray(c.maps) && c.maps.length) return json({ ...c, cached: true });
    }
    // المصدر: ما قرأه التحضير من صفحات الدرس — لا نقرأ الصور مرّةً أخرى
    const ex = await readCache(admin, bookKey(cur.id));
    if (!ex || !ex.summary) return json({ error: "no_extract", message: "حضّر الدرس أولاً: الخرائط تُبنى من قراءة صفحات الدرس أثناء التحضير." }, 409);

    const apiKey = Deno.env.get("OPENROUTER_API_KEY");
    if (!apiKey) return json({ error: "server_not_configured" }, 500);
    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });

    const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
    if (!quota.ok) return quota.error === "quota_unavailable" ? json({ error: "quota_unavailable" }, 503) : json({ error: "quota_exceeded" }, 429);
    const refund = async (body: Record<string, unknown>, status: number) => { await refundQuota(admin, user.id, user.email || "", "text"); return json(body, status); };

    const e = ex.exam || {};
    const src = [
      `الصف: ${grade} | المادة: ${subject} | ${cur.unit} | الدرس: ${cur.lesson}`,
      "ملخّص صفحات الدرس:\n" + ex.summary,
      e.rules?.length ? "القواعد والتعريفات:\n- " + e.rules.join("\n- ") : "",
      e.vocabulary?.length ? "المفردات:\n- " + e.vocabulary.map((v: Any) => `${v.ar}${v.def ? ": " + v.def : ""}`).join("\n- ") : "",
      e.worked_examples?.length ? "أمثلة محلولة:\n- " + e.worked_examples.slice(0, 4).map((w: Any) => `${w.problem} ← ${w.answer}`).join("\n- ") : "",
      e.figures?.length ? "الأشكال:\n- " + e.figures.slice(0, 6).join("\n- ") : "",
    ].filter(Boolean).join("\n\n").slice(0, 9000);
    const young = Number(grade) <= 4;
    const system = [
      "أنت مصمّم تعليمي خبير في المنظِّمات البصرية (الخرائط الذهنية لبوزان وخرائط التفكير لهيرل). أمامك مستخلص صفحات درسٍ واحد من كتابٍ عُماني معتمد.",
      "ابنِ محتوى خرائط ذهنية للدرس من هذا المستخلص وحده: لا تُضف معلومة ليست فيه، وانقل المصطلحات والأرقام والرموز كما وردت.",
      "القواعد: كلماتٌ مفتاحية قصيرة لا جُمل طويلة؛ عربيةٌ فصحى سليمة؛ رتّب الفروع بترتيب ورودها في الدرس؛ لكل فرعٍ وخطوةٍ إيموجي واحد يدلّ على معناه بوضوح (لا تكرّر الإيموجي نفسه).",
      young ? "الطلاب صغار (الصفوف ١–٤): ٣–٥ فروع، وتفصيلتان أو ثلاث لكل فرع، بكلماتٍ يفهمها الطفل." : "٤–٦ فروع، و٢–٤ تفاصيل لكل فرع.",
      "أعد دائماً الخريطة الشعاعية (radial) للدرس كله. ثم أضف نوعاً أو نوعين فقط إن كان الدرس يناسبهما فعلاً: tree إن كان فيه تصنيفٌ أو أنواع أو أقسام، وflow إن كان فيه إجراءٌ أو خطواتٌ متسلسلة أو مراحل (٣–٨ خطوات). لا تختلق تصنيفاً أو خطواتٍ غير موجودة.",
      `أعد JSON فقط بهذا الشكل: ${JSON.stringify(SHAPE)}`,
    ].join("\n");
    const model = st.model_mindmap || st.model_summary || "google/gemini-2.5-flash";
    const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta Mind Maps" },
      body: JSON.stringify({ model, messages: [{ role: "system", content: withSubject(system, subject, "mindmap") }, { role: "user", content: src }], temperature: 0.3, max_tokens: 4000, response_format: { type: "json_object" } }),
    }, { st, task: "summary" });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) return await refund({ error: "provider_error", detail: String(j?.error?.message || "").slice(0, 200) }, 502);
    await logAiCost(admin, user.id, "generate-mindmap", "text", model, j?.usage);
    const p = parseAiJson(String(j?.choices?.[0]?.message?.content || ""));
    const raw: Any = p.ok ? p.value : null;
    const maps = (Array.isArray(raw?.maps) ? raw.maps : []).map(clean).filter(Boolean);
    if (!maps.some((m: Any) => m.type === "radial")) return await refund({ error: "bad_output" }, 502);
    const out = { v: mmVersion(subject), cur_id: cur.id, lesson: cur.lesson, unit: cur.unit, grade, subject, icon: String(raw?.icon || "").slice(0, 8), maps, model, at: new Date().toISOString() };
    await admin.storage.from("library-files").upload(mmKey(cur.id), new Blob([JSON.stringify(out)], { type: "application/json" }), { upsert: true, contentType: "application/json" });
    return json(out);
  } catch (e) {
    console.error("generate-mindmap", String(e));
    return json({ error: "server_error" }, 500);
  }
});
