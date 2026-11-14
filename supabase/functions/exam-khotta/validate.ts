// فحص الاختبار بقواعد وثيقة التقويم (منقول من exam_lib.py في مهارة exam-khotta — ما يخصّ الرياضيات).
import { SPEC_MATH } from "./spec.ts";
// deno-lint-ignore no-explicit-any
type Any = any;
export const SUBJECT = "الرياضيات";
export const OTHER = ["short", "fill", "tf", "match", "order", "table", "explain", "creative"];
const AR = "٠١٢٣٤٥٦٧٨٩";
export const ar = (n: number | string) => String(n).replace(/[0-9]/g, (d) => AR[+d]);
export const cat = (t: string) => (t === "mcq" ? "mcq" : t === "long" ? "long" : "other");
export const band = (g: number, map: Record<string, unknown>) => {
  for (const k of Object.keys(map)) { const [a, b] = k.split("-").map(Number); if (g >= a && g <= (b || a)) return k; }
  return "";
};

// ── الفحص: قواعد الوثيقة كما في exam_lib.py (ما يخصّ الرياضيات) ──
export function validate(ex: Any, kind: string, grade: number, lessons: string[], gridRows: Any[] | null): string[] {
  const E: string[] = [];
  const tool = SPEC_MATH.tools[kind];
  const forms = ex?.forms || {};
  const A: Any[] = Array.isArray(forms["أ"]) ? forms["أ"] : [];
  const B: Any[] = Array.isArray(forms["ب"]) ? forms["ب"] : [];
  if (!A.length || !B.length) return ["يجب أن يحتوي الناتج على forms.أ و forms.ب."];
  const checkForm = (name: string, items: Any[]) => {
    const n = items.length;
    if (n < tool.items[0] || n > tool.items[1]) E.push(`النموذج (${name}): عدد المفردات ${n}، والمطلوب ${tool.items[0]}–${tool.items[1]}.`);
    let total = 0;
    const aoSum: Record<string, number> = {}, lvSum: Record<string, number> = {};
    const used = new Set<string>();
    items.forEach((it, i) => {
      const k = `النموذج (${name}) المفردة ${i + 1}`;
      const m = it?.marks;
      if (!Number.isInteger(m) || m < 1) E.push(`${k}: الدرجة يجب أن تكون عدداً صحيحاً موجباً.`);
      total += Number.isInteger(m) ? m : 0;
      for (const f of ["stem", "objective", "page", "lesson"]) if (!String(it?.[f] ?? "").trim()) E.push(`${k}: الحقل ${f} مطلوب.`);
      const partsAnswered = Array.isArray(it?.parts) && it.parts.length && it.parts.every((p: Any) => p && p.answer != null && String(p.answer).trim());
      if (it?.answer == null && !(Array.isArray(it?.steps) && it.steps.length) && !partsAnswered) E.push(`${k}: answer أو steps مطلوب (وللإجابة الطويلة: إجابة كل جزء في steps).`);
      if (!lessons.includes(String(it?.lesson))) E.push(`${k}: الدرس «${it?.lesson}» ليس من الدروس المحدّدة (${lessons.join("، ")}).`);
      else used.add(String(it.lesson));
      if (!["mcq", "long", ...OTHER].includes(it?.type)) E.push(`${k}: النوع «${it?.type}» غير معروف.`);
      // ── الدرجة على قدر العمل (ملاحظة الأستاذ عيسى): الاختيار من متعدد درجة واحدة دائماً،
      // وكل درجةٍ فوق الأولى يقابلها جزءٌ أو خطوةٌ مستقلّة تُصحَّح وحدها ويُذكر توزيعها في الإرشادات.
      const nSteps = Array.isArray(it?.steps) ? it.steps.filter((x: Any) => String(x ?? "").trim()).length : 0;
      const nParts = Array.isArray(it?.parts) ? it.parts.length : 0;
      if (it?.type === "mcq" && m !== 1) E.push(`${k}: الاختيار من متعدد درجته ١ دائماً (وجدتُ ${m}).`);
      if (it?.type === "tf" && m > 2) E.push(`${k}: الصواب والخطأ مع التفسير ١–٢ درجة.`);
      if (Number.isInteger(m) && m >= 2 && it?.type !== "mcq") {
        if (Math.max(nSteps, nParts) < 2) E.push(`${k}: درجتها ${m} فيجب أن تتطلّب ${m} خطوات/أجزاء مستقلّة على الأقل مكتوبة في steps أو parts، وإلا فاجعلها درجة واحدة أو زِد مطلوبها.`);
        if (!/درج/.test(String(it?.guidance || ""))) E.push(`${k}: الإرشادات يجب أن توزّع الدرجات (${m}) على الخطوات: «درجة لـ… ودرجة لـ…».`);
      }
      if (m === 1 && nParts >= 2) E.push(`${k}: مفردة من ${nParts} أجزاء لا تكون بدرجة واحدة؛ لكل جزء درجة.`);
      if (m === 1 && it?.type !== "mcq" && /جميع|كلّ? عوامل|كلّ? مضاعفات|كلّ? القيم|كلّ? الحلول|اذكر ثلاث|اكتب ثلاث|اكتب أربع/.test(String(it?.stem || "")))
        E.push(`${k}: السؤال يطلب عدّة إجابات («${String(it.stem).slice(0, 40)}…») فدرجته ٢ على الأقل مع توزيعها في الإرشادات.`);
      if (m === 1 && it?.type !== "mcq" && nSteps >= 4) E.push(`${k}: حلّه ${nSteps} خطوات فلا يكون بدرجة واحدة؛ اجعله درجتين أو بسّط المطلوب.`);
      if (it?.type === "mcq") {
        if (!Array.isArray(it.choices) || it.choices.length !== 4) E.push(`${k}: الاختيار من متعدد بأربعة بدائل.`);
        if (!Number.isInteger(it.answer) || it.answer < 0 || it.answer > 3) E.push(`${k}: answer رقم البديل الصحيح ٠–٣.`);
      }
      if (it?.type === "tf" && it.explain !== true) E.push(`${k}: الصواب والخطأ مع التفسير دائماً (explain: true).`);
      if (it?.type === "match" && !(Array.isArray(it.right) && Array.isArray(it.left) && it.right.length > it.left.length && it.right.length >= 4))
        E.push(`${k}: المزاوجة: بدائل العمود الثاني أكثر من البنود بواحد على الأقل، و٤ على الأقل.`);
      if (kind === "short_test") {
        if (!SPEC_MATH.ao[it?.ao]) E.push(`${k}: ao يجب أن يكون AO1 أو AO2 أو AO3.`);
        if (!SPEC_MATH.levels[it?.level]) E.push(`${k}: level يجب أن يكون L أو M أو H.`);
        aoSum[it?.ao] = (aoSum[it?.ao] || 0) + (m || 0);
        lvSum[it?.level] = (lvSum[it?.level] || 0) + (m || 0);
      }
    });
    if (total !== tool.total) E.push(`النموذج (${name}): مجموع الدرجات ${total}، والمطلوب ${tool.total}.`);
    if (kind === "quiz") {
      const pat = items.map((x) => x?.marks).sort().join("+");
      if (!["1+2+2", "1+1+3", "2+3"].includes(pat)) E.push(`النموذج (${name}): توزيع درجات السؤال القصير ${pat}؛ المسموح فقط: ١+٢+٢ أو ١+١+٣ (ثلاث مفردات) أو ٢+٣ (مفردتان).`);
      if (items.filter((x) => x?.type === "mcq").length > 1) E.push(`النموذج (${name}): مفردة اختيار من متعدد واحدة على الأكثر في السؤال القصير.`);
    }
    if (kind === "quiz" && (used.size < tool.lessons[0] || used.size > tool.lessons[1])) E.push(`النموذج (${name}): السؤال القصير من درس أو درسين.`);
    if (kind === "short_test") {
      for (const [a, v] of Object.entries(tool.ao as Record<string, number>)) if ((aoSum[a] || 0) !== v) E.push(`النموذج (${name}): درجات ${a} = ${aoSum[a] || 0}، والمطلوب ${v}.`);
      for (const [l, v] of Object.entries(tool.level as Record<string, number>)) if ((lvSum[l] || 0) !== v) E.push(`النموذج (${name}): درجات الصعوبة ${l} = ${lvSum[l] || 0}، والمطلوب ${v}.`);
      const bg = tool.by_grade[band(grade, tool.by_grade)];
      if (bg) {
        const mcq = items.filter((x) => x.type === "mcq"), lng = items.filter((x) => x.type === "long"), oth = items.filter((x) => OTHER.includes(x.type));
        if (mcq.length !== bg.mcq.count || mcq.some((x) => x.marks !== bg.mcq.each)) E.push(`النموذج (${name}): ${bg.mcq.count} مفردتا اختيار من متعدد بدرجة ${bg.mcq.each} لكلٍّ.`);
        if (bg.long) { if (lng.length !== bg.long.count || lng.some((x) => x.marks !== bg.long.marks)) E.push(`النموذج (${name}): مفردة إجابة طويلة واحدة بـ${bg.long.marks} درجات.`); }
        else if (lng.length) E.push(`النموذج (${name}): لا إجابة طويلة في هذا الصف.`);
        const [oa, ob] = bg.other.count, [ea, eb] = bg.other.each;
        if (oth.length < oa || oth.length > ob) E.push(`النموذج (${name}): المفردات الأخرى ${oa}–${ob}.`);
        if (oth.some((x) => x.marks < ea || x.marks > eb)) E.push(`النموذج (${name}): درجة المفردات الأخرى ${ea}–${eb}.`);
        if (oth.reduce((s, x) => s + (x.marks || 0), 0) !== bg.other.marks) E.push(`النموذج (${name}): مجموع درجات المفردات الأخرى ${bg.other.marks}.`);
        const types = new Set(oth.map((x) => x.type));
        if (oth.length >= 3 && types.size < 2) E.push(`النموذج (${name}): نوّع أنواع المفردات الأخرى.`);
      }
      if (gridRows) {
        if (items.length !== gridRows.length) E.push(`النموذج (${name}): الشبكة المختارة ${gridRows.length} مفردات بهذا الترتيب.`);
        else gridRows.forEach((r, i) => {
          const it = items[i];
          if (cat(it.type) !== r[0] || it.ao !== r[1] || it.level !== r[2] || it.marks !== r[3])
            E.push(`النموذج (${name}) المفردة ${i + 1}: الشبكة تطلب (${r[0]}، ${r[1]}، ${r[2]}، ${r[3]} درجة) ووجدتُ (${cat(it.type)}، ${it.ao}، ${it.level}، ${it.marks}).`);
        });
      }
      const minL = tool.lessons[0];
      if (used.size < Math.min(minL, lessons.length)) E.push(`النموذج (${name}): يغطّي ${used.size} دروس فقط؛ وزّع المفردات على الدروس المحدّدة.`);
    }
  };
  checkForm("أ", A); checkForm("ب", B);
  if (A.length === B.length) A.forEach((a, i) => {
    const b = B[i];
    if (cat(a.type) !== cat(b?.type) || a.marks !== b?.marks || a.lesson !== b?.lesson || (kind === "short_test" && (a.ao !== b?.ao || a.level !== b?.level)))
      E.push(`المفردة ${i + 1}: النموذج (ب) يجب أن يطابق (أ) في النوع والدرجة والدرس${kind === "short_test" ? " والهدف والصعوبة" : ""}.`);
    if (a.type === "mcq" && b?.type === "mcq" && JSON.stringify(a.choices?.[a.answer]) === JSON.stringify(b.choices?.[b.answer]))
      E.push(`المفردة ${i + 1}: الإجابة الصحيحة نفسها في النموذجين؛ غيّر الأعداد في (ب).`);
  });
  else E.push("عدد مفردات النموذجين يجب أن يتساوى.");
  return E;
}

