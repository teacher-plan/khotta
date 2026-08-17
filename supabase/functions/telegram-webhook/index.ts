// Telegram Webhook — يستقبل تفاعلات المستخدم مع الأزرار
// عندما يضغط المستخدم على زر، Telegram ترسل callback هنا

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendTelegram, editTelegram, sendTelegramOps } from "../_shared/telegram.ts";

// ═══ Phase 1.5 — القسم 3: تحقّق X-Telegram-Bot-Api-Secret-Token ═══
// تلغرام يرسل هذا الترويسة مع كل تحديث webhook حين يُضبَط secret_token عند
// تسجيل setWebhook (راجع: https://core.telegram.org/bots/api#setwebhook).
// قبل هذا التعديل: لا تحقّقٌ إطلاقاً — أي طرفٍ يعرف رابط الدالّة (عامّ،
// بلا JWT) يستطيع انتحال تحديثات تلغرام وتشغيل أي معالج زرٍّ/أمرٍ نصّي.
//
// السرّ مُخزَّنٌ في متغيّر بيئة الدالّة فقط (TELEGRAM_WEBHOOK_SECRET) —
// نفس نمط بقية أسرار تلغرام في هذا المشروع (Deno.env.get، لا شيء في
// الواجهة). بوتٌ واحد أو بوتان: السرّ نفسه يُستعمَل لكلا الرابطين
// (الأصلي و?bot=ops) ما لم يُضبَط سرٌّ منفصل TELEGRAM_WEBHOOK_SECRET_OPS.
//
// ⚠️ حالة النشر الحالية: هذا التحقّق مكتوبٌ في الكود لكنه BLOCKED عملياً
// حتى تُنفَّذ خطوتان خارجيتان لا تستطيعهما هذه الوكالة (انظر تقرير Phase
// 1.5 القسم 6 للأوامر الدقيقة):
//   ١) توليد قيمة سرّية عشوائية وتخزينها: supabase secrets set TELEGRAM_WEBHOOK_SECRET=...
//   ٢) تسجيلها لدى تلغرام عبر setWebhook مع secret_token بنفس القيمة.
// إلى أن يُضبَط TELEGRAM_WEBHOOK_SECRET كسرٍّ في بيئة الدالّة، isSecretConfigured
// تكون false والتحقّق "يتنازل بأمان" (يسمح بالمرور كسابق عهده) بدل أن
// يقفل webhook تلغرام الحيّ فجأةً بلا تنسيقٍ مسبق — هذا مقصودٌ صراحةً؛
// إبقاء البوت يعمل أولويةٌ حتى يضبط المدير السرّ فعلياً في الخطوتين أعلاه.
function verifyTelegramSecret(req: Request): { ok: boolean; configured: boolean } {
  const expected = Deno.env.get("TELEGRAM_WEBHOOK_SECRET") || "";
  if (!expected) return { ok: true, configured: false }; // لا سرّ مضبوط بعد — NOT YET DEPLOYED
  const got = req.headers.get("X-Telegram-Bot-Api-Secret-Token") || "";
  // لا نُسجّل got أو expected أبداً في أي console.log/سجلّ — القسم 3 صراحةً.
  return { ok: got.length > 0 && got === expected, configured: true };
}

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

// ── قائمة المنتظِرات للترحيب ──────────────────────────────────────────
// البوت لا يراسل المعلّمة بنفسه (تلغرام يمنع البوتات من بدء محادثةٍ مع من
// لم يبدأها)، لكنه يختصر الطريق إلى ضغطتين: زرُّ اسمها يفتح واتساب
// والرسالةُ مكتوبة، وزرُّ «تمّ» يُسجّل أنها رُحّب بها فتخرج من القائمة.
//
// ولولا التسجيل لظلّت الخمسُ أنفسهنّ تظهر أبداً: إرسالُ واتساب يقع خارج
// المنصّة فلا سبيل إلى معرفته إلا بإقرارٍ منك.
const PEND_PAGE = 5;

