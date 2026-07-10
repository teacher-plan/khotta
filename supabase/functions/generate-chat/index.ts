// v2026.07.10 ════════════════════════════════════════════════════════════════
// Edge Function: generate-chat
// «فهيم» — مساعد المعلم الذكي: محادثة تربوية بسياق المعلم الحقيقي
// (صفوفه وموادّه ودرس اليوم). يحفظ المحادثة في ai_chats (وينشئ الجدول
// ذاتياً إن لم تُطبَّق الهجرة) ويعيد الرد.
//
// النشر: تلقائي عبر GitHub Actions
// الأسرار: OPENROUTER_API_KEY
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

    const b = await req.json().catch(() => ({}));
    const chatId = typeof b.chatId === "string" && b.chatId ? b.chatId : null;
    const userMsg = String(b.message || "").trim().slice(0, 2000);
    const context = String(b.context || "").slice(0, 1500);
    // آخر رسائل المحادثة من العميل (نقتصر على ١٢ لضبط التكلفة)
    const history: Array<{ role: string; content: string }> =
      (Array.isArray(b.history) ? b.history : [])
        .filter((m: { role?: string; content?: string }) => (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
        .slice(-12)
        .map((m: { role: string; content: string }) => ({ role: m.role, content: String(m.content).slice(0, 2000) }));
    if (!userMsg) return json({ error: "no_message" }, 400);

    const model = st.chat_model || st.ai_model || "google/gemini-2.5-flash";

    const system = [
      "أنت «فهيم» 🦉 — المساعد التربوي الذكي لمنصة «خطتي الفصلية» للمعلمين في سلطنة عُمان.",
      "شخصيتك: ودود، عملي، مختصر، مشجّع — تجيب كزميل خبير لا كموسوعة.",
      "تخصصك حصراً: التعليم والتدريس (تحضير الدروس، استراتيجيات التدريس، إدارة الصف، التقويم، التعامل مع الطلاب وأولياء الأمور، منهج كامبردج المطبق في عمان، صياغة الأسئلة والأنشطة).",
      "أي طلب خارج التعليم (برمجة، سياسة، ترفيه عام، واجبات شخصية...) اعتذر عنه بلطف وبجملة واحدة وأعد التوجيه لما تستطيعه.",
      "أجب بالعربية الفصحى الميسّرة. اجعل الإجابات قصيرة عملية (٣-٦ أسطر غالباً) إلا إن طُلب التفصيل.",
      context ? `سياق المعلم الحالي (استخدمه لتخصيص إجاباتك دون أن تعيده حرفياً): ${context}` : "",
    ].filter(Boolean).join("\n");

    const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Assistant Chat",
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: system },
          ...history,
          { role: "user", content: userMsg },
        ],
        temperature: 0.6,
        max_tokens: 900,
      }),
    });
    const or = await orResp.json();
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);
    const reply = or?.choices?.[0]?.message?.content || "";
    if (!reply) return json({ error: "no_reply" }, 502);

    // ═ حفظ المحادثة (بإنشاء الجدول ذاتياً عند الحاجة) ═
    const newMessages = [...history, { role: "user", content: userMsg }, { role: "assistant", content: reply }];
    const title = (history.find((m) => m.role === "user")?.content || userMsg).slice(0, 60);
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

    return json({ reply, chatId: savedId, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
