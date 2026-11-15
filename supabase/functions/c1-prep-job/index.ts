// v2026.11.15 ════════════════════════════════════════════════════════════════
// Edge Function: c1-prep-job — إعداد تحضير الدرس في الخلفية
//
// المعلّم يضغط «التحضير» ثم يخرج من خُطّة إن شاء: العمل يجري على الخادم، والنتيجة
// تُحفظ في c1_prep_jobs، ويصله إشعارٌ على هاتفه (c1_notifications kind='prep' ←
// مشغّل c1_notif_push ← c1-push) وفي جرس المنصّة. المتصفح يدمج الخطة الجاهزة في
// plan_state متى فُتح (لا يكتب الخادم في الملف الشخصي فلا يتسابق مع حفظ المتصفح).
//
// المراحل (كلٌّ في استدعاءٍ مستقل كي لا يتجاوز مجموعها حدّ ١٥٠ ثانية للخطة المجانية):
//   start   (جلسة المعلّم) → يُنشئ المهمة ويردّ فوراً، ثم في الخلفية:
//             ملخّص صفحات الكتاب (إن لم يُرسل) ← يستدعي نفسه بمرحلة plan
//   plan    (مفتاح الخدمة فقط) → generate-lesson-plan ← حفظ النتيجة والإشعار
// الدالّتان المستدعاتان تُناديان برمز جلسة المعلّم نفسه، فتُحسب الحصّة الشهرية كالمعتاد.
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { isServiceRoleRequest } from "../_shared/adminGuard.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
}
// deno-lint-ignore no-explicit-any
type Any = any;

const URL_BASE = Deno.env.get("SUPABASE_URL")!;
const SVC = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const ANON = Deno.env.get("SUPABASE_ANON_KEY") || "";

function bg(p: Promise<unknown>) {
  const rt = (globalThis as Any).EdgeRuntime;
  if (rt && typeof rt.waitUntil === "function") rt.waitUntil(p);
  else p.catch(() => {});
}

