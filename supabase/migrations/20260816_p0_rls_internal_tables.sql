-- ════════════════════════════════════════════════════════════════════
-- P0/١ — إقفال الجداول الداخلية الثلاثة عشر
--
-- كانت تُنشأ بلا ROW LEVEL SECURITY وبلا سياسات، فأي معلّمة مسجَّلة تقرأ
-- بمفتاح anon وحده: user_analytics (بريد كل معلّمة واسمها واستهلاكها)،
-- error_logs (user_id وstack_trace)، file_processing_status (uploaded_by)،
-- وتكتب في agent_schedules فتُعطّل المراقبة.
--
-- العلاج الأصغر والأسلم: تفعيل RLS بلا أيّ سياسة.
--   • service_role يتجاوز RLS بحكم تصميم Postgres — فكل الوكلاء ودوال
--     الحافة تبقى تعمل بلا حرفٍ واحد من التعديل.
--   • authenticated وanon بلا سياسة = صفر صفوف، صفر كتابة.
-- وتُحقّق أن هذا لا يكسر شيئاً: بحثٌ عن ‎from('<table>')‎ في كل ملفات
-- الواجهة أعاد صفراً للثلاثة عشر جميعاً — لا أحد منها يُقرأ من المتصفح.
-- ════════════════════════════════════════════════════════════════════

ALTER TABLE public.health_checks           ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.emergency_alerts        ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.file_processing_status  ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.error_logs              ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.performance_metrics     ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.service_status          ENABLE ROW LEVEL SECURITY;

ALTER TABLE public.agent_schedules         ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_messages          ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.agent_logs              ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_analytics          ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_surveys            ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.usage_tracking          ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.analytics_insights      ENABLE ROW LEVEL SECURITY;

-- سحبُ الامتيازات أيضاً: RLS يحرس الصفوف، وسحبُ GRANT يحرس الجدول نفسه.
-- الاثنان معاً فلا يكفي أن تُنسى سياسةٌ يوماً ليُفتح الباب.
REVOKE ALL ON public.health_checks,          public.emergency_alerts,
              public.file_processing_status, public.error_logs,
              public.performance_metrics,    public.service_status,
              public.agent_schedules,        public.agent_messages,
              public.agent_logs,             public.user_analytics,
              public.user_surveys,           public.usage_tracking,
              public.analytics_insights
  FROM anon, authenticated;

COMMENT ON TABLE public.user_analytics IS
  'جدولٌ داخليّ للوكلاء — RLS مفعّل بلا سياسات: service_role فقط. لا يُقرأ من المتصفح.';
COMMENT ON TABLE public.error_logs IS
  'جدولٌ داخليّ للوكلاء — RLS مفعّل بلا سياسات: service_role فقط. لا يُقرأ من المتصفح.';
