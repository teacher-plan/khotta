-- 🎮 قسم الألعاب التعليمية: الثيمات المشتركة + ألعاب المعلمين
-- الثيمات تولَّد مرة واحدة (Nano Banana) وتُخزَّن كأصول عامة يستخدمها الجميع

create table if not exists game_themes (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  emoji text default '🎨',
  bg_url text,                -- خلفية الساحة (من التخزين)
  colors jsonb,               -- {accent,card,ink} ألوان مشتقة من الثيم
  created_by uuid,
  created_at timestamptz default now()
);
alter table game_themes enable row level security;
create policy "themes_read" on game_themes for select to authenticated using (true);
create policy "themes_admin_insert" on game_themes for insert to authenticated with check (is_app_admin());
create policy "themes_admin_delete" on game_themes for delete to authenticated using (is_app_admin());

-- لعبة محفوظة لمعلم: محتوى واحد + قالب مختار (يمكن تبديله لاحقاً)
create table if not exists games (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid(),
  grade text, subject text, unit text, lesson text,
  title text,
  template text not null,      -- wheel | match | quiz
  theme_id uuid references game_themes(id) on delete set null,
  content jsonb not null,      -- {pairs:[[a,b]]} أو {questions:[{q,c,a}]} أو {items:[..]}
  created_at timestamptz default now()
);
alter table games enable row level security;
create policy "games_own" on games for all to authenticated
  using (user_id = auth.uid()) with check (user_id = auth.uid());
