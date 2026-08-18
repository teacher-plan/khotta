// دالة مساعدة لإرسال الرسائل عبر Telegram
// تُستخدم من جميع الوكلاء

// إمّا زرُّ ردٍّ (callback_data) أو زرُّ رابط (url). وزرُّ الرابط يسع روابط
// طويلة لا تُحسب على حدّ نصّ الرسالة (٤٠٩٦ حرفاً) — وهو ما يجعله الطريق
// الوحيد لقائمةٍ فيها رابط واتساب برسالةٍ مكتوبة لكل صفّ.
interface TelegramButton {
  text: string;
  callback_data?: string;
  url?: string;
}

interface TelegramOptions {
  parse_mode?: "HTML" | "Markdown";
  inline_keyboard?: TelegramButton[][];
}

// ═══ بوتان منفصلان: التسجيل/الترحيب/الدفع (الأصلي) وفحوصٌ دورية (جديد) ═══
// نفس منطق الإرسال، توكن ووجهة مختلفان فقط — فصلٌ يمنع اختلاط تنبيهات
// المراقبة التشغيلية برسائل التواصل مع المعلّمات، بلا أي تغييرٍ في محتوى
// أو منطق أيٍّ من الرسالتين.
async function sendVia(
  token: string | undefined,
  chatId: string | undefined,
  message: string,
  options?: TelegramOptions,
): Promise<{ ok: boolean; message_id?: number; error?: string }> {
  if (!token || !chatId) {
    console.error("❌ Telegram configuration missing");
    return { ok: false, error: "Missing bot token or chat id" };
  }

  const body: Record<string, unknown> = {
    chat_id: chatId,
    text: message,
    parse_mode: options?.parse_mode || "HTML",
  };

  if (options?.inline_keyboard) {
    body.reply_markup = { inline_keyboard: options.inline_keyboard };
  }

  try {
    const response = await fetch(
      `https://api.telegram.org/bot${token}/sendMessage`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }
    );

    const data = await response.json() as { ok: boolean; result?: { message_id: number }; description?: string };

    if (!data.ok) {
      console.error("❌ Telegram API error:", data.description);
      return { ok: false, error: data.description };
    }

    console.log(`✅ Message sent: ${data.result?.message_id}`);
    return { ok: true, message_id: data.result?.message_id };
  } catch (error) {
    console.error("❌ Error sending Telegram message:", error);
    return { ok: false, error: String(error) };
  }
}

async function editVia(
  token: string | undefined,
  chatId: string | undefined,
  messageId: number,
  message: string,
  options?: TelegramOptions,
): Promise<{ ok: boolean; error?: string }> {
  if (!token || !chatId) {
    return { ok: false, error: "Missing configuration" };
  }

  const body: Record<string, unknown> = {
    chat_id: chatId,
    message_id: messageId,
    text: message,
    parse_mode: options?.parse_mode || "HTML",
  };

  if (options?.inline_keyboard) {
    body.reply_markup = { inline_keyboard: options.inline_keyboard };
  }

  try {
    const response = await fetch(
      `https://api.telegram.org/bot${token}/editMessageText`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }
    );

    const data = await response.json() as { ok: boolean; description?: string };
    return { ok: data.ok, error: data.description };
  } catch (error) {
    return { ok: false, error: String(error) };
  }
}

// ── البوت الأصلي: التسجيل والترحيب ومتابعة الدفع (registration-notifier،
//    telegram-webhook) — بلا أي تغيير في التوقيع أو السلوك ──
export function sendTelegram(message: string, options?: TelegramOptions) {
  return sendVia(Deno.env.get("TELEGRAM_BOT_TOKEN"), Deno.env.get("TELEGRAM_CHAT_ID"), message, options);
}
export function editTelegram(messageId: number, message: string, options?: TelegramOptions) {
  return editVia(Deno.env.get("TELEGRAM_BOT_TOKEN"), Deno.env.get("TELEGRAM_CHAT_ID"), messageId, message, options);
}

// ── البوت الجديد: الفحوصات الدورية (system-health-check، credit-monitor،
//    daily-summary، file-processor-monitor) ──
export function sendTelegramOps(message: string, options?: TelegramOptions) {
  return sendVia(Deno.env.get("TELEGRAM_BOT_TOKEN_OPS"), Deno.env.get("TELEGRAM_CHAT_ID_OPS"), message, options);
}
export function editTelegramOps(messageId: number, message: string, options?: TelegramOptions) {
  return editVia(Deno.env.get("TELEGRAM_BOT_TOKEN_OPS"), Deno.env.get("TELEGRAM_CHAT_ID_OPS"), messageId, message, options);
}

// ── قائمة الأوامر الأصلية في تلغرام (زرّ "/" بجانب مربّع الكتابة) ──
// setMyCommands يُسجّل القائمة لدى تلغرام نفسه، فتظهر للمستخدم قائمةً
// قابلةً للنقر بدل حفظ الأوامر وكتابتها يدوياً. العملية idempotent —
// إعادة استدعائها بنفس القائمة لا تُنشئ شيئاً جديداً، فآمنٌ تكرارها.
export async function setOpsBotCommands(
  commands: Array<{ command: string; description: string }>,
): Promise<{ ok: boolean; error?: string }> {
  const token = Deno.env.get("TELEGRAM_BOT_TOKEN_OPS");
  if (!token) return { ok: false, error: "TELEGRAM_BOT_TOKEN_OPS غير مضبوط" };
  try {
    const response = await fetch(`https://api.telegram.org/bot${token}/setMyCommands`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ commands }),
    });
    const data = await response.json() as { ok: boolean; description?: string };
    return { ok: data.ok, error: data.description };
  } catch (error) {
    return { ok: false, error: String(error) };
  }
}
