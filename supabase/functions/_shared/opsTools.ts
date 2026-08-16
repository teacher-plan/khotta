// ═══ KHOTTA Autonomous Management — Phase 2: طبقة الأدوات (Tool Layer) ═══
//
// كل دالّةٍ هنا قراءةٌ صرفة، مُعامَلاتها ثابتة، لا SQL حرّ يبنيه استدعاءٌ
// خارجي ولا نموذج ذكاء اصطناعي. الوكيل (ops-analyze) وrefik (ops-copilot)
// لا يملكان إلا هذه الأدوات — لا وصولاً مباشراً للقاعدة بصلاحياتٍ حرّة.
//
// كل دالّةٍ تُعيد ملخّصاً مُجمَّعاً (aggregate) لا سجلّاتٍ خاماً كاملة —
// حماية للكلفة (سياق أصغر لنداء الذكاء الاصطناعي) وللخصوصية (لا نصوص
// أخطاءٍ كاملة تحمل بيانات مستخدمين تُغذَّى لنموذجٍ خارجي بلا داع).
//
// deno-lint-ignore-file no-explicit-any

export async function get_system_health(admin: any) {
  const since = new Date(Date.now() - 15 * 60 * 1000).toISOString();
  const { data } = await admin
    .from("health_checks")
    .select("component_name,status,response_time_ms,error_message,severity,checked_at")
    .gte("checked_at", since)
    .order("checked_at", { ascending: false })
    .limit(60);
  // آخر حالةٍ لكل مكوّن فقط — لا كل الفحوصات المتكرّرة كل ٥ دقائق.
  const latest = new Map<string, any>();
  for (const row of data || []) if (!latest.has(row.component_name)) latest.set(row.component_name, row);
  const components = [...latest.values()];
  const critical = components.filter((c) => c.status === "critical").length;
  const warning = components.filter((c) => c.status === "warning").length;
  return {
    overall: critical > 0 ? "critical" : warning > 0 ? "warning" : components.length ? "healthy" : "unknown",
    checked_components: components.length,
    critical,
    warning,
    components,
  };
}

export async function get_recent_errors(admin: any, hours = 1) {
  const since = new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();
  const { data } = await admin
    .from("error_logs")
    .select("error_type,function_name,error_code,occurred_at")
    .gte("occurred_at", since)
    .order("occurred_at", { ascending: false })
    .limit(200);
  const rows = data || [];
  const byFunction: Record<string, number> = {};
  for (const r of rows) { const k = r.function_name || "unknown"; byFunction[k] = (byFunction[k] || 0) + 1; }
  return { window_hours: hours, total: rows.length, by_function: byFunction, sample: rows.slice(0, 10) };
}

export async function get_emergency_alerts(admin: any) {
  const { data } = await admin
    .from("emergency_alerts")
    .select("alert_type,severity,title,affected_component,resolved,created_at")
    .eq("resolved", false)
    .order("created_at", { ascending: false })
    .limit(30);
  return { unresolved_count: (data || []).length, alerts: data || [] };
}

export async function get_ai_usage(admin: any) {
  const month = new Date().toISOString().slice(0, 7);
  const { data } = await admin.from("ai_usage").select("kind,count").eq("month", month);
  const byKind: Record<string, number> = {};
  for (const r of data || []) byKind[r.kind] = (byKind[r.kind] || 0) + (r.count || 0);
  return { month, requests_by_kind: byKind, total_requests: Object.values(byKind).reduce((a, b) => a + b, 0) };
}

