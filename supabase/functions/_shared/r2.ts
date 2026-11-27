// Cloudflare R2 — التخزين الأساسي للملفات (صور، PDF، Word، صوت). Supabase يبقى للبيانات النصية والجداول.
// المفاتيح بالمسار نفسه الذي كان في Supabase: «library-files/…» و«user-files/…»،
// والرابط العام https://files.khotati.com/<المفتاح>. إن لم تُضبط الأسرار تعيد الدوال null
// فيرجع المستدعي إلى Supabase كما كان.
import { AwsClient } from "https://esm.sh/aws4fetch@1.0.20";

const ACC = Deno.env.get("R2_ACCOUNT_ID") || "";
const KEY = Deno.env.get("R2_ACCESS_KEY_ID") || "";
const SEC = Deno.env.get("R2_SECRET_ACCESS_KEY") || "";
const BUCKET = Deno.env.get("R2_BUCKET") || "";
export const R2_PUBLIC = (Deno.env.get("R2_PUBLIC_BASE") || "https://files.khotati.com").replace(/\/$/, "");
export const r2Ready = () => !!(ACC && KEY && SEC && BUCKET);

let client: AwsClient | null = null;
const cli = () => client ||= new AwsClient({ accessKeyId: KEY, secretAccessKey: SEC, service: "s3", region: "auto" });
const enc = (k: string) => k.split("/").map(encodeURIComponent).join("/");
const objUrl = (k: string) => `https://${ACC}.r2.cloudflarestorage.com/${BUCKET}/${enc(k)}`;
export const r2PublicUrl = (k: string) => `${R2_PUBLIC}/${enc(k)}`;

// يرفع ويعيد الرابط العام، أو null عند التعذّر
export async function r2Put(key: string, body: BodyInit, type: string, cache = "public, max-age=31536000"): Promise<string | null> {
  if (!r2Ready()) return null;
  try {
    const r = await cli().fetch(objUrl(key), { method: "PUT", body, headers: { "Content-Type": type, "Cache-Control": cache } });
    if (!r.ok) { console.error("r2Put", r.status, key); return null; }
    return r2PublicUrl(key);
  } catch (e) { console.error("r2Put", String(e)); return null; }
}

export async function r2Exists(key: string): Promise<boolean> {
  if (!r2Ready()) return false;
  try { return (await cli().fetch(objUrl(key), { method: "HEAD" })).ok; } catch { return false; }
}

export async function r2Delete(key: string): Promise<boolean> {
  if (!r2Ready()) return false;
  try { const r = await cli().fetch(objUrl(key), { method: "DELETE" }); return r.ok || r.status === 404; } catch { return false; }
}
