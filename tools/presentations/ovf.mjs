import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const b=await chromium.launch();
// الاستخدام: node tools/presentations/ovf.mjs ملف١.html [ملف٢.html…]
for(const f of process.argv.slice(2))for(const [w,h] of [[1280,720],[1366,768]]){
const p=await b.newPage({viewport:{width:w,height:h}});
await p.setContent(fs.readFileSync(f,'utf8'));await p.waitForTimeout(300);
const r=await p.evaluate(()=>{const out=[];const H=innerHeight,W=innerWidth;
 document.querySelectorAll('.slide').forEach((s,i)=>{
  s.querySelectorAll('.st,.st-t').forEach(e=>e.classList.add('in'));
  s.querySelectorAll('.flip').forEach(e=>e.classList.add('open'));
  s.querySelectorAll('.sq').forEach(e=>e.classList.add('open'));
  s.style.transition='none';s.classList.add('on');
  let top=1e9,bot=-1e9,l=1e9,rr=-1e9;s.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width)return;top=Math.min(top,r.top);bot=Math.max(bot,r.bottom);l=Math.min(l,r.left);rr=Math.max(rr,r.right);});
  if(top<0||bot>H+1||l<0||rr>W+1)out.push(`${i+1}: top${Math.round(top)} bot${Math.round(bot)}/${H} l${Math.round(l)} r${Math.round(rr)}/${W}`);
  s.classList.remove('on');});return out;});
console.log(f.split('/').pop(),w,h,r.length?r:'OK');await p.close();}
await b.close();
