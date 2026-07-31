// أدوات مشتركة لنداء الذكاء الاصطناعي عبر OpenRouter.
//
// تحلّ مشكلتين:
//  ١) الازدحام: حدّ الطلبات في الدقيقة مربوط بالحساب لا بالمفتاح، فلو ضغطت
//     عدّة معلّمات زرّ التوليد في اللحظة نفسها رُفض بعضها بـ 429. كان ذلك
//     يظهر للمعلّمة خطأً فورياً؛ صار الطلب ينتظر ويعيد المحاولة بهدوء.
//  ٢) النموذج الواحد لكل المهامّ: تلخيصٌ قصير كان يُنفَّذ بالنموذج نفسه الذي
//     تُبنى به خطّة درسٍ كاملة. صار لكل مهمّة مفتاحها في ai_settings.

// أخطاء تستحقّ إعادة المحاولة: ازدحام (429) أو عطل مؤقّت عند المزوّد (5xx).
// أما 4xx الأخرى فخطأٌ في الطلب نفسه، وإعادته تكرّر الفشل وتضيّع الوقت.
function worthRetry(status: number) {
  return status === 429 || (status >= 500 && status < 600);
}

// سقفٌ إجمالي محافظ: دوالّ الحافة عندها مهلة تنفيذ، فطول الانتظار يعني
// انقطاعاً بلا نتيجة — وهو أسوأ للمعلّمة من رسالة خطأٍ سريعة.
const MAX_ATTEMPTS = 3;
const MAX_WAIT_MS = 9000;

function waitMs(attempt: number, retryAfter: string | null) {
  // المزوّد أدرى بموعد انفراج الازدحام، فرأيه مقدَّم على حسابنا.
  const ra = parseFloat(retryAfter || "");
  if (isFinite(ra) && ra > 0) return Math.min(ra * 1000, MAX_WAIT_MS);
  // تباعدٌ أُسّي مع تشويشٍ عشوائي: بدونه ترتدّ الطلبات المرفوضة كلها في
  // اللحظة نفسها فتصنع ازدحاماً ثانياً بدل أن تنفرج.
  const base = 1200 * Math.pow(2, attempt - 1);
  return Math.min(base + Math.random() * 400, MAX_WAIT_MS);
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

// بديلٌ مباشر عن fetch لنداءات OpenRouter — نفس التوقيع ونفس المخرَج،
// فلا يحتاج ما بعده أيّ تغيير.
export async function orFetch(url: string, init: RequestInit): Promise<Response> {
  let last: Response | null = null;
  const started = Date.now();
  for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
    let r: Response;
    try {
      r = await fetch(url, init);
    } catch (e) {
      // انقطاع شبكة بين الحافة والمزوّد — يستحقّ محاولةً أخرى.
      if (attempt === MAX_ATTEMPTS) throw e;
      await sleep(waitMs(attempt, null));
      continue;
    }
    if (r.ok || !worthRetry(r.status) || attempt === MAX_ATTEMPTS) return r;
    const d = waitMs(attempt, r.headers.get("retry-after"));
    // لا نبدأ انتظاراً يتجاوز ميزانية الوقت المتبقّية بلا طائل.
    if (Date.now() - started + d > MAX_WAIT_MS * 2) return r;
    console.warn(`openrouter ${r.status} — إعادة المحاولة ${attempt}/${MAX_ATTEMPTS} بعد ${d}ms`);
    // نستهلك الجسم كي لا يتسرّب الاتصال، ونحتفظ بآخر ردٍّ للطوارئ.
    try { await r.text(); } catch { /* تجاهُل */ }
    last = r;
    await sleep(d);
  }
  return last!;
}

// اختيار النموذج حسب المهمّة.
// الترتيب: مفتاح المهمّة → الإعداد العام (ai_model) → الافتراضي.
// أُبقي ai_model قبل الافتراضي عمداً: المشرفة ضبطته صراحةً، فتجاهله يغيّر
// جودة المخرجات في منصّةٍ حيّة بلا إذنها. الاقتصاد يبدأ حين تضبط مفاتيح المهامّ.
export function pickModel(
  st: Record<string, string>,
  task: string,
  fallback: string,
): string {
  return st["model_" + task] || st.ai_model || fallback;
}

// مثلها للمهامّ التي تقرأ صور صفحات الكتاب — لا يجوز أن تسقط إلى نموذجٍ نصّي،
// لأنه يُسقط الصور بصمت فيخرج الدرس من معرفةٍ عامة لا من الكتاب المعتمد.
export function pickVisionModel(
  st: Record<string, string>,
  task: string,
  fallback: string,
): string {
  return st["model_" + task] || st.vision_model || fallback;
}
