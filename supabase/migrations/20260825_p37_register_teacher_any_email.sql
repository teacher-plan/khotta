-- بعد إلغاء خاصية درايف، لم يعد التسجيل بحاجة لبريد Gmail تحديداً.
-- استبدال شرط "@gmail.com فقط" بتحقّق عام من صيغة البريد الإلكتروني.
CREATE OR REPLACE FUNCTION public.register_teacher(p_name text, p_phone text, p_email text, p_stage text, p_referred_by text DEFAULT NULL::text)
 RETURNS void
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
DECLARE
  v_email text := lower(trim(p_email));
BEGIN
  IF v_email !~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$' THEN
    RAISE EXCEPTION 'invalid_email_domain';
  END IF;

  IF EXISTS (
    SELECT 1 FROM pre_registrations
    WHERE stage = p_stage AND (phone = p_phone OR lower(email) = v_email)
  ) THEN
    RAISE EXCEPTION 'already_registered';
  END IF;

  INSERT INTO pre_registrations(name, phone, email, stage, referred_by)
  VALUES (p_name, p_phone, v_email, p_stage, p_referred_by);
END;
$function$;
