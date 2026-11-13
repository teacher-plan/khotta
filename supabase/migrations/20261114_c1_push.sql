-- ════════════════════════════════════════════════════════════════════
-- إشعارات الهاتف (Web Push) لمنصّة الحلقة الأولى cycle1
--   • c1_push_subs: اشتراك كل جهاز (endpoint) لكل معلّم، وتفضيلاته.
--     لا يقرؤه المتصفح إطلاقاً (RLS بلا سياسات): الدالّة c1-push وحدها بمفتاح الخدمة.
--   • c1_push_call(mode, payload): نداء الدالّة بمفتاح الخدمة من الخزانة (نمط call_agent).
--   • مشغّل على c1_notifications: رسالة الإدارة أو الاستبيان ← إشعار فوري.
--   • جدولة: تذكير صباحي ٦:٣٠ (الأحد–الخميس)، وتذكير مسائي ٧:٣٠ (السبت–الأربعاء) بتوقيت مسقط.
-- متعادلة (idempotent).
-- ════════════════════════════════════════════════════════════════════
create extension if not exists pg_cron;
create extension if not exists pg_net;

create table if not exists public.c1_push_subs (
  endpoint   text primary key,
  user_id    uuid not null,
  sub        jsonb not null,
  prefs      jsonb not null default '{"msgs":true,"morning":true,"evening":true}'::jsonb,
  ua         text,
  created_at timestamptz not null default now(),
  last_ok    timestamptz
);
create index if not exists idx_c1_push_subs_user on public.c1_push_subs(user_id);
alter table public.c1_push_subs enable row level security;
revoke all on public.c1_push_subs from anon, authenticated;

create or replace function public.c1_push_call(p_mode text, p_payload jsonb default '{}'::jsonb)
returns void
language plpgsql
security definer
set search_path = public, extensions, vault
as $$
declare v_key text;
begin
  select decrypted_secret into v_key from vault.decrypted_secrets where name = 'service_role_key';
  if v_key is null then raise warning 'c1_push_call: مفتاح الخدمة غير موجود في الخزانة'; return; end if;
  perform net.http_post(
    url     := 'https://mkdsnnfkkdwdkywnwnjh.supabase.co/functions/v1/c1-push',
    headers := jsonb_build_object('Content-Type','application/json','Authorization','Bearer ' || v_key),
    body    := jsonb_build_object('mode', p_mode) || coalesce(p_payload, '{}'::jsonb),
    timeout_milliseconds := 20000
  );
exception when others then
  raise warning 'c1_push_call(%) فشل: %', p_mode, sqlerrm;
end;
$$;
revoke all on function public.c1_push_call(text, jsonb) from public, anon, authenticated;

-- رسائل الإدارة (بلا ملفٍّ مرفق) والاستبيانات فقط — لا تقييمات المكتبة ولا مشاركاتها
create or replace function public.c1_notif_push_trg()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  if new.user_id is not null and (new.kind = 'survey' or (coalesce(new.kind,'info') = 'info' and new.item_id is null)) then
    perform public.c1_push_call('notif', jsonb_build_object('id', new.id));
  end if;
  return new;
end;
$$;
revoke all on function public.c1_notif_push_trg() from public, anon, authenticated;

drop trigger if exists c1_notif_push on public.c1_notifications;
create trigger c1_notif_push after insert on public.c1_notifications
  for each row execute function public.c1_notif_push_trg();

-- الجدولة بتوقيت UTC (مسقط = UTC+4): ٦:٣٠ص = ٢:٣٠ UTC، و٧:٣٠م = ١٥:٣٠ UTC
do $$ begin
  perform cron.unschedule(jobname) from cron.job where jobname in ('c1-push-morning','c1-push-evening');
end $$;
select cron.schedule('c1-push-morning', '30 2 * * 0-4', $$select public.c1_push_call('morning')$$);
select cron.schedule('c1-push-evening', '30 15 * * 6,0,1,2,3', $$select public.c1_push_call('evening')$$);
