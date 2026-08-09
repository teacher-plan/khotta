-- نظام مراقبة صحة النظام (System Health Monitoring)
-- يراقب أداء الخوادم والدوال والبيانات بشكل مستمر

-- جدول تسجيل حالة الفحوصات
CREATE TABLE IF NOT EXISTS health_checks (
  check_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  check_type TEXT NOT NULL,  -- "function", "database", "storage", "file_processing"
  component_name TEXT NOT NULL,  -- اسم الدالة أو المكون
  status TEXT NOT NULL,  -- "healthy", "warning", "critical", "unknown"
  response_time_ms INT,
  error_message TEXT,
  error_details JSONB,
  checked_at TIMESTAMPTZ DEFAULT NOW(),
  severity INT  -- 1-5 (1=info, 2=warning, 3=error, 4=critical, 5=fatal)
);

-- جدول التنبيهات الطارئة (Emergency Alerts)
CREATE TABLE IF NOT EXISTS emergency_alerts (
  alert_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  alert_type TEXT NOT NULL,  -- "function_down", "database_slow", "storage_full", etc.
  severity INT NOT NULL,  -- 1-5
  title TEXT NOT NULL,
  description TEXT,
  affected_component TEXT,
  action_required TEXT,  -- الإجراء المقترح
  resolved BOOLEAN DEFAULT FALSE,
  resolved_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول الملفات المعالجة (Processing Status)
CREATE TABLE IF NOT EXISTS file_processing_status (
  file_id UUID PRIMARY KEY,
  file_name TEXT NOT NULL,
  file_size_bytes INT,
  uploaded_by UUID REFERENCES auth.users(id),
  processing_type TEXT,  -- "segment_book", "extract_lessons", etc.
  status TEXT NOT NULL,  -- "pending", "processing", "completed", "failed"
  progress_percent INT DEFAULT 0,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  error_message TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- جدول سجل الأخطاء (Error Logs)
CREATE TABLE IF NOT EXISTS error_logs (
  error_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  error_type TEXT,  -- "function_error", "database_error", "api_error"
  function_name TEXT,
  error_message TEXT NOT NULL,
  error_code TEXT,
  stack_trace TEXT,
  user_id UUID REFERENCES auth.users(id),
  occurred_at TIMESTAMPTZ DEFAULT NOW(),
  resolved BOOLEAN DEFAULT FALSE
);

-- جدول الأداء (Performance Metrics)
CREATE TABLE IF NOT EXISTS performance_metrics (
  metric_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  metric_name TEXT NOT NULL,  -- "db_response_time", "function_duration", etc.
  component TEXT,
  value FLOAT NOT NULL,
  unit TEXT,  -- "ms", "MB", "%"
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- جدول حالة الخدمات (Service Status)
CREATE TABLE IF NOT EXISTS service_status (
  service_id TEXT PRIMARY KEY,
  service_name TEXT NOT NULL,
  status TEXT NOT NULL,  -- "operational", "degraded", "down"
  status_message TEXT,
  last_checked TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes للأداء
CREATE INDEX IF NOT EXISTS idx_health_checks_checked_at ON health_checks(checked_at DESC);
CREATE INDEX IF NOT EXISTS idx_health_checks_status ON health_checks(status);
CREATE INDEX IF NOT EXISTS idx_health_checks_component ON health_checks(component_name);
CREATE INDEX IF NOT EXISTS idx_emergency_alerts_severity ON emergency_alerts(severity DESC);
CREATE INDEX IF NOT EXISTS idx_emergency_alerts_resolved ON emergency_alerts(resolved);
CREATE INDEX IF NOT EXISTS idx_emergency_alerts_created ON emergency_alerts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_file_processing_status ON file_processing_status(status);
CREATE INDEX IF NOT EXISTS idx_error_logs_occurred ON error_logs(occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_error_logs_function ON error_logs(function_name);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_timestamp ON performance_metrics(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_performance_metrics_component ON performance_metrics(component);

-- تعليقات
COMMENT ON TABLE health_checks IS 'سجل جميع فحوصات الصحة الدورية';
COMMENT ON TABLE emergency_alerts IS 'تنبيهات طارئة تحتاج إجراء فوري';
COMMENT ON TABLE file_processing_status IS 'تتبع حالة معالجة الملفات الكبيرة';
COMMENT ON TABLE error_logs IS 'سجل جميع الأخطاء في النظام';
COMMENT ON TABLE performance_metrics IS 'مقاييس الأداء التفصيلية';
COMMENT ON TABLE service_status IS 'حالة كل خدمة رئيسية';

-- بيانات أولية للخدمات
INSERT INTO service_status (service_id, service_name, status, status_message)
VALUES
  ('supabase-api', 'Supabase API', 'operational', 'جميع الخدمات تعمل بشكل طبيعي'),
  ('database', 'PostgreSQL Database', 'operational', 'قاعدة البيانات تعمل بشكل طبيعي'),
  ('storage', 'Supabase Storage', 'operational', 'خدمة التخزين تعمل بشكل طبيعي'),
  ('edge-functions', 'Edge Functions', 'operational', 'جميع الدوال تعمل بشكل طبيعي')
ON CONFLICT DO NOTHING;
