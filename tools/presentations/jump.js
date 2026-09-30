// شريط الانتقال السريع + ملاحظات المعلّم (فكرة الأستاذ عيسى):
// • زرّا «تمارين كتاب الطالب» و«تمارين كتاب النشاط» ينقلان مباشرةً إلى شريحة الانطلاق (افتحوا الكتاب صفحة كذا وابدؤوا من السؤال كذا)،
//   وزرّ «العودة إلى الدرس» يعيد إلى الشريحة التي كان المعلّم عندها.
// • شريحة الانطلاق: يختار المعلّم رقم السؤال فيظهر للطلاب كبيراً، ثم «انتقل إلى الحل» يفتح شريحة حلّ ذلك السؤال.
// • ملاحظات المعلّم (.tnote داخل الشريحة) تُنزَع من الشريحة وتظهر في لوحةٍ خاصة عند تفعيل «وضع المعلّم» (زرّ 🧑‍🏫 أو حرف N / ن).
(function(){
  var D=window.DECK;if(!D)return;
  var S=[].slice.call(document.querySelectorAll('.slide'));
  function ar(n){return String(n).replace(/\d/g,function(d){return '٠١٢٣٤٥٦٧٨٩'[d];});}
  var notes=S.map(function(s){var h=[].slice.call(s.querySelectorAll('.tnote')).map(function(n){var x=n.innerHTML;n.remove();return x;});return h.join('<hr>');});
  function idx(sel){for(var i=0;i<S.length;i++)if(S[i].matches(sel))return i;return -1;}
  var L={sb:idx('.launch-sb'),ab:idx('.launch-ab')};
  var app=[L.sb,L.ab,idx('.exs')].filter(function(i){return i>=0;});app=app.length?Math.min.apply(null,app):-1;
  var back=null,bar=document.createElement('div');bar.id='jbar';bar.setAttribute('role','toolbar');bar.setAttribute('aria-label','انتقال سريع');
  function btn(id,txt,title){var b=document.createElement('button');b.id=id;b.type='button';b.innerHTML=txt;b.title=title;bar.appendChild(b);return b;}
  var bT=btn('jt','🧑‍🏫','وضع المعلّم: إظهار ملاحظات الشريحة على الشاشة (N)');
  var bW=btn('jw','🪟','نافذة المعلّم: الملاحظات في نافذةٍ منفصلة تُسحب إلى شاشة الحاسوب (W)');
  var bR=btn('jr','↩ العودة إلى الدرس','العودة إلى الشريحة التي كنت عندها');
  var bS=L.sb>=0?btn('js','📘 تمارين كتاب الطالب','الانتقال إلى تمارين كتاب الطالب'):null;
  var bA=L.ab>=0?btn('ja','📗 تمارين كتاب النشاط','الانتقال إلى تمارين كتاب النشاط'):null;
  document.body.appendChild(bar);
  var P=document.createElement('aside');P.id='tpanel';P.setAttribute('aria-live','polite');document.body.appendChild(P);
  function jump(i){if(i<0)return;var c=D.cur();if(app<0||c<app)back=c;D.go(i);}
  if(bS)bS.onclick=function(e){e.stopPropagation();jump(L.sb);};
  if(bA)bA.onclick=function(e){e.stopPropagation();jump(L.ab);};
  bR.onclick=function(e){e.stopPropagation();D.go(back!=null?back:Math.max(0,app-1));};
  var T=false;try{T=localStorage.getItem('tnotes')==='1';}catch(e){}
  function setT(v){T=v;bT.classList.toggle('on',T);try{localStorage.setItem('tnotes',T?'1':'0');}catch(e){}upd(D.cur());}
  bT.onclick=function(e){e.stopPropagation();setT(!T);};
  document.addEventListener('keydown',function(e){if(e.key==='n'||e.key==='N'||e.key==='ن'){setT(!T);}});
  function upd(i){
    var inApp=app>=0&&i>=app;bR.hidden=!inApp;
    var sec=(L.ab>=0&&i>=L.ab&&(L.sb<L.ab||i<L.sb))?'ab':(L.sb>=0&&i>=L.sb&&(L.ab<L.sb||i<L.ab))?'sb':'';
    if(bS)bS.classList.toggle('on',sec==='sb');if(bA)bA.classList.toggle('on',sec==='ab');
    P.innerHTML=notes[i]?'<b>🧑‍🏫 للمعلّم</b>'+notes[i]:'';P.hidden=!(T&&notes[i]);
  }
  document.addEventListener('deck:slide',function(e){upd(e.detail);pw(e.detail);});
  // ─ نافذة المعلّم: تتبع الشرائح وتعرض الملاحظة وعنوان الشريحة التالية، والطلاب لا يرونها ─
  var W=null;
  function title(i){var s=S[i];if(!s)return '— نهاية العرض —';var h=s.querySelector('h1,h2,.lh');return h?h.textContent.trim():'(شريحة بلا عنوان)';}
  function pw(i){if(!W||W.closed)return;var d=W.document;
    d.getElementById('n').textContent=ar(i+1)+' / '+ar(S.length);d.getElementById('t').textContent=title(i);
    d.getElementById('b').innerHTML=notes[i]||'<i>لا ملاحظة لهذه الشريحة</i>';d.getElementById('x').textContent=title(i+1);}
  function openW(){
    W=window.open('','tnotes','width=560,height=640');if(!W)return;
    W.document.open();W.document.write('<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><title>نافذة المعلّم</title><style>'+
      'body{font-family:system-ui,sans-serif;margin:0;padding:18px;background:#FFFDF4;color:#0B1D3A;font-size:22px;line-height:1.6}'+
      '#n{float:left;background:#0B1D3A;color:#fff;border-radius:99px;padding:2px 14px;font-size:18px}#t{font-weight:800;font-size:24px;margin:0 0 10px}'+
      '#b{background:#fff;border:3px solid #E9A23B;border-radius:14px;padding:12px 14px;font-weight:700;min-height:120px}#b hr{border:0;border-top:1px dashed #E9A23B}'+
      '.k{margin-top:14px;color:#22385C;font-size:18px}#x{font-weight:800}.nav{display:flex;gap:10px;margin-top:16px}.nav button{flex:1;font-size:22px;padding:10px;border-radius:12px;border:2px solid #9FB3CC;background:#fff;cursor:pointer}'+
      '</style></head><body><span id="n"></span><p id="t"></p><div id="b"></div><p class="k">التالية: <span id="x"></span></p>'+
      '<div class="nav"><button id="pv">→ السابق</button><button id="nx">التالي ←</button></div></body></html>');
    W.document.close();
    W.document.getElementById('nx').onclick=function(){document.getElementById('next').click();};
    W.document.getElementById('pv').onclick=function(){document.getElementById('prev').click();};
    pw(D.cur());
  }
  bW.onclick=function(e){e.stopPropagation();openW();};
  document.addEventListener('keydown',function(e){if(e.key==='w'||e.key==='W'||e.key==='ص'){openW();}});
  // ─ شريحة الانطلاق ─
  S.forEach(function(s){
    if(!s.matches('.launch'))return;
    var bk=s.getAttribute('data-bk'),num=s.querySelector('.lnum'),go=s.querySelector('.lgo');
    s.querySelectorAll('.lq').forEach(function(q){q.addEventListener('click',function(e){e.stopPropagation();
      s.querySelectorAll('.lq').forEach(function(x){x.classList.toggle('on',x===q);});
      var n=q.getAttribute('data-q'),l=q.getAttribute('data-l');num.textContent=l;s.classList.add('chosen');
      go.hidden=false;go.setAttribute('data-q',n);go.innerHTML='انتقل إلى حلّ السؤال '+l+' ←';});});
    go.addEventListener('click',function(e){e.stopPropagation();var t=idx('.exq-'+bk+'-'+go.getAttribute('data-q'));if(t>=0)D.go(t);});
  });
  setT(T);
})();
