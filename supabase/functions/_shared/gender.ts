// صيغة مخاطبة المعلّم في رسائل الخادم (بريد، تلجرام، واتساب).
// المصدر بالترتيب: اختياره (في الملف أو في التسجيل) ← مرحلته: معلّمات الحلقة
// الأولى نساءٌ كلّهنّ فالمؤنّث، وغيرها المذكّر وهو العامّ في العربية.
export type Gender = "m" | "f";
export function teacherGender(gender?: string | null, stage?: string | null): Gender {
  if (gender === "m" || gender === "f") return gender;
  return stage === "cycle1" ? "f" : "m";
}
// g("اضغطي", "اضغط") — مثل khG في الواجهة
export const genderPick = (g: Gender) => (fem: string, masc: string) => (g === "f" ? fem : masc);
