-- ══════════════════════════════════════════════════════════════════════
-- استخراج البنية الحقيقية للجداول الأربعة الأساسية
-- ══════════════════════════════════════════════════════════════════════
-- الصقه في: لوحة Supabase ← SQL Editor ← Run
-- ثم انسخ الناتج كاملاً وسلّمه، فيُستبدل به الملف التقديري
-- 00000000_base_tables_reconstructed.sql بالبنية الفعلية.
--
-- الاستعلام للقراءة فقط. لا يُعدّل ولا يحذف شيئاً.
-- ══════════════════════════════════════════════════════════════════════

with t as (
  select unnest(array['curriculum','book_sources','cycle1_profiles','allowed_emails']) as tbl
)

-- ① الأعمدة وأنواعها وقيمها الافتراضية
select
  '① عمود' as البند,
  c.table_name || '.' || c.column_name as الاسم,
  c.data_type
    || coalesce('(' || c.character_maximum_length || ')', '')
    || case when c.is_nullable = 'NO' then ' not null' else '' end
    || coalesce(' default ' || c.column_default, '') as التفاصيل
from information_schema.columns c
join t on t.tbl = c.table_name
where c.table_schema = 'public'

union all

-- ② المفاتيح والقيود الفريدة والأجنبية
select
  '② قيد',
  tc.table_name || ' · ' || tc.constraint_type,
  tc.constraint_name || ' (' || string_agg(kcu.column_name, ', ' order by kcu.ordinal_position) || ')'
from information_schema.table_constraints tc
join information_schema.key_column_usage kcu
  on kcu.constraint_name = tc.constraint_name and kcu.table_schema = tc.table_schema
join t on t.tbl = tc.table_name
where tc.table_schema = 'public'
  and tc.constraint_type in ('PRIMARY KEY','UNIQUE','FOREIGN KEY')
group by tc.table_name, tc.constraint_type, tc.constraint_name

union all

-- ③ قيود التحقّق (check)
select
  '③ تحقّق',
  rel.relname,
  con.conname || ': ' || pg_get_constraintdef(con.oid)
from pg_constraint con
join pg_class rel on rel.oid = con.conrelid
join pg_namespace ns on ns.oid = rel.relnamespace
join t on t.tbl = rel.relname
where ns.nspname = 'public' and con.contype = 'c'

union all

-- ④ الفهارس
select
  '④ فهرس',
  tablename,
  indexdef
from pg_indexes
join t on t.tbl = pg_indexes.tablename
where schemaname = 'public'

union all

-- ⑤ سياسات الصلاحيات
select
  '⑤ صلاحية',
  tablename || ' · ' || cmd,
  policyname
    || ' | using: ' || coalesce(qual, '—')
    || ' | check: ' || coalesce(with_check, '—')
from pg_policies
join t on t.tbl = pg_policies.tablename
where schemaname = 'public'

union all

-- ⑥ هل الحماية مفعّلة؟
select
  '⑥ حماية',
  rel.relname,
  case when rel.relrowsecurity then 'RLS مفعّلة' else '⚠️ RLS معطّلة' end
from pg_class rel
join pg_namespace ns on ns.oid = rel.relnamespace
join t on t.tbl = rel.relname
where ns.nspname = 'public'

union all

-- ⑦ عدد الصفوف (لمعرفة أيّها مستعمل فعلاً)
select '⑦ صفوف', 'curriculum',      count(*)::text from public.curriculum
union all
select '⑦ صفوف', 'book_sources',    count(*)::text from public.book_sources
union all
select '⑦ صفوف', 'cycle1_profiles', count(*)::text from public.cycle1_profiles
union all
select '⑦ صفوف', 'allowed_emails',  count(*)::text from public.allowed_emails

order by 1, 2, 3;
