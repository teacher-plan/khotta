// Edge Function: storage-usage — استهلاك التخزين على Supabase وCloudflare R2
// للصفحة الرئيسية في لوحة الإدارة، وتحرير مساحة Supabase من النسخ المكرّرة.
//
// • get: آخر لقطة (عمرها أقل من ساعة) أو قياسٌ جديد. القياس = حجم القاعدة
//   وملفات كل باكِت من storage.objects (admin_storage_usage)، ومجموع ملفات R2
//   بعدّها فعلاً (ListObjectsV2)، وكم من صفحات الكتب وأدلّة المعلّم على Supabase
//   لها نسخةٌ مطابقة الحجم على R2 (يمكن حذفها من Supabase بلا أي أثر).
// • free_copies: للمشرف بضغطةٍ منه فقط — يحذف من Supabase صفحات books/ و
//   teacher-guides/ التي ثبت أن لها نسخة مطابقة الحجم على R2، دفعةً دفعة.
//   القراءة كلها تمرّ أصلاً بـR2 أولاً (cycle1 وmanager والذكاء الاصطناعي).
//
// الأسرار: نفس أسرار r2-files (R2_ACCOUNT_ID، R2_ACCESS_KEY_ID، R2_SECRET_ACCESS_KEY، R2_BUCKET).
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { AwsClient } from "https://esm.sh/aws4fetch@1.0.20";
import { authorizeOps } from "../_shared/adminGuard.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
function json(b: unknown, s = 200) {
  return new Response(JSON.stringify(b), { status: s, headers: { ...cors, "Content-Type": "application/json" } });
}

// حدود الخطط المجانية — بالغيغابايت العشري (١٠٠٠^٣) لا الثنائي، فنُحسب أقرب إلى الحدّ لا أبعد.
const GB = 1_000_000_000;
export const LIMITS = {
  supabase_storage: 1 * GB, // Supabase Free: 1 GB ملفات
  supabase_db: 0.5 * GB, //    Supabase Free: 500 MB قاعدة بيانات
  r2_storage: 10 * GB, //      Cloudflare R2 Free: 10 GB-month
};
const MAX_AGE_MS = 60 * 60 * 1000;
const COPY_PREFIXES = ["books/", "teacher-guides/"]; // مسارات نُسخت إلى R2 تحت library-files/

const ACC = Deno.env.get("R2_ACCOUNT_ID") || "";
const KEY = Deno.env.get("R2_ACCESS_KEY_ID") || "";
const SEC = Deno.env.get("R2_SECRET_ACCESS_KEY") || "";
const BUCKET = Deno.env.get("R2_BUCKET") || "";
const r2On = !!(ACC && KEY && SEC && BUCKET);

function xmlText(s: string) {
  return s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, "&");
}

// يعدّ كائنات R2 (كلّها أو تحت بادئة) صفحةً بعد صفحة، ويمرّر كل كائن إلى cb
async function r2List(prefix: string, cb: (key: string, size: number) => void) {
  const r2 = new AwsClient({ accessKeyId: KEY, secretAccessKey: SEC, service: "s3", region: "auto" });
  let token = "";
  for (let page = 0; page < 2000; page++) {
    const u = new URL(`https://${ACC}.r2.cloudflarestorage.com/${BUCKET}`);
    u.searchParams.set("list-type", "2");
    u.searchParams.set("max-keys", "1000");
    if (prefix) u.searchParams.set("prefix", prefix);
    if (token) u.searchParams.set("continuation-token", token);
    const r = await r2.fetch(u.toString());
    if (!r.ok) throw new Error("r2_list_" + r.status);
    const xml = await r.text();
    for (const m of xml.matchAll(/<Contents>([\s\S]*?)<\/Contents>/g)) {
      const k = /<Key>([\s\S]*?)<\/Key>/.exec(m[1]);
      const s = /<Size>(\d+)<\/Size>/.exec(m[1]);
      if (k) cb(xmlText(k[1]), s ? Number(s[1]) : 0);
    }
    const t = /<NextContinuationToken>([\s\S]*?)<\/NextContinuationToken>/.exec(xml);
    if (!/<IsTruncated>true<\/IsTruncated>/.test(xml) || !t) return;
    token = xmlText(t[1]);
  }
}

// deno-lint-ignore no-explicit-any
async function sbList(admin: any, prefix: string, cb: (name: string, bytes: number) => boolean | void) {
  let after = "";
  for (;;) {
    const { data, error } = await admin.rpc("admin_storage_list", { p_bucket: "library-files", p_prefix: prefix, p_after: after, p_limit: 5000 });
    if (error) throw new Error("sb_list: " + error.message);
    const rows = (data || []) as { name: string; bytes: number }[];
    for (const r of rows) if (cb(r.name, Number(r.bytes) || 0) === false) return;
    if (rows.length < 5000) return;
    after = rows[rows.length - 1].name;
  }
}

