// حارسُ الوكلاء الإدارية — دوالٌ تعمل بمفتاح الخدمة، فمسلكٌ مفتوح فيها يعني
// أن أي أحدٍ على الإنترنت يقرأ بيانات كل المعلّمات ويُغرق تلجرام ويستهلك
// الموارد. كانت credit-monitor وfile-processor-monitor وdaily-summary
// وsystem-health-check بلا تحقّقٍ إطلاقاً.
//
// المنطق منقولٌ حرفياً من registration-notifier — النمط الوحيد المُثبَت في
// المشروع — لا نظامٌ جديد: لا نطابق نصّ المفتاح لأن للمشروع صيغتين لصلاحية
// الخدمة نفسها (JWT قديم و«sb_secret_…» جديد)، فنتحقّق من الصلاحية لا الحروف.

export function isServiceRoleRequest(req: Request): boolean {
  const svc = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
  const auth = (req.headers.get("Authorization") || "").replace("Bearer ", "").trim();
  if (!auth) return false;
  if (svc && auth === svc) return true;
  try {
    const [, payload] = auth.split(".");
    if (!payload) return false;
    const claims = JSON.parse(atob(payload.replace(/-/g, "+").replace(/_/g, "/")));
    // التحقّق من أنه كائنٌ فعلاً: JSON.parse("null") و‎parse("5")‎ يمرّان
    // ثم يرمي الوصولُ إلى الخاصية — والرمي داخل حارسٍ يعني ٥٠٠ لا ٤٠١.
    return !!claims && typeof claims === "object" && claims.role === "service_role";
  } catch {
    return false;
  }
}

// ردٌّ موحَّد: لا يُفصح إن كان المفتاح خاطئاً أم ناقصاً.
export function unauthorized(cors: Record<string, string>): Response {
  return new Response(JSON.stringify({ error: "unauthorized" }), {
    status: 401,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}
