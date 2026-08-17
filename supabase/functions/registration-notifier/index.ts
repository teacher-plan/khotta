// v2026.08.13 ════════════════════════════════════════════════════════════════
// وكيل تنبيه التسجيلات (Registration Notifier Agent)
// يرسل رسالة تلغرام فور حجز معلّمة مقعدها في صفحة ترويج الحلقة الأولى.
//
// يعمل بمسلكين، وكلاهما يمرّ بالعلامة نفسها فلا يزدوج الإرسال:
//  ١ خطّاف قاعدة البيانات (Database Webhook) على INSERT — الطريق الفوري.
//  ٢ مسحٌ احتياطيّ بلا حمولة — يلتقط ما فات الخطّاف حين يتعطّل أو يُبطئ.
// الاعتماد على الخطّاف وحده يعني أن عطلاً عابراً يُسقط حجزاً بلا أن يُلحظ،
// وعلى المسح وحده يعني تأخّراً بمقدار دورة المسح. فبهما معاً: فوريٌّ ومضمون.
//
// النشر: تلقائي عبر GitHub Actions
// الأسرار: TELEGRAM_BOT_TOKEN و TELEGRAM_CHAT_ID
// يتطلّب: 20260813_registration_notifier.sql (عمود notified_at)
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendTelegram } from "../_shared/telegram.ts";
import { startRun, finishRun } from "../_shared/agentRun.ts";

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

