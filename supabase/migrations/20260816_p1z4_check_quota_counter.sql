DO $$
DECLARE d json;
BEGIN
  SELECT json_agg(json_build_object('user_id',user_id,'month',month,'kind',kind,'count',count))
    INTO d
  FROM public.ai_usage
  WHERE user_id = '4ad320f7-77b4-4e51-a200-0dd5c262fb8b';
  RAISE EXCEPTION '%', COALESCE(d::text, 'no-rows');
END;
$$;
