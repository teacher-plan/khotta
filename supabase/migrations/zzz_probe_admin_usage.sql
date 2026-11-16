-- مؤقّت: إحصاءاتٌ مجمّعة (أعداد فقط) لمراجعة صفحة الإدارة. يُحذف بعد التشغيل.
do $$
declare r jsonb;
  function_exists boolean;
begin
  select jsonb_build_object(
    'allowed_by_cycle',(select jsonb_object_agg(coalesce(cycle,'null'),n) from (select cycle,count(*) n from allowed_emails group by cycle) x),
    'c1_profiles',(select count(*) from cycle1_profiles),
    'c1_active_7d',(select count(*) from cycle1_profiles where updated_at>now()-interval '7 days'),
    'c1_active_30d',(select count(*) from cycle1_profiles where updated_at>now()-interval '30 days'),
    'profiles',(select count(*) from profiles),
    'profiles_active_30d',(select count(*) from profiles where updated_at>now()-interval '30 days'),
    'announcements_90d',(select count(*) from announcements where created_at>now()-interval '90 days'),
    'surveys_90d',(select count(*) from surveys where created_at>now()-interval '90 days'),
    'survey_resp_90d',(select count(*) from survey_responses where created_at>now()-interval '90 days'),
    'c1_messages_90d',(select count(*) from c1_messages where created_at>now()-interval '90 days'),
    'c1_surveys_90d',(select count(*) from c1_surveys where created_at>now()-interval '90 days'),
    'private_messages_90d',(select count(*) from private_messages where created_at>now()-interval '90 days'),
    'library_files_90d',(select count(*) from library_files where created_at>now()-interval '90 days'),
    'schools_c2',(select count(*) from schools),
    'c1_schools',(select count(*) from c1_schools),
    'referrers',(select count(*) from referrers),
    'testimonials',(select count(*) from testimonials),
    'pre_reg_90d',(select count(*) from pre_registrations where created_at>now()-interval '90 days'),
    'grade_templates',(select count(*) from grade_templates),
    'lesson_prep_gen_30d',(select count(*) from lesson_prep_generations where created_at>now()-interval '30 days'),
    'c1_prep_jobs',(select count(*) from c1_prep_jobs),
    'ai_cost_30d',(select round(coalesce(sum(cost_usd),0)::numeric,2) from ai_cost_log where created_at>now()-interval '30 days'),
    'violation_types',(select count(*) from violation_types),
    'c1_suggestions_90d',(select count(*) from c1_suggestions where created_at>now()-interval '90 days'),
    'page_views_30d',(select count(*) from page_views where created_at>now()-interval '30 days')
  ) into r;
  raise exception 'PROBE %', r;
end $$;
