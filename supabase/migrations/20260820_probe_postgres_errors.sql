-- probe: هل error_logs يسجّل شيئاً؟ وهل توجد أنماط أخطاءٍ حديثة يمكن رؤيتها
-- من داخل القاعدة (استعلامات فاشلة مسجَّلة، اتصالات، إلخ). يتراجع عن نفسه.
do $$
declare v text;
declare c_errlog int;
declare c_recent int;
begin
  select count(*) into c_errlog from public.error_logs;
  select count(*) into c_recent from public.error_logs where occurred_at > now() - interval '48 hours';

  select string_agg(
    coalesce(function_name,'-') || ' | ' || coalesce(left(error_message,150),'-') ||
    ' | ' || occurred_at::text,
    e'\n' order by occurred_at desc)
  into v
  from (select * from public.error_logs order by occurred_at desc limit 15) t;

  raise exception 'PROBE | error_logs_total=% | error_logs_48h=% | recent=%',
    c_errlog, c_recent, coalesce(v,'(none)');
end $$;
