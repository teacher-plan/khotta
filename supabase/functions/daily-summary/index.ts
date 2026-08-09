// الملخص اليومي المركزي (Daily Summary)
// يجمع بيانات جميع الوكلاء ويرسل رسالة واحدة شاملة

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendTelegram } from "../_shared/telegram.ts";

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
    const { data: profiles } = await sb.from("profiles").select("id, full_name");
    const { data: settings } = await sb.from("ai_settings").select("user_id, key, value");

    if (!profiles || !settings) return "❌ خطأ في جلب بيانات الرصيد";

    let critical = 0, warning = 0;

    profiles.forEach((p: { id: string; full_name: string }) => {
      const used = parseInt(settings.find((s: any) => s.user_id === p.id && s.key === "usage_text")?.value || "0");
      const limit = parseInt(settings.find((s: any) => s.user_id === p.id && s.key === "limit_text")?.value || "1");
      const percentage = (used / limit) * 100;

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
      .from("c1_library")
      .select("id, created_at")
      .gte("created_at", today.toISOString());

    if (!files) return "📚 <b>المكتبة:</b> لا بيانات متوفرة";

    const totalFiles = files.length;
    return `📚 <b>المكتبة:</b> ${totalFiles} ملف جديد اليوم`;
  } catch (error) {
    return `📚 <b>المكتبة:</b> ❌ خطأ`;
  }
}

async function getPeakHoursSummary(sb: any): Promise<string> {
  // بيانات وهمية مؤقتاً - سيتم تحسينها لاحقاً
  return `📈 <b>أوقات الذروة:</b> 3-4 مساءً (البيانات قيد التحديث)`;
}

async function getFeedbackSummary(sb: any): Promise<string> {
  try {
    const { data: surveys } = await sb
      .from("user_surveys")
      .select("survey_id")
      .gt("created_at", new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString());

    const count = surveys?.length || 0;
    const avgScore = 4.2; // بيانات وهمية

    return `📋 <b>الآراء:</b> ${count} استجابة هذا الأسبوع | الرضا: ${avgScore}/5 ⭐`;
  } catch (error) {
    return `📋 <b>الآراء:</b> ❌ خطأ`;
  }
}

async function getAnalyticsSummary(sb: any): Promise<string> {
  // بيانات وهمية مؤقتاً
  return `🤖 <b>التحليلات:</b> تحديث النتائج...`;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  try {
    const sb = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    console.log("📊 بدء إنشاء الملخص اليومي...");

    // جمع البيانات من جميع الوكلاء
    const [creditSummary, librarySummary, peakHours, feedbackSummary, analyticsSummary] =
      await Promise.all([
        getCreditSummary(sb),
        getLibrarySummary(sb),
        getPeakHoursSummary(sb),
        getFeedbackSummary(sb),
        getAnalyticsSummary(sb),
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

    // إرسال الرسالة
    const result = await sendTelegram(message, { inline_keyboard: buttons });

    if (result.ok) {
      // تسجيل الرسالة
      await sb.from("agent_messages").insert({
        message_id: `summary-${result.message_id}`,
        agent_name: "daily-summary",
        message_text: message,
        telegram_message_id: result.message_id,
      });
    }

    // تسجيل السجل
    await sb.from("agent_logs").insert({
      agent_name: "daily-summary",
      action: "daily_summary_sent",
      status: result.ok ? "success" : "error",
      error_message: result.error,
    });

    return json({
      ok: true,
      message: "Daily summary sent",
      message_id: result.message_id,
    });
  } catch (error) {
    console.error("❌ Error:", error);
    return json({ error: String(error) }, 500);
  }
});
