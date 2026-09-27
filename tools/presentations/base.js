
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide')),cur=0;
  // الخطوات: عناصر .st، ومستويات الشجرة .st-t بترتيب ظهورها في الشريحة
  function steps(s){return [].slice.call(s.querySelectorAll('.st,.st-t'));}
  function act(el,on){
    var a=el.getAttribute('data-act');if(!a)return;
    var p=a.split(':'),t=document.getElementById(p[0]);if(!t)return;
    p[1].split(',').forEach(function(c){
      var rm=c.charAt(0)==='-',k=rm?c.slice(1):c;
      if(on)t.classList.toggle(k,!rm);else t.classList.toggle(k,rm);
    });
  }
  function show(el,on){
    el.classList.toggle('in',on);
    var a=el.getAttribute('data-act');
    if(a&&/:done$/.test(a)){var m=document.getElementById(a.split(':')[0]);
      if(on){m.classList.add('go');setTimeout(function(){if(el.classList.contains('in'))m.classList.add('done');},650);}
      else m.classList.remove('go','done');return;}
    act(el,on);
  }
  function go(i,fromBack){
    i=Math.max(0,Math.min(slides.length-1,i));
    slides.forEach(function(s,k){s.classList.toggle('on',k===i);s.classList.toggle('gone',k<i);});
    var st=steps(slides[i]);st.forEach(function(e){show(e,!!fromBack);});
    cur=i;ui();
  }
  function next(){
    var h=steps(slides[cur]).filter(function(e){return !e.classList.contains('in');});
    if(h.length){show(h[0],true);tone('step');ui();return;}
    if(cur<slides.length-1){go(cur+1);tone('slide');}
  }
  function prev(){
    var v=steps(slides[cur]).filter(function(e){return e.classList.contains('in');});
    if(v.length){show(v[v.length-1],false);ui();return;}
    if(cur>0)go(cur-1,true);
  }
  function ui(){
    document.getElementById('cnt').textContent=ar(cur+1)+' / '+ar(slides.length);
    var st=steps(slides[cur]),done=st.filter(function(e){return e.classList.contains('in');}).length;
    var f=(cur+(st.length?done/st.length:1))/slides.length;
    document.getElementById('pg').style.width=Math.max(3,f*100)+'%';
  }
  function ar(n){return String(n).replace(/\d/g,function(d){return '٠١٢٣٤٥٦٧٨٩'[d];});}

  // ─ الأسئلة ─
  document.querySelectorAll('.q').forEach(function(q){
    var ok=+q.getAttribute('data-ok'),fb=q.nextElementSibling,bs=[].slice.call(q.querySelectorAll('.ch'));
    bs.forEach(function(b,i){b.addEventListener('click',function(e){
      e.stopPropagation();
      if(q.classList.contains('solved'))return;
      if(i===ok){
        q.classList.add('solved');b.classList.add('ok');bs.forEach(function(x){if(x!==b)x.classList.add('dim');});
        fb.className='fb ok';fb.innerHTML='✔ أحسنت! '+fb.getAttribute('data-why');tone('ok');confetti();
      }else{
        b.classList.remove('no');void b.offsetWidth;b.classList.add('no');
        fb.className='fb no';fb.textContent='✘ حاول مرة أخرى';tone('no');
      }
    });});
  });
  document.querySelectorAll('.flip').forEach(function(f){f.addEventListener('click',function(e){e.stopPropagation();if(!f.classList.contains('open')){f.classList.add('open');tone('ok');}});});

  // ─ التحكم ─
  document.getElementById('next').onclick=next;
  document.getElementById('prev').onclick=prev;
  document.getElementById('fs').onclick=function(){
    var d=document;if(d.fullscreenElement)d.exitFullscreen();else if(d.documentElement.requestFullscreen)d.documentElement.requestFullscreen().catch(function(){});
  };
  document.addEventListener('keydown',function(e){
    if(e.key==='ArrowLeft'||e.key===' '||e.key==='PageDown'||e.key==='Enter'){e.preventDefault();next();}
    else if(e.key==='ArrowRight'||e.key==='PageUp'||e.key==='Backspace'){e.preventDefault();prev();}
  });
  // السحب بالإصبع: يساراً = التالي، يميناً = السابق (كتقليب صفحة عربية)
  var sx=null,sy=null;
  document.getElementById('deck').addEventListener('pointerdown',function(e){if(e.pointerType==='touch'){sx=e.clientX;sy=e.clientY;}});
  document.getElementById('deck').addEventListener('pointerup',function(e){
    if(sx==null)return;var dx=e.clientX-sx,dy=e.clientY-sy;sx=null;
    if(Math.abs(dx)>60&&Math.abs(dx)>Math.abs(dy)*1.3){dx<0?next():prev();}
  });

  // ─ أصوات مُركّبة (لا ملفات) ─
  var AC=null;
  function tone(k){
    try{
      AC=AC||new (window.AudioContext||window.webkitAudioContext)();if(AC.state==='suspended')AC.resume();
      var seq={ok:[[1047,0],[1568,.09]],no:[[196,0],[165,.12]],step:[[880,0]],slide:[[660,0],[990,.05]]}[k]||[];
      seq.forEach(function(n){
        var o=AC.createOscillator(),g=AC.createGain(),t=AC.currentTime+n[1];
        o.type=k==='no'?'triangle':'sine';o.frequency.value=n[0];
        var v=k==='step'?.05:k==='slide'?.06:.16,d=k==='no'?.25:.35;
        g.gain.setValueAtTime(0,t);g.gain.linearRampToValueAtTime(v,t+.01);g.gain.exponentialRampToValueAtTime(.0001,t+d);
        o.connect(g);g.connect(AC.destination);o.start(t);o.stop(t+d+.02);
      });
    }catch(e){}
  }
  // ─ احتفال بسيط ─
  function confetti(){
    var c=document.getElementById('fx'),x=c.getContext('2d');c.width=innerWidth;c.height=innerHeight;
    var cols=['#0E7C86','#E0533D','#E9A23B','#7A3FD1','#1C9A55'],P=[];
    for(var i=0;i<120;i++)P.push({x:innerWidth/2,y:innerHeight*.45,vx:(Math.random()-.5)*16,vy:-Math.random()*15-4,r:Math.random()*7+4,c:cols[i%5],a:Math.random()*6});
    var t=0;(function f(){x.clearRect(0,0,c.width,c.height);P.forEach(function(p){p.vy+=.45;p.x+=p.vx;p.y+=p.vy;p.a+=.2;
      x.save();x.translate(p.x,p.y);x.rotate(p.a);x.fillStyle=p.c;x.fillRect(-p.r/2,-p.r/4,p.r,p.r/2);x.restore();});
      if(++t<90)requestAnimationFrame(f);else x.clearRect(0,0,c.width,c.height);})();
  }
  go(0);
})();
