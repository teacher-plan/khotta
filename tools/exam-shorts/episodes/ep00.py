# الحلقة ٠ — تعريف بالسلسلة «٤٠ من ٤٠»: الفكرة، وما في كل حلقة، والمهارات، والدعوة للمتابعة.
from blocks import *
from build import CHK

TAG = 'سلسلة حلّ امتحانات الوزارة'

SKILLS = ['فكّ الأقواس والتقريب', 'الكسور', 'جزء من كمية', 'الجبر', 'الكسور العشرية', 'العوامل والمضاعفات', 'النسبة المئوية',
          'الأعداد الصحيحة والجذور', 'العدد الكسري والمسائل', 'وحدات القياس', 'المساحة', 'الزوايا', 'إيجاد المجهول']
AR = '١٢٣٤٥٦٧٨٩'
num = lambda k: ''.join('٠١٢٣٤٥٦٧٨٩'[int(c)] for c in str(k))

NARRATION = [
    'السلام عليكم يا طلاب الصف السابع. تبي تجيب أربعين من أربعين في امتحان الرياضيات؟ هذي السلسلة لك.',
    'في سلسلة أربعين من أربعين، نحلّ امتحان حقيقي من امتحانات الوزارة، سؤال سؤال، ونشرح كل سؤال بطريقة واضحة.',
    'كل حلقة فيها سؤالين. أول شي نتعلّم القاعدة، وبعدين نحلّ خطوة خطوة، وننبّهك على الخطأ الشائع، وفي الأخير سؤال تحدّي تجاوب عليه في التعليقات.',
    'ثلاث عشرة حلقة تغطّي مهارات الامتحان: الكسور، والنسبة المئوية، والجبر، والزوايا، والمساحة، وغيرها.',
    'والهدف مو بس نحلّ الامتحان. الهدف إنك تفهم طريقة الحل، عشان تحلّ أي سؤال يشبهه.',
    'تابع القناة، وفعّل التنبيهات، وشارك السلسلة مع زملائك. يالله نبدأ من الحلقة الأولى.',
]

ROW = lambda t, icon, txt: (f'<div class="steprow" data-t="{t}" data-fx="up" style="font-size:26px">'
                            f'<span style="font-size:28px">{icon}</span><span style="flex:1">{txt}</span>{CHK(t)}</div>')

SCENES = [
    STACK(T(0, AVATAR),
          T(0.3, '<span class="pill w" style="font-size:24px">أ. عيسى الحارثي</span>', cls='center'),
          T('@تبي تجيب', 'تبي تجيب ٤٠ من ٤٠؟', cls='center', style='font-weight:900;font-size:30px'),
          T('@هذي السلسلة', '٤٠ من ٤٠', cls='title', style='font-size:86px;line-height:1.1'),
          '<div data-deco="1" data-t="@هذي السلسلة" data-fx="wipe" style="height:9px;width:240px;margin:-12px auto 0;background:var(--coral);border-radius:6px"></div>',
          T('@هذي السلسلة', 'رياضيات الصف السابع', 'fade', 'center', 'font-weight:800;font-size:22px;color:var(--mut)'), gap=18),
    STACK(T(0, 'الفكرة', cls='title', style='font-size:56px;line-height:1.1'),
          T('@نحلّ امتحان', '<div class="card" style="padding:5px"><img src="{{img:head}}" style="width:100%;display:block"></div>', 'up'),
          T('@نحلّ امتحان', '<span class="pill">امتحانٌ حقيقي من الوزارة</span>', cls='center'),
          T('@سؤال سؤال', '<span class="pill w">سؤالاً سؤالاً، بشرحٍ واضح</span>', cls='center'), gap=22),
    STACK(T(0, 'في كل حلقة', cls='title', style='font-size:52px;line-height:1.1'),
          T('@كل حلقة فيها', '<span class="pill">سؤالان من امتحان الوزارة</span>', cls='center'),
          ROW('@نتعلّم القاعدة', '📌', 'القاعدة'),
          ROW('@نحلّ خطوة', '✍️', 'الحل خطوة خطوة'),
          ROW('@الخطأ الشائع', '⚠️', 'الخطأ الشائع'),
          ROW('@سؤال تحدّي', '💬', 'سؤال تحدٍّ في التعليقات'), gap=16),
    STACK(T(0, '١٣ حلقة', cls='title', style='font-size:56px;line-height:1.1'),
          '<div class="chips" style="gap:8px">' + ''.join(
              f'<span class="mark" data-t="@مهارات الامتحان" data-fx="pop" style="font-size:17px;padding:4px 10px">{num(k + 1)} • {s}</span>'
              for k, s in enumerate(SKILLS)) + '</div>', gap=24),
    STACK(T(0, 'الهدف', cls='title', style='font-size:56px;line-height:1.1'),
          T('@مو بس', '<span class="wrongbox" style="display:inline-block;border:3px dashed #B3261E;border-radius:12px;background:#FDECEA;padding:6px 16px;font-weight:900;font-size:26px;color:#B3261E">ليس حفظ الجواب فقط</span>', cls='center'),
          ANS('@الهدف إنك', 'أن تفهم طريقة الحل', 36),
          T('@عشان تحلّ', '<span class="pill">فتحلّ أي سؤالٍ يشبهه</span>', cls='center'), gap=26),
    STACK(T(0, 'تابعنا! 🔔', cls='title', style='font-size:58px;line-height:1.1'),
          '<div style="display:flex;gap:8px;justify-content:center">'
          '<span class="pill w" data-t="@تابع القناة" style="font-size:19px">✅ متابعة</span>'
          '<span class="pill w" data-t="@وفعّل" style="font-size:19px">🔔 التنبيهات</span>'
          '<span class="pill" data-t="@وشارك" style="font-size:19px">↗ مشاركة</span></div>',
          T('@يالله نبدأ', '<span class="pill" style="background:var(--ink);font-size:26px">الحلقة ١ تبدأ الآن ▶</span>', cls='center'),
          T('@يالله نبدأ', 'إعداد: أ. عيسى الحارثي', 'fade', 'center', 'font-weight:800;font-size:20px'), gap=26, justify='center'),
]
