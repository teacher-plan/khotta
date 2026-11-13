do $$ declare r text; begin
select string_agg(format('%s|%s', status_code, left(content::text,200)), ' ;; ' order by created desc) into r from (select * from net._http_response order by created desc limit 3) x;
raise exception 'PROBE>> % || cron: %', r, (select string_agg(jobname||' '||schedule,', ') from cron.job where jobname like 'c1-push%');
end $$;
