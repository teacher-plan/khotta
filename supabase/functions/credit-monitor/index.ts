// وكيل مراقبة الرصيد (Credit Monitor Agent)
// يراقب استهلاك الرصيد لكل معلمة ويرسل تنبيهات عند الوصول لحد معين

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

interface TeacherQuota {
  user_id: string;
  email: string;
  teacher_name: string | null;
  ai_quota_used: number;
  ai_quota_limit: number;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  try {
    const sb = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    console.log("📊 بدء مراقبة الرصيد...");

    // جلب جميع المعلمات والمعلومات الخاصة بهن
    const { data: profiles, error: profileError } = await sb
      .from("profiles")
      .select("id, email, full_name");

    if (profileError) {
      console.error("❌ Error fetching profiles:", profileError);
      return json({ error: "Failed to fetch profiles" }, 500);
    }

    // جلب إعدادات AI لكل معلمة
    const { data: aiSettings, error: settingsError } = await sb
      .from("ai_settings")
      .select("user_id, key, value");

    if (settingsError) {
      console.error("❌ Error fetching AI settings:", settingsError);
      return json({ error: "Failed to fetch settings" }, 500);
    }

    // بناء خريطة الحصص لكل معلمة
    const quotaMap = new Map<string, TeacherQuota>();

    profiles?.forEach((profile: { id: string; email: string; full_name: string | null }) => {
      quotaMap.set(profile.id, {
        user_id: profile.id,
        email: profile.email,
        teacher_name: profile.full_name,
        ai_quota_used: 0,
        ai_quota_limit: 0,
      });
    });

    // ملء البيانات من ai_settings
    aiSettings?.forEach((setting: { user_id: string; key: string; value: string }) => {
      const quota = quotaMap.get(setting.user_id);
      if (quota) {
        if (setting.key === "usage_text") quota.ai_quota_used = parseInt(setting.value) || 0;
        if (setting.key === "limit_text") quota.ai_quota_limit = parseInt(setting.value) || 0;
      }
    });

    // تصنيف المعلمات حسب الحالة
    const critical: TeacherQuota[] = [];  // > 80%
    const warning: TeacherQuota[] = [];   // 50-80%
    const healthy: TeacherQuota[] = [];   // < 50%

    quotaMap.forEach((quota) => {
      if (quota.ai_quota_limit === 0) return;
      const percentage = (quota.ai_quota_used / quota.ai_quota_limit) * 100;

      if (percentage > 80) critical.push(quota);
      else if (percentage > 50) warning.push(quota);
      else healthy.push(quota);
    });

    // بناء الرسالة
    let messageText = `📊 <b>ملخص الرصيد اليومي</b>\n`;
    messageText += `━━━━━━━━━━━━━━━━━━━━━━\n`;

    if (critical.length > 0) {
      messageText += `\n🔴 <b>حالة حرجة (> 80%):</b>\n`;
      critical.forEach((q) => {
        const percentage = ((q.ai_quota_used / q.ai_quota_limit) * 100).toFixed(0);
        messageText += `   ${q.teacher_name || "معلمة"}: ${percentage}% (${q.ai_quota_used}/${q.ai_quota_limit})\n`;
      });
    }

    if (warning.length > 0) {
      messageText += `\n🟡 <b>تحذير (50-80%):</b>\n`;
      warning.forEach((q) => {
        const percentage = ((q.ai_quota_used / q.ai_quota_limit) * 100).toFixed(0);
        messageText += `   ${q.teacher_name || "معلمة"}: ${percentage}%\n`;
      });
    }

    messageText += `\n🟢 <b>سليمة (< 50%):</b> ${healthy.length} معلمة`;
    messageText += `\n━━━━━━━━━━━━━━━━━━━━━━`;

    // الأزرار
    const buttons = [
      [
        { text: "💰 تفصيلي", callback_data: "credit:detailed" },
        { text: "📈 إحصائيات", callback_data: "credit:stats" },
      ],
      [{ text: "⏰ إعادة الآن", callback_data: "credit:reschedule" }],
    ];

    // إرسال الرسالة
    const result = await sendTelegram(messageText, { inline_keyboard: buttons });

    if (result.ok) {
      // تسجيل الرسالة في قاعدة البيانات
      await sb.from("agent_messages").insert({
        message_id: `credit-${result.message_id}`,
        agent_name: "credit-monitor",
        message_text: messageText,
        telegram_message_id: result.message_id,
      });

      // تحديث آخر تشغيل
      await sb.from("agent_schedules").update({
        last_run: new Date().toISOString(),
      }).eq("agent_name", "credit-monitor");
    }

    // تسجيل السجل
    await sb.from("agent_logs").insert({
      agent_name: "credit-monitor",
      action: "summary_sent",
      status: result.ok ? "success" : "error",
      error_message: result.error,
      data_collected: {
        critical_count: critical.length,
        warning_count: warning.length,
        healthy_count: healthy.length,
      },
    });

    return json({ ok: true, message: "Credit monitor completed" });
  } catch (error) {
    console.error("❌ Unexpected error:", error);
    return json({ error: String(error) }, 500);
  }
});
