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
    const periodStart = st["budget_period_start"] || "2026-01-01";

    // من أنفقت شيئاً خلال هذه الفترة (بلا هذا القيد نجمع كل معلّمةٍ سجّلت
    // منذ إنشاء الحساب حتى لو صفراً — نداءٌ بلا فائدة).
    const { data: costRows, error: cErr } = await sb
      .from("ai_cost_log")
      .select("user_id, cost_usd")
      .gte("created_at", periodStart + "T00:00:00Z")
      .not("user_id", "is", null);
    if (cErr) throw cErr;

    const usedByUser = new Map<string, number>();
    (costRows || []).forEach((r: { user_id: string; cost_usd: number | null }) => {
      usedByUser.set(r.user_id, (usedByUser.get(r.user_id) || 0) + (r.cost_usd || 0));
    });

    const crossed = [...usedByUser.entries()].filter(([, used]) => used / budgetUsd >= 0.8);
    if (crossed.length === 0) {
      await finishRun(sb, run, { status: "SUCCESS", resultSummary: "لا معلّمة تجاوزت ٨٠٪", recordsRead: usedByUser.size });
      return json({ ok: true, checked: usedByUser.size, alerted: 0 });
    }

    // من أُرسل لها التنبيه فعلاً في هذه الفترة تحديداً
    const { data: alertRows } = await sb
      .from("budget_alerts")
      .select("user_id, period_start, alert_80_sent_at")
      .in("user_id", crossed.map(([uid]) => uid));
    const already = new Map<string, string>();
    (alertRows || []).forEach((r: { user_id: string; period_start: string; alert_80_sent_at: string | null }) => {
      if (r.period_start === periodStart && r.alert_80_sent_at) already.set(r.user_id, r.alert_80_sent_at);
    });

    const toNotify = crossed.filter(([uid]) => !already.has(uid));
    let sentCount = 0;
    for (const [uid, used] of toNotify) {
      const { data: prof } = await sb.from("cycle1_profiles").select("id, email, data").eq("id", uid).maybeSingle();
      if (!prof?.email) continue;
      const name = (prof.data?.display_name as string) || "معلّمتنا";
      const pct = Math.min(100, Math.round((used / budgetUsd) * 100));
      const r = await sendMail(prof.email, "تنبيهٌ لطيف بشأن رصيد الذكاء الاصطناعي 🌙", alertHtml(name, pct));
      await sb.from("budget_alerts").upsert({
        user_id: uid, period_start: periodStart,
        alert_80_sent_at: r.sent ? new Date().toISOString() : null,
        updated_at: new Date().toISOString(),
      });
      if (r.sent) sentCount++;
      else console.error(`budget-alert-check: تعذّر إرسال البريد لـ${uid}:`, r.reason);
    }

    await finishRun(sb, run, {
      status: "SUCCESS",
      resultSummary: `${sentCount} بريدٍ أُرسل من أصل ${toNotify.length} تجاوزت ٨٠٪`,
      recordsRead: usedByUser.size, recordsWritten: sentCount,
    });
    return json({ ok: true, checked: usedByUser.size, crossed: crossed.length, alerted: sentCount });
  } catch (error) {
    console.error("❌ budget-alert-check:", error);
    await finishRun(sb, run, { status: "FAILED", error: String(error) });
    return json({ error: String(error) }, 500);
  }
});
