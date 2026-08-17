// ═══ KHOTTA Autonomous Operations 2.0 — Phase 2: محرّك التشخيص + محرّك
// الخطورة (Diagnosis Engine + Risk Engine) ═══
//
// القسم 23 من المواصفة: منطقٌ حتميٌّ أولاً — لا نداء LLM لكل خطوة. حالاتٌ
// مثل "فشلٌ متكرّر بنفس رسالة الخطأ" تُشخَّص بقواعد صريحة بلا أي نداء
// ذكاءٍ اصطناعي. الـLLM محجوزٌ فقط حين تحتاج البيانات تفسيراً لغوياً/
// ربطاً بين أدلّةٍ متعدّدة لا تحسمه قاعدةٌ بسيطة.
//
// القسم 20: أنبوبٌ صريحٌ ثابت — Evidence → Diagnosis (rules|llm) → Risk —
// لا وكيلٌ (agentic loop) يقرّر خطوته التالية بحرّية.
//
// deno-lint-ignore-file no-explicit-any
import {
  get_recent_agent_runs, get_related_incidents, get_function_health,
  get_agent_schedule, get_database_capacity,
} from "./opsTools.ts";

export interface EvidenceItem {
  source: string;
  timestamp: string;
  type: string;
  value: unknown;
  reliability: "VERIFIED" | "DERIVED" | "UNKNOWN";
}

// جمعُ أدلّةٍ ضيّقة ومحدَّدة لحادثةٍ بعينها — لا "تفريغ القاعدة كلها"
// (القسم 2). كل بندٍ يحمل مصدره ووقته ونوعه وموثوقيته صراحةً.
export async function collectEvidence(
  admin: any,
  incident: { component: string; summary: string; source_agent?: string | null },
): Promise<EvidenceItem[]> {
  const now = new Date().toISOString();
  const agentId = incident.source_agent || incident.component;
  const [runs, related, fnHealth, schedule, dbCap] = await Promise.all([
    get_recent_agent_runs(admin, agentId, 10),
    get_related_incidents(admin, incident.component, 10),
    get_function_health(admin, agentId),
    get_agent_schedule(admin, agentId),
    incident.component.includes("database") || incident.component.includes("capacity")
      ? get_database_capacity(admin) : Promise.resolve(null),
  ]);

  const items: EvidenceItem[] = [
    { source: "get_recent_agent_runs", timestamp: now, type: "agent_run_history", value: runs, reliability: "VERIFIED" },
    { source: "get_related_incidents", timestamp: now, type: "incident_history", value: related, reliability: "VERIFIED" },
    { source: "get_function_health", timestamp: now, type: "function_health", value: fnHealth, reliability: "VERIFIED" },
    { source: "get_agent_schedule", timestamp: now, type: "schedule_config", value: schedule, reliability: "VERIFIED" },
  ];
  if (dbCap) items.push({ source: "get_database_capacity", timestamp: now, type: "db_capacity", value: dbCap, reliability: dbCap.available ? "VERIFIED" : "UNKNOWN" });
  return items;
}

export interface DeterministicDiagnosis {
  matched: boolean;
  suspected_root_cause?: string;
  confidence?: number;
  confidence_reasoning?: string;
  contributing_factors?: string[];
  recommended_action_id?: string | null;
  recommended_action_params?: Record<string, unknown>;
}

