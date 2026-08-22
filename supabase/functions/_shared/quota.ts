// حصّة استخدام الذكاء الاصطناعي — تُفرض على الخادم (لا يمكن تجاوزها من المتصفح)
// kind: 'text' (خطط/اختبارات/محادثة...) أو 'img' (إنفوجرافيك/شرائح مرسومة)
//       أو 'search' (بحث الويب داخل المحادثة) — يُستعمل الآن فقط للتصنيف في
//       ai_cost_log، لا لحدٍّ منفصل. المشرف بلا حدود.
//
// ⚠️ P1 (٢٠٢٦-٠٨-١٩): استُبدلت الحدود الثلاثة المنفصلة (quota_text/img/search
// كعددٍ خام) بحصّةٍ نقديةٍ موحّدة (budget_omr) تُستهلك بحرّية عبر أي مزيج.
// الفحصُ الآن غير ذرّي عمداً: يقرأ مجموع ai_cost_log.cost_usd منذ
// budget_period_start ويقارنه بالحصّة *قبل* النداء. لا خصمٌ مسبق ولا استرجاع
// — التكلفة الحقيقية تُعرَف فقط بعد نجاح النداء (logAiCost)، فلا شيء
// "يُؤخَذ" مقدَّماً كي يُرَدّ عند الفشل. هذا يعني نداءً واحداً يتجاوز الحصّة
// قد يمرّ (القرار الإداري: تُكمَل العملية الجارية ثم تُرفض التالية) —
// مقبولٌ صراحةً هنا: سقفٌ ناعم لا حارسٌ ماليٌّ صارم.
//
// ٢ الفشلُ يبقى مغلقاً (fail-closed): عطلٌ في القراءة يمنع النداء، لا يُلغي
//   الحصّة.

const ADMIN_EMAIL = "teacherplane2026project@gmail.com";

export interface QuotaResult { ok: boolean; used: number; limit: number; error?: string }

// دفاعٌ إضافي فوق الحصة الشهرية: نداءان من المستخدمة نفسها أقرب من هذه
// المهلة يُرفض ثانيهما بصرف النظر عن الحصة المتبقية — يمنع ذروةً لحظية
// من ضغطةٍ متكررة أو تبويباتٍ متعددة، لا يستبدل take_quota.
const RATE_LIMIT_MS = 2000;

// deno-lint-ignore no-explicit-any
export async function takeQuota(
  admin: any,
  userId: string,
  email: string,
  kind: "text" | "img" | "search",
  st: Record<string, string>,
  // نداءٌ ثانٍ من نفس الطلب (مثلاً فحص "img" بعد فحص "text" العام، أو
  // فحص "search" بعد أيٍّ منهما) لا يجوز أن يصطدم بحدّ المعدّل — هذا الحدّ
  // مصمَّمٌ لمنع طلباتٍ متكرّرة من المستخدمة نفسها، لا لمنع طلبٍ واحدٍ
  // يحتاج أكثر من فحص حصّةٍ داخلياً. بلا هذا الخيار كانت أي رسالة تطلب
  // صورةً أو بحثاً تُرفض بخطأ "نفد رصيدك" الكاذب لأن الفحص الثاني يقع
  // خلال أقلّ من RATE_LIMIT_MS من الأول.
  opts?: { skipRateLimit?: boolean },
): Promise<QuotaResult> {
  if ((email || "").toLowerCase() === ADMIN_EMAIL) return { ok: true, used: 0, limit: 0 };

  if (!opts?.skipRateLimit) {
    try {
      const { data: allowed, error: rlErr } = await admin.rpc("check_ai_rate_limit", {
        p_user: userId, p_min_ms: RATE_LIMIT_MS,
      });
      // الدالة قد لا تكون منشورةً بعد (مرحلة انتقالية كما في take_quota) —
      // عطلٌ هنا لا يمنع التوليد، فهذه طبقةٌ إضافية لا حارسٌ وحيد.
      if (!rlErr && allowed === false) {
        return { ok: false, used: 0, limit: 0, error: "rate_limited" };
      }
    } catch (_e) { /* طبقةٌ إضافية: تجاهل عطلها ولا نمنع التوليد بسببه */ }
  }

  const budgetOmr = parseFloat(st["budget_omr"] || "") || 13;
  const rate = parseFloat(st["usd_omr_rate"] || "") || 0.3845;
  const budgetUsd = budgetOmr / rate;

  try {
    // الحصّة تُقاس منذ تفعيل حساب هذه المعلّمة تحديداً (allowed_emails.
    // added_at) — توافقاً مع مدّة اشتراكها (٥ أشهر)، لا من تاريخٍ عامٍّ واحد
    // لكل المعلّمات (انظر 20260819_p30_budget_per_account_period.sql).
    const { data: acc } = await admin
      .from("allowed_emails")
      .select("added_at")
      .ilike("email", email)
      .maybeSingle();
    const periodStart = acc?.added_at
      ? String(acc.added_at).slice(0, 10)
      : (st["budget_period_start"] || "2026-01-01");

    const { data, error } = await admin
      .from("ai_cost_log")
      .select("cost_usd")
      .eq("user_id", userId)
      .gte("created_at", periodStart + "T00:00:00Z");
    if (error) throw error;

    const used = (data || []).reduce(
      (s: number, r: { cost_usd: number | null }) => s + (r.cost_usd || 0), 0,
    );
    if (used >= budgetUsd) {
      return { ok: false, used, limit: budgetUsd, error: "budget_exhausted" };
    }
    return { ok: true, used, limit: budgetUsd };
  } catch (e) {
    console.error("quota check failed (fail-closed):", String((e as { message?: string })?.message || e));
    // مغلقٌ عند الفشل: لا نداءَ للذكاء الاصطناعي ما لم نتأكّد من وجود رصيد.
    return { ok: false, used: 0, limit: budgetUsd, error: "quota_unavailable" };
  }
}

