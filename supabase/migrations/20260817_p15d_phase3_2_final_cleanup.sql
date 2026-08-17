-- تنظيفٌ نهائي — لا بقايا اختبارٍ في جداول الإنتاج.
DELETE FROM public.repair_executions
  WHERE incident_id IN (SELECT id FROM public.ops_incidents WHERE dedup_key = '__phase3_2_final_test__credit-monitor');
DELETE FROM public.ops_incidents WHERE dedup_key = '__phase3_2_final_test__credit-monitor';
