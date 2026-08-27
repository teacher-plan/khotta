// ════════════════════════════════════════════════════════════════
// Edge Function: activate-teacher
// تفعيل حساب معلّمة بضغطة واحدة بعد تأكيد اشتراكها:
// إنشاء الحساب ببريدها الذي سجّلت به، وتصريحه للدخول، ثم إرسال
// بياناتها إلى بريدها. السماحية للمشرف وحده.
//
// النشر: supabase functions deploy activate-teacher
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

// حروفٌ بلا ملتبسات (0/O و1/l/I): كلمة المرور تُقرأ من بريدٍ وتُنسخ يدوياً
// أحياناً، والالتباس فيها يعني معلّمةً تظنّ حسابها معطّلاً وهو سليم.
function genPassword() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789";
  const bytes = new Uint32Array(10);
  crypto.getRandomValues(bytes);
  let p = "";
  for (let i = 0; i < 10; i++) p += chars[bytes[i] % chars.length];
  return p;
}

// مدد الصلاحية. الافتراضي «مدفوع» كي يبقى سلوك أي نداءٍ قديم لا يمرّر
// plan كما كان تماماً من ناحية الإنشاء، مع إضافة تاريخ انتهاءٍ صريح.
const PLAN_DAYS: Record<string, number> = {
  paid: 150,   // خمسة أشهر (٥ × ٣٠ يوماً)
  trial: 14,   // تفعيل تجريبي
};
// تجربة العام الدراسي الحالي: بدل ١٤ يوماً من التفعيل، تنتهي في تاريخٍ
// ثابت (نهاية أول يوم دوامٍ فعلياً، ٣٠/٨/٢٠٢٦ بتوقيت عُمان) — فمن تُفعّل
// حسابها مبكراً تُبقي تجربتها حتى بداية الفصل بدل أن تنتهي قبله. بعد هذا
// التاريخ نعود تلقائياً لقاعدة الأيام المعتادة، وإلا صار كل تفعيلٍ تجريبيّ
// لاحقٍ خلال العام منتهياً منذ لحظته (تاريخٌ في الماضي).
const TRIAL_FIXED_DEADLINE = new Date("2026-08-30T20:00:00Z"); // نهاية ٣٠/٨ بتوقيت عُمان (UTC+4)

// اختيارُ تاريخ نهايةٍ يدويٍّ للتجربة (من لوحة الإدارة) — معلّمةٌ قد تطلب
// تجربةً في منتصف الفصل، فالتاريخ الثابت وحده (٣٠/٨) لا يناسبها. صيغة
// customDate: "YYYY-MM-DD"؛ تُرفَض بصمتٍ (رجوعٌ للمنطق التلقائي) إن كانت
// غير صالحة أو في الماضي — لا تُفشِل التفعيل بسبب مُدخلٍ سيّئ.
function expiryFor(plan: string, customDate?: string): string {
  if (plan === "trial" && customDate) {
    const d = new Date(customDate + "T20:00:00Z"); // نهاية اليوم المختار بتوقيت عُمان
    if (!isNaN(d.getTime()) && d.getTime() > Date.now()) return d.toISOString();
  }
  if (plan === "trial" && Date.now() < TRIAL_FIXED_DEADLINE.getTime()) {
    return TRIAL_FIXED_DEADLINE.toISOString();
  }
  const days = PLAN_DAYS[plan] ?? PLAN_DAYS.paid;
  return new Date(Date.now() + days * 24 * 60 * 60 * 1000).toISOString();
}

