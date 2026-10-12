/* رموز رياضية ملوّنة في زوايا كل شريحة — مواضع وألوان تتغيّر بين الشرائح،
   وتبقى دائماً في الأطراف (لا تقترب من منطقة المحتوى الوسطى). */
(function(){
  var SYM=['+','×','÷','=','√','٪','△','○','□','٢','٣','π','∞','★'];
  var COL=['#FFB703','#06D6A0','#4CC9F0','#F78C6B','#B388EB','#FF7AA2','#FFD166'];
  var SPOTS=[[4,6],[88,5],[3,78],[90,80],[46,3],[93,42],[2,44],[70,90],[22,90]];
  document.querySelectorAll('.slide').forEach(function(s,i){
    var n=5;
    for(var k=0;k<n;k++){
      var sp=SPOTS[(i*3+k*2)%SPOTS.length],d=document.createElement('span');
      d.className='dz';d.setAttribute('aria-hidden','true');
      d.textContent=SYM[(i*5+k*3)%SYM.length];
      d.style.color=COL[(i+k)%COL.length];
      d.style.fontSize=(4+((i+k*7)%4)*1.3)+'vh';
      d.style.left=sp[0]+'%';d.style.top=sp[1]+'%';
      d.style.transform='rotate('+(((i*37+k*53)%40)-20)+'deg)';
      d.style.setProperty('--r2',(((i+k)%2)?8:-8)+'deg');
      d.style.animationDelay=(-k*1.3)+'s';
      s.insertBefore(d,s.firstChild);
    }
    // لون قلم التحديد يتبدّل بين الشرائح
    var hl=['rgba(255,209,102,.6)','rgba(76,201,240,.35)','rgba(255,122,162,.35)','rgba(6,214,160,.35)','rgba(179,136,235,.35)'][i%5];
    s.style.setProperty('--hl',hl);
  });
})();

// صمّام الأمان: إن تجاوز محتوى شريحةٍ ارتفاع الشاشة (مع كشف كل الخطوات والبطاقات) صُغِّر قليلاً — حتى ٠٫٦، ويشمل خروج سطرٍ من مربّعه
(function(){
  function fitAll(){
    document.querySelectorAll('.slide').forEach(function(s){
      s.style.setProperty('--fit',1);s.classList.add('fit-m');   // يُرسَم مؤقتاً للقياس رغم content-visibility
      var fl=[].slice.call(s.querySelectorAll('.flip:not(.open)'));fl.forEach(function(e){e.classList.add('open');});
      for(var k=0;k<6;k++){
        var cs=getComputedStyle(s),r=s.getBoundingClientRect(),top=1e9,bot=-1e9,lf=1e9,rt=-1e9;
        // كل العناصر لا الأبناء المباشرون فقط: سطرٌ رياضي أعرض من مربّعه يُحسب أيضاً (ما عدا الزخارف والملاحظات والعناصر المطلقة)
        (function walk(p){[].forEach.call(p.children,function(c){if(c.classList.contains('dz')||c.tagName==='ASIDE'||getComputedStyle(c).position==='absolute')return;var b=c.getBoundingClientRect();if(b.height&&b.width){top=Math.min(top,b.top);bot=Math.max(bot,b.bottom);lf=Math.min(lf,b.left);rt=Math.max(rt,b.right);}walk(c);});})(s);
        var H=r.height-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom),W=r.width-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
        var cx=r.left+r.width/2,f=+(s.style.getPropertyValue('--fit')||1),need=Math.min(H/(bot-top),W/(rt-lf),(W/2)/Math.max(cx-lf,rt-cx));  // والخروج من جهةٍ واحدة (شبكة RTL تفيض يساراً)
        [].forEach.call(s.querySelectorAll('.box,.xcard,.err,.opt'),function(b){if(b.clientWidth&&b.scrollWidth>b.clientWidth+2)need=Math.min(need,b.clientWidth/b.scrollWidth);});  // سطرٌ أعرض من مربّعه
        if(need>=1)break;
        s.style.setProperty('--fit',Math.max(.6,f*need*.99).toFixed(3));
      }
      fl.forEach(function(e){e.classList.remove('open');});s.classList.remove('fit-m');
    });
  }
  window.__fitAll=fitAll;fitAll();
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fitAll);
  var t;addEventListener('resize',function(){clearTimeout(t);t=setTimeout(fitAll,150);});
})();
