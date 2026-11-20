// v2026.11.20 ════════════════════════════════════════════════════════════════
// Edge Function: c1-school-logo — شعار المدرسة للشهادات (حساب إدارة المدرسة وحده)
//
//   action:"locate"  {image:dataURL}  ← نموذج رؤيةٍ يُرجع «مكان» الشعار فقط (صندوقاً 0–1000).
//        لا يرسم ولا يعيد إخراج الشعار: القصّ يجري في المتصفّح من الصورة الأصلية نفسها،
//        فيبقى الشعار مطابقاً للأصل حرفاً حرفاً (نماذج الصور تعيد الرسم فتغيّر التفاصيل).
//   action:"save"    {png:dataURL}    ← يحفظ الشعار المقصوص ويعتمده لمدرسة المستدعي.
//   action:"remove"                   ← يزيل الشعار.
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { orFetch, pickVisionModel } from "../_shared/ai.ts";
import { logAiCost } from "../_shared/quota.ts";
import { parseAiJson } from "../_shared/aiJson.ts";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (b: unknown, s = 200) => new Response(JSON.stringify(b), { status: s, headers: { ...cors, "Content-Type": "application/json" } });
// deno-lint-ignore no-explicit-any
type Any = any;
const MAX_IN = 8 * 1024 * 1024, MAX_PNG = 2 * 1024 * 1024;

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const jwt = (req.headers.get("Authorization") || "").replace("Bearer ", "");
    const { data: { user }, error: uErr } = await admin.auth.getUser(jwt);
    if (uErr || !user) return json({ error: "unauthorized" }, 401);
    const { data: school } = await admin.from("c1_schools").select("id,name").eq("admin_email", String(user.email || "").toLowerCase()).maybeSingle();
    if (!school) return json({ error: "forbidden" }, 403);
    const b: Any = await req.json().catch(() => ({}));

    if (b.action === "remove") {
      await admin.from("c1_schools").update({ logo_url: null, logo_at: null }).eq("id", school.id);
      return json({ ok: true });
    }

    // موضع الشعار وحجمه في الشهادات
    const pos = ["left", "center", "right"].includes(b.pos) ? b.pos : null;
    const size = ["s", "m", "l"].includes(b.size) ? b.size : null;
    if (b.action === "style") {
      if (!pos && !size) return json({ error: "bad_style" }, 400);
      await admin.from("c1_schools").update({ ...(pos ? { logo_pos: pos } : {}), ...(size ? { logo_size: size } : {}) }).eq("id", school.id);
      return json({ ok: true });
    }

    if (b.action === "save") {
      const png = String(b.png || "");
      if (!png.startsWith("data:image/png;base64,")) return json({ error: "bad_image" }, 400);
      const bin = Uint8Array.from(atob(png.split(",")[1] || ""), (c) => c.charCodeAt(0));
      if (bin.length > MAX_PNG) return json({ error: "too_large" }, 413);
      const key = `school-logos/${school.id}-${Date.now()}.png`;
      const { error } = await admin.storage.from("library-files").upload(key, new Blob([bin], { type: "image/png" }), { upsert: true, contentType: "image/png", cacheControl: "31536000" });
      if (error) return json({ error: "upload_failed" }, 500);
      const url = admin.storage.from("library-files").getPublicUrl(key).data.publicUrl;
      await admin.from("c1_schools").update({ logo_url: url, logo_at: new Date().toISOString(), ...(pos ? { logo_pos: pos } : {}), ...(size ? { logo_size: size } : {}) }).eq("id", school.id);
      return json({ ok: true, logo_url: url });
    }

    if (b.action === "locate") {
      const img = String(b.image || "");
      if (!img.startsWith("data:image/")) return json({ error: "bad_image" }, 400);
      if (img.length > MAX_IN * 1.4) return json({ error: "file_too_large" }, 413);
      const apiKey = Deno.env.get("OPENROUTER_API_KEY");
      if (!apiKey) return json({ error: "server_not_configured" }, 500);
      const { data: rows } = await admin.from("ai_settings").select("key,value");
      const st: Record<string, string> = {};
      (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
      const model = pickVisionModel(st, "roster", "google/gemini-2.5-flash");
      const system = [
        `أنت أداة تحديد مواقع دقيقة. في الصورة شعار مدرسة «${school.name}» (قد تكون الصورة الشعار وحده، أو ورقة رسمية أو لافتة أو شاشة فيها الشعار مع نصوصٍ أخرى).`,
        "مهمّتك الوحيدة: تحديد المستطيل الذي يحيط بالشعار نفسه بإحكام — الرمز/الختم/الرسم، ومعه اسم المدرسة فقط إن كان جزءاً مرسوماً من الشعار ملتصقاً به.",
        "أوامر صارمة: لا تصف الشعار ولا تعدّله ولا ترسمه؛ لا تُدخل في المستطيل ترويسة الوزارة أو نصوص الورقة أو التوقيعات أو الأختام الأخرى إلا إن كانت هي الشعار؛ إن وُجد أكثر من شعار فاختر شعار المدرسة لا شعار الوزارة أو الدولة؛ اجعل الحواف ملاصقةً للشعار بهامشٍ صغير جداً.",
        "الإحداثيات مطبّعة من 0 إلى 1000 نسبةً لأبعاد الصورة: [ymin, xmin, ymax, xmax] (الأعلى ثم اليسار ثم الأسفل ثم اليمين).",
        'أعد JSON فقط: {"found":true,"box":[ymin,xmin,ymax,xmax],"bg":"light|dark|transparent|busy","note":"ملاحظة قصيرة بالعربية إن لزم"} — وإن لم تجد شعاراً: {"found":false,"note":"السبب"}',
      ].join("\n");
      const r = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
        method: "POST",
        headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta School Logo" },
        body: JSON.stringify({ model, temperature: 0, max_tokens: 300, response_format: { type: "json_object" },
          messages: [{ role: "system", content: system }, { role: "user", content: [{ type: "text", text: "حدّد مكان شعار المدرسة." }, { type: "image_url", image_url: { url: img } }] }] }),
      }, { st, task: "roster" });
      const j = await r.json().catch(() => ({}));
      if (!r.ok) return json({ error: "provider_error", detail: String(j?.error?.message || "").slice(0, 200) }, 502);
      await logAiCost(admin, user.id, "c1-school-logo", "text", model, j?.usage);
      const p = parseAiJson(String(j?.choices?.[0]?.message?.content || ""));
      const v: Any = p.ok ? p.value : null;
      if (!v || !v.found) return json({ found: false, note: String(v?.note || "").slice(0, 160) });
      const box = Array.isArray(v.box) ? v.box.slice(0, 4).map((n: unknown) => Math.max(0, Math.min(1000, Number(n) || 0))) : [];
      if (box.length !== 4 || box[2] - box[0] < 15 || box[3] - box[1] < 15) return json({ found: false, note: "تعذّر تحديد حدود الشعار" });
      return json({ found: true, box, bg: String(v.bg || "light").slice(0, 12), note: String(v.note || "").slice(0, 160) });
    }
    return json({ error: "bad_action" }, 400);
  } catch (e) {
    console.error("c1-school-logo", String(e));
    return json({ error: "server_error" }, 500);
  }
});
