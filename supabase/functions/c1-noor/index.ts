// v2026.11.10 ════════════════════════════════════════════════════════════════
// Edge Function: c1-noor — ربط حساب المعلّم في منصّة نور (lms.moe.gov.om)
// بمنصّة الحلقة الأولى (cycle1) لنشر التحضير ومرفقاته بزرٍّ واحد.
//
// • كلمة مرور نور تُشفَّر (AES-GCM) وتُحفظ في جدول c1_noor_accounts الذي لا
//   يقرؤه المتصفح إطلاقاً (RLS بلا سياسات) — الدالّة وحدها تقرؤه بمفتاح الخدمة.
// • جلسة نور (الكوكيز) تُحفظ مشفّرةً كذلك وتُعاد ٢٥ دقيقة، ثم يُعاد الدخول.
// • لا ذكاء اصطناعي هنا: لا كلفة استدعاء، ولا حصّة.
//
// الأفعال (body.action): status · connect · disconnect · refresh · set_cfg ·
//   lessons · slots · criteria · publish_prep · upload (multipart)
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { Noor, NoorError } from "./noor.ts";

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

const MSG: Record<string, string> = {
  bad_credentials: "اسم المستخدم أو كلمة المرور في نور غير صحيحة.",
  captcha: "طلبت نور التحقّق (reCAPTCHA). سجّل الدخول إلى نور من المتصفح مرةً ثم أعد المحاولة.",
  not_teacher: "هذا الحساب في نور ليس حساب معلّم.",
  not_linked: "لم يُربط حساب نور بعد.",
  session_expired: "انتهت جلسة نور، أعد المحاولة.",
  no_week: "لا يوجد أسبوع دراسي في نور يشمل هذا التاريخ.",
  upload_form_missing: "تعذّر فتح صفحة رفع الملفات في نور.",
  no_file: "لم تستقبل نور الملف.",
  homework_form_missing: "تعذّر فتح صفحة إنشاء الواجب في نور.",
  homework_not_created: "لم تُنشئ نور الواجب.",
  prep_not_found: "أُرسل التحضير لكن لم يظهر في قائمة تحاضير نور. تحقّق من نور قبل إعادة المحاولة.",
  noor_down: "تعذّر الوصول إلى منصّة نور الآن.",
};

// ── التشفير: AES-GCM بمفتاح NOOR_KEY (أو مشتقٍّ من مفتاح الخدمة إن لم يُضبط) ──
let keyP: Promise<CryptoKey> | null = null;
function aesKey() {
  if (!keyP) {
    const raw = Deno.env.get("NOOR_KEY") || ("noor-v1:" + Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"));
    keyP = crypto.subtle.digest("SHA-256", new TextEncoder().encode(raw))
      .then((d) => crypto.subtle.importKey("raw", d, "AES-GCM", false, ["encrypt", "decrypt"]));
  }
  return keyP;
}
const b64 = (u: Uint8Array) => btoa(String.fromCharCode(...u));
const unb64 = (s: string) => Uint8Array.from(atob(s), (c) => c.charCodeAt(0));
async function enc(s: string) {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv }, await aesKey(), new TextEncoder().encode(s)));
  return b64(iv) + "." + b64(ct);
}
async function dec(s: string) {
  const [iv, ct] = s.split(".");
  return new TextDecoder().decode(await crypto.subtle.decrypt({ name: "AES-GCM", iv: unb64(iv) }, await aesKey(), unb64(ct)));
}

