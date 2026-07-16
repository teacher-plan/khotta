// v2026.07.10 ════════════════════════════════════════════════════════════════
// Edge Function: generate-game-content
// يولّد محتوى لعبة تعليمية (أزواج مطابقة / أسئلة اختيار / قائمة عناصر)
// من درس محدد — ويقرأ صفحات الكتاب الفعلية إن كانت المادة مقطَّعة.
// نموذج نصي اقتصادي؛ المحتوى JSON يُصب داخل قوالب لعب مُختبرة في الواجهة.
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

    // ⛔ حصة الاستخدام الشهرية — تُفرض على الخادم
    const quota = await takeQuota(admin, user.id, user.email || "", "text", st);
    if (!quota.ok) return json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);

    const b = await req.json().catch(() => ({}));
    const grade = String(b.grade || "");
    const subject = String(b.subject || "");
    const lessonNames: string[] = Array.isArray(b.lessonNames) ? b.lessonNames.map(String) : [];
    const structure = ["pairs", "quiz", "items", "groups"].includes(b.structure) ? b.structure : "quiz";
    const count = Math.max(3, Math.min(15, parseInt(b.count) || 6));
    const images: string[] = Array.isArray(b.images) ? b.images.slice(0, 12) : [];
    if (!lessonNames.length) return json({ error: "no_lessons" }, 400);

    // مع صفحات الكتاب: نموذج رؤية مضمون دائماً (ai_model قد يكون نصياً فيُسقط الصور بصمت)
    const model = images.length
      ? (st.vision_model || "google/gemini-2.5-flash")
      : (st.ai_model || "google/gemini-2.5-flash");

    const gradeNum = parseInt(grade) || 0;
    const age = gradeNum ? gradeNum + 6 : 0;

    // الهيكل المطلوب حسب نوع اللعبة
    const schemas: Record<string, string> = {
      pairs: '{"items":[{"a":"المصطلح أو المفهوم (قصير)","b":"معناه أو مقابله (قصير)"}]}',
      quiz: '{"items":[{"q":"نص السؤال","c":["خيار ١","خيار ٢","خيار ٣","خيار ٤"],"a":0}]}',
      items: '{"items":["سؤال أو عنصر قصير","سؤال آخر"]}',
      groups: '{"groupNames":["اسم المجموعة الأولى","اسم المجموعة الثانية"],"items":[{"t":"عنصر قصير","g":0}]}',
    };
    const structureNotes: Record<string, string> = {
      pairs: "أزواج مطابقة: كل زوج مصطلح/مفهوم من الدرس ومعناه. اجعل النصين قصيرين (كلمة إلى ٦ كلمات) ليظهرا على بطاقات لعب صغيرة.",
      quiz: "أسئلة اختيار من متعدد بأربعة خيارات، حقل a هو موضع الإجابة الصحيحة (٠-٣). أسئلة قصيرة مباشرة تناسب مسابقة سريعة موقوتة على شاشة الصف.",
      items: "قائمة أسئلة/مهام قصيرة جداً (سطر واحد) تُكتب على قطاعات عجلة عشوائية أو داخل صناديق مغلقة — يُسأل بها الطالب شفهياً.",
      groups: "تصنيف: اختر تصنيفاً ثنائياً جوهرياً في الدرس (مثل: مذكر/مؤنث، صلب/سائل، أكبر من/أصغر من)، ضع اسمي المجموعتين في groupNames، وكل عنصر قصير مع حقل g يحدد مجموعته الصحيحة (٠ أو ١). وزّع العناصر بالتساوي تقريباً.",
    };

    const system = [
      "أنت معلم خبير في سلطنة عُمان (منهج كامبردج) تعدّ محتوى لعبة صفية تعليمية ممتعة.",
      age ? `أعمار الطلاب: ${age} سنوات تقريباً (الصف ${grade}) — لغة وأمثلة تناسب هذا العمر تماماً.` : "",
      images.length
        ? "الصور المرفقة صفحات هذا الدرس من كتاب الطالب المعتمد — ابنِ المحتوى من مفاهيمها وأمثلتها الفعلية حصراً."
        : "لا صور مرفقة من الكتاب — بناءً على خبرتك بمنهج كامبردج المعتمد في سلطنة عُمان لهذا الصف والمادة، توقّع المحتوى الفعلي المرجّح لهذا الدرس تحديداً (لا محتوى عام) واستخدمه مباشرة بثقة.",
      structureNotes[structure],
      `أنشئ ${count} عنصراً بالضبط. عربية فصحى سليمة، بلا تكرار، متدرجة السهولة.`,
      `أعد JSON فقط بهذا الشكل حصراً: ${schemas[structure]}`,
    ].filter(Boolean).join("\n");

    const userMsg = `الصف: ${grade} | المادة: ${subject}\nالدرس: ${lessonNames.join("، ")}`;
    const userContent: unknown[] = [{ type: "text", text: userMsg }];
    for (const u of images) userContent.push({ type: "image_url", image_url: { url: u } });

    const callOr = (withImages: boolean) =>
      fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Game Generator",
        },
        body: JSON.stringify({
          model,
          messages: [
            { role: "system", content: system },
            { role: "user", content: withImages ? userContent : userMsg },
          ],
          response_format: { type: "json_object" },
          temperature: 0.5,
          max_tokens: 2000,
        }),
      });
    let grounded = images.length > 0;
    let orResp = await callOr(images.length > 0);
    let or = await orResp.json();
    // النموذج لا يدعم الصور؟ نعيد المحاولة نصياً — مع إعلام الواجهة (grounded=false)
    if (!orResp.ok && images.length && /image input|multimodal|support image/i.test(JSON.stringify(or))) {
      grounded = false;
      orResp = await callOr(false);
      or = await orResp.json();
    }
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);

    const text = or?.choices?.[0]?.message?.content || "";
    let parsed: { items?: unknown[]; groupNames?: string[] } | null = null;
    try { parsed = JSON.parse(text); }
    catch (_) { const m = text.match(/\{[\s\S]*\}/); parsed = m ? JSON.parse(m[0]) : null; }
    if (!parsed || !Array.isArray(parsed.items) || !parsed.items.length) {
      return json({ error: "bad_output", detail: text.slice(0, 300) }, 502);
    }
    return json({ items: parsed.items, groupNames: parsed.groupNames || null, structure, grounded, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
