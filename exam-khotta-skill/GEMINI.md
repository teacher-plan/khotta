# تعليمات Gemini CLI

مجلد إعداد اختبارات بمهارة «Exam-khotta» (`exam-khotta`).
- التثبيت مرّة واحدة: `gemini skills install <مسار>/.claude/skills/exam-khotta`، أو انسخ المجلد إلى
  `~/.gemini/skills/exam-khotta/` أو `.gemini/skills/exam-khotta/` (اسم المجلد يبقى `exam-khotta`).
- انسخ هذا الملف إلى مجلد عملك.
- عند طلب اختبار قصير أو سؤال قصير: فعّل مهارة exam-khotta واقرأ `SKILL.md` واتبعه حرفياً.
- اطرح الأسئلة **نصّاً** مرقّمة باختيارات مرقّمة في رسالة واحدة، ثم انتظر.
- المتطلبات: `pip install pymupdf pillow python-docx`، و Playwright لملفات PDF.
- خاطب المعلّم بالعربية، ولا تضع الكتب داخل مجلد المهارة.