// صفحات Supabase التي لها على R2 نسخةٌ بالحجم نفسه
// deno-lint-ignore no-explicit-any
async function findCopies(admin: any, r2Pages: Map<string, number> | null, max = Infinity) {
  const pages = r2Pages || new Map<string, number>();
  if (!r2Pages) for (const p of COPY_PREFIXES) await r2List("library-files/" + p, (k, s) => pages.set(k, s));
  const names: { name: string; bytes: number }[] = [];
  let bytes = 0, count = 0;
  for (const p of COPY_PREFIXES) {
    await sbList(admin, p, (name, b) => {
      if (b > 0 && pages.get("library-files/" + name) === b) {
        count++; bytes += b;
        if (names.length < max) names.push({ name, bytes: b });
      }
    });
  }
  return { count, bytes, names };
}

// deno-lint-ignore no-explicit-any
async function measure(admin: any) {
  const { data: sb, error } = await admin.rpc("admin_storage_usage");
  if (error) throw new Error("usage: " + error.message);
  const buckets = (sb?.buckets || []) as { bucket: string; objects: number; bytes: number }[];
  const storageBytes = buckets.reduce((t, b) => t + Number(b.bytes || 0), 0);

  // deno-lint-ignore no-explicit-any
  const r2: any = { configured: r2On, limit_bytes: LIMITS.r2_storage };
  let copies = null;
  if (r2On) {
    const folders = new Map<string, { objects: number; bytes: number }>();
    const pages = new Map<string, number>();
    let total = 0, objects = 0;
    try {
      await r2List("", (k, s) => {
        total += s; objects++;
        const parts = k.split("/");
        const f = parts[0] === "library-files" && parts.length > 2 ? parts[0] + "/" + parts[1] : parts[0];
        const cur = folders.get(f) || { objects: 0, bytes: 0 };
        cur.objects++; cur.bytes += s; folders.set(f, cur);
        if (COPY_PREFIXES.some((p) => k.startsWith("library-files/" + p))) pages.set(k, s);
      });
      r2.bytes = total; r2.objects = objects;
      r2.folders = [...folders.entries()].map(([folder, v]) => ({ folder, ...v })).sort((a, b) => b.bytes - a.bytes).slice(0, 12);
      const c = await findCopies(admin, pages, 0);
      copies = { objects: c.count, bytes: c.bytes };
    } catch (e) {
      r2.error = String((e as Error).message || e);
    }
  }
  return {
    measured_at: new Date().toISOString(),
    supabase: {
      storage_bytes: storageBytes, storage_limit_bytes: LIMITS.supabase_storage,
      db_bytes: Number(sb?.db_bytes || 0), db_limit_bytes: LIMITS.supabase_db,
      buckets, folders: sb?.folders || [],
    },
    r2,
    copies, // صفحاتٌ على Supabase لها نسخة على R2 — يمكن تحريرها
  };
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  const auth = await authorizeOps(req);
  if (!auth.ok) return json({ error: "unauthorized" }, 401);
  const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const b = await req.json().catch(() => ({}));

  try {
    if (!b.action || b.action === "get") {
      if (!b.force) {
        const { data: last } = await admin.from("storage_usage_snapshots").select("taken_at,data").order("taken_at", { ascending: false }).limit(1).maybeSingle();
        if (last && Date.now() - new Date(last.taken_at).getTime() < MAX_AGE_MS) return json({ ...last.data, cached: true });
      }
      const data = await measure(admin);
      await admin.from("storage_usage_snapshots").insert({ data });
      await admin.from("storage_usage_snapshots").delete().lt("taken_at", new Date(Date.now() - 30 * 864e5).toISOString());
      return json({ ...data, cached: false });
    }

    if (b.action === "free_copies") {
      // ضغطةٌ واعية من المشرف نفسه — لا من وكيلٍ مجدول
      if (auth.isService) return json({ error: "admin_only" }, 403);
      if (!r2On) return json({ error: "r2_not_configured" }, 503);
      const batch = Math.min(Math.max(Number(b.batch) || 1500, 100), 3000);
      const c = await findCopies(admin, null, batch);
      let deleted = 0, freed = 0;
      const sizeOf = new Map(c.names.map((x) => [x.name, x.bytes] as [string, number]));
      for (let i = 0; i < c.names.length; i += 100) {
        const chunk = c.names.slice(i, i + 100).map((x) => x.name);
        const { data, error } = await admin.storage.from("library-files").remove(chunk);
        if (error) return json({ error: "remove_failed", detail: error.message, deleted, freed_bytes: freed }, 502);
        for (const o of data || []) { deleted++; freed += sizeOf.get(o.name) || 0; }
      }
      await admin.from("storage_usage_snapshots").delete().gte("id", 0); // القياس القديم لم يعد صحيحاً
      return json({ deleted, freed_bytes: freed, remaining: Math.max(0, c.count - deleted) });
    }

    return json({ error: "bad_action" }, 400);
  } catch (e) {
    console.error("storage-usage:", e);
    return json({ error: "server_error", detail: String((e as Error).message || e) }, 500);
  }
});
