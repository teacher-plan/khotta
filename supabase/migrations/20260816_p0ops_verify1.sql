DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'ai_cost_log_rows', (SELECT json_agg(json_build_object('function_name',function_name,'kind',kind,'model',model,'cost_usd',cost_usd,'created_at',created_at)) FROM public.ai_cost_log WHERE user_id = '1618acc4-1b30-4c5c-b8d1-e581bf1ca479'),
    'ai_usage_rows', (SELECT json_agg(json_build_object('month',month,'kind',kind,'count',count)) FROM public.ai_usage WHERE user_id = '1618acc4-1b30-4c5c-b8d1-e581bf1ca479')
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