// ═══ KHOTTA Autonomous Management — Phase 0 ═══
// تسجيل تكلفة النداء الحقيقية — قراءةٌ صرفة، لا تمسّ الحصة ولا التقييد.
// المصدر الوحيد للتكلفة هو usage.cost القادم من OpenRouter نفسه؛ لا تقدير
// ولا جدول أسعار محليّ. NULL صراحةً إن غاب الرقم أو كان غير صالح — لا
// نخترع صفراً ولا أي قيمةٍ بديلة.
//
// ⚠️ استقلاليةٌ متعمَّدة: يُستدعى بعد نجاح استجابة الذكاء الاصطناعي
// (المكان الوحيد الذي يُعرَف فيه usage.cost أصلاً)، لا من داخل takeQuota
// أو refundQuota — هاتان تعملان قبل نداء المزوّد ولا تريان استجابته إطلاقاً.
// فشل التسجيل هنا لا يُرجع خطأً ولا يُلقي استثناءً: توليد الذكاء الاصطناعي
// أولى بالنجاح من هذا السجل التحليليّ — نكتفي بـconsole.error لرصد العطل.
// ⚠️ Phase 2: kind تضمّ الآن 'ops' — نداءات ops-analyze/ops-copilot
// التحليلية، لا تخصّ معلّمةً بعينها. get_ai_cost() يفرزها بمعزلٍ عن
// تكلفة المستخدمين بهذه القيمة تحديداً — لا تُستعمَل 'ops' لغير ذلك.
// userId قد يكون null لنداءٍ تُطلقه وكيلٌ مجدولة بلا مستخدمٍ محدَّد.
// deno-lint-ignore no-explicit-any
export async function logAiCost(
  admin: any,
  userId: string | null,
  functionName: string,
  kind: "text" | "img" | "search" | "ops",
  model: string | null | undefined,
  usage: unknown,
  // Phase 1.5 — القسم 8: run_id اختياري يربط سطر التكلفة بتشغيلة agent_runs
  // (ops-analyze/ops-copilot فقط، لهما agent_runs الآن) — undefined/null لا
  // يغيّر أي سلوكٍ قائم، فيبقى استدعاء generate-* وغيرها بلا هذا المعامل صحيحاً.
  runId?: string | null,
): Promise<void> {
  try {
    const u = usage as { cost?: unknown } | null | undefined;
    const cost = u && typeof u.cost === "number" && isFinite(u.cost) ? u.cost : null;
    const { error } = await admin.from("ai_cost_log").insert({
      user_id: userId,
      function_name: functionName,
      kind,
      model: model || null,
      cost_usd: cost,
      run_id: runId ?? null,
    });
    if (error) console.error(`ai_cost_log: تعذّر التسجيل (${functionName}):`, error.message);
  } catch (e) {
    console.error(`ai_cost_log: استثناءٌ أثناء التسجيل (${functionName}):`, String(e));
  }
}

// لا خصمَ مقدَّماً بعد التحوّل إلى الحصّة النقدية (انظر تعليق takeQuota
// أعلاه) — التكلفة تُسجَّل فقط بعد نجاحٍ فعلي عبر logAiCost، فتوليدٌ فاشل
// لا يترك أي أثرٍ في ai_cost_log أصلاً ولا شيء يحتاج استرجاعاً. أُبقيت
// الدالة بلا حذفٍ (بلا تنفيذٍ فعلي) كي لا تنكسر نداءاتها القائمة في دوالّ
// الحافة الأخرى أثناء الانتقال — تُحذف نهائياً بعد التأكد من إزالة كل نداء.
// deno-lint-ignore no-explicit-any
export async function refundQuota(
  _admin: any,
  _userId: string,
  _email: string,
  _kind: "text" | "img" | "search",
): Promise<void> {
  // no-op عمداً
}
