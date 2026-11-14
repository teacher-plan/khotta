-- كتاب المهارات الحياتية للتاسع ف١: صفحة PDF = الصفحة المطبوعة + ٣، فالإزاحة ٤ (صيغة المنصّة: المطبوعة + الإزاحة − ١). متعادلة.
update public.book_sources set offset_pages=4, updated_at=now() where semester='الفصل الأول' and grade='9' and subject='المهارات الحياتية';
