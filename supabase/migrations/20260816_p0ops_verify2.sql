DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'ai_cost_log_count', (SELECT count(*) FROM public.ai_cost_log WHERE user_id = '1618acc4-1b30-4c5c-b8d1-e581bf1ca479'),
    'ai_cost_log_costs', (SELECT json_agg(cost_usd ORDER BY created_at) FROM public.ai_cost_log WHERE user_id = '1618acc4-1b30-4c5c-b8d1-e581bf1ca479'),
    'ai_usage_count', (SELECT count FROM public.ai_usage WHERE user_id = '1618acc4-1b30-4c5c-b8d1-e581bf1ca479' AND kind='text' AND month='2026-08')
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