const SESSION_MS = 25 * 60e3;

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const authHeader = req.headers.get("Authorization") || "";
    if (!authHeader) return json({ error: "unauthorized" }, 401);
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const { data: { user }, error: userErr } = await admin.auth.getUser(authHeader.replace("Bearer ", ""));
    if (userErr || !user) return json({ error: "unauthorized" }, 401);

    // الطلب: JSON عادةً، أو multipart لرفع ملف (meta + file)
    let b: Any = {};
    let file: File | null = null;
    const ct = req.headers.get("content-type") || "";
    if (ct.includes("multipart/form-data")) {
      const fd = await req.formData();
      try { b = JSON.parse(String(fd.get("meta") || "{}")); } catch { b = {}; }
      const f = fd.get("file");
      if (f && typeof f !== "string") file = f as File;
      // الملف يصل مضغوطاً (gzip) من المتصفح: جدار Cloudflare أمام Supabase يحجب
      // جسماً فيه HTML وسكربتات (ملف اللعبة) ظنّاً أنه هجوم، والمضغوط لا يُقرأ.
      if (file && b.gz) {
        const raw = await new Response(file.stream().pipeThrough(new DecompressionStream("gzip"))).blob();
        file = new File([raw], String(b.filename || "file"), { type: String(b.mime || "application/octet-stream") });
      }
    } else {
      b = await req.json().catch(() => ({}));
    }
    const action = String(b.action || "");

    const getRow = async () => (await admin.from("c1_noor_accounts").select("*").eq("user_id", user.id).maybeSingle()).data;
    const save = (patch: Any) => admin.from("c1_noor_accounts").update({ ...patch, updated_at: new Date().toISOString() }).eq("user_id", user.id);
    const pub = (row: Any) => row ? { linked: true, username: row.username, courses: row.courses || [], cfg: row.cfg || {}, updated_at: row.updated_at } : { linked: false };

    if (action === "status") return json(pub(await getRow()));

    if (action === "connect") {
      const username = String(b.username || "").trim(), password = String(b.password || "");
      if (!username || !password) return json({ error: "missing", message: "أدخل اسم المستخدم وكلمة المرور." }, 400);
      const n = new Noor();
      await n.login(username, password);
      const courses = await n.courses();
      const prev = await getRow();
      const row = {
        user_id: user.id, username, pass_enc: await enc(password),
        sess_enc: await enc(JSON.stringify(n.jar)), sess_at: new Date().toISOString(),
        courses, cfg: prev?.cfg || {}, updated_at: new Date().toISOString(),
      };
      const { error } = await admin.from("c1_noor_accounts").upsert(row);
      if (error) throw error;
      return json(pub(row));
    }

    const row = await getRow();
    if (!row) return json({ error: "not_linked", message: MSG.not_linked }, 400);

    if (action === "disconnect") {
      try { if (row.sess_enc) await new Noor(JSON.parse(await dec(row.sess_enc))).logout(); } catch { /* */ }
      await admin.from("c1_noor_accounts").delete().eq("user_id", user.id);
      return json({ linked: false });
    }

    if (action === "set_cfg") {
      const cfg = { ...(row.cfg || {}) };
      for (const k of ["map", "lessons", "defaults"]) if (b.cfg && b.cfg[k] !== undefined) cfg[k] = { ...(cfg[k] || {}), ...b.cfg[k] };
      await save({ cfg });
      return json({ ok: true, cfg });
    }

    // ── جلسة نور: يعيد استعمال الكوكيز المحفوظة، وإلا يدخل من جديد ──
    let n: Noor | null = null;
    let fresh = false;
    const session = async (force = false) => {
      if (!force && !n && row.sess_enc && row.sess_at && Date.now() - new Date(row.sess_at).getTime() < SESSION_MS) {
        try { n = new Noor(JSON.parse(await dec(row.sess_enc))); return n; } catch { /* يدخل من جديد */ }
      }
      if (n && !force) return n;
      n = new Noor();
      await n.login(row.username, await dec(row.pass_enc));
      fresh = true;
      return n;
    };
    const run = async <T>(fn: (x: Noor) => Promise<T>): Promise<T> => {
      try { return await fn(await session()); } catch (e) {
        if (e instanceof NoorError && e.code === "session_expired" && !fresh) return await fn(await session(true));
        throw e;
      }
    };
    const persist = async (extra: Any = {}) => {
      if (n) await save({ sess_enc: await enc(JSON.stringify((n as Noor).jar)), sess_at: fresh ? new Date().toISOString() : row.sess_at, ...extra });
      else if (Object.keys(extra).length) await save(extra);
    };
    const course = (cid: string) => (row.courses || []).find((c: Any) => c.cid === String(cid));

    if (action === "refresh") {
      const courses = await run((x) => x.courses());
      await persist({ courses });
      return json(pub({ ...row, courses }));
    }

    if (action === "lessons") {
      const c = course(b.cid);
      if (!c) return json({ error: "bad_course" }, 400);
      const cache = row.cache || {};
      if (!b.refresh && cache[c.cid]?.lessons?.length && Date.now() - (cache[c.cid].at || 0) < 14 * 864e5) {
        return json({ lessons: cache[c.cid].lessons });
      }
      const lessons = await run(async (x) => {
        const out: Any[] = [];
        for (const s of await x.semesters(c.enc)) {
          for (const u of await x.subNodes(s.id)) {
            for (const l of await x.subNodes(u.id)) out.push({ id: l.id, name: l.name, unit: u.name, sem: s.name });
          }
        }
        return out;
      });
      cache[c.cid] = { lessons, at: Date.now() };
      await persist({ cache });
      return json({ lessons });
    }

    if (action === "slots") {
      const c = course(b.cid);
      if (!c || !/^\d{4}-\d{2}-\d{2}$/.test(String(b.date || ""))) return json({ error: "bad_input" }, 400);
      const slots = await run((x) => x.slots(c.cid, b.date));
      await persist();
      return json({ slots });
    }

    if (action === "criteria") {
      const criteria = await run((x) => x.criteria(String(b.lesson_id || "")));
      await persist();
      return json({ criteria });
    }

    if (action === "publish_prep") {
      const c = course(b.cid);
      if (!c || !b.lesson_id || !b.title || !/^\d{4}-\d{2}-\d{2}$/.test(String(b.date || "")) || !Array.isArray(b.slots) || !b.slots.length) {
        return json({ error: "bad_input", message: "بيانات النشر ناقصة (الدرس أو التاريخ أو الحصص)." }, 400);
      }
      const out = await run(async (x) => {
        const before = new Set((await x.preps(c.cid)).map((p) => p.id));
        const r = await x.publishPrep({
          enc: c.enc, lessonId: String(b.lesson_id), title: String(b.title), date: b.date,
          slots: b.slots.map((s: Any) => ({ lts: String(s.lts), timeslot: String(s.timeslot) })),
          criteria: (b.criteria || []).map(String), taxonomy: (b.taxonomy || []).map(String),
          strategies: (b.strategies || []).map(String), aids: (b.aids || []).map(String),
          fields: b.fields || {},
        });
        const after = await x.preps(c.cid);
        const added = after.filter((p) => !before.has(p.id));
        const mine = added.find((p) => p.title.replace(/\s+/g, "") === String(b.title).replace(/\s+/g, "")) || added[added.length - 1];
        return { prep_id: mine?.id || "", week: r.week, status: r.status };
      });
      await persist();
      if (!out.prep_id) return json({ error: "prep_not_found", message: MSG.prep_not_found }, 502);
      return json({ ok: true, ...out });
    }

    if (action === "upload") {
      const c = course(b.cid);
      if (!c || !file || !b.prep_id || !b.lesson_id) return json({ error: "bad_input", message: "الملف أو التحضير مفقود." }, 400);
      if (file.size > 25 * 1024 * 1024) return json({ error: "too_big", message: "الملف أكبر من ٢٥ ميغابايت." }, 400);
      const r = await run((x) => x.uploadFile({
        cid: c.cid, prepId: String(b.prep_id), lessonId: String(b.lesson_id), title: String(b.title || file!.name),
        comments: String(b.comments || ""), date: String(b.date), sections: (b.sections || []).map(String),
        file: file!, filename: String(b.filename || file!.name || "file"), criteria: (b.criteria || []).map(String),
        kind: b.kind === "Scorm" ? "Scorm" : "Material",
      }));
      await persist();
      if (!r.ok) return json({ error: r.err || "upload_failed", message: MSG[r.err] || "لم تؤكّد نور حفظ الملف." }, 502);
      return json({ ok: true });
    }

    if (action === "homework") {
      const c = course(b.cid);
      const items = (Array.isArray(b.items) ? b.items : []).filter((q: Any) => q && q.text && Array.isArray(q.choices) && q.choices.length >= 2 && q.choices.length <= 6)
        .map((q: Any) => ({ text: String(q.text).slice(0, 2000), choices: q.choices.map((x: Any) => String(x).slice(0, 500)), answer: Math.max(1, Math.min(q.choices.length, +q.answer || 1)) }));
      const dt = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/;
      if (!c || !items.length || items.length > 20 || !b.title || !dt.test(String(b.publish || "")) || !dt.test(String(b.due || ""))) {
        return json({ error: "bad_input", message: "بيانات الواجب ناقصة (١–٢٠ سؤالاً وتاريخا النشر والتسليم)." }, 400);
      }
      const out = await run(async (x) => {
        const qurl = await x.createHomework({ cid: c.cid, title: String(b.title).slice(0, 200), publish: b.publish, due: b.due,
          prepId: b.prep_id ? String(b.prep_id) : "", lessonId: b.lesson_id ? String(b.lesson_id) : "", sections: (b.sections || []).map(String) });
        const r = await x.addQuestions(qurl, items);
        return { qurl, added: r.ok };
      });
      await persist();
      if (!out.added) return json({ error: "questions_failed", message: "أُنشئ الواجب لكن لم تُضَف أسئلته — افتحه في نور.", qurl: out.qurl }, 502);
      return json({ ok: true, qurl: out.qurl, count: items.length });
    }

    return json({ error: "bad_action" }, 400);
  } catch (e) {
    if (e instanceof NoorError) return json({ error: e.code, message: MSG[e.code] || e.message }, e.code === "bad_credentials" ? 400 : 502);
    const msg = String((e as Error)?.message || e);
    if (/fetch|network|connect|timed? ?out|dns/i.test(msg)) return json({ error: "noor_down", message: MSG.noor_down }, 502);
    console.error("c1-noor", msg);
    return json({ error: "server", message: "خطأ في الخادم." }, 500);
  }
});
