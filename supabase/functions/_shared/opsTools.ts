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
    .select("id,severity,status,component,summary,confidence,occurrence_count,first_seen_at,last_seen_at,resolved_at,source_agent,requires_human_attention")
    .order("detected_at", { ascending: false })
    .limit(limit);
  return { incidents: data || [] };
}

// ═══ Autonomous Operations 2.0 — Phase 1: أدوات الوكلاء/السعة (قراءة فقط) ═══

export async function get_agent_registry(admin: any) {
  const { data } = await admin
    .from("agent_registry")
    .select("agent_id,display_name,agent_type,status,schedule_cron,trigger_kind,autonomy_level,permission_level,notes")
    .order("agent_id");
  return { agents: data || [] };
}

// صحة الوكيل مُشتَقّة من بيانات حقيقية (agent_runs إن وُجدت تشغيلات، وإلا
// agent_logs القديمة) — لا حالة ثابتة/تجميلية أبداً.
export async function get_agent_runs_summary(admin: any, hours = 24) {
  const since = new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();
  const { data: runs } = await admin
    .from("agent_runs")
    .select("agent_id,status,started_at,completed_at,duration_ms,error")
    .gte("started_at", since)
    .order("started_at", { ascending: false })
    .limit(500);
  const rows = runs || [];
  const byAgent: Record<string, { total: number; success: number; failed: number; last_status: string; last_run_at: string; health: string }> = {};
  for (const r of rows) {
    const k = r.agent_id;
    if (!byAgent[k]) byAgent[k] = { total: 0, success: 0, failed: 0, last_status: r.status, last_run_at: r.started_at, health: "UNKNOWN" };
    byAgent[k].total++;
    if (r.status === "SUCCESS") byAgent[k].success++;
    if (r.status === "FAILED") byAgent[k].failed++;
  }
  for (const k of Object.keys(byAgent)) {
    const a = byAgent[k];
    // مُشتَقّةٌ من نسبة النجاح الفعلية في النافذة، لا رقمٌ ثابت.
    a.health = a.total === 0 ? "UNKNOWN"
      : a.last_status === "FAILED" && a.failed / a.total > 0.5 ? "FAILED"
      : a.last_status === "FAILED" ? "DEGRADED"
      : a.failed > 0 ? "WARNING"
      : "HEALTHY";
  }
  return {
    window_hours: hours,
    total_runs: rows.length,
    by_agent: byAgent,
    note: rows.length === 0 ? "لا تشغيلات مسجَّلة في agent_runs بعد ضمن هذه النافذة — الوكلاء القديمة (قبل Phase 1) لا تكتب هنا إلا بعد التحديث التدريجي." : undefined,
  };
}

// سعة قاعدة البيانات — يفرّق صراحةً عن Supabase Storage/تكلفة الذكاء
// الاصطناعي (أدواتٌ منفصلة). يتدهور بأمان إلى INSUFFICIENT_DATA/NOT
// AVAILABLE بدل اختلاق نمو/توقّع بلا تاريخٍ كافٍ.
export async function get_database_capacity(admin: any) {
  const { data: latest } = await admin
    .from("db_capacity_history")
    .select("measured_at,size_mb,limit_mb,usage_percent,top_tables")
    .order("measured_at", { ascending: false })
    .limit(1)
    .maybeSingle();

  if (!latest) {
    return {
      available: false,
      reason: "لا قياسات بعد — database-capacity-monitor لم يُشغَّل مرةً بعد أو لم يمرّ دورة كاملة.",
      database_size_mb: null, usage_percent: "NOT_AVAILABLE", top_tables: [], growth: "INSUFFICIENT_DATA",
    };
  }

  const { data: history } = await admin
    .from("db_capacity_history")
    .select("measured_at,size_mb")
    .order("measured_at", { ascending: false })
    .limit(30);
  const points = (history || []).slice().reverse();
  let growthNote = "INSUFFICIENT_DATA";
  let mbPerDay: number | null = null;
  if (points.length >= 4) {
    const first = points[0]; const last = points[points.length - 1];
    const hours = (new Date(last.measured_at).getTime() - new Date(first.measured_at).getTime()) / 3_600_000;
    if (hours >= 24) { mbPerDay = Math.round(((last.size_mb - first.size_mb) / hours) * 24 * 100) / 100; growthNote = "OK"; }
  }

  return {
    available: true,
    measured_at: latest.measured_at,
    database_size_mb: latest.size_mb,
    limit_mb: latest.limit_mb,
    usage_percent: latest.usage_percent ?? "NOT_AVAILABLE",
    top_tables: latest.top_tables || [],
    growth: growthNote === "OK" ? { status: "OK", mb_per_day: mbPerDay } : { status: "INSUFFICIENT_DATA" },
    resource_kind: "database_storage", // ليس Supabase Storage ولا تكلفة AI
  };
}

