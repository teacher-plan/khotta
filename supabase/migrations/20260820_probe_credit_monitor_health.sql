-- probe: آخر تشغيلات credit-monitor وأخطاؤها (يتراجع عن نفسه)
do $$
declare v text;
begin
  select string_agg(
    status || ' | started=' || started_at::text ||
    ' | dur=' || coalesce(duration_ms::text,'-') || 'ms' ||
    ' | err=' || coalesce(left(error,200),'-'),
    e'\n' order by started_at desc)
  into v
  from (select * from public.agent_runs where agent_id='credit-monitor' order by started_at desc limit 10) t;
  raise exception 'PROBE | %', coalesce(v,'no rows');
end $$;
