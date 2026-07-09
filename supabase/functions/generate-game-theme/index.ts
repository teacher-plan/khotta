// v2026.07.10 ════════════════════════════════════════════════════════════════
// Edge Function: generate-game-theme
// (للمشرف فقط) يولّد خلفية ثيم لقسم الألعاب بنموذج الصور (Nano Banana)
// ويرفعها لتخزين دائم — الثيم يولَّد مرة واحدة ويخدم كل المعلمين مجاناً.
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

const ADMIN_EMAIL = "teacherplane2026project@gmail.com";

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

    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });

    const b = await req.json().catch(() => ({}));
    const name = String(b.name || "").trim().slice(0, 60);
    const emoji = String(b.emoji || "🎨").slice(0, 4);
    const desc = String(b.desc || "").trim().slice(0, 500);
    const colors = (b.colors && typeof b.colors === "object") ? b.colors : null;
    if (!name || !desc) return json({ error: "missing_fields" }, 400);

    const model = st.slide_model || "google/gemini-2.5-flash-image";

    const prompt = [
      `خلفية ساحة لعبة تعليمية للأطفال (7-13 سنة) بثيم: ${desc}.`,
      "عريضة (16:9)، رسم كرتوني مسطح لطيف بألوان مبهجة متناسقة.",
      "بالغ الأهمية: المنطقة الوسطى من الصورة يجب أن تكون هادئة وخالية من التفاصيل والعناصر البارزة — ستوضع فوقها بطاقات لعب وأزرار، فاجعل التفاصيل الجميلة على الأطراف والحواف فقط.",
      "بدون أي نص أو كتابة أو حروف في الصورة إطلاقاً. بدون وجوه بشرية.",
      "إضاءة دافئة، عمق بسيط، جودة عالية.",
    ].join(" ");

    const call = (cfg: Record<string, unknown> | null) =>
      fetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + apiKey,
          "Content-Type": "application/json",
          "HTTP-Referer": "https://khotati.com",
          "X-Title": "Khotta Game Theme Generator",
        },
        body: JSON.stringify({
          model,
          messages: [{ role: "user", content: prompt }],
          modalities: ["image", "text"],
          ...(cfg ? { image_config: cfg } : {}),
        }),
      });

    let orResp = await call({ aspect_ratio: "16:9", image_size: "2K" });
    let or = await orResp.json();
    if (!orResp.ok) { orResp = await call({ aspect_ratio: "16:9" }); or = await orResp.json(); }
    if (!orResp.ok) { orResp = await call(null); or = await orResp.json(); }
    if (!orResp.ok) return json({ error: "provider_error", detail: or }, 502);
    const img = or?.choices?.[0]?.message?.images?.[0]?.image_url?.url || "";
    if (!img || !img.startsWith("data:image/")) return json({ error: "no_image" }, 502);

    // فك الترميز والرفع لتخزين دائم
    const b64 = img.split(",")[1];
    const bin = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0));
    const path = `game-themes/${Date.now()}_${Math.random().toString(36).slice(2, 8)}.png`;
    const { error: upErr } = await admin.storage.from("library-files").upload(path, bin, {
      cacheControl: "31536000",
      contentType: "image/png",
      upsert: false,
    });
    if (upErr) return json({ error: "upload_failed", detail: upErr.message }, 500);
    const { data: pub } = admin.storage.from("library-files").getPublicUrl(path);

    const { data: row, error: insErr } = await admin.from("game_themes").insert({
      name, emoji, bg_url: pub.publicUrl, colors, created_by: user.id,
    }).select().single();
    if (insErr) return json({ error: "db_error", detail: insErr.message }, 500);

    return json({ theme: row, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
