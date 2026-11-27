# قالب «حزمة الدرس» للمخزن المشترك: ورقة عمل + اختبار قصير + نموذج إجابة.
# يُنفَّذ بعد summary2.py و area_sum.py (exec)، فيرث الرأس والتذييل والخطوط وقاعدة «لا شَرطة فاصلة».
# المحتوى أصليّ من إعدادنا، مبنيّ على أهداف الدرس وأخطائه الشائعة في دليل المعلّم، وبأرقامٍ غير أرقام تمارين الكتاب.

def student_bar(extra=''):
    return ('<div class="sbar"><span>الاسم: <i></i></span><span>الشعبة: <i class="s"></i></span>'
            f'<span>التاريخ: <i class="s"></i></span>{extra}</div>')

def level(name, icon, cls): return f'<div class="lvl {cls}"><b>{icon}</b>{name}</div>'

def lines(n=1): return '<div class="al">' + '<span></span>' * n + '</div>'

def q(n, text, body='', fig='', marks=None, ans_lines=0):
    mk = f'<span class="mk">{ {1: "درجة واحدة", 2: "درجتان"}.get(marks, a(marks) + " درجات")}</span>' if marks else ''
    inner = f'<div class="qt"><span class="qn">{a(n)}</span><div class="qx">{text}{body}{lines(ans_lines) if ans_lines else ""}</div>{mk}</div>'
    if fig:
        return f'<div class="qq fig"><div>{inner}</div>{fig}</div>'
    return f'<div class="qq">{inner}</div>'

def mcq(opts): return '<div class="mc">' + ''.join(f'<span><i>{l}</i>{o}</span>' for l, o in zip('أبجد', opts)) + '</div>'

def blank(w=22): return f'<span class="bl" style="--w:{w}mm"></span>'

def gtable(head, rows):
    """جدولٌ يكمله الطالب: الخانة '' تُرسم فراغاً."""
    return ('<table class="gt"><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' +
            ''.join('<tr>' + ''.join(f'<td>{c if c else "<i></i>"}</td>' for c in r) + '</tr>' for r in rows) + '</table>')

def key_item(n, steps, ans):
    rows = ''.join(f'<tr><td class="e">{e}</td><td class="r">{r}</td></tr>' for e, r in steps)
    return f'<div class="ki"><span class="qn">{a(n)}</span><div><table>{rows}</table><div class="ka">✔ {ans}</div></div></div>'

def score_box(total): return f'<div class="score"><b>الدرجة</b><span><i></i>من {a(total)}</span></div>'

CSS += r'''
.sbar{display:flex;gap:6mm;font-size:11pt;font-weight:700;color:var(--nav);margin:0 0 1mm;align-items:flex-end}
.sbar span{display:flex;gap:2mm;align-items:flex-end;flex:1}.sbar span:nth-child(n+2){flex:.55}
.sbar i{flex:1;border-bottom:1.2px dotted var(--ink2);height:5mm}
.lvl{display:flex;align-items:center;gap:2.5mm;font-size:13pt;font-weight:800;padding:1.3mm 4mm;border-radius:2.5mm;margin-top:1mm}
.lvl b{font-size:13pt}
.lvl.l1{background:#EEF4FD;color:#1E5FB8}.lvl.l2{background:#EFF8F2;color:#157347}.lvl.l3{background:#F4F1FD;color:#5B3CC4}
.qq{border:1.1px solid var(--line);border-radius:3mm;padding:2.2mm 3.5mm;background:#fff}
.qq.fig{display:flex;gap:4mm;align-items:center}.qq.fig>div:first-child{flex:1}
.qq .sfig svg{height:var(--h,24mm)}
.qt{display:flex;gap:3mm;align-items:flex-start}
.qn{flex:none;width:7mm;height:7mm;border-radius:50%;background:var(--nav);color:#fff;display:inline-flex;align-items:center;justify-content:center;font-weight:800;font-size:10.5pt;margin-top:.6mm}
.qx{flex:1;font-size:11.5pt;font-weight:600;line-height:1.75}
.mk{flex:none;background:#FFF7E6;border:1px solid #F1C66B;color:#9A5B00;border-radius:99px;padding:.3mm 3mm;font-size:9.5pt;font-weight:800;white-space:nowrap}
.al{display:flex;flex-direction:column;gap:0;margin-top:1mm}
.al span{display:block;height:8.5mm;border-bottom:1.2px dotted #9AA9C0}
.mc{display:flex;flex-wrap:wrap;gap:2mm 6mm;margin-top:1.2mm}
.mc>span{display:inline-flex;align-items:center;gap:2mm;border:1.2px solid var(--line);border-radius:99px;padding:.6mm 4mm .6mm 2mm;font-weight:700}
.mc>span>i{font-style:normal;width:6mm;height:6mm;border-radius:50%;border:1.3px solid var(--nav);display:inline-flex;align-items:center;justify-content:center;font-size:9.5pt;color:var(--nav)}
.bl{display:inline-block;width:var(--w);border-bottom:1.3px dotted var(--ink2);height:1em;vertical-align:baseline}
.gt{border-collapse:separate;border-spacing:0;border:1.2px solid var(--line);border-radius:3mm;overflow:hidden;margin-top:1.5mm;font-size:12pt}
.gt th{background:var(--nav);color:#fff;padding:1mm 4mm;font-weight:700}
.gt td{border-top:1px solid var(--line);padding:1.2mm 4mm;text-align:center;font-weight:700;min-width:24mm;height:9mm;font-family:'KDigits','Readex Pro',sans-serif}
.gt td i{display:inline-block;width:16mm;border-bottom:1.2px dotted var(--ink2);height:5mm}
.score{display:flex;align-items:center;gap:3mm;font-weight:800;color:var(--nav);font-size:11pt}
.score span{display:flex;align-items:flex-end;gap:2mm;border:1.4px solid var(--nav);border-radius:2.5mm;padding:1mm 3mm}
.score i{display:inline-block;width:12mm;height:6mm}
.ki{display:flex;gap:3mm;align-items:flex-start;border-bottom:1px dashed var(--line);padding:.9mm 0}
.ki:last-child{border-bottom:0}
.ki>div{flex:1}.ki table{border-collapse:collapse}
.ki td{padding:.2mm 2mm;vertical-align:middle}.ki td.e{font-size:11pt;font-weight:700;white-space:nowrap}
.ki td.r{font-size:10pt;color:var(--ink2);font-weight:600}
.ka{display:inline-block;margin-top:.6mm;background:var(--exbg);color:var(--ex);border-radius:2mm;padding:.4mm 3mm;font-weight:800;font-size:11pt}
.kh{background:#FDF1EF;border:1px solid #F2B8B2;color:var(--w);border-radius:2.5mm;padding:1.3mm 4mm;font-weight:800;font-size:11pt}
.qq .sfig{flex:none}
'''