// ═══ Phase 1.5 — القسم 13: أداةٌ جديدة لتلخيص حالة كل وكيل صراحةً ═══
// تجيب مباشرةً على أسئلة الكوبايلوت الشائعة: "هل كل الوكلاء يعملون؟"،
// "أي وكيل فشل آخر مرة؟"، "هل هناك وكيل متوقف؟" — من agent_registry
// (الهوية/الحالة المُعلَنة) مدموجةً بـagent_runs (الصحة المُشتقّة الفعلية،
// نفس منطق get_agent_runs_summary أعلاه). قراءةٌ صرفة، لا كتابة.
export async function get_agent_status_summary(admin: any, hours = 24) {
  const { data: registry } = await admin
    .from("agent_registry")
    .select("agent_id,display_name,agent_type,status,schedule_cron,trigger_kind,autonomy_level")
    .order("agent_id");

  const since = new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();
  const { data: runs } = await admin
    .from("agent_runs")
    .select("agent_id,status,started_at,completed_at,duration_ms,error")
    .gte("started_at", since)
    .order("started_at", { ascending: false })
    .limit(1000);
  const rows = runs || [];

  const agents = (registry || []).map((a: any) => {
    const agentRuns = rows.filter((r: any) => r.agent_id === a.agent_id);
    const lastRun = agentRuns[0]; // الأحدث (مرتَّبةٌ تنازلياً أصلاً)
    const lastSuccess = agentRuns.find((r: any) => r.status === "SUCCESS");
    const lastFailed = agentRuns.find((r: any) => r.status === "FAILED");
    let consecutiveFailures = 0;
    for (const r of agentRuns) { if (r.status === "FAILED") consecutiveFailures++; else break; }
    const successCount = agentRuns.filter((r: any) => r.status === "SUCCESS").length;
    const successRate = agentRuns.length ? Math.round((successCount / agentRuns.length) * 1000) / 10 : null;
    const durations = agentRuns.filter((r: any) => typeof r.duration_ms === "number").map((r: any) => r.duration_ms);
    const avgDurationMs = durations.length ? Math.round(durations.reduce((s: number, d: number) => s + d, 0) / durations.length) : null;

    // صحةٌ محسوبةٌ من بياناتٍ حقيقية، لا قيمةٌ ثابتة/تجميلية (القسم 2).
    let health: string;
    if (a.status !== "ACTIVE") health = "DISABLED";
    else if (!agentRuns.length) health = "UNKNOWN"; // لا تشغيلاتٍ بعد ضمن النافذة
    else if (consecutiveFailures >= 3) health = "FAILED";
    else if (lastRun?.status === "FAILED") health = "DEGRADED";
    else if (consecutiveFailures > 0 || (successRate !== null && successRate < 90)) health = "WARNING";
    else health = "HEALTHY";

    return {
      agent_id: a.agent_id, display_name: a.display_name, agent_type: a.agent_type,
      registered_status: a.status, schedule_cron: a.schedule_cron, trigger_kind: a.trigger_kind,
      health,
      last_run_at: lastRun?.started_at ?? null,
      last_run_status: lastRun?.status ?? null,
      last_success_at: lastSuccess?.started_at ?? null,
      last_failed_at: lastFailed?.started_at ?? null,
      last_error: lastFailed?.error ?? null,
      consecutive_failures: consecutiveFailures,
      success_rate_percent: successRate,
      avg_duration_ms: avgDurationMs,
      runs_in_window: agentRuns.length,
    };
  });

  const healthyCount = agents.filter((a) => a.health === "HEALTHY").length;
  const failedCount = agents.filter((a) => a.health === "FAILED" || a.health === "DEGRADED").length;
  const unknownCount = agents.filter((a) => a.health === "UNKNOWN").length;

  return {
    window_hours: hours,
    total_agents: agents.length,
    healthy: healthyCount,
    failed_or_degraded: failedCount,
    unknown: unknownCount,
    agents,
    note: agents.every((a) => a.runs_in_window === 0)
      ? "لا تشغيلاتٍ مسجَّلة في agent_runs بعد ضمن هذه النافذة لأيّ وكيل — يلزم انتظار دورةٍ واحدة على الأقل بعد نشر Phase 1.5."
      : undefined,
  };
}

