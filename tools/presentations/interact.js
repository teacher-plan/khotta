// أدوات التفاعل (طلب الأستاذ عيسى، ٢٨ أكتوبر): منافسة الفريقين، لوحة الأرقام، اسحب ورتّب، طابق.
// تُبنى في ملف الدرس بالدوال TEAMS() و KEYPAD() و ORDER() و MATCH() من common_slides.py.
(function(){
  var D=window.DECK||{},tone=D.tone||function(){},fx=D.fx||function(){};
  function ar(s){return String(s).replace(/\d/g,function(d){return '٠١٢٣٤٥٦٧٨٩'[d];}).replace(/\./g,'٫');}
  function num(s){return parseFloat(String(s).replace(/[٠-٩]/g,function(d){return '٠١٢٣٤٥٦٧٨٩'.indexOf(d);}).replace(/[٫,]/g,'.'));}
  function stop(e){e.stopPropagation();}
  function guard(el){['click','pointerdown','touchstart','keydown'].forEach(function(t){el.addEventListener(t,stop);});}
  function shake(el){el.classList.remove('no');void el.offsetWidth;el.classList.add('no');}

  // ─ منافسة الفريقين: لوحة نقاط ثابتة أسفل الشاشة بعد «ابدأ المنافسة»، وبعد كل إجابة صحيحة: «النقطة لمن؟» ─
  var K='kh-teams',T={on:false,a:0,b:0,last:[]};
  try{var sv=JSON.parse(sessionStorage.getItem(K)||'null');if(sv)T=sv;}catch(_){}
  function save(){try{sessionStorage.setItem(K,JSON.stringify(T));}catch(_){}}
  var bar=document.createElement('div');bar.className='ixt-bar';bar.innerHTML=
    '<button class="ixt a"><span class="ixt-n">🔵 الأزرق</span><b class="ixt-s"></b></button>'+
    '<button class="ixt-u" title="تراجع">↺</button>'+
    '<button class="ixt b"><span class="ixt-n">🔴 الأحمر</span><b class="ixt-s"></b></button>';
  var pop=document.createElement('div');pop.className='ixt-pop';pop.innerHTML=
    '<span>النقطة لمن؟</span><button class="ixt-g a">🔵</button><button class="ixt-g b">🔴</button><button class="ixt-g x">لا أحد</button>';
  document.body.appendChild(bar);document.body.appendChild(pop);guard(bar);guard(pop);
  function draw(){bar.classList.toggle('on',T.on);bar.querySelector('.a .ixt-s').textContent=ar(T.a);bar.querySelector('.b .ixt-s').textContent=ar(T.b);
    bar.classList.toggle('la',T.a>T.b);bar.classList.toggle('lb',T.b>T.a);}
  function point(t){if(t!=='a'&&t!=='b')return;T[t]++;T.last.push(t);save();draw();tone('ok');
    var el=bar.querySelector('.'+t);el.classList.remove('pop');void el.offsetWidth;el.classList.add('pop');}
  bar.querySelector('.a').onclick=function(){point('a');};
  bar.querySelector('.b').onclick=function(){point('b');};
  bar.querySelector('.ixt-u').onclick=function(){var t=T.last.pop();if(t&&T[t]>0)T[t]--;save();draw();tone('step');};
  var pt=null;
  function ask(){if(!T.on)return;pop.classList.add('on');clearTimeout(pt);pt=setTimeout(function(){pop.classList.remove('on');},8000);}
  pop.querySelectorAll('.ixt-g').forEach(function(b){b.onclick=function(){pop.classList.remove('on');if(b.classList.contains('a'))point('a');else if(b.classList.contains('b'))point('b');};});
  document.addEventListener('deck:ok',ask);
  document.querySelectorAll('.ixt-start').forEach(function(b){guard(b);b.onclick=function(){T={on:true,a:0,b:0,last:[]};save();draw();tone('ok');fx();};});
  document.querySelectorAll('.ixt-end').forEach(function(b){guard(b);b.onclick=function(){
    var w=b.closest('.slide').querySelector('.ixt-win');
    if(w)w.textContent=T.a===T.b?'تعادل! '+ar(T.a)+' – '+ar(T.b)+' 🤝':(T.a>T.b?'🏆 فاز الفريق الأزرق ':'🏆 فاز الفريق الأحمر ')+ar(Math.max(T.a,T.b))+' – '+ar(Math.min(T.a,T.b));
    fx();tone('ok');T.on=false;save();draw();};});
  draw();
  function win(el){fx();tone('ok');try{document.dispatchEvent(new CustomEvent('deck:ok',{detail:{el:el}}));}catch(_){}}

  // ─ لوحة الأرقام: يكتب الطالب الناتج ثم «تحقّق» ─
  document.querySelectorAll('.ixk').forEach(function(k){
    guard(k);var out=k.querySelector('.ixk-out'),fb=k.querySelector('.ixk-fb'),v='';
    k.querySelectorAll('.ixk-keys button').forEach(function(b){b.addEventListener('click',function(){
      if(k.classList.contains('ok'))return;var t=b.getAttribute('data-k');
      if(t==='del')v=v.slice(0,-1);
      else if(t==='go'){
        if(!v)return;
        if(Math.abs(num(v)-num(k.getAttribute('data-a')))<1e-9){k.classList.add('ok');fb.textContent='✔ أحسنت! '+(k.getAttribute('data-w')||'');win(k);}
        else{shake(k);fb.textContent='✘ '+(k.getAttribute('data-h')||'حاول مرة أخرى');tone('no');}
        return;}
      else if(v.length<8&&!(t==='.'&&v.indexOf('.')>=0))v+=(t==='.'&&!v?'0.':t);
      out.textContent=v?ar(v):'؟';out.classList.toggle('empty',!v);fb.textContent='';k.classList.remove('no');tone('step');
    });});
  });

  // ─ اسحب ورتّب: تُسحب البطاقة بالإصبع أو الفأرة إلى مكانها، ثم «تحقّق» ─
  document.querySelectorAll('.ixo').forEach(function(o){
    guard(o);var list=o.querySelector('.ixo-l'),fb=o.querySelector('.ixo-fb'),drag=null,y0=0;
    function zoomOf(el){var z=1,e=el;while(e&&e!==document.body){var q=parseFloat(getComputedStyle(e).zoom);if(q>0)z*=q;e=e.parentElement;}return z;}
    // نقل البطاقة داخل الصفحة يُسقط «التقاط المؤشّر»، فالحركة والإفلات على مستوى الصفحة كلها
    function place(it,tv){it.style.transform='';var nt=it.getBoundingClientRect().top;it.style.transform='translateY('+((tv-nt)/zoomOf(it))+'px)';}
    function mv(e){if(!drag)return;var it=drag,tv=e.clientY-y0,hh=it.getBoundingClientRect().height,c=tv+hh/2,p=it.previousElementSibling,n=it.nextElementSibling;
      if(p){var pr=p.getBoundingClientRect();if(c<(pr.top+pr.bottom)/2){list.insertBefore(it,p);tone('step');}}
      if(n){var nr=n.getBoundingClientRect();if(c>(nr.top+nr.bottom)/2){list.insertBefore(n,it);tone('step');}}
      place(it,tv);}
    function up(){if(!drag)return;drag.classList.remove('drag');drag.style.transform='';drag=null;
      document.removeEventListener('pointermove',mv);document.removeEventListener('pointerup',up);document.removeEventListener('pointercancel',up);}
    list.querySelectorAll('.ixo-i').forEach(function(it){
      it.addEventListener('pointerdown',function(e){if(o.classList.contains('ok'))return;drag=it;y0=e.clientY-it.getBoundingClientRect().top;it.classList.add('drag');
        o.querySelectorAll('.ixo-i').forEach(function(x){x.classList.remove('good','bad');});fb.textContent='';
        document.addEventListener('pointermove',mv);document.addEventListener('pointerup',up);document.addEventListener('pointercancel',up);e.preventDefault();});
    });
    o.querySelector('.ixo-go').addEventListener('click',function(){
      var its=[].slice.call(list.querySelectorAll('.ixo-i')),all=true;
      its.forEach(function(x,i){var g=+x.getAttribute('data-i')===i;x.classList.toggle('good',g);x.classList.toggle('bad',!g);if(!g)all=false;});
      if(all){o.classList.add('ok');fb.textContent='✔ ترتيبٌ صحيح!';win(o);}
      else{fb.textContent='✘ البطاقات الحمراء في غير مكانها';tone('no');}
    });
  });

  // ─ طابق: المس مسألة ثم ناتجها ─
  var COLS=['#2563EB','#16A34A','#C2410C','#7C3AED','#DB2777','#0E7C86'];
  document.querySelectorAll('.ixm').forEach(function(m){
    guard(m);var sel=null,done=0,fb=m.querySelector('.ixm-fb'),tot=m.querySelectorAll('.ixm-a .ixm-i').length;
    m.querySelectorAll('.ixm-i').forEach(function(it){it.addEventListener('click',function(){
      if(it.classList.contains('m'))return;
      var side=it.parentNode.classList.contains('ixm-a')?'a':'b';
      if(!sel||sel.side===side){if(sel)sel.el.classList.remove('sel');sel={el:it,side:side};it.classList.add('sel');tone('step');return;}
      var other=sel.el;other.classList.remove('sel');sel=null;
      if(other.getAttribute('data-m')===it.getAttribute('data-m')){
        var c=COLS[done%COLS.length];[other,it].forEach(function(x){x.classList.add('m');x.style.borderColor=c;x.style.background=c+'1A';x.style.color=c;});
        done++;tone('ok');
        if(done===tot){fb.textContent='✔ طابقتَ كل المسائل!';win(m);}
      }else{shake(other);shake(it);tone('no');fb.className='ixm-fb bad';fb.textContent='✘ ليست هذه';setTimeout(function(){fb.textContent='';fb.className='ixm-fb';},1200);}
    });});
  });
})();
