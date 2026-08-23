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

// سقف 200MB. الملفّ يُحمَّل كاملاً في ذاكرة الدالة قبل رفعه، فالسقف محكومٌ
// بذاكرتها لا برغبتنا — ورفعُه أكثر من هذا يُسقط الدالة بلا رسالةٍ مفهومة.
const MAX_BYTES = 200 * 1024 * 1024;
const ADMIN_EMAIL = "teacherplane2026project@gmail.com";

// حماية من SSRF: نجلب https فقط ومن مضيفات عامة (لا عناوين داخلية/خاصة)
function isForbiddenHost(host: string) {
  const h = host.toLowerCase();
  if (h === "localhost" || h.endsWith(".local") || h.endsWith(".internal")) return true;
  if (/^\d+\.\d+\.\d+\.\d+$/.test(h)) return isForbiddenIpv4(h);
  return false;
}

function isForbiddenIpv4(h: string) {
  const p = h.split(".").map(Number);
  if (p[0] === 10 || p[0] === 127 || p[0] === 0) return true;
  if (p[0] === 172 && p[1] >= 16 && p[1] <= 31) return true;
  if (p[0] === 192 && p[1] === 168) return true;
  if (p[0] === 169 && p[1] === 254) return true; // metadata
  return false;
}

// IPv6: يرفض ::1 (loopback)، fe80::/10 (link-local — يشمل عنوان التعريف
// السحابي عبر IPv6 على بعض المزودات)، fc00::/7 (unique local)، و
// ::ffff:a.b.c.d (عنوان IPv4 مُطعَّمٌ داخل IPv6 يُلتفّ به حول الفحص أعلاه).
function isForbiddenIpv6(h: string) {
  const s = h.toLowerCase().replace(/^\[|\]$/g, "");
  if (s === "::1" || s === "::") return true;
  if (s.startsWith("fe80:") || s.startsWith("fe8") || s.startsWith("fe9") || s.startsWith("fea") || s.startsWith("feb")) return true;
  if (/^f[cd][0-9a-f]{2}:/.test(s)) return true; // fc00::/7
  const v4 = s.match(/^::ffff:(\d+\.\d+\.\d+\.\d+)$/);
  if (v4) return isForbiddenIpv4(v4[1]);
  return false;
}

// يحلّ اسم المضيف إلى عناوينه الفعلية ويرفض إن كان أيٌّ منها داخلياً —
// يمنع DNS rebinding والالتفاف عبر اسمٍ ظاهره عام لكنه يُحلّ محلياً.
async function hasForbiddenResolvedIp(hostname: string): Promise<boolean> {
  if (/^\d+\.\d+\.\d+\.\d+$/.test(hostname)) return isForbiddenIpv4(hostname);
  if (hostname.includes(":")) return isForbiddenIpv6(hostname);
  try {
    const [v4, v6] = await Promise.all([
      Deno.resolveDns(hostname, "A").catch(() => [] as string[]),
      Deno.resolveDns(hostname, "AAAA").catch(() => [] as string[]),
    ]);
    if (v4.some(isForbiddenIpv4)) return true;
    if (v6.some(isForbiddenIpv6)) return true;
    if (v4.length === 0 && v6.length === 0) return true; // تعذّر الحلّ — نرفض احتياطاً
    return false;
  } catch (_e) {
    return true; // فشل التحقق يعني رفضاً (fail-closed)
  }
}

// يجلب الرابط دون اتّباع أي تحويلة تلقائياً، ويعيد التحقّق من كل تحويلة
// (المضيف والعنوان المُحلَّل) قبل تتبّعها — التحقّق من الرابط الأصلي فقط
// لا يمنع 302 نحو عنوانٍ داخلي.
async function safeFetch(startUrl: string, maxHops = 5): Promise<Response> {
  let current = startUrl;
  for (let hop = 0; hop < maxHops; hop++) {
    const u = new URL(current);
    if (u.protocol !== "https:") throw new Error("bad_url");
    if (isForbiddenHost(u.hostname)) throw new Error("bad_url");
    if (await hasForbiddenResolvedIp(u.hostname)) throw new Error("bad_url");
    const resp = await fetch(current, {
      headers: { "User-Agent": "Mozilla/5.0 KhottaBookFetcher" },
      redirect: "manual",
    });
    if (resp.status >= 300 && resp.status < 400) {
      const loc = resp.headers.get("location");
      if (!loc) return resp;
      current = new URL(loc, current).toString();
      continue;
    }
    return resp;
  }
  throw new Error("too_many_redirects");
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
    if (await hasForbiddenResolvedIp(parsed.hostname)) return json({ error: "bad_url" }, 400);

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
      resp = await safeFetch(url);
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
