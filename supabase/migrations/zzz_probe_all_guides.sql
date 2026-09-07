DO $$
DECLARE r record; s text := '';
BEGIN
  FOR r IN SELECT grade, subject, page_count, status, offset_pages,
                  coalesce(jsonb_array_length(toc), 0) as toc_len
           FROM teacher_guides ORDER BY subject, grade
  LOOP
    s := s || format('%s/g%s: pc=%s st=%s off=%s toc=%s | ',
                      r.subject, r.grade, r.page_count, r.status, r.offset_pages, r.toc_len);
  END LOOP;
  RAISE EXCEPTION 'DATA=%', s;
END $$;
