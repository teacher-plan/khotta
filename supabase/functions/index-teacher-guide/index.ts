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
// ⚠️ دفعةٌ واحدة لكل نداءٍ للدالّة، والعميل يُكرّر النداء متقدّماً:
// مسحُ الدفعات الستّ داخل نداءٍ واحد كان يستغرق دقائق فينقطع الاتصال قبل
// الردّ («Failed to send a request to the Edge Function» — فشلٌ في النقل لا
// خطأٌ من الدالّة، ظهر فعلياً في الرياضيات والإنجليزية بينما نجحت المواد
// التي وُجد فهرسها في أوّل دفعة). كل نداءٍ الآن نداءُ رؤيةٍ واحد (~٢٠ ثانية)
// فلا يقترب من أي مهلة، والتقدّم يظهر للمشرف دفعةً دفعة.
const SCAN_BATCH = 12;      // صفحات لكل نداء رؤية
const SCAN_MAX_PAGES = 132; // أقصى مدًى نبحث فيه عن الفهرس (١١ دفعة)
// ⚠️ رُفع من ٧٢ إلى ١٣٢: دليل رياضيات الصف الرابع (٢٠٤ صفحة) فشل فعلياً
// بفهرسٍ يقع بعد الصفحة ٧٢ — ٧٢ كانت كافيةً للأدلة الأصغر فقط.

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

    // ── إزاحة الترقيم ──
    // الفهرس يعطي رقم الصفحة *المطبوع*، وصورنا مرقّمة بترتيب ورق الـPDF.
    // الغلاف والمقدمات تجعل الاثنين مختلفَين، فترسل الواجهةُ صفحاتِ درسٍ
    // آخر بلا أن يشعر أحد. نقيسها هنا: نعرض ورقةً بعينها ونسأل النموذج عن
    // الرقم المطبوع عليها، فالإزاحة = رقم الورقة − المطبوع + ١.
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
    // نحسب الإزاحة من مدخلين مستقلّين من الفهرس ونقبلها فقط إن اتّفقا
    // (بفارق صفحةٍ واحدة كحدٍّ أقصى) بدل الاكتفاء بمرشّحٍ واحد قد يصادف
    // صفحة مقدّمةٍ أو رقم تمرينٍ فيُخرج إزاحةً خاطئة بصمت (وهذا فعلياً ما
    // حدث: ٣٠ بدل ٠-٣ المعتادة في أحد الأدلة).
    const computeOffset = async (idxEntries: unknown[], g: { offset_pages?: number | null; page_count: number }): Promise<number> => {
      let offsetPages = g.offset_pages || 1;
      try {
        const distinctPrinted = Array.from(new Set(
          (idxEntries as { guide_page?: number }[])
            .map((e) => e.guide_page)
            .filter((p): p is number => typeof p === "number" && p > 0),
        )).sort((a, b) => a - b);

        const candidateOffsets: number[] = [];
        for (const firstPrinted of distinctPrinted.slice(0, 3)) {
          let found: number | null = null;
          for (const probeSheet of [firstPrinted, Math.min(firstPrinted + 6, g.page_count)]) {
            const printed = await printedOnSheet(probeSheet);
            if (printed) { found = probeSheet - printed + 1; break; }
          }
          if (found !== null) candidateOffsets.push(found);
          if (candidateOffsets.length >= 2) break;
        }

        if (candidateOffsets.length >= 2 && Math.abs(candidateOffsets[0] - candidateOffsets[1]) <= 1) {
          offsetPages = candidateOffsets[0];
        } else if (candidateOffsets.length >= 2) {
          console.error(`index-teacher-guide: إزاحةٌ غير متّفقٍ عليها لدليل ${guideId} (${candidateOffsets.join(", ")}) — أُبقيت القيمة السابقة ${offsetPages} بلا تحديث.`);
        } else if (candidateOffsets.length === 1) {
          offsetPages = candidateOffsets[0];
        }
      } catch (e) {
        console.error("offset probe failed (نُبقي الإزاحة كما هي):", String(e));
      }
      return offsetPages;
    };

    // دفعةٌ واحدة لكل نداء: العميل يبدأ بـscan_from=1 ويتقدّم بما يُعيده
    // next_from حتى يُعثر على الفهرس أو يُستنفد المدى.
    // ⚠️ أفضل مطابقةٍ حتى الآن تُمرَّر ذهاباً وإياباً مع العميل (best_entries/
    // best_count) لأن كل نداءٍ عديم الحالة: صفحة فهرسٍ فرعية صغيرة (مثلاً
    // فهرس وحدةٍ واحدة من ٢-٣ دروس) كانت تُقبل فوراً بمجرّد وجود أي بند،
    // فيتوقّف البحث قبل بلوغ الفهرس الرئيسي الحقيقي — وهذا فعلياً ما خفض
    // نسبة التغطية (بعض الأدلة انتهت بفهرسٍ من بندين أو ثلاثة فقط بينما
    // منهج الفصل عشرات الدروس).
    const lastPage = Math.min(SCAN_MAX_PAGES, guide.page_count);
    const start = Math.max(1, parseInt(b.scan_from) || 1);
    const bestEntriesIn: unknown[] = Array.isArray(b.best_entries) ? b.best_entries : [];
    const bestCountIn = new Set(
      (bestEntriesIn as { matched_curriculum_id?: number | null }[]).map((e) => e.matched_curriculum_id).filter((v) => v != null),
    ).size;
    // فهرسٌ حقيقي للفصل يُغطّي عادةً معظم دروسه؛ نقبل دفعةً فوراً فقط إن
    // بلغت هذا الحدّ، وإلا نُبقيها كأفضل مرشّحٍ مؤقّت ونواصل البحث.
    // مقيَّدٌ بعدد دروس الفصل نفسه: حدٌّ أدنى ٨ كان يجعل الهدف مستحيلاً في
    // موادّ صغيرةٍ (فصلٌ بستّة دروسٍ فقط مثلاً) فيفشل الفهرس دائماً مهما
    // كان صحيحاً.
    const neededEntries = Math.min(curRows.length, Math.max(4, Math.ceil(curRows.length * 0.4)));
    if (start > lastPage) {
      if (bestCountIn > 0) {
        console.error(`index-teacher-guide: لم يُعثر على فهرسٍ كاملٍ في الصفحات ١-${lastPage}، استُخدم أفضل مرشّحٍ جزئي بـ${bestCountIn} بنداً فقط من أصل ${curRows.length} درساً (دليل ${guideId}، ${guide.subject} صف ${guide.grade}).`);
        const offsetPages = await computeOffset(bestEntriesIn, guide);
        await admin.from("teacher_guides").update({
          toc: bestEntriesIn, offset_pages: offsetPages, status: "indexed",
          indexed_at: new Date().toISOString(), updated_at: new Date().toISOString(),
        }).eq("id", guideId);
        return json({ done: true, entries: bestEntriesIn, partial: true, scanned_to: lastPage, offset_pages: offsetPages });
      }
      console.error(`index-teacher-guide: لم يُعثر على فهرس في الصفحات ١-${lastPage} (دليل ${guideId}، ${guide.subject} صف ${guide.grade}، ${guide.page_count} صفحة)`);
      await admin.from("teacher_guides").update({ status: "index_failed" }).eq("id", guideId);
      return json({ error: "index_not_found", detail: `لم يُعثر على فهرسٍ في أول ${lastPage} صفحة من الدليل (عدد صفحاته ${guide.page_count})` }, 502);
    }
    const end = Math.min(start + SCAN_BATCH - 1, lastPage);
    const scannedTo = end;

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
      // خطأٌ عابرٌ في دفعةٍ واحدة (حدّ معدّل، انقطاعٌ مؤقّت) لا يجوز أن
      // يُسقط ما جُمع من مطابقاتٍ في الدفعات السابقة — كان يحدث فعلياً:
      // status يُصبح index_failed بينما toc القديم يبقى بلا تحديث، فيظهر
      // الدليل "فاشلاً" رغم مطابقاتٍ سابقة صحيحة كانت قد جُمعت هذا التشغيل.
      if (bestCountIn > 0) {
        return json({ done: false, exhausted: false, next_from: start, scanned_to: start - 1, best_entries: bestEntriesIn, retry_after_error: true });
      }
      await admin.from("teacher_guides").update({ status: "index_failed" }).eq("id", guideId);
      return json({ error: orErrCode(r.status, m), detail: m.slice(0, 200) }, 502);
    }

    const text = j?.choices?.[0]?.message?.content || "";
    const parsed = parseAiJson<{ entries?: unknown[] }>(text);
    const rawEntries: unknown[] = parsed.ok ? (parsed.value.entries || []) : [];
    const usage = j?.usage || null;

    // ── تعويض فهرسٍ بمستوى الوحدة لا الدرس ──
    // بعض الأدلة لا تملك فهرساً يُدرج كل درسٍ برقم صفحته؛ فهرسها الوحيد
    // (عادةً في مقدّمة الدليل) يذكر عنوان كل وحدةٍ فقط، فيترك النموذج
    // matched_curriculum_id فارغاً لكل بند — إذ لا يستطيع اختيار درساً
    // واحداً من بين دروس الوحدة الثلاثة بلا معلومةٍ إضافية. فعلياً هذا هو
    // ما حدث في "الهوية والمواطنة" (فهرسٌ كاملٌ ٩ بنود، صفر مطابقة).
    // نُكمل هنا: لكل بندٍ غير مطابقٍ له عنوان وحدةٍ يُطابق وحدةً في منهج
    // الكتاب، نوزّع دروس تلك الوحدة على مدى صفحاتها (من بداية الوحدة إلى
    // بداية الوحدة التالية) بالتساوي — تقديرٌ تقريبي (confidence: low)
    // أفضل من مطابقةٍ معدومة، ويبقى المشرف قادراً على تصحيحه يدوياً.
    const alreadyMatched = new Set(
      rawEntries.map((e) => (e as { matched_curriculum_id?: number | null }).matched_curriculum_id).filter((v) => v != null),
    );
    const unitEntries = (rawEntries as { guide_unit?: string | null; guide_page?: number; matched_curriculum_id?: number | null }[])
      .filter((e) => e.matched_curriculum_id == null && e.guide_unit && typeof e.guide_page === "number")
      .sort((a, b) => (a.guide_page || 0) - (b.guide_page || 0));
    const derived: unknown[] = [];
    for (let i = 0; i < unitEntries.length; i++) {
      const ue = unitEntries[i];
      const unitLessons = curRows
        .filter((r: { unit?: string }) => r.unit && ue.guide_unit && r.unit.trim() === (ue.guide_unit as string).trim())
        .filter((r: { id: number }) => !alreadyMatched.has(r.id))
        .sort((a: { sort: number }, b: { sort: number }) => a.sort - b.sort);
      if (!unitLessons.length) continue;
      const startPage = ue.guide_page as number;
      const nextPage = unitEntries[i + 1]?.guide_page;
      unitLessons.forEach((lessonRow: { id: number; unit: string; lesson: string }, idx: number) => {
        const guess = typeof nextPage === "number"
          ? Math.round(startPage + ((nextPage - startPage) * idx) / unitLessons.length)
          : startPage;
        derived.push({
          guide_unit: ue.guide_unit, guide_lesson: lessonRow.lesson, guide_page: guess,
          matched_curriculum_id: lessonRow.id, confidence: "low", derived: true,
        });
      });
    }
    const entries: unknown[] = rawEntries.concat(derived);
    const matchedCount = new Set(
      (entries as { matched_curriculum_id?: number | null }[]).map((e) => e.matched_curriculum_id).filter((v) => v != null),
    ).size;

    // أفضل مرشّحٍ نعرفه حتى الآن (المُمرَّر من العميل، أو هذه الدفعة إن
    // كانت أكبر منه) — يُستعمل إن استُنفد المدى بلا فهرسٍ يبلغ neededEntries.
    // المقياس هو عدد الدروس المُطابَقة فعلياً لا عدد بنود الفهرس الخام،
    // فبعض الأدلة تُخرج بنوداً كثيرة لكن قلّةً منها تُطابَق (رياضياتٌ مثلاً).
    const bestSoFar = matchedCount > bestCountIn ? entries : bestEntriesIn;

    if (matchedCount < neededEntries) {
      // دفعةٌ فيها بندٌ أو بضعة — على الأرجح فهرس وحدةٍ فرعي لا الفهرس
      // الرئيسي لدروس الفصل كاملةً. لا نقبلها فوراً؛ نُبقيها كأفضل مرشّح
      // ونواصل البحث عن فهرسٍ أشمل في الصفحات التالية.
      const nextFrom = end + 1;
      if (nextFrom > lastPage) {
        if (bestSoFar.length) {
          console.error(`index-teacher-guide: لم يُعثر على فهرسٍ يبلغ ${neededEntries} بنداً، استُخدم أفضل مرشّحٍ جزئي بـ${bestSoFar.length} بنداً (دليل ${guideId}، ${guide.subject} صف ${guide.grade}).`);
          const offsetPages = await computeOffset(bestSoFar, guide);
          await admin.from("teacher_guides").update({
            toc: bestSoFar, offset_pages: offsetPages, status: "indexed",
            indexed_at: new Date().toISOString(), updated_at: new Date().toISOString(),
          }).eq("id", guideId);
          return json({ done: true, entries: bestSoFar, partial: true, scanned_to: scannedTo, offset_pages: offsetPages });
        }
        console.error(`index-teacher-guide: لم يُعثر على فهرس في الصفحات ١-${lastPage} (دليل ${guideId}، ${guide.subject} صف ${guide.grade}، ${guide.page_count} صفحة)`);
        await admin.from("teacher_guides").update({ status: "index_failed" }).eq("id", guideId);
        return json({ done: false, exhausted: true, scanned_to: scannedTo, detail: `لم يُعثر على فهرسٍ في أول ${lastPage} صفحة` });
      }
      return json({ done: false, exhausted: false, next_from: nextFrom, scanned_to: scannedTo, best_entries: bestSoFar });
    }

    const offsetPages = await computeOffset(entries, guide);

    await admin.from("teacher_guides").update({
      toc: entries,
      offset_pages: offsetPages,
      status: "indexed",
      indexed_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    }).eq("id", guideId);

    return json({ done: true, entries, model, usage, scanned_to: scannedTo, offset_pages: offsetPages });
  } catch (e) {
    console.error("server_error:", String(e));
    return json({ error: "server_error" }, 500);
  }
});
