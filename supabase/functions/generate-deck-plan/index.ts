// v2026.08.09 ════════════════════════════════════════════════════════════════
// Edge Function: generate-deck-plan
// النصف النصّي من العرض التقديمي الهجين: يقرأ الدرس مرّةً واحدة ويُخرج لكل
// شريحة عنواناً ونقاطاً + اسم قالب تخطيط من قائمةٍ ثابتة تُرسلها الواجهة،
// + وصفاً بصرياً (imagePrompt) تُبنى منه خلفية الشريحة لاحقاً.
//
// لماذا القوالب الثابتة: صورةٌ تُولَّد توليدياً لا تلتزم بإحداثيات دقيقة مهما
// طُلب منها، فترك نموذج الصور يقرّر أين «يفرغ» مكاناً للنص يعني حتماً تراكب
// نصٍّ فوق رسمة في بعض الشرائح. هنا يختار النموذج النصّي قالباً معروف
// الإحداثيات للكود، فيرسم نموذجُ الصور داخل حدوده وتضع الواجهةُ النصَّ فوق
// المنطقة المحجوزة نفسها — الكود هو الضامن، لا اجتهاد النموذج.
//
// لا يولّد أي صورة: خصمه من حصّة النصّ (text) وحدها، والصور تُخصم لاحقاً
// عبر generate-slide-image مرّةً لكل شريحة.
//
// النشر: تلقائي عبر GitHub Actions
// الأسرار: OPENROUTER_API_KEY
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

