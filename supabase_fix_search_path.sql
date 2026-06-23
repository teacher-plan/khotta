-- تصحيح: pgcrypto مثبّتة في مخطط extensions لا public على Supabase
-- يضيف extensions لمسار البحث في الدوال التي تستخدم gen_salt/crypt

alter function school_login(text, text) set search_path = public, extensions;
alter function admin_create_school(text, text, text, jsonb) set search_path = public, extensions;
alter function admin_reset_school_password(bigint, text) set search_path = public, extensions;

notify pgrst, 'reload schema';
