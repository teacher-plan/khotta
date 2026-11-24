-- ══ مراقبة التخزين: Supabase وCloudflare R2 في الصفحة الرئيسية للإدارة ══
-- الهدف (طلب الأستاذ عيسى، ٢٢ نوفمبر): ألّا نقترب من حدود خطة Supabase المجانية
-- (١ غيغابايت ملفات، ٥٠٠ ميغابايت قاعدة بيانات)، والملفات الثقيلة على R2.
--
-- الدوالّ هنا لمفتاح الخدمة وحده (تناديها الدالّة storage-usage بعد التحقّق من
-- أن الطالب مشرف)، فلا تُكشف أسماء ملفات المعلّمين لأي جلسة مستخدم.
-- قراءةٌ صرفة: الحذف لا يتمّ بـSQL أبداً بل عبر واجهة Storage نفسها.

-- ① ملخّص الاستهلاك: حجم القاعدة، وكل باكِت، وأثقل المجلّدات
create or replace function public.admin_storage_usage()
returns jsonb
language sql
stable
security definer
set search_path = ''
as $$
  select jsonb_build_object(
    'db_bytes', pg_database_size(current_database()),
    'buckets', coalesce((
      select jsonb_agg(b order by (b->>'bytes')::bigint desc) from (
        select jsonb_build_object(
          'bucket', o.bucket_id,
          'objects', count(*),
          'bytes', coalesce(sum((o.metadata->>'size')::bigint), 0)
        ) b
        from storage.objects o group by o.bucket_id
      ) x), '[]'::jsonb),
    'folders', coalesce((
      select jsonb_agg(f order by (f->>'bytes')::bigint desc) from (
        select jsonb_build_object(
          'bucket', o.bucket_id,
          'folder', split_part(o.name, '/', 1),
          'objects', count(*),
          'bytes', coalesce(sum((o.metadata->>'size')::bigint), 0)
        ) f
        from storage.objects o group by o.bucket_id, split_part(o.name, '/', 1)
        order by coalesce(sum((o.metadata->>'size')::bigint), 0) desc
        limit 15
      ) y), '[]'::jsonb)
  );
$$;

-- ② قائمة الملفات تحت مجلّد (صفحاتٌ متتالية بالاسم) — لمقارنتها بنسخ R2
create or replace function public.admin_storage_list(p_bucket text, p_prefix text, p_after text default '', p_limit int default 1000)
returns table(name text, bytes bigint)
language sql
stable
security definer
set search_path = ''
as $$
  select o.name, coalesce((o.metadata->>'size')::bigint, 0)
  from storage.objects o
  where o.bucket_id = p_bucket
    and o.name like p_prefix || '%'
    and o.name > coalesce(p_after, '')
  order by o.name
  limit least(greatest(p_limit, 1), 5000);
$$;

revoke all on function public.admin_storage_usage() from public, anon, authenticated;
revoke all on function public.admin_storage_list(text, text, text, int) from public, anon, authenticated;
grant execute on function public.admin_storage_usage() to service_role;
grant execute on function public.admin_storage_list(text, text, text, int) to service_role;

-- ③ لقطات الاستهلاك: آخر قياس يُعرض فوراً، ويُعاد القياس كل ساعة على الأكثر
--    (عدّ ملفات R2 يستهلك عمليات قائمة — مجانية حتى مليون شهرياً — فلا نكرّره لكل زيارة)
create table if not exists public.storage_usage_snapshots (
  id bigint generated always as identity primary key,
  taken_at timestamptz not null default now(),
  data jsonb not null
);
create index if not exists storage_usage_snapshots_taken_at_idx on public.storage_usage_snapshots (taken_at desc);
alter table public.storage_usage_snapshots enable row level security;
revoke all on public.storage_usage_snapshots from anon, authenticated;
grant all on public.storage_usage_snapshots to service_role;

comment on table public.storage_usage_snapshots is
  'لقطات استهلاك التخزين (Supabase + R2) تكتبها الدالّة storage-usage وتقرؤها وحدها — بلا وصول لأي جلسة مستخدم.';
