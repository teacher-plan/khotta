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

function mailHtml(name: string, email: string, password: string, link: string) {
  const esc = (s: string) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));
  return `<!doctype html><html lang="ar" dir="rtl"><body style="margin:0;background:#F3EDE3;font-family:Tahoma,Arial,sans-serif;color:#2A1503">
<div style="max-width:520px;margin:24px auto;background:#FFFDF9;border:1.5px solid #E3D2BD;border-radius:18px;padding:26px">
  <div style="font-size:12px;font-weight:bold;letter-spacing:2px;color:#A83030">منصة خُطّة</div>
  <h1 style="font-size:22px;margin:6px 0 4px">أهلاً ${esc(name)} 👋</h1>
  <p style="font-size:14px;line-height:1.9;color:#7A6A58;margin:0 0 18px">
    فُعِّل حسابكِ في منصّة «خُطّة» للحلقة الأولى. هذه بيانات دخولكِ:</p>
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
    const regId = b.regId;
    if (!regId) return json({ error: "no_reg" }, 400);

    const { data: reg, error: regErr } = await admin.from("pre_registrations")
      .select("id,name,email,stage,account_email").eq("id", regId).maybeSingle();
    if (regErr || !reg) return json({ error: "reg_not_found" }, 404);
    if (reg.account_email) return json({ error: "already_active", email: reg.account_email }, 409);

    const email = String(reg.email || "").trim().toLowerCase();
    // بريدها هو اسم دخولها: بريدٌ مولَّد لا تعرفه يعني أنها لا تستطيع
    // استرجاع كلمة مرورها بنفسها أبداً، وكل نسيانٍ يمرّ بالإدارة.
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json({ error: "bad_email" }, 400);

    const cycle = reg.stage === "cycle1" ? "cycle1" : "main";
    const password = genPassword();

    // email_confirm: البريد معروفٌ منها ومؤكَّدٌ بالدفع، فطلب تأكيدٍ ثانٍ
    // خطوةٌ تُسقِط معلّماتٍ عند أول عقبة.
    const { data: created, error: cErr } = await admin.auth.admin.createUser({
      email, password, email_confirm: true,
    });
    if (cErr || !created?.user) {
      const m = String(cErr?.message || "");
      if (/already|exists|registered/i.test(m)) return json({ error: "email_in_use" }, 409);
      return json({ error: "create_failed", detail: m }, 502);
    }

    const { error: aErr } = await admin.from("allowed_emails").insert({ email, cycle });
    // بلا هذا الصف لا تدخل المعلّمة وإن وُجد حسابها، فنتراجع عن الإنشاء
    // بدل أن نترك حساباً معطّلاً لا تفسير له.
    if (aErr) {
      await admin.auth.admin.deleteUser(created.user.id).catch(() => {});
      return json({ error: "allow_failed", detail: aErr.message }, 502);
    }

    await admin.from("pre_registrations")
      .update({ account_email: email, account_password: password })
      .eq("id", regId);

    const link = cycle === "cycle1" ? "https://khotati.com/cycle1.html" : "https://khotati.com/";
    const mail = await sendMail(email, "تفعيل حسابكِ في منصّة خُطّة", mailHtml(reg.name || "معلّمتنا", email, password, link));

    return json({ ok: true, email, password, mailed: mail.sent, mailReason: mail.reason || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
