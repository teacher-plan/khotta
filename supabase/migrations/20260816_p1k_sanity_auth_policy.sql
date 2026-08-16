DROP POLICY IF EXISTS sanity_insert_auth ON public._audit_sanity;
CREATE POLICY sanity_insert_auth ON public._audit_sanity FOR INSERT TO authenticated WITH CHECK (true);
GRANT INSERT ON public._audit_sanity TO authenticated;
GRANT USAGE ON SEQUENCE public._audit_sanity_id_seq TO authenticated;
