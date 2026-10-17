# تشغيل «Exam-khotta» على كل منصّة

| المنصّة | الأسئلة | الكتب والوثيقة | الفحص الآلي وملفات PDF/Word |
|---|---|---|---|
| **Claude Code** | منبثقة (`/exam-khotta`) | تُجلب آلياً | ✔ |
| **Codex** | نصّاً مرقّمة | تُجلب آلياً | ✔ |
| **Gemini CLI** | نصّاً مرقّمة | تُجلب آلياً | ✔ |
| **Claude.ai** | نصّاً | ترفق صفحات الدروس | ✔ غالباً (تنفيذ الشيفرة)، بلا إنترنت |
| **ChatGPT** | نصّاً | ترفق صفحات الدروس | جزئياً (محلّل البيانات: Word غالباً، وPDF قد لا يتوفّر) |
| **Gemini** (التطبيق) | نصّاً | ترفق صفحات الدروس | ✘ — يكتب النموذج الورقة ودليل التصحيح بنفسه |

## Claude Code
انسخ `.claude/skills/exam-khotta` إلى `~/.claude/skills/exam-khotta`، وافتح Claude Code في مجلد عملك، واكتب `/exam-khotta`.

## Codex
1. انسخ `exam-khotta` إلى `~/.codex/skills/exam-khotta` (بحيث يكون `SKILL.md` فيه مباشرةً).
2. انسخ `AGENTS.md` إلى مجلد عملك، واكتب: «استخدم مهارة exam-khotta وأعدّ الاختبار القصير الأول».

## Gemini CLI
1. `gemini skills install <المسار>/.claude/skills/exam-khotta` (أو انسخه إلى `~/.gemini/skills/exam-khotta`).
2. انسخ `GEMINI.md` إلى مجلد عملك، وتحقّق بـ `/skills list`.

## Claude.ai
- **مهارة (الأفضل):** فعّل «تنفيذ الشيفرة وإنشاء الملفات»، ثم الإعدادات ← الميزات ← المهارات ← ارفع `exam-khotta.zip`.
- **أو مشروع:** الصق `platforms/CHAT_INSTRUCTIONS.md` في تعليمات المشروع، وارفع ملفات المعرفة أدناه.

## ChatGPT
GPT مخصّص أو مشروع: الصق `platforms/CHAT_INSTRUCTIONS.md` في التعليمات، وارفع ملفات المعرفة، وفعّل «محلّل البيانات».
لبناء الملفات بالمحرّك نفسه: ارفع `exam-khotta.zip` في المحادثة واطلب «فكّ الحزمة وابنِ بـ build_exam.py».

## Gemini — Gem
«Gem جديد»: التعليمات من `platforms/CHAT_INSTRUCTIONS.md`، وملفات المعرفة (حتى ١٠).

## ملفات المعرفة للمحادثات
من `.claude/skills/exam-khotta/` (حتى ١٠ ملفات؛ اختر ما يخصّ مادّتك):
1. `SKILL.md`
2. `specs/<المادة>.summary.md` و`specs/<المادة>.json` (مثل `islamic-5-12`)
3. `subjects/<المادة>.md` (قواعد الكتابة: math، science، arabic، islamic)
4. `guides/WRITING.md`
5. `guides/FORMAT.md`
6. `examples/<مثال المادّة>.json`
7. فهرس صفّك من `indexes/` إن وُجد

**الآيات في المحادثة:** إن أتاحت البيئة الإنترنت فاكتب `quran[112:1-4]` ويجلبها المحرّك؛ وإلا فانقلها من صورة صفحة الكتاب
المرفقة حرفاً حرفاً، ولا تكتبها من الذاكرة.

لا ترفع الكتب كاملةً إلى GPT أو Gem مشترك؛ أرفق صفحات الدروس في المحادثة نفسها.
