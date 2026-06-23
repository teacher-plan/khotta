-- ════════════════════════════════════════════════════════════════
-- خطتي الفصلية — تفعيل حماية شاملة لقاعدة البيانات (RLS)
-- شغّل هذا الملف كاملاً مرة واحدة من: Supabase Dashboard > SQL Editor
-- ════════════════════════════════════════════════════════════════

create extension if not exists pgcrypto;

-- ── 1) تشفير كلمات مرور المدارس وحذف العمود النصي الصريح ──
alter table schools add column if not exists password_hash text;
update schools set password_hash = crypt(password, gen_salt('bf'))
  where password_hash is null and password is not null;
alter table schools drop column if exists password;

-- ── 2) جدول جلسات لوحة المدرسة (admin.html) — يحل محل تخزين id الخام في localStorage ──
create table if not exists school_sessions (
  id uuid primary key default gen_random_uuid(),
  school_id bigint not null references schools(id) on delete cascade,
  token uuid not null unique default gen_random_uuid(),
  created_at timestamptz not null default now(),
  expires_at timestamptz not null default now() + interval '60 days'
);
alter table school_sessions enable row level security;
-- لا توجد أي سياسة هنا عمداً: الوصول فقط عبر الدوال (security definer) أدناه

-- ── 3) دوال آمنة على مستوى القاعدة (تتجاوز RLS بأمان لأنها security definer) ──

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

create or replace function school_session_restore(p_token uuid)
returns table(id bigint, name text, username text, structure jsonb)
language plpgsql security definer set search_path = public as $$
begin
  return query
    select s.id, s.name, s.username, s.structure
    from schools s join school_sessions ss on ss.school_id = s.id
    where ss.token = p_token and ss.expires_at > now();
end; $$;

create or replace function school_logout(p_token uuid)
returns void language sql security definer set search_path = public as $$
  delete from school_sessions where token = p_token;
$$;

create or replace function school_get_violations(p_token uuid)
returns setof violations
language sql security definer set search_path = public as $$
  select v.* from violations v
  join school_sessions ss on ss.school_id = v.school_id
  where ss.token = p_token and ss.expires_at > now()
  order by v.created_at desc;
$$;

create or replace function admin_create_school(p_name text, p_username text, p_password text, p_structure jsonb)
returns table(id bigint, name text, username text)
language plpgsql security definer set search_path = public as $$
begin
  if lower(coalesce(auth.jwt()->>'email','')) <> 'teacherplane2026project@gmail.com' then
    raise exception 'forbidden';
  end if;
  return query
    insert into schools(name, username, password_hash, structure, created_by)
    values (p_name, lower(p_username), crypt(p_password, gen_salt('bf')), p_structure, auth.jwt()->>'email')
    returning schools.id, schools.name, schools.username;
end; $$;

create or replace function admin_reset_school_password(p_school_id bigint, p_new_password text)
returns void language plpgsql security definer set search_path = public as $$
begin
  if lower(coalesce(auth.jwt()->>'email','')) <> 'teacherplane2026project@gmail.com' then
    raise exception 'forbidden';
  end if;
  update schools set password_hash = crypt(p_new_password, gen_salt('bf')) where id = p_school_id;
end; $$;

revoke all on school_sessions from anon, authenticated;
grant execute on function school_login(text,text) to anon, authenticated;
grant execute on function school_session_restore(uuid) to anon, authenticated;
grant execute on function school_logout(uuid) to anon, authenticated;
grant execute on function school_get_violations(uuid) to anon, authenticated;
grant execute on function admin_create_school(text,text,text,jsonb) to authenticated;
grant execute on function admin_reset_school_password(bigint,text) to authenticated;

-- ── 4) دالة مساعدة لفحص "هل المستخدم الحالي هو الأدمن؟" تُستخدم داخل السياسات ──
create or replace function is_app_admin()
returns boolean language sql stable as $$
  select lower(coalesce(auth.jwt()->>'email','')) = 'teacherplane2026project@gmail.com';
$$;

-- ── 5) تفعيل RLS على جميع الجداول ──
alter table schools enable row level security;
alter table violations enable row level security;
alter table profiles enable row level security;
alter table banned_users enable row level security;
alter table push_subscriptions enable row level security;
alter table survey_responses enable row level security;
alter table surveys enable row level security;
alter table announcements enable row level security;
alter table private_messages enable row level security;
alter table allowed_emails enable row level security;
alter table invites enable row level security;
alter table violation_types enable row level security;
alter table library_links enable row level security;
alter table library_items enable row level security;
alter table subjects enable row level security;
alter table curriculum enable row level security;
alter table grade_templates enable row level security;
alter table pre_registrations enable row level security;
alter table referrers enable row level security;
alter table app_settings enable row level security;

