#!/usr/bin/env node
// فحصٌ بنيويّ لصفحات المنصة قبل النشر.
//
// سببُ وجوده: تعديلٌ بتعبيرٍ نمطيّ حذف جزءاً من سطرٍ يبدأ بـ@media، فبقي
// الاستعلام مفتوحاً وابتلع كلَّ ما بعده من قواعد. الصفحة لم تُخطئ ولم
// تتوقّف — عُرضت بلا تنسيقٍ إطلاقاً، ولا شيء في البناء لاحظ ذلك. الخطأ
// الصامت لا يُكتشف إلا بعينٍ تنظر، وقد لا تنظر إلا بعد أن تراه معلّمة.
//
// يفحص ثلاثة أشياء تُكسر بالتعديل النصّي ولا يلحظها شيءٌ آخر:
//   ١) توازن الأقواس في كل كتلة <style>
//   ٢) التعليقات غير المغلقة داخلها
//   ٣) توازن الأقواس في كل كتلة <script>
//
// يخرج بحالة ١ عند أي خلل، فيوقف سير العمل قبل أن يصل إلى المعلّمات.

import fs from 'node:fs';

// اكتشافٌ تلقائيّ لا قائمةٌ مكتوبة: القائمة الثابتة تفوّت ما يُضاف بعدها،
// وأوّلُ ما فاتها index.html — أكبر صفحةٍ في المستودع.
function findHtml(dir, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (e.name === 'node_modules' || e.name === '.git' || e.name.startsWith('.')) continue;
    const p = dir === '.' ? e.name : `${dir}/${e.name}`;
    if (e.isDirectory()) findHtml(p, out);
    else if (e.name.endsWith('.html')) out.push(p);
  }
  return out;
}

const FILES = process.argv.slice(2).length ? process.argv.slice(2) : findHtml('.').sort();

let failed = 0;

/** يزيل التعليقات كي لا تُحسب أقواسها، ويُبقي طول النصّ لتحديد السطر */
function stripCssComments(css) {
  return css.replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '));
}

/** رقم السطر الذي فُتح فيه قوسٌ لم يُغلق */
function unclosedAt(text, offsetLine) {
  const stack = [];
  let line = offsetLine;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (c === '\n') line++;
    else if (c === '{') stack.push(line);
    else if (c === '}') stack.pop();
  }
  return stack.length ? stack[0] : null;
}

for (const file of FILES) {
  if (!fs.existsSync(file)) continue;
  const src = fs.readFileSync(file, 'utf8');
  const problems = [];

  // ── كتل التنسيق ──
  for (const m of src.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)) {
    const raw = m.group ?? m[1];
    const startLine = src.slice(0, m.index).split('\n').length;

    if ((raw.match(/\/\*/g) || []).length !== (raw.match(/\*\//g) || []).length) {
      problems.push(`تعليق CSS غير مغلق في الكتلة التي تبدأ عند السطر ${startLine}`);
    }

    const clean = stripCssComments(raw);
    const open = (clean.match(/\{/g) || []).length;
    const close = (clean.match(/\}/g) || []).length;
    if (open !== close) {
      const at = unclosedAt(clean, startLine);
      problems.push(
        `أقواس CSS غير متوازنة (${open} فتح / ${close} إغلاق)` +
        (at ? ` — القاعدة المفتوحة تبدأ عند السطر ${at}` : '')
      );
    }

    // استعلامٌ فارغ: أثرُ حذفٍ أزال محتواه وترك غلافه
    for (const e of clean.matchAll(/@(?:media|supports)[^{\n]*\{\s*\}/g)) {
      problems.push(`استعلام فارغ (بقايا حذف): ${e[0].slice(0, 60).trim()}`);
    }
  }

  // ── كتل السكربت ──
  for (const m of src.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)) {
    const startLine = src.slice(0, m.index).split('\n').length;
    try {
      new Function(m[1]);
    } catch (e) {
      problems.push(`خطأ نحويّ في السكربت الذي يبدأ عند السطر ${startLine}: ${e.message}`);
    }
  }

  if (problems.length) {
    failed++;
    console.error(`\n🔴 ${file}`);
    problems.forEach((p) => console.error(`   • ${p}`));
  } else {
    console.log(`✅ ${file}`);
  }
}

if (failed) {
  console.error(`\nفشل الفحص في ${failed} ملف — أُوقف النشر.`);
  process.exit(1);
}
console.log('\nكل الصفحات سليمة بنيوياً.');