function _waNum(p: string): string {
  let d = String(p || "").replace(/\D/g, "");
  if (d.startsWith("00")) d = d.slice(2);
  return d ? (d.length === 8 ? "968" + d : d) : "";
}
function _welcomeText(n: string): string {
  const nm = String(n || "").trim();
  return [
    nm ? `أهلاً بكِ ${nm} 🌸` : "أهلاً بكِ 🌸", "",
    "وصلَنا حجزُ مقعدكِ في منصّة «خُطّتي الفصلية» — الحلقة الأولى، وسعدنا بانضمامكِ.", "",
    "سنتواصل معكِ لتفعيل اشتراككِ مع بداية أول أسبوع دوام بإذن الله، ويصلكِ حسابُكِ جاهزاً.", "",
    "وإلى ذلك الحين، أيُّ استفسارٍ يخطر لكِ فاكتبيه هنا — نجيبكِ بسرور 🌷",
  ].join("\n");
}
async function sendPendingList(): Promise<{ ok: boolean; listed: number; error?: string }> {
  const sb = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );
  const { data, error } = await sb.from("pre_registrations")
    .select("id,name,phone")
    .eq("stage", "cycle1").eq("payment_status", "pending")
    .is("welcomed_at", null)
    .order("created_at", { ascending: true })      // الأقدم أولاً: هي أطولهنّ انتظاراً
    .limit(60);

  // خطأٌ في الاستعلام (كعمودٍ غير موجود) لا يُخلَط بحالة «لا أحد ينتظر» —
  // فيسبق الأول رسالةً مطمئنةً كاذبة، بينما القائمة الحقيقية لم تُفحص أصلاً.
  if (error) {
    console.error("sendPendingList query failed:", error.message);
    await sendTelegram(`⚠️ تعذّر جلب القائمة: ${error.message}`);
    return { ok: false, listed: 0, error: error.message };
  }

  const esc = (x: string) => String(x ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  if (!data || !data.length) {
    await sendTelegram("✅ لا أحد ينتظر الترحيب — رُحِّب بالجميع.");
    return { ok: true, listed: 0 };
  }

  // الروابط في أزرارٍ لا في نصّ الرسالة: رابط واتساب برسالةٍ مكتوبة يقارب
  // ١٤٠٠ حرف، وأربعَ عشرة منها تتجاوز حدّ النصّ (٤٠٩٦) خمسة أضعاف.
  // وللأزرار حدُّها أيضاً: قِيس على واجهة تلغرام — ستّة أزرار (٨٨٤٧ حرفاً)
  // تمرّ وسبعة (١٠٢٦٩) تُرفض. فخمسةٌ في المرّة بهامشِ زرٍّ كامل.
  const page = data.filter((r: { phone?: string }) => _waNum(r.phone || "")).slice(0, PEND_PAGE);
  const rows: Array<Array<{ text: string; url?: string; callback_data?: string }>> = [];
  for (const r of page) {
    rows.push([{ text: `🌸 ${(r.name || "بلا اسم").slice(0, 26)}`,
      url: `https://wa.me/${_waNum(r.phone || "")}?text=${encodeURIComponent(_welcomeText(r.name || ""))}` }]);
  }
  if (page.length) {
    rows.push([{ text: `✅ رحّبتُ بهؤلاء (${page.length})`,
      callback_data: "pend:done:" + page.map((r: { id: number }) => r.id).join(",") }]);
  }

  const head = [`⏳ <b>في انتظار الترحيب: ${data.length}</b>`, "",
    "اضغط اسم المعلّمة ليُفتح واتساب ورسالةُ الترحيب مكتوبةٌ فيه."];
  if (data.length > page.length) head.push("", `<i>تُعرض ${page.length} — وبعد الضغط على «رحّبتُ بهؤلاء» تظهر التالية.</i>`);
  const noPhone = data.filter((r: { phone?: string }) => !_waNum(r.phone || ""));
  if (noPhone.length) head.push("", `⚠️ بلا رقم هاتف: ${noPhone.map((r: { name?: string }) => esc(r.name || "")).join("، ")}`);

  const sent = await sendTelegram(head.join("\n"), { inline_keyboard: rows });
  // الفشل لا يُبتلع: كان يُرجَع ok وقد رفض تلغرام الرسالة، فيظنّ المشرف أنّ
  // الأمر لم يصل أصلاً ويعيده مراراً بلا أثر.
  if (!sent.ok) console.error("pending list failed:", sent.error);
  return { ok: sent.ok, listed: page.length, error: sent.error };
}

