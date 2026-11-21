-- فحص مؤقت بعد النشر: هل تعمل الوكلاء المجدولة بالحارس الجديد؟ (أعداد فقط)
do $$ declare r text;
begin
  select 'health_checks_since_deploy='||count(*) into r from health_checks where checked_at > '2026-11-21 17:50:00+00';
  select r||' | 401s='||count(*) from net._http_response where created > '2026-11-21 17:50:00+00' and status_code=401 into r;
  select r||' | 2xx='||count(*) from net._http_response where created > '2026-11-21 17:50:00+00' and status_code between 200 and 299 into r;
  raise exception 'PROBE %', r;
end $$;
