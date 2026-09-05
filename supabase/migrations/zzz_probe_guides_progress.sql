-- فحصٌ للقراءة فقط (يُحذف بعد الاطّلاع): كم دليلاً سُجِّل حتى الآن؟
select grade, subject, page_count, status, created_at
from public.teacher_guides
order by created_at;
