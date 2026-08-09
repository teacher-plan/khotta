-- نظام الوكلاء الذكيين (Agent System)
-- جداول لتتبع وجدولة الوكلاء والرسائل والسجلات

-- جدول جدولة الوكلاء
CREATE TABLE IF NOT EXISTS agent_schedules (
  agent_name TEXT PRIMARY KEY,
  scheduled_hour INT DEFAULT 17,  -- الساعة (0-23)
  scheduled_minute INT DEFAULT 0, -- الدقيقة (0-59)
  enabled BOOLEAN DEFAULT TRUE,
  description TEXT,
  last_run TIMESTAMPTZ,
  next_run TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول سجل الرسائل والتفاعلات
CREATE TABLE IF NOT EXISTS agent_messages (
  message_id TEXT PRIMARY KEY,
  agent_name TEXT NOT NULL,
  message_text TEXT NOT NULL,
  sent_at TIMESTAMPTZ DEFAULT NOW(),
  telegram_message_id INT,
  user_action TEXT,  -- "reschedule", "detailed_report", "disable", "enable"
  action_timestamp TIMESTAMPTZ
);

-- جدول سجلات تنفيذ الوكلاء
CREATE TABLE IF NOT EXISTS agent_logs (
  log_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  agent_name TEXT NOT NULL,
  action TEXT,  -- "started", "completed", "failed"
  status TEXT,  -- "success", "error", "pending"
  error_message TEXT,
  execution_time_ms INT,
  data_collected JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول بيانات المستخدمين للتحليل
CREATE TABLE IF NOT EXISTS user_analytics (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  teacher_name TEXT,
  total_ai_calls INT DEFAULT 0,
  ai_quota_used INT DEFAULT 0,
  ai_quota_limit INT DEFAULT 0,
  files_uploaded INT DEFAULT 0,
  last_activity_at TIMESTAMPTZ,
  satisfaction_score INT,  -- 1-5
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول الاستبيانات والآراء
CREATE TABLE IF NOT EXISTS user_surveys (
  survey_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  survey_type TEXT,  -- "satisfaction", "feature_request", "bug_report"
  responses JSONB,
  submitted_at TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول تتبع أوقات الاستخدام
CREATE TABLE IF NOT EXISTS usage_tracking (
  event_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  event_type TEXT,  -- "login", "feature_used", "content_viewed"
  feature_name TEXT,
  session_duration_sec INT,
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- جدول مقترحات التحليل الذكي
CREATE TABLE IF NOT EXISTS analytics_insights (
  insight_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  insight_type TEXT,  -- "warning", "suggestion", "trend"
  title TEXT NOT NULL,
  description TEXT,
  severity INT,  -- 1-5 (1=low, 5=critical)
  affected_users INT,
  recommendation TEXT,
  status TEXT DEFAULT 'pending',  -- "pending", "reviewed", "dismissed"
  created_at TIMESTAMPTZ DEFAULT NOW(),
  reviewed_at TIMESTAMPTZ
);

-- Indexes للأداء
CREATE INDEX IF NOT EXISTS idx_agent_schedules_enabled ON agent_schedules(enabled);
CREATE INDEX IF NOT EXISTS idx_agent_messages_sent_at ON agent_messages(sent_at DESC);
CREATE INDEX IF NOT EXISTS idx_agent_logs_agent_name ON agent_logs(agent_name);
CREATE INDEX IF NOT EXISTS idx_user_analytics_updated ON user_analytics(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_user_id ON usage_tracking(user_id);
CREATE INDEX IF NOT EXISTS idx_usage_tracking_timestamp ON usage_tracking(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_insights_severity ON analytics_insights(severity DESC);

-- إضافة البيانات الأولية للوكلاء
INSERT INTO agent_schedules (agent_name, scheduled_hour, scheduled_minute, description)
VALUES
  ('credit-monitor', 17, 0, 'مراقبة استهلاك الرصيد لكل معلمة'),
  ('library-monitor', 17, 5, 'مراقبة المكتبة والملفات المرفوعة'),
  ('peak-hours-monitor', 17, 10, 'تحليل أوقات الذروة والاستخدام'),
  ('feedback-collector', 17, 15, 'جمع آراء المستخدمين'),
  ('analytics-agent', 17, 20, 'تحليل البيانات وتوليد الاقتراحات')
ON CONFLICT DO NOTHING;

-- التعليقات
COMMENT ON TABLE agent_schedules IS 'جداول جدولة الوكلاء - تحدد متى يعمل كل وكيل';
COMMENT ON TABLE agent_messages IS 'سجل جميع الرسائل المرسلة للمستخدم عبر Telegram';
COMMENT ON TABLE agent_logs IS 'سجل تنفيذ الوكلاء - لتتبع الأخطاء والأداء';
COMMENT ON TABLE user_analytics IS 'بيانات تحليلية عن كل معلمة لإنتاج الاقتراحات';
