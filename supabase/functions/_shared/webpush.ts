// إرسال Web Push بلا مكتبات — WebCrypto فقط (يعمل في Deno وفي Node 22 للاختبار).
//   • التوقيع: VAPID (RFC 8292) — JWT بخوارزمية ES256.
//   • التشفير: aes128gcm (RFC 8291 + RFC 8188) بسجلٍّ واحد.
// المفتاح الخاص: JWK (P-256) في السرّ VAPID_PRIVATE_JWK، والعامّ base64url (65 بايت) في VAPID_PUBLIC_KEY.

const te = new TextEncoder();

export function b64u(buf: ArrayBuffer | Uint8Array): string {
  const u = buf instanceof Uint8Array ? buf : new Uint8Array(buf);
  let s = "";
  for (let i = 0; i < u.length; i++) s += String.fromCharCode(u[i]);
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
export function unb64u(s: string): Uint8Array {
  const b = s.replace(/-/g, "+").replace(/_/g, "/") + "===".slice((s.length + 3) % 4);
  return Uint8Array.from(atob(b), (c) => c.charCodeAt(0));
}
function concat(...parts: Uint8Array[]): Uint8Array {
  const out = new Uint8Array(parts.reduce((n, p) => n + p.length, 0));
  let o = 0;
  for (const p of parts) { out.set(p, o); o += p.length; }
  return out;
}
async function hmac(key: Uint8Array, data: Uint8Array): Promise<Uint8Array> {
  const k = await crypto.subtle.importKey("raw", key, { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return new Uint8Array(await crypto.subtle.sign("HMAC", k, data));
}

export type PushSub = { endpoint: string; keys: { p256dh: string; auth: string } };
export type Vapid = { publicKey: string; privateJwk: JsonWebKey; subject: string };

async function vapidAuth(endpoint: string, v: Vapid): Promise<string> {
  const aud = new URL(endpoint).origin;
  const head = b64u(te.encode(JSON.stringify({ typ: "JWT", alg: "ES256" })));
  const body = b64u(te.encode(JSON.stringify({ aud, exp: Math.floor(Date.now() / 1000) + 12 * 3600, sub: v.subject })));
  const key = await crypto.subtle.importKey("jwk", { ...v.privateJwk, key_ops: ["sign"], ext: true }, { name: "ECDSA", namedCurve: "P-256" }, false, ["sign"]);
  const sig = new Uint8Array(await crypto.subtle.sign({ name: "ECDSA", hash: "SHA-256" }, key, te.encode(head + "." + body)));
  return `vapid t=${head}.${body}.${b64u(sig)}, k=${v.publicKey}`;
}

// يُعيد جسم الطلب المشفّر (aes128gcm)
export async function encryptPayload(sub: PushSub, payload: Uint8Array, salt?: Uint8Array, asKeys?: CryptoKeyPair): Promise<Uint8Array> {
  const uaPublic = unb64u(sub.keys.p256dh);
  const authSecret = unb64u(sub.keys.auth);
  const as = asKeys || (await crypto.subtle.generateKey({ name: "ECDH", namedCurve: "P-256" }, true, ["deriveBits"]) as CryptoKeyPair);
  const asPublic = new Uint8Array(await crypto.subtle.exportKey("raw", as.publicKey));
  const uaKey = await crypto.subtle.importKey("raw", uaPublic, { name: "ECDH", namedCurve: "P-256" }, false, []);
  const ecdh = new Uint8Array(await crypto.subtle.deriveBits({ name: "ECDH", public: uaKey }, as.privateKey, 256));
  const prkKey = await hmac(authSecret, ecdh);
  const ikm = (await hmac(prkKey, concat(te.encode("WebPush: info\0"), uaPublic, asPublic, new Uint8Array([1])))).slice(0, 32);
  const s = salt || crypto.getRandomValues(new Uint8Array(16));
  const prk = await hmac(s, ikm);
  const cek = (await hmac(prk, concat(te.encode("Content-Encoding: aes128gcm\0"), new Uint8Array([1])))).slice(0, 16);
  const nonce = (await hmac(prk, concat(te.encode("Content-Encoding: nonce\0"), new Uint8Array([1])))).slice(0, 12);
  const aes = await crypto.subtle.importKey("raw", cek, "AES-GCM", false, ["encrypt"]);
  const ct = new Uint8Array(await crypto.subtle.encrypt({ name: "AES-GCM", iv: nonce }, aes, concat(payload, new Uint8Array([2]))));
  const rs = new Uint8Array([0, 0, 16, 0]); // 4096
  return concat(s, rs, new Uint8Array([asPublic.length]), asPublic, ct);
}

// يُرسل إشعاراً واحداً. gone=true يعني أن الاشتراك انتهى (404/410) فيُحذف.
export async function sendPush(sub: PushSub, data: unknown, v: Vapid, opts: { ttl?: number; urgency?: string; topic?: string } = {}) {
  const body = await encryptPayload(sub, te.encode(JSON.stringify(data)));
  const headers: Record<string, string> = {
    "Content-Encoding": "aes128gcm",
    "Content-Type": "application/octet-stream",
    TTL: String(opts.ttl ?? 6 * 3600),
    Urgency: opts.urgency || "normal",
    Authorization: await vapidAuth(sub.endpoint, v),
  };
  if (opts.topic) headers.Topic = opts.topic.replace(/[^A-Za-z0-9_-]/g, "").slice(0, 32);
  const r = await fetch(sub.endpoint, { method: "POST", headers, body });
  const text = r.ok ? "" : (await r.text().catch(() => "")).slice(0, 200);
  return { ok: r.ok, status: r.status, gone: r.status === 404 || r.status === 410, text };
}
