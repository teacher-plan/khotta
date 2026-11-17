-- ════════════════════════════════════════════════════════════════════
-- تشديد أمني بعد فحص Supabase Advisors (١٧ نوفمبر) — بلا أي تغيير في
-- سلوك المنصّة للمعلّم أو المشرف.
--
-- ١) أصوات الاستبيانات: كانت سياسة القراءة «true» فيستطيع أي معلّمٍ تقنياً
--    قراءة من صوّت لأي خيار. الواجهة لا تحتاج إلا صفّ المعلّم نفسه (والأعداد
--    من الدالّة c1_survey_tallies)، والمشرف يرى الكل.
-- ٢) دوالّ تشغيلٍ داخلية (SECURITY DEFINER) كان يستدعيها أي أحد حتى بلا
--    تسجيل دخول عبر /rest/v1/rpc. يستدعيها فقط: وكيل autonomous-scheduler
--    بمفتاح الخدمة، ومهامّ pg_cron بصفة postgres، ومُشغِّل pre_registrations
--    — وكلّها لا تتأثّر بسحب الصلاحية من anon/authenticated.
-- ٣) تثبيت search_path لثلاث دوالّ (تحذير function_search_path_mutable).
-- ════════════════════════════════════════════════════════════════════

-- ١) أصوات الاستبيانات
drop policy if exists "c1srvr_read_all" on c1_survey_responses;
drop policy if exists "c1srvr_read_own_or_admin" on c1_survey_responses;
create policy "c1srvr_read_own_or_admin" on c1_survey_responses
  for select to authenticated
  using (user_id = auth.uid() or is_app_admin());

-- ٢) دوالّ التشغيل الداخلية
revoke execute on function public.claim_incident_for_repair(uuid, text, text, integer) from public, anon, authenticated;
revoke execute on function public.release_incident_claim(uuid) from public, anon, authenticated;
revoke execute on function public.prune_usage_tracking() from public, anon, authenticated;
revoke execute on function public.notify_new_registration() from public, anon, authenticated;
grant execute on function public.claim_incident_for_repair(uuid, text, text, integer) to service_role;
grant execute on function public.release_incident_claim(uuid) to service_role;
grant execute on function public.prune_usage_tracking() to service_role;

-- ٣) search_path ثابت
alter function public.is_app_admin() set search_path = public;
alter function public.update_grade_templates_timestamp() set search_path = public;
alter function public.shared_preps_lock_filled() set search_path = public;
