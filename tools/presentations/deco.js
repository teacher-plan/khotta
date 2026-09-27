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
