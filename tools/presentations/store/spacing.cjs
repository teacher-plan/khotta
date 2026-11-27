// قياس راحة البصر لملفات المخزن (بالملّيمتر): الهامش الجانبي، أقل مسافة بين الكتل، المسافة قبل التذييل، أقل حشوٍ داخل الصناديق، وتراكب النصوص.
// NODE_PATH=$(npm root -g) node tools/presentations/store/spacing.cjs <مجلد ملفات HTML>
// الحدود المقبولة: هامش ≥ ١٣ · مسافة ≥ ٢٫٨ · قبل التذييل ≥ ٠ (الحشو السفلي ٦ ملم محسوبٌ أصلاً) · حشو ≥ ١٫٥ · تراكب = لا شيء
// قياس الهوامش والمسافات والتراكب في كل صفحة A4 (بالملّيمتر)
const {chromium}=require('playwright');const fs=require('fs'),path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:900,height:1200}});
for(const f of fs.readdirSync(process.argv[2]).filter(x=>x.endsWith('.html'))){
 await p.goto('file://'+path.join(process.argv[2],f));await p.evaluate(()=>document.fonts.ready);await p.evaluate(()=>window.__fit||null);
 const r=await p.evaluate(()=>{const mm=v=>Math.round(v/3.7795*10)/10;const out=[];
  document.querySelectorAll('.page').forEach((pg,pi)=>{const P=pg.getBoundingClientRect();const body=pg.querySelector('.body'),ft=pg.querySelector('footer');
   const kids=[...body.children].filter(e=>e.getBoundingClientRect().height>2);
   // هامش جانبي: أقرب نصّ/صندوق لحافّة الورقة
   let minSide=1e9;pg.querySelectorAll('.body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width<2||r.height<2)return;minSide=Math.min(minSide,r.left-P.left,P.right-r.right);});
   // المسافة بين الكتل المتتالية
   let minGap=1e9;for(let i=1;i<kids.length;i++){minGap=Math.min(minGap,kids[i].getBoundingClientRect().top-kids[i-1].getBoundingClientRect().bottom);}
   // المسافة بين آخر كتلة والتذييل
   const last=kids.length?kids[kids.length-1].getBoundingClientRect().bottom:0;const toFoot=ft.getBoundingClientRect().top-last;
   // الحشو الداخلي للصناديق: أقرب نصّ لحدّ صندوقه
   let minPad=1e9,where='';pg.querySelectorAll('.rule,.ex,.warn,.pr,.qq,.goal,.tb,.gt,.ki,.mc>span').forEach(box=>{const B=box.getBoundingClientRect();
     const w=document.createTreeWalker(box,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(!n.textContent.trim())continue;const rg=document.createRange();rg.selectNodeContents(n);for(const r of rg.getClientRects()){
       const d=Math.min(r.left-B.left,B.right-r.right,r.top-B.top,B.bottom-r.bottom);if(d<minPad){minPad=d;where=box.className+' «'+n.textContent.trim().slice(0,18)+'»';}}}});
   // تراكب نصّين
   const rects=[];const w=document.createTreeWalker(pg,NodeFilter.SHOW_TEXT);let n;while(n=w.nextNode()){if(!n.textContent.trim())continue;const rg=document.createRange();rg.selectNodeContents(n);for(const r of rg.getClientRects())if(r.width>1)rects.push([r,n.textContent.trim().slice(0,14)]);}
   let ov=[];for(let i=0;i<rects.length;i++)for(let j=i+1;j<rects.length;j++){const a=rects[i][0],c=rects[j][0];const ix=Math.min(a.right,c.right)-Math.max(a.left,c.left),iy=Math.min(a.bottom,c.bottom)-Math.max(a.top,c.top);if(ix>2&&iy>3)ov.push(rects[i][1]+'×'+rects[j][1]);}
   out.push({p:pi+1,side:mm(minSide),gap:mm(minGap),toFoot:mm(toFoot),pad:mm(minPad),padAt:where.slice(0,50),overlap:ov.slice(0,3)});});return out;});
 console.log('\n'+f);for(const x of r)console.log(`  ص${x.p}: هامش جانبي ${x.side} · أقل مسافة بين الكتل ${x.gap} · قبل التذييل ${x.toFoot} · أقل حشو ${x.pad} (${x.padAt})${x.overlap.length?' · تراكب: '+x.overlap.join('، '):''}`);}
await b.close();})();
