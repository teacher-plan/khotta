DO $$
DECLARE v text;
BEGIN
  SELECT format('public=%s file_size_limit=%s allowed_mime_types=%s',
    public, file_size_limit, allowed_mime_types)
  INTO v FROM storage.buckets WHERE id='user-files';
  RAISE EXCEPTION 'PROBE_BUCKET | %', coalesce(v,'NOT FOUND');
END $$;
