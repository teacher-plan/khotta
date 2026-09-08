DO $$
DECLARE d text;
BEGIN
  SELECT format(
    'pv_last=%s | recent_regs=%s',
    (SELECT max(created_at) FROM page_views WHERE page='cycle1-landing'),
    (SELECT string_agg(created_at::text || '(notified=' || coalesce(notified_at::text,'NULL') || ')', ' | ' ORDER BY created_at DESC)
       FROM (SELECT created_at, notified_at FROM pre_registrations WHERE stage='cycle1' ORDER BY created_at DESC LIMIT 8) x)
  ) INTO d;
  RAISE EXCEPTION 'DATA=%', d;
END $$;
