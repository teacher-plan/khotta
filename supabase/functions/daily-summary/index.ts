// الملخص اليومي المركزي (Daily Summary)
// يجمع بيانات جميع الوكلاء ويرسل رسالة واحدة شاملة

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendTelegramOps as sendTelegram } from "../_shared/telegram.ts";
import { isServiceRoleRequest, unauthorized } from "../_shared/adminGuard.ts";
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

async function getCreditSummary(sb: any): Promise<string> {
  try {
    const month = new Date().toISOString().slice(0, 7);
    const { data: settingsRows } = await sb.from("ai_settings").select("key, value");
    const settings: Record<string, string> = {};
    settingsRows?.forEach((r: { key: string; value: string }) => (settings[r.key] = r.value));
    const limits: Record<string, number> = {
      text: parseInt(settings.quota_text || "") || 300,
      img: parseInt(settings.quota_img || "") || 200,
      search: parseInt(settings.quota_search || "") || 20,
    };

    const { data: usageRows } = await sb
      .from("ai_usage")
      .select("user_id, kind, count")
      .eq("month", month);

    if (!usageRows) return "💰 <b>الرصيد:</b> لا بيانات متوفرة";

    let critical = 0, warning = 0;
    usageRows.forEach((r: { kind: string; count: number }) => {
      const limit = limits[r.kind];
      if (!limit) return;
      const percentage = (r.count / limit) * 100;
      if (percentage > 80) critical++;
      else if (percentage > 50) warning++;
    });

    return `💰 <b>الرصيد:</b> ${critical} حرجة، ${warning} تحذير`;
  } catch (error) {
    return `💰 <b>الرصيد:</b> ❌ خطأ (${error})`;
  }
}

async function getLibrarySummary(sb: any): Promise<string> {
  try {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const { data: files } = await sb
      .from("c1_library_items")
      .select("id, created_at")
      .gte("created_at", today.toISOString());

    if (!files) return "📚 <b>المكتبة:</b> لا بيانات متوفرة";

    const totalFiles = files.length;
    return `📚 <b>المكتبة:</b> ${totalFiles} ملف جديد اليوم`;
  } catch (error) {
    return `📚 <b>المكتبة:</b> ❌ خطأ`;
  }
}

// Phase 1.5 — تدقيق ثقة: هذه الدالّة كانت تُعيد نصّاً ثابتاً مختلَقاً
// ("3-4 مساءً") لا صلة له بأي استعلامٍ حقيقي. لا مصدر بيانات فعلي لأوقات
// الذروة في المشروع اليوم (لا عمود توقيت استخدامٍ مجمَّع بالساعة) — بدل
// اختلاق رقمٍ نُزيل الادّعاء ونصرّح بعدم توفّر البيانات، حرفياً كما طلبت
// المواصفة (القسم 4): "البيانات غير متوفرة حالياً" لا بديلاً مُختلَقاً.
async function getPeakHoursSummary(_sb: any): Promise<string> {
  return `📈 <b>أوقات الذروة:</b> البيانات غير متوفرة حالياً (لا مصدر بياناتٍ حقيقي لهذا المؤشر بعد)`;
}

// avgScore كانت رقماً ثابتاً (4.2) لا صلة له باستبيانات user_surveys
// الفعلية رغم أن الجدول يحمل عمود responses الذي تُخزَّن فيه التقييمات
// (انظر telegram-webhook: "responses": {"rating": N}). حُسب المتوسط الآن
// من نفس الصفوف المقروءة فعلاً، لا رقمٍ مُختلَق.
async function getFeedbackSummary(sb: any): Promise<string> {
  try {
    const { data: surveys } = await sb
      .from("user_surveys")
      .select("responses")
      .gt("created_at", new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString());

    const count = surveys?.length || 0;
    if (!count) return `📋 <b>الآراء:</b> لا استجابات هذا الأسبوع`;

    const ratings = (surveys || [])
      .map((s: { responses?: { rating?: number } }) => s.responses?.rating)
      .filter((r: unknown): r is number => typeof r === "number" && r >= 1 && r <= 5);

    if (!ratings.length) {
      return `📋 <b>الآراء:</b> ${count} استجابة هذا الأسبوع | الرضا: البيانات غير متوفرة حالياً (لا تقييم رقمي في الاستجابات)`;
    }
    const avg = ratings.reduce((a: number, b: number) => a + b, 0) / ratings.length;
    return `📋 <b>الآراء:</b> ${count} استجابة هذا الأسبوع | الرضا: ${avg.toFixed(1)}/5 ⭐ (من ${ratings.length} تقييماً رقمياً)`;
  } catch (error) {
    return `📋 <b>الآراء:</b> ❌ خطأ`;
  }
}

// لا مصدر بيانات "تحليلات" حقيقي وراء هذا القسم اليوم (لا جدول/RPC
// تحليلاتٍ مجمَّعة) — كانت تُعيد نصّاً ثابتاً بلا استعلامٍ إطلاقاً.
// إزالة الادّعاء بدل اختلاق بديل، تطبيقاً حرفياً لقاعدة القسم 4.
async function getAnalyticsSummary(_sb: any): Promise<string> {
  return `🤖 <b>التحليلات:</b> البيانات غير متوفرة حالياً (لا مصدر بياناتٍ حقيقي لهذا المؤشر بعد)`;
}

