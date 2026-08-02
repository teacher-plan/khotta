// ════════════════════════════════════════════════════════════════
// Edge Function: request-password-reset
//
// «نسيت كلمة المرور؟» في شاشة الدخول كان ينادي resetPasswordForEmail من
// المتصفّح مباشرةً. وسوبابيز لا يعرف شيئاً عن حلقاتنا، فكان يرسل الرابط إلى:
//   • حساب المشرف — وهو يدخل بـ Google ولا كلمة مرور له. الرابط لا «يعيد»
//     كلمةً بل يُنشئ واحدة، أي يفتح للحساب الإداري باب دخولٍ ثانياً لم يكن.
//   • معلّمة الحلقة الأخرى — تضع كلمتها ثم تُقذف برسالة «هذا حساب الحلقة
//     الثانية»، فتظنّ الاستعادة فشلت وقد نجحت.
//
// والفحص لا يصحّ في المتصفّح: allowed_emails مغلقٌ على غير المسجَّلين، وأيّ
// فحصٍ يظهر أثره يكشف من عنده حسابٌ في المنصّة — وهو ما تجنّبناه عمداً.
//
// النشر: supabase functions deploy request-password-reset
// ════════════════════════════════════════════════════════════════
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const cors = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

function json(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}

// المشرف يدخل بـ Google. لا كلمة مرور له، ولا يجوز أن تُصنع له واحدة من
// صفحةٍ عامّة يفتحها أيّ أحد.
const ADMIN_EMAIL = "teacherplane2026project@gmail.com";

// وجهة العودة تُحسَب هنا لا تُؤخذ من الطلب: رابط الاستعادة يحمل رمز جلسة،
// فلو قَبِلنا وجهةً من المتصفّح لأمكن توجيهه إلى موقعٍ غريب يلتقط الرمز
// ويملك الحساب. الخيارات مغلقةٌ في قائمةٍ نعرفها.
const REDIRECT: Record<string, string> = {
  cycle1: "https://khotati.com/cycle1.html",
  main: "https://khotati.com/",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: cors });

  // الردّ واحدٌ مهما كان الجواب — لا يفرّق بين بريدٍ مسجَّل وغيره، ولا بين
  // حلقةٍ وأخرى. أيُّ فرقٍ في الردّ يجعل الصفحة أداةً لمعرفة من عنده حساب.
  const same = () => json({ ok: true });

  try {
    const b = await req.json().catch(() => ({}));
    const email = String(b.email || "").trim().toLowerCase();
    const cycle = b.cycle === "cycle1" ? "cycle1" : "main";

    if (!/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email)) return same();
    if (email === ADMIN_EMAIL) {
      console.warn("طلب استعادة لحساب المشرف — رُفض");
      return same();
    }

    const admin = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
    );

    // ilike لا eq: البريد يُخزَّن كما كُتب وقد يختلف في حالة الأحرف، وbريدٌ
    // موجودٌ يُقرأ غائباً يترك المعلّمة بلا استعادةٍ بلا سببٍ ظاهر.
    const { data: row, error } = await admin.from("allowed_emails")
      .select("email,cycle").ilike("email", email).maybeSingle();
    if (error) {
      console.error("تعذّرت قراءة allowed_emails:", error.message);
      return same();
    }
    if (!row) return same();                       // غير مصرَّح له أصلاً
    if ((row.cycle || "main") !== cycle) {
      console.warn(`طلب استعادة من حلقة ${cycle} لحسابٍ في ${row.cycle}`);
      return same();                               // الحلقة الأخرى
    }

    // نمرّ بعميل anon لا بمفتاح الخدمة: هذا المسار هو الذي يرسل رسالة سوبابيز
    // بالقالب العربي المضبوط في اللوحة. ومفتاح الخدمة لا يرسل شيئاً.
    const anon = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
    );
    const { error: sendErr } = await anon.auth.resetPasswordForEmail(email, {
      redirectTo: REDIRECT[cycle],
    });
    // حتى الفشل يُبتلع في الردّ: رسالةُ خطأٍ هنا تُخبر السائل أنّ البريد
    // موجود. نسجّله في السجلّ لنراه نحن.
    if (sendErr) console.error("فشل إرسال الاستعادة:", sendErr.message);

    return same();
  } catch (e) {
    console.error("request-password-reset:", String(e));
    return same();
  }
});
