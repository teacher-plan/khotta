// وكيلٌ يُشغَّل مرّةً واحدة يدوياً (لا جدولة): يرسل رسالة تذكيرٍ لطيفة لكل
// معلّمةٍ حسابها تجريبي وينتهي خلال يومين، ولم تدخل المنصّة منذ يومين
// فأكثر (أو لم تدخل قط) — دفعةٌ لتفعيل التجربة قبل انتهائها والاستفادة من
// عرض الفصل الكامل بـ١٥ ريالاً.
//
// الحارس: نفس نمط budget-alert-check (service_role فقط)، فيُستدعى إمّا
// يدوياً عبر net.http_post بمفتاح الخدمة من الخزانة أو مستقبلاً بجدولة.
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { isServiceRoleRequest, unauthorized } from "../_shared/adminGuard.ts";

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

function reengageHtml(name: string) {
  const feature = (svgPath: string, title: string, desc: string) => `
    <tr><td style="padding:10px 0;vertical-align:top">
      <table role="presentation" width="100%"><tr>
        <td width="40" style="vertical-align:top">
          <div style="width:32px;height:32px;border-radius:9px;background:#FBF4EA;border:1.5px solid #E3D2BD;
            display:inline-flex;align-items:center;justify-content:center">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#A83030" stroke-width="2"
              stroke-linecap="round" stroke-linejoin="round"><path d="${svgPath}"/></svg>
          </div>
        </td>
        <td style="padding-inline-start:10px">
          <div style="font-size:14px;font-weight:bold;color:#2A1503;margin-bottom:2px">${title}</div>
          <div style="font-size:12.5px;color:#7A6A58;line-height:1.7">${desc}</div>
        </td>
      </tr></table>
    </td></tr>`;

  return `<!doctype html><html lang="ar" dir="rtl"><body style="margin:0;background:#F3EDE3;font-family:Tahoma,Arial,sans-serif;color:#2A1503">
<div style="max-width:560px;margin:24px auto;background:#FFFDF9;border:1.5px solid #E3D2BD;border-radius:18px;padding:28px 26px">

  <div style="font-size:12px;font-weight:bold;letter-spacing:2px;color:#A83030">منصة خُطّة</div>
  <h1 style="font-size:22px;margin:8px 0 6px">تبقّى يومٌ واحدٌ فقط، ${esc(name)} ⏳</h1>
  <p style="font-size:14.5px;line-height:1.95;color:#7A6A58;margin:0 0 18px">
    لاحظنا أنّكِ لم تدخلي حسابكِ التجريبي في «خُطّة» منذ فترة، وتجربتكِ المجانية على وشك الانتهاء غداً.
    قبل أن تفوتكِ، أحببنا تذكيركِ بما تحصلين عليه، وبعرضٍ لا يتكرر لبداية الفصل.</p>

  <div style="background:#FBF4EA;border:1.5px solid #E3D2BD;border-radius:14px;padding:18px 16px;margin-bottom:20px;text-align:center">
    <div style="font-size:13px;color:#7A6A58;margin-bottom:4px">عرض بداية العام الدراسي</div>
    <div style="font-size:26px;font-weight:bold;color:#A83030">١٥ ريالاً فقط <span style="font-size:14px;font-weight:normal;color:#7A6A58">للفصل الدراسي كاملاً</span></div>
  </div>

  <p style="font-size:14.5px;font-weight:bold;color:#2A1503;margin:0 0 4px">احصلي على:</p>
  <table role="presentation" width="100%" style="margin-bottom:8px">
    ${feature("M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z",
      "تحاضير الحلقة الأولى بمطابقة منصّة نور",
      "توليد تحضيرٍ كاملٍ من دليل المعلم وكتاب الطالب معاً بالذكاء الاصطناعي، على نفس الهيكل المعتمد رسمياً في منصّة نور — تنسخينه مباشرةً بلا إعادة صياغة.")}
    ${feature("M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z",
      "تحضير الدروس من الكتاب مباشرة",
      "خطط دروسٍ جاهزة، وبطاقات وأنشطة وانفوجرافيك تُولَّد من صفحات الكتاب نفسها في دقائق.")}
    ${feature("M3 3v18h18M7 15l4-4 4 4 5-6",
      "متابعة الطالبات بالنجوم والسجلّ",
      "رصدُ سلوك كل طالبةٍ وتحصيلها بلمسةٍ واحدة، مع لوحة صدارةٍ تحفّزهنّ تلقائياً.")}
    ${feature("M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 19.5A2.5 2.5 0 0 0 6.5 22H20V2H6.5A2.5 2.5 0 0 0 4 4.5v15z",
      "٣٠ نشاط احتياطٍ جاهزاً بلا إنترنت",
      "لحصص الانتظار أو انقطاع الشبكة — نشاطٌ مناسبٌ لكل موقف، جاهزٌ فوراً.")}
    ${feature("M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM4.2 12a7.8 7.8 0 0 1 .4-2.4l-1.7-1.3 1.5-2.6 2 .6a8 8 0 0 1 2-1.2l.3-2.1h3l.3 2.1a8 8 0 0 1 2 1.2l2-.6 1.5 2.6-1.7 1.3a7.8 7.8 0 0 1 0 4.8l1.7 1.3-1.5 2.6-2-.6a8 8 0 0 1-2 1.2l-.3 2.1h-3l-.3-2.1a8 8 0 0 1-2-1.2l-2 .6-1.5-2.6 1.7-1.3a7.8 7.8 0 0 1-.4-2.4z",
      "شهاداتٌ تلقائية",
      "شهادات تفوّقٍ وتميّزٍ تُصمَّم وتُصدَر تلقائياً من بيانات كل طالبة.")}
    ${feature("M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 5h-2v6l4.2 2.5 1-1.6-3.2-1.9V7z",
      "خُطّة AI — مرشدكِ التربوي",
      "استشيريها في أي موقفٍ صفّي أو إداري، وهي تعرف صفوفكِ وطالباتكِ فعلياً.")}
  </table>

  <a href="https://khotati.com/cycle1.html" style="display:block;text-align:center;background:#C9453B;color:#fff;text-decoration:none;
     font-weight:bold;font-size:15.5px;padding:14px;border-radius:12px;margin-top:6px">ادخلي إلى حسابكِ الآن</a>

  <p style="font-size:12px;line-height:1.9;color:#7A6A58;margin:18px 0 0;text-align:center">
    استغلّي العرض قبل انتهاء التجربة غداً — وإن واجهتكِ أي صعوبةٍ في الدخول، راسلينا وسنساعدكِ فوراً. 🌸</p>
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

  try {
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);

    const { data: allowed, error: aErr } = await admin
      .from("allowed_emails")
      .select("email")
      .not("expires_at", "is", null)
      .gt("expires_at", new Date().toISOString())
      .lte("expires_at", new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString());
    if (aErr) return json({ error: "query_failed", detail: aErr.message }, 500);
    if (!allowed || !allowed.length) return json({ ok: true, sent: 0, skipped: 0, failed: 0, note: "no_trial_accounts_expiring_soon" });

    // نجلب المستخدمين دفعةً واحدة (auth.admin.listUsers) لأن auth.users غير
    // متاحٍ عبر PostgREST مباشرةً؛ ٥٠ صفحةً كافيةٌ لحجم القاعدة الحالي.
    const emailSet = new Set(allowed.map((a) => (a.email || "").toLowerCase()));
    const usersByEmail = new Map<string, { last_sign_in_at: string | null; id: string }>();
    let page = 1;
    while (true) {
      const { data, error } = await admin.auth.admin.listUsers({ page, perPage: 200 });
      if (error) return json({ error: "list_users_failed", detail: error.message }, 500);
      for (const u of data.users) {
        if (u.email) usersByEmail.set(u.email.toLowerCase(), { last_sign_in_at: u.last_sign_in_at || null, id: u.id });
      }
      if (data.users.length < 200) break;
      page++;
      if (page > 20) break; // حارس صلابة، لن يُبلَغ فعلياً بهذا الحجم
    }

    const { data: profs } = await admin.from("cycle1_profiles").select("id,data");
    const nameById = new Map<string, string>();
    (profs || []).forEach((p: { id: string; data?: { display_name?: string } }) => {
      if (p.data?.display_name) nameById.set(p.id, p.data.display_name);
    });

    // ما أُرسل بنجاحٍ من قبل لا يُعاد — الجدول هو ضمان عدم التكرار عند أي
    // إعادة نداءٍ (شبكةٌ منقطعة، تحقّقٌ يدوي، إلخ).
    const { data: already } = await admin.from("trial_reengagement_log").select("email,status");
    const alreadySent = new Set((already || []).filter((r: { status: string }) => r.status === "sent").map((r: { email: string }) => r.email.toLowerCase()));
    const skipped = alreadySent.size;

    const twoDaysAgo = Date.now() - 2 * 24 * 60 * 60 * 1000;
    const targets: { email: string; name: string }[] = [];
    for (const email of emailSet) {
      if (alreadySent.has(email)) continue;
      const u = usersByEmail.get(email);
      const lastMs = u?.last_sign_in_at ? new Date(u.last_sign_in_at).getTime() : null;
      const inactive = !u || lastMs === null || lastMs < twoDaysAgo;
      if (inactive) {
        const name = (u && nameById.get(u.id)) || "معلّمتنا الفاضلة";
        targets.push({ email, name });
      }
    }

    // ⚠️ الإرسال الفعلي يستمر في الخلفية عبر waitUntil لا في الطلب نفسه:
    // ٢٧ نداء Resend متتابعاً قد يتجاوز مهلة تنفيذ الدالّة، فينقطع الاتصال
    // قبل أي ردٍّ — وهذا فعلياً ما حدث (net._http_response لم تحمل صفاً
    // إطلاقاً رغم محاولتين، وtrial_reengagement_log بقي فارغاً كلياً).
    // الردّ الآن فوريٌّ بعدد المستهدَفات؛ التقدّم الفعلي يُتابَع من الجدول.
    const sendAll = async () => {
      let sent = 0, failed = 0;
      const failures: string[] = [];
      for (const t of targets) {
        const r = await sendMail(t.email, "يومٌ واحدٌ يفصلكِ عن نهاية تجربتكِ في «خُطّة» 🌸", reengageHtml(t.name));
        await admin.from("trial_reengagement_log").upsert({
          email: t.email, status: r.sent ? "sent" : "failed", reason: r.reason || null, sent_at: new Date().toISOString(),
        });
        if (r.sent) sent++;
        else { failed++; failures.push(`${t.email}: ${r.reason}`); }
      }
      console.log(`trial-reengagement-email: sent=${sent} failed=${failed} skipped_already_sent=${skipped} total_targets=${targets.length}`);
      if (failures.length) console.error("trial-reengagement-email failures:\n" + failures.join("\n"));
    };

    // deno-lint-ignore no-explicit-any
    const rt = (globalThis as any).EdgeRuntime;
    if (rt && typeof rt.waitUntil === "function") {
      rt.waitUntil(sendAll());
    } else {
      // بيئة اختبارٍ محلية بلا EdgeRuntime — ننفّذ مباشرةً بلا خلفية.
      await sendAll();
    }

    return json({ ok: true, started: true, skipped_already_sent: skipped, total_targets: targets.length });
  } catch (e) {
    console.error("trial-reengagement-email server_error:", String(e));
    return json({ error: "server_error", detail: String(e).slice(0, 300) }, 500);
  }
});
