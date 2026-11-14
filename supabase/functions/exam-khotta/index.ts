// v2026.11.14 ════════════════════════════════════════════════════════════════
// Edge Function: exam-khotta — «اختبار قصير» و«سؤال قصير» بمواصفات وثيقة تقويم تعلّم الطلبة
// (الرياضيات ٥–١٠) — منقولةٌ من مهارة exam-khotta في المستودع (exam-khotta-skill/):
//   • المواصفات وقواعد الكتابة من spec.ts (مولَّد بـ tools/sync-exam-spec.py)، لا نسخة ثانية تتخلّف.
//   • يقرأ النموذجُ صفحاتِ الدروس من كتاب الطالب وصفحاتِ دليل المعلم (الأهداف برموزها والأخطاء الشائعة)
//     من مكتبة المنصّة نفسها، ويكتب النموذجين (أ) و(ب) بالشبكة نفسها.
//   • الفحص على الخادم بقواعد الوثيقة (المجموع، التوزيع على AO والصعوبة، الأنواع والعدد، تطابق النموذجين…)،
//     وعند المخالفة يُعاد الطلب مرّة واحدة بقائمة الأخطاء. لا يُسلَّم اختبارٌ مخالف بصمت.
// المرحلة الأولى: لحسابات المختبر فقط (LAB_EMAILS).
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { takeQuota, refundQuota, logAiCost } from "../_shared/quota.ts";
import { parseAiJson } from "../_shared/aiJson.ts";
import { orFetch, orErrCode } from "../_shared/ai.ts";
import { SPEC_MATH, WRITING, MATH_RULES } from "./spec.ts";
import { validate, SUBJECT, OTHER, ar, band } from "./validate.ts";
import { isServiceRoleRequest } from "../_shared/adminGuard.ts";
import { readCache, bookKey, guideKey, bookExtract, guideContextFor, EXTRACT_VERSION } from "../_shared/lessonExtract.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
// deno-lint-ignore no-explicit-any
type Any = any;

// قواعد الدرجات — تفصيلية لأن النموذج كان يضع درجتين على اختيار من متعدد ودرجةً واحدة على «أوجد جميع العوامل».
const MARKS_RULES = (kind: string) => [
  "قواعد الدرجات (إلزامية، ويُرفض الاختبار المخالف):",
  "١) الاختيار من متعدد = درجة واحدة دائماً، في كل الأدوات وكل الصفوف. لا تكتب marks: 2 لمفردة mcq أبداً.",
  "٢) الدرجة تساوي عدد ما يُصحَّح مستقلاً: مفردة الدرجة الواحدة لها إجابة واحدة وخطوة واحدة (استدعاء، حساب مباشر، إكمال فراغ واحد).",
  "٣) المفردة التي تطلب عدّة إجابات (أوجد جميع العوامل، اكتب كل المضاعفات حتى…، اذكر ثلاثة…) أو حلاً من خطوتين فأكثر درجتها ٢ على الأقل، وفي الإرشادات: «درجة لـ… ودرجة لـ…» (مثال: جميع عوامل ٢٠ = ١، ٢، ٤، ٥، ١٠، ٢٠ — درجتان: درجة لثلاثة عوامل صحيحة على الأقل، ودرجة لاكتمالها دون زيادة).",
  "٤) مفردة الدرجتين أو الثلاث: اكتب خطوات حلّها في steps (خطوة لكل درجة على الأقل) أو قسّمها أجزاءً في parts (جزء لكل درجة). وإن كانت أجزاء فلكل جزء درجة.",
  "٥) لا تضع درجة واحدة على سؤال من أجزاء (أ، ب)، ولا درجات كثيرة على سؤال من خطوة واحدة.",
  kind === "quiz"
    ? "٦) السؤال القصير (٥ درجات): أحد ثلاثة توزيعات فقط — ثلاث مفردات ١+٢+٢ أو ١+١+٣، أو مفردتان ٢+٣. مفردة اختيار من متعدد واحدة على الأكثر وبدرجة ١. مفردة الثلاث درجات تكون بأجزاء (أ، ب، ج) لكل جزء درجة أو بثلاث خطوات مستقلّة."
    : "٦) الاختبار القصير: التزم بدرجات الشبكة حرفياً؛ ومفردة الدرجتين فيها خطوتان مستقلّتان على الأقل.",
].join("\n");

