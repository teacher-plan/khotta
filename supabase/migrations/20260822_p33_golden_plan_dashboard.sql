-- ════════════════════════════════════════════════════════════════════
-- P33 — لوحة "متابعة الخطة الذهبية": إحصائياتٌ فعلية بدل تصفّحٍ يدوي
--
-- سجلّ إعادة الاستخدام: shAdopt في الواجهة تتبنّى نسخةً من c1_shared_assets
-- دون أن تترك أثراً — فلا نعرف كم مرّة استُخدمت الخطة الذهبية فعلاً، ولا
-- المبلغ الذي وفّرته. هذا الجدول يُسجَّل إليه سطرٌ عند كل تبنٍّ فقط (لا عند
-- كل توليدٍ جديد)، فمجموعه = عدد المرّات التي غنينا فيها عن نداء ذكاءٍ
-- اصطناعي. القراءة للمشرف وحده — رقم "التوفير" ليس شأن المعلّمة.
create table if not exists public.c1_golden_reuses (
  id uuid primary key default gen_random_uuid(),
  kind text not null check (kind in ('prep','info','slides','game')),
  source_asset_id uuid references public.c1_shared_assets(id) on delete set null,
  lesson_id text not null,
  grade text not null,
  subject text not null,
  lesson text not null,
  reused_by uuid not null default auth.uid(),
  created_at timestamptz not null default now()
);
create index if not exists cgr_kind_created on public.c1_golden_reuses(kind, created_at desc);
create index if not exists cgr_lesson on public.c1_golden_reuses(lesson_id);

alter table public.c1_golden_reuses enable row level security;
drop policy if exists "cgr_insert_own" on public.c1_golden_reuses;
create policy "cgr_insert_own" on public.c1_golden_reuses
  for insert to authenticated with check (reused_by = auth.uid());
drop policy if exists "cgr_admin_select" on public.c1_golden_reuses;
create policy "cgr_admin_select" on public.c1_golden_reuses
  for select to authenticated using (is_app_admin());

-- عتبة عدد النسخ قبل إعادة الاستخدام (SH_VARIANTS في الواجهة، كانت ثابتةً
-- ٣ في الكود) تصير قابلةً للتعديل من لوحة الإدارة — مفتاحان جديدان في
-- ai_settings. يلزم توسعة القائمة البيضاء لقراءة العميل (20260816_p0) وإلا
-- رفضت RLS قراءتهما من صفحة المعلّمة رغم كتابتهما من لوحة الإدارة بنجاح.
drop policy if exists "ai_settings_client_read" on public.ai_settings;
create policy "ai_settings_client_read" on public.ai_settings
  for select to anon, authenticated
  using (key in ('quota_text','quota_img','quota_search','c1_tt_defaults','game_cfg',
                 'sh_variants_info','sh_variants_prep'));
