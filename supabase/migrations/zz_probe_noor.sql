do $$ declare r text; begin
select string_agg(format('%s|%s|%s|%s', u.email, a.username, jsonb_array_length(coalesce(a.courses,'[]'::jsonb)), coalesce((select string_agg(k,',') from jsonb_object_keys(coalesce(a.cfg,'{}'::jsonb)) k),'')), ' ;; ')
 into r from c1_noor_accounts a join auth.users u on u.id=a.user_id;
raise exception 'PROBE>> %', r; end $$;
