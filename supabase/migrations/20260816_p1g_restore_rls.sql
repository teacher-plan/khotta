-- إعادة تفعيل RLS فوراً بعد التشخيص المؤقت، وإعادة سياسة الإدراج إلى
-- شرطها الصحيح (لا true — كان ذلك للعزل فقط).
ALTER TABLE public.pre_registrations ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS pre_reg_public_insert ON public.pre_registrations;
CREATE POLICY pre_reg_public_insert ON public.pre_registrations
  FOR INSERT TO anon
  WITH CHECK (
    account_email IS NULL
    AND (payment_status IS NULL OR payment_status = 'pending')
    AND notified_at IS NULL
    AND welcomed_at IS NULL
  );

NOTIFY pgrst, 'reload schema';
