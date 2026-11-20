// v2026.11.09 ════════════════════════════════════════════════════════════════
// Edge Function: c1-insights
// ذكاءٌ اصطناعيّ لمنصّة الحلقة الأولى (cycle1) في وضعين:
//   • mode='exam'    — المعلّم: خطةٌ علاجية من ملخّص تحليل اختبار (أرقامٌ فقط،
//                      بلا أسماء طلاب: لا يغادر اسمُ طالبٍ المنصّة في هذا الوضع).
//   • mode='copilot' — حساب إدارة المدرسة: يُجيب عن سؤالٍ من بيانات غياب
//                      معلّمي مدرسته وسلوك طلابهم. البيانات يجمعها الخادم بنفسه
//                      من المدرسة التي يديرها صاحب الجلسة — لا يُوثَق بما يرسله المتصفح.
// الحصّة: نفس الحصّة الموحّدة (takeQuota) لكل مستخدم، وتُسجَّل الكلفة.
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { orFetch, orErrCode } from "../_shared/ai.ts";
import { takeQuota, logAiCost } from "../_shared/quota.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
}

const PERIODS: Record<string, string> = { q: "الطابور", "1": "الحصة ١", "2": "الحصة ٢", "3": "الحصة ٣", "4": "الحصة ٤", "5": "الحصة ٥", "6": "الحصة ٦", "7": "الحصة ٧", "8": "الحصة ٨" };

// deno-lint-ignore no-explicit-any
type Any = any;

