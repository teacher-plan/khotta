// v2026.11.06 ════════════════════════════════════════════════════════════════
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

// ملخّصٌ مضغوط لبيانات المدرسة يقرؤه النموذج: لكل شعبةٍ غيابُ كل يومٍ وحصّة،
// ولكل طالبٍ عددُ أيام غيابه ومخالفاته بأنواعها ونجومه — آخر ٩٠ يوماً.
function schoolDigest(school: Any, teachers: Any[]): string {
  const since = new Date(Date.now() - 90 * 864e5).toISOString().slice(0, 10);
  const today = new Date(Date.now() + 4 * 3600e3).toISOString().slice(0, 10); // توقيت مسقط
  const lines: string[] = [];
  lines.push(`المدرسة: ${school.name} · تاريخ اليوم: ${today} · البيانات من ${since}`);
  lines.push(`عدد المعلّمين المنضمّين: ${teachers.length}`);
  for (const t of teachers) {
    const d = t.data || {};
    const classes: Any[] = [];
    (d.grades || []).forEach((g: Any) => (g.classes || []).forEach((c: Any) => classes.push({ ...c, grade: g.num })));
    lines.push(`\n## المعلّم: ${d.display_name || t.email || ""} — الشعب: ${classes.map((c) => `${c.name} (${(c.subjects || []).join("، ")}، ${(c.students || []).length} طالباً)`).join(" | ")}`);
    for (const c of classes) {
      const abs = (d.absence || {})[c.id] || {};
      const days = Object.keys(abs).filter((x) => x >= since).sort();
      if (days.length) {
        lines.push(`### غياب ${c.name}:`);
        for (const day of days) {
          const parts = Object.keys(abs[day] || {}).sort().map((p) => {
            const names: string[] = abs[day][p] || [];
            return `${PERIODS[p] || p}: ${names.length ? names.join("، ") : "الكل حاضر"}`;
          });
          lines.push(`- ${day}: ${parts.join(" / ")}`);
        }
      }
      const beh = (d.beh_log || {})[c.id] || [];
      const studs: string[] = c.students || [];
      const rows: string[] = [];
      studs.forEach((nm, i) => {
        const log: Any[] = (beh[i] || []).filter((e: Any) => String(e.date || "").slice(0, 10) >= since);
        const viol = log.filter((e) => e.kind === "viol");
        const stars = log.filter((e) => e.kind === "star").length;
        if (!viol.length && !stars) return;
        const types: Record<string, number> = {};
        viol.forEach((e) => { const k = e.type || e.note || "مخالفة"; types[k] = (types[k] || 0) + 1; });
        rows.push(`${nm}: نجوم ${stars}${viol.length ? ` · مخالفات ${viol.length} (${Object.entries(types).map(([k, v]) => `${k}×${v}`).join("، ")}) آخرها ${String(viol[viol.length - 1].date || "").slice(0, 10)}` : ""}`);
      });
      if (rows.length) { lines.push(`### سلوك ${c.name}:`); rows.forEach((r) => lines.push(`- ${r}`)); }
    }
  }
  let txt = lines.join("\n");
  if (txt.length > 24000) txt = txt.slice(0, 24000) + "\n…(اقتُطع الباقي لطوله)";
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
        const { data: profs } = await admin.from("cycle1_profiles").select("id,email,data").in("id", ids);
        teachers = profs || [];
      }
      const digest = schoolDigest(school, teachers);
      system = [
        `أنت «مساعد الإدارة» في منصّة خُطّة لمدرسة «${school.name}» في سلطنة عُمان. تخدم فريق إدارة المدرسة (المدير ومساعده والأخصائي الاجتماعي).`,
        "تُجيب فقط من البيانات المرفقة أدناه (غياب الطلاب بالحصص، وسجلّ السلوك والنجوم) التي سجّلها المعلّمون. إن لم تكفِ البيانات للإجابة فقل ذلك صراحةً واذكر ما ينقص، ولا تخمّن ولا تخترع أرقاماً أو أسماء.",
        "الغياب: «الطابور» ثم الحصص ١–٨. الطالب الذي حضر الطابور ثم غاب عن حصصٍ لاحقة في اليوم نفسه حالةُ «تسرّبٍ من الحصص» تستحق التنبيه.",
        "أجب بالعربية الفصحى الميسّرة، مختصراً ومنظّماً: الأرقام أولاً، ثم الأسماء عند الحاجة في قائمة أو جدول Markdown صغير، ثم توصيةٌ عمليةٌ واحدة أو اثنتان (تواصلٌ مع وليّ الأمر، إحالةٌ للأخصائي، متابعةٌ مع معلّم).",
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
        max_tokens: mode === "exam" ? 1400 : 1200,
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
