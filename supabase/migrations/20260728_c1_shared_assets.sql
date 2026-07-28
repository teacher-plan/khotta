-- 🎲 مساحة مشتركة للألعاب والملخصات البصرية — الحلقة الأولى
--
-- تشترك معلمات الحلقة الأولى في ما يُجهّزنه، مفهرساً بالصف والمادة والدرس.
-- كل لعبة أو ملخص تُولّده معلمة يُنشر هنا تلقائياً باسمها (shAutoPublish)،
-- ولها إلغاؤه متى شاءت. والأخرى تُعاين ثم تضغط «حفظ» فتنتقل نسخة إلى
-- بطاقة الدرس عندها — والحفظ لا يُعيد النشر، وإلا امتلأ الجدول بمكررات.
--
-- لماذا نُخزّن نسخة (content/image_url) بدل الإشارة إلى صف في games؟
-- لأن games محكومة بسياسة games_own (كل معلمة ترى ألعابها وحدها). لو أشرنا
-- إليها لاضطررنا لثقب تلك السياسة، فينكشف ما وراء المنشور من ألعاب خاصة.
-- النسخة تُبقي ذلك العزل قائماً، وهي أمتن كذلك: حذف المالكة للعبتها
-- الأصلية لا يُعطب نسخ الأخريات.
--
-- lesson_id ثابت عبر المعلمات لأنه مشتق من صفوف المنهج نفسها
-- (stableLessonId في الواجهة)، فالربط ببطاقة الدرس دقيق لا بالاسم.

create table if not exists c1_shared_assets (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid(),
  uploader_name text,
  kind text not null check (kind in ('game','info')),

  -- الفهرسة: صف + مادة + درس
  grade text not null,
  subject text not null,
  unit text,
  lesson text not null,
  lesson_id text not null,

  title text,

  -- عند kind='game': نسخة اللعبة وقت المشاركة
  template text,
  theme_id uuid references game_themes(id) on delete set null,
  content jsonb,

  -- عند kind='info': رابط الصورة داخل مخزن library-files العام
  image_url text,

  created_at timestamptz default now(),

  -- كل نوع يحمل حمولته: لا لعبة بلا محتوى ولا ملخص بلا صورة
  constraint c1sa_payload check (
    (kind = 'game' and content is not null and template is not null)
    or (kind = 'info' and image_url is not null)
  )
);

create index if not exists c1sa_lookup on c1_shared_assets (subject, grade, lesson_id);
create index if not exists c1sa_recent on c1_shared_assets (created_at desc);
-- مشاركة واحدة لكل (معلمة، نوع، درس): إعادة التوليد تُحدّث النسخة لا تُكرّرها.
-- الأعمدة الثلاثة هنا يجب أن تطابق onConflict في shAutoPublish بالواجهة
-- تماماً، وإلا رفض ON CONFLICT العملية.
create unique index if not exists c1sa_once on c1_shared_assets (user_id, kind, lesson_id);

alter table c1_shared_assets enable row level security;

-- القراءة للجميع: هذا هو معنى «مشترك»
drop policy if exists "c1sa_read_all" on c1_shared_assets;
create policy "c1sa_read_all" on c1_shared_assets
  for select to authenticated using (true);

-- الكتابة والحذف للمالكة وحدها
drop policy if exists "c1sa_insert_own" on c1_shared_assets;
create policy "c1sa_insert_own" on c1_shared_assets
  for insert to authenticated with check (user_id = auth.uid());

drop policy if exists "c1sa_update_own" on c1_shared_assets;
create policy "c1sa_update_own" on c1_shared_assets
  for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists "c1sa_delete_own" on c1_shared_assets;
create policy "c1sa_delete_own" on c1_shared_assets
  for delete to authenticated using (user_id = auth.uid());
