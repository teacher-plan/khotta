-- p58: إلغاء نظام ثيمات الألعاب القديم.
-- صار لكل لعبةٍ ثيمها الثابت المرسوم بالكود في الواجهة (GM_WORLDS في cycle1.html)،
-- فلا ثيمٌ يُختار ولا يُخزَّن. تُفرَّغ المراجع ثم تُحذف الثيمات المجهّزة سابقاً
-- (صورها في library-files/game-themes حُذفت من التخزين في الخطوة نفسها).
-- الجدول والعمودان theme_id يبقيان (فارغين) كي لا تنكسر نسخٌ قديمة مفتوحة في متصفحات المعلمين.
update public.games set theme_id = null where theme_id is not null;
update public.c1_shared_assets set theme_id = null where theme_id is not null;
delete from public.game_themes;
-- إعدادات المشرف لكل لعبة: يُزال منها الثيم الافتراضي وقفله، وتبقى الأصوات والخيارات
update public.ai_settings
   set value = (select coalesce(jsonb_object_agg(k, case when jsonb_typeof(v)='object' then v - 'theme' - 'lock' else v end), '{}'::jsonb)::text
                  from jsonb_each(value::jsonb) e(k, v)),
       updated_at = now()
 where key = 'game_cfg' and value is not null and value <> '';
