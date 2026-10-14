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
من `.claude/skills/exam-khotta/`:
1. `SKILL.md`
2. `specs/math-5-10.md` (ومعه `specs/math-5-10.json`)
3. `guides/WRITING.md`
4. `guides/FORMAT.md`
5. `indexes/math-7-1.json` أو `indexes/math-7-2.json` (فهرس صفّك)
6. `examples/math7-1_short-test-1.json` (مثال كامل)

لا ترفع الكتب كاملةً إلى GPT أو Gem مشترك؛ أرفق صفحات الدروس في المحادثة نفسها.