function mailHtml(name: string, email: string, password: string, link: string, plan = "paid") {
  const trial = plan === "trial";
  const esc = (s: string) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));
  return `<!doctype html><html lang="ar" dir="rtl"><body style="margin:0;background:#F3EDE3;font-family:Tahoma,Arial,sans-serif;color:#2A1503">
<div style="max-width:520px;margin:24px auto;background:#FFFDF9;border:1.5px solid #E3D2BD;border-radius:18px;padding:26px">
  <div style="font-size:12px;font-weight:bold;letter-spacing:2px;color:#A83030">منصة خُطّة</div>
  <h1 style="font-size:22px;margin:6px 0 4px">أهلاً ${esc(name)} 👋</h1>
  <p style="font-size:14px;line-height:1.9;color:#7A6A58;margin:0 0 18px">
    ${trial
      ? "فُتِح لكِ حسابٌ تجريبيّ في منصّة «خُطّة» للحلقة الأولى لمدّة ١٤ يوماً، تستخدمين فيه المنصّة كاملةً بلا نقص. هذه بيانات دخولكِ:"
      : "فُعِّل حسابكِ في منصّة «خُطّة» للحلقة الأولى. هذه بيانات دخولكِ:"}</p>
  <div style="background:#FBF4EA;border:1.5px solid #E3D2BD;border-radius:12px;padding:14px;margin-bottom:16px">
    <div style="font-size:12px;color:#7A6A58">البريد الإلكتروني</div>
    <div style="font-size:15px;font-weight:bold;direction:ltr;text-align:left;margin-bottom:10px">${esc(email)}</div>
    <div style="font-size:12px;color:#7A6A58">كلمة المرور</div>
    <div style="font-size:19px;font-weight:bold;letter-spacing:2px;direction:ltr;text-align:left">${esc(password)}</div>
  </div>
  <a href="${esc(link)}" style="display:block;text-align:center;background:#C9453B;color:#fff;text-decoration:none;
     font-weight:bold;font-size:15px;padding:13px;border-radius:12px">ادخلي إلى حسابكِ</a>
  <p style="font-size:12px;line-height:1.9;color:#7A6A58;margin:16px 0 0">
    ننصحكِ بتغيير كلمة المرور بعد أول دخول. وإن واجهتكِ أي مشكلة فراسلينا وسنساعدكِ فوراً.</p>
</div></body></html>`;
}

