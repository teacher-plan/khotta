// Telegram Webhook — يستقبل تفاعلات المستخدم مع الأزرار
// عندما يضغط المستخدم على زر، Telegram ترسل callback هنا

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendTelegram, editTelegram, sendTelegramOps, setOpsBotCommands, setMainBotCommands } from "../_shared/telegram.ts";

// ═══ قائمة أوامر بوت العمليات الأصلية (زرّ "/" في تلغرام) ═══
// قيدٌ من تلغرام: اسم الأمر يقبل حروفاً إنجليزية صغيرة وأرقاماً و_ فقط
// (لا عربية) — فالقائمة تعرض الأسماء الإنجليزية بوصفٍ عربي، بينما تبقى
// المرادفات العربية (/الحالة، /الحوادث…) تعمل كما هي عند كتابتها يدوياً.
const OPS_BOT_COMMANDS = [
  { command: "help", description: "📋 عرض كل الأوامر المتاحة" },
  { command: "status", description: "📊 ملخّصٌ شامل + الإصلاح الذاتي (٢٤ ساعة)" },
  { command: "health", description: "🩺 حالة النظام الآن — أعطالٌ أو تحذيرات" },
  { command: "incidents", description: "🚨 الحوادث المفتوحة حالياً وخطورتها" },
  { command: "agents", description: "🧩 حالة كل وكيلٍ وآخر تشغيلة له" },
  { command: "cost", description: "💳 تكلفة الذكاء الاصطناعي هذا الشهر" },
  { command: "capacity", description: "💾 امتلاء قاعدة البيانات ومعدّل نموّها" },
  { command: "credit", description: "💰 استهلاك المعلّمات ومن تجاوزت حدّها" },
  { command: "files", description: "📁 ملخّص معالجة الملفات" },
  { command: "summary", description: "📈 الملخّص اليومي الكامل" },
];

// ═══ قائمة أوامر البوت الأصلي (الترحيب/الدفع/التسجيلات) ═══
// نفس قيد تلغرام: أسماءٌ إنجليزية فقط. المرادفات العربية (/دفع، /دفع2،
// /دفع3، /انتظار…) تعمل عند كتابتها يدوياً لكنها لا تظهر في هذه القائمة.
const MAIN_BOT_COMMANDS = [
  { command: "pending", description: "🕐 في انتظار التفعيل — مع رابط ترحيب" },
  { command: "payment", description: "💳 متابعة الدفع (تذكير١) — مع رابط واتساب" },
  { command: "payment2", description: "💳 متابعة الدفع (تذكير٢) — تجربة مجانية" },
  { command: "payment3", description: "💳 متابعة الدفع (تذكير٣) — تذكيرٌ أخير" },
  { command: "registrations", description: "📊 تسجيلات الحلقة الأولى — الإجمالي واليوم" },
  { command: "summary", description: "📋 الملخص الشامل الآن" },
];