// ملخّصٌ مضغوط لبيانات المدرسة يقرؤه النموذج (٢١ نوفمبر: مؤشّراتٌ محسوبةٌ مسبقاً أولاً —
// النموذج يخطئ في العدّ من البيانات الخام، فنعطيه الأرقام جاهزة — ثم البيانات الخام للتفاصيل).
// opts.days: الفترة (٧ / ٣٠ / ٩٠ يوماً)، opts.cls: شعبةٌ واحدة (اسمها) أو الكل.
const WD = ["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"];
function schoolDigest(school: Any, teachers: Any[], opts: { days: number; cls: string } = { days: 90, cls: "" }): string {
  const days = [7, 30, 90].includes(opts.days) ? opts.days : 90;
  const since = new Date(Date.now() - days * 864e5).toISOString().slice(0, 10);
  const today = new Date(Date.now() + 4 * 3600e3).toISOString().slice(0, 10); // توقيت مسقط
  const only = String(opts.cls || "").trim();
  const lines: string[] = [];
  lines.push(`المدرسة: ${school.name} · تاريخ اليوم: ${today} (${WD[new Date(today + "T12:00:00").getDay()]}) · الفترة: آخر ${days} يوماً (من ${since})${only ? ` · الشعبة: ${only} فقط` : " · كل الشعب"}`);
  lines.push(`عدد المعلّمين المنضمّين: ${teachers.length}`);

  // ── المؤشّرات المحسوبة ──
  const clsRows: string[] = [], wd: Record<number, number> = {}, truP: Record<string, number> = {};
  const stuAbs: Array<{ k: string; n: number; streak: number }> = [], stuLate: Array<{ k: string; n: number }> = [];
  const tRows: string[] = [];
  let totStu = 0, totAbs = 0, totRec = 0;
  for (const t of teachers) {
    const d = t.data || {}, tname = d.display_name || t.email || "";
    // عمل المعلّم في الفترة
    const ps = d.plan_state || {};
    let prep = 0, game = 0, info = 0, noor = 0, done = 0;
    for (const v of Object.values(ps) as Any[]) {
      if (!v || typeof v !== "object") continue;
      if (String(v.prep_at || "").slice(0, 10) >= since) prep++;
      if (String(v.game_at || "").slice(0, 10) >= since) game++;
      if (String(v.info_at || "").slice(0, 10) >= since) info++;
      if (v.noor && String((v.noor && v.noor.at) || v.prep_at || "").slice(0, 10) >= since) noor++;
      if (v.done) done++;
    }
    const recDays = new Set<string>();
    (d.grades || []).forEach((g: Any) => (g.classes || []).forEach((c: Any) => {
      if (only && c.name !== only) return;
      const studs: string[] = (c.students || []).filter(Boolean);
      const abs = (d.absence || {})[c.id] || {}, late = (d.absence_late || {})[c.id] || {};
      const dd = Object.keys(abs).filter((x) => x >= since && x <= today);
      let absDays = 0;
      const per: Record<string, string[]> = {};
      for (const day of dd) {
        recDays.add(day);
        const D = abs[day] || {};
        const q: string[] | null = Array.isArray(D.q) ? D.q : null;
        const any = new Set<string>();
        Object.keys(D).forEach((p) => (D[p] || []).forEach((n: string) => any.add(n)));
        const dayAbs = q ? new Set(q) : any;
        absDays += dayAbs.size;
        const w = new Date(day + "T12:00:00").getDay();
        wd[w] = (wd[w] || 0) + dayAbs.size;
        dayAbs.forEach((n) => { (per[n] = per[n] || []).push(day); });
        if (q) Object.keys(D).filter((p) => p !== "q").forEach((p) => (D[p] || []).forEach((n: string) => { if (!q.includes(n)) truP[p] = (truP[p] || 0) + 1; }));
      }
      const lateCount: Record<string, number> = {};
      Object.keys(late).filter((x) => x >= since).forEach((day) => { const seen = new Set<string>(); Object.values(late[day] || {}).forEach((arr: Any) => (arr || []).forEach((n: string) => seen.add(n))); seen.forEach((n) => { lateCount[n] = (lateCount[n] || 0) + 1; }); });
      Object.entries(per).forEach(([n, ds]) => {
        ds.sort(); let best = 1, cur = 1;
        for (let k = 1; k < ds.length; k++) { const gap = (new Date(ds[k]).getTime() - new Date(ds[k - 1]).getTime()) / 864e5; cur = gap <= 3 ? cur + 1 : 1; best = Math.max(best, cur); } // ≤٣ أيام: يتخطّى نهاية الأسبوع
        stuAbs.push({ k: `${n} (${c.name})`, n: ds.length, streak: best });
      });
      Object.entries(lateCount).forEach(([n, k]) => stuLate.push({ k: `${n} (${c.name})`, n: k }));
      const beh = (d.beh_log || {})[c.id] || [];
      let viol = 0, stars = 0;
      studs.forEach((_, i) => (beh[i] || []).forEach((e: Any) => { if (String(e.date || "").slice(0, 10) < since) return; if (e.kind === "viol") viol++; else if (e.kind === "star") stars++; }));
      const rate = dd.length && studs.length ? Math.round((absDays / (dd.length * studs.length)) * 1000) / 10 : 0;
      totStu += studs.length; totAbs += absDays; totRec += dd.length * studs.length;
      clsRows.push(`- ${c.name} (${tname}): ${studs.length} طالباً · أيام مسجّلة ${dd.length} · غياب ${absDays} يوم-طالب (${rate}٪) · تأخّر ${Object.values(lateCount).reduce((a, b) => a + b, 0)} · مخالفات ${viol} · نجوم ${stars}`);
    }));
    tRows.push(`- ${tname}: حضّر ${prep} درساً · ألعاب ${game} · إنفوجرافيك ${info} · نشر في نور ${noor} · دروس منجزة (إجمالي) ${done} · أيام سجّل فيها الغياب ${recDays.size} · آخر نشاط ${String(t.updated_at || "").slice(0, 10) || "—"}`);
  }
  lines.push(`\n## مؤشّرات محسوبة للفترة (اعتمدها في الأرقام)`);
  lines.push(`- نسبة الغياب العامة: ${totRec ? Math.round((totAbs / totRec) * 1000) / 10 : 0}٪ (${totAbs} يوم-طالب من ${totRec}) · عدد الطلاب ${totStu}`);
  if (Object.keys(wd).length) lines.push(`- الغياب حسب اليوم: ${[0, 1, 2, 3, 4].map((w) => `${WD[w]} ${wd[w] || 0}`).join(" · ")}`);
  if (Object.keys(truP).length) lines.push(`- التسرّب من الحصص (حضر الطابور وغاب عن الحصة): ${Object.entries(truP).sort((a, b) => b[1] - a[1]).map(([p, n]) => `${PERIODS[p] || p}: ${n}`).join(" · ")}`);
  const topA = stuAbs.sort((a, b) => b.n - a.n).slice(0, 12);
  if (topA.length) lines.push(`- أكثر الطلاب غياباً (أيام): ${topA.map((x) => `${x.k} ${x.n}${x.streak >= 3 ? ` (متتالٍ ${x.streak})` : ""}`).join(" · ")}`);
  const streaks = stuAbs.filter((x) => x.streak >= 3).sort((a, b) => b.streak - a.streak).slice(0, 12);
  if (streaks.length) lines.push(`- غيابٌ متتالٍ ٣ أيام دراسية فأكثر: ${streaks.map((x) => `${x.k} ${x.streak}`).join(" · ")}`);
  const topL = stuLate.filter((x) => x.n >= 3).sort((a, b) => b.n - a.n).slice(0, 12);
  if (topL.length) lines.push(`- تأخّرٌ متكرّر (٣ أيام فأكثر): ${topL.map((x) => `${x.k} ${x.n}`).join(" · ")}`);
  lines.push(`\n## الشعب`); clsRows.forEach((r) => lines.push(r));
  lines.push(`\n## عمل المعلّمين في الفترة (للمتابعة والدعم لا للمقارنة واللوم)`); tRows.forEach((r) => lines.push(r));

  // ── البيانات الخام (للتفاصيل والأسماء) ──
  lines.push(`\n## البيانات التفصيلية`);
  for (const t of teachers) {
    const d = t.data || {};
    const classes: Any[] = [];
    (d.grades || []).forEach((g: Any) => (g.classes || []).forEach((c: Any) => { if (!only || c.name === only) classes.push({ ...c, grade: g.num }); }));
    if (!classes.length) continue;
    lines.push(`\n### المعلّم: ${d.display_name || t.email || ""} — الشعب: ${classes.map((c) => `${c.name} (${(c.subjects || []).join("، ")}، ${(c.students || []).length} طالباً)`).join(" | ")}`);
    for (const c of classes) {
      const abs = (d.absence || {})[c.id] || {};
      const ds = Object.keys(abs).filter((x) => x >= since).sort();
      if (ds.length) {
        lines.push(`#### غياب ${c.name}:`);
        for (const day of ds) {
          const parts = Object.keys(abs[day] || {}).sort().map((p) => {
            const names: string[] = abs[day][p] || [];
            return `${PERIODS[p] || p}: ${names.length ? names.join("، ") : "الكل حاضر"}`;
          });
          lines.push(`- ${day}: ${parts.join(" / ")}`);
        }
      }
      const late = (d.absence_late || {})[c.id] || {};
      const ldays = Object.keys(late).filter((x) => x >= since).sort();
      if (ldays.length) {
        lines.push(`#### تأخّر ${c.name}:`);
        for (const day of ldays) lines.push(`- ${day}: ${Object.keys(late[day] || {}).sort().map((p) => `${PERIODS[p] || p}: ${(late[day][p] || []).join("، ")}`).join(" / ")}`);
      }
      const beh = (d.beh_log || {})[c.id] || [];
      const rows: string[] = [];
      (c.students || []).forEach((nm: string, i: number) => {
        const log: Any[] = (beh[i] || []).filter((e: Any) => String(e.date || "").slice(0, 10) >= since);
        const viol = log.filter((e) => e.kind === "viol"), stars = log.filter((e) => e.kind === "star").length;
        if (!viol.length && !stars) return;
        const types: Record<string, number> = {};
        viol.forEach((e) => { const k = e.type || e.note || "مخالفة"; types[k] = (types[k] || 0) + 1; });
        rows.push(`${nm}: نجوم ${stars}${viol.length ? ` · مخالفات ${viol.length} (${Object.entries(types).map(([k, v]) => `${k}×${v}`).join("، ")}) آخرها ${String(viol[viol.length - 1].date || "").slice(0, 10)}` : ""}`);
      });
      if (rows.length) { lines.push(`#### سلوك ${c.name}:`); rows.forEach((r) => lines.push(`- ${r}`)); }
    }
  }
  // ملخّص الظواهر: كل نوع مخالفةٍ بعدد حالاته، وكم معلّماً وشعبةً وطالباً سجّله
  const agg: Record<string, { n: number; t: Set<string>; c: Set<string>; s: Set<string> }> = {};
  for (const t of teachers) {
    const d = t.data || {};
    (d.grades || []).forEach((g: Any) => (g.classes || []).forEach((c: Any) => {
      if (only && c.name !== only) return;
      const beh = (d.beh_log || {})[c.id] || [];
      (c.students || []).forEach((nm: string, i: number) => (beh[i] || []).forEach((e: Any) => {
        if (e.kind !== "viol" || String(e.date || "").slice(0, 10) < since) return;
        const k = e.type || e.note || "مخالفة";
        const x = agg[k] = agg[k] || { n: 0, t: new Set(), c: new Set(), s: new Set() };
        x.n++; x.t.add(d.display_name || t.email || ""); x.c.add(c.name); x.s.add(c.name + "/" + nm);
      }));
    }));
  }
  const aggRows = Object.entries(agg).sort((a, b) => b[1].n - a[1].n)
    .map(([k, x]) => `- ${k}: ${x.n} حالة · ${x.t.size} معلّم · ${x.c.size} شعبة (${[...x.c].join("، ")}) · ${x.s.size} طالب`);
  const at = lines.findIndex((l) => l.startsWith("\n## الشعب"));
  if (aggRows.length) lines.splice(at, 0, "\n## ملخّص المخالفات حسب النوع", ...aggRows);
  let txt = lines.join("\n");
  if (txt.length > 30000) txt = txt.slice(0, 30000) + "\n…(اقتُطع الباقي لطوله — المؤشّرات المحسوبة أعلاه كاملة)";
  return txt;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) return json({ error: "unauthorized" }, 401);
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const { data: { user }, error: userErr } = await admin.auth.getUser(authHeader.replace("Bearer ", ""));
    if (userErr || !user) return json({ error: "unauthorized" }, 401);

    const apiKey = Deno.env.get("OPENROUTER_API_KEY");
    if (!apiKey) return json({ error: "server_not_configured" }, 500);
    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
    if (st.generator_enabled === "0") return json({ error: "disabled" }, 403);

    const b = await req.json().catch(() => ({}));
    const mode = b.mode === "copilot" ? "copilot" : "exam";
    const male = b.gender === "m";
    let system = "", userMsg = "", history: Array<{ role: string; content: string }> = [];

    if (mode === "exam") {
      const summary = b.summary && typeof b.summary === "object" ? b.summary : null;
      if (!summary) return json({ error: "no_summary" }, 400);
      const sumTxt = JSON.stringify(summary).slice(0, 6000);
      system = [
        "أنت خبيرٌ في التقويم التربوي وتحليل نتائج الاختبارات في مدارس سلطنة عُمان.",
        `تكتب ${male ? "لمعلّم" : "لمعلّمة"}، فخاطبه بصيغة ${male ? "المذكّر" : "المؤنّث"}، بالعربية الفصحى الميسّرة.`,
        "أمامك ملخّصٌ رقميّ لتحليل اختبار: نسبة إتقان كل سؤال ومعامل تمييزه والدرس الذي يقيسه، وإتقان كل درس، وتوزيع المستويات (أ ٩٠+، ب ٨٠–٨٩، ج ٦٥–٧٩، د ٥٠–٦٤، هـ أقل من ٥٠).",
        "اكتب خطةً علاجية عملية قصيرة بعناوين Markdown (##) وقوائم نقطية، بهذه الأقسام بالترتيب:",
        "## قراءة سريعة للنتائج (٣–٤ نقاط: أبرز ما تكشفه الأرقام)",
        "## ما يحتاج إعادة تدريس (الدروس/الأسئلة ذات الإتقان المنخفض، ولكلٍّ فكرةُ إعادة تدريسٍ مختلفة عن الشرح الأول)",
        "## أسئلةٌ تُراجَع صياغتها (ضعيفة التمييز أو شديدة الصعوبة/السهولة، ولماذا)",
        "## خطة المجموعات (العلاج، والدعم، والإثراء: نشاطٌ قصير محدّد لكلّ منها مدّته ١٠–١٥ دقيقة)",
        "## متابعة (كيف يتحقّق من التحسّن: سؤال خروج، أو اختبار قصير بعد أسبوع)",
        "لا تخترع أرقاماً غير الموجودة، ولا أسماء طلاب. كن محدّداً ومختصراً (٢٥٠–٤٠٠ كلمة).",
      ].join("\n");
      userMsg = "ملخّص تحليل الاختبار:\n" + sumTxt;
    } else {
      // من يدير مدرسةً؟ البريد في حساب الإدارة المشترك
      const email = (user.email || "").toLowerCase();
      const { data: school } = await admin.from("c1_schools").select("id,name").eq("admin_email", email).maybeSingle();
      if (!school) return json({ error: "forbidden" }, 403);
      const question = String(b.question || "").trim().slice(0, 1500);
      if (!question) return json({ error: "no_message" }, 400);
      const { data: mem } = await admin.from("c1_school_members").select("teacher_id").eq("school_id", school.id);
      const ids = (mem || []).map((m: { teacher_id: string }) => m.teacher_id);
      let teachers: Any[] = [];
      if (ids.length) {
        const { data: profs } = await admin.from("cycle1_profiles").select("id,email,data,updated_at").in("id", ids);
        teachers = profs || [];
      }
      const digest = schoolDigest(school, teachers, { days: Number(b.days) || 30, cls: String(b.cls || "").slice(0, 60) });
      system = [
        `أنت «مساعد الإدارة» في منصّة خُطّة لمدرسة «${school.name}» في سلطنة عُمان. تخدم فريق إدارة المدرسة (المدير ومساعده والأخصائي الاجتماعي).`,
        "تُجيب فقط من البيانات المرفقة أدناه (غياب الطلاب بالحصص، وسجلّ السلوك والنجوم) التي سجّلها المعلّمون. إن لم تكفِ البيانات للإجابة فقل ذلك صراحةً واذكر ما ينقص، ولا تخمّن ولا تخترع أرقاماً أو أسماء.",
        "التأخّر يُسجَّل منفصلاً عن الغياب (أقسام «تأخّر الشعبة»): المتأخّر حاضرٌ لا يُحسب غائباً، والتأخّر المتكرّر (٣ أيام فأكثر في الشهر) يستحق التنبيه والتواصل مع وليّ الأمر.",
        "الغياب: «الطابور» ثم الحصص ١–٨. الطالب الذي حضر الطابور ثم غاب عن حصصٍ لاحقة في اليوم نفسه حالةُ «تسرّبٍ من الحصص» تستحق التنبيه.",
        "أجب بالعربية الفصحى الميسّرة، مختصراً ومنظّماً: الأرقام أولاً، ثم الأسماء عند الحاجة في قائمة أو جدول Markdown صغير، ثم توصيةٌ عمليةٌ واحدة أو اثنتان (تواصلٌ مع وليّ الأمر، إحالةٌ للأخصائي، متابعةٌ مع معلّم).",
        "عند السؤال عن الظواهر أو المشكلات: الظاهرة المدرسية هي ما يسجّله معلّمون كثيرون في شعبٍ كثيرة (استعن بملخّص المخالفات حسب النوع)، وفرّق بينها وبين ما يتركّز في شعبةٍ واحدة أو في طالبين. رتّبها بالانتشار، واذكر هل هي في ازدياد، ثم اقترح حلولاً عملية بثلاثة مستويات: وقائية للمدرسة، ومتابعة للشعب الأكثر، وفردية للطلاب المتكرّرين، مع من يتولّى الإجراء (الإدارة، المعلّمون، الأخصائي الاجتماعي، وليّ الأمر) وكيف يُقاس الأثر.",
        "إن تفاوت المعلّمون كثيراً في عدد ما يسجّلونه فنبّه إلى احتمال اختلاف معايير التسجيل، واقترح توحيدها، دون لومِ معلّمٍ بعينه.",
        "اعتمد في كل رقمٍ قسمَ «مؤشّرات محسوبة» و«الشعب» (محسوبةٌ بدقّة من البيانات) ولا تعدّ بنفسك من البيانات التفصيلية؛ ارجع إليها للأسماء والتواريخ فقط. اذكر الفترة التي تتحدّث عنها.",
        "قسم «عمل المعلّمين» للمتابعة والدعم: اذكر الإنجاز بإيجابية، واقترح دعماً عملياً لمن يحتاجه (تدريب على أداة، توزيع عبء)، ولا ترتّب المعلّمين ولا تلُم أحداً. «أيام سجّل فيها الغياب» القليلة تعني غالباً بياناتٍ ناقصة لا غياباً أقل — نبّه إلى ذلك عند تفسير الأرقام.",
        "عند طلب وثيقة (رسالة لوليّ أمر، محضر اجتماع، تعميم للمعلّمين، تقرير للمديرية، خطة علاجية، شهادة شكر): اكتبها كاملةً جاهزةً للطباعة بلغةٍ رسمية لطيفة، بفراغاتٍ واضحة [هكذا] لما لا تعرفه (التاريخ الهجري، اسم المدير…)، ولا تضع في رسالة وليّ الأمر بيانات طالبٍ آخر.",
        "اختم كل إجابةٍ تحليلية بسطرٍ واحد: «**الإجراء المقترح:** …».",
        "تعامل مع بيانات الطلاب بسرّية واحترام، ولا تُصدر أحكاماً على أشخاص.",
        "\nالبيانات:\n" + digest,
      ].join("\n");
      history = (Array.isArray(b.history) ? b.history : [])
        .filter((m: Any) => (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
        .slice(-6).map((m: Any) => ({ role: m.role, content: String(m.content).slice(0, 2000) }));
      userMsg = question;
    }

    const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
    if (!quota.ok) return quota.error === "quota_unavailable"
      ? json({ error: "quota_unavailable" }, 503)
      : json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);

    const model = st.model_insights || st.model_chat || st.chat_model || st.ai_model || "google/gemini-2.5-flash";
    const orResp = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta C1 Insights" },
      body: JSON.stringify({
        model,
        messages: [{ role: "system", content: system }, ...history, { role: "user", content: userMsg }],
        temperature: 0.4,
        max_tokens: mode === "exam" ? 1400 : 2400,
      }),
    }, { st, task: "chat" });
    const or = await orResp.json();
    if (!orResp.ok) {
      const m = String(or?.error?.message || or?.message || "");
      console.error(`openrouter ${orResp.status} في c1-insights: ${m}`);
      return json({ error: orErrCode(orResp.status, m) }, 502);
    }
    const text = String(or?.choices?.[0]?.message?.content || "").trim();
    if (!text) return json({ error: "bad_output" }, 502);
    await logAiCost(admin, user.id, "c1-insights", "text", model, or?.usage);
    return json({ text, model });
  } catch (e) {
    console.error("server_error:", String(e));
    return json({ error: "server_error" }, 500);
  }
});
