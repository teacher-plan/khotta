-- 🎓 مخزن الدروس المشترك — الحلقة الأولى
--
-- معلمات الصف والمادة الواحدة يُدرّسن الدروس نفسها، فلا معنى لأن تُولّد كل
-- واحدة خطة الدرس وملخصه وعرضه من جديد. يُخزَّن ما تُولّده أولاهنّ هنا،
-- وتتبنّاه البقية فوراً بلا استدعاء ذكاء اصطناعي ولا ملف تخزين جديد.
--
-- الخطة والملخص يُجمع لهما ثلاث نسخ لكل درس (SH_VARIANTS في الواجهة): أول
-- ثلاث معلمات تُولّد كل واحدة نسختها، ثم تُعطى البقية واحدة عشوائياً — كي لا
-- يصير اجتهاد الأولى قاعدةً للجميع. والعرض واللعبة نسخة واحدة.
--
-- المكسب على ٥٠ معلمة × ٢٠ درساً، بخمس معلمات للدرس الواحد:
--   استدعاءات AI  ١٠٠٠ لكل نوع  ←  ٢٠٠ للعرض، ٦٠٠ للخطة والملخص
-- ولو وُلّدت الثلاث دفعةً عند الأولى بدل التراكم لكلّف ذلك الدروسَ التي
-- تُدرّسها معلمة واحدة ثلاثة استدعاءات بلا مستفيد، ولأطال انتظارها ثلاثاً.
--
-- أربعة أنواع:
--   prep   خطة الدرس (jsonb)
--   info   الملخص البصري (رابط صورة ثابت لا يُكتب فوقه)
--   slides العرض التقديمي (jsonb)
--   game   اللعبة (jsonb + قالب)
--
-- التبنّي ينسخ الحمولة إلى ملف المعلمة (عدا الصورة فتُشار إشارةً)، فتعديلها
-- على نسختها لا يمسّ أحداً، وحذفها من حسابها لا يحذف الأصل من المخزن.
--
-- لماذا نُخزّن نسخة (content/image_url) بدل الإشارة إلى صف في games؟
-- لأن games محكومة بسياسة games_own (كل معلمة ترى ألعابها وحدها). لو أشرنا
-- إليها لاضطررنا لثقب تلك السياسة، فينكشف ما وراء المنشور من ألعاب خاصة.
--
-- lesson_id ثابت عبر المعلمات لأنه مشتق من صفوف المنهج نفسها
-- (stableLessonId في الواجهة)، فمطابقة الدرس دقيقة لا بالاسم.

create table if not exists c1_shared_assets (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null default auth.uid(),
  uploader_name text,
  kind text not null constraint c1sa_kind check (kind in ('prep','info','slides','game')),

  -- الفهرسة: صف + مادة + درس
  grade text not null,
  subject text not null,
  unit text,
  lesson text not null,
  lesson_id text not null,

  title text,

  -- الحمولة: jsonb لـ prep/slides/game، ورابط صورة لـ info
  template text,                                    -- قالب اللعبة
  theme_id uuid references game_themes(id) on delete set null,
  content jsonb,
  image_url text,                                   -- داخل مخزن library-files العام

  created_at timestamptz default now(),

  -- كل نوع يحمل حمولته: لا خطة ولا عرض بلا محتوى، ولا ملخص بلا صورة،
  -- ولا لعبة بلا محتوى وقالب معاً
  constraint c1sa_payload check (
    (kind in ('prep','slides') and content is not null)
    or (kind = 'info' and image_url is not null)
    or (kind = 'game' and content is not null and template is not null)
  )
);

-- الاستعلام الحارّ: «هل جهّزت زميلة هذا الدرس؟» يُنفَّذ قبل كل توليد
create index if not exists c1sa_pool on c1_shared_assets (lesson_id, kind, created_at desc);
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
