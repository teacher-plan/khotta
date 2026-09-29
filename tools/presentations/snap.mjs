// لقطات لشرائح مختارة مكشوفة الخطوات: node snap.mjs ملف.html مجلد_الإخراج [أرقام…]
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import fs from 'fs';
const [f,out,...nums]=process.argv.slice(2);fs.mkdirSync(out,{recursive:true});
const b=await chromium.launch({proxy:process.env.HTTPS_PROXY?{server:process.env.HTTPS_PROXY}:undefined});
const p=await b.newPage({viewport:{width:+(process.env.W||1280),height:+(process.env.H||720)}});
const html=fs.readFileSync(f,'utf8');
await p.route('http://deck.local/**',r=>r.fulfill({contentType:'text/html',body:html}));
await p.goto('http://deck.local/x.html');await p.waitForTimeout(2000);
const n=await p.evaluate(()=>document.querySelectorAll('.slide').length);
const list=nums.length?nums.map(Number):[...Array(n).keys()].map(i=>i+1);
for(const i of list){
  await p.evaluate(i=>{document.querySelectorAll('.slide').forEach((s,k)=>{s.style.transition='none';s.classList.toggle('on',k===i-1);});
    const s=document.querySelectorAll('.slide')[i-1];s.querySelectorAll('.st,.st-t').forEach(e=>{e.style.transition='none';e.classList.add('in');});
    s.querySelectorAll('.flip').forEach(e=>e.classList.add('open'));if(window.__openSq)s.querySelectorAll('.sq').forEach(e=>e.classList.add('open'));},i);
  await p.waitForTimeout(900);await p.screenshot({path:`${out}/s${String(i).padStart(2,'0')}.png`});
}
await b.close();
