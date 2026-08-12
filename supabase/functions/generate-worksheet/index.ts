// v2026.08.12 ════════════════════════════════════════════════════════════════
// Edge Function: generate-worksheet
// يولّد ورقة عمل A4 جاهزة للطباعة (أبيض وأسود) لدرس محدد — HTML/SVG خالص.
// «ورقة العمل» في مدارس سلطنة عُمان: صفحة A4 مقسَّمة بتقسيمٍ ثابت، تُطبع
// بالأبيض والأسود، فالرسم فيها خطوطٌ لا ألوان. لذلك نولّدها بنموذجٍ نصّي
// رخيص يرسم بـ SVG، لا بنموذج صور: الفرق في الكلفة نحو مئة ضعف، والمخرَج
// هنا أدقّ — نصٌّ عربي حادّ عند الطباعة بدل نصٍّ مرسومٍ داخل صورة.
//
// النشر: تلقائي عبر GitHub Actions
// الأسرار: OPENROUTER_API_KEY
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { takeQuota, refundQuota } from "../_shared/quota.ts";
import { orFetch, orErrCode, pickModel } from "../_shared/ai.ts";

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

// النموذج يردّ أحياناً بشرحٍ قبل الكود أو يغلّفه بسياج ماركداون. نأخذ الكود
// وحده: أيّ حرفٍ خارجه يظهر نصّاً سائباً أعلى الورقة المطبوعة.
function extractHtml(raw: string): string {
  const fenced = raw.match(/```(?:html)?\s*([\s\S]*?)```/i);
  let out = (fenced ? fenced[1] : raw).trim();
  // لو بقي كلامٌ تمهيدي قبل أول وسم، نقصّه من أول عنصرٍ فعلي.
  const start = out.search(/<(?:!doctype|html|style|div|section|body)\b/i);
  if (start > 0) out = out.slice(start);
  return out.trim();
}

// حارس الاكتمال: ورقةٌ مبتورة (انقطع التوليد عند سقف الرموز) تُطبع ناقصة
// بلا أن يظهر خطأ — والمعلّمة تكتشفها بعد الطباعة. نردّها خطأً بدل ذلك.
function looksTruncated(html: string): boolean {
  if (html.length < 400) return true;
  const open = (html.match(/<(div|section|table|svg)\b/gi) || []).length;
  const close = (html.match(/<\/(div|section|table|svg)>/gi) || []).length;
  return open - close > 2;
}

