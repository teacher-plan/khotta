// v2026.11.14 ════════════════════════════════════════════════════════════════
// Edge Function: c1-push — إشعارات الهاتف (Web Push) لمنصّة الحلقة الأولى
//
// من المتصفح (جلسة المعلّم): key · subscribe · unsubscribe · prefs · test
// من القاعدة (مفتاح الخدمة، عبر c1_push_call):
//   • notif   — رسالة إدارة أو استبيان أُدرج في c1_notifications ← إشعار فوري لصاحبه
//   • morning — ٦:٣٠ص: حصص اليوم ودروسها من جدول المعلّم وخطته
//   • evening — ٧:٣٠م: دروس الغد التي لم يُنشأ لها تحضير بعد (لا يُرسل شيئاً إن كانت كلها جاهزة)
// السرّان: VAPID_PUBLIC_KEY (base64url) وVAPID_PRIVATE_JWK (JWK) — يضعهما تشغيل set-vapid-keys.
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
import { sendPush, type PushSub, type Vapid } from "../_shared/webpush.ts";
import { isServiceRoleRequest } from "../_shared/adminGuard.ts";

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

const APP_URL = "https://khotati.com/cycle1.html";
const DAYS = ["sun", "mon", "tue", "wed", "thu"];
const AR = (v: number | string) => String(v).replace(/\d/g, (c) => "٠١٢٣٤٥٦٧٨٩"[+c]);
const DEF_PREFS = { msgs: true, morning: true, evening: true };

function vapid(): Vapid | null {
  const pub = Deno.env.get("VAPID_PUBLIC_KEY") || "";
  const priv = Deno.env.get("VAPID_PRIVATE_JWK") || "";
  if (!pub || !priv) return null;
  try { return { publicKey: pub, privateJwk: JSON.parse(priv), subject: "mailto:teacherplane2026project@gmail.com" }; } catch { return null; }
}

// تاريخ مسقط (UTC+4) بعد إزاحة أيام: [YYYY-MM-DD، رقم اليوم 0=الأحد]
function mct(addDays = 0): [string, number] {
  const d = new Date(Date.now() + 4 * 3600e3 + addDays * 864e5);
  return [d.toISOString().slice(0, 10), d.getUTCDay()];
}

