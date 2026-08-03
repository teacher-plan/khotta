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

// ═══ مفاتيح متعدّدة ═══
// مفتاحٌ واحد يعني نقطة انهيارٍ واحدة: نفاد رصيده أو تعطّل حسابه يوقف المنصّة
// كلَّها — وهو ما وقع فعلاً. المفاتيح الإضافية اختيارية: يُقرأ ما وُجد منها.
// وتوزيع المهامّ عليها يعزل الأعطال أيضاً: خللٌ في مفتاح الصور لا يُسكت المحادثة.
const KEY_ENV = ["OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2", "OPENROUTER_API_KEY_3", "OPENROUTER_API_KEY_4"];

// الخانات بمواضعها لا مضغوطة: رقم المفتاح مرتبطٌ باسم المتغيّر لا بترتيب
// الموجود. لو أُضيف _3 دون _2 لصار مفتاح الشرائح يعمل بمفتاح الإنفوجرافيك
// بلا أن يظهر شيء — إسنادٌ خاطئ صامت، وهو أسوأ من غياب المفتاح.
export function orKeySlots(): (string | null)[] {
  const seen = new Set<string>();
  return KEY_ENV.map((name) => {
    const v = (Deno.env.get(name) || "").trim();
    if (!v || seen.has(v)) return null;
    seen.add(v);
    return v;
  });
}

export function orKeys(): string[] {
  return orKeySlots().filter((k): k is string => !!k);
}

// عطلٌ يخصّ المفتاح نفسه لا الطلب: انتهاء صلاحية (401)، نفاد رصيد (402)،
// حظر (403)، أو بلوغ حدّ الحساب (429). عندها لا معنى لإعادة المحاولة بالمفتاح
// ذاته — ننتقل إلى التالي فوراً.
function keyFault(status: number) {
  return status === 401 || status === 402 || status === 403 || status === 429;
}

// ═ مجموعات المهامّ ═
// أربع مجموعاتٍ بدل أربع عشرة مهمّة: ضبطُ كلٍّ على حدة بابُ خطأ، والتقسيم
// المنطقي يجمع ما يتعطّل معاً ويفصل ما يجب أن ينجو منفرداً.
//  ١ التحضير: الخطة والمحادثة والألعاب وقراءة الكتاب — قلب عمل المعلّمة اليومي.
//  ٢ الإنفوجرافيك: أغلى بندٍ وأكثره استهلاكاً، فعزله يقي البقية من نفاده.
//  ٣ الشرائح: العرض المصوَّر وصوره.
//  ٤ الإدارة: تقطيع الكتب والاختبارات وكشوف الأسماء — عملٌ ثقيل يجري مرّةً
//    واحدة، ولا يصحّ أن يستهلك رصيد الصفّ اليومي.
const KEY_GROUP: Record<string, number> = {
  plan: 1, plan_vision: 1, chat: 1, chat_vision: 1, game: 1, game_vision: 1, summary: 1,
  infographic: 2,
  slides: 3, slide_image: 3, presentation: 3,
  extract: 4, segment: 4, exam: 4, exam_vision: 4, game_theme: 4, roster: 4,
};

// ترتيب المفاتيح لمهمّةٍ بعينها: ما يختاره المشرف أولاً، ثم مجموعتها، ثم
// الباقي احتياطاً — فالتحوّل التلقائي يبقى قائماً مهما كان التقسيم.
// key_<task> في ai_settings يتقدّم على المجموعة، فيبقى الضبط الدقيق ممكناً.
export function keyOrder(st: Record<string, string>, task?: string): string[] {
  const keys = orKeys();
  if (!task || keys.length < 2) return keys;
  const slots = orKeySlots();
  const explicit = parseInt(st["key_" + task] || "") || 0;
  const group = parseInt(st["keygrp_" + (KEY_GROUP[task] || 0)] || "") || KEY_GROUP[task] || 0;
  // خانةٌ فارغة تعني أن المفتاح لم يُضَف بعد: نسقط إلى الترتيب الطبيعي بدل
  // تعطيل المهمّة، ولا نأخذ مفتاح خانةٍ أخرى ظنّاً أنه المقصود.
  for (const pick of [explicit, group]) {
    const first = pick >= 1 && pick <= slots.length ? slots[pick - 1] : null;
    if (first) return [first, ...keys.filter((k) => k !== first)];
  }
  return keys;
}

