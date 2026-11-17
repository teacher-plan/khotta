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

// ميزانية خطوة الخطة: أقصر من حدّ ١٥٠ث للدالّة المنتظِرة (انظر generate-lesson-plan)
const PLAN_BUDGET = 110_000;
// زرّ «حضّر الوحدة» تجريبيٌّ لحسابٍ واحد (طلب الأستاذ عيسى ١٨ نوفمبر)
const UNIT_USERS = ["xx@y.com"];

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
    if (job.batch_id) { bg(batchPlan(job, String(jwt || ""), payload || job.payload || {})); return json({ ok: true, accepted: true }); }
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

  // ══ طابور الوحدة ══════════════════════════════════════════════
  // كل درسٍ مهمةٌ queued تحمل payload، و«run» يأخذ أقدمها ويُعدّها في استدعاءٍ
  // مستقل (كي لا يتراكم الوقت في دالّةٍ واحدة)، ونهاية كل درس تستدعي «run» للتالي.
  const selfCall = (body: Any) => fetch(`${URL_BASE}/functions/v1/c1-prep-job`, {
    method: "POST", headers: { "Content-Type": "application/json", Authorization: "Bearer " + SVC }, body: JSON.stringify(body),
  });

  const batchDone = async (batchId: string) => {
    const { data: rest } = await admin.from("c1_prep_jobs").select("status,user_id").eq("batch_id", batchId);
    if (!rest || !rest.length) return;
    const st = rest.map((r: Any) => r.status);
    if (st.some((x: string) => x === "queued" || x === "running")) return;
    const ok = st.filter((x: string) => x === "done").length, bad = st.length - ok;
    // علامةٌ ذرّية تمنع إشعارين إن انتهى استدعاءان معاً (الثاني ينتظر قفل الصفّ ثم لا يطابق)
    const { data: mark } = await admin.from("c1_prep_jobs").update({ payload: { notified: true } })
      .eq("batch_id", batchId).is("payload->notified", null).select("id");
    if (!mark || !mark.length) return;
    await admin.from("c1_notifications").insert({
      user_id: rest[0].user_id, kind: "prep",
      message: bad ? `⚠️ جهز تحضير ${ok} من ${st.length} دروس الوحدة — افتح الخطة واضغط «أعد الناقص»` : `✅ جهز تحضير الوحدة كاملة (${ok} دروس) — اضغط لعرضها في الخطة`,
    });
  };

  // نتيجة درسٍ من الطابور: نجاح، أو إعادة (حتى ٣ محاولات)، أو إيقاف الطابور عند نفاد الرصيد
  async function settle(job: Any, jwt: string, ok: boolean, patch: Any, code = "") {
    if (ok) {
      await admin.from("c1_prep_jobs").update({ ...patch, status: "done", finished_at: new Date().toISOString() }).eq("id", job.id);
    } else if (code === "quota_exceeded" || code === "disabled") {
      await admin.from("c1_prep_jobs").update({ status: "error", error: ERR[code], finished_at: new Date().toISOString() })
        .eq("batch_id", job.batch_id).in("status", ["queued", "running"]);
    } else if ((job.attempts || 0) < 3) {
      await admin.from("c1_prep_jobs").update({ status: "queued", error: patch.error || null }).eq("id", job.id);
    } else {
      await admin.from("c1_prep_jobs").update({ status: "error", error: patch.error || "حدث خطأ أثناء الإعداد", finished_at: new Date().toISOString() }).eq("id", job.id);
    }
    const r = await selfCall({ action: "run", batch_id: job.batch_id, jwt }).catch(() => null);
    if (!r || !r.ok) await batchDone(job.batch_id);
  }

  async function batchPlan(job: Any, jwt: string, payload: Any) {
    try {
      const r = await callFn("generate-lesson-plan", jwt, { ...payload, budget_ms: PLAN_BUDGET });
      if (r.ok && r.j && r.j.plan) await settle(job, jwt, true, { plan: r.j.plan });
      else await settle(job, jwt, false, { error: ERR[r.j?.error] || "حدث خطأ أثناء الإعداد" }, String(r.j?.error || ""));
    } catch (e) {
      console.error("c1-prep-job batchPlan", String(e));
      await settle(job, jwt, false, { error: "حدث خطأ أثناء الإعداد" });
    }
  }

  if (action === "run") {
    if (!isServiceRoleRequest(req)) return json({ error: "unauthorized" }, 401);
    const batchId = String(b.batch_id || ""), jwt = String(b.jwt || "");
    const { data: busy } = await admin.from("c1_prep_jobs").select("id").eq("batch_id", batchId).eq("status", "running").limit(1);
    if (busy && busy.length) return json({ ok: true, busy: true });
    const { data: next } = await admin.from("c1_prep_jobs").select("*").eq("batch_id", batchId).eq("status", "queued")
      .order("created_at").order("lesson_id").limit(1);
    if (!next || !next.length) { await batchDone(batchId); return json({ ok: true, finished: true }); }
    const job = next[0];
    const { data: claimed } = await admin.from("c1_prep_jobs")
      .update({ status: "running", started_at: new Date().toISOString(), attempts: (job.attempts || 0) + 1 })
      .eq("id", job.id).eq("status", "queued").select("*");
    if (!claimed || !claimed.length) return json({ ok: true, raced: true });
    const cj = claimed[0], p: Any = { ...(cj.payload || {}) };
    bg((async () => {
      try {
        if (!p.bookContext && Array.isArray(p.images) && p.images.length && !cj.summary) {
          const s = await callFn("summarize-lesson-pages", jwt, { grade: p.grade, subject: p.subject, unit: p.unit, lesson: p.lesson, images: p.images });
          if (s.ok && s.j && s.j.summary) {
            p.bookContext = String(s.j.summary).slice(0, 4000);
            await admin.from("c1_prep_jobs").update({ summary: s.j.summary }).eq("id", cj.id);
          } else if (s.j?.error === "quota_exceeded") { await settle(cj, jwt, false, {}, "quota_exceeded"); return; }
        } else if (!p.bookContext && cj.summary) p.bookContext = String(cj.summary).slice(0, 4000);
        p.images = [];
        const r = await selfCall({ action: "plan", job_id: cj.id, jwt, payload: p });
        if (!r.ok) throw new Error("chain " + r.status);
      } catch (e) {
        console.error("c1-prep-job run", String(e));
        await settle(cj, jwt, false, { error: "حدث خطأ أثناء الإعداد" });
      }
    })());
    return json({ ok: true, job_id: cj.id });
  }

  // ── من المتصفح ──
  const jwt0 = (req.headers.get("Authorization") || "").replace("Bearer ", "");
  if (action === "unit" || action === "kick") {
    const { data: { user: u }, error: ue } = await admin.auth.getUser(jwt0);
    if (ue || !u) return json({ error: "unauthorized" }, 401);

    if (action === "kick") {
      // حارسٌ: درسٌ «يُعَدّ» منذ أكثر من ٦ دقائق مات استدعاؤه (حدّ الـ١٥٠ث) — يُعاد أو يُعلَن فشله
      const stale = new Date(Date.now() - 6 * 60e3).toISOString();
      const { data: dead } = await admin.from("c1_prep_jobs").select("*").eq("user_id", u.id).eq("status", "running")
        .lt("started_at", stale);
      const { data: deadSingle } = await admin.from("c1_prep_jobs").select("*").eq("user_id", u.id).eq("status", "running")
        .is("batch_id", null).eq("consumed", false).lt("created_at", stale);
      for (const j of deadSingle || []) await finish(j.id, u.id, j.lesson_name, false, { error: "انقطع الإعداد — أعد المحاولة" });
      const batches = new Set<string>();
      for (const j of dead || []) {
        if (!j.batch_id) continue;
        batches.add(j.batch_id);
        await admin.from("c1_prep_jobs").update((j.attempts || 0) < 3 ? { status: "queued" } : { status: "error", error: "انقطع الإعداد", finished_at: new Date().toISOString() })
          .eq("id", j.id).eq("status", "running");
      }
      // طابورٌ فيه دروسٌ تنتظر ولا شيء يعمل (انقطعت السلسلة) يُستأنف بجلسة المعلّم الحالية
      const { data: waiting } = await admin.from("c1_prep_jobs").select("batch_id").eq("user_id", u.id).eq("status", "queued").not("batch_id", "is", null);
      for (const w of waiting || []) batches.add(w.batch_id);
      for (const bid of batches) await selfCall({ action: "run", batch_id: bid, jwt: jwt0, user_id: u.id }).catch(() => {});
      return json({ ok: true, resumed: batches.size, failed_single: (deadSingle || []).length });
    }

    // action === "unit"
    if (!UNIT_USERS.includes(String(u.email || "").toLowerCase())) return json({ error: "forbidden" }, 403);
    const lessons: Any[] = Array.isArray(b.lessons) ? b.lessons.slice(0, 20) : [];
    const meta0 = { grade: String(b.grade || ""), subject: String(b.subject || ""), unit: String(b.unit || "") };
    const sem = String(b.semester || "الفصل الأول");
    const { data: active } = await admin.from("c1_prep_jobs").select("lesson_id").eq("user_id", u.id).in("status", ["queued", "running"]);
    const skip = new Set((active || []).map((r: Any) => r.lesson_id));
    const batchId = crypto.randomUUID();
    const base = Date.now();
    const rows = lessons.filter((l: Any) => l && l.lessonId && l.lesson && !skip.has(String(l.lessonId))).map((l: Any, i: number) => ({
      user_id: u.id, lesson_id: String(l.lessonId).slice(0, 80), lesson_name: String(l.lesson).slice(0, 200), meta: meta0,
      status: "queued", batch_id: batchId, created_at: new Date(base + i).toISOString(),   // الترتيب = ترتيب الدروس
      payload: { grade: meta0.grade, subject: meta0.subject, unit: meta0.unit, lesson: String(l.lesson).slice(0, 200), semester: sem,
        bookContext: String(l.bookContext || "").slice(0, 4000),
        images: (Array.isArray(l.images) ? l.images : []).filter((x: Any) => typeof x === "string" && /^https:\/\//.test(x)).slice(0, 20) },
    }));
    if (!rows.length) return json({ ok: true, n: 0 });
    const { error: ie } = await admin.from("c1_prep_jobs").insert(rows);
    if (ie) { console.error("c1-prep-job unit insert", ie.message); return json({ error: "server" }, 500); }
    const r = await selfCall({ action: "run", batch_id: batchId, jwt: jwt0, user_id: u.id }).catch(() => null);
    if (!r || !r.ok) return json({ error: "server" }, 500);
    return json({ ok: true, batch_id: batchId, n: rows.length, skipped: lessons.length - rows.length });
  }

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
    budget_ms: PLAN_BUDGET,
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