-- ── 6) السياسات (policies) ──

-- schools: لا insert/update مباشر (فقط عبر الدوال أعلاه)؛ select/delete للأدمن المسجّل فعلياً فقط
drop policy if exists schools_admin_select on schools;
create policy schools_admin_select on schools for select to authenticated using (is_app_admin());
drop policy if exists schools_admin_delete on schools;
create policy schools_admin_delete on schools for delete to authenticated using (is_app_admin());

-- المعلمون العاديون يحتاجون قراءة id/name فقط (للقائمة المنسدلة عند الإعداد)
revoke select on schools from authenticated;
grant select (id, name) on schools to authenticated;
drop policy if exists schools_authenticated_basic_select on schools;
create policy schools_authenticated_basic_select on schools for select to authenticated using (true);

-- لوحة الأدمن تحتاج أعمدة أكثر (username, structure...) فلا يمكن منحها عبر صلاحيات الأعمدة
-- (تختلف حسب السياسة)، لذا تُستخدم دالة RPC آمنة بدلاً من القراءة المباشرة
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

-- violations: أي معلّم مسجّل دخول يستطيع تسجيل مخالفة؛ لا قراءة مباشرة (لوحة المدرسة تقرأ عبر RPC)
drop policy if exists violations_insert on violations;
create policy violations_insert on violations for insert to authenticated with check (true);

-- profiles: كل مستخدم يدير بياناته فقط؛ الأدمن يقرأ الكل
drop policy if exists profiles_own on profiles;
create policy profiles_own on profiles for all to authenticated using (auth.uid() = id) with check (auth.uid() = id);
drop policy if exists profiles_admin_select on profiles;
create policy profiles_admin_select on profiles for select to authenticated using (is_app_admin());

-- banned_users: كل مستخدم يفحص حالته فقط؛ الأدمن يدير الكل
drop policy if exists banned_own_select on banned_users;
create policy banned_own_select on banned_users for select to authenticated using (auth.uid() = user_id or is_app_admin());
drop policy if exists banned_admin_write on banned_users;
create policy banned_admin_write on banned_users for all to authenticated using (is_app_admin()) with check (is_app_admin());

-- push_subscriptions: كل مستخدم يدير اشتراكه فقط
drop policy if exists push_own on push_subscriptions;
create policy push_own on push_subscriptions for all to authenticated using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- survey_responses: كل مستخدم يكتب إجابته فقط ويقرأها؛ الأدمن يقرأ الكل
drop policy if exists survey_resp_own on survey_responses;
create policy survey_resp_own on survey_responses for select to authenticated using (auth.uid() = user_id or is_app_admin());
drop policy if exists survey_resp_insert on survey_responses;
create policy survey_resp_insert on survey_responses for insert to authenticated with check (auth.uid() = user_id);
drop policy if exists survey_resp_admin_delete on survey_responses;
create policy survey_resp_admin_delete on survey_responses for delete to authenticated using (is_app_admin());

-- surveys: الجميع يقرأ الاستطلاع النشط؛ الأدمن يدير الكل
drop policy if exists surveys_read on surveys;
create policy surveys_read on surveys for select to authenticated using (true);
drop policy if exists surveys_admin_write on surveys;
create policy surveys_admin_write on surveys for all to authenticated using (is_app_admin()) with check (is_app_admin());

-- announcements: الجميع يقرأ؛ الأدمن يكتب
drop policy if exists ann_read on announcements;
create policy ann_read on announcements for select to authenticated using (true);
drop policy if exists ann_admin_write on announcements;
create policy ann_admin_write on announcements for insert to authenticated with check (is_app_admin());
drop policy if exists ann_admin_delete on announcements;
create policy ann_admin_delete on announcements for delete to authenticated using (is_app_admin());

-- private_messages: المستخدم يقرأ رسائله فقط؛ الأدمن يقرأ ويكتب الكل
drop policy if exists pm_read on private_messages;
create policy pm_read on private_messages for select to authenticated using (auth.uid() = to_user_id or is_app_admin());
drop policy if exists pm_admin_write on private_messages;
create policy pm_admin_write on private_messages for insert to authenticated with check (is_app_admin());
drop policy if exists pm_admin_delete on private_messages;
create policy pm_admin_delete on private_messages for delete to authenticated using (is_app_admin());

