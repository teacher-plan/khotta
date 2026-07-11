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

const MAX_BYTES = 150 * 1024 * 1024; // سقف 150MB — أعلى من ذلك يتجاوز ذاكرة الدالة نفسها
const ADMIN_EMAIL = "teacherplane2026project@gmail.com";

// حماية من SSRF: نجلب https فقط ومن مضيفات عامة (لا عناوين داخلية/خاصة)
function isForbiddenHost(host: string) {
  const h = host.toLowerCase();
  if (h === "localhost" || h.endsWith(".local") || h.endsWith(".internal")) return true;
  if (/^\d+\.\d+\.\d+\.\d+$/.test(h)) {
    const p = h.split(".").map(Number);
    if (p[0] === 10 || p[0] === 127 || p[0] === 0) return true;
    if (p[0] === 172 && p[1] >= 16 && p[1] <= 31) return true;
    if (p[0] === 192 && p[1] === 168) return true;
    if (p[0] === 169 && p[1] === 254) return true; // metadata
  }
  return false;
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
    // استيراد الكتب من روابط خارجية صلاحية مشرف فقط
    if ((user.email || "").toLowerCase() !== ADMIN_EMAIL) return json({ error: "forbidden" }, 403);

    const b = await req.json().catch(() => ({}));
    const url = String(b.url || "").trim();
    let parsed: URL;
    try { parsed = new URL(url); } catch (_) { return json({ error: "bad_url" }, 400); }
    if (parsed.protocol !== "https:") return json({ error: "bad_url" }, 400);
    if (isForbiddenHost(parsed.hostname)) return json({ error: "bad_url" }, 400);

    // تنظيف الملفات المؤقتة القديمة (أقدم من ٢٤ ساعة) — لا تتراكم بعد اليوم
    try {
      const { data: cached } = await admin.storage.from("library-files").list("book-cache", { limit: 100 });
      const dayAgo = Date.now() - 24 * 3600 * 1000;
      const stale = (cached || []).filter((f) => parseInt(f.name.split("_")[0]) < dayAgo).map((f) => "book-cache/" + f.name);
      if (stale.length) await admin.storage.from("library-files").remove(stale);
    } catch (_) { /* التنظيف اجتهادي */ }

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
