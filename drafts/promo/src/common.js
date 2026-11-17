// shared helpers for Khotta promo films — every value is a pure function of t
const Q=new URLSearchParams(location.search);
const W=+Q.get('w')||1920,H=+Q.get('h')||1080,V=H>W;
const OUT=document.getElementById('c');OUT.width=W;OUT.height=H;const OX_=OUT.getContext('2d');
const WC=document.createElement('canvas');WC.width=W;WC.height=H;const X=WC.getContext('2d');
const u=Math.min(W,H)/1080,cx=W/2,cy=H/2;
const P={cream:'#F1E3C8',paper:'#EFE4CC',green:'#5B8F5B',dgreen:'#2F5A36',gold:'#C9A84A',brown:'#3D2416',coral:'#E8664A',crim:'#B03040',dark:'#1A0F09',line:'#CDB98E',white:'#F7F2E8'};
const cl=(v,a=0,b=1)=>Math.min(b,Math.max(a,v)),seg=(t,a,b)=>cl((t-a)/(b-a)),mix=(a,b,k)=>a+(b-a)*k;
const crit=(x,w=14)=>x<=0?0:1-(1+w*x)*Math.exp(-w*x);
const under=(x,w=16,z=.62)=>{if(x<=0)return 0;const wd=w*Math.sqrt(1-z*z);return 1-Math.exp(-z*w*x)*(Math.cos(wd*x)+z*w/wd*Math.sin(wd*x))};
const expo=x=>x<=0?0:x>=1?1:x<.5?Math.pow(2,20*x-10)/2:(2-Math.pow(2,-20*x+10))/2;
const ein=x=>x<=0?0:x>=1?1:Math.pow(2,10*x-10);
function rnd(s){return()=>{s|=0;s=s+0x6D2B79F5|0;let t=Math.imul(s^s>>>15,1|s);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function rr(x,y,w,h,r,c=X){c.beginPath();c.roundRect(x,y,w,h,Math.max(0,Math.min(r,Math.abs(w)/2,Math.abs(h)/2)))}
function font(size,o={}){return `${o.w||900} ${size}px ${o.f||'Cairo'}`}
function measure(s,size,o={}){X.save();X.font=font(size,o);if(o.ls)X.letterSpacing=o.ls+'px';const m=X.measureText(s).width;X.restore();return m}
// fit: largest size <= max that fits maxW
function fit(s,max,maxW,o={}){const m=measure(s,max,o);return m>maxW?max*maxW/m:max}
function txt(s,x,y,size,col,o={},c=X){c.save();c.font=font(size,o);c.textAlign=o.al||'center';c.textBaseline=o.bl||'alphabetic';c.direction=o.ltr?'ltr':'rtl';if(o.ls)c.letterSpacing=o.ls+'px';c.fillStyle=col;c.globalAlpha*=o.a??1;c.fillText(s,x,y);c.restore()}
const LOGO='خُطّة';
const TL=[[44,42,156,146,'green'],[170,42,258,248,'gold'],[272,42,376,146,'brown'],[390,42,466,146,'outline'],[44,160,156,248,'coral'],[272,160,376,248,'crim'],[404,160,466,248,'brown']];
// icon tiles centred at (x,y) with total width w
function tilesAt(x,y,w){const s=w/422;return TL.map(([a,b,c,d,k])=>({x:x+(a-255)*s,y:y+(b-145)*s,w:(c-a)*s,h:(d-b)*s,k,s}))}
function drawTile(T,o={}){const {sc=1,a=1,dx=0,dy=0,rot=0,col}=o;if(a<=0||sc<=0)return;X.save();X.globalAlpha*=a;X.translate(T.x+T.w/2+dx,T.y+T.h/2+dy);X.rotate(rot);X.scale(sc,sc);rr(-T.w/2,-T.h/2,T.w,T.h,26*T.s);
 if(T.k==='outline'){X.lineWidth=Math.max(2,5*T.s);X.strokeStyle=col||P.line;X.stroke()}else{X.fillStyle=col||P[T.k];X.fill()}X.restore()}
window.frame=(t,sub=2)=>{OX_.globalAlpha=1;for(let k=0;k<sub;k++){X.save();X.filter='none';X.globalAlpha=1;X.globalCompositeOperation='source-over';render(t+k/(60*sub));X.restore();OX_.globalAlpha=1/(k+1);OX_.drawImage(WC,0,0)}OX_.globalAlpha=1};
window.ready=document.fonts.load('900 100px Cairo').then(()=>Promise.all(['800 40px Tajawal','500 30px "IBM Plex Mono"','600 30px Cairo','700 30px Cairo'].map(f=>document.fonts.load(f)))).then(()=>document.fonts.ready).then(()=>true);
