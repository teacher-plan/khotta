// دالة مساعدة لإرسال الرسائل عبر Telegram
// تُستخدم من جميع الوكلاء
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

interface TelegramButton {
  text: string;
  callback_data: string;
}

interface TelegramOptions {
  parse_mode?: "HTML" | "Markdown";
  inline_keyboard?: TelegramButton[][];
}

async function getTelegramSecrets() {
  const token = Deno.env.get("TELEGRAM_BOT_TOKEN") || "";
  const chatId = Deno.env.get("TELEGRAM_CHAT_ID") || "";

  if (token && chatId) return { token, chatId };

  const sb = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
  );

  const { data: botTokenData } = await sb
    .from("vault.decrypted_secrets")
    .select("decrypted_secret")
    .eq("name", "telegram_bot_token")
    .maybeSingle();

  const { data: chatIdData } = await sb
    .from("vault.decrypted_secrets")
    .select("decrypted_secret")
    .eq("name", "telegram_chat_id")
    .maybeSingle();

  return {
    token: botTokenData?.decrypted_secret || "",
    chatId: chatIdData?.decrypted_secret || "",
  };
}

export async function sendTelegram(
  message: string,
  options?: TelegramOptions
): Promise<{ ok: boolean; message_id?: number; error?: string }> {
  const { token, chatId } = await getTelegramSecrets();

  if (!token || !chatId) {
    console.error("❌ Telegram configuration missing");
    return { ok: false, error: "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID" };
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

export async function editTelegram(
  messageId: number,
  message: string,
  options?: TelegramOptions
): Promise<{ ok: boolean; error?: string }> {
  const { token, chatId } = await getTelegramSecrets();

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
