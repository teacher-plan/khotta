DO $$
DECLARE v jsonb;
BEGIN
  SELECT jsonb_agg(jsonb_build_object('lesson_id',lesson_id,'kind',kind,'grade',grade,'subject',subject,'user_id',user_id))
  INTO v
  FROM public.c1_shared_assets
  WHERE lesson_id IN (
    'L1w8ola','L24213l','L5ktecc','L97cjro','Lamvrdy','Lfdrjav','Lfw2fkm','Lggac16','Lgiov9a',
    'Lhg7uj7','Lhn7259','Ljadmue','Lqlhul3','Lshetcl','Ltqs9fz','Lvagzhv','Lyr3106',
    'L150mkmy','L199nkpd','L1k969n6','L1q9llev','L1tuypas','L1ty92df','L1v4acyy'
  );
  RAISE EXCEPTION 'PROBE_SHARED | %', COALESCE(v::text,'NULL');
END $$;
