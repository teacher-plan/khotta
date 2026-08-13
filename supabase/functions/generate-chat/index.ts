// v2026.07.10 ════════════════════════════════════════════════════════════════
// Edge Function: generate-chat
// «خُطّة AI» — مساعدٌ ذكيٌّ عامّ، ويقرأ سياق المعلم حين يكون السؤال عن عمله
// (صفوفه وموادّه ودرس اليوم). يحفظ المحادثة في ai_chats (وينشئ الجدول
// ذاتياً إن لم تُطبَّق الهجرة) ويعيد الرد.
//
// النشر: تلقائي عبر GitHub Actions
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

async function ensureChatTable() {
  const dbUrl = Deno.env.get("SUPABASE_DB_URL");
  if (!dbUrl) throw new Error("no SUPABASE_DB_URL");
  const { default: postgres } = await import("https://deno.land/x/postgresjs@v3.4.5/mod.js");
  const sql = postgres(dbUrl, { prepare: false });
  try {
    await sql.unsafe(`
      create table if not exists ai_chats (
        id uuid primary key default gen_random_uuid(),
        user_id uuid not null default auth.uid(),
        title text,
        messages jsonb not null default '[]'::jsonb,
        created_at timestamptz default now(),
        updated_at timestamptz default now()
      );
      alter table ai_chats enable row level security;
      drop policy if exists "chats_own" on ai_chats;
      create policy "chats_own" on ai_chats for all to authenticated
        using (user_id = auth.uid()) with check (user_id = auth.uid());
    `);
  } finally {
    await sql.end({ timeout: 3 });
  }
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
    let webOn = false;
    let imgOn = false;
    const refund = async (body: Record<string, unknown>, status: number) => {
      await refundQuota(admin, user.id, user.email || "", "text");
      if (webOn) await refundQuota(admin, user.id, user.email || "", "search");
      if (imgOn) await refundQuota(admin, user.id, user.email || "", "img");
      return json(body, status);
    };

    const b = await req.json().catch(() => ({}));
    const chatId = typeof b.chatId === "string" && b.chatId ? b.chatId : null;
    const userMsg = String(b.message || "").trim().slice(0, 2000);
    // كان السقف ١٥٠٠ حرفاً والعميل يرسل حتى ٢٨٠٠ — فيُقصّ نصف السياق صامتاً،
    // ويقع القصّ على آخره حيث النجوم والسلوك والإنجازات: أدقّ ما فيه وأكثره
    // فائدةً في سؤالٍ عن طالبةٍ بعينها. صار السقف يسع ما يُرسَل.
    const context = String(b.context || "").slice(0, 3200);
    // بحث الويب اختياريّ بضغطةٍ من المعلّمة، لا تلقائيّ: لكلّ استعمالٍ ثمنٌ
    // يقارب أربعين رسالةً عادية، فتفعيله على كل سؤالٍ يُنفق بلا حاجة
    const web = b.web === true;
    // حصة بحثٍ منفصلة: من نفدت حصةُ بحثها يُجاب سؤالها بلا بحث، ولا يُمنع
    if (web) {
      const wq = await takeQuota(admin, user.id, user.email || "", "search", st);
      webOn = wq.ok;
    }
    // آخر رسائل المحادثة من العميل (ثمانٍ: التاريخ يُعاد قراءته كاملاً مع
    // كل سؤال، فطوله يبطّئ أوّل حرفٍ في الردّ أكثر مما ينفع سياقه)
    const history: Array<{ role: string; content: string }> =
      (Array.isArray(b.history) ? b.history : [])
        .filter((m: { role?: string; content?: string }) => (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
        .slice(-8)
        .map((m: { role: string; content: string }) => ({ role: m.role, content: String(m.content).slice(0, 2000) }));
    // صورٌ ترفعها المعلمة ليقرأها المساعد (صفحة كتاب، ورقة طالبة، تعميم إداري).
    // أربع كحد أقصى: المدخل يُحاسب بالحجم، وأربع تكفي درساً كاملاً.
    const images: string[] = (Array.isArray(b.images) ? b.images : [])
      .filter((u: unknown) => typeof u === "string" && /^data:image\//.test(u as string))
      .slice(0, 4) as string[];
    if (!userMsg && !images.length) return json({ error: "no_message" }, 400);

    // ═ طلب رسم صورة ═
    // ترسله الواجهة صريحاً بزرٍّ تضغطه المعلّمة، ولا نستنبطه من نصّها:
    // الاستنباط يخطئ في الاتجاهين، وكلا خطأيه مكلف. «اشرحي لي الصورة»
    // تُقرأ طلبَ رسم فتدفع ثمن صورةٍ لم تُرَد، و«أريد شيئاً يوضّح الدرس»
    // تُقرأ سؤالاً فتأتيها فقرةُ نصٍّ وهي تنتظر رسماً. والزرّ لا يلتبس.
    const wantImage = b.makeImage === true;
    const imageModel = st.model_chat_image || st.model_infographic || st.slide_model
                    || "google/gemini-3.1-flash-image-preview";

    // الصورة تُخصم من حصّة الصور لا من حصّة النصّ: ثمنها يقارب ثلاثمئة رسالة،
    // فخصمها رسالةً واحدة يجعل حصّة النصّ بابَ إنفاقٍ لا سقفاً له.
    if (wantImage) {
      const iq = await takeQuota(admin, user.id, user.email || "", "img", st);
      if (!iq.ok) return refund({ error: "quota_exceeded_img", used: iq.used, limit: iq.limit }, 429);
      imgOn = true;
    }

    // مع صورة نحتاج نموذج رؤية مضموناً: النموذج النصي يُسقط الصور بصمت
    // فتظن المعلمة أنه قرأها وهو يجيب من فراغ.
    const model = wantImage
      ? imageModel
      : images.length
      ? ensureVision(st.model_chat_vision || st.vision_model || "google/gemini-2.5-flash", "google/gemini-2.5-flash")
      : (st.model_chat || st.chat_model || st.ai_model || "google/gemini-2.5-flash-lite");

    // المساعد عامٌّ لا متخصّصٌ تربويّ. كان تعريفه يحصره في التعليم ويأمره
    // أن «يعود إليه كلما أمكن»، فيَجُرّ الأسئلة العامة إلى الصفّ ويحشر
    // المدرسة في جوابٍ لا يخصّها — فتنصرف المعلّمة إلى مساعدٍ عامٍّ آخر.
    // معرفته بصفوفها ميزةٌ إضافية تُستدعى عند الحاجة، لا هُويّةٌ تحكم كل ردّ.
    // توجيهُ الرسم: يُبنى حول طلب المعلّمة لا يستبدله. والهوية العُمانية
    // مذكورةٌ صراحةً لأن نماذج الصور تميل إلى خليجيّاتٍ أخرى حين تُترك،
    // فتخرج الطالبة بزيٍّ ليس زيّ مدرستها.
    const imagePrompt = [
      userMsg || "ارسم صورةً تعليمية جميلة تصلح للعرض في صفٍّ ابتدائي.",
      images.length ? "الصور المرفقة مرجعٌ للرسم — احتفظ بأسلوبها وموضوعها." : "",
      "الصورة للعرض أمام طالباتٍ في الصفوف الأولى: واضحة، بألوانٍ مبهجة، بلا تفاصيل مزدحمة.",
      "إن كتبت أي نصٍّ داخل الصورة فليكن بعربيةٍ فصيحةٍ سليمة الحروف والاتصال، قليلاً وكبيراً مقروءاً من آخر الصف.",
      "إن رسمت أشخاصاً أو مبانيَ أو بيئة فالهوية العُمانية حصراً (الزي المدرسي العُماني، الكمّة والدشداشة) — لا غترة ولا عقال ولا هوية خليجية أخرى.",
    ].filter(Boolean).join("\n");

    const system = [
      "أنت «خُطّة AI» — مساعدٌ ذكيٌّ عامّ داخل منصة «خطتي الفصلية». تخدم مستخدمك في أي شيء يسأل عنه، تماماً كأي مساعدٍ ذكيٍّ عامّ.",
      "شخصيتك: ودود، عملي، مختصر، صادق — تجيب كزميلٍ واسع الاطلاع لا كموسوعة.",
      "مجالك مفتوح: معلومات عامة، علوم، تقنية، صحة عامة، كتابة وصياغة وتلخيص، ترجمة، حساب، برمجة، سفر، طبخ، تنظيم وقت، مشورة عملية، وأي شأنٍ يوميّ — كلها أسئلةٌ مشروعة تُجيب عنها مباشرة.",
      "مستخدمك معلّم، فإن كان السؤال تعليمياً فأنت ضليعٌ فيه أيضاً (تحضير الدروس، استراتيجيات التدريس، إدارة الصف، التقويم، أولياء الأمور، منهج كامبردج المطبق في عُمان، صياغة الأسئلة والأنشطة).",
      "لكن لا تفترض أن كل سؤال عن التدريس. أجب عن السؤال كما هو، ولا تُقحم المدرسة أو الصفّ أو الطلاب في جوابٍ لم يُذكروا فيه.",
      "ما تعتذر عنه فقط: ما يضر أو يخالف نظام سلطنة عُمان، أو ما يخصّ طفلاً بعينه بحكم طبي أو نفسي — عندها انصح بإحالته للمختص.",
      "لا تدّعِ اطلاعاً على أخبار أو أسعار أو أحداث بعد وقت تدريبك، ولا تخترع مصدراً أو رابطاً. إن لم تعرف فقل ذلك بجملة واحدة.",
      "لا تُدرج مراجع ولا روابط ولا قائمة مصادر في ردّك، ولا حتى حين تكون معلومتك من بحث الويب — أعطِ الجواب نفسه فقط. ولا تُذيّل ردّك بأرقام استشهاد. أمّا إن طلب المستخدم صراحةً المصدر أو الرابط أو المرجع، فأعطِه حينها.",
      "أجب بلغة السؤال (العربية الفصحى الميسّرة افتراضاً). اجعل الإجابة بقدر ما يحتاجه السؤال: سطران لسؤالٍ بسيط، وتفصيلٌ منظّم لسؤالٍ يستحقه.",
      context ? `معلوماتٌ عن مستخدمك — لا تستعملها إلا إن كان السؤال تعليمياً أو متّصلاً بعمله، ولا تعِدها حرفياً: ${context}` : "",
    ].filter(Boolean).join("\n");

    const orResp = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Assistant Chat",
      },
      body: JSON.stringify({
        model,
        // نموذج الصور لا يأخذ نظاماً ولا تاريخاً: النظام يصفه مساعداً نصّياً
        // فيخرج بنصٍّ بدل الصورة، والتاريخ يشوّش الموضوع بدروسٍ سابقة. تُرسل
        // الصور المرفقة إن وُجدت — فطلب «عدّلي هذه» يحتاج الأصل بين يديه.
        messages: wantImage
          ? [{ role: "user", content: images.length
                ? [{ type: "text", text: imagePrompt }, ...images.map((u) => ({ type: "image_url", image_url: { url: u } }))]
                : imagePrompt }]
          : [
          { role: "system", content: system },
          ...history,
          { role: "user", content: images.length
            ? [{ type: "text", text: userMsg || "اقرأ هذه الصورة ولخّصها لي." },
               ...images.map((u) => ({ type: "image_url", image_url: { url: u } }))]
            : userMsg },
        ],
        ...(wantImage ? { modalities: ["image", "text"], image_config: { aspect_ratio: "16:9", image_size: "1K" } } : {}),
        temperature: 0.6,
        max_tokens: images.length ? 1400 : 900,
        // OpenRouter يوزّع الطلب على عدة مزوّدين للنموذج نفسه، وترتيبه
        // الافتراضي يوازن السعر بالسرعة. المحادثة تُقاس بسرعة أوّل حرف،
        // فنطلب صراحةً أعلى إنتاجية.
        provider: { sort: "throughput" },
        // ثلاث نتائج لا خمس: السعر بالنتيجة ($4 لكل ألف)، والثلاث تكفي
        // للتحقّق من خبرٍ أو رقمٍ وتوفّر أربعين بالمئة من ثمن البحث
        ...(webOn ? { plugins: [{ id: "web", max_results: 3 }] } : {}),
      }),
    }, { st, task: "chat" });
    const or = await orResp.json();
    if (!orResp.ok) {
      const _m = String(or?.error?.message || or?.message || "");
      console.error(`openrouter ${orResp.status} في generate-chat: ${_m}`);
      return refund({ error: orErrCode(orResp.status, _m), detail: _m.slice(0, 200) }, 502);
    }
    const _msg = or?.choices?.[0]?.message || {};
    // نماذج الصور تعيدها في images[].image_url.url، وبعضها يضعها في content
    // كـdata URI. نقبل الصيغتين حتى لا يتوقّف الأمر على مزوّدٍ بعينه.
    const genImage: string = wantImage
      ? (_msg?.images?.[0]?.image_url?.url
         || (typeof _msg?.content === "string" && /^data:image\//.test(_msg.content) ? _msg.content : "")
         || "")
      : "";
    const reply = typeof _msg?.content === "string" && !/^data:image\//.test(_msg.content) ? _msg.content : "";

    // طلبت صورةً فلم تأتِ: لا نُسلّمها نصّاً اعتذارياً وقد خُصمت حصّتها —
    // نستردّ ونصرّح بالفشل لتعيد المحاولة.
    if (wantImage && !genImage) return refund({ error: "no_image" }, 502);
    if (!wantImage && !reply) return refund({ error: "no_reply" }, 502);

    // ═ حفظ المحادثة (بإنشاء الجدول ذاتياً عند الحاجة) ═
    // سقف حجم المحادثة المحفوظة — لا تنمو بلا حد
    const askedText = userMsg || (wantImage ? "(طلب رسم صورة)" : "(صورة مرفقة)");
    // نحفظ نص السؤال لا الصور: تخزين data URI يضخّم الصف ويُعاد إرساله كل دور.
    // والصورة المولَّدة كذلك: يُحفظ أثرها نصّاً، فالمعلّمة تنزّلها إن أرادتها
    // باقيةً، وحفظُ عشرات الصور في صفٍّ واحد يُبطئ فتح المحادثة على الجوال.
    const savedReply = wantImage ? "🖼️ (صورة مولَّدة)" : reply;
    const newMessages = [...history, { role: "user", content: askedText + (images.length ? ` [${images.length} صورة]` : "") }, { role: "assistant", content: savedReply }].slice(-60);
    const title = (history.find((m) => m.role === "user")?.content || askedText).slice(0, 60);
    let savedId = chatId;
    const doSave = async () => {
      if (chatId) {
        const { error } = await admin.from("ai_chats")
          .update({ messages: newMessages, updated_at: new Date().toISOString() })
          .eq("id", chatId).eq("user_id", user.id);
        if (error) throw error;
      } else {
        const { data, error } = await admin.from("ai_chats")
          .insert({ user_id: user.id, title, messages: newMessages })
          .select("id").single();
        if (error) throw error;
        savedId = data.id;
      }
    };
    try { await doSave(); }
    catch (e) {
      const msg = String((e as { message?: string })?.message || e);
      if (/does not exist|42P01|schema cache/i.test(msg)) {
        try { await ensureChatTable(); await doSave(); }
        catch (e2) { console.error("chat save bootstrap failed", e2); }
      } else console.error("chat save failed", msg);
    }

    // webUsed يُخبر الواجهة إن جرى البحث فعلاً: من نفدت حصتها تُجاب بلا بحث
    // وينبغي أن ترى ذلك، لا أن تظنّ جوابها مبنيّاً على مصدرٍ حديث
    return json({ reply, image: genImage || null, chatId: savedId, model, webUsed: webOn, usage: or?.usage || null });
  } catch (e) {
    // لا استرداد هنا: قد يقع الخطأ قبل تعريف refund أصلاً (وقبل خصم الحصّة)
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
