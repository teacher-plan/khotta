// v2026.11.18 ════════════════════════════════════════════════════════════════
// Edge Function: c1-school-timing — قراءة توقيت المدرسة من ملف (صورة/PDF/Word/Excel)
//
// يرفعه حساب إدارة المدرسة وحده (c1_schools.admin_email)، فيُرجع أوقات الطابور والحصص
// والفسحة لتراجعها الإدارة ثم تحفظها (c1_school_set_timing). لا يحفظ شيئاً بنفسه:
// قراءةُ وقتٍ خطأً تعني إشعاراً في غير وقته لكل معلّمي المدرسة، فالمراجعة إلزامية.
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
function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { ...cors, "Content-Type": "application/json" } });
}
// deno-lint-ignore no-explicit-any
type Any = any;
const MAX_FILES = 3;
const MAX_BYTES = 8 * 1024 * 1024;

// «٧:٢٠» أو «7.20» أو «1:00» (ظهراً) ← «HH:MM» بنظام ٢٤ ساعة
function hm(v: Any): string | null {
  const s = String(v ?? "").replace(/[٠-٩]/g, (c) => String("٠١٢٣٤٥٦٧٨٩".indexOf(c))).trim();
  const m = s.match(/(\d{1,2})\s*[:.٫]\s*(\d{2})/);
  if (!m) return null;
  let h = +m[1];
  const mi = +m[2];
  if (h < 6) h += 12;            // دوام المدرسة نهاراً: «١:٠٠» تعني الواحدة ظهراً
  if (h > 23 || mi > 59) return null;
  return String(h).padStart(2, "0") + ":" + String(mi).padStart(2, "0");
}
const mins = (t: string) => +t.slice(0, 2) * 60 + +t.slice(3);

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const jwt = (req.headers.get("Authorization") || "").replace("Bearer ", "");
    const { data: { user }, error: uErr } = await admin.auth.getUser(jwt);
    if (uErr || !user) return json({ error: "unauthorized" }, 401);
    const { data: school } = await admin.from("c1_schools").select("id").eq("admin_email", String(user.email || "").toLowerCase()).maybeSingle();
    if (!school) return json({ error: "forbidden" }, 403);

    const apiKey = Deno.env.get("OPENROUTER_API_KEY");
    if (!apiKey) return json({ error: "server_not_configured" }, 500);
    const { data: rows } = await admin.from("ai_settings").select("key,value");
    const st: Record<string, string> = {};
    (rows || []).forEach((r: { key: string; value: string }) => { st[r.key] = r.value; });
    const model = pickVisionModel(st, "roster", "google/gemini-2.5-flash");

    const b: Any = await req.json().catch(() => ({}));
    const files: Any[] = Array.isArray(b.files) ? b.files.slice(0, MAX_FILES) : [];
    if (!files.length) return json({ error: "no_files" }, 400);
    const content: unknown[] = [{ type: "text", text: "اقرأ توقيت الدوام المدرسي من هذا الملف." }];
    for (const f of files) {
      const txt = String(f?.text || "").slice(0, 20000).trim();
      if (txt) { content.push({ type: "text", text: `محتوى الملف «${String(f?.name || "").slice(0, 80)}»:\n${txt}` }); continue; }
      const url = String(f?.data || "");
      if (!url.startsWith("data:")) continue;
      if (url.length > MAX_BYTES * 1.4) return json({ error: "file_too_large" }, 413);
      if (url.startsWith("data:application/pdf")) content.push({ type: "file", file: { filename: String(f?.name || "timing.pdf"), file_data: url } });
      else if (url.startsWith("data:image/")) content.push({ type: "image_url", image_url: { url } });
    }
    if (content.length < 2) return json({ error: "unsupported_type" }, 400);

    const system = [
      "أنت مساعد يقرأ جدول توقيت الدوام في مدرسة عُمانية (أوقات بدء الحصص وانتهائها) من صورة أو PDF أو نصٍّ مستخرج.",
      "أعد JSON فقط بهذا الشكل: {\"assembly\":[\"07:00\",\"07:20\"] أو null,\"periods\":[[\"07:20\",\"08:00\"],...],\"breaks\":[{\"after\":3,\"from\":\"09:20\",\"to\":\"09:40\"}],\"note\":\"\"}",
      "periods: الحصص الدراسية وحدها بترتيبها (الأولى أولاً)، كل حصةٍ [بداية، نهاية]. لا تضع الطابور ولا الفسحة ولا الصلاة ضمن الحصص.",
      "breaks: كل فسحة أو استراحة أو صلاة بين الحصص، و after رقم الحصة التي تسبقها (١ = بعد الحصة الأولى).",
      "الأوقات بنظام ٢٤ ساعة HH:MM بأرقام لاتينية. أوقات بعد الظهر المكتوبة مثل 1:00 تعني 13:00.",
      "إن كان في الملف أكثر من توقيت (مثل توقيت الخميس أو رمضان أو الشتاء) فأعد التوقيت المعتاد لأيام الأسبوع، واذكر الاختلاف باختصار في note بالعربية.",
      "لا تخترع وقتاً غير مكتوب. إن لم تجد توقيت دوام في الملف فأعد periods فارغة واذكر السبب في note.",
    ].join("\n");

    const orResp = await orFetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: { "Authorization": "Bearer " + apiKey, "Content-Type": "application/json", "HTTP-Referer": "https://khotati.com", "X-Title": "Khotta School Timing" },
      body: JSON.stringify({ model, messages: [{ role: "system", content: system }, { role: "user", content }], response_format: { type: "json_object" }, temperature: 0, max_tokens: 3000 }),
    }, { st, task: "roster" });
    const or = await orResp.json();
    if (!orResp.ok) {
      console.error("c1-school-timing openrouter", orResp.status, String(or?.error?.message || "").slice(0, 200));
      return json({ error: orResp.status === 429 ? "busy" : "provider_error" }, 502);
    }
    await logAiCost(admin, user.id, "c1-school-timing", "img", model, or?.usage);
    const p = parseAiJson<Any>(or?.choices?.[0]?.message?.content || "");
    if (!p.ok) return json({ error: "bad_ai_output" }, 502);
    const v = p.value || {};

    // تنظيفٌ وتحقّق: أزواجٌ صحيحة، البداية قبل النهاية، والحصص متصاعدة
    const periods: string[][] = [];
    for (const x of Array.isArray(v.periods) ? v.periods : []) {
      const a = hm(Array.isArray(x) ? x[0] : x?.from), z = hm(Array.isArray(x) ? x[1] : x?.to);
      if (!a || !z || mins(z) <= mins(a)) continue;
      if (periods.length && mins(a) < mins(periods[periods.length - 1][0])) continue;
      periods.push([a, z]);
    }
    const asm = Array.isArray(v.assembly) ? [hm(v.assembly[0]), hm(v.assembly[1])] : null;
    const breaks = (Array.isArray(v.breaks) ? v.breaks : [])
      .map((x: Any) => ({ after: Math.max(1, Math.min(periods.length, Math.round(+x?.after || 0))), from: hm(x?.from), to: hm(x?.to) }))
      .filter((x: Any) => x.from && x.to && x.after >= 1);
    const br = breaks[0];
    const timing = periods.length ? {
      assembly: asm && asm[0] && asm[1] ? asm : null,
      periods,
      breakAfter: br ? br.after : Math.min(3, periods.length),
      breakTime: br ? [br.from, br.to] : null,
      breaks,
    } : null;
    return json({ timing, note: String(v.note || "").slice(0, 300) });
  } catch (e) {
    console.error("c1-school-timing", String(e));
    return json({ error: "server_error" }, 500);
  }
});
