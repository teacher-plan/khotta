// v2026.07.25 ════════════════════════════════════════════════════════════════
// Edge Function: generate-lesson-slides
// يولّد عرضاً تقديمياً تفاعلياً قصيراً (٥-١٠ شرائح) لدرس واحد — الحلقة الأولى.
// لا يُولّد أي صور: يعيد بيانات بنيوية (عناوين/نقاط/ودجات تفاعلية بأرقامها)
// تُرسم لاحقاً بالكود في الواجهة (SVG/CSS جاهزة) — صفر تكلفة رسم صور،
// واتساق بصري تام بثيم كل مادة.
//
// النشر: تلقائي عبر GitHub Actions
// الأسرار: OPENROUTER_API_KEY
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { takeQuota } from "../_shared/quota.ts";

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

    const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
    if (!quota.ok) return json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const unit = String(b.unit || "");
    const lesson = String(b.lesson || "");
    const bookContext = String(b.bookContext || "").slice(0, 4000);
    const slideCount = Math.max(5, Math.min(12, parseInt(b.slideCount) || 10));
    if (!lesson) return json({ error: "no_lesson" }, 400);

    const model = st.ai_model || "google/gemini-2.5-flash";
    const gradeNum = parseInt(grade) || 0;
    const age = gradeNum ? gradeNum + 6 : 0;

    // ═ مكتبة الودجات التفاعلية المتاحة — النموذج يختار ويملأ الأرقام فقط، والرسم كله بالكود ═
    const widgetSchema = [
      'counters: {"total":15,"remove":4} — عناصر تُعدّ ثم يُزال بعضها (طرح/تجميع/عدّ)',
      'numberline: {"from":15,"delta":4,"op":"sub"|"add"} — خط أعداد بكرة تقفز',
      'choice: {"question":"نص الموقف أو السؤال","options":["خيار أ","خيار ب"],"correctIndex":0} — بطاقتا اختيار، الخطأ يهتز والصحيح يُتوَّج',
      'scramble: {"words":["كلمة1","كلمة2","..."]} — كلمات مبعثرة تُركَّب بالترتيب الصحيح (حديث/جملة/تهجئة)',
      'flipcards: {"cards":[{"q":"سؤال قصير","a":"الإجابة"}]} — ٢-٤ بطاقات قلّابة',
      'checklist: {"items":["هدف 1","هدف 2","هدف 3"]} — أهداف تُشطب بالضغط',
      'sort: {"items":[{"text":"عبارة","correct":true}]} — ٢-٤ عبارات صواب/خطأ تُحدَّد بالضغط',
      'equation: {"left":"15","op":"−","right":"4","answer":"11"} — معادلة كبيرة بارزة',
      'none — شريحة نقاط عادية بلا ودجة (bullets فقط)',
    ].join("\n");

    const schema = JSON.stringify({
      slides: [
        {
          type: "cover|content|closing",
          tag: "وسم قصير أعلى الشريحة (مثال: درس اليوم / الفكرة الأساسية / هيا نتدرب)",
          title: "عنوان الشريحة",
          points: ["نقطة قصيرة إن لزم", "..."],
          widget: { kind: "من القائمة أعلاه أو none", params: "حسب نوع الودجة" },
          notes: "ملاحظة إلقاء قصيرة للمعلمة (١-٢ جملة): ماذا تقول أو تسأل الصف عند هذه الشريحة بالضبط",
          narration: "جملة أو جملتان قصيرتان بلسان معلم ودود تُقرآن للطلاب بصوت عالٍ تلخصان فكرة الشريحة بلغة طفل",
        },
      ],
      homework: "واجب منزلي قصير مناسب (للشريحة الأخيرة فقط)",
    });

    const system = [
      "أنت مصمم مناهج ومصمم تعليمي خبير في سلطنة عُمان، تبني عرضاً تفاعلياً قصيراً لصف من الحلقة الأولى (١-٤) بمنهج كامبردج.",
      "هذا عرض تعليمي حقيقي لا ترفيهي: كل شريحة يجب أن تخدم هدفاً تعليمياً واضحاً مرتبطاً مباشرة بالدرس، لا حشواً ولا زخرفة بلا معنى.",
      `أعمار الطلاب: ${age || "٧-١٠"} سنوات تقريباً — لغة وأمثلة وطول جمل تناسب هذا العمر النمائي بدقة، جمل قصيرة مباشرة.`,
      bookContext
        ? `ملخص فعلي لمحتوى هذا الدرس من كتاب الطالب المعتمد — ابنِ كل شريحة من محتواه حصراً (المفاهيم، الأمثلة، الأرقام، الأنشطة كما وردت):\n${bookContext}`
        : "لا صفحات كتاب مرفقة — بناءً على خبرتك بمنهج كامبردج المعتمد في سلطنة عُمان لهذا الصف والمادة، توقّع المحتوى الفعلي المرجّح لهذا الدرس تحديداً (لا محتوى عام) وابنِ العرض عليه مباشرة بثقة.",
      `ابنِ بالضبط ${slideCount} شرائح بهذا الترتيب التربوي:`,
      "١) شريحة غلاف (type=cover): عنوان الدرس فقط، بلا ودجة أو widget=none.",
      "٢) شريحة أهداف (widget=checklist): ٣ مخرجات تعليمية بصيغة «أنا أستطيع أن...» تعكس مستويات بلوم (تذكر/فهم/تطبيق).",
      "٣) شريحة أو شريحتان للفكرة الأساسية: اشرح المفهوم المحوري للدرس عملياً، واختر الودجة الأنسب تماماً لطبيعته الرياضية/اللغوية/العلمية/القيمية من القائمة (لا تفرض عدّادات على درس لا يحتاجها، ولا اختياراً على درس عددي).",
      "بقية الشرائح الوسطى: تدرّج منطقي في عمق الفهم (تطبيق ثم تدريب)، كل شريحة بودجة مختلفة قدر الإمكان لتنويع النشاط.",
      "الشريحة قبل الأخيرة: تدريب ختامي تفاعلي (widget=flipcards أو sort أو choice) يقيس تحقق المخرجات.",
      "الشريحة الأخيرة (type=closing): خلاصة الدرس نقاطاً + واجب منزلي قصير في حقل homework العلوي (خارج الشرائح).",
      "قائمة الودجات المتاحة وشكل كل منها بالضبط:",
      widgetSchema,
      "الأرقام في الودجات يجب أن تكون منطقية ومتناسقة (مثلاً numberline.delta لا يتجاوز 9، counters.total بين 5-20).",
      "حقل notes: ملاحظة إلقاء عملية للمعلمة لكل شريحة (ماذا تقول/تسأل بالضبط) — لا تظهر للطلاب.",
      "حقل narration: تعليق صوتي قصير بلسان معلم ودود يُقرأ للطلاب آلياً — جمل بسيطة مشكولة جزئياً حيث يلزم، بلا أرقام لاتينية.",
      "صُغ كل نص بالعربية الفصحى السليمة، بلا أي رموز تعبيرية (إيموجي).",
      `أعد الناتج JSON فقط بهذا الشكل حصراً: ${schema}`,
    ].filter(Boolean).join("\n");

    const userMsg = [
      `الصف: ${grade} | المادة: ${subject}`,
      unit ? `الوحدة: ${unit}` : "",
      `الدرس: ${lesson}`,
    ].filter(Boolean).join("\n");

    const callOnce = async () => {
      const r = await fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Lesson Slides Generator",
        },
        body: JSON.stringify({
          model,
          messages: [
            { role: "system", content: system },
            { role: "user", content: userMsg },
          ],
          response_format: { type: "json_object" },
          temperature: 0.5,
          max_tokens: 3000,
        }),
      });
      const j = await r.json();
      if (!r.ok) return { ok: false as const, detail: j };
      const text = j?.choices?.[0]?.message?.content || "";
      let parsed: { slides?: unknown[]; homework?: string } | null = null;
      try { parsed = JSON.parse(text); }
      catch (_) { const m = text.match(/\{[\s\S]*\}/); try { parsed = m ? JSON.parse(m[0]) : null; } catch (_2) { parsed = null; } }
      if (!parsed || !Array.isArray(parsed.slides) || parsed.slides.length < 3) return { ok: false as const, detail: text.slice(0, 300) };
      return { ok: true as const, parsed, usage: j?.usage || null };
    };

    let attempt = await callOnce();
    if (!attempt.ok) attempt = await callOnce();
    if (!attempt.ok) return json({ error: "bad_output", detail: attempt.detail }, 502);
    return json({ slides: attempt.parsed.slides, homework: attempt.parsed.homework || "", model, usage: attempt.usage });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
