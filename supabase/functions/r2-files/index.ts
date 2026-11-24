// Edge Function: r2-files — رفع ملفات المعلّمين وحذفها على Cloudflare R2.
//
// المتصفّح لا يحمل مفاتيح R2 أبداً: يطلب من هذه الدالّة رابط رفعٍ موقَّعاً صالحاً
// خمس دقائق لمسارٍ داخل مجلّده هو (user-files/<معرّفه>/…)، بعد التحقّق من حصّته
// (can_upload_file). والحذف لا يتمّ إلا لملفٍّ مسجَّلٍ باسمه في user_files.
// إن لم تُضبط أسرار R2 تردّ «not_configured» فيرجع المتصفّح إلى Supabase كما كان.
//
// الأسرار: R2_ACCOUNT_ID، R2_ACCESS_KEY_ID، R2_SECRET_ACCESS_KEY، R2_BUCKET،
//          R2_PUBLIC_BASE (اختياري، الافتراضي https://files.khotati.com)
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { AwsClient } from "https://esm.sh/aws4fetch@1.0.20";
import { isServiceRoleRequest } from "../_shared/adminGuard.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(b: unknown, s = 200) {
  return new Response(JSON.stringify(b), { status: s, headers: { ...cors, "Content-Type": "application/json" } });
}

