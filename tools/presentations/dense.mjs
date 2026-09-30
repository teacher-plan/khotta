// فحص الازدحام: الشرائح التي صغّرها صمّام الأمان (--fit < 1) أو التي يملأ محتواها أكثر من ٨٥٪ من ارتفاع الشاشة بعد كشف كل الخطوات.
// node tools/presentations/dense.mjs ملف.html [ملف…]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const b=await chromium.launch();
for(const f of process.argv.slice(2)){
 const p=await b.newPage({viewport:{width:1280,height:720}});
 await p.setContent(fs.readFileSync(f,'utf8'));await p.waitForTimeout(500);
 const r=await p.evaluate(()=>{const out=[];const H=innerHeight;
  document.querySelectorAll('.slide').forEach((s,i)=>{
   s.querySelectorAll('.st,.st-t').forEach(e=>e.classList.add('in'));s.querySelectorAll('.flip').forEach(e=>e.classList.add('open'));
   s.style.transition='none';s.classList.add('on');
   let top=1e9,bot=-1e9;[...s.children].forEach(c=>{if(c.classList.contains('dz')||getComputedStyle(c).position==='absolute')return;const r=c.getBoundingClientRect();if(!r.height)return;top=Math.min(top,r.top);bot=Math.max(bot,r.bottom);});
   const fit=+(s.style.getPropertyValue('--fit')||1),fill=(bot-top)/H,blocks=s.children.length;
   if(fit<1||fill>.85)out.push(`${i+1}: fit ${fit} · ملء ${Math.round(fill*100)}٪ · ${s.querySelector('h1,h2,.lh')?.textContent.trim().slice(0,40)||''}`);
   s.classList.remove('on');});return out;});
 console.log(f.split('/').pop(), r.length, 'شريحة مزدحمة');r.forEach(x=>console.log('  '+x));await p.close();}
await b.close();