// تُسجَّلان مرّةً واحدة لكل نسخةٍ حيّة من الدالّة (لا في كل رسالة): العملية
// idempotent وخفيفة، وتُطلَق بلا await فلا تُؤخّر الردّ ولا تُسقطه إن فشلت.
let opsCommandsRegistered = false;
function ensureOpsCommandsRegistered(): void {
  if (opsCommandsRegistered) return;
  opsCommandsRegistered = true;
  setOpsBotCommands(OPS_BOT_COMMANDS)
    .then((r) => { if (!r.ok) console.error("setMyCommands فشل:", r.error); })
    .catch((e) => console.error("setMyCommands رمى:", String(e)));
}
let mainCommandsRegistered = false;
function ensureMainCommandsRegistered(): void {
  if (mainCommandsRegistered) return;
  mainCommandsRegistered = true;
  setMainBotCommands(MAIN_BOT_COMMANDS)
    .then((r) => { if (!r.ok) console.error("setMyCommands (main) فشل:", r.error); })
    .catch((e) => console.error("setMyCommands (main) رمى:", String(e)));
}

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
// ثلاث رسائل تذكير متدرّجة — كل معلّمةٍ تصعد من مرحلةٍ لتاليتها عبر زرّ
// «تابعتُ هؤلاء»، فلا تصلها نفس الرسالة مرّتين. الأولى تحثّ على الدفع
// المباشر (استعجال + رقم التحويل)، الثانية تعرض تجربةً مجانية لمن ترددت،
// والثالثة تذكيرٌ أخير بلا ذكر تحويلٍ — تفتح باباً للسؤال فقط.
// ⚠️ فراغٌ واحدٌ بين الفقرات هنا لا فراغان: هذا النصّ يُطعَّم كاملاً داخل
// رابط واتساب (wa.me?text=…)، وكل سطرٍ فارغٍ إضافي يُضاعف الحجم المُرمَّز
// (URL-encoded) — ومع خمسة أزرارٍ في رسالةٍ واحدة كان هذا وحده يكفي
// لتجاوز حدّ تلغرام لحجم لوحة الأزرار (BUTTON reply markup is too long)،
// فلا يصل شيءٌ للمعلّمة ولا للمشرف. راجع أيضاً PAY_PAGE أدناه.
const PAY_REMINDERS: Array<{ label: string; text: (nm: string, price: number) => string }> = [
  {
    label: "الأول",
    text: (nm, price) => [
      nm ? `مرحباً ${nm} 🌟` : "مرحباً 🌟", "",
      "بقي أسبوعٌ واحد على بداية العام الدراسي — ومنصة «خُطّتي الفصلية» معكِ لتبدئي عامكِ بلا فوضى صفٍّ ولا تشتت، وذهنٍ مرتاح من بداية الفصل حتى نهايته.", "",
      "كوني من أوائل المشتركات وتميّزي بتوظيف أحدث وسائل الذكاء الاصطناعي في كل حصة. ✨", "",
      `حوّلي قيمة الاشتراك (${price} ريالاً عُمانياً) على *${_payNum}*، وأرسلي صورة الإيصال هنا ليُفعَّل حسابكِ فوراً 📌`,
    ].join("\n"),
  },
  {
    label: "الثاني",
    text: (nm, price) => [
      nm ? `مرحباً ${nm} 🌟` : "مرحباً 🌟", "",
      "نعلم أن قرار الاشتراك يحتاج وقتاً — لذا وفّرنا لكِ تجربةً مجانية لاختبار ميزات منصة «خُطّتي الفصلية» بنفسكِ قبل أن تقرّري.", "",
      "جرّبي كيف تُدار الحصة بلا فوضى ولا تشتت، وكيف يوظَّف الذكاء الاصطناعي في تحضيرها. ✨", "",
      `وإن أعجبتكِ، فتفعيل الحساب الكامل يتم بتحويل قيمة الاشتراك (${price} ريالاً عُمانياً) على نفس الرقم *${_payNum}*، وإرسال صورة الإيصال هنا 📌`,
    ].join("\n"),
  },
  {
    label: "الثالث",
    text: (nm) => [
      nm ? `مرحباً ${nm} 🌟` : "مرحباً 🌟", "",
      "لم نسمع منكِ بعد — وربما لديكِ سؤالٌ لم يجد إجابته، أو فقط لم تتسنَّ لكِ الفرصة بعد وسط انشغال هذه الأيام.", "",
      "نحن هنا لأي استفسار، ونودّ أن تبدئي عامكِ الدراسي معنا. 📌", "",
      "اكتبي لنا سؤالكِ أو ما يشغلكِ، وسنجيبكِ بسرور 🌷",
    ].join("\n"),
  },
];

// دفعة أزرار قائمة الدفع أصغر من PEND_PAGE (٥) عمداً: نصوص التذكير الآن
// أطول بكثير من نصّ الترحيب القصير، وخمسة أزرارٍ منها معاً تتجاوز حدّ
// تلغرام لحجم لوحة الأزرار كاملةً (انظر التعليق أعلى PAY_REMINDERS).
const PAY_PAGE = 2;

