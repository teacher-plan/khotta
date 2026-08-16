// استخراجُ JSON من ردّ نموذجٍ لغويّ — بأمان.
//
// النماذج تُحيط الكائن بنصّ أحياناً، أو بسياج ```json، أو تُقطع الإجابة عند
// حدّ الرموز فيصل نصفُ كائن. والنمطُ الذي كان مستعملاً في ستّ دوال:
//     const m = text.match(/\{[\s\S]*\}/);  parsed = m ? JSON.parse(m[0]) : {…}
// فيه عطلان:
//   ١ الـregex جشعٌ: يلتقط من أول ‏{‏ إلى آخر ‏}‏ في النصّ كلِّه. فلو سبق
//     الكائنَ شرحٌ فيه قوس، أو تلاه، فالمقتطَع ليس كائناً صالحاً.
//   ٢ الـJSON.parse الثاني خارج أيِّ try، فرميُه يهرب إلى المعالج العامّ
//     ويعود ٥٠٠ للمعلّمة بعد أن خُصمت حصّتها.
//
// البديل: مسحُ الأقواس بعدّادٍ يحترم النصوص والهروب، فيُقتطَع أوّلُ كائنٍ
// متوازنٍ فعلاً. وكلُّ تحليلٍ داخل try. والنتيجةُ صريحة: نجاحٌ أو سببُ فشل.

export type AiJsonResult<T> =
  | { ok: true; value: T }
  | { ok: false; reason: "empty" | "no_json" | "bad_json"; raw: string };

// يُزيل سياج ``` و```json إن وُجد.
function stripFence(s: string): string {
  const m = s.match(/```(?:json)?\s*([\s\S]*?)```/i);
  return m ? m[1] : s;
}

// الكائنُ المتوازن الذي يبدأ عند موضعٍ بعينه، مع احترام السلاسل والهروب:
// نصٌّ مثل {"a":"}"} كان يكسر أيَّ عدٍّ ساذج للأقواس.
function balancedFrom(s: string, start: number): string | null {
  let depth = 0, inStr = false, esc = false;
  for (let i = start; i < s.length; i++) {
    const c = s[i];
    if (esc) { esc = false; continue; }
    if (c === "\\") { if (inStr) esc = true; continue; }
    if (c === '"') { inStr = !inStr; continue; }
    if (inStr) continue;
    if (c === "{") depth++;
    else if (c === "}") { depth--; if (depth === 0) return s.slice(start, i + 1); }
  }
  return null;   // قُطع الردّ قبل إغلاق الكائن
}

// كلُّ الكائنات المرشَّحة بالترتيب. لا نكتفي بالأول: النماذج تشرح بالعربية
// قبل الإجابة، والشرحُ قد يحوي قوساً — «لاحظي أن {الصيغة} كالتالي:» —
// فأوّلُ كائنٍ متوازنٍ يكون الشرحَ لا الجواب. نُجرّبها حتى يُحلَّل واحد.
function* candidates(s: string): Generator<string> {
  for (let i = 0; i < s.length; i++) {
    if (s[i] !== "{") continue;
    const obj = balancedFrom(s, i);
    if (obj) { yield obj; i += obj.length - 1; }
  }
}

export function parseAiJson<T = unknown>(text: string): AiJsonResult<T> {
  const raw = String(text ?? "");
  if (!raw.trim()) return { ok: false, reason: "empty", raw };

  const body = stripFence(raw).trim();

  try { return { ok: true, value: JSON.parse(body) as T }; } catch { /* نُكمل */ }

  let sawCandidate = false;
  for (const slice of candidates(body)) {
    sawCandidate = true;
    try { return { ok: true, value: JSON.parse(slice) as T }; } catch { /* نُجرّب التالي */ }
  }
  return {
    ok: false,
    reason: sawCandidate ? "bad_json" : "no_json",
    raw: raw.slice(0, 300),
  };
}

// مصفوفةٌ غيرُ فارغة تحت مفتاحٍ متوقَّع.
// كان ‏(parsed as {questions?:unknown[]})?.questions || []‏ يُرجع ٢٠٠ ومعه
// صفرُ أسئلة حين يردّ النموذج بشكلٍ آخر — فتدفع المعلّمة حصّةً وتستلم فراغاً
// بلا تفسير. الآن يُميَّز «نجحَ وفيه محتوى» عمّا سواه.
export function requireArray(
  obj: unknown,
  key: string,
): { ok: true; items: unknown[] } | { ok: false; reason: string } {
  const v = (obj as Record<string, unknown> | null)?.[key];
  if (!Array.isArray(v)) return { ok: false, reason: `الحقل «${key}» ليس مصفوفة` };
  if (!v.length) return { ok: false, reason: `الحقل «${key}» فارغ` };
  return { ok: true, items: v };
}