// ── قائمة متابعة الدفع ────────────────────────────────────────────────
// مثل قائمة الترحيب تماماً — خمسٌ في كل مرّة، وزرٌّ يفتح واتساب برسالة
// الدفع جاهزةً، وزرُّ «تابعتُ» يُسجّل المتابعة ويجلب الدفعة التالية.
// عمود welcomed_at وحده لا يكفي معياراً هنا: قد تُرحَّب المعلّمة وتظلّ لم
// تدفع أياماً، فتحتاج متابعةً لاحقةً منفصلة عن الترحيب الأول.
let _payNum = 76787595; // احتياطي إن تعذّر جلب الرقم من app_settings
function _payWaNum(p: string): string {
  let d = String(p || "").replace(/\D/g, "");
  if (d.startsWith("00")) d = d.slice(2);
  return d ? (d.length === 8 ? "968" + d : d) : "";
}
function _payText(n: string, price: number): string {
  const nm = String(n || "").trim();
  return [
    nm ? `مرحباً ${nm} 🌸` : "مرحباً 🌸", "",
    "أهلاً بكِ في منصة «خُطّتي الفصلية» — سعدنا بتسجيلكِ.", "",
    `لتفعيل حسابك يتبقّى تحويل مبلغ ${price} ريالاً عُمانياً، وهو اشتراك الفصل الدراسي كاملاً.`, "",
    "طريقة الدفع:",
    `• تحويل على الرقم: ${_payNum}`, "",
    "وبعد التحويل أرسلي صورة الإيصال هنا ليُفعَّل حسابك 🌷",
  ].join("\n");
}
async function sendPaymentList(): Promise<{ ok: boolean; listed: number; error?: string }> {
  const sb = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );

  const { data: priceRow } = await sb.from("app_settings")
    .select("value").eq("key", "subscription_price").maybeSingle();
  const price = Number(priceRow?.value) || 15;

  // خلافاً للترحيب، المتابعة تتكرّر: من تابعناها اليوم قد تحتاج متابعةً
  // ثانيةً بعد أيام لو لم تدفع بعد. فالترتيب يضع من لم تُتابَع قطّ أولاً،
  // ومن تابعناها ينتقلن لآخر الطابور بدل أن يختفين نهائياً كالترحيب.
  const { data, error } = await sb.from("pre_registrations")
    .select("id,name,phone")
    .eq("stage", "cycle1").eq("payment_status", "pending")
    .order("payment_followup_at", { ascending: true, nullsFirst: true })
    .order("created_at", { ascending: true })
    .limit(60);

  if (error) {
    console.error("sendPaymentList query failed:", error.message);
    await sendTelegram(`⚠️ تعذّر جلب القائمة: ${error.message}`);
    return { ok: false, listed: 0, error: error.message };
  }

  const esc = (x: string) => String(x ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  if (!data || !data.length) {
    await sendTelegram("✅ لا أحد بانتظار الدفع — الجميع مُفعَّلات أو رُوسِلن بالفعل.");
    return { ok: true, listed: 0 };
  }

  const page = data.filter((r: { phone?: string }) => _payWaNum(r.phone || "")).slice(0, PEND_PAGE);
  const rows: Array<Array<{ text: string; url?: string; callback_data?: string }>> = [];
  for (const r of page) {
    rows.push([{ text: `💳 ${(r.name || "بلا اسم").slice(0, 26)}`,
      url: `https://wa.me/${_payWaNum(r.phone || "")}?text=${encodeURIComponent(_payText(r.name || "", price))}` }]);
  }
  if (page.length) {
    rows.push([{ text: `✅ تابعتُ هؤلاء (${page.length})`,
      callback_data: "pay:done:" + page.map((r: { id: number }) => r.id).join(",") }]);
  }

  const head = [`💳 <b>بانتظار الدفع: ${data.length}</b>`, "",
    "اضغط اسم المعلّمة ليُفتح واتساب ورسالةُ الدفع مكتوبةٌ فيه."];
  if (data.length > page.length) head.push("", `<i>تُعرض ${page.length} — وبعد الضغط على «تابعتُ هؤلاء» تظهر التالية.</i>`);
  const noPhone = data.filter((r: { phone?: string }) => !_payWaNum(r.phone || ""));
  if (noPhone.length) head.push("", `⚠️ بلا رقم هاتف: ${noPhone.map((r: { name?: string }) => esc(r.name || "")).join("، ")}`);

  const sent = await sendTelegram(head.join("\n"), { inline_keyboard: rows });
  if (!sent.ok) console.error("payment list failed:", sent.error);
  return { ok: sent.ok, listed: page.length, error: sent.error };
}

