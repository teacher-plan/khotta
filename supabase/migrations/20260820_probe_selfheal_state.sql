-- probe: حالة منظومة الإصلاح الذاتي الحقيقية قبل بناء Shadow-Live (يتراجع عن نفسه)
do $$
declare v_pb text; declare v_ag text; declare v_inc text; declare v_diag text; declare v_reg text;
begin
  select string_agg(playbook_id||'|mode='||mode||'|enabled='||enabled||'|risk='||risk_level||'|pattern='||incident_pattern||'|actions='||allowed_actions::text, e'\n') into v_pb from repair_playbooks;
  select string_agg(agent_id||'|type='||agent_type||'|autonomy='||autonomy_level||'|perm='||permission_level, e'\n') into v_ag from agent_registry;
  select string_agg(id::text||'|status='||status||'|component='||component||'|first_seen='||first_seen_at::text, e'\n' order by first_seen_at desc) into v_inc from (select * from ops_incidents order by first_seen_at desc limit 10) t;
  select string_agg(diagnosis_id::text||'|status='||diagnosis_status||'|conf='||confidence||'|incident='||incident_id::text, e'\n' order by created_at desc) into v_diag from (select * from ops_diagnoses order by created_at desc limit 10) t;
  select string_agg(action_id||'|enabled='||enabled||'|risk='||risk_level||'|verify='||coalesce(verification_strategy,'-'), e'\n') into v_reg from safe_action_registry;
  raise exception 'PROBE | PLAYBOOKS=[%] | AGENTS=[%] | INCIDENTS=[%] | DIAGNOSES=[%] | ACTIONS=[%]',
    coalesce(v_pb,'NONE'), coalesce(v_ag,'NONE'), coalesce(v_inc,'NONE'), coalesce(v_diag,'NONE'), coalesce(v_reg,'NONE');
end $$;
