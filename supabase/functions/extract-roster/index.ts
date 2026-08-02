// ════════════════════════════════════════════════════════════════
// Edge Function: extract-roster
// يقرأ كشف أسماء طالبات (صورة أو PDF) ويعيد الأسماء وحدها.
//
// كتابةُ ثلاثين اسماً بيدها لكل شعبة هي أطول خطوةٍ في الإعداد وأكثرها
// مدعاةً للتوقّف عنده. والكشف موجودٌ عندها أصلاً من المدرسة.
//
// النموذج قويٌّ عمداً: هذه خطوةٌ تُنفَّذ مرّةً واحدة في العام، فالفرق في
// الكلفة لا يُذكر، أمّا اسمٌ يُقرأ خطأً فيبقى على الطالبة طول العام في
// النجوم والسلوك والشهادات.
//
// النشر: supabase functions deploy extract-roster
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { orFetch, pickVisionModel } from "../_shared/ai.ts";

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

// سقفٌ على المرفقات: الدالّة بلا حصّة (خطوةٌ تُنفَّذ مرّة)، فالسقف هو ما
// يمنع أن تصير باباً مفتوحاً لاستنزاف الرصيد.
const MAX_FILES = 4;
const MAX_BYTES = 8 * 1024 * 1024;   // لكل ملف، تقديراً من طول base64

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) return json({ error: "unauthorized" }, 401);

    const admin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );
    const { data: { user }, error: userErr } =
      await admin.auth.getUser(authHeader.replace("Bearer ", ""));
    if (userErr || !user) return json({ error: "unauthorized" }, 401);

    const apiKey = Deno.env.get("OPENROUTER_API_KEY");
    if (!apiKey) return json({ error: "server_not_configured" }, 500);

    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
    // gemini-2.5-pro لا flash: الأسماء العربية بخطّ اليد أو بمسحٍ رديء هي
    // بالضبط ما يفرّق فيه النموذج القوي.
    const model = pickVisionModel(st, "roster", "google/gemini-2.5-pro");

    const b = await req.json().catch(() => ({}));
    const files: { name?: string; data?: string }[] =
      Array.isArray(b.files) ? b.files.slice(0, MAX_FILES) : [];
    if (!files.length) return json({ error: "no_files" }, 400);

    const content: unknown[] = [{
      type: "text",
      text: 'استخرج أسماء الطالبات من هذا الكشف بهذا الشكل حصراً (JSON): {"names":["الاسم الأول","الاسم الثاني"]}',
    }];

    for (const f of files) {
      const url = String(f?.data || "");
      if (!url.startsWith("data:")) continue;
      if (url.length > MAX_BYTES * 1.4) return json({ error: "file_too_large" }, 413);
      if (url.startsWith("data:application/pdf")) {
        content.push({
          type: "file",
          file: { filename: String(f?.name || "roster.pdf"), file_data: url },
        });
      } else if (url.startsWith("data:image/")) {
        content.push({ type: "image_url", image_url: { url } });
      }
    }
    if (content.length < 2) return json({ error: "unsupported_type" }, 400);

    // التعليمات مكتوبةٌ حول ما يُفسد الكشف عملياً: الترقيم، والعناوين،
    // وأرقام الجلوس، والأعمدة المجاورة — لا حول «استخرج الأسماء» فحسب.
    const system = [
      "أنت مساعد يستخرج أسماء الطالبات من كشفٍ مدرسيّ عُماني (صورة أو PDF).",
      "أعد الأسماء فقط، كلَّ اسمٍ كاملاً كما هو مكتوب حرفياً بالعربية.",
      "احذف أرقام التسلسل، وأرقام الجلوس، وأرقام الهوية، والعناوين، وأسماء الصفوف والشعب والمواد، وأسماء المعلّمات، وأي عمودٍ غير عمود الأسماء (كالدرجات والغياب والملاحظات).",
      "لا تُصلح اسماً ولا تُغيّر إملاءه ولا تُضِف ألقاباً، وأبقِ «بنت» و«بن» كما وردت.",
      "لا تخترع اسماً غير موجود، ولا تُكمل كشفاً ناقصاً.",
      "احتفظ بترتيب ورودها في الكشف، واحذف التكرار الحرفيّ.",
      "إن لم تجد كشف أسماء في الملف فأعد قائمةً فارغة.",
      "أعد JSON فقط دون أي نص خارجه.",
    ].join("\n");

    const orResp = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Roster Extractor",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content },
        ],
        response_format: { type: "json_object" },
        temperature: 0,          // نقلٌ حرفيّ لا إنشاء
        max_tokens: 4000,
      }),
    }, { st, task: "roster" });

    const or = await orResp.json();
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);

    const text = or?.choices?.[0]?.message?.content || "";
    let parsed: { names?: unknown[] };
    try {
      parsed = JSON.parse(text);
    } catch (_) {
      const m = text.match(/\{[\s\S]*\}/);
      parsed = m ? JSON.parse(m[0]) : { names: [] };
    }

    // تنظيفٌ أخير على الخادم: النموذج قد يُبقي ترقيماً أو نقطاً رغم النهي،
    // وتصحيحها هنا أضمن من تركها تصل إلى كشف المعلّمة.
    const seen = new Set<string>();
    const names = (parsed?.names || [])
      .map((n) => String(n ?? "").replace(/^[\s\d.\-–—)(:،]+/, "").trim())
      .filter((n) => n.length >= 2 && n.length <= 80)
      .filter((n) => { const k = n.replace(/\s+/g, " "); if (seen.has(k)) return false; seen.add(k); return true; });

    return json({ names, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
