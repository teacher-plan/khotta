// v2026.11.10 ════════════════════════════════════════════════════════════════
// Edge Function: c1-noor — ربط حساب المعلّم في منصّة نور (lms.moe.gov.om)
// بمنصّة الحلقة الأولى (cycle1) لنشر التحضير ومرفقاته بزرٍّ واحد.
//
// • كلمة مرور نور تُشفَّر (AES-GCM) وتُحفظ في جدول c1_noor_accounts الذي لا
//   يقرؤه المتصفح إطلاقاً (RLS بلا سياسات) — الدالّة وحدها تقرؤه بمفتاح الخدمة.
// • جلسة نور (الكوكيز) تُحفظ مشفّرةً كذلك وتُعاد ٢٥ دقيقة، ثم يُعاد الدخول.
// • لا ذكاء اصطناعي في أفعال المعلّمين؛ «مختبر نور» (lab_*) وحده يستعمله، وهو
//   مقصورٌ على حسابات LAB_EMAILS ويُحسب من حصّة صاحبه.
//
// الأفعال (body.action): status · connect · disconnect · refresh · set_cfg ·
//   lessons · slots · criteria · publish_prep · upload (multipart)
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { Noor, NoorError } from "./noor.ts";
import { orFetch, orErrCode } from "../_shared/ai.ts";
import { takeQuota, logAiCost } from "../_shared/quota.ts";
import { parseAiJson } from "../_shared/aiJson.ts";
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
  ms_mfa: "حسابك الوزاري يطلب رمز تحقّق، فاربطه بزرّ «الربط بالبريد الوزاري مع رمز التحقّق».",
  ms_code_expired: "انتهت مهلة الرمز قبل إكمال الدخول. ابدأ الربط من جديد.",
  ms_declined: "رُفض طلب الدخول من صفحة Microsoft.",
  ms_relink: "انتهت صلاحية ربط البريد الوزاري. افصل حساب نور ثم اربطه من جديد.",
  ms_pass_expired: "انتهت صلاحية كلمة مرور البريد الوزاري. غيّرها من بوابة Microsoft ثم أعد الربط.",
  ms_locked: "حساب البريد الوزاري مقفل مؤقتاً بعد محاولات كثيرة. انتظر قليلاً ثم أعد المحاولة.",
  ms_unsupported: "رفضت Microsoft الدخول بالبريد الوزاري من خارج صفحة نور. استعمل اسم المستخدم وكلمة مرور نور.",
  ms_noor_refused: "تحقّقت Microsoft من بريدك لكن نور لم تقبل الدخول. استعمل اسم المستخدم وكلمة مرور نور.",
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
const HW_DAY_CAP = 20; // حدّ نور: أسئلة الواجبات والاختبارات المحتسبة لكل تاريخ نشر

// ══ مختبر نور — حساباتٌ تجريبية فقط؛ لا يراه أي معلّمٍ آخر ولا تقبله الدالّة منه ══
const LAB_EMAILS = ["xx@y.com", "teacherplane2026project@gmail.com"];
// المستكشف قراءةٌ فقط: يُرفض أي مسارٍ قد يُغيّر شيئاً حتى لو كان GET
// المستكشف من GitHub يفتح صفحات النماذج (add/create/edit) بطلب GET فقط لقراءة حقولها
const RAW_BLOCK_SVC = /delete|remove|logout|publish|archive|trash|toggle|save|update|set_|mark|send|upload|approve|reject|copy|move|restore|import|reset|grade/i;
const RAW_BLOCK = /delete|remove|logout|publish|archive|trash|toggle|edit|add|create|save|update|set_|mark|send|compose|upload|approve|reject|copy|move|restore|import|reset|grade/i;
// تاريخ مسقط (UTC+4) بعد إزاحة أيام
function mctDate(addDays: number) {
  return new Date(Date.now() + 4 * 3600e3 + addDays * 864e5).toISOString().slice(0, 10);
}
// أيام الدراسة (الأحد–الخميس) للأسبوع الذي فيه التاريخ؛ الجمعة والسبت ← الأسبوع القادم
function schoolWeek(d: string) {
  const t = new Date(d + "T12:00:00Z");
  const wd = t.getUTCDay(); // 0 الأحد
  const start = new Date(t.getTime() + (wd >= 5 ? 7 - wd : -wd) * 864e5);
  return [0, 1, 2, 3, 4].map((i) => new Date(start.getTime() + i * 864e5).toISOString().slice(0, 10));
}

