-- إضافة نوع الملف (PDF/Word/PowerPoint/Excel/صورة/أخرى) لمكتبة الحلقة الأولى
alter table c1_library_items
  add column if not exists file_type text;
