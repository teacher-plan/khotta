// v2026.07.09 ════════════════════════════════════════════════════════════════
// Edge Function: segment-book
// التقطيع الذكي للكتاب: يقرأ دفعة من صور صفحات الكتاب بعين نموذج قوي
// ويحدد الدروس التي تبدأ فيها (الوحدة، اسم الدرس، رقم الصفحة المطبوع).
// تُستدعى على دفعات متتالية من الواجهة حتى تغطية الكتاب كاملاً.
//
// النشر:  supabase functions deploy segment-book
// الأسرار: OPENROUTER_API_KEY
// النموذج: ai_settings.seg_model ثم vision_model ثم gemini-2.5-flash
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

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

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const basePath = String(b.basePath || "");
    const sheetStart = Math.max(1, parseInt(b.sheetStart) || 1);
    const sheetEnd = Math.max(sheetStart, parseInt(b.sheetEnd) || sheetStart);
    const prevContext = String(b.prevContext || "").slice(0, 800);
    const mode = b.mode === "index" ? "index" : "scan";
    if (!basePath) return json({ error: "no_book" }, 400);
    if (sheetEnd - sheetStart > 39) return json({ error: "batch_too_large" }, 400);

    const model = st.seg_model || st.vision_model || "google/gemini-2.5-flash";

    // روابط صور الأوراق العامة من التخزين
    const supaUrl = Deno.env.get("SUPABASE_URL")!;
    const imgUrl = (sheet: number) =>
      `${supaUrl}/storage/v1/object/public/library-files/${basePath}/p${sheet}.jpg`;

    // نص التعليمات حسب الوضع: قراءة الفهرس (بنية رسمية) أو مسح الصفحات (احتياط)
    const promptText = mode === "index"
      ? [
        `هذه صور الأوراق الأولى من كتاب ${subject} للصف ${grade} (منهج كامبردج — سلطنة عُمان).`,
        "مهمتك: ابحث عن صفحة/صفحات الفهرس (جدول المحتويات) واستخرج منها البنية الرسمية الكاملة للكتاب.",
        "أعد الوحدات بالترتيب، وتحت كل وحدة دروسها الفعلية بالترتيب كما وردت في الفهرس حرفياً، مع رقم الصفحة المطبوع لكل درس كما هو مذكور أمامه في الفهرس.",
        "تنبيه بالغ الأهمية عن حدود الوحدات: أغلب الكتب تُرقّم الدروس بصيغة «رقم الوحدة-رقم الدرس» (مثل ١-٧، ١-٨، ١-٩ ثم ٣-١، ٣-٢...). هذا الترقيم هو الدليل الحاسم والموثوق على حدود الوحدة الحقيقية — استخرجه من بداية كل عنوان درس في الفهرس.",
        "كل مرة يتغيّر فيها الرقم الأول (رقم الوحدة) في ترقيم الدروس، فهذه وحدة جديدة منفصلة تماماً — حتى لو كان اسم الوحدة النصي متطابقاً حرفياً مع وحدة سابقة، وحتى لو لم يظهر أي ترقيم صريح للوحدة نفسها (وحدة ١، وحدة ٢) في الفهرس. لا تدمج أبداً دروساً بأرقام وحدة مختلفة (كـ١-٩ و٣-١) تحت وحدة واحدة بسبب تشابه الاسم النصي فقط.",
        "اجعل حقل unit لكل مجموعة يتضمن رقم الوحدة المستخرج من ترقيم دروسها بوضوح (مثال: «القياس ١» للدروس ١-س، و«القياس ٢» للدروس ٢-س، حتى إن كان اسم الفصل الظاهر في الفهرس نفس الكلمة).",
        "إن لم يوجد ترقيم درس على الإطلاق، استخدم موضع/تسلسل الدروس في الفهرس وأي فواصل بصرية (عناوين فصول متتالية) لتمييز الوحدات المستقلة، ولا تجمع تحت اسم وحدة واحد إلا الدروس المتصلة فعلاً في نفس التسلسل.",
        "مهم جداً: اعتمد على الفهرس الرسمي فقط. لا تعتبر العناوين الفرعية أو الأنشطة أو المصطلحات دروساً — الدروس هي فقط ما يذكره الفهرس كدروس. لا تخترع دروساً ولا تكرر.",
        "تجاهل: المقدمة، التمهيد، صفحات المراجعة العامة، الملاحق.",
        'أعد JSON فقط بهذا الشكل: {"units":[{"unit":"اسم الوحدة","lessons":[{"lesson":"اسم الدرس","printedPage":12}]}]}',
        "إن لم تجد فهرساً واضحاً في هذه الأوراق، أعد: {\"units\":[]}",
      ].join("\n")
      : [
        `هذه صور أوراق متتالية من كتاب ${subject} للصف ${grade} (منهج كامبردج — سلطنة عُمان).`,
        `الورقة الأولى المعروضة هي الورقة رقم ${sheetStart} في الملف، والأخيرة رقم ${sheetEnd} (بترتيب العرض).`,
        prevContext ? `سياق سابق من الأوراق التي قبلها: ${prevContext}` : "",
        "مهمتك: حدد كل درس جديد يبدأ داخل هذه الأوراق.",
        "علامات بداية الدرس: صفحة عنوان مميزة باسم الدرس، ترقيم دروس (درس ١-٢ مثلاً)، تغيير تصميم واضح، أهداف تعلم جديدة.",
        "مهم: لا تعتبر العناوين الفرعية داخل الدرس أو أسماء الأنشطة دروساً مستقلة — الدرس الحقيقي فقط.",
        "تنبيه بالغ الأهمية: إن كانت الدروس مرقّمة بصيغة «رقم الوحدة-رقم الدرس» (مثل ١-٧ ثم ٣-١)، فتغيّر الرقم الأول يعني وحدة جديدة منفصلة تماماً حتى لو تطابق اسم الوحدة النصي — لا تدمج أبداً دروساً بأرقام وحدة مختلفة تحت وحدة واحدة، واجعل حقل unit يتضمن رقم الوحدة المستخرج من الترقيم.",
        "لكل درس أعد: unit (اسم الوحدة كما في الكتاب — وإن لم تظهر فاستنتجها من السياق السابق)، lesson (اسم الدرس حرفياً)، printedPage (رقم الصفحة المطبوع)، sheet (رقم الورقة في العرض الحالي).",
        "تجاهل: المقدمة، الفهرس، صفحات الأنشطة العامة، المراجعات، الملاحق.",
        'أعد JSON فقط: {"lessons":[{"unit":"...","lesson":"...","printedPage":12,"sheet":14}],"lastUnit":"آخر وحدة ظاهرة"}',
      ].filter(Boolean).join("\n");

    const content: unknown[] = [{ type: "text", text: promptText }];
    for (let s = sheetStart; s <= sheetEnd; s++) {
      content.push({ type: "image_url", image_url: { url: imgUrl(s) } });
    }

    const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Smart Book Segmentation",
      },
      body: JSON.stringify({
        model,
        messages: [{ role: "user", content }],
        response_format: { type: "json_object" },
        temperature: 0.1,
        max_tokens: 3000,
      }),
    });
    const or = await orResp.json();
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);

    const text = or?.choices?.[0]?.message?.content || "";
    let parsed: { lessons?: unknown[]; units?: unknown[]; lastUnit?: string } | null = null;
    try { parsed = JSON.parse(text); }
    catch (_) { const m = text.match(/\{[\s\S]*\}/); parsed = m ? JSON.parse(m[0]) : null; }
    if (!parsed) return json({ error: "bad_output", detail: text.slice(0, 300) }, 502);

    if (mode === "index") {
      // تسطيح بنية الوحدات إلى قائمة دروس مرتبة
      const units = Array.isArray(parsed.units) ? parsed.units : [];
      const lessons: unknown[] = [];
      for (const u of units as Array<{ unit?: string; lessons?: Array<{ lesson?: string; printedPage?: number }> }>) {
        const uname = String(u?.unit || "").trim();
        for (const l of (Array.isArray(u?.lessons) ? u.lessons : [])) {
          if (l && l.lesson) lessons.push({ unit: uname, lesson: String(l.lesson).trim(), printedPage: parseInt(String(l.printedPage)) || null });
        }
      }
      return json({ lessons, units, mode, model, usage: or?.usage || null });
    }
    if (!Array.isArray(parsed.lessons)) return json({ error: "bad_output", detail: text.slice(0, 300) }, 502);
    return json({ lessons: parsed.lessons, lastUnit: parsed.lastUnit || "", mode, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