// ═══ Autonomous Operations 2.0 — Phase 2: أدوات جمع الأدلّة (Evidence
// Collector) لمحرّك التشخيص — قراءةٌ صرفة كسابقاتها، مُسمّاةٌ وضيّقة، لا
// SQL حرّ. القسم 21 من المواصفة: أدواتٌ محدَّدة فقط، لا وصول DB عام.

// آخر تشغيلاتٍ لوكيلٍ بعينه — التشخيص الحتمي الأول لأي حادثة (متى نجح
// آخر مرة، كم فشلاً متتالياً، ما نصّ الخطأ، هل المدّة الزمنية شاذّة).
export async function get_recent_agent_runs(admin: any, agentId: string, limit = 10) {
  const { data } = await admin
    .from("agent_runs")
    .select("run_id,status,trigger,started_at,completed_at,duration_ms,error,result_summary,correlation_id")
    .eq("agent_id", agentId)
    .order("started_at", { ascending: false })
    .limit(limit);
  const rows = data || [];
  const lastSuccess = rows.find((r: any) => r.status === "SUCCESS");
  let consecutiveFailures = 0;
  for (const r of rows) { if (r.status === "FAILED" || r.status === "TIMEOUT") consecutiveFailures++; else break; }
  const durations = rows.filter((r: any) => typeof r.duration_ms === "number").map((r: any) => r.duration_ms);
  const avgDurationMs = durations.length ? Math.round(durations.reduce((s: number, d: number) => s + d, 0) / durations.length) : null;
  const lastDurationMs = rows[0]?.duration_ms ?? null;
  return {
    agent_id: agentId,
    runs: rows,
    last_success_at: lastSuccess?.started_at ?? null,
    consecutive_failures: consecutiveFailures,
    avg_duration_ms: avgDurationMs,
    last_duration_ms: lastDurationMs,
    duration_anomaly: (avgDurationMs && lastDurationMs && lastDurationMs > avgDurationMs * 3) ? true : false,
    distinct_errors: [...new Set(rows.filter((r: any) => r.error).map((r: any) => String(r.error).slice(0, 200)))],
  };
}

// حوادث سابقة لنفس المكوّن — يميّز عطلاً متكرّراً معروفاً عن أول ظهورٍ له.
export async function get_related_incidents(admin: any, component: string, limit = 10) {
  const { data } = await admin
    .from("ops_incidents")
    .select("id,severity,status,summary,root_cause,confidence,occurrence_count,first_seen_at,last_seen_at,resolved_at")
    .eq("component", component)
    .order("detected_at", { ascending: false })
    .limit(limit);
  const rows = data || [];
  return {
    component,
    count: rows.length,
    incidents: rows,
    had_prior_resolution: rows.some((r: any) => r.status === "RESOLVED"),
  };
}

// صحة دالّة حافة بعينها (يُستدعى مع اسمٍ محدَّد بدل كل الدوالّ — سياقٌ أضيق
// لنداء تشخيصٍ عن مكوّنٍ بعينه).
export async function get_function_health(admin: any, functionName: string) {
  const since = new Date(Date.now() - 60 * 60 * 1000).toISOString();
  const { data } = await admin
    .from("health_checks")
    .select("component_name,status,response_time_ms,error_message,checked_at")
    .eq("component_name", `function:${functionName}`)
    .gte("checked_at", since)
    .order("checked_at", { ascending: false })
    .limit(20);
  return { function_name: functionName, checks: data || [] };
}