// حصص يومٍ من جدول المعلّم مع الدرس التالي لكل شعبةٍ ومادّة
function dayLessons(data: Any, dayIdx: number) {
  const dayId = DAYS[dayIdx];
  if (!dayId) return [];
  const row = ((data.timetable || {}).schedule || {})[dayId] || {};
  const classes: Record<string, Any> = {};
  (data.grades || []).forEach((g: Any) => (g.classes || []).forEach((c: Any) => { classes[c.id] = { ...c, grade: g.num }; }));
  const state = data.plan_state || {};
  const out: Any[] = [];
  for (const p of Object.keys(row).map(Number).sort((a, b) => a - b)) {
    const v = row[p];
    if (!v || !v.c) continue;
    const cls = classes[v.c];
    if (!cls) continue;
    const subj = v.s || (cls.subjects || [])[0] || "";
    const units = ((data.plan_units || {})[`${cls.grade}|${subj}`]) || [];
    let next: Any = null;
    for (const u of units) {
      for (const l of (u.lessons || [])) {
        const st = state[l.id] || {};
        if (!st.done && !(st.classes || {})[v.c]) { next = { ...l, prep: !!st.prep }; break; }
      }
      if (next) break;
    }
    out.push({ p, cls: cls.name, subj, lesson: next });
  }
  return out;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });
  try {
    const admin = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
    const token = (req.headers.get("Authorization") || "").replace("Bearer ", "");
    const b: Any = await req.json().catch(() => ({}));
    const v = vapid();

    // إرسالٌ لكل أجهزة مستخدم، مع حذف الاشتراكات المنتهية
    const pushUser = async (userId: string, pref: string | null, data: Any, topic?: string) => {
      const { data: subs } = await admin.from("c1_push_subs").select("endpoint,sub,prefs").eq("user_id", userId);
      let sent = 0;
      for (const s of subs || []) {
        const pr = { ...DEF_PREFS, ...(s.prefs || {}) };
        if (pref && !(pr as Any)[pref]) continue;
        try {
          const r = await sendPush(s.sub as PushSub, data, v!, { topic, urgency: pref === "msgs" ? "high" : "normal" });
          if (r.ok) { sent++; await admin.from("c1_push_subs").update({ last_ok: new Date().toISOString() }).eq("endpoint", s.endpoint); }
          else if (r.gone) await admin.from("c1_push_subs").delete().eq("endpoint", s.endpoint);
          else console.warn("push", r.status, r.text);
        } catch (e) { console.warn("push err", String(e)); }
      }
      return sent;
    };

    // ══ نداءات القاعدة (مفتاح الخدمة) ══
    // للمشروع صيغتان لمفتاح الخدمة (JWT قديم و«sb_secret_…»)، فالتحقّق بالصلاحية لا بالحروف (adminGuard)
    if (isServiceRoleRequest(req)) {
      if (!v) return json({ error: "vapid_missing" }, 500);
      const mode = String(b.mode || "");

      if (mode === "notif") {
        const { data: n } = await admin.from("c1_notifications").select("*").eq("id", String(b.id || "")).maybeSingle();
        if (!n || !n.user_id) return json({ ok: true, skipped: true });
        const title = n.kind === "survey" ? "📋 استبيان جديد من الإدارة" : "📩 رسالة من الإدارة";
        const body = String(n.message || "").replace(/^(رسالة (خاصة )?جديدة من الإدارة|استبيان جديد):\s*/, "").slice(0, 180);
        const sent = await pushUser(n.user_id, "msgs", { title, body, url: APP_URL + "#msgs", tag: "c1-msg-" + n.id }, "msg");
        return json({ ok: true, sent });
      }

      if (mode === "morning" || mode === "evening") {
        const [, dow] = mct(mode === "morning" ? 0 : 1);
        if (dow > 4) return json({ ok: true, skipped: "weekend" });
        const { data: subs } = await admin.from("c1_push_subs").select("user_id,prefs");
        const users = [...new Set((subs || []).filter((s: Any) => ({ ...DEF_PREFS, ...(s.prefs || {}) } as Any)[mode]).map((s: Any) => s.user_id))];
        let sent = 0;
        for (const uid of users) {
          const { data: prof } = await admin.from("cycle1_profiles").select("data").eq("id", uid).maybeSingle();
          const data = (prof && prof.data) || {};
          const ls = dayLessons(data, dow);
          if (!ls.length) continue;
          if (mode === "morning") {
            const lines = ls.map((x) => `الحصة ${AR(x.p + 1)}: ${x.cls} · ${x.subj}${x.lesson ? " — " + x.lesson.name : ""}`);
            const body = lines.slice(0, 4).join("\n") + (lines.length > 4 ? `\nو${AR(lines.length - 4)} حصص أخرى` : "");
            sent += await pushUser(uid, "morning", { title: `☀️ صباح الخير — حصصك اليوم (${AR(ls.length)})`, body, url: APP_URL + "#yawmi", tag: "c1-morning" }, "morning");
          } else {
            const seen = new Set<string>();
            const miss = ls.filter((x) => x.lesson && !x.lesson.prep && !seen.has(x.lesson.id) && seen.add(x.lesson.id));
            if (!miss.length) continue;
            const body = miss.slice(0, 4).map((x) => `${x.lesson.name} (${x.cls} · ${x.subj})`).join("\n") + (miss.length > 4 ? `\nو${AR(miss.length - 4)} دروس أخرى` : "");
            sent += await pushUser(uid, "evening", { title: `📝 دروس الغد بلا تحضير (${AR(miss.length)})`, body, url: APP_URL + "#plan", tag: "c1-evening" }, "evening");
          }
        }
        return json({ ok: true, users: users.length, sent });
      }
      return json({ error: "bad_mode" }, 400);
    }

    // ══ نداءات المتصفح (جلسة المعلّم) ══
    if (!token) return json({ error: "unauthorized" }, 401);
    const { data: { user }, error: uErr } = await admin.auth.getUser(token);
    if (uErr || !user) return json({ error: "unauthorized" }, 401);
    const action = String(b.action || "");

    if (action === "key") return json({ key: v ? v.publicKey : "" });

    if (action === "subscribe") {
      const s = b.subscription;
      if (!s || typeof s.endpoint !== "string" || !/^https:\/\//.test(s.endpoint) || !s.keys || !s.keys.p256dh || !s.keys.auth) return json({ error: "bad_sub" }, 400);
      const { data: prev } = await admin.from("c1_push_subs").select("prefs").eq("user_id", user.id).limit(1).maybeSingle();
      const row = { endpoint: s.endpoint, user_id: user.id, sub: { endpoint: s.endpoint, keys: { p256dh: String(s.keys.p256dh), auth: String(s.keys.auth) } },
        prefs: (prev && prev.prefs) || DEF_PREFS, ua: String(req.headers.get("user-agent") || "").slice(0, 200) };
      const { error } = await admin.from("c1_push_subs").upsert(row);
      if (error) throw error;
      return json({ ok: true, prefs: row.prefs });
    }

    if (action === "unsubscribe") {
      await admin.from("c1_push_subs").delete().eq("user_id", user.id).eq("endpoint", String(b.endpoint || ""));
      return json({ ok: true });
    }

    if (action === "prefs") {
      const { data: rows } = await admin.from("c1_push_subs").select("prefs").eq("user_id", user.id).limit(1);
      let prefs = { ...DEF_PREFS, ...((rows && rows[0] && rows[0].prefs) || {}) };
      if (b.prefs && typeof b.prefs === "object") {
        for (const k of Object.keys(DEF_PREFS)) if (typeof b.prefs[k] === "boolean") (prefs as Any)[k] = b.prefs[k];
        await admin.from("c1_push_subs").update({ prefs }).eq("user_id", user.id);
      }
      const { count } = await admin.from("c1_push_subs").select("endpoint", { count: "exact", head: true }).eq("user_id", user.id);
      return json({ prefs, devices: count || 0 });
    }

    if (action === "test") {
      if (!v) return json({ error: "vapid_missing", message: "الإشعارات غير مهيّأة على الخادم بعد." }, 500);
      const sent = await pushUser(user.id, null, { title: "🔔 خُطّة", body: "الإشعارات تعمل على هذا الجهاز ✅", url: APP_URL, tag: "c1-test" });
      return json({ ok: true, sent });
    }

    if (action === "preview") {
      // معاينة نصّ تذكيري اليوم والغد بلا إرسال (للإعدادات)
      const { data: prof } = await admin.from("cycle1_profiles").select("data").eq("id", user.id).maybeSingle();
      const data = (prof && prof.data) || {};
      return json({ today: dayLessons(data, mct(0)[1]), tomorrow: dayLessons(data, mct(1)[1]) });
    }

    return json({ error: "bad_action" }, 400);
  } catch (e) {
    console.error("c1-push", String((e as Error)?.message || e));
    return json({ error: "server" }, 500);
  }
});
