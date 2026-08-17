// وكيل مراقبة معالجة الملفات (File Processor Monitor)
// يراقب الملفات المرفوعة ويتابع حالتها ويرسل تنبيهات للمستخدمات

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

// Telegram parse_mode HTML يفسّر < و > و & كوسوم — اسم ملف رفعته معلمة أو
// نص مقارنة ثابت (>2 ساعات) يكسر الرسالة كاملة برفض 400 بلا وصول إطلاقاً.
function escHtml(s: string): string {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  // 🔒 وكيلٌ إداريّ: يقرأ uploaded_by وأسماء الملفات ورسائل الأخطاء.
  if (!isServiceRoleRequest(req)) return unauthorized(cors);

  const sb = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );
  let run = { runId: null as string | null, correlationId: null as string | null, startedAt: Date.now() };

  // manual=true (نداءٌ صريح، مثل أمر تلغرام عند الحاجة) يُرسل الملخّص فعلياً
  // إلى تلغرام. تشغيلة pg_cron العادية (كل ٣٠ دقيقة) لا manual في جسمها،
  // فتكتفي بحفظ الملخّص في agent_messages ليظهر في لوحة التشغيل — بلا أي
  // رسالة تلغرام تلقائية، حتى لو لم يوجد شيءٌ يستحقّ الذكر أصلاً.
  const body = await req.json().catch(() => ({}));
  const manual = body?.manual === true;

  try {
    console.log("📁 بدء مراقبة معالجة الملفات...");
    run = await startRun(sb, "file-processor-monitor", "CRON");

    // جلب الملفات قيد المعالجة
    // ملاحظة: uploaded_by يشير إلى auth.users لا public.profiles، فلا يمكن
    // لـ PostgREST حلّ علاقة embed تلقائية بينهما — نكتفي بأعمدة الجدول نفسه
    const { data: processingFiles, error: fetchError } = await sb
      .from("file_processing_status")
      .select("*")
      .eq("status", "processing");

    if (fetchError) {
      console.error("❌ Error fetching files:", fetchError);
      await finishRun(sb, run, { status: "FAILED", error: fetchError.message });
      return json({ error: "Failed to fetch files" }, 500);
    }

    // جلب الملفات المكتملة من آخر ساعة
    const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000).toISOString();
    const { data: completedFiles } = await sb
      .from("file_processing_status")
      .select("*")
      .eq("status", "completed")
      .gte("completed_at", oneHourAgo);

    // جلب الملفات المفشلة من آخر ٢٤ ساعة
    const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
    const { data: failedFiles } = await sb
      .from("file_processing_status")
      .select("*")
      .eq("status", "failed")
      .gte("created_at", oneDayAgo);

    // إنشاء الملخص
    let summaryMessage = `📁 <b>ملخص معالجة الملفات</b>\n`;
    summaryMessage += `━━━━━━━━━━━━━━━━━━━━━━\n\n`;

    // الملفات قيد المعالجة
    if (processingFiles && processingFiles.length > 0) {
      summaryMessage += `⏳ <b>قيد المعالجة:</b> ${processingFiles.length} ملف\n`;

      const stuck = processingFiles.filter((f: any) => {
        const elapsed = Date.now() - new Date(f.updated_at).getTime();
        return elapsed > 2 * 60 * 60 * 1000; // أكثر من ساعتين
      });

      if (stuck.length > 0) {
        summaryMessage += `   🚨 <b>عالقة (أكثر من ساعتين):</b>\n`;
        stuck.forEach((f: any) => {
          const elapsed = Math.round((Date.now() - new Date(f.updated_at).getTime()) / 1000 / 60);
          summaryMessage += `      • ${escHtml(f.file_name)} (${elapsed} دقيقة)\n`;
        });
      }

      const processing = processingFiles.filter((f: any) => {
        const elapsed = Date.now() - new Date(f.updated_at).getTime();
        return elapsed <= 2 * 60 * 60 * 1000;
      });

      if (processing.length > 0) {
        summaryMessage += `   ⏳ <b>قيد المعالجة (طبيعي):</b> ${processing.length} ملف\n`;
      }
    } else {
      summaryMessage += `⏳ <b>قيد المعالجة:</b> لا توجد ملفات\n`;
    }

    // الملفات المكتملة
    if (completedFiles && completedFiles.length > 0) {
      summaryMessage += `✅ <b>اكتملت الساعة الأخيرة:</b> ${completedFiles.length} ملف\n`;
    }

    // الملفات المفشلة
    if (failedFiles && failedFiles.length > 0) {
      summaryMessage += `\n❌ <b>فشل المعالجة (آخر 24 ساعة):</b> ${failedFiles.length} ملف\n`;
      failedFiles.slice(0, 3).forEach((f: any) => {
        summaryMessage += `   • ${escHtml(f.file_name)}: ${escHtml(f.error_message || "خطأ غير معروف")}\n`;
      });
    }

    summaryMessage += `\n━━━━━━━━━━━━━━━━━━━━━━`;

    // الأزرار
    const buttons = [
      [
        { text: "📊 تفاصيل", callback_data: "files:detailed" },
        { text: "🚨 الملفات العالقة", callback_data: "files:stuck" },
      ],
      [
        { text: "❌ إعادة محاولة", callback_data: "files:retry_failed" },
      ],
    ];

    // إرسال الملخص فقط عند طلبٍ صريح (manual) — التشغيلة المجدولة تكتفي
    // بحفظه لعرضه في لوحة التشغيل، بلا إزعاج تلغرام كل ٣٠ دقيقة.
    const result = manual
      ? await sendTelegram(summaryMessage, { inline_keyboard: buttons })
      : { ok: true as const, message_id: null as number | null, error: undefined as string | undefined };

    // تسجيل الملخّص دوماً (وليس فقط عند الإرسال) — هذا هو المصدر الذي
    // تقرأ منه لوحة التشغيل آخر حالة معالجة الملفات.
    await sb.from("agent_messages").insert({
      message_id: `files-${manual && result.ok && result.message_id ? result.message_id : Date.now()}`,
      agent_name: "file-processor-monitor",
      message_text: summaryMessage,
      telegram_message_id: manual && result.ok ? result.message_id : null,
    });

    // تسجيل السجل
    await sb.from("agent_logs").insert({
      agent_name: "file-processor-monitor",
      action: "summary_sent",
      status: result.ok ? "success" : "error",
      error_message: result.error,
      data_collected: {
        processing_count: processingFiles?.length || 0,
        stuck_count: processingFiles?.filter((f: any) => {
          const elapsed = Date.now() - new Date(f.updated_at).getTime();
          return elapsed > 2 * 60 * 60 * 1000;
        }).length || 0,
        completed_count: completedFiles?.length || 0,
        failed_count: failedFiles?.length || 0,
      },
    });

    // إرسال تنبيه فوري للملفات العالقة
    const stuckFiles = processingFiles?.filter((f: any) => {
      const elapsed = Date.now() - new Date(f.updated_at).getTime();
      return elapsed > 2 * 60 * 60 * 1000;
    }) || [];

    if (stuckFiles.length > 0) {
      const emergencyMessage = `
🚨 <b>تنبيه: ملفات عالقة!</b>
━━━━━━━━━━━━━━━━━━━━━━
${stuckFiles
  .map((f: any) => {
    const elapsed = Math.round((Date.now() - new Date(f.updated_at).getTime()) / 1000 / 60 / 60);
    return `❌ ${escHtml(f.file_name)} (عالقة ${elapsed} ساعات)`;
  })
  .join("\n")}

👉 قد تحتاج هذه الملفات إلى إعادة معالجة أو حذف.
      `.trim();

      await sendTelegram(emergencyMessage);
    }

    await finishRun(sb, run, {
      status: result.ok ? "SUCCESS" : "FAILED",
      resultSummary: `قيد المعالجة ${processingFiles?.length || 0}، عالقة ${stuckFiles.length}، مكتملة ${completedFiles?.length || 0}، فاشلة ${failedFiles?.length || 0}`,
      error: result.ok ? undefined : result.error,
      recordsRead: (processingFiles?.length || 0) + (completedFiles?.length || 0) + (failedFiles?.length || 0),
      recordsWritten: result.ok ? 1 : 0,
    });

    return json({
      ok: true,
      message: "File monitor completed",
      stats: {
        processing: processingFiles?.length || 0,
        stuck: stuckFiles.length,
        completed: completedFiles?.length || 0,
        failed: failedFiles?.length || 0,
      },
    });
  } catch (error) {
    console.error("❌ Error:", error);
    await finishRun(sb, run, { status: "FAILED", error: String(error) });
    return json({ error: String(error) }, 500);
  }
});
