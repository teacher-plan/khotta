// v2026.09.01 ════════════════════════════════════════════════════════════════
// Edge Function: index-teacher-guide
// (للمشرف فقط) تقرأ فهرس دليل المعلم (أول صفحاته) بالرؤية، وتُطابقه مع
// فهرس الكتاب الموجود مسبقاً في curriculum لنفس (فصل/صف/مادة) — تمهيداً
// لتوليد تحضير كل درسٍ من صفحاته في الكتاب + دليل المعلم معاً.
//
// النشر: تلقائي عبر GitHub Actions
// الأسرار: OPENROUTER_API_KEY
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { parseAiJson } from "../_shared/aiJson.ts";
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

const ADMIN_EMAIL = "teacherplane2026project@gmail.com";
// عدد صفحات دليل المعلم التي نفحصها بحثاً عن الفهرس — عادة في المقدمة،
// لكن نمنح هامشاً (بعض الأدلة تضع فهرساً تفصيلياً بعد مقدمة طويلة).
const SCAN_PAGES = 25;

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
    if ((user.email || "").toLowerCase() !== ADMIN_EMAIL) return json({ error: "forbidden" }, 403);

    const apiKey = Deno.env.get("OPENROUTER_API_KEY");
    if (!apiKey) return json({ error: "server_not_configured" }, 500);

    const b = await req.json().catch(() => ({}));
    const guideId = parseInt(b.teacher_guide_id);
    if (!guideId) return json({ error: "no_guide_id" }, 400);

    const { data: guide, error: gErr } = await admin.from("teacher_guides").select("*").eq("id", guideId).maybeSingle();
    if (gErr || !guide) return json({ error: "guide_not_found" }, 404);
    if (!guide.base_path || !guide.page_count) return json({ error: "guide_not_uploaded" }, 400);

    await admin.from("teacher_guides").update({ status: "indexing" }).eq("id", guideId);

    const { data: curRows, error: cErr } = await admin
      .from("curriculum")
      .select("id,unit,lesson,sort,page")
      .eq("semester", guide.semester)
      .eq("grade", guide.grade)
      .eq("subject", guide.subject)
      .order("sort", { ascending: true });
    if (cErr || !curRows || !curRows.length) {
      await admin.from("teacher_guides").update({ status: "index_failed" }).eq("id", guideId);
      return json({ error: "no_curriculum_rows" }, 400);
    }

    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
    const model = ensureVision(st.model_guide_index || st.vision_model || "google/gemini-2.5-flash", "google/gemini-2.5-flash");

    const pub = (sheet: number) => admin.storage.from("library-files").getPublicUrl(`${guide.base_path}/p${sheet}.jpg`).data.publicUrl;
    const scanCount = Math.min(SCAN_PAGES, guide.page_count);
    const images: string[] = [];
    for (let i = 1; i <= scanCount; i++) images.push(pub(i));

    const curListText = curRows.map((r: { id: number; unit: string; lesson: string }) => `${r.id}: ${r.unit} — ${r.lesson}`).join("\n");

    const system = [
      "أنت خبيرٌ في مطابقة فهارس الكتب المدرسية العُمانية. أمامك صور صفحات من مقدمة دليل معلمٍ (تحتوي على فهرس/جدول محتويات في مكانٍ ما بينها).",
      "مهمتك: (١) حدد صفحة الفهرس واستخرج كل بند فيه (اسم الوحدة، اسم الدرس، رقم الصفحة كما هو مطبوع في الدليل).",
      "(٢) طابق كل بندٍ من فهرس الدليل مع أقرب درسٍ في قائمة دروس الكتاب المرقّمة أدناه (المطابقة بالمعنى لا بالنص الحرفي — قد يختلف صياغة اسم الدرس قليلاً بين الكتاب والدليل).",
      "قائمة دروس الكتاب (id: الوحدة — الدرس):",
      curListText,
      'أعد الناتج JSON فقط بهذا الشكل: {"entries":[{"guide_unit":"...","guide_lesson":"...","guide_page":12,"matched_curriculum_id":37,"confidence":"high"}]}',
      "confidence تكون high إن كانت المطابقة شبه مؤكدة، medium إن محتملة، low إن غير متأكد — واترك matched_curriculum_id فارغاً (null) إن لم تجد أي تطابق معقول.",
      "لا تخترع بنوداً غير موجودة فعلاً في صور الفهرس.",
    ].join("\n");

    const userContent: unknown[] = [{ type: "text", text: "صور صفحات دليل المعلم (ابحث عن الفهرس بينها):" }];
    for (const u of images) userContent.push({ type: "image_url", image_url: { url: u } });

    const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Guide Index Matcher",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          { role: "user", content: userContent },
        ],
        response_format: { type: "json_object" },
        temperature: 0.2,
        max_tokens: 4000,
      }),
    }, { st, task: "guide_index" });

    const j = await r.json();
    if (!r.ok) {
      const m = String(j?.error?.message || j?.message || "");
      console.error(`openrouter ${r.status} في index-teacher-guide: ${m}`);
      await admin.from("teacher_guides").update({ status: "index_failed" }).eq("id", guideId);
      return json({ error: orErrCode(r.status, m), detail: m.slice(0, 200) }, 502);
    }

    const text = j?.choices?.[0]?.message?.content || "";
    const parsed = parseAiJson<{ entries?: unknown[] }>(text);
    const entries = parsed.ok ? (parsed.value.entries || []) : [];
    if (!entries.length) {
      await admin.from("teacher_guides").update({ status: "index_failed" }).eq("id", guideId);
      return json({ error: "no_entries_found" }, 502);
    }

    await admin.from("teacher_guides").update({
      toc: entries,
      status: "indexed",
      indexed_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }).eq("id", guideId);

    return json({ entries, model, usage: j?.usage || null });
  } catch (e) {
    console.error("server_error:", String(e));
    return json({ error: "server_error" }, 500);
  }
});