// القوالب المسموح بها افتراضياً — الواجهة تُرسل قائمتها الفعلية، وهذه
// شبكة أمانٍ لو وصل الطلب بلا قائمة
const FALLBACK_LAYOUTS = ["right-text", "left-text", "top-text", "bottom-text"];

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

    const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
    if (!quota.ok) return json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);
    const refund = async (body: Record<string, unknown>, status: number) => {
      await refundQuota(admin, user.id, user.email || "", "text");
      return json(body, status);
    };

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const unit = String(b.unit || "");
    const lesson = String(b.lesson || "");
    if (!lesson) return refund({ error: "no_lesson" }, 400);
    const bookContext = String(b.bookContext || "").slice(0, 4000);
    const teacherPrompt = String(b.teacherPrompt || "").slice(0, 2000);
    const slideCount = Math.max(3, Math.min(10, parseInt(b.slideCount) || 6));
    const layouts: string[] = Array.isArray(b.layouts) && b.layouts.length
      ? b.layouts.map(String).slice(0, 12)
      : FALLBACK_LAYOUTS;

    const gradeNum = parseInt(grade) || 0;
    const age = gradeNum ? gradeNum + 6 : 0;
    const model = st.model_deck_plan || st.model_slides || st.ai_model || "google/gemini-2.5-flash";

    const schema = JSON.stringify({
      slides: [{
        title: "عنوان الشريحة قصير",
        bullets: ["نقطة قصيرة", "نقطة قصيرة"],
        layout: layouts[0],
        imagePrompt: "وصف المشهد البصري المطلوب رسمه لهذه الشريحة",
      }],
    });

    const system = [
      "أنت مصمم تعليمي خبير في سلطنة عُمان، تبني عرضاً تقديمياً قصيراً لصف من الحلقة الأولى (١-٤).",
      "المنهج المعتمد: منهج كامبردج (Cambridge) كما يطبَّق في مدارس سلطنة عُمان.",
      age ? `أعمار الطلاب: ${age} سنوات تقريباً (الصف ${grade}) — اللغة والأمثلة وطول الجمل تناسب هذا العمر بدقة، جمل قصيرة مباشرة.` : "المحتوى موجّه لطلاب المدرسة الابتدائية (٧-١٠ سنوات).",
      "المحتوى مقدَّم لطلاب داخل الصف، لا لمعلمين ولا لقرّاء بالغين.",
      bookContext
        ? `ملخص فعلي لمحتوى هذا الدرس من كتاب الطالب المعتمد — ابنِ كل شريحة من محتواه حصراً (المفاهيم، الأمثلة، الأرقام كما وردت):\n${bookContext}`
        : "لا ملخص كتابٍ مرفق — بناءً على خبرتك بمنهج كامبردج المعتمد في سلطنة عُمان لهذا الصف والمادة، توقّع المحتوى الفعلي المرجّح لهذا الدرس تحديداً (لا محتوى عام) وابنِ العرض عليه.",
      `ابنِ بالضبط ${slideCount} شرائح بتسلسل تربوي: الأولى غلافٌ بعنوان الدرس، ثم شرائح تشرح المفاهيم بتدرّج، ثم مثال أو تطبيق، والأخيرة خلاصة.`,
      "كل شريحة: عنوان قصير (٦ كلمات فأقل) + نقطتان إلى أربع نقاط قصيرة جداً (٨ كلمات لكل نقطة كحدٍّ أقصى). الشريحة تُعرض على شاشة صف، فالنص الطويل لا يُقرأ.",
      "شريحة الغلاف: العنوان فقط بلا نقاط (bullets مصفوفة فارغة).",
      "",
      "حقل layout — اختر لكل شريحة قالب تخطيطٍ واحداً من هذه القيم حصراً:",
      layouts.map((l) => `- ${l}`).join("\n"),
      "نوّع القوالب بين الشرائح ولا تُكرّر قالباً واحداً في كل العرض. القالب يحدّد أين سيوضع النص وأين تُرسم الصورة، فاختره بما يناسب المحتوى: النص الطويل نسبياً يناسبه قالبٌ جانبي، والعنوان وحده يناسبه قالبٌ علويّ أو سفليّ.",
      "",
      "حقل imagePrompt — وصفٌ عربيٌّ موجز (جملة إلى جملتين) للمشهد البصري التعليمي الذي يوضّح محتوى هذه الشريحة تحديداً: أشياء واقعية مألوفة للطالب من بيئته. لا تذكر فيه أي نصٍّ مكتوب ولا أرقاماً تُكتب داخل الصورة — الصورة خلفيةٌ توضيحية والنص يُركَّب فوقها بالكود.",
      "الهوية البصرية في imagePrompt: إن ذُكرت شخصيات أو أزياء أو مبانٍ فيجب أن تعكس الهوية العُمانية حصراً (الزي المدرسي العُماني، الكمة والدشداشة العُمانية) — لا مظاهر أي دولة خليجية أخرى.",
      "",
      "صُغ كل نص بالعربية الفصحى السليمة، بلا أي رموز تعبيرية (إيموجي).",
      "الأرقام دائماً بالترقيم العربي-الهندي (٠١٢٣٤٥٦٧٨٩) لا اللاتيني، وأي معادلة أو عملية حسابية تُكتب من اليمين إلى اليسار متوافقة مع اتجاه النص العربي.",
      `أعد الناتج JSON فقط بهذا الشكل حصراً: ${schema}`,
    ].filter(Boolean).join("\n");

    const userMsg = [
      `الصف: ${grade} | المادة: ${subject}`,
      unit ? `الوحدة: ${unit}` : "",
      `الدرس: ${lesson}`,
      `عدد الشرائح المطلوب: ${slideCount}`,
      teacherPrompt ? `توجيهات المعلمة: ${teacherPrompt}` : "",
    ].filter(Boolean).join("\n");

    const callOnce = async () => {
      const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model,
          messages: [
            { role: "system", content: system },
            { role: "user", content: userMsg },
          ],
          response_format: { type: "json_object" },
          temperature: 0.5,
          max_tokens: 2000,
        }),
      }, { st, task: "slides" });
      const j = await r.json();
      if (!r.ok) {
        return { ok: false as const, detail: j, status: r.status, msg: String(j?.error?.message || j?.message || "") };
      }
      const text = j?.choices?.[0]?.message?.content || "";
      let parsed: { slides?: unknown[] } | null = null;
      try { parsed = JSON.parse(text); }
      catch (_) {
        const m = text.match(/\{[\s\S]*\}/);
        try { parsed = m ? JSON.parse(m[0]) : null; } catch (_2) { parsed = null; }
      }
      // كل شريحةٍ ناقصة هنا تعني صورةً أقلّ عند المعلمة، والصور مدفوعة —
      // نرفض المخرَج الناقص ليُعاد الطلب بدل تمريره ثم اكتشافه في الواجهة
      if (!parsed || !Array.isArray(parsed.slides) || parsed.slides.length < slideCount) {
        return { ok: false as const, detail: String(text).slice(0, 300) };
      }
      return { ok: true as const, parsed, usage: j?.usage || null };
    };

    let attempt = await callOnce();
    if (!attempt.ok) attempt = await callOnce();
    if (!attempt.ok) {
      const st_ = (attempt as { status?: number }).status;
      const m_ = (attempt as { msg?: string }).msg || "";
      if (st_) {
        console.error(`openrouter ${st_} في generate-deck-plan: ${m_}`);
        return refund({ error: orErrCode(st_, m_), detail: m_.slice(0, 200) }, 502);
      }
      return refund({ error: "bad_output", detail: attempt.detail }, 502);
    }

    // تطهير المخرَج: قالبٌ خارج القائمة يعني نصاً يُركَّب في مكانٍ لم يُحجز
    // له فراغ في الصورة — نُرجعه إلى قالبٍ معروف بدل تمرير التراكب
    const allowed = new Set(layouts);
    const slides = (attempt.parsed.slides as Record<string, unknown>[])
      .slice(0, slideCount)
      .map((s, i) => ({
        title: String(s?.title || "").slice(0, 120),
        bullets: (Array.isArray(s?.bullets) ? s.bullets : []).map(String).slice(0, 4),
        layout: allowed.has(String(s?.layout)) ? String(s.layout) : layouts[i % layouts.length],
        imagePrompt: String(s?.imagePrompt || "").slice(0, 500),
      }));

    return json({ slides, model, usage: attempt.usage });
  } catch (e) {
    // لا استرداد هنا: قد يقع الخطأ قبل تعريف refund أصلاً (وقبل خصم الحصّة)
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
