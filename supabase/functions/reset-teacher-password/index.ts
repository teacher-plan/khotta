// v2026.07.09 ════════════════════════════════════════════════════════════════
// Edge Function: reset-teacher-password
// تُولّد كلمة مرور جديدة لحساب معلم وتحدّثها في Supabase Auth
// مباشرة (auth.admin.updateUserById) + في عمود account_password.
// السماحية: فقط مستخدم مصادَق بنفس بريد المشرف (ADMIN_EMAIL).
// service_role key لا يصل أبداً لكود المتصفح — يبقى على الخادم فقط.
//
// النشر:  supabase functions deploy reset-teacher-password
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const ADMIN_EMAIL = "teacherplane2026project@gmail.com";

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

function genPassword() {
  const chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789";
  const bytes = new Uint32Array(8);
  crypto.getRandomValues(bytes);
  let p = "";
  for (let i = 0; i < 8; i++) p += chars[bytes[i] % chars.length];
  return p;
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
    if (userErr || !user || (user.email || "").toLowerCase() !== ADMIN_EMAIL.toLowerCase()) {
      return json({ error: "forbidden" }, 403);
    }

    const { regId, email } = await req.json();
    if (!regId || !email) return json({ error: "missing_params" }, 400);

    // إيجاد مستخدم Auth بالبريد المطلوب
    let targetId: string | null = null;
    for (let page = 1; page <= 20 && !targetId; page++) {
      const { data, error } = await admin.auth.admin.listUsers({ page, perPage: 200 });
      if (error) return json({ error: "lookup_failed", detail: error.message }, 500);
      const found = data.users.find((u) => (u.email || "").toLowerCase() === String(email).toLowerCase());
      if (found) { targetId = found.id; break; }
      if (data.users.length < 200) break;
    }
    if (!targetId) return json({ error: "user_not_found" }, 404);

    const newPassword = genPassword();
    const { error: updErr } = await admin.auth.admin.updateUserById(targetId, { password: newPassword });
    if (updErr) return json({ error: "update_failed", detail: updErr.message }, 500);

    const { error: dbErr } = await admin.from("pre_registrations").update({ account_password: newPassword }).eq("id", regId);
    if (dbErr) return json({ error: "db_update_failed", detail: dbErr.message }, 500);

    return json({ password: newPassword });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
