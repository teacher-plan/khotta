# «عمارة العمليات» — وسيلة تذكّر لترتيب العمليات الحسابية (تحلّ محلّ رسمة الرجل):
# ننزل من السطح إلى الأرض طابقاً طابقاً، وداخل الطابق الواحد نمشي من اليمين إلى اليسار كما نقرأ.
# HTML بأنماط مضمَّنة ووحدات em فقط، فتعمل كما هي في العرض وورقة الملخّص ومصدر الفيديو (.dc.html).
# building(wrap) — wrap(i, html) تغلّف الطابق i (للظهور خطوةً خطوة)؛ الحجم من font-size الحاوية.

BLUE, RED, PURPLE, GREEN, INK = '#2563EB', '#C7361B', '#7A3FD1', '#1B7A3E', '#14305C'

def _badge(n, c):
    return (f'<b style="flex: none; width: 1.5em; height: 1.5em; border-radius: 50%; background: {c}; color: #FFFFFF; '
            f'display: flex; align-items: center; justify-content: center; font-size: .8em">{n}</b>')

def _win(t, c, bg):
    return (f'<span style="flex: none; width: 1.7em; height: 1.5em; border-radius: .25em; background: {bg}; border: .08em solid {c}; color: {c}; '
            f'display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.05em; line-height: 1">{t}</span>')

ROOT = ('<svg viewBox="0 0 40 32" style="width: 1.25em; height: 1em" aria-hidden="true"><path d="M38 18 L34 15 L28 30 L22 4 L2 4" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        '<text x="12" y="27" font-size="19" font-weight="700" fill="currentColor" text-anchor="middle">٩</text></svg>')  # جذرٌ مرسوم يبدأ من اليمين
ARROW = '<span style="flex: none; font-size: .9em; opacity: .75">←</span>'

def _rooms(a, b, c, bg):  # غرفتان في طابق واحد: نمرّ على اليمنى ثم اليسرى
    return f'<span style="display: flex; align-items: center; gap: .3em; direction: rtl">{_win(a, c, bg)}{ARROW}{_win(b, c, bg)}</span>'

def _floor(n, label, c, bg, extra, radius='.3em'):
    return (f'<div style="display: flex; align-items: center; justify-content: space-between; gap: .6em; padding: .45em .7em; '
            f'background: {bg}; border: .09em solid {c}; border-radius: {radius}; color: {c}; font-weight: 700">'
            f'<span style="display: flex; align-items: center; gap: .45em">{_badge(n, c)}<span>{label}</span></span>{extra}</div>')

def building(wrap=lambda i, h: h, sub=True):
    roof = _floor('١', 'الأقواس', BLUE, '#EAF1FF', f'<span style="font-weight: 800; font-size: 1.2em; line-height: 1">( )</span>', '2.2em 2.2em .3em .3em')
    f2 = _floor('٢', 'الأسس والجذور', RED, '#FDECE8', '<span style="display: flex; gap: .35em">' + _win('<span style="display: inline-flex; align-items: flex-start; direction: rtl">٥<sup style="font-size: .55em">٢</sup></span>', RED, '#FFFFFF') + _win(ROOT, RED, '#FFFFFF') + '</span>')
    f3 = _floor('٣', 'الضرب والقسمة', PURPLE, '#F3ECFD', _rooms('×', '÷', PURPLE, '#FFFFFF'))
    f4 = _floor('٤', 'الجمع والطرح', GREEN, '#E6F6EC', _rooms('+', '−', GREEN, '#FFFFFF'))
    floors = [roof, f2, f3, f4]
    shaft = ('<div style="flex: none; width: 2.8em; display: flex; flex-direction: column; align-items: center; justify-content: space-between; '
             f'background: #EEF3F9; border: .08em solid #C9D6E8; border-radius: .5em; padding: .35em 0; color: {INK}; font-weight: 800">'
             '<span style="font-size: .66em">السطح</span><span style="flex: 1; width: .12em; background: #9FB3CC; margin: .2em 0; position: relative"></span>'
             '<span style="font-size: 1em; line-height: 1">▼</span><span style="font-size: .66em">الأرض</span></div>')
    body = ''.join(wrap(i, f) for i, f in enumerate(floors))
    ground = f'<div style="height: .35em; background: {INK}; border-radius: .2em; margin-top: .15em"></div>'
    cap = (f'<div style="font-size: .62em; font-weight: 700; color: #3B5480; text-align: center">ننزل من <b>السطح</b> إلى <b>الأرض</b> · '
           f'وفي الطابق الواحد: من اليمين إلى اليسار ←</div>') if sub else ''
    return (f'<div dir="rtl" style="display: inline-flex; flex-direction: column; gap: .35em; direction: rtl">'
            f'<div style="font-weight: 800; color: {INK}; text-align: center; font-size: .85em">عمارة العمليات</div>'
            f'<div style="display: flex; gap: .45em; align-items: stretch"><div style="display: flex; flex-direction: column; gap: .3em; min-width: 11.5em">{body}{ground}</div>{shaft}</div>{cap}</div>')

# نشيدٌ قصير يردّده الصف (من تأليف المساعد — ليس من المرجع)
CHANT = ['الأقواسُ أوّلاً نفكُّها', 'والأسُّ والجذرُ بعدَها', 'ضربٌ وقسمةٌ من اليمين', 'وجمعٌ وطرحٌ في الأخير']
