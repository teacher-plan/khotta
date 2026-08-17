-- تنظيفٌ بعد التقاط الدليل: حذف صفّي الاختبار الاصطناعي فقط (repair_executions
-- ثم ops_incidents الموسوم __phase3_1_test__)، بلا أثرٍ متبقٍّ في جداول
-- الإنتاج. لا يمسّ أي صفٍّ حقيقيٍّ آخر.
DELETE FROM public.repair_executions
  WHERE incident_id IN (SELECT id FROM public.ops_incidents WHERE dedup_key = '__phase3_1_test__credit-monitor');

DELETE FROM public.ops_incidents WHERE dedup_key = '__phase3_1_test__credit-monitor';
