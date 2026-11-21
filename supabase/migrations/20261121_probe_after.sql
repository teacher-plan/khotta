-- فحص مؤقت: هل عادت الوكلاء؟ (أعداد فقط)
do $$ declare r text;
begin
  select 'health_checks_last10min='||count(*) into r from health_checks where checked_at > now() - interval '10 minutes';
  select r||' | 401s_last10='||count(*) from net._http_response where created > now() - interval '10 minutes' and status_code=401 into r;
  select r||' | 2xx_last10='||count(*) from net._http_response where created > now() - interval '10 minutes' and status_code between 200 and 299 into r;
  raise exception 'PROBE %', r;
end $$;
