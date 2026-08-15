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

    // استقبال رسائل نصية (للاستبيانات وأوامر الطلب الفوري)
    if (body.message && body.message.text) {
      const text = body.message.text.trim();
      const userId = body.message.from?.id;

      console.log(`💬 Message received: "${text}" from user ${userId}`);

      // طلب فوري للملخص الشامل بدل انتظار الموعد المجدول (5 مساءً)
      if (text === "/ملخص" || text === "/summary" || text === "/report") {
        await sendTelegram("⏳ جاري تجهيز الملخص الآن...");

        const fnResponse = await fetch(
          `${Deno.env.get("SUPABASE_URL")}/functions/v1/daily-summary`,
          {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${Deno.env.get("SUPABASE_ANON_KEY")}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({}),
          }
        );

        if (!fnResponse.ok) {
          await sendTelegram("❌ تعذّر تجهيز الملخص الآن — حاول لاحقاً.");
        }

        return json({ ok: fnResponse.ok });
      }

      // عدد المسجّلات في الحلقة الأولى — سؤالٌ يتكرّر أثناء حملة الترويج،
      // وفتحُ لوحة Supabase على الهاتف لأجله متعبٌ. الأسماء الخمسة الأخيرة
      // تكفي للاطمئنان دون إغراق الرسالة بقائمةٍ تطول كل يوم.
      if (text === "/تسجيلات" || text === "/registrations" || text === "/count") {
        const sb = createClient(
          Deno.env.get("SUPABASE_URL")!,
          Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
        );

        const { count: total } = await sb.from("pre_registrations")
          .select("id", { count: "exact", head: true }).eq("stage", "cycle1");

        // بداية يوم مسقط (UTC+4) محسوبةً بالإزاحة: لا توقيت صيفي فالإزاحة ثابتة.
        const since = new Date(Date.now() + 4 * 3600 * 1000);
        since.setUTCHours(0, 0, 0, 0);
        const dayStart = new Date(since.getTime() - 4 * 3600 * 1000).toISOString();

        const { count: today } = await sb.from("pre_registrations")
          .select("id", { count: "exact", head: true })
          .eq("stage", "cycle1").gte("created_at", dayStart);

        const { data: latest } = await sb.from("pre_registrations")
          .select("name,created_at").eq("stage", "cycle1")
          .order("created_at", { ascending: false }).limit(5);

        const esc = (s: string) => String(s ?? "")
          .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

        const lines = [
          "📊 <b>تسجيلات الحلقة الأولى</b>",
          "",
          `👥 الإجمالي: <b>${total ?? 0}</b>`,
          `📅 اليوم: <b>${today ?? 0}</b>`,
        ];
        if (latest?.length) {
          lines.push("", "<b>آخر المسجّلات:</b>");
          for (const r of latest) lines.push(`• ${esc(r.name || "بلا اسم")}`);
        }

        await sendTelegram(lines.join("\n"));
        return json({ ok: true });
      }

      // من لم تُفعَّل بعد — مع رابط ترحيبٍ جاهز لكلٍّ منهنّ.
      // البوت لا يراسل المعلّمة بنفسه (تلغرام يمنع البوتات من بدء محادثةٍ مع
      // من لم يبدأها)، لكنه يختصر الطريق إلى ضغطةٍ واحدة من الهاتف.
      if (text === "/pending" || text === "/انتظار" || text === "/المتبقيات") {
        const sb = createClient(
          Deno.env.get("SUPABASE_URL")!,
          Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
        );
        const { data } = await sb.from("pre_registrations")
          .select("name,phone,created_at")
          .eq("stage", "cycle1").eq("payment_status", "pending")
          .order("created_at", { ascending: false }).limit(20);

        const esc = (s: string) => String(s ?? "")
          .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        const wa = (p: string) => {
          let d = String(p || "").replace(/\D/g, "");
          if (d.startsWith("00")) d = d.slice(2);
          return d ? `https://wa.me/${d.length === 8 ? "968" + d : d}` : "";
        };
        const welcome = (n: string) => [
          n ? `أهلاً بكِ ${n} 🌸` : "أهلاً بكِ 🌸", "",
          "وصلَنا حجزُ مقعدكِ في منصّة «خُطّتي الفصلية» — الحلقة الأولى، وسعدنا بانضمامكِ.", "",
          "سنتواصل معكِ لتفعيل اشتراككِ مع بداية أول أسبوع دوام بإذن الله، ويصلكِ حسابُكِ جاهزاً.", "",
          "وإلى ذلك الحين، أيُّ استفسارٍ يخطر لكِ فاكتبيه هنا — نجيبكِ بسرور 🌷",
        ].join("\n");

        if (!data || !data.length) {
          await sendTelegram("✅ لا حجوزات في الانتظار — كلّهنّ مُفعَّلات.");
          return json({ ok: true });
        }
        // الروابط في أزرارٍ لا في نصّ الرسالة: رابط واتساب برسالةٍ مكتوبة
        // يقارب ١٤٠٠ حرف، وأربعَ عشرة منها تتجاوز حدّ النصّ (٤٠٩٦) خمسة
        // أضعاف فتُرفض الرسالة كلّها. وروابطُ الأزرار لا تُحسب على ذلك الحدّ.
        //
        // لكنّ للأزرار حدّها: قِيس بالتجربة على واجهة تلغرام — ستّة أزرار
        // (٨٨٤٧ حرفاً) تمرّ وسبعة (١٠٢٦٩) تُرفض. فخمسةٌ في المرّة، وهامشُ
        // زرٍّ كامل يحتمل الأسماء الطويلة دون أن تسقط الرسالة.
        const rows = data.slice(0, 5).map((r: { name?: string; phone?: string }) => {
          const u = wa(r.phone || "");
          const nm = (r.name || "بلا اسم").slice(0, 26);
          return u ? [{ text: `🌸 ${nm}`, url: `${u}?text=${encodeURIComponent(welcome(r.name || ""))}` }] : [];
        }).filter((r: unknown[]) => r.length);

        const head = [`⏳ <b>في انتظار التفعيل: ${data.length}</b>`, "",
          "اضغطي اسم المعلّمة ليُفتح واتساب ورسالةُ الترحيب مكتوبةٌ فيه."];
        if (data.length > rows.length) head.push("", `<i>تُعرض ${rows.length} — أعيدي الأمر بعد إرسالها.</i>`);
        const noPhone = data.filter((r: { phone?: string }) => !wa(r.phone || ""));
        if (noPhone.length) head.push("", `⚠️ بلا رقم: ${noPhone.map((r: { name?: string }) => esc(r.name || "")).join("، ")}`);

        const sent = await sendTelegram(head.join("\n"), { inline_keyboard: rows });
        // الفشل لا يُبتلع: كان يُرجَع ok وقد رفض تلغرام الرسالة، فيظنّ المشرف
        // أنّ الأمر لم يصل أصلاً ويعيده مراراً بلا أثر.
        if (!sent.ok) {
          console.error("pending list failed:", sent.error);
          return json({ ok: false, error: sent.error }, 502);
        }
        return json({ ok: true, listed: rows.length });
      }

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
