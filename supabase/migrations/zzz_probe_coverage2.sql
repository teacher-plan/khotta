DO $$
DECLARE r record; s text := '';
BEGIN
  FOR r IN
    WITH cur AS (
      SELECT grade, subject, semester, count(*) total
      FROM curriculum GROUP BY grade, subject, semester
    ),
    tm AS (
      SELECT g.id, g.grade, g.subject, g.semester, g.status, g.page_count,
        (SELECT count(DISTINCT (e->>'matched_curriculum_id'))
         FROM jsonb_array_elements(coalesce(g.toc,'[]'::jsonb)) e
         WHERE e->>'matched_curriculum_id' IS NOT NULL AND e->>'matched_curriculum_id' <> 'null'
        ) AS matched,
        coalesce(jsonb_array_length(g.toc),0) as toc_len
      FROM teacher_guides g
    )
    SELECT t.subject, t.grade, t.status, c.total, t.matched, t.toc_len,
           (c.total - t.matched) as missing
    FROM tm t JOIN cur c ON c.grade=t.grade AND c.subject=t.subject AND c.semester=t.semester
    ORDER BY missing DESC
  LOOP
    s := s || format('%s/g%s: st=%s total=%s matched=%s toc=%s missing=%s | ',
                      r.subject, r.grade, r.status, r.total, r.matched, r.toc_len, r.missing);
  END LOOP;
  RAISE EXCEPTION 'DATA=%', s;
END $$;
