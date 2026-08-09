// Telegram Webhook — يستقبل تفاعلات المستخدم مع الأزرار
// عندما يضغط المستخدم على زر، Telegram ترسل callback هنا

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendTelegram, editTelegram } from "../_shared/telegram.ts";

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

// معالجات الأزرار
async function handleCallbackQuery(
  callbackData: string,
  messageId: number,
  sb: any
): Promise<string> {
  const [module, action, ...extra] = callbackData.split(":");

  console.log(`🔘 Button pressed: ${callbackData}`);

  switch (module) {
    case "credit":
      if (action === "detailed") {
        return "💰 <b>تقرير الرصيد المفصل</b>\n\nقيد التحديث...";
      } else if (action === "reschedule") {
        return "⏰ تم إعادة جدولة وكيل الرصيد للتشغيل الآن";
      }
      break;

    case "library":
      if (action === "detailed") {
        return "📚 <b>الملفات الجديدة</b>\n\nقيد التحديث...";
      }
      break;

    case "summary":
      if (action === "reschedule") {
        // تحديث جدول الجدولة
        await sb.from("agent_schedules").update({
          scheduled_hour: new Date().getHours(),
          scheduled_minute: new Date().getMinutes(),
        }).eq("agent_name", "daily-summary");

        return "⏰ تم تحديث وقت الملخص!\nسيتم التشغيل كل يوم في هذا الوقت";
      } else if (action === "refresh") {
        return "🔄 جاري تحديث الملخص...";
      }
      break;

    case "feedback":
      if (action === "new") {
        return "📋 <b>استبيان جديد</b>\n\nكم من 1-5 درجات رضاك عن المنصة؟";
      }
      break;

    default:
      return "❓ أمر غير معروف";
  }

  return "✅ تم معالجة الطلب";
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  if (req.method !== "POST") {
    return json({ error: "Method not allowed" }, 405);
  }

  try {
    const body = await req.json();

    // استقبال callback من Telegram
    if (body.callback_query) {
      const query = body.callback_query;
      const messageId = query.message?.message_id;
      const callbackData = query.data;
      const userId = query.from?.id;

      console.log(`📨 Callback received: ${callbackData} from user ${userId}`);

      if (!messageId || !callbackData) {
        return json({ ok: false, error: "Invalid callback" });
      }

      const sb = createClient(
        Deno.env.get("SUPABASE_URL")!,
        Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
      );

      // معالجة الضغطة
      const responseText = await handleCallbackQuery(callbackData, messageId, sb);

      // تحديث الرسالة بالرد
      const editResult = await editTelegram(messageId, responseText);

      // تسجيل الإجراء
      await sb.from("agent_messages").update({
        user_action: callbackData,
        action_timestamp: new Date().toISOString(),
      }).eq("telegram_message_id", messageId);

      return json({ ok: editResult.ok });
    }

    // استقبال رسائل نصية (للاستبيانات وغيرها)
    if (body.message && body.message.text) {
      const text = body.message.text;
      const userId = body.message.from?.id;

      console.log(`💬 Message received: "${text}" from user ${userId}`);

      // معالجة الردود على الاستبيانات
      if (text.match(/^[1-5]$/)) {
        // تقييم من 1-5
        const sb = createClient(
          Deno.env.get("SUPABASE_URL")!,
          Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
        );

        await sb.from("user_surveys").insert({
          survey_type: "satisfaction",
          responses: { rating: parseInt(text) },
        });

        await sendTelegram(`✅ شكراً على التقييم! إجابتك: ${text}/5 ⭐`);
        return json({ ok: true });
      }
    }

    return json({ ok: true, message: "Processed" });
  } catch (error) {
    console.error("❌ Error:", error);
    return json({ error: String(error) }, 500);
  }
});
