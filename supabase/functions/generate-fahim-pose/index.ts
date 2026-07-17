// v2026.07.17 ════════════════════════════════════════════════════════════════
// Edge Function: generate-fahim-pose
// يولّد وضعية جديدة لشخصية "فهيم" (ثعلب المنصة) بالاعتماد على صورة الشعار
// الأساسية assistant/mascot.png كمرجع بصري، مع الحفاظ الحرفي على تصميم
// الشخصية (الشكل، الألوان، الأسلوب) وتغيير الوضعية/التعبير فقط حسب الوصف.
// يُستدعى من لوحة المشرف (manager.html) حصراً.
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

    const quota = await takeQuota(admin, user.id, user.email || "", "img", st);
    if (!quota.ok) return json({ error: "quota_exceeded", used: quota.used, limit: quota.limit }, 429);

    const b = await req.json().catch(() => ({}));
    const poseDesc = String(b.poseDesc || "").slice(0, 500);
    if (!poseDesc) return json({ error: "no_pose_desc" }, 400);

    // نجلب صورة الشعار الأساسية من التخزين لنستخدمها كمرجع بصري ثابت
    const { data: pub } = admin.storage.from("library-files").getPublicUrl("assistant/mascot.png");
    const mascotUrl = pub?.publicUrl;
    if (!mascotUrl) return json({ error: "no_mascot" }, 500);
    const mascotResp = await fetch(mascotUrl + "?v=" + Date.now());
    if (!mascotResp.ok) return json({ error: "mascot_fetch_failed" }, 500);
    const mascotBuf = await mascotResp.arrayBuffer();
    const mascotB64 = "data:image/png;base64," + btoa(String.fromCharCode(...new Uint8Array(mascotBuf)));

    let model = st.slide_model || st.info_model || "google/gemini-2.5-flash-image";
    if (!model.startsWith("google/")) model = "google/gemini-3.1-flash-image-preview";

    const editInstr = [
      "هذه هي الشخصية الرسمية لمنصة تعليمية — ثعلب وديّ اسمه «فهيم» يظهر بجانب المعلمات.",
      `أعد رسم نفس الشخصية بالضبط — نفس الشكل، الألوان، الملابس إن وُجدت، والأسلوب الفني الكرتوني — لكن غيّر وضعيتها وتعبيرها فقط لتُظهر: «${poseDesc}».`,
      "حافظ حرفياً على هوية الشخصية البصرية (نفس الوجه ونفس تناسق الألوان) دون أي تغيير في التصميم الأساسي.",
      "اجعل الخلفية شفافة أو بيضاء ناصعة تماماً بلا أي عناصر أخرى، والشخصية وحدها في وسط الإطار، بنفس زاوية وحجم الصورة الأصلية تقريباً.",
      "لا نص ولا كتابة داخل الصورة إطلاقاً.",
    ].join("\n");

    const r = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + apiKey,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://khotati.com",
        "X-Title": "Khotta Fahim Pose Generator",
      },
      body: JSON.stringify({
        model,
        messages: [{ role: "user", content: [
          { type: "text", text: editInstr },
          { type: "image_url", image_url: { url: mascotB64 } },
        ] }],
        modalities: ["image", "text"],
      }),
    });
    const or = await r.json();
    if (!r.ok) return json({ error: "provider_error", detail: or }, 502);
    const msg = or?.choices?.[0]?.message;
    const outImg = msg?.images?.[0]?.image_url?.url || "";
    if (!outImg) return json({ error: "no_image", detail: msg?.content || null }, 502);
    return json({ image: outImg, model, usage: or?.usage || null });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
