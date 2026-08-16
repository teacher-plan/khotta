-- ════════════════════════════════════════════════════════════════════
-- KHOTTA Autonomous Management — Phase 3 جدول: ops_incidents
--
-- سجلّ الحوادث المُكتشَفة آلياً من system-health-check الحالية (بلا تعديل
-- منطقها القائم — إضافةٌ بعده فقط). كل حادثةٍ تُجمَّع لا تُكرَّر: تكرار
-- نفس المكوّن المعطوب يزيد occurrence_count ويحدّث last_seen_at بدل صفٍّ
-- جديد وتنبيهٍ جديد. لا كتابة إلا من service_role (الوكلاء الحالية).
-- ════════════════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS public.ops_incidents (
  id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  -- مفتاح التجميع: المكوّن المتأثّر — كل حوادث المكوّن نفسه ضمن نافذةٍ
  -- مفتوحة تُعدّ حادثةً واحدة، لا حادثةً لكل فحصٍ فاشل.
  dedup_key        text        NOT NULL,
  severity         text        NOT NULL CHECK (severity IN ('P0','P1','P2','P3')),
  status           text        NOT NULL DEFAULT 'DETECTED'
                                CHECK (status IN ('DETECTED','INVESTIGATING','IDENTIFIED','RECOMMENDATION','RESOLVED')),
  component        text        NOT NULL,
  summary          text        NOT NULL,
  evidence         jsonb,        -- شواهد الفحوصات الخام (لا نصوصاً حرّة مُخترَعة)
  root_cause       text,         -- من ops-analyze عند توفّره — قد يبقى NULL
  confidence       text        CHECK (confidence IS NULL OR confidence IN ('VERIFIED','LIKELY','UNKNOWN')),
  recommendation   text,
  affected_users   int,
  occurrence_count int         NOT NULL DEFAULT 1,
  first_seen_at    timestamptz NOT NULL DEFAULT now(),
  last_seen_at     timestamptz NOT NULL DEFAULT now(),
  detected_at      timestamptz NOT NULL DEFAULT now(),
  resolved_at      timestamptz,
  telegram_message_id int
);

-- البحث عن حادثةٍ مفتوحة بنفس المفتاح — الاستعلام الأكثر تكراراً (كل ٥ دقائق).
CREATE INDEX IF NOT EXISTS idx_ops_incidents_dedup_open
  ON public.ops_incidents (dedup_key, status) WHERE status <> 'RESOLVED';
-- قوائم العرض: الأحدث أولاً، والتصفية بالخطورة/الحالة للوحة والـcopilot.
CREATE INDEX IF NOT EXISTS idx_ops_incidents_detected_at ON public.ops_incidents (detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_ops_incidents_severity     ON public.ops_incidents (severity);
CREATE INDEX IF NOT EXISTS idx_ops_incidents_status        ON public.ops_incidents (status);

ALTER TABLE public.ops_incidents ENABLE ROW LEVEL SECURITY;
-- داخليٌّ بالكامل — كنمط الجداول الداخلية القائمة: لا سياسة، service_role
-- فقط. القراءة من المشرف تمرّ عبر ops-analyze/ops-copilot (حارسٌ في
-- الدالّة يتحقّق من is_app_admin())، لا مباشرةً من REST.
REVOKE ALL ON public.ops_incidents FROM anon, authenticated;

COMMENT ON TABLE public.ops_incidents IS
  'حوادث مُكتشَفة آلياً من system-health-check — مُجمَّعة لا مكرَّرة. داخليٌّ: service_role فقط، القراءة الإدارية عبر ops-analyze.';
