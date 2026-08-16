DO $$
DECLARE d json;
BEGIN
  SELECT json_build_object(
    'now', now(),
    'health_checks_recent', (
      SELECT json_agg(t) FROM (
        SELECT component_name, status, error_message, response_time_ms, checked_at
        FROM public.health_checks
        WHERE component_name IN ('function:generate-lesson-plan','function:generate-game-content')
        ORDER BY checked_at DESC LIMIT 10
      ) t
    ),
    'error_logs_recent', (
      SELECT json_agg(t) FROM (
        SELECT function_name, error_type, error_code, occurred_at
        FROM public.error_logs
        WHERE function_name IN ('generate-lesson-plan','generate-game-content')
          AND occurred_at > now() - interval '6 hours'
        ORDER BY occurred_at DESC LIMIT 20
      ) t
    ),
    'ai_cost_log_recent_lesson_plan', (
      SELECT json_agg(t) FROM (
        SELECT created_at, model, cost_usd
        FROM public.ai_cost_log
        WHERE function_name='generate-lesson-plan'
        ORDER BY created_at DESC LIMIT 5
      ) t
    ),
    'ai_cost_log_recent_game_content', (
      SELECT json_agg(t) FROM (
        SELECT created_at, model, cost_usd
        FROM public.ai_cost_log
        WHERE function_name='generate-game-content'
        ORDER BY created_at DESC LIMIT 5
      ) t
    ),
    'emergency_alerts_recent', (
      SELECT json_agg(t) FROM (
        SELECT alert_type, severity, affected_component, resolved, created_at
        FROM public.emergency_alerts
        WHERE affected_component IN ('function:generate-lesson-plan','function:generate-game-content')
        ORDER BY created_at DESC LIMIT 10
      ) t
    )
  ) INTO d;
  RAISE EXCEPTION '%', d::text;
END;
$$;
