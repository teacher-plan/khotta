// وكيل تنبيه تجاوز ٨٠٪ من حصّة الذكاء الاصطناعي الفصلية — يُجدوَل كل ٦
// ساعات (نمط credit-monitor)، ويُرسل بريداً لطيفاً لكل معلّمةٍ عبرت ٨٠٪
// من budget_omr لأوّل مرّةٍ هذا الفصل (budget_period_start) — مرّةً واحدة
// فقط لكل فترة، عبر budget_alerts.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { isServiceRoleRequest, unauthorized } from "../_shared/adminGuard.ts";
import { startRun, finishRun } from "../_shared/agentRun.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
}
function esc(s: string) {
  return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));
}

// نفس قالب رسائل المنصّة الحقيقي (activate-teacher/index.ts) — لا قالبٌ جديد.
function alertHtml(name: string, pct: number) {
  return `<!doctype html><html lang="ar" dir="rtl"><body style="margin:0;background:#F3EDE3;font-family:Tahoma,Arial,sans-serif;color:#2A1503">
<div style="max-width:520px;margin:24px auto;background:#FFFDF9;border:1.5px solid #E3D2BD;border-radius:18px;padding:26px">
  <div style="font-size:12px;font-weight:bold;letter-spacing:2px;color:#A83030">منصة خُطّة</div>
  <h1 style="font-size:22px;margin:6px 0 4px">مرحباً بكِ ${esc(name)} 🌸</h1>
  <p style="font-size:14px;line-height:1.9;color:#7A6A58;margin:0 0 18px">
    نودّ إعلامكِ بأنكِ استخدمتِ <b style="color:#2A1503">${pct}٪</b> من حصّة الذكاء الاصطناعي المخصّصة لكِ لهذا الفصل الدراسي في منصّة خُطّتي الفصلية.</p>
  <div style="background:#FBF4EA;border:1.5px solid #E3D2BD;border-radius:12px;padding:14px;margin-bottom:16px">
    <div style="font-size:12px;color:#7A6A58;margin-bottom:6px">رصيدكِ المستهلَك</div>
    <div style="background:#E3D2BD;border-radius:8px;height:10px;overflow:hidden">
      <div style="background:#C9453B;height:100%;width:${pct}%"></div>
    </div>
    <div style="font-size:12px;color:#7A6A58;margin-top:8px">${pct}٪ مُستهلَك</div>
  </div>
  <p style="font-size:14px;line-height:1.9;color:#7A6A58;margin:0 0 18px">
    نُقدّر حقّاً حماسكِ في الاستفادة من أدوات التحضير والألعاب والانفوجرافيك — هذا بالضبط ما صُمّمت من أجله المنصّة!<br><br>
    نُذكّركِ فقط حتى تكون الصورة واضحةً أمامك، ولا داعي لأي قلق: يمكنكِ الاستمرار في الاستخدام بشكل طبيعي، وفي حال وصل رصيدكِ للحدّ الأقصى سيصلكِ إشعارٌ آخر بذلك.</p>
  <a href="https://khotati.com/cycle1.html" style="display:block;text-align:center;background:#C9453B;color:#fff;text-decoration:none;
     font-weight:bold;font-size:15px;padding:13px;border-radius:12px">متابعة رصيدي</a>
  <p style="font-size:12px;line-height:1.9;color:#7A6A58;margin:16px 0 0">
    يمكنكِ متابعة رصيدكِ في أي وقت من أعلى الصفحة، بجانب أيقونة حسابكِ.</p>
</div></body></html>`;
}

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
    if (!r.ok) return { sent: false, reason: (await r.text()).slice(0, 200) };
    return { sent: true };
  } catch (e) {
    return { sent: false, reason: String(e).slice(0, 200) };
  }
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (!isServiceRoleRequest(req)) return unauthorized(cors);

  const sb = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  let run = { runId: null as string | null, correlationId: null as string | null, startedAt: Date.now() };

  try {
    run = await startRun(sb, "budget-alert-check", "CRON");

    const { data: settingsRows, error: sErr } = await sb.from("ai_settings").select("key, value");
    if (sErr) throw sErr;
    const st: Record<string, string> = {};
    (settingsRows || []).forEach((r: { key: string; value: string }) => (st[r.key] = r.value));

    const budgetOmr = parseFloat(st["budget_omr"] || "") || 13;
    const rate = parseFloat(st["usd_omr_rate"] || "") || 0.3845;
    const budgetUsd = budgetOmr / rate;
    const fallbackPeriod = st["budget_period_start"] || "2026-01-01";

    // كلّ التكلفة المسجَّلة لكل معلّمة — الفترة الآن لكل حسابٍ على حدة
    // (تفعيله الخاص)، لا تاريخاً عامّاً واحداً يُصفّى به الاستعلام هنا.
    // الجدول جديدٌ (منذ ١٦ أغسطس) فحجمه صغيرٌ بما يكفي لجلبه كاملاً.
    const { data: costRows, error: cErr } = await sb
      .from("ai_cost_log")
      .select("user_id, cost_usd, created_at")
      .not("user_id", "is", null);
    if (cErr) throw cErr;

    const rowsByUser = new Map<string, { cost: number; at: string }[]>();
    (costRows || []).forEach((r: { user_id: string; cost_usd: number | null; created_at: string }) => {
      const arr = rowsByUser.get(r.user_id) || [];
      arr.push({ cost: r.cost_usd || 0, at: r.created_at });
      rowsByUser.set(r.user_id, arr);
    });

    const uids = [...rowsByUser.keys()];
    const { data: teacherRows } = await sb.from("cycle1_profiles").select("id, email, data").in("id", uids);
    const teacherById = new Map<string, { email: string; name: string | null }>();
    (teacherRows || []).forEach((t: { id: string; email: string; data: Record<string, unknown> | null }) => {
      teacherById.set(t.id, { email: t.email, name: (t.data?.display_name as string) || null });
    });

    const emails = [...new Set([...teacherById.values()].map((t) => t.email.toLowerCase()))];
    const { data: accRows } = await sb.from("allowed_emails").select("email, added_at").in("email", emails);
    const addedAtByEmail = new Map<string, string>();
    (accRows || []).forEach((a: { email: string; added_at: string }) => addedAtByEmail.set(a.email.toLowerCase(), a.added_at));

    // تفعيل حساب كل معلّمة تحديداً — لا تاريخٌ عامّ واحد (انظر
    // 20260819_p30_budget_per_account_period.sql لنفس المنطق في get_my_ai_budget).
    const crossed: [string, number, string][] = []; // [uid, used, periodStart]
    for (const [uid, rows] of rowsByUser) {
      const t = teacherById.get(uid);
      if (!t?.email) continue;
      const periodStart = (addedAtByEmail.get(t.email.toLowerCase()) || fallbackPeriod).slice(0, 10);
      const used = rows.filter((r) => r.at >= periodStart).reduce((s, r) => s + r.cost, 0);
      if (used / budgetUsd >= 0.8) crossed.push([uid, used, periodStart]);
    }

    if (crossed.length === 0) {
      await finishRun(sb, run, { status: "SUCCESS", resultSummary: "لا معلّمة تجاوزت ٨٠٪", recordsRead: rowsByUser.size });
      return json({ ok: true, checked: rowsByUser.size, alerted: 0 });
    }

    // من أُرسل لها التنبيه فعلاً في فترتها الحالية تحديداً (لو أُعيد تفعيل
    // حسابها لاحقاً بتاريخٍ جديد، هذا يُعامَل فترةً جديدة تستحقّ تنبيهاً جديداً)
    const { data: alertRows } = await sb
      .from("budget_alerts")
      .select("user_id, period_start, alert_80_sent_at")
      .in("user_id", crossed.map(([uid]) => uid));
    const already = new Map<string, string>();
    (alertRows || []).forEach((r: { user_id: string; period_start: string; alert_80_sent_at: string | null }) => {
      if (r.alert_80_sent_at) already.set(r.user_id + "|" + r.period_start, r.alert_80_sent_at);
    });

    const toNotify = crossed.filter(([uid, , ps]) => !already.has(uid + "|" + ps));
    let sentCount = 0;
    for (const [uid, used, ps] of toNotify) {
      const t = teacherById.get(uid);
      if (!t?.email) continue;
      const name = t.name || "معلّمتنا";
      const pct = Math.min(100, Math.round((used / budgetUsd) * 100));
      const r = await sendMail(t.email, "تنبيهٌ لطيف بشأن رصيد الذكاء الاصطناعي 🌙", alertHtml(name, pct));
      await sb.from("budget_alerts").upsert({
        user_id: uid, period_start: ps,
        alert_80_sent_at: r.sent ? new Date().toISOString() : null,
        updated_at: new Date().toISOString(),
      });
      if (r.sent) sentCount++;
      else console.error(`budget-alert-check: تعذّر إرسال البريد لـ${uid}:`, r.reason);
    }

    await finishRun(sb, run, {
      status: "SUCCESS",
      resultSummary: `${sentCount} بريدٍ أُرسل من أصل ${toNotify.length} تجاوزت ٨٠٪`,
      recordsRead: rowsByUser.size, recordsWritten: sentCount,
    });
    return json({ ok: true, checked: rowsByUser.size, crossed: crossed.length, alerted: sentCount });
  } catch (error) {
    console.error("❌ budget-alert-check:", error);
    await finishRun(sb, run, { status: "FAILED", error: String(error) });
    return json({ error: String(error) }, 500);
  }
});
