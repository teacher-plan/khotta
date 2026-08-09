-- 🔴 إصلاح: مخزن الدروس المشترك كان يرفض الخطة والعرض بصمت
--
-- ملف 20260728_c1_shared_assets.sql يعرّف الجدول بأربعة أنواع
-- (prep, info, slides, game)، لكن الإنتاج بقي على نسخةٍ أقدم بنوعين فقط
-- (game, info). السبب أن الملف يبدأ بـ«create table if not exists»، وهي
-- لا تفعل شيئاً إطلاقاً حين يكون الجدول موجوداً سلفاً — فتغييرُ القيود
-- داخل تعريف الجدول لا يصل الإنتاج أبداً مهما أُعيد تشغيل الملف.
--
-- الأثر المقيس: الجدول يحوي game=٣ و info=٣ و prep=٠ و slides=٠. أي أن
-- كل نشرٍ لخطة درسٍ أو عرضٍ تقديميّ رُفض بالقيد منذ إنشاء الميزة، وابتلع
-- الرفضَ معالجٌ فارغ في shAutoPublish. المكسب الموعود في تعليق ذلك الملف
-- (توفير استدعاءات الذكاء الاصطناعي بتبنّي ما جهّزته زميلة) لم يتحقق
-- للخطة والعرض قط — تحقّق للملخص واللعبة وحدهما.
--
-- الإصلاح آمن: الصفوف القائمة كلها game/info، وهي تجتاز القيد الجديد
-- (الأوسع) بلا استثناء، فلا صفَّ يُرفض ولا بيانات تُمَس.

-- ــ النوع ــ
-- الاسم المولَّد تلقائياً في الإنتاج يختلف عن المسمّى في الملف الأصلي،
-- فنُسقط كليهما احتياطاً قبل إعادة الإنشاء بالاسم المقصود
alter table c1_shared_assets drop constraint if exists c1_shared_assets_kind_check;
alter table c1_shared_assets drop constraint if exists c1sa_kind;
alter table c1_shared_assets
  add constraint c1sa_kind check (kind in ('prep','info','slides','game'));

-- ــ الحمولة ــ
-- كل نوع يحمل حمولته: لا خطة ولا عرض بلا محتوى، ولا ملخص بلا صورة،
-- ولا لعبة بلا محتوى وقالب معاً
alter table c1_shared_assets drop constraint if exists c1sa_payload;
alter table c1_shared_assets
  add constraint c1sa_payload check (
    (kind in ('prep','slides') and content is not null)
    or (kind = 'info' and image_url is not null)
    or (kind = 'game' and content is not null and template is not null)
  );
