// v2026.07.09 ════════════════════════════════════════════════════════════════
// Edge Function: generate-lesson-plan
// مساعد التحضير اليومي — يولّد خطة حصة (45 دقيقة) منظمة لدرس محدد
// بنموذج نصي اقتصادي، وتُخزَّن في lesson_preps لإعادة الاستخدام.
//
// النشر:  supabase functions deploy generate-lesson-plan
// الأسرار: OPENROUTER_API_KEY
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { takeQuota, refundQuota } from "../_shared/quota.ts";
import { orFetch, ensureVision, orErrCode } from "../_shared/ai.ts";

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
    const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
    if (!quota.ok) return json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);
    // كل مخرجٍ بخطأٍ بعد هذه النقطة يستردّ ما خُصم: المعلمة لا تُحاسَب
    // على توليدٍ لم تستلمه.
    const refund = async (body: Record<string, unknown>, status: number) => {
      await refundQuota(admin, user.id, user.email || "", "text");
      return json(body, status);
    };

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const unit = String(b.unit || "");
    const lesson = String(b.lesson || "");
    const images: string[] = Array.isArray(b.images) ? b.images.slice(0, 12) : [];
    // ملخص نصي جاهز من صفحات الكتاب (مُعَدّ مسبقاً بدالة summarize-lesson-pages) —
    // بديل أرخص عن إرفاق الصور نفسها في كل استدعاء توليد
    const bookContext = String(b.bookContext || "").slice(0, 4000);
    if (!lesson) return json({ error: "no_lesson" }, 400);

    // عند إرفاق صفحات الكتاب نحتاج نموذجاً يدعم الرؤية
    // مع صفحات الكتاب: نموذج رؤية مضمون (لا نمرّ بـ ai_model النصي)
    const model = images.length
      ? ensureVision(st.model_plan_vision || st.vision_model || "google/gemini-2.5-flash", "google/gemini-2.5-flash")
      : (st.model_plan || st.ai_model || "google/gemini-2.5-flash");

    // عمر الطلاب في عُمان: الصف الأول = ٧ سنوات (العمر = الصف + ٦)
    const gradeNum = parseInt(grade) || 0;
    const age = gradeNum ? gradeNum + 6 : 0;

    // هيكل التحضير المعتمد في منصة نور (سلطنة عُمان)
    const schema = JSON.stringify({
      outcomes: [{ level: "التذكر", text: "أنا أستطيع أن أذكر ..." }],
      strategies: ["استراتيجية تدريس مناسبة"],
      resources: ["مصدر أو وسيلة تعليمية"],
      concepts: ["مفهوم أساسي في الدرس"],
      warmup: "التهيئة والتمهيد والتعلم القبلي: نص تفصيلي — ماذا يفعل المعلم بالضبط وماذا يقول حرفياً بين قوسي اقتباس، وكيف يستدعي التعلم القبلي",
      procedures: [{ title: "الخطوة/النشاط", minutes: 10, detail: "سير مفصل: ما يفعله المعلم، ما يقوله حرفياً، ما يعمله الطلاب، وكيف ينتقل للتالي" }],
      formative: "التقويم التكويني أثناء الدرس: كيف يتحقق المعلم من الفهم لحظياً (أسئلة سريعة، ملاحظة، إشارات)",
      summative: [{ q: "سؤال ختامي يقيس مخرجاً محدداً", a: "الإجابة النموذجية", outcome: "المخرج الذي يقيسه" }],
      homework: "واجب منزلي قصير مناسب",
      tip: "نصيحة تربوية خاصة بهذا الدرس",
    });

    const system = [
      "أنت خبير مناهج وطرائق تدريس متمرس في سلطنة عُمان، تعدّ تحضيراً رسمياً بهيكل منصة نور، مبنياً على أسس تربوية بحتة.",
      "المنهج المعتمد: منهج كامبردج (Cambridge) كما يطبَّق في مدارس سلطنة عُمان — راعِ فلسفته: الفهم العميق، الاستقصاء، وربط التعلم بالحياة.",
      bookContext
        ? `ملخص فعلي لمحتوى هذا الدرس من كتاب الطالب المعتمد — استخدمه كمصدر أساسي حصري (لا من معرفة عامة):\n${bookContext}`
        : images.length
        ? "الصور المرفقة هي صفحات هذا الدرس من كتاب الطالب المعتمد. اقرأها بدقّة وابنِ التحضير من محتواها الفعلي حصراً (المفاهيم، الأمثلة، الأنشطة، الأرقام كما وردت) لا من معرفة عامة."
        : "لا صور مرفقة من الكتاب — بناءً على خبرتك بمنهج كامبردج المعتمد في سلطنة عُمان لهذا الصف والمادة، توقّع المحتوى الفعلي المرجّح لهذا الدرس تحديداً (لا محتوى عام) وابنِ التحضير عليه مباشرة بثقة.",
      age ? `أعمار الطلاب: ${age} سنوات تقريباً (الصف ${grade}) — كل الصياغات والأنشطة والأمثلة يجب أن تناسب هذا العمر النمائي بدقة.` : "",
      "المخرجات التعليمية (outcomes): 3-5 مخرجات بصيغة «أنا أستطيع أن …» موزعة على مستويات بلوم مختلفة، وحقل level يحدد المستوى (التذكر، الفهم، التطبيق، التحليل...).",
      "الاستراتيجيات (strategies): 2-3 استراتيجيات تدريس حقيقية مناسبة للدرس والعمر (التعلم التعاوني، لعب الأدوار، الاستقصاء...).",
      "المصادر (resources): مصادر ووسائل واقعية متاحة في الصف العماني.",
      "المفاهيم (concepts): المفاهيم الأساسية التي يبنى عليها الدرس.",
      "التهيئة (warmup): فقرة تفصيلية عملية — ماذا يفعل المعلم خطوة خطوة وماذا يقول حرفياً (ضع أقواله بين «») وكيف يستحضر التعلم القبلي المرتبط.",
      "الإجراءات (procedures): سير الدرس كاملاً من البداية للنهاية في 3-5 خطوات موقوتة (مجموعها ~45 دقيقة بعد التهيئة)، كل خطوة بتفصيل عملي: فعل المعلم، قوله الحرفي، عمل الطلاب.",
      "التقويم التكويني (formative): آليات تحقق لحظية أثناء الدرس.",
      "التقويم الختامي (summative): 3 أسئلة تقيس المخرجات تحديداً، كل سؤال مرتبط بمخرج (حقل outcome) مع إجابته النموذجية.",
      "صُغ بالعربية الفصحى بلغة تربوية رسمية دقيقة.",
      `أعد الناتج JSON فقط بهذا الشكل حصراً: ${schema}`,
    ].filter(Boolean).join("\n");

    const userMsg = [
      `الصف: ${grade} | المادة: ${subject}`,
      unit ? `الوحدة: ${unit}` : "",
      `الدرس: ${lesson}`,
    ].filter(Boolean).join("\n");

    // محتوى المستخدم: نص + صور صفحات الدرس إن وُجدت
    const userContent: unknown[] = [{ type: "text", text: userMsg }];
    for (const u of images) userContent.push({ type: "image_url", image_url: { url: u } });

    // الخطة هي أساس التحضير كله — لا نستسلم من أول محاولة:
    // (١) محاولة كاملة (بالصور إن وُجدت) → (٢) إعادة عند خروج غير سليم → (٣) تراجع نصي بلا صور
    const callOnce = async (withImages: boolean) => {
      const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Lesson Prep",
        },
        body: JSON.stringify({
          model: withImages ? model : (st.model_plan || st.ai_model || "google/gemini-2.5-flash"),
          messages: [
            { role: "system", content: system },
            { role: "user", content: withImages && images.length ? userContent : userMsg },
          ],
          response_format: { type: "json_object" },
          temperature: 0.4,
          max_tokens: 3200,
        }),
      }, { st, task: "plan" });
      const j = await r.json();
      // رمزُ الحالة يُمرَّر مع الفشل: بدونه يُبتلع نفادُ الرصيد داخل
      // «bad_output» فيُقرأ عطلاً في المحتوى لا في الحساب
      if (!r.ok) return { ok: false as const, detail: j, status: r.status, msg: String(j?.error?.message || j?.message || "") };
      const text = j?.choices?.[0]?.message?.content || "";
      let plan: unknown;
      try { plan = JSON.parse(text); }
      catch (_) { const m = text.match(/\{[\s\S]*\}/); try { plan = m ? JSON.parse(m[0]) : null; } catch (_2) { plan = null; } }
      const pl = plan as { procedures?: unknown[]; outcomes?: unknown[]; phases?: unknown[] } | null;
      if (!pl || !(pl.procedures || pl.phases)) return { ok: false as const, detail: text.slice(0, 300) };
      return { ok: true as const, plan, usage: j?.usage || null };
    };

    let attempt = await callOnce(images.length > 0);
    if (!attempt.ok) attempt = await callOnce(images.length > 0);          // إعادة مرة
    if (!attempt.ok && images.length) attempt = await callOnce(false);     // تراجع نصي
    if (!attempt.ok) {
      const st_ = (attempt as { status?: number }).status;
      const m_ = (attempt as { msg?: string }).msg || "";
      if (st_) {
        console.error(`openrouter ${st_} في generate-lesson-plan: ${m_}`);
        return refund({ error: orErrCode(st_, m_), detail: m_.slice(0, 200) }, 502);
      }
      return refund({ error: "bad_output", detail: attempt.detail }, 502);
    }
    return json({ plan: attempt.plan, model, usage: attempt.usage });
  } catch (e) {
    // لا استرداد هنا: قد يقع الخطأ قبل تعريف refund أصلاً (وقبل خصم الحصّة)
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
