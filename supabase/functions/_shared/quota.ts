// حصص استخدام الذكاء الاصطناعي — تُفرض على الخادم (لا يمكن تجاوزها من المتصفح)
// kind: 'text' (خطط/اختبارات/محادثة...) أو 'img' (إنفوجرافيك/شرائح مرسومة)
//       أو 'search' (بحث الويب داخل المحادثة)
// الحدود من ai_settings: quota_text و quota_img و quota_search.
// المشرف بلا حدود.
//
// ⚠️ تغيُّران جوهريان (P0):
//  ١ الخصمُ صار ذرّيّاً عبر RPC ‏take_quota — كان قراءةً ثم كتابةً منفصلتين،
//    فعشرة طلباتٍ متزامنة على آخر نقطةٍ تمرّ كلُّها والعدّاد يزيد واحداً.
//  ٢ الفشلُ صار مغلقاً (fail-closed) لا مفتوحاً — كان أيُّ عطلٍ في القاعدة
//    يُرجع ok:true فيُلغي الحصص كلَّها مدّة العطل، وهو بابُ استنزافٍ يُفتح
//    بمجرّد إثقال القاعدة. والمالُ لا يُنفَق على شكٍّ.

const ADMIN_EMAIL = "teacherplane2026project@gmail.com";

// الافتراضيات مطابقةٌ لما هو مثبَّت في ai_settings الآن (٦٥ / ٦٠٠ / ١٢٥).
// كانت img=200 هنا و80 في التعليق أعلاه و65 في القاعدة — ثلاثة أرقام لشيءٍ
// واحد. تُقرأ الحدود من ai_settings دائماً، وهذه شبكةُ أمانٍ لا أكثر.
const QK: Record<string, string> = { img: "quota_img", search: "quota_search", text: "quota_text" };
const DEF: Record<string, number> = { img: 65, search: 125, text: 600 };

export interface QuotaResult { ok: boolean; used: number; limit: number; error?: string }

// deno-lint-ignore no-explicit-any
export async function takeQuota(
  admin: any,
  userId: string,
  email: string,
  kind: "text" | "img" | "search",
  st: Record<string, string>,
): Promise<QuotaResult> {
  if ((email || "").toLowerCase() === ADMIN_EMAIL) return { ok: true, used: 0, limit: 0 };

  const month = new Date().toISOString().slice(0, 7);
  const limit = parseInt(st[QK[kind]] || "") || DEF[kind];

  try {
    const { data, error } = await admin.rpc("take_quota", {
      p_user: userId, p_month: month, p_kind: kind, p_limit: limit,
    });
    if (error) throw error;

    // الدالة تُرجع صفّاً واحداً: {allowed, used, lim}
    const row = Array.isArray(data) ? data[0] : data;
    if (!row || typeof row.allowed !== "boolean") {
      throw new Error("take_quota أعادت شكلاً غير متوقَّع");
    }
    return { ok: row.allowed, used: row.used ?? 0, limit: row.lim ?? limit };
  } catch (e) {
    const msg = String((e as { message?: string })?.message || e);

    // مرحلةٌ انتقالية: الدوال تُنشر تلقائياً عند الدفع، والهجرة تُنفَّذ يدوياً.
    // فبين اللحظتين لا وجود لـ take_quota، ولو أغلقنا هنا لتوقّف كلُّ توليدٍ
    // عند كلِّ معلّمة — انقطاعٌ كامل ثمناً لإصلاح. فنسقط إلى المسلك القديم
    // (غيرِ الذرّي) في هذه الحالة وحدها: لا أسوأ من اليوم، ويصير ذرّيّاً
    // لحظةَ تنفيذ الهجرة. يُحذف هذا الفرع بعد التأكّد من تنفيذها.
    if (/does not exist|42883|Could not find the function|schema cache/i.test(msg)) {
      console.error("⚠️ take_quota غير موجودة — نفّذ 20260816_p0_quota_atomic.sql. مسلكٌ مؤقّت غير ذرّي.");
      try {
        const { data, error } = await admin.from("ai_usage").select("count")
          .eq("user_id", userId).eq("month", month).eq("kind", kind).maybeSingle();
        if (error) throw error;
        const used = data?.count || 0;
        if (used >= limit) return { ok: false, used, limit };
        if (data) {
          await admin.from("ai_usage").update({ count: used + 1 })
            .eq("user_id", userId).eq("month", month).eq("kind", kind);
        } else {
          await admin.from("ai_usage").insert({ user_id: userId, month, kind, count: 1 });
        }
        return { ok: true, used: used + 1, limit };
      } catch (e2) {
        console.error("legacy quota path failed (fail-closed):", String(e2));
        return { ok: false, used: 0, limit, error: "quota_unavailable" };
      }
    }

    console.error("quota check failed (fail-closed):", msg);
    // مغلقٌ عند الفشل: لا نداءَ للذكاء الاصطناعي ما لم نتأكّد من وجود رصيد.
    return { ok: false, used: 0, limit, error: "quota_unavailable" };
  }
}

// إعادةُ ما خُصم عند فشل التوليد.
// الخصم يقع قبل النداء كي لا يُتجاوز الحدّ بطلباتٍ متوازية، لكن المعلمة كانت
// تُحاسَب على توليدٍ لم تستلمه: ست محاولاتٍ فاشلة لعرضٍ واحد تلتهم ستّاً من
// حصتها بلا مخرَج واحد.
// GREATEST(count-1,0) في الدالة يمنع النزول تحت الصفر مهما تزامنت النداءات.
// deno-lint-ignore no-explicit-any
export async function refundQuota(
  admin: any,
  userId: string,
  email: string,
  kind: "text" | "img" | "search",
): Promise<void> {
  if ((email || "").toLowerCase() === ADMIN_EMAIL) return;
  const month = new Date().toISOString().slice(0, 7);
  try {
    const { error } = await admin.rpc("refund_quota", {
      p_user: userId, p_month: month, p_kind: kind,
    });
    if (error) throw error;
  } catch (e) {
    // الاسترجاع اجتهادي: فشله يترك خصماً زائداً، وهو أهون من منع الردّ
    console.error("quota refund failed", String((e as { message?: string })?.message || e));
  }
}
