-- تصحيح إزاحات المهارات الحياتية (ف١): الصيغة في المنصّة «صفحة PDF = المطبوعة + الإزاحة − ١»،
-- فالإزاحة = الفرق + ١. العاشر: الكتاب +١ ← ٢، والدليل +٢ ← ٣. التاسع: الكتاب +٣ ← ٤، والدليل +١ ← ٢. متعادلة.
update public.book_sources set offset_pages=2, updated_at=now() where semester='الفصل الأول' and grade='10' and subject='المهارات الحياتية';
update public.book_sources set offset_pages=4, updated_at=now() where semester='الفصل الأول' and grade='9' and subject='المهارات الحياتية';
update public.teacher_guides set offset_pages=3, updated_at=now() where semester='الفصل الأول' and grade=10 and subject='المهارات الحياتية';
update public.teacher_guides set offset_pages=2, updated_at=now() where semester='الفصل الأول' and grade=9 and subject='المهارات الحياتية';