// تكلفةُ الذكاء الاصطناعي — المصدر الوحيد ai_cost_log (Phase 0). يفرّق بين
// تكلفة المستخدمين (kind فيها text/img/search) وتكلفة العمليات نفسها
// (kind='ops' — نداءات ops-analyze وops-copilot) كي لا يختلط الحسابان.
export async function get_ai_cost(admin: any) {
  const now = new Date();
  const todayStart = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate())).toISOString();
  const weekStart = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString();
  const monthStart = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), 1)).toISOString();

  const { data: monthRows } = await admin
    .from("ai_cost_log")
    .select("cost_usd,kind,function_name,model,user_id,created_at")
    .gte("created_at", monthStart)
    .limit(5000);
  const rows = monthRows || [];

  const sum = (arr: any[]) => arr.reduce((s, r) => s + (typeof r.cost_usd === "number" ? r.cost_usd : 0), 0);
  const userRows = rows.filter((r) => r.kind !== "ops");
  const opsRows = rows.filter((r) => r.kind === "ops");

  const byFn: Record<string, number> = {};
  const byModel: Record<string, number> = {};
  const byUser: Record<string, number> = {};
  for (const r of userRows) {
    byFn[r.function_name] = (byFn[r.function_name] || 0) + (r.cost_usd || 0);
    if (r.model) byModel[r.model] = (byModel[r.model] || 0) + (r.cost_usd || 0);
    if (r.user_id) byUser[r.user_id] = (byUser[r.user_id] || 0) + (r.cost_usd || 0);
  }
  const topUsers = Object.entries(byUser).sort((a, b) => b[1] - a[1]).slice(0, 5)
    .map(([user_id, cost]) => ({ user_id, cost_usd: cost }));

  return {
    period: { today_from: todayStart, week_from: weekStart, month_from: monthStart },
    user_cost_usd: {
      today: sum(userRows.filter((r) => r.created_at >= todayStart)),
      week: sum(userRows.filter((r) => r.created_at >= weekStart)),
      month: sum(userRows),
    },
    ops_cost_usd: {
      today: sum(opsRows.filter((r) => r.created_at >= todayStart)),
      week: sum(opsRows.filter((r) => r.created_at >= weekStart)),
      month: sum(opsRows),
    },
    requests_month: userRows.length,
    avg_cost_usd: userRows.length ? sum(userRows) / userRows.length : 0,
    cost_by_function: byFn,
    cost_by_model: byModel,
    top_users: topUsers,
    known_limitation:
      "extract-lessons وgenerate-game-theme وsegment-book تستدعي الذكاء الاصطناعي لكنها لا تُسجَّل هنا بعد (خارج نطاق Phase 0) — التكلفة الفعلية الكلية أعلى مما يظهر.",
  };
}

export async function get_quota_status(admin: any) {
  const { data } = await admin.from("ai_settings").select("key,value")
    .in("key", ["quota_text", "quota_img", "quota_search"]);
  const limits: Record<string, string> = {};
  for (const r of data || []) limits[r.key] = r.value;
  return { monthly_limits: limits };
}

export async function get_database_health(admin: any) {
  const start = Date.now();
  const { error } = await admin.from("profiles").select("count", { count: "exact" });
  const responseMs = Date.now() - start;
  // rpc() يُعيد "thenable" لا Promise كاملاً (لا .catch() عليه مباشرةً —
  // هذا بالضبط ما كسر الأداة: TypeError عند تسلسل .catch()). النمط الصحيح
  // نفسه المستعمَل في system-health-check: await مباشرةً، ثم تجاهُل الخطأ
  // بأمان عبر optional chaining على data.
  const { data: sizeRows } = await admin.rpc("database_size");
  return {
    response_ms: responseMs,
    status: error ? "critical" : responseMs > 2000 ? "warning" : "healthy",
    error: error ? error.message : null,
    database_size_mb: sizeRows?.[0]?.database_size_mb ?? null,
  };
}

export async function get_edge_function_health(admin: any) {
  const since = new Date(Date.now() - 15 * 60 * 1000).toISOString();
  const { data } = await admin
    .from("health_checks")
    .select("component_name,status,response_time_ms,error_message,checked_at")
    .like("component_name", "function:%")
    .gte("checked_at", since)
    .order("checked_at", { ascending: false })
    .limit(30);
  const latest = new Map<string, any>();
  for (const row of data || []) if (!latest.has(row.component_name)) latest.set(row.component_name, row);
  return { functions: [...latest.values()] };
}

// لا أداة get_recent_deployments حقيقية بعد: لا رمز GitHub متاحٌ لدوالّ
// الحافة اليوم، وإضافته سرٌّ جديد خارج نطاق هذه المرحلة. نُبقيها محدودةً
// صراحةً بدل اختراع مصدرٍ لا وجود له.
export function get_recent_deployments() {
  return {
    available: false,
    reason: "لا تكامل مع GitHub Actions من دوالّ الحافة بعد — قيدٌ معروف، لم يُضَف سرٌّ جديد لتفاديه.",
  };
}

export async function get_recent_incidents(admin: any, limit = 10) {
  const { data } = await admin
    .from("ops_incidents")
    .select("id,severity,status,component,summary,confidence,occurrence_count,first_seen_at,last_seen_at,resolved_at")
    .order("detected_at", { ascending: false })
    .limit(limit);
  return { incidents: data || [] };
}
