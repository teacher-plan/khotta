/* ═══════════════════════════════════════════════════════════════════
   العُدّة المشتركة — الأنشطة والفعاليات التفاعلية
   ───────────────────────────────────────────────────────────────────
   كل ما يتكرّر في الأنشطة الواحد والعشرين مجموعٌ هنا: المؤقّت، النقاط،
   لوحة المعلّمة، وضع العرض، الأصوات، التغذية الراجعة، التأمّل الختامي.
   النشاط لا يكتب منها شيئاً — يستدعيها ويكتب محتواه هو فقط.

   الأصوات مُركّبة بـWebAudio لا ملفاتٍ مسجّلة: ملفُّ صوتٍ واحد يزن أضعاف
   النشاط كلّه، ويتطلّب تحميلاً قد لا يتمّ في مدرسةٍ بلا شبكة.
   ═══════════════════════════════════════════════════════════════════ */
(function (global) {
  'use strict';

  const AR = n => String(n).replace(/[0-9]/g, d => '٠١٢٣٤٥٦٧٨٩'[+d]);
  const $ = s => document.querySelector(s);
  const el = (t, c, h) => { const e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  /** خلطٌ عشوائيّ حقيقي (فيشر-ييتس). sort(()=>Math.random()-.5) منحازٌ فعلاً
      ويُعيد ترتيباتٍ متشابهة، فتشعر الطالبات بتكرار الأسئلة. */
  function shuffle(a) {
    const r = a.slice();
    for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; }
    return r;
  }

  /** موزّعٌ لا يُعيد عنصراً حتى تنتهي المجموعة — «عشوائيٌّ» ساذج يكرّر
      السؤال نفسه مرّتين متتاليتين فتفقد الطالبات الثقة بالنشاط. */
  function Bag(items) {
    let pool = [];
    return { next() { if (!pool.length) pool = shuffle(items); return pool.pop(); },
             reset() { pool = []; }, size: items.length };
  }

  /* ── الصوت ── */
  let ctx = null, soundOn = true;
  function ac() { if (!ctx) { const C = global.AudioContext || global.webkitAudioContext; if (C) ctx = new C(); } if (ctx && ctx.state === 'suspended') ctx.resume(); return ctx; }
  function tone(freq, dur, type, vol, delay) {
    if (!soundOn) return; const c = ac(); if (!c) return;
    const t0 = c.currentTime + (delay || 0);
    const o = c.createOscillator(), g = c.createGain();
    o.type = type || 'sine'; o.frequency.setValueAtTime(freq, t0);
    // منحنى الخفوت يمنع الطقطقة التي تُسمع كعطلٍ في مكبّر الصف
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(vol || 0.13, t0 + 0.015);
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    o.connect(g); g.connect(c.destination); o.start(t0); o.stop(t0 + dur + 0.03);
  }
  const SFX = {
    tap:  () => tone(520, 0.07, 'sine', 0.07),
    ok:   () => { tone(660, 0.13, 'sine', 0.12); tone(880, 0.2, 'sine', 0.11, 0.1); },
    win:  () => { [523, 659, 784, 1047].forEach((f, i) => tone(f, 0.28, 'triangle', 0.11, i * 0.11)); },
    soft: () => { tone(392, 0.18, 'sine', 0.09); tone(330, 0.22, 'sine', 0.08, 0.12); },
    tick: () => tone(1100, 0.04, 'square', 0.045),
    time: () => { [660, 560, 460].forEach((f, i) => tone(f, 0.3, 'triangle', 0.12, i * 0.16)); },
    star: () => { [784, 988, 1319].forEach((f, i) => tone(f, 0.22, 'sine', 0.1, i * 0.08)); },
  };

  /* ── ملء الشاشة وقفل الإيقاظ ──
     البروجكتر يريد الشاشة كلّها، والجهاز يجب ألّا ينام والمعلّمة تشرح
     ولا تلمسه. النظام يُسقط القفل عند تبديل النافذة فنستعيده. */
  let wake = null;
  async function wakeOn() { try { if (navigator.wakeLock && !wake) wake = await navigator.wakeLock.request('screen'); } catch (e) {} }
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'visible') wakeOn(); });
  function fullToggle() {
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    else if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen().catch(() => {});
  }

  /* ── التغذية الراجعة ──
     لا عبارة إحباطٍ واحدة في القسم كلّه: الخطأ يُقابَل بدعوةٍ للتفكير لا
     بحكمٍ على الطالبة. */
  let fbEl = null, fbT = null;
  function say(msg, kind) {
    if (!fbEl) { fbEl = el('div', 'fb'); document.body.appendChild(fbEl); }
    fbEl.className = 'fb on' + (kind ? ' ' + kind : '');
    fbEl.textContent = msg;
    clearTimeout(fbT); fbT = setTimeout(() => fbEl.classList.remove('on'), 2600);
  }
  const PRAISE = ['أحسنتم التفكير!', 'تفكيرٌ جميل!', 'عملٌ رائع من الفريق!', 'ممتاز، واصلوا!',
    'إجابةٌ موفّقة!', 'تعاونٌ مميّز!', 'أعجبني تركيزكم!'];
  const ENCOURAGE = ['فكرةٌ قريبة — لنُفكّر معاً مرّةً أخرى.', 'محاولةٌ جيّدة! من يُساعد؟',
    'لنقترب أكثر… ما رأيكم؟', 'شكراً لمحاولتك — من عنده فكرةٌ أخرى؟'];
  const praise = () => say(PRAISE[Math.floor(Math.random() * PRAISE.length)], '');
  const encourage = () => say(ENCOURAGE[Math.floor(Math.random() * ENCOURAGE.length)], 'warn');

  /* ── المؤقّت ── */
  function Timer(opts) {
    const o = Object.assign({ secs: 60, onTick: null, onEnd: null, ring: null, label: null }, opts);
    let left = o.secs, total = o.secs, id = null, running = false;
    function paint() {
      const m = Math.floor(left / 60), s = left % 60;
      const txt = m ? AR(m) + ':' + AR(String(s).padStart(2, '0')) : AR(s);
      if (o.ring) { o.ring.style.setProperty('--p', total ? left / total : 0); const i = o.ring.querySelector('i'); if (i) i.textContent = txt; }
      if (o.label) o.label.textContent = txt;
      const box = o.ring && o.ring.closest('.timer');
      if (box) box.classList.toggle('low', left <= 10 && left > 0);
      if (o.onTick) o.onTick(left);
    }
    function step() {
      left--;
      // النقرة في آخر خمسٍ فقط: نقرةٌ كل ثانيةٍ لدقيقةٍ كاملة تُوتّر الصف
      if (left <= 5 && left > 0) SFX.tick();
      paint();
      if (left <= 0) { stop(); SFX.time(); if (o.onEnd) o.onEnd(); }
    }
    function start(){ if(running) return; running = true; id = setInterval(step, 1000); paint(); }
    function pause(){ running = false; clearInterval(id); }
    function stop(){ pause(); }
    function reset(n){ pause(); total = left = (n == null ? o.secs : n); paint(); }
    function add(n){ left += n; total = Math.max(total, left); paint(); }
    return { start, pause, stop, reset, add, paint,
             get left(){ return left; }, get running(){ return running; } };
  }

  /* ── الفرق والنقاط ── */
  const TEAM_COLORS = ['#487848', '#D9A93C', '#2F7D74', '#D86048', '#6B4E9E', '#B0721A'];
  const TEAM_NAMES = ['الفريق الأول', 'الفريق الثاني', 'الفريق الثالث', 'الفريق الرابع', 'الفريق الخامس', 'الفريق السادس'];
  function Teams(host, n) {
    let list = [], pending = null;   // pending: القيمة المنتظرة إسنادها لفريق
    function build(count) {
      list = Array.from({ length: count }, (_, i) => ({ name: TEAM_NAMES[i] || 'فريق ' + AR(i + 1), score: 0, color: TEAM_COLORS[i % TEAM_COLORS.length] }));
      render();
    }
    /** إعادة الربط بحاويةٍ جديدة مع بقاء الأسماء والنقاط — الجولة الجديدة
        تُعيد بناء المسرح، والنقاط لا يجوز أن تضيع معه. */
    function mount(newHost) { host = newHost; render(); }
    function render() {
      const top = Math.max.apply(null, list.map(t => t.score));
      host.innerHTML = '';
      list.forEach((t, i) => {
        const c = el('div', 'team' + (t.score === top && top > 0 ? ' lead' : ''));
        c.innerHTML = `<div class="hd"><span class="dot" style="background:${t.color}"></span>
          <input class="nm2" value="${esc(t.name)}" aria-label="اسم الفريق"/></div>
          <div class="sc">${AR(t.score)}</div>
          <div class="ops"><button data-d="1" aria-label="إضافة نقطة">+</button>
          <button data-d="-1" aria-label="خصم نقطة">−</button></div>`;
        c.querySelector('.nm2').onchange = e => { t.name = e.target.value.trim() || t.name; };
        c.querySelectorAll('.ops button').forEach(b => b.onclick = ev => {
          ev.stopPropagation();
          const d = +b.dataset.d;
          t.score = Math.max(0, t.score + d);
          if (d > 0) SFX.star(); render();
        });
        // في وضع الإسناد: بطاقة الفريق كلّها زرّ. المعلّمة واقفةٌ أمام الصف
        // ولا تملك وقتاً لنافذةٍ تسألها رقم الفريق.
        if (pending) {
          c.style.cursor = 'pointer';
          c.style.boxShadow = '0 0 0 5px var(--gold),0 4px 0 rgba(42,21,3,.18)';
          c.onclick = () => { const p = pending; pending = null; award(i, p.pts, p.why); };
        }
        host.appendChild(c);
      });
    }
    function award(i, pts, why) {
      if (!list[i]) return;
      list[i].score += pts; SFX.star(); render();
      if (why) say(list[i].name + ' + ' + AR(pts) + ' — ' + why, 'info');
    }
    /** ضغطة قيمةٍ ثم ضغطة فريق: خطوتان بلا كتابةٍ ولا نافذة */
    function ask(pts, why) {
      pending = { pts, why };
      say('اضغطي على الفريق الذي يستحقّ: ' + why, 'info');
      render();
    }
    function reset() { list.forEach(t => t.score = 0); render(); }
    build(n || 2);
    return { build, mount, reset, award, ask, render, get list() { return list; } };
  }

  /* صفُّ نقاط القيم — مشتركٌ في كل نشاط.
     الفوز في هذا القسم ليس للأسرع: بلا هذه الأزرار يبقى «كافئ التعاون»
     جملةً في دليل المعلّمة لا فعلاً ممكناً في ثانيتين. */
  const DEFAULT_VALUES = [[1, 'التعاون'], [1, 'الإصغاء والاحترام'], [1, 'المشاركة والمحاولة'], [1, 'تفكيرٌ مبدع']];
  function valuesRow(teams, pairs) {
    const row = el('div', 'vals hide-present');
    (pairs || DEFAULT_VALUES).forEach(([pts, why]) => {
      const b = el('button', '', '★ ' + why);
      b.onclick = () => { SFX.tap(); teams.ask(pts, why); };
      row.appendChild(b);
    });
    return row;
  }

  /* ── لوحة المعلّمة ──
     تُبنى من كائنٍ يصفها لا من HTML مكتوبٍ في كل نشاط: بهذا تتطابق
     بنيتها في الأنشطة الواحد والعشرين، وتعرف المعلّمة أين تجد كل شيء
     في أيّ نشاطٍ تفتحه. */
  const TP_FIELDS = [
    ['goal', 'الهدف التربوي'], ['tools', 'الأدوات المطلوبة'], ['groups', 'تقسيم الطلاب'],
    ['steps', 'خطوات التنفيذ'], ['time', 'الوقت المقترح'], ['script', 'تُقرأ للطلاب'],
    ['tips', 'إدارة الصف'], ['points', 'احتساب النقاط'], ['levels', 'مستويات الصعوبة'],
    ['close', 'الأسئلة الختامية'],
  ];
  function teacherPanel(info) {
    const veil = el('div', 'veil'); const p = el('div', 'tp');
    let h = `<button class="btn sm ic x" aria-label="إغلاق">✕</button><h2>لوحة المعلّمة</h2>
      <div style="opacity:.75;font-size:16px">${esc(info.title || '')}</div>`;
    TP_FIELDS.forEach(([k, label]) => {
      const v = info[k]; if (!v) return;
      h += `<h3>${label}</h3>`;
      h += Array.isArray(v)
        ? `<${k === 'steps' ? 'ol' : 'ul'}>${v.map(x => `<li>${esc(x)}</li>`).join('')}</${k === 'steps' ? 'ol' : 'ul'}>`
        : `<p style="margin:0">${esc(v)}</p>`;
    });
    p.innerHTML = h;
    document.body.append(veil, p);
    const close = () => { p.classList.remove('on'); veil.classList.remove('on'); };
    p.querySelector('.x').onclick = close; veil.onclick = close;
    return { open() { p.classList.add('on'); veil.classList.add('on'); }, close };
  }

  /* ── التأمّل الختامي ──
     ينتهي كل نشاطٍ به بلا استثناء: النشاط بلا سؤالِ «ماذا تعلّمنا؟» يبقى
     تسليةً، والفرق بين الاثنين هو هذه الشاشة. */
  function reflect(stage, data, onAgain) {
    stage.innerHTML = '';
    const box = el('div', 'reflect');
    box.innerHTML = `<h2>ماذا تعلّمنا اليوم؟</h2>
      <div class="chip" style="margin-bottom:6px">القيمة: <b>${esc(data.value || '')}</b></div>
      <div class="qs">${(data.questions || []).map((q, i) => `<div><b>${AR(i + 1)}.</b><span>${esc(q)}</span></div>`).join('')}</div>`;
    const go = el('div', '', '');
    go.style.cssText = 'display:flex;gap:12px;justify-content:center;flex-wrap:wrap';
    const a = el('button', 'btn p big', 'نشاطٌ جديد');
    a.onclick = () => { SFX.tap(); onAgain(); };
    const b = el('button', 'btn', 'الفهرس');
    b.onclick = () => location.href = 'index.html';
    go.append(a, b); box.appendChild(go); stage.appendChild(box);
    SFX.win();
  }

  /* ── التركيب ──
     يبني القشرة كاملة (الشريط العلوي، المسرح، شريط الأدوات) ويُسلّم النشاط
     مسرحه وأدواته. النشاط يكتب محتواه فقط. */
  function build(cfg) {
    document.title = cfg.title;
    if (cfg.accent) { document.documentElement.style.setProperty('--a', cfg.accent); }
    if (cfg.accent2) { document.documentElement.style.setProperty('--a2', cfg.accent2); }

    const scene = el('div', 'scene'); scene.innerHTML = cfg.scene || '';
    const top = el('div', 'top');
    const stage = el('div', 'stage');
    const bottom = el('div', 'bottom');
    document.body.append(scene, top, stage, bottom);

    const tp = teacherPanel(Object.assign({ title: cfg.title }, cfg.teacher || {}));

    top.innerHTML = `<a class="btn sm ic" href="index.html" title="الفهرس" aria-label="الفهرس">☰</a>
      <span class="nm">${esc(cfg.title)}</span>`;
    const tBtn = el('button', 'btn sm', 'لوحة المعلّمة');
    tBtn.onclick = () => { SFX.tap(); tp.open(); };
    const pBtn = el('button', 'btn sm', 'وضع العرض');
    pBtn.onclick = () => {
      const on = document.body.classList.toggle('present');
      pBtn.textContent = on ? 'إنهاء وضع العرض' : 'وضع العرض';
      if (on) { fullToggle(); wakeOn(); }
      SFX.tap();
    };
    top.append(tBtn, pBtn);

    // شريط الأدوات: الأزرار الثابتة في كل نشاط. النشاط يُضيف ما يخصّه.
    const mk = (label, title, fn, cls) => { const b = el('button', 'btn sm ' + (cls || ''), label); b.title = title; b.setAttribute('aria-label', title); b.onclick = () => { SFX.tap(); fn(b); }; return b; };
    const sBtn = mk('🔊', 'الصوت', b => { soundOn = !soundOn; b.textContent = soundOn ? '🔊' : '🔇'; });
    const api = {
      stage, top, bottom, teacher: tp, AR, esc, el, shuffle, Bag, SFX, say, praise, encourage,
      Timer, Teams, valuesRow, reflect: (d, again) => reflect(stage, d, again),
      present: () => pBtn.click(),
      addTool: (b) => { bottom.insertBefore(b, sBtn); return b; },
      tool: mk,
    };
    bottom.append(
      mk('⤾ إعادة', 'إعادة النشاط من البداية', () => cfg.onRestart && cfg.onRestart()),
      sBtn,
      mk('⛶', 'ملء الشاشة', fullToggle),
      mk('؟', 'التعليمات', () => tp.open())
    );
    // مسافةٌ مرنة تدفع أدوات النشاط يميناً وأدوات النظام يساراً
    bottom.insertBefore(el('span', '', ''), bottom.firstChild).style.cssText = 'flex:1;order:5';

    document.addEventListener('keydown', e => {
      if (e.key === 'F' || e.key === 'f') fullToggle();
      else if (e.key === 'Escape' && document.body.classList.contains('present')) pBtn.click();
    });
    wakeOn();
    return api;
  }

  global.Kit = { build, AR, esc, el, $, shuffle, Bag, SFX, say, Timer, Teams, valuesRow, TEAM_COLORS };
})(window);
