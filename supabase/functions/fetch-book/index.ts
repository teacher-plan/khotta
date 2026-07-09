// v2026.07.09 ════════════════════════════════════════════════════════════════
// Edge Function: fetch-book
// تجلب ملف كتاب (PDF) من رابط خارجي (موقع الوزارة مثلاً) على الخادم —
// لتجاوز قيود CORS في المتصفح — وترفعه لتخزين مؤقت وتعيد رابطاً داخلياً
// يستطيع المتصفح تحميله ومعالجته (تقطيع نصّي/رؤية).
//
// النشر:  supabase functions deploy fetch-book
// المخزن المطلوب: bucket عام باسم library-files (موجود أصلاً)
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

const MAX_BYTES = 300 * 1024 * 1024; // سقف 300MB

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

    const b = await req.json().catch(() => ({}));
    const url = String(b.url || "").trim();
    if (!/^https?:\/\/.+/i.test(url)) return json({ error: "bad_url" }, 400);

    // جلب الملف من المصدر الخارجي (الخادم لا تقيّده CORS)
    let resp: Response;
    try {
      resp = await fetch(url, { headers: { "User-Agent": "Mozilla/5.0 KhottaBookFetcher" } });
    } catch (e) {
      return json({ error: "fetch_failed", detail: String(e) }, 502);
    }
    if (!resp.ok) return json({ error: "source_error", status: resp.status }, 502);

    const ctype = (resp.headers.get("content-type") || "").toLowerCase();
    const buf = new Uint8Array(await resp.arrayBuffer());
    if (buf.byteLength > MAX_BYTES) return json({ error: "too_large", bytes: buf.byteLength }, 413);
    if (buf.byteLength < 500) return json({ error: "empty_or_blocked" }, 502);

    // تحقّق بسيط أنه PDF (التوقيع %PDF أو نوع المحتوى)
    const isPdf = ctype.includes("pdf") ||
      (buf[0] === 0x25 && buf[1] === 0x50 && buf[2] === 0x44 && buf[3] === 0x46);
    if (!isPdf) return json({ error: "not_pdf", ctype }, 415);

    const path = `book-cache/${Date.now()}_${Math.random().toString(36).slice(2, 9)}.pdf`;
    const { error: upErr } = await admin.storage.from("library-files").upload(path, buf, {
      cacheControl: "600",
      contentType: "application/pdf",
      upsert: false,
    });
    if (upErr) return json({ error: "upload_failed", detail: upErr.message }, 500);

    const { data: pub } = admin.storage.from("library-files").getPublicUrl(path);
    return json({ url: pub.publicUrl, bytes: buf.byteLength, path });
  } catch (e) {
    return json({ error: "server_error", detail: String(e) }, 500);
  }
});