// القسم 3+4: قواعدُ تمييزٍ حتمية بين "عرَض" و"سببٌ مُرجَّح" لأنماطٍ معروفة
// بلا نداء LLM إطلاقاً — رخيصةٌ وسريعةٌ وحتمية 100%. تُعيد matched:false
// إن لم تطابق نمطاً معروفاً، فينتقل المُستدعي إلى تحليل LLM.
export function ruleBasedDiagnose(evidence: EvidenceItem[]): DeterministicDiagnosis {
  const runsItem = evidence.find((e) => e.source === "get_recent_agent_runs")?.value as any;
  if (!runsItem) return { matched: false };

  const failures = runsItem.consecutive_failures || 0;
  const errors: string[] = runsItem.distinct_errors || [];
  const sameError = errors.length === 1 && failures >= 2;

  // نمطٌ ١: فشلٌ متكرّر (٣+) بنفس رسالة الخطأ تماماً — ثقةٌ عالية أن السبب
  // ثابتٌ ومتكرّر لا عارضاً.
  if (failures >= 3 && sameError) {
    return {
      matched: true,
      suspected_root_cause: `فشلٌ متكرّر (${failures} مرّات متتالية) بنفس رسالة الخطأ: "${errors[0]}" — يشير إلى سببٍ ثابت (تبعية معطوبة/إعداد خاطئ) لا عطلاً عابراً.`,
      confidence: 85,
      confidence_reasoning: `${failures} تشغيلاتٍ فاشلة متتالية بنفس نصّ الخطأ حرفياً، لا رسائل متغيّرة — نمط فشلٍ ثابت مؤكَّدٌ من agent_runs مباشرةً.`,
      contributing_factors: [`${failures} فشلاً متتالياً`, "نفس رسالة الخطأ في كل مرّة"],
      recommended_action_id: "rerun_monitor_agent",
      recommended_action_params: { agent_id: runsItem.agent_id },
    };
  }

  // نمطٌ ٢: مدّة تنفيذٍ شاذّة (٣× المتوسّط) — احتمال بطء تبعيةٍ خارجية
  // (استعلام DB بطيء/API خارجي بطيء) لا خطأ برمجي.
  if (runsItem.duration_anomaly) {
    return {
      matched: true,
      suspected_root_cause: "مدّة تنفيذٍ أطول بأكثر من ٣ أضعاف المتوسّط في آخر تشغيلة — سببٌ محتمَل: بطء استعلام قاعدة بيانات أو استجابة API خارجي، وليس بالضرورة خطأً برمجياً (SYMPTOM لا ROOT CAUSE مؤكَّد).",
      confidence: 55,
      confidence_reasoning: "مدّةٌ شاذّة إحصائياً مقارنةً بالمتوسّط التاريخي، لكن لا دليل مباشر على المصدر بالتحديد (استعلامٌ بعينه أم API خارجي) — ثقةٌ متوسّطة فقط.",
      contributing_factors: ["مدّة تنفيذٍ أعلى من ٣× المتوسّط"],
      recommended_action_id: "rerun_monitor_agent",
      recommended_action_params: { agent_id: runsItem.agent_id },
    };
  }

  // نمطٌ ٣: فشلةٌ واحدة فقط، لا نمط متكرّر — أدلّةٌ غير كافية لتشخيصٍ واثق.
  if (failures === 1) {
    return {
      matched: true,
      suspected_root_cause: undefined,
      confidence: 20,
      confidence_reasoning: "فشلةٌ واحدة فقط بلا تكرار — قد تكون عطلاً عابراً (شبكة/زمن استجابة مؤقّت). أدلّةٌ غير كافية لتحديد سببٍ جذري بثقة.",
      contributing_factors: ["فشلةٌ واحدة معزولة، لا نمط بعد"],
      recommended_action_id: null,
    };
  }

  return { matched: false };
}

// القسم 5: محرّك الخطورة — مستقلٌّ تماماً عن التشخيص، حتميٌّ بالكامل
// (بلا LLM إطلاقاً)، مبنيٌّ فقط على خواصّ الإجراء المُقترَح نفسه من
// safe_action_registry — لا من نصّ التشخيص.
export interface RiskAssessment {
  risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
  requires_human: boolean;
  factors: {
    data_modification: boolean;
    user_impact: boolean;
    financial_impact: boolean;
    reversibility: "REVERSIBLE" | "IRREVERSIBLE";
    blast_radius: "SINGLE_AGENT" | "MULTI_COMPONENT" | "PLATFORM_WIDE";
    production_impact: boolean;
    security_impact: boolean;
  };
}

export function assessRisk(action: {
  category: string; risk_level: string; reversible: boolean;
} | null): RiskAssessment {
  if (!action) {
    // لا إجراءٌ آمن مطابق — لا خطورة تنفيذٍ لأنه لا تنفيذ أصلاً، لكن
    // requires_human=true دوماً (توصيةٌ يدوية فقط).
    return {
      risk_level: "LOW", requires_human: true,
      factors: { data_modification: false, user_impact: false, financial_impact: false, reversibility: "REVERSIBLE", blast_radius: "SINGLE_AGENT", production_impact: false, security_impact: false },
    };
  }
  const dataModification = action.category === "RESCHEDULE";
  const reversibility = action.reversible ? "REVERSIBLE" : "IRREVERSIBLE";
  // القسم 13: إجراءٌ لا يمكن التراجع عنه يرفع خطورته آلياً بدرجةٍ واحدة
  // على الأقل — بلا استثناء، حتى لو كان مسجَّلاً LOW في القاعدة.
  let level = action.risk_level as RiskAssessment["risk_level"];
  if (!action.reversible) {
    const order: RiskAssessment["risk_level"][] = ["LOW", "MEDIUM", "HIGH", "CRITICAL"];
    const idx = order.indexOf(level);
    level = order[Math.min(idx + 1, order.length - 1)];
  }
  // القسم 8: MEDIUM/HIGH/CRITICAL أو مساسٌ بمستخدمين/بيانات مالية/
  // أكاديمية/مخطط/مصادقة/أمن ⇒ موافقةٌ بشرية إلزامية. هذا تقييمٌ استشاريٌّ
  // للعرض في التشخيص فقط — البوّابة الفعلية وقت التنفيذ هي عمود
  // safe_action_registry.requires_human_approval نفسه (opsActionRegistry.ts)،
  // لا هذه الدالّة؛ لا ازدواج مصدر حقيقة (source of truth) وقت التنفيذ.
  const requiresHuman = level !== "LOW";
  return {
    risk_level: level,
    requires_human: requiresHuman,
    factors: {
      data_modification: dataModification,
      user_impact: false,       // كلا الإجراءين الحاليَّين لا يمسّان بيانات مستخدمين إطلاقاً
      financial_impact: false,
      reversibility,
      blast_radius: "SINGLE_AGENT",
      production_impact: action.category === "RERUN_MONITOR",  // يستدعي دالّة حافة إنتاجية فعلياً
      security_impact: false,
    },
  };
}
