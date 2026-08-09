// وكيل مراقبة الرصيد (Credit Monitor Agent)
// يراقب استهلاك حصة الذكاء الاصطناعي الشهرية لكل معلمة ويرسل تنبيهات
//
// الحدود عامة لكل المعلمات (من ai_settings: quota_text/quota_img/quota_search
// بلا user_id — انظر _shared/quota.ts)، والاستهلاك الفعلي لكل معلمة مسجّل
// في ai_usage (user_id, month, kind, count).

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendTelegram } from "../_shared/telegram.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

// Telegram parse_mode HTML يفسّر < و > و & كوسوم — أي اسم/بريد معلمة أو
// نص ثابت يحتوي عليها يكسر الرسالة كاملة برفض 400 من الـAPI بلا رسالة
// تصل إطلاقاً. يجب تهريب كل نص متغيّر ونصوص المقارنة الثابتة (< 50%).
function escHtml(s: string): string {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

interface TeacherUsage {
  user_id: string;
  email: string;
  teacher_name: string | null;
  used: number;
  limit: number;
  kind: string;
}

const QUOTA_KEYS: Record<string, string> = {
  text: "quota_text",
  img: "quota_img",
  search: "quota_search",
};
const QUOTA_DEFAULTS: Record<string, number> = { text: 300, img: 200, search: 20 };

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  try {
    const sb = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    );

    console.log("📊 بدء مراقبة الرصيد...");

    const month = new Date().toISOString().slice(0, 7);

    // الحدود العامة من ai_settings
    const { data: settingsRows, error: settingsError } = await sb
      .from("ai_settings")
      .select("key, value");

    if (settingsError) {
      console.error("❌ Error fetching ai_settings:", settingsError);
      return json({ error: "Failed to fetch settings" }, 500);
    }

    const settings: Record<string, string> = {};
    settingsRows?.forEach((r: { key: string; value: string }) => (settings[r.key] = r.value));

    const limits: Record<string, number> = {
      text: parseInt(settings[QUOTA_KEYS.text] || "") || QUOTA_DEFAULTS.text,
      img: parseInt(settings[QUOTA_KEYS.img] || "") || QUOTA_DEFAULTS.img,
      search: parseInt(settings[QUOTA_KEYS.search] || "") || QUOTA_DEFAULTS.search,
    };

    // الاستهلاك الفعلي لكل معلمة هذا الشهر
    const { data: usageRows, error: usageError } = await sb
      .from("ai_usage")
      .select("user_id, kind, count")
      .eq("month", month);

    if (usageError) {
      console.error("❌ Error fetching ai_usage:", usageError);
      return json({ error: "Failed to fetch usage" }, 500);
    }

    if (!usageRows || usageRows.length === 0) {
      await sendTelegram("📊 <b>ملخص الرصيد اليومي</b>\n━━━━━━━━━━━━━━━━━━━━━━\nلا يوجد استهلاك مسجّل لهذا الشهر بعد.");
      return json({ ok: true, message: "No usage this month" });
    }

    // أسماء المعلمات من cycle1_profiles (display_name داخل data)
    const userIds = [...new Set(usageRows.map((r: { user_id: string }) => r.user_id))];
    const { data: teacherRows } = await sb
      .from("cycle1_profiles")
      .select("id, email, data")
      .in("id", userIds);

    const nameMap = new Map<string, { email: string; name: string | null }>();
    teacherRows?.forEach((t: { id: string; email: string; data: Record<string, unknown> | null }) => {
      nameMap.set(t.id, {
        email: t.email,
        name: (t.data?.display_name as string) || null,
      });
    });

    // تصنيف حسب النسبة (لكل نوع استخدام على حدة)
    const critical: TeacherUsage[] = [];
    const warning: TeacherUsage[] = [];
    let healthyCount = 0;

    usageRows.forEach((r: { user_id: string; kind: string; count: number }) => {
      const limit = limits[r.kind] ?? 0;
      if (!limit) return;
      const percentage = (r.count / limit) * 100;
      const info = nameMap.get(r.user_id);
      const entry: TeacherUsage = {
        user_id: r.user_id,
        email: info?.email || "غير معروف",
        teacher_name: info?.name || null,
        used: r.count,
        limit,
        kind: r.kind,
      };

      if (percentage > 80) critical.push(entry);
      else if (percentage > 50) warning.push(entry);
      else healthyCount++;
    });

    // بناء الرسالة
    let messageText = `📊 <b>ملخص الرصيد اليومي</b> (${month})\n`;
    messageText += `━━━━━━━━━━━━━━━━━━━━━━\n`;

    if (critical.length > 0) {
      messageText += `\n🔴 <b>حالة حرجة (أكثر من 80%):</b>\n`;
      critical.forEach((q) => {
        const percentage = ((q.used / q.limit) * 100).toFixed(0);
        const label = escHtml(q.teacher_name || q.email);
        messageText += `   ${label}: ${q.kind} ${percentage}% (${q.used}/${q.limit})\n`;
      });
    }

    if (warning.length > 0) {
      messageText += `\n🟡 <b>تحذير (50-80%):</b>\n`;
      warning.forEach((q) => {
        const percentage = ((q.used / q.limit) * 100).toFixed(0);
        const label = escHtml(q.teacher_name || q.email);
        messageText += `   ${label}: ${q.kind} ${percentage}%\n`;
      });
    }

    messageText += `\n🟢 <b>سليمة (أقل من 50%):</b> ${healthyCount} حالة`;
    messageText += `\n━━━━━━━━━━━━━━━━━━━━━━`;

    const buttons = [
      [
        { text: "💰 تفصيلي", callback_data: "credit:detailed" },
        { text: "📈 إحصائيات", callback_data: "credit:stats" },
      ],
      [{ text: "⏰ إعادة الآن", callback_data: "credit:reschedule" }],
    ];

    const result = await sendTelegram(messageText, { inline_keyboard: buttons });

    if (result.ok) {
      await sb.from("agent_messages").insert({
        message_id: `credit-${result.message_id}-${Date.now()}`,
        agent_name: "credit-monitor",
        message_text: messageText,
        telegram_message_id: result.message_id,
      });

      await sb.from("agent_schedules").update({
        last_run: new Date().toISOString(),
      }).eq("agent_name", "credit-monitor");
    }

    await sb.from("agent_logs").insert({
      agent_name: "credit-monitor",
      action: "summary_sent",
      status: result.ok ? "success" : "error",
      error_message: result.error,
      data_collected: {
        critical_count: critical.length,
        warning_count: warning.length,
        healthy_count: healthyCount,
      },
    });

    return json({ ok: true, message: "Credit monitor completed" });
  } catch (error) {
    console.error("❌ Unexpected error:", error);
    return json({ error: String(error) }, 500);
  }
});
