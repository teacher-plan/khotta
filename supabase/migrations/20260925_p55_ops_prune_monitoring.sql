-- ════════════════════════════════════════════════════════════════════
-- P55 — تنظيف دوريّ لسجلّات المراقبة المتراكمة.
--
-- الخلفية: جداول تشخيصٍ عابرة تنمو بسرعة من وكلاء المراقبة
-- (health_checks بلغ ١٠٤٬٤٩٣ صفاً، agent_runs ١٣٣١٨، scheduler_runs ١٠٨٥٢).
-- ليست بياناتِ مستخدمين، بل قياساتٌ لحظية غرضها التشخيص القريب. نُبقي نافذةً
-- كافية (١٤ يوماً للتفصيلية، ٣٠ للأخطاء وسعة القاعدة) ونحذف ما قبلها،
-- ونجدول التنظيف يومياً. آمنٌ: يمسّ سجلّات التشخيص وحدها لا جداول المعلّمين.
-- ════════════════════════════════════════════════════════════════════

-- دالّةٌ محميّةٌ بحارس وجود الجدول/العمود (فلا تفشل على نسخةٍ ناقصة)، تحذف
-- الصفوف الأقدم من مدّة كل جدول. security definer لتتجاوز RLS عند الحذف.
create or replace function public.ops_prune_monitoring()
returns void
language plpgsql
security definer
set search_path = public
as $$
declare
  spec_txt text;
  -- الجداول الورقية (لا يشير إليها مفتاحٌ أجنبيّ). db_capacity_history قبل
  -- agent_runs عمداً: الأولى تشير للثانية، فتُقلَّم أولاً. كل حذفٍ معزولٌ
  -- بمعالج استثناء حتى لا يُسقط عطلٌ في جدولٍ تنظيفَ البقية (وأهمّها
  -- health_checks الأضخم).
  specs text[] := array[
    'health_checks:checked_at:14',
    'scheduler_runs:started_at:14',
    'agent_logs:created_at:14',
    'agent_messages:sent_at:14',
    'performance_metrics:timestamp:14',
    'db_capacity_history:measured_at:30',
    'error_logs:occurred_at:30'
  ];
  parts text[];
  tbl text; col text; days text;
begin
  foreach spec_txt in array specs loop
    parts := string_to_array(spec_txt, ':');
    tbl := parts[1]; col := parts[2]; days := parts[3];
    if to_regclass('public.'||quote_ident(tbl)) is not null
       and exists(select 1 from information_schema.columns
                  where table_schema='public' and table_name=tbl and column_name=col) then
      begin
        execute format('delete from public.%I where %I < now() - (%L||'' days'')::interval', tbl, col, days);
      exception when others then
        raise notice 'ops_prune: تُخطّي % (%)', tbl, sqlerrm;
      end;
    end if;
  end loop;

  -- agent_runs يُشار إليه من db_capacity_history: نحذف فقط ما مضى عليه ٣٠ يوماً
  -- وغير المشار إليه (بعد تقليم db_capacity_history أعلاه) — فلا ينتهك المفتاح.
  if to_regclass('public.agent_runs') is not null then
    begin
      delete from public.agent_runs ar
      where ar.started_at < now() - interval '30 days'
        and not exists (select 1 from public.db_capacity_history d where d.run_id = ar.id);
    exception when others then
      raise notice 'ops_prune: تُخطّي agent_runs (%)', sqlerrm;
    end;
  end if;
end $$;

revoke all on function public.ops_prune_monitoring() from public, anon, authenticated;

-- تشغيلةٌ أولى فورية لتقليص التراكم الحالي.
select public.ops_prune_monitoring();

-- جدولةٌ يومية (٠٣:٣٠ بتوقيت UTC). إلغاءٌ سابقٌ آمنٌ إن وُجدت الوظيفة.
do $$
begin
  perform cron.unschedule('ops-prune-monitoring');
exception when others then null;
end $$;
select cron.schedule('ops-prune-monitoring', '30 3 * * *', $$select public.ops_prune_monitoring()$$);