// سجلّ agent_schedules الحالي لوكيلٍ بعينه — يكشف تغييرات جدولةٍ حديثة
// كسببٍ محتمَل (contributing factor) لتشغيلٍ فائتٍ أو متأخّر.
export async function get_agent_schedule(admin: any, agentName: string) {
  const { data } = await admin
    .from("agent_schedules")
    .select("*")
    .eq("agent_name", agentName)
    .maybeSingle();
  return { agent_name: agentName, schedule: data || null, found: !!data };
}

// ═══ Phase 3 — القسم 28: أدواتٌ للكوبايلوت عن الإصلاح الذاتي (Self-
// Healing). قراءةٌ صرفة من repair_playbooks/repair_executions/
// self_healing_controls الحقيقية حصراً — لا اختلاق أرقام إن كانت الجداول
// فارغةً (كل شيءٍ يبدأ في Shadow Mode، فقد لا توجد بياناتٌ بعد). ═══

// "أي Playbook استُخدم؟" / "كم عملية Self-Healing تمّت؟" اليوم — ولماذا لم
// يُصلَح كذا تحديداً. كل الحقول من repair_executions الحقيقية حصراً —
// preconditions_result/confidence_at_decision/blast_radius موجودةٌ سلفاً في
// الجدول (Phase 3)، لم تكن تُقرَأ هنا قبل Phase 3.5-B Observability.
export async function get_self_healing_summary(admin: any, hours = 24) {
  const since = new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();
  const { data } = await admin
    .from("repair_executions")
    .select("repair_id,incident_id,playbook_id,status,mode,started_at,escalation_reason,confidence_at_decision,preconditions_result,error")
    .gte("started_at", since)
    .order("started_at", { ascending: false })
    .limit(200);
  const rows = data || [];
  const would_auto_heal = rows.filter((r: any) => r.status === "WOULD_AUTO_HEAL").length;
  const succeeded = rows.filter((r: any) => r.status === "SUCCEEDED").length;
  const failed = rows.filter((r: any) => ["FAILED", "VERIFICATION_FAILED"].includes(r.status)).length;
  const blockedStatuses = ["ESCALATED", "PRECONDITION_FAILED", "RISK_BLOCKED", "RATE_LIMITED", "COOLDOWN_ACTIVE", "CIRCUIT_OPEN", "DISABLED", "NO_PLAYBOOK_MATCH", "CLAIM_FAILED", "DUPLICATE_EXECUTION_BLOCKED", "ACTION_VALIDATION_FAILED", "INVALID_INCIDENT", "INVALID_DIAGNOSIS"];
  const escalated = rows.filter((r: any) => blockedStatuses.includes(r.status)).length;
  const circuit_open = rows.filter((r: any) => r.status === "CIRCUIT_OPEN").length;
  const by_playbook: Record<string, number> = {};
  for (const r of rows) by_playbook[r.playbook_id] = (by_playbook[r.playbook_id] || 0) + 1;
  const by_status: Record<string, number> = {};
  for (const r of rows) by_status[r.status] = (by_status[r.status] || 0) + 1;
  // "لماذا لم يُصلَح هذا؟" — تفاصيل كل تقييمٍ محجوب (لا نجاح)، مع السبب
  // الحقيقي المُخزَّن (escalation_reason/preconditions_result/error) — لا
  // إعادة صياغةٍ أو تخمين. حتى 30 صفّاً — كافٍ لسؤالٍ عن حادثةٍ بعينها.
  const blocked_details = rows
    .filter((r: any) => blockedStatuses.includes(r.status))
    .slice(0, 30)
    .map((r: any) => ({
      incident_id: r.incident_id, playbook_id: r.playbook_id, status: r.status,
      confidence_at_decision: r.confidence_at_decision, escalation_reason: r.escalation_reason,
      failed_preconditions: r.preconditions_result || null, error: r.error,
    }));
  return {
    window_hours: hours,
    total_evaluations: rows.length,
    would_auto_heal_shadow_mode: would_auto_heal,     // لا "إصلاحاتٍ فعلية" — كل شيءٍ Shadow اليوم
    actual_auto_heals_executed: succeeded,             // يبقى 0 بالضرورة ما دام لا Playbook في AUTO
    failed, escalated, circuit_breaker_triggered: circuit_open,
    by_playbook, by_status, blocked_details,
    note: rows.length ? null : "لا تقييمات Self-Healing مسجَّلة بعد في هذه النافذة الزمنية.",
  };
}