// الإرسال عبر Resend. غيابُ المفتاح لا يُفشل التفعيل: الحساب يُنشأ وتُعاد
// كلمة المرور للمشرف ليرسلها بنفسه — تعطُّل البريد لا يوقف الاشتراك.
async function sendMail(to: string, subject: string, html: string) {
  const key = (Deno.env.get("RESEND_API_KEY") || "").trim();
  const from = (Deno.env.get("MAIL_FROM") || "").trim();
  if (!key || !from) return { sent: false, reason: "mail_not_configured" };
  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: { "Authorization": "Bearer " + key, "Content-Type": "application/json" },
      body: JSON.stringify({ from, to: [to], subject, html }),
    });
    if (!r.ok) {
      const d = await r.text();
      return { sent: false, reason: d.slice(0, 200) };
    }
    return { sent: true };
  } catch (e) {
    return { sent: false, reason: String(e).slice(0, 200) };
  }
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) return json({ error: "unauthorized" }, 401);

    const admin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );
    const userClient = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
      { global: { headers: { Authorization: authHeader } } },
    );
    const { data: { user } } = await userClient.auth.getUser();
    if (!user) return json({ error: "unauthorized" }, 401);
    const { data: isAdmin } = await userClient.rpc("is_app_admin");
    if (!isAdmin) return json({ error: "forbidden" }, 403);

    const b = await req.json().catch(() => ({}));

    // وضع الاختبار: يرسل رسالةً نموذجية ولا ينشئ حساباً ولا يمسّ صفّاً.
    // بدونه لا سبيل للتأكّد من إعداد البريد إلا بتفعيل معلّمةٍ حقيقية —
    // وخطأ الإعداد عندها يكلّف حساباً مفعَّلاً لم تصلها بياناته.
    if (b.test === true) {
      const to = String(b.to || "").trim();
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(to)) return json({ error: "bad_email" }, 400);
      const r = await sendMail(to, "رسالة اختبار — منصّة خُطّة",
        mailHtml("معلّمتنا", to, "PaSSw0rdTest", "https://khotati.com/cycle1.html"));
      // السبب كان يظهر للمشرف في المتصفح فقط ويضيع فوراً — الآن يُسجَّل هنا
      // أيضاً ليبقى قابلاً للفحص لاحقاً عبر سجلّات الدالة (edge_logs).
      if (!r.sent) console.error(`activate-teacher (test): فشل الإرسال إلى ${to} — السبب: ${r.reason}`);
      return json({ ok: true, test: true, mailed: r.sent, mailReason: r.reason || null, to });
    }

    // خطّة الاشتراك: paid (خمسة أشهر) أو trial (١٤ يوماً). أي قيمةٍ أخرى
    // — أو غيابُها — تُعامَل مدفوعةً، فلا يكسر نداءٌ قديم شيئاً.
    const plan = b.plan === "trial" ? "trial" : "paid";

    const regId = b.regId;
    if (!regId) return json({ error: "no_reg" }, 400);

    // ─── تمديد حسابٍ قائم ───
    // لازمٌ لا كماليّ: معلّمةٌ جرّبت أسبوعين ثم دفعت لا سبيل لترقيتها بغيره،
    // ولا يُنشئ شيئاً ولا يمسّ كلمة مرورها — يحرّك تاريخ الانتهاء وحده.
    if (b.action === "extend") {
      const { data: r0 } = await admin.from("pre_registrations")
        .select("account_email").eq("id", regId).maybeSingle();
      const acct = String(r0?.account_email || "").trim().toLowerCase();
      if (!acct || acct === "__activating__") return json({ error: "not_active" }, 409);
      const expires_at = expiryFor(plan);
      const { error: exErr } = await admin.from("allowed_emails")
        .update({ expires_at }).ilike("email", acct);
      if (exErr) { console.error("extend_failed:", exErr.message); return json({ error: "extend_failed" }, 502); }
      return json({ ok: true, extended: true, email: acct, plan, expires_at });
    }

    const { data: reg0, error: regErr } = await admin.from("pre_registrations")
      .select("id,name,email,stage,account_email").eq("id", regId).maybeSingle();
    if (regErr || !reg0) return json({ error: "reg_not_found" }, 404);
    if (reg0.account_email) return json({ error: "already_active", email: reg0.account_email }, 409);

    // ⚠️ حجزٌ ذرّي قبل أي عمل: كان الفحص أعلاه (قراءة ثم لاحقاً كتابة)
    // يترك نافذةً — نقرتا تفعيلٍ على نفس التسجيل في اللحظة نفسها تريان
    // account_email فارغاً معاً، فتُنشئان حسابَي Auth لبريدٍ واحد، ويفشل
    // الثاني بعد أن استهلك رمز مرورٍ ولّده. عبارةُ UPDATE واحدة يحرسها
    // الشرط داخلها تجعل الحجز فوزاً لطلبٍ واحد فقط — نفس نمط take_quota.
    const claimMark = "__activating__";
    const { data: claimed, error: claimErr } = await admin.from("pre_registrations")
      .update({ account_email: claimMark })
      .eq("id", regId).is("account_email", null)
      .select("id,name,email,stage").maybeSingle();
    if (claimErr) { console.error("server_error:", claimErr.message); return json({ error: "server_error" }, 500); }
    if (!claimed) {
      // لم يُرجَع صفّ = طلبٌ آخر (أو تفعيلٌ سابق) سبقنا إلى الحجز
      const { data: now } = await admin.from("pre_registrations")
        .select("account_email").eq("id", regId).maybeSingle();
      return json({ error: "already_active", email: now?.account_email || null }, 409);
    }
    const reg = claimed;

    // من هنا فصاعداً: أي خروجٍ بخطأ يجب أن يُعيد account_email إلى NULL
    // وإلا بقي الصفّ محجوزاً للأبد بعلامةٍ لا معلّمة تملكها ولا يقبلها
    // فحص البريد — تسجيلٌ ميت لا يستطيع أحدٌ إعادة تفعيله.
    const release = () => admin.from("pre_registrations")
      .update({ account_email: null }).eq("id", regId).then(() => {});

    const email = String(reg.email || "").trim().toLowerCase();
    // بريدها هو اسم دخولها: بريدٌ مولَّد لا تعرفه يعني أنها لا تستطيع
    // استرجاع كلمة مرورها بنفسها أبداً، وكل نسيانٍ يمرّ بالإدارة.
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { await release(); return json({ error: "bad_email" }, 400); }

    const cycle = reg.stage === "cycle1" ? "cycle1" : "main";
    const password = genPassword();

    // email_confirm: البريد معروفٌ منها ومؤكَّدٌ بالدفع، فطلب تأكيدٍ ثانٍ
    // خطوةٌ تُسقِط معلّماتٍ عند أول عقبة.
    const { data: created, error: cErr } = await admin.auth.admin.createUser({
      email, password, email_confirm: true,
    });
    if (cErr || !created?.user) {
      await release();
      const m = String(cErr?.message || "");
      if (/already|exists|registered/i.test(m)) return json({ error: "email_in_use" }, 409);
      return json({ error: "create_failed", detail: m }, 502);
    }

    const expires_at = expiryFor(plan, plan === "trial" ? String(b.trialEndDate || "") : undefined);
    const { error: aErr } = await admin.from("allowed_emails").insert({ email, cycle, expires_at });
    // بلا هذا الصف لا تدخل المعلّمة وإن وُجد حسابها، فنتراجع عن الإنشاء
    // بدل أن نترك حساباً معطّلاً لا تفسير له.
    if (aErr) {
      await admin.auth.admin.deleteUser(created.user.id).catch(() => {});
      await release();
      console.error("allow_failed:", aErr.message);
      return json({ error: "allow_failed" }, 502);
    }

    // ⚠️ لا تُكتب كلمة المرور هنا. كانت تُحفظ نصّاً صريحاً في
    // account_password رغم أنّ 20260711_security_hardening.sql أسقط العمود
    // عمداً — إصلاحٌ نُقض من حيث لا يُدرى. والحفظ لا داعي له أصلاً: الكلمة
    // تصل المعلّمة بالبريد وتُرجَع للمشرف في الردّ، ونسيانُها بابُه
    // reset-teacher-password لا قراءةُ نصٍّ مخزَّن.
    //
    // وفحصُ الخطأ لازم: كتابةٌ إلى عمودٍ محذوف تُفشل العبارة كلَّها، فكان
    // account_email يضيع معها بصمت — والمشرف يرى «فُعِّل» بلا بريدٍ مسجَّل.
    const { error: uErr } = await admin.from("pre_registrations")
      .update({ account_email: email })
      .eq("id", regId);
    if (uErr) console.error("activate-teacher: تعذّر حفظ account_email:", uErr.message);

    const link = cycle === "cycle1" ? "https://khotati.com/cycle1.html" : "https://khotati.com/";
    const mail = await sendMail(
      email,
      plan === "trial" ? "حسابكِ التجريبي في منصّة خُطّة" : "تفعيل حسابكِ في منصّة خُطّة",
      mailHtml(reg.name || "معلّمتنا", email, password, link, plan),
    );
    // نفس ملاحظة وضع الاختبار: كان السبب يظهر للمشرف مرّةً واحدة في المتصفح
    // ثم يضيع — الآن يبقى في سجلّات الدالة لفحصه لاحقاً بلا اعتماد على أن
    // يكون أحدٌ قد رأى الرسالة وقتها أو تذكّر نصّها.
    if (!mail.sent) console.error(`activate-teacher: فشل إرسال بريد التفعيل إلى ${email} (regId=${regId}) — السبب: ${mail.reason}`);

    return json({ ok: true, email, password, plan, expires_at, mailed: mail.sent, mailReason: mail.reason || null });
  } catch (e) {
    console.error("server_error:", String(e));
    return json({ error: "server_error" }, 500);
  }
});