// ═══ Phase 1.5 — القسم 5: تدقيق أزرار "إعادة المحاولة" ═══
// قاعدةٌ صارمة: لا يجوز لزرٍّ أن يدّعي إنجاز شيءٍ لم يحدث فعلاً. الأزرار
// أدناه كانت (قبل هذا التعديل) تُعيد نصّ نجاحٍ ثابتاً بلا أي كود تنفيذيٍّ
// خلفه (credit:reschedule، summary:refresh) أو تسقط على المعالج الافتراضي
// "✅ تم معالجة الطلب" رغم عدم وجود معالجٍ إطلاقاً (files:retry_failed) —
// وهذا بالضبط ما تحظره المواصفة. "إعادة المحاولة" هنا تعني حصراً: إعادة
// تشغيل نفس العملية المعروفة فوراً (نداء دالّة الحافة نفسها) — لا تشخيصاً
// ولا إصلاحاً تلقائياً.
async function invokeAgentNow(fnName: string): Promise<{ ok: boolean; error?: string }> {
  try {
    const r = await fetch(
      `${Deno.env.get("SUPABASE_URL")}/functions/v1/${fnName}`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({}),
      },
    );
    return { ok: r.ok, error: r.ok ? undefined : `HTTP ${r.status}` };
  } catch (e) {
    return { ok: false, error: String(e) };
  }
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
        // لا تقرير مفصّل مبنيّ فعلاً بعد — "قيد التحديث" لا تدّعي اكتمالاً،
        // فتبقى صادقة (PRESENT BUT NOT ACTIVE، موثَّقة صراحةً لا مخفيّة).
        return "💰 <b>تقرير الرصيد المفصل</b>\n\nهذه الميزة قيد التطوير ولم تُفعَّل بعد.";
      } else if (action === "reschedule") {
        // إعادة تشغيلٍ حقيقية: نداء credit-monitor الآن فعلياً، لا ادّعاءٌ فارغ.
        const r = await invokeAgentNow("credit-monitor");
        return r.ok
          ? "🔄 أُعيد تشغيل مراقب الرصيد الآن — انتظر رسالة الملخص التالية."
          : `❌ تعذّرت إعادة التشغيل الآن (${r.error}). حاول لاحقاً.`;
      }
      break;

    case "library":
      if (action === "detailed") {
        return "📚 <b>الملفات الجديدة</b>\n\nهذه الميزة قيد التطوير ولم تُفعَّل بعد.";
      }
      break;

    case "summary":
      if (action === "reschedule") {
        // تحديث جدول الجدولة — كتابةٌ حقيقية على agent_schedules (سلوكٌ
        // أصلي، لم يُعدَّل هنا؛ مذكورٌ في تقرير Phase 1.5 كإجراءٍ حقيقي).
        await sb.from("agent_schedules").update({
          scheduled_hour: new Date().getHours(),
          scheduled_minute: new Date().getMinutes(),
        }).eq("agent_name", "daily-summary");

        return "⏰ تم تحديث وقت الملخص!\nسيتم التشغيل كل يوم في هذا الوقت";
      } else if (action === "refresh") {
        // إعادة تشغيلٍ حقيقية: نداء daily-summary الآن، لا ادّعاءٌ فارغ.
        const r = await invokeAgentNow("daily-summary");
        return r.ok
          ? "🔄 أُعيد إنشاء الملخص — ستصلك رسالةٌ جديدة الآن."
          : `❌ تعذّر تحديث الملخص الآن (${r.error}). حاول لاحقاً.`;
      }
      break;

    case "feedback":
      if (action === "new") {
        return "📋 <b>استبيان جديد</b>\n\nكم من 1-5 درجات رضاك عن المنصة؟";
      }
      break;

    case "files":
      // Phase 1.5: "❌ إعادة محاولة" (files:retry_failed) كانت تسقط على
      // المعالج الافتراضي فتُعيد "✅ تم معالجة الطلب" رغم عدم وجود أي كود
      // إعادة معالجةٍ خلفها إطلاقاً — أخطر حالات الادّعاء الكاذب في هذا
      // التدقيق. لا تنفيذ آمناً وموثوقاً لإعادة معالجة ملفٍ فاشل جاهزاً
      // اليوم (يتطلّب تصميماً أكبر: أي معالجٍ لأي نوع ملف، وبأي حدود إعادة
      // محاولة) — الزرّ الآن يصرّح بذلك بدل الادّعاء.
      return "⚠️ إعادة المعالجة التلقائية غير مُفعَّلة بعد — راجعي الملفات العالقة يدوياً من لوحة الإدارة.";

    default:
      return "❓ أمر غير معروف";
  }

  // لم يعد هناك مسارٌ صامت يصل إلى هنا بادّعاء نجاحٍ عام؛ أي زرٍّ غير
  // مُعرَّف صراحةً أعلاه يُعيد رسالة "أمر غير معروف" الآن (القسم 5).
  return "❓ أمر غير معروف — لا إجراء مرتبط بهذا الزرّ.";
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  if (req.method !== "POST") {
    return json({ error: "Method not allowed" }, 405);
  }

  // Phase 1.5 — القسم 3: رفض التحديثات بلا سرٍّ صحيح، فقط إن كان السرّ
  // مضبوطاً فعلاً في بيئة الدالّة (configured=true). طالما لم يُضبَط بعد
  // (البوت الحيّ لا يرسل الترويسة إطلاقاً اليوم) نستمرّ كسابق عهدنا —
  // BLOCKED حتى تُنجَز خطوتا الضبط الخارجيتان أعلاه.
  const secretCheck = verifyTelegramSecret(req);
  if (secretCheck.configured && !secretCheck.ok) {
    console.error("telegram-webhook: رُفض طلبٌ — X-Telegram-Bot-Api-Secret-Token غائبٌ أو خاطئ");
    return json({ error: "unauthorized" }, 401);
  }

  // Phase 1.5 — القسم 1: telegram-webhook NOT_INTEGRATED مع agent_runs عمداً
  // في هذه المرحلة: عشرات مسارات return مبكرة (كل زرّ/أمرٍ نصّي) تجعل
  // إغلاق كل تشغيلةٍ بأمانٍ عند كل مخرجٍ عملاً كبيراً يخاطر بترك صفوف
  // RUNNING معلَّقة إن نُسي مخرجٌ واحد — يبقى التتبّع الحالي عبر agent_logs/
  // agent_messages (موجودٌ مسبقاً) كافياً هنا؛ التكامل الكامل مع agent_runs
  // موصًى به كخطوةٍ لاحقة (انظر التقرير، القسم 4 وقسم "المشاكل المعروفة").
  try {
    const body = await req.json();
    // بوت الفحص الدوري يسجّل رابط Webhook بمعامل ?bot=ops مميَّز — لا سبيل
    // آخر لتمييز مصدر التحديث لأن حمولة Telegram نفسها لا تحمل هوية البوت.
    const isOpsBot = new URL(req.url).searchParams.get("bot") === "ops";

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

      // «رحّبتُ بهؤلاء»: يُعلّم المعروضات ثم يعرض الدفعة التالية.
      // يُعالَج قبل المعالج العامّ لأن ذاك يستبدل نصّ الرسالة، ونحن نريد
      // إبقاءها سجلّاً لمن رُحّب بهنّ وإرسال قائمةٍ جديدة تحتها.
      if (callbackData.startsWith("pend:done:")) {
        const ids = callbackData.slice(10).split(",").map((x) => Number(x)).filter(Boolean);
        if (ids.length) {
          await sb.from("pre_registrations")
            .update({ welcomed_at: new Date().toISOString() }).in("id", ids);
        }
        // نُزيل الأزرار من الرسالة القديمة كي لا تُضغط مرّتين فتُعلَّم دفعةٌ
        // رُحِّب بها فعلاً، أو يُفتح واتساب لمن انتهى أمرها.
        await editTelegram(messageId, `✅ سُجّل الترحيب بـ${ids.length} معلّمة.`);
        await sendPendingList();
        return json({ ok: true, marked: ids.length });
      }

      // «تابعتُ هؤلاء» في قائمة الدفع: يُسجَّل وقت المتابعة (لا حذفٌ من
      // القائمة، فمن لم تدفع بعد تعود لآخر الطابور لا خارجه).
      if (callbackData.startsWith("pay:done:")) {
        const ids = callbackData.slice(9).split(",").map((x) => Number(x)).filter(Boolean);
        if (ids.length) {
          await sb.from("pre_registrations")
            .update({ payment_followup_at: new Date().toISOString() }).in("id", ids);
        }
        await editTelegram(messageId, `✅ سُجّلت متابعة الدفع لـ${ids.length} معلّمة.`);
        await sendPaymentList();
        return json({ ok: true, marked: ids.length });
      }

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

      // طلب فوري للملخص الشامل بدل انتظار الموعد المجدول (5 مساءً) —
      // نُقل بالكامل إلى بوت الفحص الدوري (isOpsBot) بناءً على طلبٍ صريح؛
      // البوت القديم (الترحيب/الدفع) لم يعد يستجيب لهذا الأمر إطلاقاً.
      if (isOpsBot && (text === "/ملخص" || text === "/summary" || text === "/report")) {
        await sendTelegramOps("⏳ جاري تجهيز الملخص الآن...");

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
          await sendTelegramOps("❌ تعذّر تجهيز الملخص الآن — حاول لاحقاً.");
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
        await sendPendingList();
        return json({ ok: true });
      }

      // متابعة من سجّلن ولم تدفع بعد — نفس فكرة /pending برسالة الدفع بدل الترحيب.
      if (text === "/payment" || text === "/دفع" || text === "/متابعة_الدفع") {
        await sendPaymentList();
        return json({ ok: true });
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