// stage: مرحلة التذكير المطلوب عرضها الآن (0 = الأول، 1 = الثاني، 2 = الثالث)
// — تجلب من هي بالضبط عند payment_reminder_stage=stage، فلا تتكرّر رسالةٌ
// على من تجاوزتها ولا تُقفَز رسالةٌ على من لم تصلها بعد.
async function sendPaymentList(stage: number): Promise<{ ok: boolean; listed: number; error?: string }> {
  const reminder = PAY_REMINDERS[stage];
  if (!reminder) return { ok: false, listed: 0, error: "invalid_stage" };

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
    .eq("payment_reminder_stage", stage)
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
    await sendTelegram(`✅ لا أحد بانتظار التذكير ${reminder.label} — إمّا دفعن أو انتقلن لمرحلةٍ تالية.`);
    return { ok: true, listed: 0 };
  }

  const page = data.filter((r: { phone?: string }) => _payWaNum(r.phone || "")).slice(0, PAY_PAGE);
  const rows: Array<Array<{ text: string; url?: string; callback_data?: string }>> = [];
  for (const r of page) {
    rows.push([{ text: `💳 ${(r.name || "بلا اسم").slice(0, 26)}`,
      url: `https://wa.me/${_payWaNum(r.phone || "")}?text=${encodeURIComponent(reminder.text(r.name || "", price))}` }]);
  }
  if (page.length) {
    rows.push([{ text: `✅ تابعتُ هؤلاء (${page.length})`,
      callback_data: `pay:done:${stage}:` + page.map((r: { id: number }) => r.id).join(",") }]);
  }

  const head = [`💳 <b>بانتظار التذكير ${reminder.label}: ${data.length}</b>`, "",
    "اضغط اسم المعلّمة ليُفتح واتساب ورسالةُ الدفع مكتوبةٌ فيه."];
  if (data.length > page.length) head.push("", `<i>تُعرض ${page.length} — وبعد الضغط على «تابعتُ هؤلاء» تظهر التالية.</i>`);
  const noPhone = data.filter((r: { phone?: string }) => !_payWaNum(r.phone || ""));
  if (noPhone.length) head.push("", `⚠️ بلا رقم هاتف: ${noPhone.map((r: { name?: string }) => esc(r.name || "")).join("، ")}`);

  const sent = await sendTelegram(head.join("\n"), { inline_keyboard: rows });
  if (!sent.ok) {
    // كان الفشل هنا يُبتلع بصمت (console.error فقط) فيظنّ المشرف أن الأمر
    // لم يصل أصلاً — تشخيصه يحتاج سجلّات لا نملك وصولاً سهلاً إليها.
    console.error("payment list failed:", sent.error);
    await sendTelegram(`⚠️ تعذّر إرسال قائمة التذكير ${reminder.label} (${page.length} معلّمة): ${sent.error || "سببٌ غير معروف"}`);
  }
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

