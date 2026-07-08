-- الخطة الذهبية: مخزن التحضير المشترك — أول معلم يولّد، والبقية يستوردون مجاناً
create table if not exists shared_preps (
  lesson_id text primary key,
  grade int,
  subject text,
  unit text,
  lesson text,
  plan jsonb not null,
  slides jsonb,
  exam_html text,
  info_b64 text,
  created_by uuid references auth.users(id) on delete set null,
  created_at timestamptz default now()
);

alter table shared_preps enable row level security;

-- كل معلم مسجّل يقرأ، وأول من يولّد يكتب (الصف موجود = لا يُستبدل)
drop policy if exists "shared_read" on shared_preps;
create policy "shared_read" on shared_preps for select using (auth.uid() is not null);

drop policy if exists "shared_insert" on shared_preps;
create policy "shared_insert" on shared_preps for insert with check (auth.uid() is not null);

-- المشرف فقط يحذف/يستبدل محتوى غير مناسب
drop policy if exists "shared_admin_delete" on shared_preps;
create policy "shared_admin_delete" on shared_preps for delete using (is_app_admin());

-- شرائح العرض المرسومة (صور base64) ضمن الحزمة المشتركة
alter table shared_preps add column if not exists slide_imgs jsonb;
