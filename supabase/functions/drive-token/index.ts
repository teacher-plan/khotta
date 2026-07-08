// ════════════════════════════════════════════════════════════════
// Edge Function: drive-token
// تُجدّد توكن وصول Google Drive للمعلم المُصادَق عليه باستخدام
// refresh_token المخزّن في جدول drive_tokens — يبقى client_secret
// الخاص بجوجل سرياً على الخادم ولا يصل أبداً لكود المتصفح.
//
// النشر:  supabase functions deploy drive-token
// الأسرار المطلوبة (من لوحة Supabase → Edge Functions → Secrets):
//   GOOGLE_CLIENT_ID      = معرّف عميل OAuth (نفس المستخدم في موفّر Google)
//   GOOGLE_CLIENT_SECRET  = السر المقابل له (من Google Cloud Console)
//   (SUPABASE_URL و SUPABASE_SERVICE_ROLE_KEY متوفّران تلقائياً)
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

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  try {
    const authHeader = req.headers.get("Authorization");
    if (!authHeader) return json({ error: "unauthorized" }, 401);

    const admin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    // تحديد هوية المستخدم من توكن الجلسة
    const jwt = authHeader.replace("Bearer ", "");
    const { data: { user }, error: userErr } = await admin.auth.getUser(jwt);
    if (userErr || !user) return json({ error: "unauthorized" }, 401);

    // جلب refresh_token الخاص بهذا المستخدم
    const { data: row } = await admin
      .from("drive_tokens")
      .select("refresh_token")
      .eq("user_id", user.id)
      .maybeSingle();

    if (!row?.refresh_token) { console.error("drive-token: not_linked for", user.id); return json({ error: "not_linked" }, 404); }
    if (!Deno.env.get("GOOGLE_CLIENT_ID") || !Deno.env.get("GOOGLE_CLIENT_SECRET")) {
      console.error("drive-token: GOOGLE_CLIENT_ID/SECRET secrets are missing!");
      return json({ error: "server_not_configured" }, 500);
    }

    // تبادل refresh_token بتوكن وصول جديد من جوجل
    const resp = await fetch("https://oauth2.googleapis.com/token", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        client_id: Deno.env.get("GOOGLE_CLIENT_ID")!,
        client_secret: Deno.env.get("GOOGLE_CLIENT_SECRET")!,
        refresh_token: row.refresh_token,
        grant_type: "refresh_token",
      }),
    });

    const g = await resp.json();
    if (!resp.ok || !g.access_token) {
      // refresh_token قد يكون أُبطل (المستخدم ألغى الإذن) — يحتاج إعادة ربط
      console.error("drive-token: refresh_failed", JSON.stringify(g).slice(0, 300));
      return json({ error: "refresh_failed", detail: g }, 400);
    }

    return json({ access_token: g.access_token, expires_in: g.expires_in });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
