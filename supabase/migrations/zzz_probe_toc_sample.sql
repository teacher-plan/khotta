DO $$
DECLARE t text; c text;
BEGIN
  SELECT toc::text INTO t FROM teacher_guides WHERE subject='الهوية والمواطنة' AND grade=3;
  SELECT string_agg(id::text || ':' || unit || '—' || lesson, ' | ') INTO c
    FROM curriculum WHERE subject='الهوية والمواطنة' AND grade=3;
  RAISE EXCEPTION 'TOC=% ||| CUR=%', left(t,1500), left(c,1000);
END $$;