async function callFn(name: string, jwt: string, body: Any) {
  const r = await fetch(`${URL_BASE}/functions/v1/${name}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: "Bearer " + jwt, ...(ANON ? { apikey: ANON } : {}) },
    body: JSON.stringify(body),
  });
  const j = await r.json().catch(() => ({}));
  return { ok: r.ok, status: r.status, j };
}

const ERR: Record<string, string> = {
  quota_exceeded: "نفد رصيد التوليد لهذا الشهر",
  quota_unavailable: "الخدمة مشغولة مؤقتاً",
  disabled: "التوليد متوقّف مؤقتاً من الإدارة",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const admin = createClient(URL_BASE, SVC);
  const b: Any = await req.json().catch(() => ({}));
  const action = String(b.action || "");

  const finish = async (jobId: string, userId: string, name: string, ok: boolean, patch: Any) => {
    await admin.from("c1_prep_jobs").update({ ...patch, status: ok ? "done" : "error", finished_at: new Date().toISOString() }).eq("id", jobId);
    await admin.from("c1_notifications").insert({
      user_id: userId, kind: "prep",
      message: ok ? `✅ جهز تحضير درس «${name}» — اضغط لعرضه في الخطة` : `⚠️ تعذّر إعداد تحضير درس «${name}»${patch.error ? " — " + patch.error : ""}`,
    });
  };

  // ── المرحلة الثانية: الخطة نفسها (مفتاح الخدمة فقط — يستدعيها هذا الملف) ──
  if (action === "plan") {
    if (!isServiceRoleRequest(req)) return json({ error: "unauthorized" }, 401);
    const { job_id, jwt, payload } = b;
    const { data: job } = await admin.from("c1_prep_jobs").select("*").eq("id", String(job_id || "")).maybeSingle();
    if (!job || job.status !== "running") return json({ ok: true, skipped: true });
    bg((async () => {
      try {
        const r = await callFn("generate-lesson-plan", String(jwt || ""), payload || {});
        if (r.ok && r.j && r.j.plan) await finish(job.id, job.user_id, job.lesson_name, true, { plan: r.j.plan });
        else await finish(job.id, job.user_id, job.lesson_name, false, { error: ERR[r.j?.error] || "حدث خطأ أثناء الإعداد" });
      } catch (e) {
        console.error("c1-prep-job plan", String(e));
        await finish(job.id, job.user_id, job.lesson_name, false, { error: "حدث خطأ أثناء الإعداد" });
      }
    })());
    return json({ ok: true, accepted: true });
  }

  // ── المرحلة الأولى: من المتصفح ──
  if (action !== "start") return json({ error: "bad_action" }, 400);
  const jwt = (req.headers.get("Authorization") || "").replace("Bearer ", "");
  const { data: { user }, error: uErr } = await admin.auth.getUser(jwt);
  if (uErr || !user) return json({ error: "unauthorized" }, 401);

  const lessonId = String(b.lessonId || "").slice(0, 80);
  const lessonName = String(b.lesson || "").slice(0, 200);
  if (!lessonId || !lessonName) return json({ error: "bad_input" }, 400);

  // مهمة جارية للدرس نفسه؟ لا نبدأ ثانية (ضغطتان متتاليتان، أو جهازان)
  const since = new Date(Date.now() - 12 * 60e3).toISOString();
  const { data: running } = await admin.from("c1_prep_jobs").select("id").eq("user_id", user.id).eq("lesson_id", lessonId)
    .eq("status", "running").gte("created_at", since).limit(1);
  if (running && running.length) return json({ ok: true, job_id: running[0].id, already: true });

  const meta = { grade: String(b.grade || ""), subject: String(b.subject || ""), unit: String(b.unit || "") };
  const { data: job, error: jErr } = await admin.from("c1_prep_jobs")
    .insert({ user_id: user.id, lesson_id: lessonId, lesson_name: lessonName, meta }).select("id").single();
  if (jErr || !job) { console.error("c1-prep-job insert", jErr?.message); return json({ error: "server" }, 500); }

  const payload: Any = {
    grade: meta.grade, subject: meta.subject, unit: meta.unit, lesson: lessonName, images: [],
    bookContext: String(b.bookContext || "").slice(0, 4000), semester: String(b.semester || "الفصل الأول"),
  };
  const images: string[] = Array.isArray(b.images) ? b.images.filter((u: Any) => typeof u === "string" && /^https:\/\//.test(u)).slice(0, 20) : [];

  bg((async () => {
    try {
      // ملخّص صفحات الكتاب أولاً إن لم يكن محفوظاً عند المتصفح (يُحفظ مع المهمة ليُخزَّن هناك)
      if (!payload.bookContext && images.length) {
        const s = await callFn("summarize-lesson-pages", jwt, { grade: meta.grade, subject: meta.subject, unit: meta.unit, lesson: lessonName, images });
        if (s.ok && s.j && s.j.summary) {
          payload.bookContext = String(s.j.summary).slice(0, 4000);
          await admin.from("c1_prep_jobs").update({ summary: s.j.summary }).eq("id", job.id);
        }
      }
      // المرحلة الثانية في استدعاءٍ مستقلّ (مهلته كاملة)
      const r = await fetch(`${URL_BASE}/functions/v1/c1-prep-job`, {
        method: "POST", headers: { "Content-Type": "application/json", Authorization: "Bearer " + SVC },
        body: JSON.stringify({ action: "plan", job_id: job.id, jwt, payload }),
      });
      if (!r.ok) throw new Error("chain " + r.status);
    } catch (e) {
      console.error("c1-prep-job start", String(e));
      await finish(job.id, user.id, lessonName, false, { error: "حدث خطأ أثناء الإعداد" });
    }
  })());

  return json({ ok: true, job_id: job.id });
});
