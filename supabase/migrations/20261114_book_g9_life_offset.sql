-- كتاب المهارات الحياتية للتاسع ف١: صفحة PDF = الصفحة المطبوعة + ٣ (الاستيراد يضع ١ افتراضياً). متعادلة.
update public.book_sources set offset_pages=3, updated_at=now() where semester='الفصل الأول' and grade='9' and subject='المهارات الحياتية';
