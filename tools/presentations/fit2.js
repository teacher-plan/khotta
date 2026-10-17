// الحجم المتناسق (FIT2): يحلّ محلّ صمّام deco.js. لكل شريحة (مع كشف كل الخطوات والبطاقات):
// ١) سطرٌ قصير أو عددٌ لا يلتفّ (.nowr)؛ ٢) كتلةٌ أعرض من مربّعها يصغر خطّها وحدها (حتى ٦٠٪)؛
// ٣) إن تجاوز المحتوى الإطار الآمن (داخل هوامش الشريحة) صُغِّرت الشريحة كلها (حتى ٥٠٪) — فيبقى دائماً فراغٌ بين آخر سطر وحدّ الشاشة.
(function(){
  var PROSE='.lead,.note,.rule,.ask,.hint,.can,.fb,.pq,.rulecard,.xrule,p,.tnote,aside';
  document.querySelectorAll('.slide *').forEach(function(e){
    if(e.closest(PROSE))return;
    var t='';e.childNodes.forEach(function(n){if(n.nodeType===3)t+=n.textContent;});
    if(t.trim()&&e.textContent.trim().length<=34)e.classList.add('nowr');
  });
  function skip(e){return e.classList.contains('dz')||e.tagName==='ASIDE'||getComputedStyle(e).position==='absolute';}
  function shrinkBlocks(s){
    var els=[].slice.call(s.querySelectorAll('*')).reverse(),hit=false;
    els.forEach(function(e){
      if(skip(e)||!e.clientWidth)return;var cs=getComputedStyle(e);if(cs.overflowX!=='visible'||cs.display==='inline')return;
      var cw=e.clientWidth,sw=e.scrollWidth;if(sw<=cw+2)return;
      var r=Math.max(.6,cw/sw*.97),kids=[].filter.call(e.children,function(c){return !skip(c);});
      if(!kids.length)return;hit=true;
      kids.forEach(function(c){c.style.zoom=((parseFloat(c.style.zoom)||1)*r).toFixed(3);c.setAttribute('data-shr','');});
    });
    return hit;
  }
  function box(s){var top=1e9,bot=-1e9,lf=1e9,rt=-1e9;
    (function walk(p){[].forEach.call(p.children,function(c){if(skip(c))return;var b=c.getBoundingClientRect();if(b.height&&b.width){top=Math.min(top,b.top);bot=Math.max(bot,b.bottom);lf=Math.min(lf,b.left);rt=Math.max(rt,b.right);}walk(c);});})(s);
    return {top:top,bot:bot,lf:lf,rt:rt};}
  function fitSlide(s){
    s.style.setProperty('--fit',1);s.classList.add('fit-m');
    [].forEach.call(s.querySelectorAll('[data-shr]'),function(e){e.style.zoom='';e.removeAttribute('data-shr');});
    var fl=[].slice.call(s.querySelectorAll('.flip:not(.open)'));fl.forEach(function(e){e.classList.add('open');});
    for(var k=0;k<4&&shrinkBlocks(s);k++);
    for(k=0;k<6;k++){
      var cs=getComputedStyle(s),r=s.getBoundingClientRect(),b=box(s);
      var H=r.height-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom),W=r.width-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
      var cx=r.left+parseFloat(cs.paddingLeft)+W/2,f=+(s.style.getPropertyValue('--fit')||1);
      var need=Math.min(H/(b.bot-b.top),(W/2)/Math.max(cx-b.lf,b.rt-cx,1));
      if(need>=1)break;
      s.style.setProperty('--fit',Math.max(.5,f*need*.98).toFixed(3));
    }
    fl.forEach(function(e){e.classList.remove('open');});s.classList.remove('fit-m');
  }
  function fitAll(){document.querySelectorAll('.slide').forEach(fitSlide);}
  window.__fitAll=fitAll;fitAll();
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fitAll);
})();
