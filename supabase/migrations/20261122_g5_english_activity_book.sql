-- كتاب النشاط (Activity Book 5A) للغة الإنجليزية، الصف الخامس ف١: الدروس نفسها (الكتاب ٢) بصفحاتها في كتاب النشاط.
-- المنصّة تعرض الدرس مرّة واحدة وتجمع صفحاته من الكتابين (كتاب الطالب أولاً). صفحة PDF = المطبوعة + ٢ ← الإزاحة ٣. متعادلة.
delete from public.curriculum where semester='الفصل الأول' and grade=5 and subject='اللغة الإنجليزية' and book_no=2;
insert into public.curriculum (semester,grade,subject,unit,lesson,sort,page,book_no)
select c.semester,c.grade,c.subject,c.unit,c.lesson,c.sort,v.p,2
from public.curriculum c join (values (1,9),(2,10),(3,11),(4,12),(5,13),(6,14),(7,15),(8,16),(9,17),(10,18),(11,19),(12,20),(13,23),(14,76),(15,77),(16,24),(17,25),(18,26),(19,27),(20,28),(21,29),(22,30),(23,31),(24,32),(25,35),(26,78),(27,79),(28,36),(29,37),(30,38),(31,39),(32,40),(33,41),(34,42),(35,43),(36,44),(37,47),(38,80),(39,81),(40,48),(41,49),(42,50),(43,51),(44,52),(45,53),(46,54),(47,55),(48,56),(49,59),(50,82),(51,83),(52,60),(53,null),(54,null)) v(s,p) on v.s=c.sort
where c.semester='الفصل الأول' and c.grade=5 and c.subject='اللغة الإنجليزية' and c.book_no=1 and v.p is not null;
update public.book_sources set offset_pages=3, updated_at=now() where semester='الفصل الأول' and grade='5' and subject='اللغة الإنجليزية' and book_no=2;