// Phase 3 — القسم 29: قسم "ملخّص الإصلاح الذاتي" — من repair_executions
// الحقيقي حصراً (آخر ٢٤ ساعة). كل الـPlaybooks تعمل بوضع Shadow Mode فقط
// اليوم، فالأعداد الحقيقية غالباً صفرٌ أو قليلة — هذا متوقَّعٌ وصحيح، لا
// خطأً يُخفى. لو الجدول فارغاً تماماً (لا صفٍّ إطلاقاً في هذه النافذة):
// "البيانات غير متوفرة حالياً" حرفياً كما يطلب القسم 4/29 — لا اختلاق صفرٍ
// موهوم يُقرأ وكأنه فحصٌ فعلي تمّ (نفس درس Phase 1.5: peakHours/analytics).
async function getSelfHealingSummary(sb: any): Promise<string> {
  try {
    const since = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
    const { data, error } = await sb
      .from("repair_executions")
      .select("status")
      .gte("started_at", since);
    if (error) return `🩹 <b>ملخّص الإصلاح الذاتي:</b> البيانات غير متوفرة حالياً (تعذّر القراءة)`;
    if (!data || !data.length) {
      return `🩹 <b>ملخّص الإصلاح الذاتي:</b> البيانات غير متوفرة حالياً (لا تقييمات Self-Healing مسجَّلة آخر ٢٤ ساعة)`;
    }
    const wouldAutoHeal = data.filter((r: { status: string }) => r.status === "WOULD_AUTO_HEAL").length;
    const succeeded = data.filter((r: { status: string }) => r.status === "SUCCEEDED").length;
    const failed = data.filter((r: { status: string }) => ["FAILED", "VERIFICATION_FAILED"].includes(r.status)).length;
    const escalated = data.filter((r: { status: string }) =>
      ["ESCALATED", "PRECONDITION_FAILED", "RISK_BLOCKED", "RATE_LIMITED", "COOLDOWN_ACTIVE", "CIRCUIT_OPEN", "DISABLED"].includes(r.status)
    ).length;
    const circuitOpen = data.filter((r: { status: string }) => r.status === "CIRCUIT_OPEN").length;
    // كل الـPlaybooks Shadow Mode اليوم — "أُصلِح فعلياً" (succeeded) يجب أن
    // يبقى 0 بالضرورة؛ لا نصف WOULD_AUTO_HEAL كإصلاحٍ فعلي حصل.
    return `🩹 <b>ملخّص الإصلاح الذاتي (Shadow Mode):</b> ${data.length} تقييماً | كان سيُصلَح تلقائياً لو AUTO: ${wouldAutoHeal} | أُصلِح فعلياً: ${succeeded} | فشل: ${failed} | صُعِّد: ${escalated} | قاطعٌ مفتوح: ${circuitOpen}`;
  } catch (error) {
    return `🩹 <b>ملخّص الإصلاح الذاتي:</b> ❌ خطأ (${error})`;
  }
}

