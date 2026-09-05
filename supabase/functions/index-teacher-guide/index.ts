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
// البحث عن الفهرس يتم على دفعاتٍ متتابعة لا دفعةً واحدة: أوّل محاولةٍ فعلية
// أرسلت أوّل ٢٥ صفحة من دليلٍ عدده ٤٠٤ صفحات فلم تجد الفهرس (رجع
// no_entries_found)، لأن الأدلة الكبيرة تضع فهرسها بعد مقدماتٍ وأُطرٍ عامة
// طويلة. نمسح الآن مدًى أوسع، لكن على دفعاتٍ صغيرة نتوقف عند أوّل دفعةٍ
// يظهر فيها الفهرس — فلا ندفع ثمن الصفحات الباقية بلا داعٍ.
const SCAN_BATCH = 12;      // صفحات لكل نداء رؤية
const SCAN_MAX_PAGES = 72;  // أقصى مدًى نبحث فيه عن الفهرس (٦ دفعات)

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

    const curListText = curRows.map((r: { id: number; unit: string; lesson: string }) => `${r.id}: ${r.unit} — ${r.lesson}`).join("\n");

    const system = [
      "أنت خبيرٌ في مطابقة فهارس الكتب المدرسية العُمانية. أمامك صورُ صفحاتٍ متتابعة من دليل معلم؛ قد تحتوي على فهرس/جدول محتويات وقد لا تحتوي.",
      "مهمتك: (١) إن وُجدت صفحة فهرسٍ بين الصور، استخرج كل بندٍ فيها (اسم الوحدة، اسم الدرس، رقم الصفحة كما هو مطبوع في الدليل).",
      "(٢) طابق كل بندٍ من فهرس الدليل مع أقرب درسٍ في قائمة دروس الكتاب المرقّمة أدناه (المطابقة بالمعنى لا بالنص الحرفي — قد تختلف صياغة اسم الدرس قليلاً بين الكتاب والدليل).",
      "قائمة دروس الكتاب (id: الوحدة — الدرس):",
      curListText,
      'أعد الناتج JSON فقط بهذا الشكل: {"entries":[{"guide_unit":"...","guide_lesson":"...","guide_page":12,"matched_curriculum_id":37,"confidence":"high"}]}',
      "confidence تكون high إن كانت المطابقة شبه مؤكدة، medium إن محتملة، low إن غير متأكد — واترك matched_curriculum_id فارغاً (null) إن لم تجد أي تطابق معقول.",
      "لا تخترع بنوداً غير موجودة فعلاً في صور الفهرس.",
      'مهمٌّ جداً: إن لم تكن هذه الصور تحوي فهرساً إطلاقاً (صفحات مقدمةٍ أو دروسٍ عادية) فأعد {"entries":[]} بلا أي اجتهاد.',
    ].join("\n");

    // مسحٌ على دفعات: نتوقف عند أوّل دفعةٍ يظهر فيها الفهرس فعلاً.
    const lastPage = Math.min(SCAN_MAX_PAGES, guide.page_count);
    let entries: unknown[] = [];
    let usage: unknown = null;
    let scannedTo = 0;

    for (let start = 1; start <= lastPage && !entries.length; start += SCAN_BATCH) {
      const end = Math.min(start + SCAN_BATCH - 1, lastPage);
      scannedTo = end;
      const userContent: unknown[] = [{
        type: "text",
        text: `صفحات دليل المعلم من ${start} إلى ${end} — ابحث عن الفهرس بينها:`,
      }];
      for (let i = start; i <= end; i++) userContent.push({ type: "image_url", image_url: { url: pub(i) } });

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
        console.error(`openrouter ${r.status} في index-teacher-guide (صفحات ${start}-${end}): ${m}`);
        await admin.from("teacher_guides").update({ status: "index_failed" }).eq("id", guideId);
        return json({ error: orErrCode(r.status, m), detail: m.slice(0, 200) }, 502);
      }

      const text = j?.choices?.[0]?.message?.content || "";
      const parsed = parseAiJson<{ entries?: unknown[] }>(text);
      const batch = parsed.ok ? (parsed.value.entries || []) : [];
      if (batch.length) { entries = batch; usage = j?.usage || null; }
    }

    if (!entries.length) {
      // يُسجَّل صراحةً: أوّل فشلٍ حقيقي مرّ صامتاً بلا أثرٍ في السجلّ فتعذّر
      // تشخيصه إلا بقراءة رمز الحالة وحده.
      console.error(`index-teacher-guide: لم يُعثر على فهرس في الصفحات ١-${scannedTo} (دليل ${guideId}، ${guide.subject} صف ${guide.grade}، ${guide.page_count} صفحة)`);
      await admin.from("teacher_guides").update({ status: "index_failed" }).eq("id", guideId);
      return json({ error: "index_not_found", detail: `لم يُعثر على فهرسٍ في أول ${scannedTo} صفحة من الدليل (عدد صفحاته ${guide.page_count})` }, 502);
    }

    // ── إزاحة الترقيم ──
    // الفهرس يعطي رقم الصفحة *المطبوع*، وصورنا مرقّمة بترتيب ورق الـPDF.
    // الغلاف والمقدمات تجعل الاثنين مختلفَين، فترسل الواجهةُ صفحاتِ درسٍ
    // آخر بلا أن يشعر أحد. نقيسها هنا مرّةً واحدة: نعرض ورقةً بعينها ونسأل
    // النموذج عن الرقم المطبوع عليها، فالإزاحة = رقم الورقة − المطبوع + ١.
    // (نفس معنى offset_pages في book_sources الذي يضبطه المشرف يدوياً للكتاب.)
    const printedOnSheet = async (sheet: number): Promise<number | null> => {
      const rr = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Guide Offset Probe",
        },
        body: JSON.stringify({
          model,
          messages: [{
            role: "user",
            content: [
              { type: "text", text: 'ما رقم الصفحة المطبوع على هذه الصفحة (عادةً في أعلاها أو أسفلها)؟ أعد JSON فقط بالشكل {"printed": 12} أو {"printed": null} إن لم يظهر رقمٌ مطبوع.' },
              { type: "image_url", image_url: { url: pub(sheet) } },
            ],
          }],
          response_format: { type: "json_object" },
          temperature: 0,
          max_tokens: 100,
        }),
      }, { st, task: "guide_index" });
      if (!rr.ok) return null;
      const jj = await rr.json();
      const pp = parseAiJson<{ printed?: number | null }>(jj?.choices?.[0]?.message?.content || "");
      const v = pp.ok ? pp.value.printed : null;
      return typeof v === "number" && isFinite(v) && v > 0 ? v : null;
    };

    let offsetPages = guide.offset_pages || 1;
    try {
      const firstPrinted = (entries as { guide_page?: number }[])
        .map((e) => e.guide_page).filter((p): p is number => typeof p === "number" && p > 0)
        .sort((a, b) => a - b)[0];
      if (firstPrinted) {
        // نجرّب ورقتين: الورقة المساوية للرقم المطبوع، ثم واحدةٌ أبعد قليلاً
        // إن لم يظهر رقمٌ على الأولى (صفحاتُ بدايةِ الوحدات كثيراً بلا ترقيم).
        for (const probeSheet of [firstPrinted, Math.min(firstPrinted + 6, guide.page_count)]) {
          const printed = await printedOnSheet(probeSheet);
          if (printed) { offsetPages = probeSheet - printed + 1; break; }
        }
      }
    } catch (e) {
      console.error("offset probe failed (نُبقي الإزاحة كما هي):", String(e));
    }

    await admin.from("teacher_guides").update({
      toc: entries,
      offset_pages: offsetPages,
      status: "indexed",
      indexed_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }).eq("id", guideId);

    return json({ entries, model, usage, scanned_to: scannedTo, offset_pages: offsetPages });
  } catch (e) {
    console.error("server_error:", String(e));
    return json({ error: "server_error" }, 500);
  }
});