const SHEET_RULES = [
  "القواعد الإلزامية لورقة العمل:",
  "• صفحة A4 واحدة: العنصر الجذر <div class=\"a4\"> بعرض 210mm وارتفاع أدنى 297mm وحشوة داخلية 14mm.",
  "• أبيض وأسود فقط — لا أي لون (الطباعة المدرسية بالأبيض والأسود). الخلفية #fff والحبر #111 والحدود صلبة سوداء.",
  "• dir=\"rtl\" على الجذر وخطٌّ عربي: font-family:'Segoe UI',Tahoma,sans-serif.",
  "• ترويسة: عنوان الورقة، والصف والمادة، وسطران للاسم والتاريخ بخطوط نقطٍ للتعبئة.",
  "• أقسام مرقّمة بالأرقام العربية الهندية (١، ٢، ٣) كلٌّ بتعليمة واضحة بصيغة المؤنث الموجَّهة للطالب.",
  "• الرسم بـ SVG مضمّن فقط: دوائر ومثلثات ومربّعات ونجوم وخطوط — أشكالٌ مفرّغة بحدٍّ أسود (fill:none;stroke:#111) لا مملوءة، ليلوّنها الطالب.",
  "• مساحات إجابةٍ حقيقية: مربّعات فارغة وسطور كتابةٍ مسطّرة — لا تترك سؤالاً بلا موضع إجابة.",
  "• @media print: إخفاء الظلال، و@page{size:A4;margin:0}.",
  "• أعِد كود HTML وحده — بلا شرحٍ قبله أو بعده، وبلا سياج ماركداون. ابدأ بـ <style> وأنهِ بإغلاق آخر وسم.",
  "• أغلق كل وسمٍ فتحته. الورقة تُطبع كما هي، فأي وسمٍ ناقص يفسد التخطيط.",
].join("\n");

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

    const b = await req.json().catch(() => ({}));
    const edit = b.edit === true;
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const lessonNames: string[] = Array.isArray(b.lessonNames) ? b.lessonNames.map(String) : [];
    const bookContext = String(b.bookContext || "").slice(0, 4000);
    const instructions = String(b.instructions || "").slice(0, 600);
    const currentHtml = String(b.currentHtml || "");
    const editRequest = String(b.editRequest || "").slice(0, 600);

    if (edit) {
      if (!currentHtml || !editRequest) return json({ error: "no_edit_input" }, 400);
    } else if (!lessonNames.length) {
      return json({ error: "no_lessons" }, 400);
    }

    // ⛔ حصة الاستخدام الشهرية — تُفرض على الخادم.
    // التعديل يُحاسَب كالتوليد: كلاهما نداءٌ كامل للنموذج بالورقة كلها.
    const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
    if (!quota.ok) return json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);
    const refund = async (body: Record<string, unknown>, status: number) => {
      await refundQuota(admin, user.id, user.email || "", "text");
      return json(body, status);
    };

    const model = pickModel(st, "worksheet", "google/gemini-2.5-flash");
    const gradeNum = parseInt(grade) || 0;
    const age = gradeNum ? gradeNum + 6 : 0;

    let system: string;
    let userMsg: string;

    if (edit) {
      system = [
        "أنت مصمّم أوراق عملٍ مدرسية في سلطنة عُمان. لديك ورقة عمل HTML جاهزة، والمعلّمة تطلب تعديلاً عليها.",
        "طبّق التعديل المطلوب وحده، وأبقِ كل ما عداه كما هو حرفياً — التخطيط والأقسام غير المذكورة لا تُمَسّ.",
        "أعِد الورقة كاملةً بعد التعديل (لا الجزء المعدَّل وحده).",
        SHEET_RULES,
      ].join("\n\n");
      // الورقة كاملةً لا مقتطعة: التعديل على نصفٍ منها يُعيد نصفاً.
      userMsg = `ورقة العمل الحالية:\n${currentHtml}\n\nالتعديل المطلوب:\n${editRequest}`;
    } else {
      system = [
        "أنت معلم خبير في سلطنة عُمان (منهج كامبردج) تصمّم أوراق عملٍ مطبوعة للحلقة الأولى.",
        age ? `أعمار الطالبات: ${age} سنوات تقريباً (الصف ${grade}) — التعليمات بجملٍ قصيرة جداً ومفرداتٍ يعرفنها، والأشكال كبيرة واضحة.` : "",
        bookContext
          ? `ملخص فعلي لمحتوى هذا الدرس من كتاب الطالب المعتمد — ابنِ الأسئلة منه حصراً (لا من معرفة عامة):\n${bookContext}`
          : "لا ملخص متاح من الكتاب — بناءً على خبرتك بمنهج كامبردج المعتمد في سلطنة عُمان لهذا الصف والمادة، توقّع المحتوى الفعلي المرجّح لهذا الدرس تحديداً (لا محتوى عام) وابنِ عليه.",
        "صمّم ٤ إلى ٦ أنشطةٍ متنوّعة الأسلوب (عدّ، مطابقة بخطوط، تظليل، تتبّع، دائرة حول الإجابة، إكمال فراغ) متدرّجة من الأسهل إلى الأصعب — لا تكرّر نمط النشاط نفسه.",
        instructions ? `تعليمات إضافية من المعلّمة، التزم بها:\n${instructions}` : "",
        SHEET_RULES,
      ].filter(Boolean).join("\n\n");
      userMsg = `الصف: ${grade} | المادة: ${subject}\nالدرس: ${lessonNames.join("، ")}`;
    }

    // سقفٌ واسع: ورقة A4 كاملة بأشكال SVG مضمّنة تتجاوز بسهولة أربعة آلاف رمز،
    // وبلوغ السقف يقطع الورقة في منتصفها بلا رسالة خطأ.
    const orResp = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Worksheet Generator",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content: userMsg },
        ],
        temperature: edit ? 0.3 : 0.6,
        max_tokens: 16000,
      }),
    }, { st, task: "worksheet" });

    const or = await orResp.json();
    if (!orResp.ok) {
      const _m = String(or?.error?.message || or?.message || "");
      console.error(`openrouter ${orResp.status} في generate-worksheet: ${_m}`);
      return refund({ error: orErrCode(orResp.status, _m), detail: _m.slice(0, 200) }, 502);
    }

    const html = extractHtml(or?.choices?.[0]?.message?.content || "");
    if (!html || looksTruncated(html)) {
      return refund({ error: "bad_output", detail: html.slice(0, 300) }, 502);
    }

    return json({ html, model, usage: or?.usage || null });
  } catch (e) {
    // لا استرداد هنا: قد يقع الخطأ قبل تعريف refund أصلاً (وقبل خصم الحصّة)
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
