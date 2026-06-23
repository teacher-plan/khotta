-- تصحيح: عمود username في الجدول schools يتعارض مع عمود الإخراج username في returns table
-- مما يسبب الخطأ: column reference "username" is ambiguous (42702)

create or replace function school_login(p_username text, p_password text)
returns table(id bigint, name text, username text, structure jsonb, token uuid)
language plpgsql security definer set search_path = public, extensions as $$
declare v_row schools%rowtype; v_token uuid;
begin
  select * into v_row from schools s where lower(s.username) = lower(p_username) limit 1;
  if v_row.id is null or v_row.password_hash is null
     or crypt(p_password, v_row.password_hash) <> v_row.password_hash then
    return;
  end if;
  insert into school_sessions(school_id) values (v_row.id) returning school_sessions.token into v_token;
  return query select v_row.id, v_row.name, v_row.username, v_row.structure, v_token;
end; $$;

notify pgrst, 'reload schema';