// صلاحية الحسابات: أيّ حسابٍ يوشك على الانتهاء خلال أسبوع. الحسابات
// الدائمة (expires_at = NULL) خارج الاستعلام أصلاً بحكم الفلتر.
async function getExpirySummary(sb: any): Promise<{ text: string; urgent: boolean }> {
  try {
    const soon = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString();
    const { data, error } = await sb
      .from("allowed_emails")
      .select("email,expires_at")
      .not("expires_at", "is", null)
      .lte("expires_at", soon)
      .order("expires_at", { ascending: true });
    if (error) return { text: `⏳ <b>صلاحية الحسابات:</b> غير متوفرة (${error.message})`, urgent: false };
    if (!data || !data.length) return { text: `⏳ <b>صلاحية الحسابات:</b> لا حساب ينتهي خلال أسبوع ✅`, urgent: false };
    const expired = data.filter((r: any) => new Date(r.expires_at).getTime() <= Date.now());
    const lines = data.slice(0, 10).map((r: any) => {
      const d = Math.ceil((new Date(r.expires_at).getTime() - Date.now()) / 86400000);
      return d <= 0 ? `  • ${r.email} — <b>منتهٍ</b>` : `  • ${r.email} — ${d} يوم`;
    });
    const more = data.length > 10 ? `\n  … و${data.length - 10} غيرها` : "";
    return {
      text: `⏳ <b>صلاحية الحسابات:</b> ${data.length} حساباً ينتهي خلال أسبوع (منها ${expired.length} منتهٍ)\n${lines.join("\n")}${more}`,
      // الدفع إلى تلغرام عند ≤ ٣ أيام فقط. القائمة كاملةً تظهر في اللوحة
      // كل يوم؛ أما الرسالة فتُحجز للنافذة التي يلزم فيها قرارٌ فعلاً —
      // وإلا صار الحساب الواحد سبعَ رسائل متطابقة (وهي شكوى سابقة).
      urgent: data.some((r: any) =>
        (new Date(r.expires_at).getTime() - Date.now()) <= 3 * 24 * 60 * 60 * 1000
      ),
    };
  } catch (error) {
    return { text: `⏳ <b>صلاحية الحسابات:</b> ❌ خطأ (${error})`, urgent: false };
  }
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  // 🔒 وكيلٌ إداريّ: يجمع بيانات كل المعلّمات ويرسلها إلى تلجرام.
  if (!isServiceRoleRequest(req)) return unauthorized(cors);

  const sb = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );
  let run = { runId: null as string | null, correlationId: null as string | null, startedAt: Date.now() };

  // manual=true (أمر /ملخص من تلغرام، أو زرّ «تحديث الآن») يُرسل فعلياً
  // إلى تلغرام. تشغيلة pg_cron اليومية العادية لا manual في جسمها، فتكتفي
  // بحفظ الملخّص في agent_messages ليظهر في لوحة التشغيل — تلغرام فقط عند
  // الطلب الصريح، لا تلقائياً كل يوم.
  const body = await req.json().catch(() => ({}));
  const manual = body?.manual === true;

  try {
    console.log("📊 بدء إنشاء الملخص اليومي...");
    run = await startRun(sb, "daily-summary", "CRON");

    // جمع البيانات من جميع الوكلاء
    const [creditSummary, librarySummary, peakHours, feedbackSummary, analyticsSummary, selfHealingSummary, expiry] =
      await Promise.all([
        getCreditSummary(sb),
        getLibrarySummary(sb),
        getPeakHoursSummary(sb),
        getFeedbackSummary(sb),
        getAnalyticsSummary(sb),
        getSelfHealingSummary(sb),
        getExpirySummary(sb),
      ]);

    // بناء الرسالة الكاملة
    const now = new Date().toLocaleString("ar-SA", { timeZone: "Asia/Riyadh" });
    let message = `📊 <b>الملخص اليومي</b> — ${now}\n`;
    message += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n`;
    message += `${creditSummary}\n\n`;
    message += `${librarySummary}\n\n`;
    message += `${peakHours}\n\n`;
    message += `${feedbackSummary}\n\n`;
    message += `${analyticsSummary}\n\n`;
    message += `${selfHealingSummary}\n\n`;
    message += `${expiry.text}\n\n`;
    message += `━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`;

    // الأزرار الرئيسية
    const buttons = [
      [
        { text: "💰 رصيد", callback_data: "summary:credit:details" },
        { text: "📚 مكتبة", callback_data: "summary:library:details" },
        { text: "📈 أوقات", callback_data: "summary:peaks:details" },
      ],
      [
        { text: "📋 استبيان", callback_data: "summary:feedback:new" },
        { text: "🤖 تحليل", callback_data: "summary:analytics:details" },
      ],
      [
        { text: "⏰ إعادة جدولة", callback_data: "summary:reschedule" },
        { text: "🔄 تحديث الآن", callback_data: "summary:refresh" },
      ],
    ];

    // إرسال الرسالة فقط عند طلبٍ صريح (manual) — التشغيلة اليومية المجدولة
    // تكتفي بحفظه لعرضه في لوحة التشغيل، بلا رسالة تلغرام تلقائية.
    // استثناءٌ واحد من قاعدة «لا تلغرام تلقائياً»: حسابٌ يوشك على الانتهاء
    // إجراءٌ يفوت وقتُه إن لم يُر — معلّمةٌ دافعة تُمنَع من الدخول صباحاً.
    const result = (manual || expiry.urgent)
      ? await sendTelegram(message, { inline_keyboard: buttons })
      : { ok: true as const, message_id: null as number | null, error: undefined as string | undefined };

    // تسجيل الملخّص دوماً — هذا هو المصدر الذي تقرأ منه لوحة التشغيل آخر ملخّص.
    await sb.from("agent_messages").insert({
      message_id: `summary-${(manual || expiry.urgent) && result.ok && result.message_id ? result.message_id : Date.now()}`,
      agent_name: "daily-summary",
      message_text: message,
      telegram_message_id: (manual || expiry.urgent) && result.ok ? result.message_id : null,
    });

    // تسجيل السجل
    await sb.from("agent_logs").insert({
      agent_name: "daily-summary",
      action: "daily_summary_sent",
      status: result.ok ? "success" : "error",
      error_message: result.error,
    });

    await finishRun(sb, run, {
      status: result.ok ? "SUCCESS" : "FAILED",
      resultSummary: "أُرسل الملخص اليومي" + (result.ok ? "" : " — فشل الإرسال"),
      error: result.ok ? undefined : result.error,
      recordsWritten: result.ok ? 1 : 0,
    });

    return json({
      ok: true,
      message: "Daily summary sent",
      message_id: result.message_id,
      run_id: run.runId,
    });
  } catch (error) {
    console.error("❌ Error:", error);
    await finishRun(sb, run, { status: "FAILED", error: String(error) });
    return json({ error: String(error) }, 500);
  }
});
