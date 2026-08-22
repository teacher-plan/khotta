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
import { takeQuota, refundQuota, logAiCost } from "../_shared/quota.ts";
import { parseAiJson, requireArray } from "../_shared/aiJson.ts";

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
    if (st.generator_enabled === "0") return json({ error: "disabled" }, 403);

    // ⛔ حصة الاستخدام الشهرية — كانت هذه الدالة وحدها بلا حصة رغم أنها
    // تُستدعى من حساب المعلّمة وترفع حتى أربع صور إلى أغلى نموذجٍ في المنصة:
    // رفعٌ متكرّر واحد كان يستنزف بلا أن يُحسب على أحد. تُحسَب على حصة الصور
    // لأن مدخلها صورٌ لا نصّ.
    const quota = await takeQuota(admin, user.id, user.email || "", "img", st);
    // تمييزٌ لازم: fail-closed يعني أنّ عطلاً في القاعدة يمنع التوليد أيضاً —
    // فلو قلنا «نفد رصيدك» لكذبنا على المعلّمة وأرسلناها تشكو رصيداً سليماً.
    if (!quota.ok) return quota.error === "quota_unavailable"
      ? json({ error: "quota_unavailable" }, 503)
      : json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);
    const refund = async (body: Record<string, unknown>, status: number) => {
      await refundQuota(admin, user.id, user.email || "", "img");
      return json(body, status);
    };

    // النموذج نفسه الذي يقرأ صفحات الكتاب: كان هنا gemini-2.5-pro بحجّة خطّ
    // اليد، والحجّة لا تصمد — الكشف يأتي المعلّمة من المدرسة مطبوعاً أو ملفَّ
    // Word، وملفّات Word وExcel تصل نصّاً مفكوكاً فلا رؤية فيها أصلاً. وما
    // بقي كشفٌ مطبوع، وهو أسهل من صفحة كتابٍ بجداولها وأشكالها.
    const model = pickVisionModel(st, "roster", "google/gemini-2.5-flash");

    const b = await req.json().catch(() => ({}));
    const files: { name?: string; data?: string; text?: string }[] =
      Array.isArray(b.files) ? b.files.slice(0, MAX_FILES) : [];
    if (!files.length) return refund({ error: "no_files" }, 400);

    const content: unknown[] = [{
      type: "text",
      text: 'استخرج أسماء الطلاب والطالبات من هذا الكشف بهذا الشكل حصراً (JSON): {"names":["الاسم الأول","الاسم الثاني"]}',
    }];

    // ملفّات Word/Excel/CSV تصل نصّاً مفكوكاً من المتصفّح: النموذج لا يقرأ
    // docx/xlsx فهما ZIP، والفكّ في الخادم يستدعي مكتبةً لخطوةٍ يفعلها
    // المتصفّح مجّاناً. ويبقى دور النموذج هنا قائماً — فالنصّ المفكوك يحمل
    // ترويسات الجدول وأرقام التسلسل والأعمدة المجاورة، وتنقيتُها هي المهمّة.
    for (const f of files) {
      const txt = String(f?.text || "").slice(0, 20000).trim();
      if (txt) {
        content.push({
          type: "text",
          text: `محتوى الملف «${String(f?.name || "قائمة").slice(0, 80)}»:\n${txt}`,
        });
        continue;
      }
      const url = String(f?.data || "");
      if (!url.startsWith("data:")) continue;
      if (url.length > MAX_BYTES * 1.4) return refund({ error: "file_too_large" }, 413);
      if (url.startsWith("data:application/pdf")) {
        content.push({
          type: "file",
          file: { filename: String(f?.name || "roster.pdf"), file_data: url },
        });
      } else if (url.startsWith("data:image/")) {
        content.push({ type: "image_url", image_url: { url } });
      }
    }
    if (content.length < 2) return refund({ error: "unsupported_type" }, 400);

    // التعليمات مكتوبةٌ حول ما يُفسد الكشف عملياً: الترقيم، والعناوين،
    // وأرقام الجلوس، والأعمدة المجاورة — لا حول «استخرج الأسماء» فحسب.
    const system = [
      "أنت مساعد يستخرج أسماء الطلاب (ذكوراً وإناثاً) من كشفٍ مدرسيّ عُماني (صورة أو PDF أو نصٍّ مستخرَج من ملف Word أو Excel) — لا تفترض جنساً واحداً، فبعض الشعب مختلطة.",
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
    if (!orResp.ok) {
      // نفاد الرصيد ليس «عطلاً في الاتصال»، ورسالةٌ عامّة تجعل المعلّمة تُعيد
      // المحاولة مراراً بلا جدوى وتظنّ العطل في ملفّها أو شبكتها.
      const msg = String(or?.error?.message || or?.message || "");
      const code = orResp.status === 402 || /credit|quota|insufficient|balance|payment/i.test(msg)
        ? "no_credit"
        : orResp.status === 429 ? "busy" : "provider_error";
      console.error(`openrouter ${orResp.status} في extract-roster: ${msg}`);
      return refund({ error: code, detail: msg.slice(0, 200) }, 502);
    }

    const text = or?.choices?.[0]?.message?.content || "";
    const p = parseAiJson<{ names?: unknown[] }>(text);
    if (!p.ok) {
      console.error(`extract-roster: تعذّر التحليل (${p.reason})`, p.raw);
      return refund({ error: "bad_ai_output", detail: p.raw }, 502);
    }
    const arr = requireArray(p.value, "names");
    if (!arr.ok) return refund({ error: "bad_ai_output", detail: arr.reason }, 502);

    // تنظيفٌ أخير على الخادم: النموذج قد يُبقي ترقيماً أو نقطاً رغم النهي،
    // وتصحيحها هنا أضمن من تركها تصل إلى كشف المعلّمة.
    const seen = new Set<string>();
    const names = arr.items
      .map((n) => String(n ?? "").replace(/^[\s\d.\-–—)(:،]+/, "").trim())
      .filter((n) => n.length >= 2 && n.length <= 80)
      .filter((n) => { const k = n.replace(/\s+/g, " "); if (seen.has(k)) return false; seen.add(k); return true; });

    await logAiCost(admin, user.id, "extract-roster", "img", model, or?.usage);
    return json({ names, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