function withKey(init: RequestInit, key: string): RequestInit {
  const h = new Headers(init.headers || {});
  h.set("Authorization", "Bearer " + key);
  return { ...init, headers: h };
}

export interface OrOpts { st?: Record<string, string>; task?: string }

// بديلٌ مباشر عن fetch لنداءات OpenRouter — نفس التوقيع ونفس المخرَج،
// فلا يحتاج ما بعده أيّ تغيير. يتنقّل بين المفاتيح عند عطلٍ يخصّها.
export async function orFetch(url: string, init: RequestInit, opts?: OrOpts): Promise<Response> {
  const keys = keyOrder(opts?.st || {}, opts?.task);
  // بلا مفاتيح في البيئة نمضي بما في الترويسة كما هي (توافقاً مع القديم)
  const pool: (string | null)[] = keys.length ? keys : [null];
  let last: Response | null = null;
  let lastErr: unknown = null;
  const started = Date.now();

  for (let ki = 0; ki < pool.length; ki++) {
    const key = pool[ki];
    const req = key ? withKey(init, key) : init;
    for (let attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
      let r: Response;
      try {
        r = await fetch(url, req);
      } catch (e) {
        lastErr = e;
        // انقطاع شبكة بين الحافة والمزوّد — يستحقّ محاولةً أخرى.
        if (attempt === MAX_ATTEMPTS) break;
        await sleep(waitMs(attempt, null));
        continue;
      }
      if (r.ok) return r;
      if (keyFault(r.status) && ki < pool.length - 1) {
        console.warn(`openrouter ${r.status} على المفتاح ${ki + 1} — الانتقال إلى ${ki + 2}`);
        try { await r.text(); } catch { /* تجاهُل */ }
        last = r;
        break;                              // مفتاحٌ آخر، بلا انتظار
      }
      if (!worthRetry(r.status) || attempt === MAX_ATTEMPTS) return r;
      const d = waitMs(attempt, r.headers.get("retry-after"));
      // لا نبدأ انتظاراً يتجاوز ميزانية الوقت المتبقّية بلا طائل.
      if (Date.now() - started + d > MAX_WAIT_MS * 2) return r;
      console.warn(`openrouter ${r.status} — إعادة المحاولة ${attempt}/${MAX_ATTEMPTS} بعد ${d}ms`);
      try { await r.text(); } catch { /* تجاهُل */ }
      last = r;
      await sleep(d);
    }
  }
  if (last) return last;
  throw lastErr || new Error("openrouter unreachable");
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

// عائلاتٌ نصّية معروفة لا تقرأ الصور. الضبط اليدويّ لأحدها في مهمّةٍ تقرأ
// صفحات الكتاب لا يُنتج خطأً: المزوّد يقبل الطلب ويُسقط الصور بصمت، فيؤلّف
// النموذج درساً من معرفته العامة ويظنّه أحدٌ مأخوذاً من الكتاب المعتمد.
// الخطأ الصامت أسوأ من الصاخب، فنمنعه هنا بدل انتظار من يلحظه.
const TEXT_ONLY_MODELS =
  /deepseek-(chat|v3|v4|r1)|tencent\/hy3|qwen3-30b|inclusionai\/|meituan\/|poolside\//i;

// حارسُ الرؤية: يُعيد النموذج المضبوط إن كان يقرأ الصور، وإلا عاد إلى
// الاحتياطيّ. يُلَفّ به كل سلسلة اختيارٍ في مهمّةٍ ترفق صوراً.
export function ensureVision(model: string, fallback: string): string {
  if (model && TEXT_ONLY_MODELS.test(model)) {
    console.warn("vision guard: " + model + " نصّيٌّ لا يقرأ الصور — رُدّ إلى " + fallback);
    return fallback;
  }
  return model || fallback;
}

// مثلها للمهامّ التي تقرأ صور صفحات الكتاب — لا يجوز أن تسقط إلى نموذجٍ نصّي،
// لأنه يُسقط الصور بصمت فيخرج الدرس من معرفةٍ عامة لا من الكتاب المعتمد.
export function pickVisionModel(
  st: Record<string, string>,
  task: string,
  fallback: string,
): string {
  return ensureVision(st["model_" + task] || st.vision_model || fallback, fallback);
}
