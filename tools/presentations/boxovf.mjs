// الاستخدام: node tools/presentations/boxovf.mjs ملف.html … — يبلّغ عن سطرٍ يخرج من مربّعه (بطاقة، مربّع، خطوة) أو عن الشاشة،
// على مقاسات iPad (أفقي وعمودي، داخل إطار منصّة «خطة») وشاشة 1280×720. ظهر خطأ «النص خارج الإطار» على iPad الأستاذ عيسى.
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const b=await chromium.launch();
const sizes=[[1180,820],[1180,700],[820,1000],[1280,720]];
for(const f of process.argv.slice(2))for(const [w,h] of sizes){
const p=await b.newPage({viewport:{width:w,height:h}});
await p.setContent(fs.readFileSync(f,'utf8'));await p.waitForTimeout(400);
const r=await p.evaluate(()=>{const out=[];
 document.querySelectorAll('.slide').forEach((s,i)=>{
  s.querySelectorAll('.st,.st-t').forEach(e=>e.classList.add('in'));
  s.querySelectorAll('.flip').forEach(e=>e.classList.add('open'));
  s.style.transition='none';s.classList.add('on');
  let bad=0;
  s.querySelectorAll('.box,.xcard,.err,.stp,.opt,.exit .st>div,.flip').forEach(bx=>{const R=bx.getBoundingClientRect();if(!R.width)return;
    bx.querySelectorAll('*').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width)return;if(r.left<R.left-2||r.right>R.right+2)bad=Math.max(bad,Math.round(Math.max(R.left-r.left,r.right-R.right)));});});
  let l=1e9,rr=-1e9;s.querySelectorAll('*:not(.dz)').forEach(e=>{const r=e.getBoundingClientRect();if(!r.width)return;l=Math.min(l,r.left);rr=Math.max(rr,r.right);});
  if(bad||l<0||rr>innerWidth+1)out.push(`${i+1}:box+${bad} l${Math.round(l)} r${Math.round(rr)}`);
  s.classList.remove('on');});return out;});
console.log(f.split('/').pop(),w,h,r.length?r.join(' '):'OK');await p.close();}
await b.close();
