# مجلدات التحضير في Google Drive (حساب الموصل: teacherplane2026project@gmail.com)

الشجرة: خطة — تحضير الدروس / الصف / الوحدة / الدرس — مجلدٌ لكل درس فيه: العرض (html)، الفيديو (mp4)، الملخّص (pdf) — بلا صور PNG.

| المجلد | المعرّف | صفحة التحضير |
|---|---|---|
| خطة — تحضير الدروس | `16l7GCpiWjiMxnDLQ4Rw0g2MMmOROh70v` | |
| الصف السابع | `1AD2Ce_-dnNMhldwa_M86TDYsUHgz4rEx` | |
| الوحدة الأولى — الأعداد الصحيحة والقوى والجذور | `1XVKUAWfSSocgt2lMvnGFNpfZ5ta1is2Y` | |
| ١-١ الأعداد الصحيحة | `1MXacqVM1dGHa1i9PZ1yoXlzGWlWQS9X5` | https://claude.ai/artifact/Y3GimnXMCrcZRt3HGFRpyW |
| ١-٢ المضاعفات | `1tZ4ay9uSX6XYsW1ZMGZys-FkvQHQdd2H` | https://claude.ai/artifact/DzyQ3EiAixCxaqhLbEXmBK |
| ١-٣ العوامل وقابلية القسمة | `19TWpBIDBo48aoWrdQbSIljuTwqqnDXM8` | https://claude.ai/artifact/9SBWQXXvvuNv5q33BygbKo |
| ١-٤ الأعداد الأولية | `1M17Z63KSrESWHRHFxBS8RKjek_Mdn3KG` | https://claude.ai/artifact/55iACNYFo9MWNVWptpCspU |
| ١-٥ الأسس | `1nTRLqbbV5ynhFpvjB9t7UJzOcOB_ygor` | https://claude.ai/artifact/GieP1CJptmpYwy5zhcGAfK |
| ١-٦ القوى والجذور | `1Srpp0PXEfZ7y5syhPhl-9ZtA7hd3zY2D` | https://claude.ai/artifact/3sgrEttY3JqnfFEcUHH58D |
| ١-٧ ترتيب العمليات الحسابية | `12nZqENqw08uR5ddViDyjFIn0nTLKNhit` | https://claude.ai/artifact/GJq9QcVgtNuU3wa7j6CJf7 |
| مراجعة الوحدة الأولى | `1L9VZ_BCW8c47rMmJFbHb2ErW4D0QRL-r` | https://claude.ai/artifact/Jn4W7waYU5QT2d8jMoDe18 |
| الوحدة الثانية — العبارات الجبرية والمعادلات والصيغ | `1upOVHMBnI4QawCpL3lyHLgI5H-6MItjG` | |
| ٢-١ كتابة العبارات الجبرية | `1OhvfsZWLPoGp4nyhiPo5y4E2fKplc8Jk` | https://claude.ai/artifact/C4GLzearm89H3UFqh7p3bg |
| ٢-٢ تجميع الحدود المتشابهة | `1Dyaeq4iP8kKcTLYhti1ePbiu3fF8Kakn` | https://claude.ai/artifact/Bsak63Ex47Lb4TzDA8RXWN |

## لكل درسٍ جديد
1. أنشئ مجلد الدرس داخل مجلد وحدته بأداة Google Drive `create_file` (mimeType مجلد) — ومجلد الوحدة إن لم يوجد — وأضف المعرّف هنا.
2. ابنِ صفحة التحضير بـ `kit.py … --drive-folder <المعرّف>` وانشرها بـ
   `capabilities={"downloads": true, "mcp": {"servers": [{"server": "Google Drive", "tools": ["create_file", "search_files"]}]}}`.
3. الفيديو لا يمرّ عبر موصل Drive (حجمه كبير): يحفظه المعلّم من الصفحة ثم يختار Drive — وقد يصل إلى مجلد «Saved from Chrome»، فانقله بـ `update_file` إلى مجلد الدرس واحذف ذلك المجلد.
3. الرفع نفسه يتمّ من الصفحة بزرّ «رفع التحضير إلى Drive» بحساب المعلّم (الملفات الكبيرة حتى ١٦ ميغابايت تمرّ كملف لا كنص) — لا تُرفع الملفات من الجلسة (تكلفتها عالية جداً).
4. بعد تأكّد وصول الملفات إلى Drive (`search_files` بـ parentId) لا تُحفظ الملفات الثقيلة (mp4/mp3/png/pdf) في المستودع.

## الفيديو (قرار الأستاذ عيسى)
- الفيديو **لا يُرفع من صفحة التحضير** (الرفع يتجاوز المهلة: `server_unavailable: file upload timed out`، والموصل من الجلسة لا يتّسع لملفٍ بهذا الحجم).
- يُضغط دائماً: `ffmpeg -c:v libx264 -crf 32 -preset slow -tune stillimage -c:a aac -b:a 64k -ac 1 -movflags +faststart` (١٠٨٠p، ٣–٥ ميغابايت)،
  ثم **يُرسَل مباشرةً في المحادثة** بأداة SendUserFile (ملفاً ملفاً، `display: "render"`) **باسم الدرس** (مثل `١-١_الأعداد_الصحيحة.mp4`) — اتفاق الأستاذ عيسى الثابت: الفيديو نفسه، **لا رابط صفحة**.
  ويُضاف أيضاً إلى صفحة التحضير (`kit.py --video`) احتياطاً. يرفعه المعلّم إلى مجلد الدرس بنفسه، ثم أتحقّق بـ `search_files` وأحذف النسخ القديمة.
- زرّ «رفع التحضير إلى Drive» **يتخطّى الملف الموجود بالاسم نفسه**: عند تحديث عرضٍ أو ملخّص احذف النسخة القديمة من Drive (`trash_file`) أولاً، ثم يضغط المعلّم الزرّ.
