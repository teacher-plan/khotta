-- ════════════════════════════════════════════════════════════════════
-- استثناء معلّمين من رسالةٍ جماعية بعينها (طلب الأستاذ عيسى، ١٧ نوفمبر).
--
-- excluded_user_ids: من لا تصله هذه الرسالة الجماعية وحدها. الاستثناء
-- يُفرَض في القاعدة نفسها (سياسة القراءة) لا في الواجهة فقط، فلا يصل
-- الصفُّ أصلاً إلى تطبيق المعلّم المستثنى.
--
-- إضافيٌّ بحت: العمود جديد بقيمةٍ افتراضية فارغة، فكل الرسائل الحالية
-- (ومشاركات المكتبة library_share) تبقى ظاهرةً كما كانت تماماً.
-- ════════════════════════════════════════════════════════════════════

alter table c1_messages
  add column if not exists excluded_user_ids uuid[] not null default '{}';

drop policy if exists "c1msg_read" on c1_messages;
create policy "c1msg_read" on c1_messages
  for select to authenticated
  using (
    (target_user_id is null and not (auth.uid() = any(excluded_user_ids)))
    or target_user_id = auth.uid()
    or is_app_admin()
  );
