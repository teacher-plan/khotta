// نسخةٌ مطابقة لـ gmSpellFix في cycle1.html — أيّ تعديلٍ هنا يُنقل هناك.
// ── إصلاح خيارات «انظر وتذكّر» ──
// النموذج كثيراً ما يكرّر الكلمة الصحيحة في الخيارات الأربعة (أو يكتبها
// بتشكيلٍ مختلف فقط)، فتبدو كلّها متشابهة ولا خطأ فيها. نُبقي الصحيحة مرّةً
// واحدة، ونحذف كل خيارٍ يطابقها أو يطابق غيره بعد حذف التشكيل، ونكمل الناقص
// بأخطاءٍ إملائيةٍ شائعة تُولَّد بقواعد ثابتة.
// deno-lint-ignore-file no-explicit-any no-var
var GM_SP_STRIP=/[ً-ْٰـ]/g;
function gmSpNorm(s: any){return String(s||'').replace(GM_SP_STRIP,'').trim();}
function gmSpMutations(w: string){
  var out: string[]=[],add=function(x: string){if(x&&x!==w)out.push(x);};
  var last=w.slice(-1),body=w.slice(0,-1);
  if(last==='ة'){add(body+'ه');add(body+'ت');}
  if(last==='ه'&&w.length>2)add(body+'ة');
  if(last==='ى')add(body+'ي');
  if(last==='ي'&&w.length>2)add(body+'ى');
  if(/ا$/.test(w)&&w.length>3)add(w.slice(0,-1)+'ن');
  var hasAl=w.indexOf('ال')===0&&w.length>3,stem=hasAl?w.slice(2):w,pre=hasAl?'ال':'';
  if(hasAl&&'تثدذرزسشصضطظلن'.indexOf(stem[0])>=0)add('ا'+stem);
  if(stem[0]==='ا'){add(pre+'أ'+stem.slice(1));add(pre+'إ'+stem.slice(1));}
  if(stem[0]==='أ'||stem[0]==='إ')add(pre+'ا'+stem.slice(1));
  if(stem[0]==='آ')add(pre+'ءا'+stem.slice(1));
  var SW: Record<string,string>={'ث':'س','س':'ث','ذ':'ز','ز':'ذ','ض':'ظ','ظ':'ض','ت':'ط','ط':'ت','ص':'س','ق':'ك','ئ':'ء','ؤ':'ء','ح':'ه'};
  for(var i=pre.length;i<w.length;i++){var r=SW[w[i]];if(r){add(w.slice(0,i)+r+w.slice(i+1));}}
  for(var j=pre.length+1;j<w.length-1;j++){if('اوي'.indexOf(w[j])>=0){add(w.slice(0,j)+w.slice(j+1));break;}}
  if(stem.length>=3&&'اأإآ'.indexOf(stem[0])<0&&stem[1]!=='ا')add(pre+stem[0]+'ا'+stem.slice(1));
  return out;
}
export function gmSpellFix(items: any[]){
  return (items||[]).map(function(it: any){
    if(!it||!Array.isArray(it.c))return it;
    var right=String(it.c[it.a||0]||it.w||'').trim(),rn=gmSpNorm(right);
    if(!rn)return it;
    var seen: Record<string,number>={},wrong: string[]=[];seen[rn]=1;
    it.c.forEach(function(x: any){var n=gmSpNorm(x);if(n&&!seen[n]){seen[n]=1;wrong.push(String(x).trim());}});
    if(wrong.length<3)gmSpMutations(gmSpNorm(right)).forEach(function(x: string){if(wrong.length<3&&!seen[x]){seen[x]=1;wrong.push(x);}});
    wrong=wrong.slice(0,3);
    var c=wrong.concat([right]);
    for(var k=c.length-1;k>0;k--){var m=Math.floor(Math.random()*(k+1)),t=c[k];c[k]=c[m];c[m]=t;}
    var o: any={};for(var p in it)o[p]=it[p];o.c=c;o.a=c.indexOf(right);return o;
  });
}
