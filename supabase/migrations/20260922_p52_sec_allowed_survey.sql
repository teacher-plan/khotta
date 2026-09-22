-- ════════════════════════════════════════════════════════════════════
-- P52 — سدّ ثغرتين أمنيّتين كشفهما تدقيقٌ على القاعدة الحيّة.
--
-- ملاحظة منهجية: السياسات الحيّة لم تكن مطابقةً لملفات الهجرة. فحصُ
-- pg_policies أظهر سياسةَ إدراجٍ ثانية («anyone add own email») لا أثر
-- لها في أي ملفٍ هنا. فإسقاط المعروفة وحدها كان سيترك البابَ مفتوحاً —
-- في Postgres تكفي سياسةٌ واحدة مطابِقة ليمرّ الإدراج.
-- ════════════════════════════════════════════════════════════════════

-- ── ١) allowed_emails: منع المعلّم من منح نفسه وصولاً ──
--
-- العطل: المفتاح الأساسي (email text) حسّاسٌ لحالة الأحرف، وسياسة
-- الإدراج تقارن بـlower(). فمن بريدها teacher@x.com تُدرج Teacher@X.com:
-- السياسة تمرّ والمفتاح لا يتصادم، والصفّ الجديد expires_at = NULL أي
-- صلاحيةٌ أبدية. وأثرٌ جانبيّ أسوأ: فحصُ الحصّة في quota.ts يقرأ
-- بـmaybeSingle()، ومع صفّين يعيد خطأً فتصير acc = null فيُتخطّى فحصُ
-- انتهاء الاشتراك كلّياً — أي أن الحركة نفسها تُبطل الحارس الموضوع لها.
--
-- لماذا الإسقاط آمن: سياسة allowed_admin_write نوعها ALL وقيدها
-- is_app_admin() على الطرفين، فهي تغطّي إدراج المشرف من لوحة الإدارة
-- (manager.html يُدرج من جلسة المشرف). و activate-teacher يعمل بمفتاح
-- الخدمة فيتجاوز RLS أصلاً. فلا مسار إدراجٍ حيّ يعتمد على المُسقَطتين.
drop policy if exists "allowed_own_insert"   on public.allowed_emails;
drop policy if exists "anyone add own email" on public.allowed_emails;

-- حارسٌ بنيويّ لا يعتمد على صياغة السياسات: لا صفّان ببريدٍ واحد مهما
-- اختلفت حالة أحرفه. يُنشأ بعد التأكّد من خلوّ الجدول من التكرارات
-- (فُحص: لا تكرارات)، فلا يفشل الإنشاء.
create unique index if not exists allowed_emails_email_ci
  on public.allowed_emails (lower(email));

-- ── ٢) الاستبيانات: إخفاء من صوّت بماذا ──
--
-- العطل: c1srvr_read_all قيدها true — فأي معلّمة تقرأ الجدول كاملاً
-- وترى هوية كل مصوِّتة في كل استبيانات الإدارة. والاستبيان يُقدَّم
-- للمعلّمة على أنه رأيٌ يُدلى به، لا تصويتٌ معلن.
--
-- الواجهة تحتاج ثلاثة أشياء فقط: مجموع الأصوات، وعددها لكل خيار،
-- وصوتي أنا. لا تحتاج هويةَ أحد. فتُعطى الأعداد من دالّة تجميعٍ
-- security definer، ويبقى وصولها المباشر محصوراً بصفّها.
create or replace function public.c1_survey_tallies(p_survey_ids uuid[])
returns table(survey_id uuid, option_index int, cnt bigint)
language sql
security definer
set search_path = public
stable
as $$
  select r.survey_id, r.option_index, count(*)::bigint
  from public.c1_survey_responses r
  where r.survey_id = any(p_survey_ids)
  group by r.survey_id, r.option_index;
$$;

revoke all on function public.c1_survey_tallies(uuid[]) from public, anon;
grant execute on function public.c1_survey_tallies(uuid[]) to authenticated;

comment on function public.c1_survey_tallies(uuid[]) is
  'أعدادُ الأصوات لكل خيار بلا هويّة المصوِّتين — بديلُ قراءة الجدول كاملاً.';

-- ملاحظة: تضييق c1srvr_read_all مؤجَّلٌ إلى هجرةٍ تالية (p53) تُطبَّق
-- بعد وصول الواجهة المحدَّثة إلى المستخدمين. لو ضُيّقت الآن لرأت
-- المعلّمات صفراً في كل استبيان حتى يُنشر الكود الجديد.

-- ════════════ التحقّق ════════════
-- سياسات الإدراج الباقية على allowed_emails (يجب أن تبقى الإدارية فقط):
--   select policyname, cmd from pg_policies
--   where tablename='allowed_emails' and cmd in ('INSERT','ALL');