// "كم دورة جدولةٍ عملت؟ كم متوسّط زمنها؟" — من scheduler_runs الحقيقي
// (Phase 3.5-B) حصراً. لا تُختلَق إن كان الجدول فارغاً أو غير موجود.
export async function get_scheduler_runs_summary(admin: any, hours = 24) {
  const since = new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();
  const { data, error } = await admin
    .from("scheduler_runs")
    .select("run_id,started_at,completed_at,status,incidents_scanned,incidents_claimed,incidents_evaluated,shadow_would_repair,escalated,errors,duration_ms")
    .gte("started_at", since)
    .order("started_at", { ascending: false })
    .limit(500);
  if (error) return { available: false, note: "جدول scheduler_runs غير متاحٍ بعد." };
  const rows = data || [];
  const completed = rows.filter((r: any) => r.status === "COMPLETED");
  const failedRuns = rows.filter((r: any) => r.status === "FAILED").length;
  const durations = rows.filter((r: any) => typeof r.duration_ms === "number").map((r: any) => r.duration_ms as number);
  const avg_duration_ms = durations.length ? Math.round(durations.reduce((a: number, b: number) => a + b, 0) / durations.length) : null;
  const sum = (key: string) => rows.reduce((acc: number, r: any) => acc + (r[key] || 0), 0);
  return {
    window_hours: hours,
    total_runs: rows.length,
    completed_runs: completed.length,
    failed_runs: failedRuns,
    avg_duration_ms,
    total_incidents_scanned: sum("incidents_scanned"),
    total_incidents_claimed: sum("incidents_claimed"),
    total_incidents_evaluated: sum("incidents_evaluated"),
    total_would_auto_heal: sum("shadow_would_repair"),
    total_escalated: sum("escalated"),
    total_errors: sum("errors"),
    note: rows.length ? null : "لا دورات جدولةٍ مسجَّلة بعد في هذه النافذة الزمنية.",
  };
}

export async function get_repair_playbooks_status(admin: any) {
  const { data } = await admin.from("repair_playbooks")
    .select("playbook_id,name,mode,enabled,circuit_state,risk_level,minimum_confidence,max_attempts,cooldown_minutes,affected_scope")
    .order("playbook_id");
  return { playbooks: data || [] };
}

// "هل يوجد Playbook متوقّف بسبب Circuit Breaker؟"
export async function get_circuit_breaker_status(admin: any) {
  const { data } = await admin.from("repair_playbooks")
    .select("playbook_id,name,circuit_state,circuit_opened_at")
    .eq("circuit_state", "OPEN");
  return { open_circuits: data || [], any_open: !!(data && data.length) };
}

export async function get_self_healing_controls(admin: any) {
  const { data } = await admin.from("self_healing_controls").select("*").eq("control_id", "global").maybeSingle();
  return { controls: data || null };
}

// آخر ملخّصٍ حفظه وكيلٌ في agent_messages — daily-summary/file-processor-
// monitor لم يعودا يُرسلان تلغرام تلقائياً (يكتفيان بالحفظ هنا)؛ هذه
// الدالّة هي كيف تعرضهما لوحة التشغيل بدل انتظار رسالةٍ في تلغرام.
export async function get_latest_agent_message(admin: any, agentName: string) {
  const { data } = await admin.from("agent_messages")
    .select("message_text,sent_at,telegram_message_id")
    .eq("agent_name", agentName)
    .order("sent_at", { ascending: false })
    .limit(1)
    .maybeSingle();
  if (!data) return { found: false };
  return {
    found: true,
    message_text: data.message_text,
    sent_at: data.sent_at,
    was_pushed_to_telegram: data.telegram_message_id != null,
  };
}
