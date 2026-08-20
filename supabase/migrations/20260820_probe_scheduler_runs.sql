-- probe: مقاييس autonomous-scheduler الفعلية من scheduler_runs (يتراجع عن نفسه)
do $$
declare v text; declare c int;
declare tot_scan int; declare tot_claim int; declare tot_eval int; declare tot_would int; declare tot_esc int; declare tot_err int;
begin
  select count(*) into c from scheduler_runs;
  select coalesce(sum(incidents_scanned),0), coalesce(sum(incidents_claimed),0), coalesce(sum(incidents_evaluated),0),
         coalesce(sum(shadow_would_repair),0), coalesce(sum(escalated),0), coalesce(sum(errors),0)
    into tot_scan, tot_claim, tot_eval, tot_would, tot_esc, tot_err
  from scheduler_runs;
  select string_agg(
    started_at::text||'|status='||status||'|scanned='||incidents_scanned||'|claimed='||incidents_claimed||
    '|evaluated='||incidents_evaluated||'|would='||shadow_would_repair||'|esc='||escalated||'|err='||errors,
    e'\n' order by started_at desc)
  into v
  from (select * from scheduler_runs order by started_at desc limit 15) t;
  raise exception 'PROBE | total_runs=% | SUM(scanned=%,claimed=%,evaluated=%,would=%,escalated=%,errors=%) | recent=[%]',
    c, tot_scan, tot_claim, tot_eval, tot_would, tot_esc, tot_err, coalesce(v,'NONE');
end $$;
