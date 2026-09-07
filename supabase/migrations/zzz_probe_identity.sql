DO $$
DECLARE r record; s text := '';
BEGIN
  FOR r IN SELECT grade, subject, base_path, page_count, status, offset_pages, indexed_at
           FROM teacher_guides WHERE subject = 'الهوية والمواطنة' ORDER BY grade
  LOOP
    s := s || format('grade=%s page_count=%s status=%s offset=%s base=%s | ',
                      r.grade, r.page_count, r.status, r.offset_pages, r.base_path);
  END LOOP;
  RAISE EXCEPTION 'DATA=%', s;
END $$;
