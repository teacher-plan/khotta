-- ٢٧ نوفمبر (الفحص الشامل): لوحة الإدارة تقرأ ai_cost_log مباشرةً، والجدول
-- مُغلَق عن authenticated منذ 20260816 (REVOKE ALL) — فكانت بطاقات «التحاضير
-- هذا الأسبوع» و«تكلفة الذكاء الاصطناعي» و«التوفير بإعادة الاستخدام» تفشل
-- بصمت (403). هذه دالةٌ للمشرف وحده تُرجع ملخّصاً مجمّعاً، ويبقى الجدول مغلقاً.
create or replace function public.admin_ai_cost_summary(p_since timestamptz default '-infinity')
returns table(function_name text, n bigint, n_costed bigint, total_usd numeric, avg_usd numeric)
language plpgsql stable security definer set search_path = public as $$
begin
  if not public.is_app_admin() then raise exception 'forbidden'; end if;
  return query
    select l.function_name::text, count(*)::bigint, count(l.cost_usd)::bigint,
           coalesce(sum(l.cost_usd),0)::numeric, avg(l.cost_usd)::numeric
    from public.ai_cost_log l
    where l.created_at >= p_since
    group by l.function_name;
end $$;
revoke all on function public.admin_ai_cost_summary(timestamptz) from public, anon;
grant execute on function public.admin_ai_cost_summary(timestamptz) to authenticated;
