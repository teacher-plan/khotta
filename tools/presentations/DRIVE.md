# مجلدات التحضير في Google Drive (حساب الموصل: teacherplane2026project@gmail.com)

الشجرة: خطة — تحضير الدروس / الصف / الوحدة / الدرس — مجلدٌ لكل درس فيه: العرض (html)، الفيديو (mp4)، صور الملخّص (png)، الملخّص (pdf).

| المجلد | المعرّف | صفحة التحضير |
|---|---|---|
| خطة — تحضير الدروس | `16l7GCpiWjiMxnDLQ4Rw0g2MMmOROh70v` | |
| الصف السابع | `1AD2Ce_-dnNMhldwa_M86TDYsUHgz4rEx` | |
| الوحدة الأولى — الأعداد الصحيحة والقوى والجذور | `1XVKUAWfSSocgt2lMvnGFNpfZ5ta1is2Y` | |
| ١-٦ القوى والجذور | `1Srpp0PXEfZ7y5syhPhl-9ZtA7hd3zY2D` | https://claude.ai/artifact/3sgrEttY3JqnfFEcUHH58D |
| ١-٧ ترتيب العمليات الحسابية | `12nZqENqw08uR5ddViDyjFIn0nTLKNhit` | https://claude.ai/artifact/GJq9QcVgtNuU3wa7j6CJf7 |
| مراجعة الوحدة الأولى | `1L9VZ_BCW8c47rMmJFbHb2ErW4D0QRL-r` | https://claude.ai/artifact/Jn4W7waYU5QT2d8jMoDe18 |

## لكل درسٍ جديد
1. أنشئ مجلد الدرس داخل مجلد وحدته بأداة Google Drive `create_file` (mimeType مجلد) — ومجلد الوحدة إن لم يوجد — وأضف المعرّف هنا.
2. ابنِ صفحة التحضير بـ `kit.py … --drive-folder <المعرّف>` وانشرها بـ
   `capabilities={"downloads": true, "mcp": {"servers": [{"server": "Google Drive", "tools": ["create_file", "search_files"]}]}}`.
3. الرفع نفسه يتمّ من الصفحة بزرّ «رفع التحضير إلى Drive» بحساب المعلّم (الملفات الكبيرة حتى ١٦ ميغابايت تمرّ كملف لا كنص) — لا تُرفع الملفات من الجلسة (تكلفتها عالية جداً).
4. بعد تأكّد وصول الملفات إلى Drive (`search_files` بـ parentId) لا تُحفظ الملفات الثقيلة (mp4/mp3/png/pdf) في المستودع.