// ═══ Copilot عبر تلغرام (بوت العمليات فقط) ═══
// يستدعي ops-copilot عبر مسارٍ داخليٍّ ضيّق (X-Ops-Copilot-Internal-Secret،
// منفصلٌ عن مفتاح الخدمة العام — انظر التوثيق في ops-copilot/index.ts).
// قراءةٌ فقط دوماً — لا تنفيذ إطلاقاً مهما كان نصّ السؤال. إن لم يُضبَط
// السرّ بعد في بيئة الدالّة، يفشل بأمانٍ برسالةٍ واضحة بدل صمتٍ محيّر.
async function askCopilotAndReply(question: string): Promise<void> {
  const secret = Deno.env.get("OPS_COPILOT_INTERNAL_SECRET") || "";
  if (!secret) {
    await sendTelegramOps("⚠️ المساعد (Copilot) غير مُفعَّلٍ من تلغرام بعد — يحتاج ضبط سرٍّ داخلي أولاً.");
    return;
  }
  await sendTelegramOps("⏳ جارٍ التحليل...");
  try {
    const r = await fetch(
      `${Deno.env.get("SUPABASE_URL")}/functions/v1/ops-copilot`,
      {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`,
          "X-Ops-Copilot-Internal-Secret": secret,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      },
    );
    const data = await r.json().catch(() => null);
    if (!r.ok || !data || !data.manager_summary) {
      await sendTelegramOps("❌ تعذّر الحصول على إجابةٍ الآن — حاول لاحقاً.");
      return;
    }
    const esc = (x: string) => String(x ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    const confLabel: Record<string, string> = {
      VERIFIED: "✅ موثّق", LIKELY: "🟡 محتمل", UNKNOWN: "⚪ غير مؤكَّد", INSUFFICIENT_DATA: "⚪ بياناتٌ غير كافية",
    };
    let reply = esc(String(data.manager_summary));
    if (data.technical_details) reply += `\n\n<i>${esc(String(data.technical_details).slice(0, 600))}</i>`;
    reply += `\n\n${confLabel[data.confidence] || esc(String(data.confidence || ""))}`;
    await sendTelegramOps(reply, { parse_mode: "HTML" });
  } catch (e) {
    await sendTelegramOps(`❌ خطأ: ${String(e)}`);
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

    // تسجيل قائمة الأوامر تلقائياً — بلا انتظار، فلا أثر على زمن الرد.
    if (isOpsBot) ensureOpsCommandsRegistered();
    else ensureMainCommandsRegistered();

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

      // «تابعتُ هؤلاء» في قائمة الدفع: يُسجَّل وقت المتابعة ويُرفَع
      // payment_reminder_stage خطوةً (لا حذفٌ من القائمة، فمن لم تدفع بعد
      // تنتقل للتذكير التالي لا تختفي). الصيغة "pay:done:<stage>:<ids>" —
      // تبقى الصيغة القديمة "pay:done:<ids>" (بلا مرحلة) تُقرأ كمرحلة٠
      // لتوافقٍ خلفي مع أزرار أُرسلت قبل هذا التعديل.
      if (callbackData.startsWith("pay:done:")) {
        const rest = callbackData.slice(9);
        const parts = rest.split(":");
        let stage = 0, idsStr = rest;
        if (parts.length === 2 && /^\d+$/.test(parts[0])) { stage = Number(parts[0]); idsStr = parts[1]; }
        const ids = idsStr.split(",").map((x) => Number(x)).filter(Boolean);
        if (ids.length) {
          await sb.from("pre_registrations")
            .update({ payment_followup_at: new Date().toISOString(), payment_reminder_stage: stage + 1 })
            .in("id", ids);
        }
        await editTelegram(messageId, `✅ سُجّلت متابعة الدفع (تذكير ${stage + 1}) لـ${ids.length} معلّمة.`);
        await sendPaymentList(stage);
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

        // manual:true — التشغيلة اليومية المجدولة لا تُرسل تلغرام تلقائياً
        // بعد الآن (تكتفي بحفظ الملخّص للوحة التشغيل)؛ هذا الأمر الصريح
        // وحده هو ما يطلب الإرسال الفعلي الآن.
        const fnResponse = await fetch(
          `${Deno.env.get("SUPABASE_URL")}/functions/v1/daily-summary`,
          {
            method: "POST",
            headers: {
              // daily-summary يتحقّق من isServiceRoleRequest — كان هذا
              // النداء يستخدم مفتاح anon خطأً (لا يجتاز ذلك التحقّق أبداً)؛
              // صُحِّح هنا إلى مفتاح الخدمة الصحيح.
              "Authorization": `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ manual: true }),
          }
        );

        if (!fnResponse.ok) {
          await sendTelegramOps("❌ تعذّر تجهيز الملخص الآن — حاول لاحقاً.");
        }

        return json({ ok: fnResponse.ok });
      }

      // ملخّص معالجة الملفات عند الطلب فقط — التشغيلة كل ٣٠ دقيقة لم تعد
      // تُرسل تلغرام تلقائياً (انظر ملاحظة manual أعلاه لنفس السبب).
      if (isOpsBot && (text === "/ملفات" || text === "/files")) {
        await sendTelegramOps("⏳ جاري تجهيز ملخّص الملفات الآن...");

        const fnResponse = await fetch(
          `${Deno.env.get("SUPABASE_URL")}/functions/v1/file-processor-monitor`,
          {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ manual: true }),
          }
        );

        if (!fnResponse.ok) {
          await sendTelegramOps("❌ تعذّر تجهيز ملخّص الملفات الآن — حاول لاحقاً.");
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

      // متابعة من سجّلن ولم تدفع بعد — ثلاث مراحل تذكير متدرّجة، كل أمرٍ
      // يعرض من هي بالضبط عند تلك المرحلة (انظر PAY_REMINDERS أعلاه).
      if (text === "/payment" || text === "/دفع" || text === "/متابعة_الدفع") {
        await sendPaymentList(0);
        return json({ ok: true });
      }
      if (text === "/payment2" || text === "/دفع2" || text === "/متابعة_الدفع2" || text === "/متابعة_الدفع_2") {
        await sendPaymentList(1);
        return json({ ok: true });
      }
      if (text === "/payment3" || text === "/دفع3" || text === "/متابعة_الدفع3" || text === "/متابعة_الدفع_3") {
        await sendPaymentList(2);
        return json({ ok: true });
      }

      // ═══ Copilot عبر تلغرام — بوت العمليات (ops) فقط ═══
      // "/تقرير" سؤالٌ ثابت جاهز، وأي نصٍّ حرٍّ آخر في بوت العمليات يُمرَّر
      // كسؤالٍ مباشر للكوبايلوت — نفس مسار "ما الذي كان Self-Healing
      // سيصلحه؟" و"لماذا لم يُصلَح هذا؟" المُبنيَّان مسبقاً، لكن من تلغرام
      // مباشرة. قراءةٌ فقط دوماً — لا تنفيذ إطلاقاً مهما كان نصّ السؤال
      // (الكوبايلوت نفسه يرفض أي طلب تنفيذٍ صراحةً، انظر fixIntent أعلاه).
      if (isOpsBot && (text === "/تقرير" || text === "/status")) {
        await askCopilotAndReply("لخّص حالة النظام الآن، وما الذي كان الإصلاح الذاتي سيُصلحه خلال آخر 24 ساعة؟");
        return json({ ok: true });
      }

      // اختصاراتٌ جاهزة لأكثر الأسئلة فائدةً — كلٌّ منها يمرّر سؤالاً
      // مصاغاً جيداً للكوبايلوت بدل كتابته يدوياً في كل مرّة. القائمة
      // الكاملة تظهر في /مساعدة أدناه.
      const COPILOT_SHORTCUTS: Record<string, string> = {
        "/الحالة": "ما حالة النظام الآن؟ اذكر أي مكوّنٍ حرج أو تحذيرٍ إن وُجد.",
        "/health": "ما حالة النظام الآن؟ اذكر أي مكوّنٍ حرج أو تحذيرٍ إن وُجد.",
        "/الحوادث": "ما الحوادث المفتوحة الآن؟ لكل حادثة: الخطورة، المكوّن، منذ متى، وهل تكرّرت.",
        "/incidents": "ما الحوادث المفتوحة الآن؟ لكل حادثة: الخطورة، المكوّن، منذ متى، وهل تكرّرت.",
        "/الوكلاء": "ما حالة كل وكيلٍ الآن؟ أيّها سليم، وأيّها فيه تحذير أو فشل، ومتى كان آخر تشغيلٍ لكلٍّ منها؟",
        "/agents": "ما حالة كل وكيلٍ الآن؟ أيّها سليم، وأيّها فيه تحذير أو فشل، ومتى كان آخر تشغيلٍ لكلٍّ منها؟",
        "/التكلفة": "كم تكلفة استخدام الذكاء الاصطناعي هذا الشهر؟ وهل هناك أي مؤشّر ارتفاعٍ غير معتاد؟",
        "/cost": "كم تكلفة استخدام الذكاء الاصطناعي هذا الشهر؟ وهل هناك أي مؤشّر ارتفاعٍ غير معتاد؟",
        "/السعة": "ما نسبة امتلاء قاعدة البيانات الآن؟ وما معدّل نموّها؟ هل نقترب من أي حدٍّ؟",
        "/capacity": "ما نسبة امتلاء قاعدة البيانات الآن؟ وما معدّل نموّها؟ هل نقترب من أي حدٍّ؟",
      };
      if (isOpsBot && COPILOT_SHORTCUTS[text]) {
        await askCopilotAndReply(COPILOT_SHORTCUTS[text]);
        return json({ ok: true });
      }

      // ملخّص الرصيد عند الطلب — التشغيلة كل ٦ ساعات لم تعد تُرسل إلا عند
      // وجود حالةٍ حرجة فعلية (>٨٠٪).
      if (isOpsBot && (text === "/رصيد" || text === "/credit")) {
        await sendTelegramOps("⏳ جاري تجهيز ملخّص الرصيد الآن...");
        const fnResponse = await fetch(
          `${Deno.env.get("SUPABASE_URL")}/functions/v1/credit-monitor`,
          {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ manual: true }),
          }
        );
        if (!fnResponse.ok) {
          await sendTelegramOps("❌ تعذّر تجهيز ملخّص الرصيد الآن — حاول لاحقاً.");
        }
        return json({ ok: fnResponse.ok });
      }

      if (isOpsBot && (text === "/مساعدة" || text === "/مساعد" || text === "/help" || text === "/اوامر" || text === "/أوامر" || text === "/start")) {
        await sendTelegramOps([
          "🤖 <b>أوامر بوت العمليات</b>",
          "",
          "<i>اضغط زرّ «/» بجانب مربّع الكتابة لاختيار أي أمرٍ من القائمة</i>",
          "",
          "📊 /status — ملخّصٌ شامل + الإصلاح الذاتي (٢٤ ساعة)",
          "🩺 /health — حالة النظام الآن (أعطالٌ حرجة/تحذيرات)",
          "🚨 /incidents — الحوادث المفتوحة حالياً وخطورتها",
          "🧩 /agents — حالة كل وكيلٍ وآخر تشغيلة له",
          "💳 /cost — تكلفة الذكاء الاصطناعي هذا الشهر",
          "💾 /capacity — امتلاء قاعدة البيانات ومعدّل نموّها",
          "💰 /credit — استهلاك المعلّمات ومن تجاوزت حدّها",
          "📁 /files — ملخّص معالجة الملفات",
          "📈 /summary — الملخّص اليومي الكامل",
          "",
          "<b>المرادفات العربية</b> (تعمل بالكتابة، لكنّ تلغرام لا يسمح بعرضها في القائمة):",
          "/تقرير · /الحالة · /الحوادث · /الوكلاء · /التكلفة · /السعة · /رصيد · /ملفات · /ملخص",
          "",
          "أو اكتب أي سؤالٍ بأسلوبك الخاص مباشرةً — مثلاً:",
          "«لماذا لم يُصلَح النظام مشكلة كذا؟»",
          "«هل يوجد شيءٌ يستحقّ انتباهي الآن؟»",
        ].join("\n"));
        return json({ ok: true });
      }

      if (isOpsBot && !text.startsWith("/")) {
        await askCopilotAndReply(text);
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
