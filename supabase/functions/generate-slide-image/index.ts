// v2026.07.09 ════════════════════════════════════════════════════════════════
// Edge Function: generate-slide-image
// يرسم شريحة عرض تقديمي واحدة (16:9) بالكامل بالذكاء الاصطناعي
// بأسلوب NotebookLM — تُستدعى مرة لكل شريحة من واجهة المولّد.
// النموذج: Gemini 3 Pro Image (Nano Banana Pro) عبر OpenRouter.
//
// النشر:  supabase functions deploy generate-slide-image
// الأسرار: OPENROUTER_API_KEY (نفس مفتاح بقية الدوال)
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { takeQuota, refundQuota } from "../_shared/quota.ts";
import { orFetch, orErrCode } from "../_shared/ai.ts";

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

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) return json({ error: "unauthorized" }, 401);
    const admin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );
    const jwt = authHeader.replace("Bearer ", "");
    const { data: { user }, error: userErr } = await admin.auth.getUser(jwt);
    if (userErr || !user) return json({ error: "unauthorized" }, 401);

    const apiKey = Deno.env.get("OPENROUTER_API_KEY");
    if (!apiKey) return json({ error: "server_not_configured" }, 500);

    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
    if (st.generator_enabled === "0") return json({ error: "disabled" }, 403);

    // ⛔ حصة الاستخدام الشهرية — تُفرض على الخادم
    const quota = await takeQuota(admin, user.id, user.email || "", "img", st);
    if (!quota.ok) return json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);
    // كل مخرجٍ بخطأٍ بعد هذه النقطة يستردّ ما خُصم: المعلمة لا تُحاسَب
    // على توليدٍ لم تستلمه.
    const refund = async (body: Record<string, unknown>, status: number) => {
      await refundQuota(admin, user.id, user.email || "", "img");
      return json(body, status);
    };

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const title = String(b.title || "").slice(0, 200);
    const bullets: string[] = (Array.isArray(b.bullets) ? b.bullets : []).map(String).slice(0, 8);
    const slideNo = Math.max(1, parseInt(b.slideNo) || 1);
    const slideTotal = Math.max(1, parseInt(b.slideTotal) || 1);
    const kind = ["cover", "content", "closing"].includes(b.kind) ? b.kind : "content";
    // عنوان احتياطي بدل إفشال الشريحة إن جاء العنوان فارغاً
    const safeTitle = title || (kind === "closing" ? "شكراً لكم" : subject || `شريحة ${slideNo}`);

    // ── وضع الخلفية المحجوزة (العرض الهجين) ──
    // reserveText يصف منطقةً يجب أن تبقى فارغة تماماً لأن الواجهة ستضع النص
    // فوقها بإحداثياتٍ مطابقة. في هذا الوضع لا يُكتب أي نصٍّ داخل الصورة
    // إطلاقاً: النص طبقةُ HTML فوقها، وكتابته مرّتين تعني ازدواجاً مقروءاً.
    const reserveText = String(b.reserveText || "").slice(0, 400);
    const imagePrompt = String(b.imagePrompt || "").slice(0, 500);
    const reserveMode = !!reserveText;

    // نموذج الرسم الموحّد — يُبدَّل من ai_settings (مفتاح slide_model) بدون نشر
    const model = st.model_slide_image || st.slide_model || "google/gemini-2.5-flash-image";

    // ── الجمهور يحكم التصميم ──
    // هؤلاء أطفال ٧-١٠ سنوات، وكثيرٌ منهم في الصف الأول والثاني لا يقرأ بعد.
    // النسخة السابقة كانت مخططاً اصطلاحياً مكتظّاً بالتسميات الصغيرة على نمط
    // NotebookLM — وهو تصميمٌ لقارئٍ بالغ لا لطفلٍ يتهجّى. وكانت تمنع الوجوه
    // والشخصيات صراحةً، وهي بالضبط ما يجذب هذا العمر ويُفهمه.
    // فالقاعدة الآن: الرسم يحمل المعنى وحده، والمكتوب سطرٌ واحد كبير تقرأه
    // المعلّمة بصوتها. وهذا يخدم غير القارئ ويقلّص مساحة الخطأ الإملائي معاً.
    const style = st.slide_style_prompt || [
      "شريحة عرض تعليمية عريضة (16:9) لأطفال المرحلة الابتدائية الدنيا — كثيرٌ منهم لا يقرأ بعد، فالرسم هو الشرح كلّه والنص مساعدٌ ثانوي.",
      "الرسم يملأ الشريحة ويُفهم بالنظر وحده دون قراءة حرفٍ واحد: مشهدٌ واحد كبير واضح، لا مخططاً اصطلاحياً ولا شبكة صناديق وأسهم.",
      "أسلوب الرسم: رسوم أطفال ودودة ملوّنة بخطوط خارجية واضحة، شخصيات مبتسمة بوجوه بسيطة معبّرة (طفل/طفلة عُمانية بالزي المدرسي) وأشياء مألوفة من بيت الطفل وصفّه — الجاذبية مقصودة لا زخرفة.",
      "ألوان دافئة زاهية مبهجة عالية التباين، وخلفية فاتحة نظيفة. تجنّب الألوان الباهتة والأسلوب الرسمي الجاف.",
      "الحجم من أجل شاشة الصف: العناصر كبيرة تُرى من آخر الفصل، بلا تفاصيل دقيقة ولا عناصر صغيرة مزدحمة.",
      // ── حدُّ النص: سببه مزدوج ──
      // (١) غير القارئ لا ينتفع بتسميةٍ مكتوبة أصلاً.
      // (٢) التجربة الحيّة أظهرت أن النموذج حين يخترع تسميات يُخطئ إملائياً
      //     («يمشأ» بدل «يملأ») ويُكرّر العبارة مرتين. حصرُ المكتوب في سطرٍ
      //     واحد راجعَه نموذجٌ نصّيٌّ سلفاً يكاد يُلغي هذا الخطر.
      "النص المكتوب في الصورة هو العنوان وحده لا غير: سطرٌ واحد أعلى الشريحة بخطٍّ عربيٍّ ضخمٍ عريضٍ واضح. المعلّمة تقرأه بصوتها للأطفال.",
      "ممنوع منعاً تاماً كتابة أي تسميات أو جملٍ أو شروحٍ أو صناديق ملاحظاتٍ أو أرقامٍ داخل الرسم. النقاط المذكورة أدناه تُترجَم إلى عناصر مرسومة يفهمها الطفل بالنظر — ولا تُكتب حروفاً أبداً.",
      "إن لم تكن واثقاً من إملاء كلمةٍ عربية فاحذفها: رسمٌ صامتٌ خيرٌ من كلمةٍ مغلوطة أمام الأطفال.",
      "الهوية العُمانية حصراً إن ظهرت أزياء أو مبانٍ (الزي المدرسي العُماني، الكمة والدشداشة) — لا مظاهر أي دولة خليجية أخرى.",
      "لا صور فوتوغرافية ولا حشو زخرفي.",
    ].join(" ");

    const kindPrompt = kind === "cover"
      ? `هذه شريحة الغلاف: العنوان ضخمٌ في الأعلى، وتحته مشهدٌ مرحٌ جذّاب عن الموضوع يشوّق الأطفال إليه.`
      : kind === "closing"
        ? "هذه الشريحة الختامية: مشهدٌ دافئ مبهج يلخّص الدرس ويُشعر الأطفال بالإنجاز (أطفال فرحون بما تعلّموه)."
        : "هذه شريحة محتوى: العنوان سطراً واحداً في الأعلى، وتحته مشهدٌ واحد كبير يجسّد معنى النقاط بالرسم وحده — يفهمه طفلٌ لا يقرأ.";

    // نمطٌ بصريٌّ مستقلّ لوضع الخلفية المحجوزة: هنا الصورة خلفيةٌ لا شريحة
    // مكتملة، فتعليمات «اكتب العنوان أعلى الشريحة» أعلاه تُناقض الغرض
    const reserveStyle = [
      "خلفية شريحة عرض تعليمية عريضة (16:9) لطلاب المرحلة الابتدائية.",
      `شرطٌ مطلق لا يجوز خرقه: ${reserveText}. هذه المنطقة ستُوضع فوقها كتابةٌ لاحقاً، فأي رسمٍ أو خطٍّ أو تفصيلٍ فيها يُفسد الشريحة.`,
      "لا تكتب أي نصٍّ أو حرفٍ أو رقمٍ داخل الصورة إطلاقاً — لا عناوين ولا تسميات ولا أرقام صفحات. الصورة رسمٌ صامتٌ بحت.",
      "أسلوب الرسم: مسطح بخطوط خارجية رفيعة داكنة (hand-drawn flat)، أشياء واقعية مألوفة للطالب من بيئته — بلا وجوه ولا شخصيات كرتونية ولا رموز تعبيرية.",
      "لونان رئيسيان هادئان متمايزان على خلفيةٍ فاتحة دافئة (أبيض مائل للكريمي)، بلمساتٍ محايدة.",
      "الهوية العُمانية حصراً إن ظهرت أزياء أو مبانٍ (الزي المدرسي العُماني، الكمة والدشداشة) — لا مظاهر أي دولة خليجية أخرى.",
      "لا صور فوتوغرافية ولا حشو زخرفي.",
    ].join(" ");

    const userPrompt = reserveMode
      ? [
        `ارسم خلفية شريحة عرض تعليمية واحدة (الشريحة ${slideNo} من ${slideTotal}) لمادة ${subject}${grade ? " للصف " + grade : ""}.`,
        imagePrompt ? `المشهد المطلوب توضيحه: ${imagePrompt}` : `موضوع الشريحة: ${safeTitle}`,
        reserveStyle,
      ].filter(Boolean).join("\n")
      : [
        `ارسم شريحة عرض تقديمي تعليمية واحدة (الشريحة ${slideNo} من ${slideTotal}) لمادة ${subject}${grade ? " للصف " + grade : ""}.`,
        kindPrompt,
        `العنوان — وهو النص الوحيد المكتوب في الصورة، اكتبه حرفياً: «${safeTitle}»`,
        bullets.length
          ? `المعاني التي يجب أن يجسّدها الرسم (ترجمها إلى عناصر مرسومة — لا تكتب أياً منها حروفاً):\n${bullets.map((x) => `- ${x}`).join("\n")}`
          : "",
        style,
      ].filter(Boolean).join("\n");

    // إن رفض النموذج إعداد المقاس نعيد المحاولة بدونه بدل إفشال الشريحة
    const call = (cfg: Record<string, unknown> | null) =>
      orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Visual Slides",
        },
        body: JSON.stringify({
          model,
          messages: [{ role: "user", content: userPrompt }],
          modalities: ["image", "text"],
          ...(cfg ? { image_config: cfg } : {}),
        }),
      }, { st, task: "slide_image" });
    let img = "";
    let usage: unknown = null;
    if (model.startsWith("google/")) {
      let orResp = await call({ aspect_ratio: "16:9" });
      let or = await orResp.json();
      if (!orResp.ok) { orResp = await call(null); or = await orResp.json(); }
      if (!orResp.ok) {
        const _m = String(or?.error?.message || or?.message || "");
        console.error(`openrouter ${orResp.status} في generate-slide-image: ${_m}`);
        return refund({ error: orErrCode(orResp.status, _m), detail: _m.slice(0, 200) }, 502);
      }
      const msg = or?.choices?.[0]?.message;
      img = msg?.images?.[0]?.image_url?.url || "";
      usage = or?.usage || null;
      if (!img) return refund({ error: "no_image", detail: msg?.content || null }, 502);
    } else {
      // النماذج غير جوجل (مثل Seedream) عبر واجهة الصور الموحدة /v1/images
      const r = await orFetch("https://openrouter.ai/api/v1/images", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Visual Slides",
        },
        // Seedream يشترط حداً أدنى كبيراً للبكسلات وسعره ثابت — نرسل دائماً 4K
        body: JSON.stringify({ model, prompt: userPrompt, resolution: "4K", aspect_ratio: "16:9" }),
      }, { st, task: "slide_image" });
      const j = await r.json();
      if (!r.ok) {
        const _m = String(j?.error?.message || j?.message || "");
        console.error(`openrouter ${r.status} في generate-slide-image: ${_m}`);
        return refund({ error: orErrCode(r.status, _m), detail: _m.slice(0, 200) }, 502);
      }
      const d = j?.data?.[0] || {};
      img = d.b64_json ? "data:image/png;base64," + d.b64_json : (d.url || "");
      if (!img) return refund({ error: "no_image", detail: j }, 502);
    }

    return json({ image: img, model, usage });
  } catch (e) {
    // لا استرداد هنا: قد يقع الخطأ قبل تعريف refund أصلاً (وقبل خصم الحصّة)
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
