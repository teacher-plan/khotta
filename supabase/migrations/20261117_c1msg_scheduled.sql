-- ════════════════════════════════════════════════════════════════════
-- جدولة رسائل الإدارة (طلب الأستاذ عيسى، ١٧ نوفمبر).
--
-- الرسالة المجدولة تُحفظ بـ created_at = وقت الإرسال المطلوب (في المستقبل).
-- سياسة القراءة تُخفيها عن المعلّمين حتى يحين وقتها، والمشرف يراها دائماً
-- (موسومةً «مجدولة»). فلا عمود جديد ولا مهمّة مجدولة: الترتيب ونافذة الدخول
-- وإيصالات القراءة كلّها تعمل على created_at كما هي.
-- لا يغيّر شيئاً للرسائل الحالية (كلّها created_at في الماضي).
-- ════════════════════════════════════════════════════════════════════

drop policy if exists "c1msg_read" on c1_messages;
create policy "c1msg_read" on c1_messages
  for select to authenticated
  using (
    is_app_admin()
    or (created_at <= now() and (
         (target_user_id is null and not (auth.uid() = any(excluded_user_ids)))
         or target_user_id = auth.uid()
       ))
  );
