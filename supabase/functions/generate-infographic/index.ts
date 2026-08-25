// v2026.07.09 ════════════════════════════════════════════════════════════════
// Edge Function: generate-infographic
// يولّد إنفوجرافيك تعليمي مرسوم (بأسلوب NotebookLM) لدرس محدد
// عبر نموذج توليد الصور Gemini 3 Pro Image (Nano Banana Pro) من OpenRouter.
// المفتاح يبقى سرياً على الخادم — نفس مفتاح generate-exam.
//
// النشر:  supabase functions deploy generate-infographic
// الأسرار: OPENROUTER_API_KEY
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { takeQuota, refundQuota, logAiCost } from "../_shared/quota.ts";
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
    // تمييزٌ لازم: fail-closed يعني أنّ عطلاً في القاعدة يمنع التوليد أيضاً —
    // فلو قلنا «نفد رصيدك» لكذبنا على المعلّمة وأرسلناها تشكو رصيداً سليماً.
    if (!quota.ok) return quota.error === "quota_unavailable"
      ? json({ error: "quota_unavailable" }, 503)
      : json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);
    // كل مخرجٍ بخطأٍ بعد هذه النقطة يستردّ ما خُصم: المعلمة لا تُحاسَب
    // على توليدٍ لم تستلمه.
    const refund = async (body: Record<string, unknown>, status: number) => {
      await refundQuota(admin, user.id, user.email || "", "img");
      return json(body, status);
    };

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const lessonNames: string[] = Array.isArray(b.lessonNames) ? b.lessonNames.map(String) : [];
    const teacherPrompt = String(b.teacherPrompt || "").slice(0, 1500);
    // صفحات الدرس من الكتاب المقطّع (مرجع محتوى)
    const bookImages: string[] = Array.isArray(b.images) ? b.images.slice(0, 10) : [];
    const bookContext = String(b.bookContext || "").slice(0, 4000);
    // الدقة ثابتةٌ من الخادم لا من العميل: لا موضعٌ في الواجهة يرسل size
    // إطلاقاً (تحقّقٌ بمسح شامل لكل نداءات هذه الدالة)، فقبولها من العميل
    // كان يسمح لمن يستدعي الدالة مباشرةً (بلا واجهة) بطلب 4K — الأغلى —
    // بنفس نقطة الرصيد الواحدة التي تُخصم قبل قراءة هذا السطر.
    const size = "2K";
    const aspect = ["9:16", "3:4", "1:1", "16:9", "21:9", "2:3", "4:3"].includes(b.aspect) ? b.aspect : "9:16";
    // وضع التعديل: صورة موجودة + تعليمات تغيير موضعي
    const editPrompt = String(b.editPrompt || "").slice(0, 1000);
    const editImage = (typeof b.editImage === "string" && b.editImage.startsWith("data:image/")) ? b.editImage : "";
    const isEdit = !!(editImage && editPrompt);
    if (!isEdit && !lessonNames.length) return json({ error: "no_lessons" }, 400);

    // نموذج الصور — موحّد مع مولّد الشرائح (مفتاح slide_model في ai_settings)
    let model = st.model_infographic || st.slide_model || st.info_model || "google/gemini-2.5-flash-image";
    // التعديل بالوصف يتطلب نموذج جوجل (يستقبل صورة ويعيد صورة معدّلة)
    if (isEdit && !model.startsWith("google/")) model = "google/gemini-3.1-flash-image-preview";

    // نمط بصري ثابت مستوحى من إنفوجرافيك NotebookLM (باستيل + رسوم كرتونية تعليمية)
    const stylePrompt = st.info_style_prompt || [
      "أسلوب بصري: إنفوجرافيك تعليمي عمودي (portrait poster) بأسلوب مرح واحترافي في آن واحد.",
      "خلفية مقسمة لمناطق بألوان باستيل ناعمة متمايزة (أزرق فاتح، أصفر كريمي، وردي فاتح، أخضر نعناعي) بحدود منحنية انسيابية.",
      "رسوم كرتونية مسطحة لطيفة توضح كل مفهوم (أشكال هندسية مقسمة للكسور، نرد، مسطرة، شخصيات مبتسمة، أيقونات ملونة).",
      "عنوان رئيسي ضخم أعلى الملصق بالعربية بخط عريض واضح.",
      "كل قسم له عنوان فرعي داخل شارة (badge) ملونة، ومحتوى مختصر بنقاط قصيرة.",
      "أرقام وأمثلة رياضية مكتوبة بوضوح تام وخط كبير، بالترقيم العربي-الهندي (٠١٢٣٤٥٦٧٨٩) لا اللاتيني، وأي معادلة أو عملية حسابية مكتوبة من اليمين إلى اليسار متوافقة مع اتجاه النص العربي.",
      "النص العربي يجب أن يكون دقيقاً إملائياً ومقروءاً بوضوح — هذا أهم شرط.",
      "لا صور فوتوغرافية، لا نص إنجليزي إلا للمصطلحات بين قوسين.",
    ].join(" ");

    const gradeNum = parseInt(grade) || 0;
    // جدول أعمارٍ صريح بدل حساب ضمني — الصفوف الأربعة الوحيدة المدعومة اليوم
    // (الحلقة الأولى) بالضبط: الأول=٧، الثاني=٨، الثالث=٩، الرابع=١٠.
    const AGE_BY_GRADE: Record<number, number> = { 1: 7, 2: 8, 3: 9, 4: 10 };
    const age = AGE_BY_GRADE[gradeNum] ?? (gradeNum ? gradeNum + 6 : 0);
    const userPrompt = [
      `أنشئ إنفوجرافيك تعليمياً واحداً متكاملاً بالعربية الفصحى لطلاب ${grade ? "الصف " + grade : "المدرسة"} في مادة ${subject}.`,
      `عنوان الدرس/الدروس: ${lessonNames.join("، ")} — استخدم هذا العنوان أولاً لتكوين فكرةٍ عامة عن موضوع الدرس واتجاهه قبل قراءة أي نصٍّ إضافي.`,
      "(معلومة خلفية للتوليد فقط — ممنوع كتابة أي جزءٍ منها كعنوانٍ أو نصٍّ داخل الإنفوجرافيك نفسه): المرجع المنهجي هو كامبردج (Cambridge) المعتمد في مدارس سلطنة عُمان تحديداً لا أي دولة أخرى. عنوان الإنفوجرافيك الظاهر يجب أن يكون اسم الدرس/الموضوع نفسه فقط، لا اسم المنهج أو الدولة.",
      age ? `أعمار الطلاب حسب الصف (جدولٌ ثابت): الصف الأول=٧ سنوات، الثاني=٨، الثالث=٩، الرابع=١٠. عمر طلاب هذا الدرس تحديداً: ${age} سنوات (الصف ${grade}) — المحتوى واللغة والرسومات يجب أن تناسب هذا العمر بدقةٍ تامة، لا عمراً أكبر ولا أصغر.` : "",
      "الهوية البصرية: إن رسمت أي شخصيات أو أزياء أو مبانٍ أو بيئة، فيجب أن تعكس الهوية العُمانية حصراً (الزي المدرسي العُماني، الكمة والدشداشة العُمانية للذكور، العمارة العُمانية) — إياك ومظاهر أي دولة خليجية أخرى (لا غترة وعقال، لا هوية سعودية أو إماراتية).",
      "إن رسمت شخصية «المعلّم/المعلّمة» في أي مشهد، فيجب أن تكون امرأةً (معلّمة) حصراً — بزيٍّ عُمانيٍّ محتشم مناسب (عباءة وحجاب)، لا رجلاً إطلاقاً بأي حال. هذه المنصّة لمعلّماتٍ إناث فقط، فلا يظهر معلّمٌ ذكر في أي رسم.",
      // أولوية الفحص البصري المباشر لصفحات الكتاب فوق أي ملخصٍ نصيٍّ وسيط —
      // ملخصٌ سابقٌ (bookContext) قد يُفقِد تفاصيل حقيقية موجودة في الصفحة
      // نفسها، فحين تتوفّر الصور الخام يُطلَب من النموذج قراءتها هو مباشرةً
      // بدل الاعتماد على تلخيصٍ جاهز.
      bookImages.length
        ? "الصور المرفقة هي صفحات هذا الدرس الفعلية من كتاب الطالب المعتمد — افحصها بصرياً بدقّة، اقرأ كل نصٍّ ورقمٍ ورسمٍ فيها فعلياً، والتزم بمحتواها الفعلي الحرفي (لا تُلخّص الفكرة العامة وتبني محتوى جديداً من عندك، ولا تعتمد على أي ملخصٍ سابق أو تخمينٍ من عنوان الدرس فقط)."
        : bookContext
        ? `لا صفحات كتابٍ خام مرفقة — إليك ملخصٌ نصي سابق لمحتوى الدرس فقط كبديلٍ مؤقت، التزم بمحتواه الفعلي حرفياً (لا تُلخّص الفكرة العامة وتبني محتوى جديداً من عندك، ولا تُعمِّم أو تفترض محتوى غير موجود فيه):\n${bookContext}`
        : "لا صفحات كتاب مرفقة — بناءً على خبرتك بمنهج كامبردج المعتمد في سلطنة عُمان لهذا الصف والمادة، توقّع المحتوى الفعلي المرجّح لهذا الدرس تحديداً (لا محتوى عام) والتزم به.",
      "رتّب المفاهيم والقواعد والحقائق الفعلية من الدرس في أقسامٍ واضحة مرقّمة بنفس تسلسل الكتاب (أولاً، ثانياً، ثالثاً...) مع تمثيل بصري مرسوم لكل مفهوم.",
      "ممنوعٌ كتابة أي سؤال تمرين أو تقويم، وممنوعٌ كتابة أي مثالٍ (سواء منقولاً من الكتاب أو مُبتكَراً من عندك) داخل الإنفوجرافيك — اكتفِ بعرض المفاهيم والحقائق والقواعد نفسها فقط، بلا أسئلة وبلا أمثلة إطلاقاً.",
      "قيودٌ صارمة على الرسوم — ممنوعةٌ منعاً باتاً مهما كان موضوع الدرس: أي مشهدٍ يصوّر طفلاً (ولداً أو بنتاً) يلمس أو يُلامَس أو يُعانَق أو يُحتَضَن من طفلٍ آخر أو من شخصٍ بالغ، وأي مشهدٍ يصوّر ولداً وبنتاً يلعبان معاً أو يتفاعلان بقربٍ جسدي. كل الشخصيات في الرسم يجب أن تكون منفصلة تماماً عن بعضها بلا أي تلامسٍ جسدي أو قربٍ حميمي، حتى لو كان موضوع الدرس نفسه عن الأمان الجسدي أو الخصوصية أو حدود اللمس — في هذه الحالة اشرح المفهوم بالنص والأيقونات الرمزية (علامات ✅/❌، دوائر، مسافات) لا برسم أجسادٍ متلامسة إطلاقاً. لا محتوى غير لائق بالأطفال بأي شكل.",
      "قبل رسم النص النهائي: راجع كل كلمةٍ عربية ستكتبها إملائياً ونحوياً وتأكّد من صحتها الكاملة (لا أخطاء إملائية ولا تشكيل خاطئ). راجع أيضاً أن كل كلمةٍ أو تسمية مرتبطة بصورتها الصحيحة فقط، ولا تُكرِّر نفس الكلمة أو الجملة تحت أكثر من صورةٍ أو في أكثر من موضعٍ في التصميم إلا إذا كانت هي فعلاً نفس الكلمة الصحيحة المقصودة لكل موضع — كل عنصرٍ بصري يجب أن يقترن بنصّه الصحيح والمختلف عن غيره، لا نصّاً منسوخاً من عنصرٍ آخر بالخطأ. لا تُظهر النتيجة النهائية إلا بعد التأكد التام من سلامة كل هذا.",
      teacherPrompt ? `توجيهات المعلم: ${teacherPrompt}` : "",
      stylePrompt,
      `توجه التصميم: ${["16:9", "21:9"].includes(aspect) ? "أفقي عريض — وزّع الأقسام جنباً إلى جنب" : aspect === "1:1" ? "مربع متوازن" : "عمودي طولي — الأقسام فوق بعضها"}.`,
    ].filter(Boolean).join("\n");

    // محتوى الطلب: النص + صفحات الدرس المرجعية (إن وُجدت)
    const genContent: unknown[] = [{ type: "text", text: userPrompt }];
    for (const u of bookImages) genContent.push({ type: "image_url", image_url: { url: u } });

    // بعض النماذج لا تقبل كل إعدادات المقاس/الجودة — نحاول كاملة ثم نتدرّج تلقائياً
    const call = (cfg: Record<string, unknown> | null) =>
      orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Infographic Generator",
        },
        body: JSON.stringify({
          model,
          messages: [{ role: "user", content: bookImages.length ? genContent : userPrompt }],
          modalities: ["image", "text"],
          ...(cfg ? { image_config: cfg } : {}),
        }),
      }, { st, task: "infographic" });
    // النماذج غير جوجل (مثل Seedream) تعمل عبر واجهة الصور الموحدة /v1/images فقط
    const callImagesApi = async () => {
      const r = await orFetch("https://openrouter.ai/api/v1/images", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Infographic Generator",
        },
        // Seedream يشترط حداً أدنى كبيراً للبكسلات وسعره ثابت — نرسل دائماً 4K
        body: JSON.stringify({ model, prompt: userPrompt, resolution: "4K", aspect_ratio: aspect }),
      }, { st, task: "infographic" });
      const j = await r.json();
      if (!r.ok) return { ok: false, detail: j, img: "" };
      const d = j?.data?.[0] || {};
      const img = d.b64_json ? "data:image/png;base64," + d.b64_json : (d.url || "");
      return { ok: !!img, detail: j, img };
    };

    // ═ وضع التعديل بالوصف: نرسل الصورة الحالية + التعليمات ونستلم نسخة معدّلة ═
    if (isEdit) {
      const editInstr = [
        "هذه صورة إنفوجرافيك تعليمي بالعربية.",
        `أعد رسم نفس الصورة بالضبط مع تطبيق هذا التعديل فقط: «${editPrompt}».`,
        "حافظ حرفياً على كل شيء آخر دون أي تغيير: التخطيط، الألوان، الرسومات، وجميع النصوص الأخرى وأماكنها.",
        "أخرج الصورة بنفس أبعاد الصورة الأصلية ونفس أسلوبها تماماً.",
      ].join("\n");
      const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Infographic Editor",
        },
        body: JSON.stringify({
          model,
          messages: [{ role: "user", content: [
            { type: "text", text: editInstr },
            { type: "image_url", image_url: { url: editImage } },
          ] }],
          modalities: ["image", "text"],
        }),
      }, { st, task: "infographic" });
      const or = await r.json();
      if (!r.ok) {
        const _m = String(or?.error?.message || or?.message || "");
        console.error(`openrouter ${r.status} في generate-infographic: ${_m}`);
        return refund({ error: orErrCode(r.status, _m), detail: _m.slice(0, 200) }, 502);
      }
      const msg = or?.choices?.[0]?.message;
      const outImg = msg?.images?.[0]?.image_url?.url || "";
      if (!outImg) return refund({ error: "no_image", detail: msg?.content || null }, 502);
      await logAiCost(admin, user.id, "generate-infographic", "img", model, or?.usage);
      return json({ image: outImg, model, usage: or?.usage || null, edited: true });
    }

    let img = "";
    let usage: unknown = null;
    if (model.startsWith("google/")) {
      // ثلاث محاولات بإعداداتٍ متدرّجة (مقاسٌ كامل ← نسبة فقط ← بلا إعداد).
      // كانت هذه السلسلة تُجرَّب فقط عند فشل HTTP الصريح؛ لكن العطل الأشيع
      // فعلياً هو عطلٌ صامت: النموذج يردّ 200 لكن بلا صورة (يرفض المقاس/النسبة
      // المطلوبة بصمتٍ ويعيد نصّاً بدلها) — وكانت هذه الحالة تُخفق فوراً بلا
      // تجربة الإعداد الأخفّ التالي، فتضطرّ المعلّمة لإعادة الضغط يدوياً حتى
      // يوافق الحظّ إعداداً يقبله النموذج. الآن الحالتان تُعاملان معاملةً واحدة.
      const configs: (Record<string, unknown> | null)[] = [{ aspect_ratio: aspect, image_size: size }, { aspect_ratio: aspect }, null];
      let orResp: Response, or: any, message: any;
      for (const cfg of configs) {
        orResp = await call(cfg);
        or = await orResp.json();
        message = or?.choices?.[0]?.message;
        img = message?.images?.[0]?.image_url?.url || "";
        if (orResp.ok && img) break; // نجاحٌ فعلي بصورةٍ حقيقية — لا داعٍ لتجربة إعداداتٍ أخرى
      }
      if (!orResp!.ok) {
        const _m = String(or?.error?.message || or?.message || "");
        console.error(`openrouter ${orResp!.status} في generate-infographic: ${_m}`);
        return refund({ error: orErrCode(orResp!.status, _m), detail: _m.slice(0, 200) }, 502);
      }
      usage = or?.usage || null;
      if (!img) {
        console.error(`generate-infographic: النموذج ${model} ردّ 200 بلا صورةٍ عبر كل الإعدادات الثلاثة — content: ${String(message?.content || "").slice(0, 200)}`);
        return refund({ error: "no_image", detail: message?.content || null }, 502);
      }
    } else {
      const r = await callImagesApi();
      if (!r.ok) {
        const _d = r.detail as { error?: { message?: string }; message?: string } | undefined;
        const _m = String(_d?.error?.message || _d?.message || "");
        console.error(`openrouter images في generate-infographic: ${_m}`);
        return refund({ error: orErrCode(402, _m) === "no_credit" ? "no_credit" : "provider_error", detail: _m.slice(0, 200) }, 502);
      }
      img = r.img;
    }

    await logAiCost(admin, user.id, "generate-infographic", "img", model, usage);
    return json({ image: img, model, usage });
  } catch (e) {
    // لا استرداد هنا: قد يقع الخطأ قبل تعريف refund أصلاً (وقبل خصم الحصّة)
    console.error("server_error:", String(e));
    return json({ error: "server_error" }, 500);
  }
});