const LAB_EMAILS = ["xx@y.com", "teacherplane2026project@gmail.com"];
Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const auth = req.headers.get("Authorization") || "";
    if (!auth) return json({ error: "unauthorized" }, 401);
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    // اختبارٌ من GitHub Actions: مفتاح الخدمة + x-lab-as (حساب مختبر) — بلا جلسة متصفّح
    let user: Any = null;
    const labAs = (req.headers.get("x-lab-as") || "").trim().toLowerCase();
    if (labAs && isServiceRoleRequest(req)) {
      if (!LAB_EMAILS.includes(labAs)) return json({ error: "forbidden" }, 403);
      const { data } = await admin.auth.admin.listUsers({ page: 1, perPage: 1000 });
      user = (data?.users || []).find((u: Any) => String(u.email || "").toLowerCase() === labAs) || null;
    } else {
      const { data: { user: u } } = await admin.auth.getUser(auth.replace("Bearer ", ""));
      user = u;
    }
    if (!user) return json({ error: "unauthorized" }, 401);
    if (!LAB_EMAILS.includes(String(user.email || "").toLowerCase())) return json({ error: "forbidden", message: "هذه الخاصية تجريبية ولم تُفتح لحسابك بعد." }, 403);
    const apiKey = Deno.env.get("OPENROUTER_API_KEY");
    if (!apiKey) return json({ error: "server_not_configured" }, 500);

    const b = await req.json().catch(() => ({}));
    const kind = b.kind === "quiz" ? "quiz" : "short_test";
    const tool = SPEC_MATH.tools[kind];
    const grade = parseInt(b.grade) || 0;
    if (!SPEC_MATH.grades.includes(grade)) return json({ error: "bad_grade", message: "المواصفات المتاحة للرياضيات ٥–١٠." }, 400);
    const semester = String(b.semester || "الفصل الأول");
    const number = Math.max(1, Math.min(2, parseInt(b.number) || 1));
    const wanted: { unit: string; lesson: string }[] = (Array.isArray(b.lessons) ? b.lessons : []).map((x: Any) => ({ unit: String(x.unit || ""), lesson: String(x.lesson || "") }));
    if (wanted.length < tool.lessons[0] || wanted.length > tool.lessons[1])
      return json({ error: "bad_lessons", message: `${tool.name}: حدّد ${ar(tool.lessons[0])}–${ar(tool.lessons[1])} دروس.` }, 400);
    const gridName = kind === "short_test" ? String(b.grid || "مقترح ١") : "";
    const gridRows: Any[] | null = kind === "short_test" ? ((tool.grids[band(grade, tool.grids)] || {})[gridName] || null) : null;

    // ── الدروس وصفحاتها من curriculum + book_sources + teacher_guides ──
    const { data: cur } = await admin.from("curriculum").select("id,unit,lesson,sort,page,book_no")
      .eq("semester", semester).eq("grade", grade).eq("subject", SUBJECT).order("sort");
    const rows: Any[] = cur || [];
    const sel = wanted.map((w) => rows.find((r) => r.unit === w.unit && r.lesson === w.lesson)).filter(Boolean);
    if (sel.length !== wanted.length) return json({ error: "lesson_not_found", message: "تعذّر العثور على بعض الدروس في المنهج." }, 400);
    const { data: bs } = await admin.from("book_sources").select("*").eq("grade", String(grade)).eq("subject", SUBJECT).eq("semester", semester).eq("book_no", 1).maybeSingle();
    const { data: tg } = await admin.from("teacher_guides").select("id,base_path,page_count,offset_pages,toc").eq("grade", grade).eq("subject", SUBJECT).eq("semester", semester).maybeSingle();
    const pub = (base: string, sheet: number) => admin.storage.from("library-files").getPublicUrl(`${base}/p${sheet}.jpg`).data.publicUrl;
    const codeOf = (r: Any) => (String(r.lesson).match(/^\s*([0-9٠-٩]+\s*[-–]\s*[0-9٠-٩]+)/) || [])[1]?.replace(/\s/g, "").replace(/[–]/g, "-") || ar(r.sort);
    const lessonsOut: Any[] = [];
    const bookImgs: Record<string, { url: string; tag: string }[]> = {}, guideImgs: Record<string, { url: string; tag: string }[]> = {};
    const perBook = Math.max(2, Math.floor(18 / sel.length)), perGuide = Math.max(1, Math.floor(8 / sel.length));
    for (const r of sel) {
      const i = rows.findIndex((x) => x.id === r.id);
      const start = parseInt(r.page) || 0;
      let end = start;
      for (let j = i + 1; j < rows.length; j++) { const np = parseInt(rows[j].page); if (np && np > start) { end = np - 1; break; } }
      const code = ar(codeOf(r)), title = String(r.lesson).replace(/^\s*[0-9٠-٩]+\s*[-–]\s*[0-9٠-٩]+\s*/, "");
      lessonsOut.push({ code, title, unit: r.unit, pages: start ? (end > start ? `${ar(start)}–${ar(end)}` : ar(start)) : "" });
      if (bs?.base_path && start) {
        const off = bs.offset_pages || 1;
        const L = bookImgs[r.id] = [] as { url: string; tag: string }[];
        for (let p = start; p <= end && L.length < 20; p++) {
          const sh = p + off - 1; if (sh >= 1 && sh <= (bs.page_count || 9999)) L.push({ url: pub(bs.base_path, sh), tag: `كتاب الطالب — الدرس ${code} — ص ${ar(p)}` });
        }
      }
      const toc: Any[] = Array.isArray(tg?.toc) ? tg!.toc : [];
      const e = toc.find((x) => x.matched_curriculum_id === r.id);
      if (tg?.base_path && e?.guide_page) {
        const sorted = toc.filter((x) => x.guide_page).map((x) => x.guide_page).sort((a: number, b: number) => a - b);
        const gs = e.guide_page; const ge = (sorted.find((p: number) => p > gs) || gs + 3) - 1;
        const off = tg.offset_pages || 1;
        const L = guideImgs[r.id] = [] as { url: string; tag: string }[];
        for (let p = gs; p <= ge && L.length < perGuide; p++) {
          const sh = p + off - 1; if (sh >= 1 && sh <= (tg.page_count || 9999)) L.push({ url: pub(tg.base_path, sh), tag: `دليل المعلم — الدرس ${code} — ص ${ar(p)}` });
        }
      }
    }
    if (!sel.some((r) => (bookImgs[r.id] || []).length)) return json({ error: "no_pages", message: "لا توجد صفحات كتابٍ مرفوعة لهذه الدروس في مكتبة المنصّة." }, 400);
    const codes = lessonsOut.map((l) => l.code);

    // ── الطلب ──
    const { data: stRows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (stRows || []).forEach((x: { key: string; value: string }) => { st[x.key] = x.value; });
    const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
    if (!quota.ok) return json({ error: "quota_exceeded", message: "نفدت حصّة الذكاء الاصطناعي." }, 429);
    const model = st.model_exam_khotta || "google/gemini-2.5-pro";

    // ── محتوى الدروس نصّاً (اقتراح الأستاذ عيسى): ما قُرئ عند التحضير مخزَّنٌ للمنصّة كلها —
    // مستخلص كتاب الطالب (book-extracts/) ومستخلص دليل المعلم (guide-summaries/). الدرس الذي
    // لم يُحضَّر بعد يُقرأ الآن بنموذج الرؤية الاقتصادي ويُخزَّن، ولا نرجع إلى الصور إلا عند الفشل.
    const T0 = Date.now();
    const within = <T,>(pr: Promise<T>, ms: number, dflt: T) => Promise.race([pr.catch(() => dflt), new Promise<T>((res) => setTimeout(() => res(dflt), ms))]);
    const texts = await Promise.all(sel.map(async (r) => {
      const cur = { ...r, semester };
      let bx: Any = await readCache(admin, bookKey(r.id));
      if (!(bx && bx.v === EXTRACT_VERSION && bx.exam)) {
        bx = await within(bookExtract(admin, st, apiKey, cur, (bookImgs[r.id] || []).map((x) => x.url), { grade, subject: SUBJECT, userId: user.id }), 70_000, null);
      }
      let gx: Any = tg?.id ? await readCache(admin, guideKey(tg.id, r.id)) : null;
      if (!gx && tg?.id && (guideImgs[r.id] || []).length) {
        const t = await within(guideContextFor(admin, st, apiKey, String(grade), SUBJECT, r.unit, r.lesson, semester), 60_000, "");
        try { gx = t ? JSON.parse(t) : null; } catch { gx = null; }
      }
      return { bx: bx && bx.exam ? bx : null, gx };
    }));
    const images: { url: string; tag: string }[] = [];
    sel.forEach((r, i) => {
      if (!texts[i].bx) images.push(...(bookImgs[r.id] || []).slice(0, perBook));
      if (!texts[i].gx) images.push(...(guideImgs[r.id] || []));
    });
    const textLessons = texts.filter((t) => t.bx).length;

    const bg = kind === "short_test" ? tool.by_grade[band(grade, tool.by_grade)] : null;
    const calc = kind === "short_test" ? (tool.calculator[band(grade, tool.calculator)] ? "يُسمح بالآلة الحاسبة." : "لا آلة حاسبة: أعداد تُحسب ذهنياً أو كتابياً بسرعة.") : "";
    const gridText = gridRows ? gridRows.map((r, i) => `${i + 1}) ${r[0] === "other" ? "أي نوع من الأنواع الأخرى (" + OTHER.join("/") + ")" : r[0]}، ${r[1]}، ${r[2]}، ${r[3]} درجة`).join("\n") : "";
    const itemShape = `{"type":"mcq|short|fill|tf|match|order|table|explain|creative|long",${kind === "short_test" ? '"ao":"AO1|AO2|AO3","level":"L|M|H",' : ""}"marks":1,"lesson":"رمز الدرس من القائمة","page":"ص ٢٤–٢٥","objective":"الهدف التعليمي برمزه من الدليل إن وُجد","stem":"نص السؤال","choices":["للـmcq أربعة بدائل"],"answer":"الإجابة (للـmcq رقم البديل الصحيح ٠–٣)","steps":["خطوات الحل إن وُجدت"],"guidance":"توزيع الدرجة وما يُقبل","lines":1,"parts":[{"label":"أ","stem":"…","lines":1}],"explain":true,"left":[],"right":[],"pairs":[],"items":[],"grid":{"rows":[["",""]],"header":true}}`;
    const system = [
      "أنت خبير تقويم في الرياضيات بسلطنة عُمان، تُعدّ أدوات التقويم مطابقةً حرفياً لوثيقة تقويم تعلّم الطلبة المعتمدة.",
      `الوثيقة: ${SPEC_MATH.document.title} (${SPEC_MATH.document.edition}).`,
      `الأداة: ${tool.name} — الدرجة ${tool.total}، المفردات ${tool.items[0]}–${tool.items[1]}، الدروس ${tool.lessons[0]}–${tool.lessons[1]}، الزمن ${tool.duration_text}.`,
      "قواعد الوثيقة لهذه الأداة:\n- " + tool.rules.join("\n- "),
      kind === "short_test" ? `أهداف التقويم: ${Object.entries(SPEC_MATH.ao).map(([k, v]: Any) => `${k} ${v.name}`).join("، ")}. الصعوبة: ${Object.entries(SPEC_MATH.levels).map(([k, v]: Any) => `${k} ${v.name}: ${v.desc}`).join(" | ")}` : "",
      bg ? `للصف ${grade}: اختيار من متعدد ${bg.mcq.count} مفردتان بدرجة ${bg.mcq.each}؛ ${bg.long ? `إجابة طويلة واحدة بـ${bg.long.marks} درجات (أجزاء أ، ب، ج لكل جزء درجة)؛ ` : ""}مفردات أخرى ${bg.other.count[0]}–${bg.other.count[1]} مجموعها ${bg.other.marks} درجات، كلٌّ بـ${bg.other.each[0]}–${bg.other.each[1]}. ${calc}` : "",
      gridRows ? `الشبكة المعتمدة (${gridName}) — التزم بها بالترتيب حرفياً (النوع، الهدف، الصعوبة، الدرجة) في النموذجين:\n${gridText}` : "",
      MARKS_RULES(kind),
      "قواعد كتابة المفردات (إلزامية):\n" + WRITING,
      "كتابة الرموز في الرياضيات:\n" + MATH_RULES,
      "المرفق لكل درس: مستخلص نصّي أمين لصفحاته من كتاب الطالب (الأهداف، القواعد، الأمثلة المحلولة، التمارين بنصّها، الأشكال)، ومستخلص دليل المعلم (الأهداف برموزها، الأخطاء الشائعة، التمارين)؛ وقد تُرفق صور الصفحات لدرسٍ لم يُستخلص بعد. ابنِ المفردات منها وفي حدود أهدافها، ولا تنسخ تمريناً أو مثالاً حرفياً — غيّر الأعداد والسياق.",
      "رمز الهدف في objective: انقله من objectives في المستخلص (الدليل ثم الكتاب) كما هو؛ وإن لم يوجد رمز فاكتب نصّ الهدف بلا رمز. لا تخترع رمزاً أبداً.",
      "حلّ كل مفردة بنفسك قبل كتابتها وتأكّد: إجابة واحدة صحيحة، وكل بديل خاطئ خاطئٌ فعلاً، والإرشادات أعداد صحيحة.",
      "الإجابة الطويلة: الأجزاء في parts، وإجابة كل جزء سطراً في steps («(أ) …»، «(ب) …»). النموذج (ب): المفردة رقم ن فيه من الدرس نفسه والنوع نفسه والهدف والصعوبة والدرجة نفسها للمفردة ن في (أ)، بأعداد وسياق مختلفين.",
      `أعد JSON فقط بالشكل: {"title":"…","forms":{"أ":[مفردة…],"ب":[مفردة…]}} والمفردة: ${itemShape} — احذف الحقول غير اللازمة لنوعها.`,
    ].filter(Boolean).join("\n\n");
    const userText = [
      `الصف: ${grade} | ${semester} | ${tool.name} ${number === 1 ? "الأول" : "الثاني"}`,
      "الدروس (استعمل الرمز في حقل lesson):",
      ...lessonsOut.map((l) => `- ${l.code} ${l.title} (${l.unit}) — صفحات الكتاب ${l.pages}`),
      String(b.note || "").trim() ? `ملاحظة المعلّم: ${String(b.note).slice(0, 500)}` : "",
    ].filter(Boolean).join("\n");
    const content: Any[] = [{ type: "text", text: userText }];
    sel.forEach((r, i) => {
      const l = lessonsOut[i], t = texts[i];
      if (t.bx) content.push({ type: "text", text: `══ الدرس ${l.code} ${l.title} — مستخلص كتاب الطالب (ص ${l.pages}):\n${JSON.stringify(t.bx.exam).slice(0, 14000)}` });
      if (t.gx) content.push({ type: "text", text: `══ الدرس ${l.code} — مستخلص دليل المعلم:\n${JSON.stringify(t.gx).slice(0, 8000)}` });
    });
    for (const im of images) { content.push({ type: "text", text: im.tag }); content.push({ type: "image_url", image_url: { url: im.url } }); }

    const call = async (messages: Any[]) => {
      const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta exam-khotta" },
        body: JSON.stringify({ model, messages, temperature: 0.3, max_tokens: 9000, response_format: { type: "json_object" } }),
      }, { st, task: "exam" });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(orErrCode(r.status, String(j?.error?.message || "")) || "ai_error");
      await logAiCost(admin, user.id, "exam-khotta", "text", model, j?.usage);
      return String(j?.choices?.[0]?.message?.content || "");
    };
    const messages: Any[] = [{ role: "system", content: system }, { role: "user", content }];
    let ex: Any = null, errs: string[] = [], raw = "";
    for (let attempt = 0; attempt < 2; attempt++) {
      if (attempt > 0 && Date.now() - T0 > 85_000) break; // لا وقت لإعادةٍ ضمن حدّ الدالة (~١٥٠ث): نسلّم مع الملاحظات
      try { raw = await call(messages); } catch (e) {
        if (attempt < 1) continue;
        await refundQuota(admin, user.id, user.email || "", "text");
        return json({ error: "ai_error", message: "تعذّر الاتصال بنموذج الذكاء الاصطناعي: " + String((e as Error).message) }, 502);
      }
      const p = parseAiJson(raw);
      ex = p.ok ? p.value : null;
      errs = ex ? validate(ex, kind, grade, codes, gridRows) : ["الردّ ليس JSON صالحاً بالشكل المطلوب."];
      if (!errs.length) break;
      messages.push({ role: "assistant", content: raw.slice(0, 12000) });
      messages.push({ role: "user", content: "الفحص الآلي بمواصفات الوثيقة وجد هذه المخالفات؛ صحّحها كلها وأعد JSON كاملاً بالشكل نفسه:\n- " + errs.join("\n- ") });
    }
    if (!ex) { await refundQuota(admin, user.id, user.email || "", "text"); return json({ error: "bad_output", message: "لم يُرجع النموذج اختباراً صالحاً." }, 502); }

    const out = {
      kind, spec: SPEC_MATH.id, subject: "math", grade, semester, number,
      title: String(ex.title || `${tool.name} ${number === 1 ? "الأول" : "الثاني"}`),
      grid: gridName || null, lessons: lessonsOut, forms: { "أ": ex.forms["أ"], "ب": ex.forms["ب"] },
      tool: { name: tool.name, total: tool.total, duration: tool.duration_short || tool.duration_text, rules: tool.rules, answer_key_columns: tool.answer_key_columns || null, ao: tool.ao, level: tool.level },
      calculator: kind === "short_test" ? !!tool.calculator[band(grade, tool.calculator)] : false,
      document: SPEC_MATH.document, model, pages_used: images.length, text_lessons: textLessons,
      check: { ok: !errs.length, errors: errs },
    };
    return json(out);
  } catch (e) {
    console.error("exam-khotta", e);
    return json({ error: "server", message: "خطأ في الخادم." }, 500);
  }
});
