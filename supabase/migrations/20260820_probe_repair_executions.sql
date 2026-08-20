-- probe: سجلّ repair_executions الحقيقي — هل Shadow-Live يعمل فعلاً؟ (يتراجع عن نفسه)
do $$
declare v text; declare c int;
begin
  select count(*) into c from repair_executions;
  select string_agg(
    status||'|playbook='||coalesce(playbook_id,'-')||'|action='||coalesce(action_id,'-')||
    '|mode='||mode||'|conf='||coalesce(confidence_at_decision::text,'-')||
    '|esc='||coalesce(left(escalation_reason,120),'-')||'|at='||started_at::text,
    e'\n' order by started_at desc)
  into v
  from (select * from repair_executions order by started_at desc limit 30) t;
  raise exception 'PROBE | total=% | rows=[%]', c, coalesce(v,'NONE');
end $$;
