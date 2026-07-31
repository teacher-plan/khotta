/* يُولّد demo.html من cycle1.html بحقن راية وضع التجربة.
   نسخةٌ مولّدة لا مكتوبة بيد — فلا يمكن أن تنحرف عن المنتج.
   يُعاد تشغيله آلياً عند كل تعديل على cycle1.html (انظر .github/workflows). */
import fs from 'fs';
const SRC='cycle1.html', OUT='demo.html';
const h=fs.readFileSync(SRC,'utf8');
const anchor='<script>\n// ══ الأساسيات ══';
if(!h.includes(anchor)){console.error('لم أجد موضع الحقن في '+SRC);process.exit(1);}
if(!h.includes('const KH_DEMO=!!window.KH_DEMO;')){
  console.error('وضع التجربة غير موجود في '+SRC+' — أُلغي التوليد بدل إنتاج نسخةٍ تطلب تسجيل دخول');
  process.exit(1);
}
const out=h.replace(anchor,'<script>window.KH_DEMO=true;<\/script>\n'+anchor)
  .replace('<title>','<title>تجربة خُطّة — ');
fs.writeFileSync(OUT,out);
console.log('وُلِّد '+OUT+' ('+(out.length/1024).toFixed(0)+'ك)');