const ACC = Deno.env.get("R2_ACCOUNT_ID") || "";
const KEY = Deno.env.get("R2_ACCESS_KEY_ID") || "";
const SEC = Deno.env.get("R2_SECRET_ACCESS_KEY") || "";
const BUCKET = Deno.env.get("R2_BUCKET") || "";
const PUBLIC = (Deno.env.get("R2_PUBLIC_BASE") || "https://files.khotati.com").replace(/\/$/, "");
const MAX = 500 * 1024 * 1024;
export const R2_PREFIX = "r2:"; // يُميَّز به المسار في user_files عن ملفات Supabase القديمة

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  if (!ACC || !KEY || !SEC || !BUCKET) return json({ error: "not_configured" }, 503);

  // فحصٌ ذاتي للإدارة فقط (مفتاح الخدمة): رفعٌ ثم قراءةٌ عامة ثم حذف لملفٍّ تجريبي.
  if (isServiceRoleRequest(req) && new URL(req.url).searchParams.get("selftest") === "1") {
    const r2t = new AwsClient({ accessKeyId: KEY, secretAccessKey: SEC, service: "s3", region: "auto" });
    const key = `user-files/_selftest/${crypto.randomUUID()}.txt`;
    const url = `https://${ACC}.r2.cloudflarestorage.com/${BUCKET}/${key}`;
    const put = await r2t.fetch(url, { method: "PUT", body: "ok", headers: { "Content-Type": "text/plain" } });
    const pub = await fetch(`${PUBLIC}/${key}`).then((r) => r.status).catch(() => 0);
    const del = await r2t.fetch(url, { method: "DELETE" });
    return json({ put: put.status, public_get: pub, delete: del.status });
  }

  // نسخ ملفات Supabase إلى R2 (للإدارة بمفتاح الخدمة): يعيد روابط رفعٍ موقّعة لما ينقص R2 فقط
  // (أو حجمه مختلف)، فينزّل المشغّل الملف من Supabase ويرفعه مباشرةً — بلا ذاكرةٍ في الدالة.
  if (isServiceRoleRequest(req) && new URL(req.url).searchParams.get("mirror") === "1") {
    const r2m = new AwsClient({ accessKeyId: KEY, secretAccessKey: SEC, service: "s3", region: "auto" });
    const bm = await req.json().catch(() => ({}));
    const items: { key: string; size: number; type?: string }[] = Array.isArray(bm.items) ? bm.items.slice(0, 50) : [];
    const out = await Promise.all(items.map(async (it) => {
      const key = String(it.key || "");
      if (!/^(library-files|user-files)\//.test(key) || key.includes("..")) return { key, skip: "bad" };
      const url = `https://${ACC}.r2.cloudflarestorage.com/${BUCKET}/${key.split("/").map(encodeURIComponent).join("/")}`;
      const h = await r2m.fetch(url, { method: "HEAD" }).catch(() => null);
      if (h && h.ok && Number(h.headers.get("content-length")) === Number(it.size)) return { key, skip: "exists" };
      const u = new URL(url); u.searchParams.set("X-Amz-Expires", "3600");
      const type = String(it.type || "application/octet-stream").slice(0, 120);
      const sgn = await r2m.sign(new Request(u, { method: "PUT", headers: { "Content-Type": type } }), { aws: { signQuery: true } });
      return { key, putUrl: sgn.url, type };
    }));
    return json({ items: out });
  }

  const authHeader = req.headers.get("Authorization") || "";
  const userClient = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_ANON_KEY")!, {
    global: { headers: { Authorization: authHeader } },
  });
  const { data: { user } } = await userClient.auth.getUser();
  if (!user) return json({ error: "unauthorized" }, 401);

  const b = await req.json().catch(() => ({}));
  const r2 = new AwsClient({ accessKeyId: KEY, secretAccessKey: SEC, service: "s3", region: "auto" });
  const objUrl = (key: string) => `https://${ACC}.r2.cloudflarestorage.com/${BUCKET}/${key.split("/").map(encodeURIComponent).join("/")}`;

  if (b.action === "sign_upload") {
    const size = Number(b.size) || 0;
    if (size <= 0 || size > MAX) return json({ error: "bad_size" }, 400);
    // الحصّة تُفحص بجلسة المعلّم نفسه (الدالّة تقرأ auth.uid())
    const { data: allowed, error: qErr } = await userClient.rpc("can_upload_file", { add_bytes: size });
    if (qErr) return json({ error: "quota_check_failed" }, 503);
    if (!allowed) return json({ error: "quota_exceeded" }, 403);
    const ext = (String(b.fileName || "").match(/\.[A-Za-z0-9]{1,8}$/) || [""])[0].toLowerCase();
    const key = `user-files/${user.id}/${crypto.randomUUID()}${ext}`;
    const type = String(b.contentType || "application/octet-stream").slice(0, 120);
    const u = new URL(objUrl(key));
    u.searchParams.set("X-Amz-Expires", "300");
    const signed = await r2.sign(new Request(u, { method: "PUT", headers: { "Content-Type": type } }), {
      aws: { signQuery: true },
    });
    return json({ putUrl: signed.url, contentType: type, path: R2_PREFIX + key, publicUrl: `${PUBLIC}/${key}` });
  }

  // ملفات المكتبة الثقيلة من لوحة الإدارة (صفحات الكتب وأدلّة المعلّم وملفات
  // المكتبة PDF) تُرفع إلى R2 مباشرةً تحت library-files/ بالمسار نفسه الذي كانت
  // تأخذه في Supabase، فتقرؤها كل المسالك الحالية (R2 أولاً). للمشرف وحده.
  if (b.action === "sign_library" || b.action === "list_library") {
    const { data: isAdmin } = await userClient.rpc("is_app_admin");
    if (!isAdmin) return json({ error: "forbidden" }, 403);
    const path = String(b.path || b.prefix || "");
    if (!/^(books|teacher-guides|library-pdfs)\/[A-Za-z0-9._\-\/]*$/.test(path) || path.includes("..")) {
      return json({ error: "bad_path" }, 400);
    }
    const key = "library-files/" + path;
    if (b.action === "list_library") {
      const u = new URL(`https://${ACC}.r2.cloudflarestorage.com/${BUCKET}`);
      u.searchParams.set("list-type", "2");
      u.searchParams.set("prefix", key);
      u.searchParams.set("max-keys", "1000");
      const r = await r2.fetch(u.toString());
      if (!r.ok) return json({ error: "list_failed" }, 502);
      const xml = await r.text();
      const items = [...xml.matchAll(/<Key>([^<]*)<\/Key>[\s\S]*?<Size>(\d+)<\/Size>/g)]
        .map((m) => ({ name: m[1].slice(key.length).replace(/^\//, ""), size: Number(m[2]) }));
      return json({ items });
    }
    const size = Number(b.size) || 0;
    if (size <= 0 || size > MAX) return json({ error: "bad_size" }, 400);
    const type = String(b.contentType || "application/octet-stream").slice(0, 120);
    const u = new URL(objUrl(key));
    u.searchParams.set("X-Amz-Expires", "600");
    const signed = await r2.sign(new Request(u, { method: "PUT", headers: { "Content-Type": type } }), {
      aws: { signQuery: true },
    });
    return json({ putUrl: signed.url, contentType: type, publicUrl: `${PUBLIC}/${key}` });
  }

  if (b.action === "delete") {
    const path = String(b.path || "");
    if (!path.startsWith(R2_PREFIX + "user-files/" + user.id + "/")) return json({ error: "forbidden" }, 403);
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const { data: row } = await admin.from("user_files").select("path").eq("user_id", user.id).eq("path", path).maybeSingle();
    if (!row) return json({ error: "not_found" }, 404);
    const r = await r2.fetch(objUrl(path.slice(R2_PREFIX.length)), { method: "DELETE" });
    if (!r.ok && r.status !== 404) return json({ error: "delete_failed" }, 502);
    await admin.from("user_files").delete().eq("user_id", user.id).eq("path", path);
    return json({ ok: true });
  }

  return json({ error: "bad_action" }, 400);
});
