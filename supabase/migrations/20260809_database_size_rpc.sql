-- دالة RPC لفحص حجم قاعدة البيانات
-- تُستخدم من system-health-check لمراقبة استهلاك التخزين

CREATE OR REPLACE FUNCTION database_size()
RETURNS TABLE (database_size_mb NUMERIC)
LANGUAGE sql
SECURITY DEFINER
SET search_path = public
AS $$
  SELECT ROUND(pg_database_size(current_database()) / 1024.0 / 1024.0, 2) AS database_size_mb;
$$;

COMMENT ON FUNCTION database_size() IS 'يُرجع حجم قاعدة البيانات الحالية بالميجابايت — يُستخدم من وكيل system-health-check';

-- تقييد الوصول: فقط service_role يستدعيها (لا anon ولا authenticated)
REVOKE ALL ON FUNCTION database_size() FROM PUBLIC;
REVOKE ALL ON FUNCTION database_size() FROM anon;
REVOKE ALL ON FUNCTION database_size() FROM authenticated;
GRANT EXECUTE ON FUNCTION database_size() TO service_role;