// Telegram بوضع HTML يفسّر < و > و & وسوماً — واسمٌ فيه «&» يكسر الرسالة
// كاملةً برفض 400، فلا تصل إطلاقاً ولا يظهر خطأ في الواجهة. كل نصٍّ آتٍ من
// نموذج التسجيل يُهرَّب: الاسم والبريد والهاتف وكود الإحالة.
function escHtml(s: string): string {
  return String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// مسقط على UTC+4 بلا توقيت صيفي، فالإزاحة ثابتة ولا تحتاج مكتبة مناطق.
function muscatTime(iso: string): string {
  const d = new Date(new Date(iso).getTime() + 4 * 3600 * 1000);
  const hh = String(d.getUTCHours()).padStart(2, "0");
  const mm = String(d.getUTCMinutes()).padStart(2, "0");
  return `${hh}:${mm}`;
}

interface Reg {
  id?: string | number;
  name?: string;
  phone?: string;
  email?: string;
  stage?: string;
  referred_by?: string | null;
  created_at?: string;
}

// wa.me يريد الرقم دوليّاً بلا رموز ولا بادئة «00». صفحة الحجز تُطبّع الرقم
// إلى ثمانية أرقام محليّة، لكن لوحة الإدارة تُدخل حجوزاتٍ يدويّاً بمسارٍ لا
// يُطبّع — فنُكرّر التطبيع هنا بدل افتراض صيغةٍ واحدة تُنتج رابطاً معطّلاً.
function waLink(phone: string): string {
  let d = String(phone || "").replace(/\D/g, "");
  if (d.startsWith("00")) d = d.slice(2);
  if (!d) return "";
  return `https://wa.me/${d.length === 8 ? "968" + d : d}`;
}

// رسالة الترحيب — نصّها نفسه المستعمل في لوحة الإدارة، فلا تختلف صياغتان
// لمعلّمتين حسب المكان الذي أُرسلت منه.
function welcomeText(name: string): string {
  const n = String(name || "").trim();
  return [
    n ? `أهلاً بكِ ${n} 🌸` : "أهلاً بكِ 🌸",
    "",
    "وصلَنا حجزُ مقعدكِ في منصّة «خُطّتي الفصلية» — الحلقة الأولى، وسعدنا بانضمامكِ.",
    "",
    "سنتواصل معكِ لتفعيل اشتراككِ مع بداية أول أسبوع دوام بإذن الله، ويصلكِ حسابُكِ جاهزاً.",
    "",
    "وإلى ذلك الحين، أيُّ استفسارٍ يخطر لكِ فاكتبيه هنا — نجيبكِ بسرور 🌷",
  ].join("\n");
}

function buildMessage(r: Reg, rank: number | null): string {
  const name = escHtml(r.name || "بلا اسم");
  const phone = escHtml(r.phone || "—");
  const email = escHtml(r.email || "—");
  const wa = waLink(r.phone || "");
  const when = r.created_at ? muscatTime(r.created_at) : "";

  const lines = [
    "🎉 <b>حجز جديد — الحلقة الأولى</b>",
    "",
    `👩‍🏫 <b>${name}</b>`,
    wa ? `📱 <a href="${wa}">${phone}</a>` : `📱 ${phone}`,
    `✉️ ${email}`,
  ];
  // كود الإحالة يظهر فقط إن وُجد: سطرٌ فارغ «الإحالة: —» في كل رسالة يزيد
  // طولها بلا فائدة، والرسائل تُقرأ على الهاتف.
  if (r.referred_by) lines.push(`🔗 إحالة: <code>${escHtml(r.referred_by)}</code>`);
  lines.push("");
  const tail = [when ? `🕐 ${when} (مسقط)` : "", rank ? `📊 التسجيل رقم ${rank}` : ""]
    .filter(Boolean).join("  ·  ");
  if (tail) lines.push(tail);

  // زرُّ الترحيب: يفتح واتساب والرسالةُ مكتوبةٌ فيه، فلا يبقى إلا الإرسال.
  // البوت لا يستطيع مراسلة المعلّمة بنفسه — تلغرام يمنع البوتات من بدء
  // محادثةٍ مع من لم يبدأها، ولا يعرفها برقم هاتفها. فأقصرُ طريقٍ ممكن:
  // يصلك الإشعار وأنت في أي مكان، فتضغط ضغطةً واحدة وتُرسل الترحيب فوراً
  // بدل أن تنتظر حتى تفتح لوحة الإدارة على الحاسوب.
  if (wa) {
    lines.push("");
    lines.push(`<a href="${wa}?text=${encodeURIComponent(welcomeText(r.name || ""))}">🌸 إرسال الترحيب</a>`);
  }

  return lines.join("\n");
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  const started = Date.now();
  const svc = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
  const sb = createClient(Deno.env.get("SUPABASE_URL")!, svc);

  // 🔒 حارس: الوكيل يكتب في تلغرامك مباشرةً، فمسلكٌ مفتوح يعني أن أي أحدٍ
  // يستطيع إغراقك بحجوزاتٍ ملفّقة.
  //
  // لا نطابق نصّ المفتاح: المشروع يملك صيغتين لصلاحية الخدمة نفسها — الـJWT
  // القديم و«sb_secret_…» الجديد — والمُشغِّل يرسل ما في الخزانة بينما البيئة
  // تحقن الأخرى، فتفشل المطابقة النصّية على مفتاحين صحيحين كليهما. نتحقّق من
  // الصلاحية لا من الحروف: أي حاملٍ دورُه service_role يُقبل.
  const auth = (req.headers.get("Authorization") || "").replace("Bearer ", "").trim();
  const isServiceRole = auth === svc || (() => {
    try {
      const [, payload] = auth.split(".");
      return JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/"))).role === "service_role";
    } catch { return false; }
  })();
  if (!auth || !isServiceRole) return json({ error: "unauthorized" }, 401);

  // Phase 1.5: DB_WEBHOOK إن حملت حمولةً (record لاحقاً)، وإلا مسحٌ احتياطي
  // (ON_DEMAND/CRON خارجي — لا جدولة pg_cron مؤكَّدة له، انظر التقرير).
  let run = { runId: null as string | null, correlationId: null as string | null, startedAt: Date.now() };

  try {
    const body = await req.json().catch(() => ({}));
    // حمولة خطّاف Supabase: { type, table, record }. غيابها = مسحٌ احتياطيّ.
    const hooked: Reg | null = body?.record ?? null;
    run = await startRun(sb, "registration-notifier", hooked ? "WEBHOOK" : "ON_DEMAND");

    let rows: Reg[] = [];
    if (hooked && hooked.id != null) {
      // نقرأ الصف من الجدول لا من الحمولة: الحمولة نصٌّ يصل من الخارج، وقراءةُ
      // المصدر تضمن أننا لا نُرسل عن حجزٍ لا وجود له، وتُظهر notified_at الحقيقي.
      const { data } = await sb.from("pre_registrations")
        .select("id,name,phone,email,stage,referred_by,created_at,notified_at")
        .eq("id", hooked.id).maybeSingle();
      if (data && data.stage === "cycle1" && !data.notified_at) rows = [data];
    } else {
      // المسح الاحتياطيّ: الأقدم أولاً ليصل ترتيب الرسائل كترتيب الحجوزات.
      // وسقفٌ خمسون يمنع سيلاً يُغرق المحادثة لو تعطّل الخطّاف طويلاً.
      const { data } = await sb.from("pre_registrations")
        .select("id,name,phone,email,stage,referred_by,created_at")
        .eq("stage", "cycle1").is("notified_at", null)
        .order("created_at", { ascending: true }).limit(50);
      rows = data || [];
    }

    if (!rows.length) return json({ ok: true, sent: 0 });

    // الترتيب الكلّي لكل حجز — رقمٌ يُطمئن أثناء حملة الترويج.
    const { count: total } = await sb.from("pre_registrations")
      .select("id", { count: "exact", head: true }).eq("stage", "cycle1");
    const base = (total || rows.length) - rows.length;

    let sent = 0;
    const failed: string[] = [];
    for (let i = 0; i < rows.length; i++) {
      const r = rows[i];
      const result = await sendTelegram(buildMessage(r, base + i + 1));
      if (!result.ok) { failed.push(String(r.id)); continue; }
      sent++;
      // العلامة تُوضع بعد نجاح الإرسال وحده: وضعُها قبله يُسقط الحجز نهائياً
      // لو فشل تلغرام، فلا المسح يلتقطه ولا أنتِ تعلمين به.
      await sb.from("pre_registrations")
        .update({ notified_at: new Date().toISOString() }).eq("id", r.id);
      await sb.from("agent_messages").insert({
        message_id: `reg-${r.id}-${Date.now()}`,
        agent_name: "registration-notifier",
        message_text: `حجز جديد: ${r.name || r.id}`,
        telegram_message_id: result.message_id,
      });
    }

    await sb.from("agent_schedules")
      .update({ last_run: new Date().toISOString() })
      .eq("agent_name", "registration-notifier");

    await sb.from("agent_logs").insert({
      agent_name: "registration-notifier",
      action: hooked ? "webhook" : "sweep",
      status: failed.length ? "error" : "success",
      error_message: failed.length ? `تعذّر الإرسال عن: ${failed.join(", ")}` : null,
      execution_time_ms: Date.now() - started,
      data_collected: { sent, failed: failed.length, total: total ?? null },
    });

    await finishRun(sb, run, {
      status: failed.length ? "PARTIAL" : "SUCCESS",
      resultSummary: `أُرسل ${sent}، فشل ${failed.length}`,
      error: failed.length ? `تعذّر الإرسال عن: ${failed.join(", ")}` : undefined,
      recordsRead: rows.length,
      recordsWritten: sent,
    });

    return json({ ok: true, sent, failed: failed.length });
  } catch (error) {
    console.error("❌ registration-notifier:", error);
    await sb.from("agent_logs").insert({
      agent_name: "registration-notifier",
      action: "error",
      status: "error",
      error_message: String(error),
      execution_time_ms: Date.now() - started,
    }).then(() => {}, () => {});
    await finishRun(sb, run, { status: "FAILED", error: String(error) });
    return json({ error: String(error) }, 500);
  }
});
