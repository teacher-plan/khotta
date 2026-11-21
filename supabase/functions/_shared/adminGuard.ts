// حارسُ الوكلاء الإدارية — دوالٌ تعمل بمفتاح الخدمة، فمسلكٌ مفتوح فيها يعني
// أن أي أحدٍ على الإنترنت يقرأ بيانات كل المعلّمات ويُغرق تلجرام ويستهلك
// الموارد. كانت credit-monitor وfile-processor-monitor وdaily-summary
// وsystem-health-check بلا تحقّقٍ إطلاقاً.
//
// المنطق منقولٌ حرفياً من registration-notifier — النمط الوحيد المُثبَت في
// المشروع — لا نظامٌ جديد: لا نطابق نصّ المفتاح لأن للمشروع صيغتين لصلاحية
// الخدمة نفسها (JWT قديم و«sb_secret_…» جديد)، فنتحقّق من الصلاحية لا الحروف.

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// التحقّق بالتوقيع لا بالقراءة: كان الحارس يفكّ حمولة الرمز ويقبل أيّ رمزٍ
// مكتوبٍ فيه role=service_role دون التحقّق من توقيعه — فالحماية كانت كلّها
// على بوّابة Supabase (verify_jwt). الآن: مطابقةٌ حرفية لمفتاح البيئة، وإلا
// يُعرض الرمز على PostgREST نفسه (الذي يتحقّق من التوقيع) مرّةً واحدة،
// ويُحفظ الحكم في ذاكرة الدالّة فلا يتكرّر النداء.
const _svcVerdict = new Map<string, boolean>();
function _claimsRole(auth: string): string {
  try {
    const [, payload] = auth.split(".");
    if (!payload) return "";
    const c = JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")));
    return c && typeof c === "object" ? String(c.role || "") : "";
  } catch { return ""; }
}
export async function isServiceRoleRequest(req: Request): Promise<boolean> {
  const svc = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
  const auth = (req.headers.get("Authorization") || "").replace("Bearer ", "").trim();
  if (!auth) return false;
  if (svc && auth === svc) return true;
  const looksService = auth.startsWith("sb_secret_") || _claimsRole(auth) === "service_role";
  if (!looksService) return false;
  if (_svcVerdict.has(auth)) return _svcVerdict.get(auth)!;
  let ok = false;
  try {
    const url = Deno.env.get("SUPABASE_URL")!;
    // جدولٌ لا يقرؤه إلا مفتاح الخدمة: رمزٌ مزوَّر أو مفتاح anon لا يمرّ
    const r = await fetch(`${url}/rest/v1/agent_registry?select=id&limit=1`, {
      headers: { apikey: auth, Authorization: "Bearer " + auth },
    });
    ok = r.ok;
    try { await r.text(); } catch { /* تجاهُل */ }
  } catch { ok = false; }
  if (_svcVerdict.size > 50) _svcVerdict.clear();
  _svcVerdict.set(auth, ok);
  return ok;
}

// ردٌّ موحَّد: لا يُفصح إن كان المفتاح خاطئاً أم ناقصاً.
export function unauthorized(cors: Record<string, string>): Response {
  return new Response(JSON.stringify({ error: "unauthorized" }), {
    status: 401,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

// ═══ KHOTTA Autonomous Management — Phase 2 ═══
// حارسٌ مزدوج لدوالّ Ops: تناديها إمّا الوكلاء المجدولة (مفتاح الخدمة،
// كنمط system-health-check القائم) أو المشرف من لوحة الإدارة (رمز جلسته
// المصادَق، محقَّقاً بـis_app_admin() على الخادم — لا يُكتفى بإخفاء الزرّ
// في الواجهة). لا مسلك ثالث: غير هذين تُرفَض الدالّة كاملةً.
//
// ⚠️ يبني عميلاً بمفتاح anon فقط للتحقّق من الهوية (نفس نمط
// openrouter-balance) — لا يُستعمَل مفتاح الخدمة إطلاقاً لتمرير طلب
// المستخدم، ولا يُعاد أي سرٍّ في الرد.
// deno-lint-ignore no-explicit-any
export interface OpsAuth { ok: boolean; isService: boolean; userId?: string; email?: string }

export async function authorizeOps(req: Request): Promise<OpsAuth> {
  if (await isServiceRoleRequest(req)) return { ok: true, isService: true };
  const authHeader = req.headers.get("Authorization");
  if (!authHeader) return { ok: false, isService: false };
  try {
    const userClient = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
      { global: { headers: { Authorization: authHeader } } },
    );
    const { data: { user } } = await userClient.auth.getUser();
    if (!user) return { ok: false, isService: false };
    const { data: isAdmin } = await userClient.rpc("is_app_admin");
    if (!isAdmin) return { ok: false, isService: false, userId: user.id, email: user.email || undefined };
    return { ok: true, isService: false, userId: user.id, email: user.email || undefined };
  } catch {
    return { ok: false, isService: false };
  }
}
