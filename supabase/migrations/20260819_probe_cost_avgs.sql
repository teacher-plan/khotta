DO $$
DECLARE v text;
BEGIN
  SELECT string_agg(format('%s/%s: n=%s avg=%s min=%s max=%s',function_name,kind,cnt,avg_cost,min_cost,max_cost), E'\n' ORDER BY function_name,kind)
  INTO v
  FROM (
    SELECT function_name, kind, count(*) cnt,
      round(avg(cost_usd)::numeric,6) avg_cost,
      round(min(cost_usd)::numeric,6) min_cost,
      round(max(cost_usd)::numeric,6) max_cost
    FROM public.ai_cost_log
    WHERE cost_usd IS NOT NULL
    GROUP BY function_name, kind
  ) t;
  RAISE EXCEPTION 'PROBE | %', COALESCE(v,'NO_ROWS');
END $$;