-- allowed_emails: كل مستخدم يقرأ/يضيف بريده فقط؛ الأدمن يدير الكل
drop policy if exists allowed_own_select on allowed_emails;
create policy allowed_own_select on allowed_emails for select to authenticated using (lower(email) = lower(auth.jwt()->>'email') or is_app_admin());
drop policy if exists allowed_own_insert on allowed_emails;
create policy allowed_own_insert on allowed_emails for insert to authenticated with check (lower(email) = lower(auth.jwt()->>'email') or is_app_admin());
drop policy if exists allowed_admin_write on allowed_emails;
create policy allowed_admin_write on allowed_emails for all to authenticated using (is_app_admin()) with check (is_app_admin());

-- invites: أي مستخدم مسجّل يقرأ/يستخدم كوداً (للتفعيل عند التسجيل)؛ الإدارة الكاملة للأدمن فقط
drop policy if exists invites_read on invites;
create policy invites_read on invites for select to authenticated using (true);
drop policy if exists invites_redeem on invites;
create policy invites_redeem on invites for update to authenticated
  using (status = 'pending')
  with check (is_app_admin() or (status in ('used','expired') and used_by = auth.jwt()->>'email'));
drop policy if exists invites_admin_write on invites;
create policy invites_admin_write on invites for insert to authenticated with check (is_app_admin());
drop policy if exists invites_admin_delete on invites;
create policy invites_admin_delete on invites for delete to authenticated using (is_app_admin());

-- الجداول المرجعية المشتركة: قراءة عامة للمسجّلين، كتابة للأدمن فقط
drop policy if exists vt_read on violation_types;
create policy vt_read on violation_types for select to authenticated using (true);
drop policy if exists vt_admin_write on violation_types;
create policy vt_admin_write on violation_types for all to authenticated using (is_app_admin()) with check (is_app_admin());

drop policy if exists ll_read on library_links;
create policy ll_read on library_links for select to authenticated using (true);
drop policy if exists ll_admin_write on library_links;
create policy ll_admin_write on library_links for all to authenticated using (is_app_admin()) with check (is_app_admin());

drop policy if exists li_read on library_items;
create policy li_read on library_items for select to authenticated using (true);
drop policy if exists li_admin_write on library_items;
create policy li_admin_write on library_items for all to authenticated using (is_app_admin()) with check (is_app_admin());

drop policy if exists subj_read on subjects;
create policy subj_read on subjects for select to authenticated using (true);
drop policy if exists subj_admin_write on subjects;
create policy subj_admin_write on subjects for all to authenticated using (is_app_admin()) with check (is_app_admin());

drop policy if exists curr_read on curriculum;
create policy curr_read on curriculum for select to authenticated using (true);
drop policy if exists curr_admin_write on curriculum;
create policy curr_admin_write on curriculum for all to authenticated using (is_app_admin()) with check (is_app_admin());

drop policy if exists gt_read on grade_templates;
create policy gt_read on grade_templates for select to authenticated using (true);
drop policy if exists gt_admin_write on grade_templates;
create policy gt_admin_write on grade_templates for all to authenticated using (is_app_admin()) with check (is_app_admin());

-- pre_registrations: أي زائر عام يضيف تسجيلاً (نموذج landing) فقط؛ القراءة/التعديل/الحذف للأدمن المسجّل فقط
drop policy if exists prereg_public_insert on pre_registrations;
create policy prereg_public_insert on pre_registrations for insert to anon, authenticated with check (true);
drop policy if exists prereg_admin_manage on pre_registrations;
create policy prereg_admin_manage on pre_registrations for select to authenticated using (is_app_admin());
drop policy if exists prereg_admin_update on pre_registrations;
create policy prereg_admin_update on pre_registrations for update to authenticated using (is_app_admin()) with check (is_app_admin());
drop policy if exists prereg_admin_delete on pre_registrations;
create policy prereg_admin_delete on pre_registrations for delete to authenticated using (is_app_admin());

-- referrers, app_settings: للأدمن فقط بالكامل
drop policy if exists ref_admin_all on referrers;
create policy ref_admin_all on referrers for all to authenticated using (is_app_admin()) with check (is_app_admin());
drop policy if exists settings_admin_all on app_settings;
create policy settings_admin_all on app_settings for all to authenticated using (is_app_admin()) with check (is_app_admin());

-- ════════════════════════════════════════════════════════════════
-- انتهى. تحقق بعد التشغيل من: تسجيل الدخول العادي، لوحة الأدمن، ولوحة المدرسة (admin.html)
-- ════════════════════════════════════════════════════════════════
