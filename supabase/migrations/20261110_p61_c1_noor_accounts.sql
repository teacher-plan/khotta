-- ════════════════════════════════════════════════════════════════
-- P61 — ربط حساب منصّة نور (cycle1): صفٌّ لكل معلّم يحفظ اسم مستخدم نور
-- وكلمة المرور مشفّرةً (AES-GCM في الدالّة c1-noor)، وجلسة نور مشفّرة،
-- ومقرّرات المعلّم وشُعَبه في نور، وإعدادات المطابقة (شعبة خطة ↔ شعبة نور،
-- درس خطة ↔ درس نور)، وذاكرة شجرة الدروس.
-- RLS مفعّلة بلا أي سياسة: لا يقرأ المتصفح هذا الجدول ولا يكتبه أبداً؛
-- الدالّة c1-noor وحدها تصل إليه بمفتاح الخدمة. متعادلة (idempotent).
-- ════════════════════════════════════════════════════════════════
create table if not exists public.c1_noor_accounts (
  user_id    uuid primary key references auth.users(id) on delete cascade,
  username   text not null,
  pass_enc   text not null,
  sess_enc   text,
  sess_at    timestamptz,
  courses    jsonb not null default '[]'::jsonb,
  cfg        jsonb not null default '{}'::jsonb,
  cache      jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.c1_noor_accounts enable row level security;
revoke all on public.c1_noor_accounts from anon, authenticated;
