-- تصحيح: المعلمون العاديون لا يستطيعون قراءة قائمة المدارس (للقائمة المنسدلة عند الإعداد)
-- لأن سياسة schools select كانت للأدمن فقط.
-- نسمح للمعلمين المسجّلين بقراءة id/name فقط (عمودياً) عبر الجدول مباشرة،
-- وننقل قائمة المدارس الكاملة التي تحتاجها لوحة الأدمن (id,name,username,structure,created_at,created_by)
-- إلى دالة RPC آمنة بدلاً من القراءة المباشرة، لأن صلاحيات الأعمدة (column grants) لا يمكن أن تختلف
-- حسب السياسة (policy)، فلا يمكن منح "كل الأعمدة للأدمن، عمودين فقط للمعلم" على نفس الجدول مباشرة.

revoke select on schools from authenticated;
grant select (id, name) on schools to authenticated;

drop policy if exists schools_authenticated_basic_select on schools;
create policy schools_authenticated_basic_select on schools
  for select to authenticated using (true);

create or replace function admin_list_schools()
returns table(id bigint, name text, username text, structure jsonb, created_at timestamptz, created_by text)
language plpgsql security definer set search_path = public as $$
begin
  if not is_app_admin() then
    raise exception 'forbidden';
  end if;
  return query
    select s.id, s.name, s.username, s.structure, s.created_at, s.created_by
    from schools s order by s.created_at desc;
end; $$;

grant execute on function admin_list_schools() to authenticated;

notify pgrst, 'reload schema';