async function labAi(admin: Any, user: Any, b: Any) {
  const apiKey = Deno.env.get("OPENROUTER_API_KEY");
  if (!apiKey) return json({ error: "server_not_configured" }, 500);
  const { data: rows } = await admin.from("ai_settings").select("key,value");
  const st: Record<string, string> = {};
  (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
  const task = String(b.task || "");
  const data = JSON.stringify(b.data || {}).slice(0, 9000);
  const base = "أنت مستشارٌ خبير في منصّة نور التعليمية (كلاسيرا) بسلطنة عُمان، تعمل لمعلّم رياضيات (خاطبه بصيغة المذكّر) بالعربية الفصحى الميسّرة.";
  const rules = "قواعد نقاط نور: سؤال واجب/اختبار ٥ نقاط (+٢ إن كان عامّاً في البنك) وحدّه ٢٠ سؤالاً لكل تاريخ نشر؛ ملف مرفق ١٥ نقطة (+١٠٪ مشاركة مع المدرسة، +٣٠٪ في المكتبة العامة) وحدّ الملفات ١٠ يومياً؛ درس تفاعلي سكورم ٤٠ نقطة؛ فيديو يوتيوب ١٠؛ موضوع نقاش ٢٠ بحسب نسبة ردود الطلاب؛ فصل افتراضي ١٠٠ بحسب الحضور؛ رسالة ١ (حدّ ٥ يومياً) عند قراءتها. كل نشاط يُضرب في نسبة تفاعل الطلاب، والمكرّر والفارغ لا يُحتسب وقد يُصفّر النقاط، وحذف المحتوى يحذف نقاطه. البطاقات: أفضل ٥٪ في المدرسة ماسية، ٤٠٪ ذهبية، ٥٥٪ خضراء.";
  let system = "", user_ = "", jsonOut = false, maxT = 1500;
  if (task === "coach") {
    system = [base, rules, "أمامك بيانات المعلّم الحالية من نور (النقاط اليومية، ما نُشر اليوم مقابل الحدود، تغطية تحضير حصص الأسبوع، تفاعل الطلاب مع الواجبات).",
      "اكتب «خطة اليوم لرفع النقاط» بعناوين Markdown (##) وقوائم قصيرة:",
      "## أين تقف (٣ نقاط بالأرقام: الاتجاه، الفجوة مع أنشط معلّمي المدرسة، ما تبقّى من حدود اليوم)",
      "## افعل اليوم (٣–٥ خطوات مرتّبة بالأثر، لكل خطوةٍ النقاط المتوقّعة تقريباً وكيف تُنفّذ من خُطّة)",
      "## ارفع تفاعل الطلاب (لأنه المضاعِف: ٢–٣ أفكار عملية مرتبطة بالأرقام)",
      "## تجنّب (ما يُسقط النقاط)",
      "لا تخترع أرقاماً غير الموجودة. ٢٠٠–٣٥٠ كلمة."].join("\n");
    user_ = "البيانات:\n" + data;
  } else if (task === "students") {
    system = [base, "أمامك تحليلٌ مجمّع لتفاعل طلاب المعلّم مع واجبات نور (بلا أسماء: معرّفات رقمية وفئات).",
      "اكتب قراءةً تربوية عملية بعناوين Markdown: ## الصورة العامة، ## الشعب (مقارنة وتفسير محتمل)، ## الواجبات (أيها تفاعلٌ ضعيف ولماذا قد يكون: الطول، التوقيت، الصعوبة)، ## خطة أسبوع لرفع نسبة التسليم (خطوات محدّدة: توقيت النشر، طول الواجب، تذكير، تحفيز، متابعة غير المسلّمين).",
      "تفاعل الطلاب يضاعف نقاط المعلّم في نور، فاربط التوصيات بذلك. لا تخترع أرقاماً. ٢٥٠–٤٠٠ كلمة."].join("\n");
    user_ = "التحليل:\n" + data;
  } else if (task === "hw") {
    const n = Math.max(3, Math.min(20, +b.n || 10));
    jsonOut = true; maxT = 5000;
    system = [base, `أنشئ ${n} سؤال اختيار من متعدد لواجب منزلي قصير في نور، من درسٍ واحد في منهج سلطنة عُمان.`,
      "الشروط: لكل سؤال ٤ خيارات، إجابة صحيحة واحدة، مشتّتات مأخوذة من أخطاء الطلاب الشائعة، تدرّج من السهل إلى الأصعب، لغة واضحة قصيرة، أرقام عربية مشرقية داخل النصوص، بلا رسوم.",
      "تنوّع: مفهوم، إجراء، تطبيق حياتي من البيئة العُمانية، تحليل خطأ. لا تكرّر سؤالاً.",
      'أعد JSON فقط في سطر واحد: {"items":[{"text":"...","choices":["...","...","...","..."],"answer":1}]} حيث answer رقم الخيار الصحيح (١–٤ بأرقام لاتينية في JSON).'].join("\n");
    user_ = `الصف: ${String(b.grade || "")}\nالمادة: ${String(b.subject || "الرياضيات")}\nالوحدة: ${String(b.unit || "")}\nالدرس: ${String(b.lesson || "")}\nالمستوى: ${String(b.level || "متوسط")}`;
  } else if (task === "post") {
    jsonOut = true; maxT = 1500;
    system = [base, "اكتب لدرسٍ واحد: (١) موضوع نقاش قصير يثير ردود الطلاب في غرفة النقاش بنور (سؤال مفتوح ممتع مرتبط بالحياة، يطلب من كل طالب ردّاً قصيراً بمثاله الخاص)، (٢) رسالة تذكير ودّية قصيرة للطلاب بالواجب المنشور وموعد تسليمه، (٣) فكرة فيديو يوتيوب قصير يُبحث عنه (كلمات بحث).",
      'أعد JSON فقط: {"topic_title":"...","topic_body":"...","message_title":"...","message_body":"...","video_query":"..."}'].join("\n");
    user_ = `الصف: ${String(b.grade || "")}\nالدرس: ${String(b.lesson || "")}\nموعد التسليم: ${String(b.due || "")}`;
  } else return json({ error: "bad_task" }, 400);

  const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
  if (!quota.ok) return json({ error: "quota_exceeded", message: "نفدت حصّة الذكاء الاصطناعي." }, 429);
  const model = st.model_insights || st.model_chat || st.chat_model || st.ai_model || "google/gemini-2.5-flash";
  const orResp = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta Noor Lab" },
    body: JSON.stringify({ model, messages: [{ role: "system", content: system }, { role: "user", content: user_ }], temperature: jsonOut ? 0.5 : 0.4, max_tokens: maxT }),
  }, { st, task: "chat" });
  const or = await orResp.json();
  if (!orResp.ok) return json({ error: orErrCode(orResp.status, String(or?.error?.message || "")), message: "تعذّر الاتصال بالذكاء الاصطناعي." }, 502);
  const text = String(or?.choices?.[0]?.message?.content || "").trim();
  await logAiCost(admin, user.id, "c1-noor-lab", "text", model, or?.usage);
  if (!jsonOut) return text ? json({ text }) : json({ error: "bad_output", message: "لم يُرجع النموذج نصاً." }, 502);
  const p = parseAiJson<Any>(text);
  if (!p.ok) return json({ error: "bad_output", message: "تعذّر قراءة ردّ النموذج، أعد المحاولة." }, 502);
  if (task === "hw") {
    const items = (Array.isArray(p.value?.items) ? p.value.items : []).filter((q: Any) => q && q.text && Array.isArray(q.choices) && q.choices.length >= 2)
      .map((q: Any) => ({ text: String(q.text), choices: q.choices.slice(0, 6).map(String), answer: Math.max(1, Math.min(q.choices.length, +q.answer || 1)) }));
    if (!items.length) return json({ error: "bad_output", message: "لم تُولَّد أسئلة صالحة." }, 502);
    return json({ items });
  }
  return json(p.value || {});
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const authHeader = req.headers.get("Authorization") || "";
    if (!authHeader) return json({ error: "unauthorized" }, 401);
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    // مستكشف المطوّر من GitHub Actions: مفتاح الخدمة + x-lab-as (بريد من LAB_EMAILS)،
    // ولا يُسمح فيه إلا بـ lab_raw (قراءة GET فقط) — لاكتشاف نماذج نور دون كلمة مرور.
    let svcLab = false;
    // deno-lint-ignore no-explicit-any
    let user: any = null;
    const labAs = (req.headers.get("x-lab-as") || "").trim().toLowerCase();
    if (labAs && isServiceRoleRequest(req)) {
      if (!LAB_EMAILS.includes(labAs)) return json({ error: "forbidden" }, 403);
      const { data } = await admin.auth.admin.listUsers({ page: 1, perPage: 1000 });
      user = (data?.users || []).find((u: Any) => String(u.email || "").toLowerCase() === labAs) || null;
      if (!user) return json({ error: "unauthorized" }, 401);
      svcLab = true;
    } else {
      const { data: { user: u }, error: userErr } = await admin.auth.getUser(authHeader.replace("Bearer ", ""));
      if (userErr || !u) return json({ error: "unauthorized" }, 401);
      user = u;
    }

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
    if (svcLab && action !== "lab_raw") return json({ error: "forbidden" }, 403);

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

    // ── الربط بالبريد الوزاري مع رمز التحقّق: رمز الجهاز من Microsoft ──
    if (action === "ms_start") {
      const d = await Noor.msDeviceStart();
      return json({ user_code: d.user_code, uri: d.uri, interval: d.interval, expires_in: d.expires_in, dc: await enc(d.device_code) });
    }
    if (action === "ms_poll") {
      let dc = "";
      try { dc = await dec(String(b.dc || "")); } catch { return json({ error: "ms_code_expired", message: MSG.ms_code_expired }, 400); }
      const t = await Noor.msDevicePoll(dc);
      if (!t) return json({ pending: true });
      if (!t.refresh) return json({ error: "ms_unsupported", message: MSG.ms_unsupported }, 400);
      const n = new Noor();
      await n.msTokenLogin(t.access);
      const courses = await n.courses();
      const email = (await Noor.msEmail(t.access)) || "البريد الوزاري";
      const prev = await getRow();
      const row = {
        user_id: user.id, username: email, pass_enc: await enc("msrt:" + t.refresh),
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
      const secret = await dec(row.pass_enc);
      if (secret.startsWith("msrt:")) {
        // حساب بريدٍ وزاري مربوطٌ برمز الجهاز: نجدّد رمز Microsoft ونحفظ الجديد
        const t = await Noor.msRefresh(secret.slice(5));
        await n.msTokenLogin(t.access);
        if (t.refresh !== secret.slice(5)) { row.pass_enc = await enc("msrt:" + t.refresh); await save({ pass_enc: row.pass_enc }); }
      } else await n.login(row.username, secret);
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

    // ── استيراد الجدول الأسبوعي وقوائم الطلاب من نور ──
    // الجدول: حصص كل مقرّرٍ في أيام هذا الأسبوع (الأحد–الخميس)، وإن خلا الأسبوع
    // (إجازة) جُرّب الأسبوع التالي. الطلاب: قائمة الدرجات لكل مقرّر وفيها الشعبة.
    if (action === "import_info") {
      const cids: string[] = (row.courses || []).map((c: Any) => c.cid);
      const out = await run(async (x) => {
        const sched: Any[] = [];
        for (const off of [0, 7, 14]) {
          const days = schoolWeek(mctDate(off));
          for (const cid of cids) {
            for (let i = 0; i < days.length; i++) {
              const sl = await x.slots(cid, days[i]).catch(() => [] as Any[]);
              for (const s of sl) {
                const p = +((String(s.period).replace(/[٠-٩]/g, (d) => String("٠١٢٣٤٥٦٧٨٩".indexOf(d))).match(/\d+/) || [])[0] || 0);
                if (p) sched.push({ cid, day: i, period: p, sec: s.section });
              }
            }
          }
          if (sched.length) return { sched, week: days[0] };
        }
        return { sched, week: "" };
      });
      const rosters: Any[] = [];
      for (const cid of cids) {
        const list = await run((x) => x.studentsScores(cid)).catch(() => [] as Any[]);
        const by: Record<string, string[]> = {};
        for (const s of list) if (s.name) (by[s.sec] = by[s.sec] || []).includes(s.name) || by[s.sec].push(s.name);
        for (const [sec, names] of Object.entries(by)) rosters.push({ cid, sec, names: names.sort((a, b) => a.localeCompare(b, "ar")) });
      }
      await persist();
      return json({ ...out, rosters });
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
      // ── حدّ نور اليومي: ٢٠ سؤالاً لكل تاريخ نشر (لكل مقرّرات المعلّم). ما زاد لا تحتسبه
      //    نور نقاطاً، فيُمنع النشر ويُشرح السبب ويُقترح أقرب يومٍ فيه متّسع ──
      const day = String(b.publish).slice(0, 10);
      const used: Record<string, number> = await run(async (x) => {
        const m: Record<string, number> = {};
        for (const cc of (row.courses || [])) {
          for (const h of await x.homeworksList(cc.cid)) { const d = h.publish.slice(0, 10); if (d >= day) m[d] = (m[d] || 0) + h.q; }
        }
        return m;
      });
      const onDay = used[day] || 0;
      if (onDay + items.length > HW_DAY_CAP) {
        await persist();
        const t = new Date(day + "T12:00:00Z");
        let free = "";
        for (let k = 1; k < 40 && !free; k++) {
          const d = new Date(t.getTime() + k * 864e5); const wd = d.getUTCDay(); const ds = d.toISOString().slice(0, 10);
          if (wd !== 5 && wd !== 6 && (used[ds] || 0) + items.length <= HW_DAY_CAP) free = ds;
        }
        const left = Math.max(0, HW_DAY_CAP - onDay);
        const ar = (v: number | string) => String(v).replace(/\d/g, (c) => "٠١٢٣٤٥٦٧٨٩"[+c]);
        return json({
          error: "daily_cap", used: onDay, cap: HW_DAY_CAP, left, suggest: free,
          message: `لم يُنشر الواجب: نور تحتسب ${ar(HW_DAY_CAP)} سؤالاً فقط لكل تاريخ نشر، وما زاد عليها لا يُحسب لك نقاطاً. ` +
            `بتاريخ ${ar(day)} في نور الآن ${ar(onDay)} سؤالاً، وهذا الواجب ${ar(items.length)} سؤالاً` +
            (left ? ` (المتاح ${ar(left)} فقط).` : " (لا متّسع).") +
            (free ? ` اختر تاريخ نشر آخر — أقرب يومٍ فيه متّسع: ${ar(free)}.` : " اختر تاريخ نشر آخر أو قلّل عدد الأسئلة."),
        }, 409);
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

    // ══ مختبر نور: حسابات المطوّر فقط (قراءةٌ من نور + ذكاء اصطناعي) ══
    if (action.startsWith("lab_")) {
      if (!LAB_EMAILS.includes((user.email || "").toLowerCase())) return json({ error: "forbidden" }, 403);
      const cids: string[] = (row.courses || []).map((c: Any) => c.cid);
      const today = mctDate(0);

      if (action === "lab_overview") {
        const out = await run(async (x) => {
          const score = await x.myScore();
          const caps = { q: 0, files: 0, scorm: 0, hw: 0 };
          const qByDate: Record<string, number> = {}, fByDate: Record<string, number> = {};
          const preps: Any[] = [], hwTitles: Any[] = [], prepOpts: Any[] = [], scorms: Any[] = [];
          const recent: Any[] = [];
          const week: Any[] = [];
          const days = schoolWeek(today);
          for (const cid of cids) {
            const hws = await x.homeworksList(cid);
            for (const h of hws) {
              const d = h.publish.slice(0, 10);
              if (d >= today) qByDate[d] = (qByDate[d] || 0) + h.q;
              if (d === today) { caps.q += h.q; caps.hw++; }
              recent.push({ kind: "hw", cid, title: h.title, at: h.publish, q: h.q });
            }
            for (const k of ["Material", "Scorm"]) {
              for (const a of await x.attachmentsList(cid, k)) {
                const d = a.publish.slice(0, 10);
                if (d >= today) fByDate[d] = (fByDate[d] || 0) + 1;
                if (d === today) { caps.files++; if (k === "Scorm") caps.scorm++; }
                recent.push({ kind: k === "Scorm" ? "scorm" : "file", cid, title: a.title, at: a.publish });
                if (k === "Scorm") scorms.push({ cid, title: a.title, publish: a.publish });
              }
            }
            for (const pr of await x.prepsList(cid).catch(() => [])) preps.push({ ...pr, cid });
            // معرّفات التحاضير الرقمية (من نموذج الرفع) — يحتاجها رفع ملفٍّ مرفقٍ بتحضيرٍ قائم
            for (const po of await x.preps(cid).catch(() => [])) prepOpts.push({ ...po, cid });
            for (const h of hws) hwTitles.push({ cid, title: h.title, publish: h.publish });
            for (const d of days) {
              const sl = await x.slots(cid, d).catch(() => []);
              week.push({ cid, date: d, slots: sl.map((s) => ({ sec: s.section, period: s.period, prep: s.has_prep })) });
            }
          }
          recent.sort((a, b) => String(b.at).localeCompare(String(a.at)));
          return { score, caps, qByDate, fByDate, preps, hwTitles, prepOpts, scorms, today, week, recent: recent.slice(0, 40), totals: { hw: recent.filter((r) => r.kind === "hw").length, files: recent.filter((r) => r.kind === "file").length, scorm: recent.filter((r) => r.kind === "scorm").length } };
        });
        await persist();
        return json(out);
      }

      if (action === "lab_students") {
        const c = course(b.cid) || course(cids[0]);
        if (!c) return json({ error: "bad_course" }, 400);
        const cache = row.cache || {};
        const key = "lab_st_" + c.cid;
        if (!b.refresh && cache[key] && Date.now() - (cache[key].at || 0) < 30 * 60e3) return json(cache[key].data);
        const data = await run(async (x) => {
          const scores = await x.studentsScores(c.cid);
          const tok = await x.monitorTokens(c.cid);
          // واجباتٌ مضى على نشرها يومٌ على الأقل: واجب اليوم لم يُتح للطلاب وقتٌ لحلّه بعد
          const cut = mctDate(0);
          const hws = (await x.homeworksList(c.cid)).filter((h) => h.publish.slice(0, 10) < cut).sort((a, b) => b.publish.localeCompare(a.publish)).slice(0, Math.min(20, +b.n || 12));
          const subs: Record<string, Any[]> = {};
          if (tok) {
            for (let i = 0; i < hws.length; i += 4) {
              const part = hws.slice(i, i + 4);
              const res = await Promise.all(part.map((h) => x.submissions(tok, h.id).catch(() => [])));
              part.forEach((h, k) => { subs[h.id] = res[k]; });
            }
          }
          // جدولٌ مضغوط: لكل واجبٍ مصفوفة [معرّف الطالب، العلامة أو null إن لم يسلّم]
          const students: Record<string, Any> = {};
          for (const s of scores) students[s.sid] = { name: s.name, sec: s.sec, score: s.score };
          const hw = hws.map((h) => {
            const list = subs[h.id] || [];
            for (const s of list) if (!students[s.sid]) students[s.sid] = { name: s.name, sec: s.sec, score: 0 };
            return { id: h.id, title: h.title, q: h.q, publish: h.publish, due: h.due, sub: list.filter((s) => s.at).map((s) => [s.sid, s.mark, s.at.slice(0, 16)]) };
          });
          return { cid: c.cid, course: c.name, students, hw, at: new Date().toISOString() };
        });
        cache[key] = { at: Date.now(), data };
        await persist({ cache });
        return json(data);
      }

      if (action === "lab_raw") {
        const path = String(b.path || "").trim();
        if (!/^\/(teacher|schadmin\/nodes)\/[\w\-/:.%?=&]*$/.test(path) || (svcLab ? RAW_BLOCK_SVC : RAW_BLOCK).test(path)) return json({ error: "bad_path", message: "مسارٌ غير مسموح (قراءة فقط، يبدأ بـ /teacher/)." }, 400);
        const r = await run((x) => x.req(path, { ajax: !!b.ajax }));
        await persist();
        return json({ status: r.status, url: r.url, size: r.text.length, text: r.text.slice(0, 250000) });
      }

      if (action === "lab_ai") return await labAi(admin, user, b);
    }

    return json({ error: "bad_action" }, 400);
  } catch (e) {
    if (e instanceof NoorError) {
      if (e.code.startsWith("ms_")) console.error("c1-noor ms", e.code, e.message);
      return json({ error: e.code, message: MSG[e.code] || e.message }, e.code === "bad_credentials" || e.code.startsWith("ms_") ? 400 : 502);
    }
    const msg = String((e as Error)?.message || e);
    if (/fetch|network|connect|timed? ?out|dns/i.test(msg)) return json({ error: "noor_down", message: MSG.noor_down }, 502);
    console.error("c1-noor", msg);
    return json({ error: "server", message: "خطأ في الخادم." }, 500);
  }
});
