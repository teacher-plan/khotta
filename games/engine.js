/* ═══════════════════════════════════════════════════════════════════
   محرّك الألعاب — نموذج أولي
   ───────────────────────────────────────────────────────────────────
   الفكرة: المحتوى منفصل عن القالب. المعلّم يكتب المحتوى مرة واحدة
   (سؤال، إجابة صحيحة، إجابات خاطئة)، وكل قالب يقرأ الصيغة نفسها
   ويعرضها بطريقته. فيتحوّل الاختبار إلى مطابقة بزرّ واحد.

   صيغة المحتوى (انظر README.md):
     { version: 1, title, settings: {shuffle, perRound},
       items: [ { q: "نص السؤال", a: "الإجابة الصحيحة", wrong: ["خطأ ١", "خطأ ٢"] } ] }

   لإضافة قالب جديد: Games.register('name', {label, needs, build(api)}).
   ═══════════════════════════════════════════════════════════════════ */
(function (global) {
  'use strict';

  const $ = s => document.querySelector(s);
  const el = (t, c, h) => { const e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; };
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const AR = n => String(n).replace(/[0-9]/g, d => '٠١٢٣٤٥٦٧٨٩'[+d]);
  const LETTERS = ['أ', 'ب', 'ج', 'د', 'هـ', 'و'];

  /** خلط فيشر-ييتس: sort(()=>Math.random()-.5) منحاز ويكرّر الترتيبات. */
  function shuffle(a) {
    const r = a.slice();
    for (let i = r.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [r[i], r[j]] = [r[j], r[i]]; }
    return r;
  }

  /* ── التحقّق من المحتوى ──
     أخطاء المحتوى تظهر للمعلّم برسالة واضحة، لا لعبةً معطوبة أمام الصف. */
  function validate(c) {
    const errs = [];
    if (!c || !Array.isArray(c.items) || !c.items.length) errs.push('لا توجد أسئلة في المحتوى.');
    else c.items.forEach((it, i) => {
      const n = AR(i + 1);
      if (!it.q || !String(it.q).trim()) errs.push(`السؤال ${n}: النص فارغ.`);
      if (!it.a || !String(it.a).trim()) errs.push(`السؤال ${n}: لا توجد إجابة صحيحة.`);
      if ((it.wrong || []).some(w => w === it.a)) errs.push(`السؤال ${n}: إجابة خاطئة تطابق الصحيحة.`);
    });
    return errs;
  }

  /* ── الصوت: نغمات WebAudio بلا ملفات، فتعمل بلا إنترنت ── */
  let ctx = null;
  function tone(freq, dur, type, vol, delay) {
    try {
      if (!ctx) { const C = global.AudioContext || global.webkitAudioContext; if (!C) return; ctx = new C(); }
      if (ctx.state === 'suspended') ctx.resume();
      const t0 = ctx.currentTime + (delay || 0), o = ctx.createOscillator(), g = ctx.createGain();
      o.type = type || 'sine'; o.frequency.value = freq;
      g.gain.setValueAtTime(0.0001, t0); g.gain.exponentialRampToValueAtTime(vol || .18, t0 + .02);
      g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
      o.connect(g).connect(ctx.destination); o.start(t0); o.stop(t0 + dur + .05);
    } catch (e) { /* الصوت تحسين لا شرط */ }
  }
  const sfx = {
    ok() { tone(660, .14, 'triangle'); tone(880, .22, 'triangle', .18, .1); },
    bad() { tone(200, .28, 'sawtooth', .08); },
    pick() { tone(520, .08, 'sine', .12); },
    win() { [523, 659, 784, 1047].forEach((f, i) => tone(f, .3, 'triangle', .16, i * .12)); }
  };

  /** يعيد تشغيل حركة CSS حتى لو كانت على العنصر نفسه. */
  function anim(node, cls) { node.classList.remove(cls); void node.offsetWidth; node.classList.add(cls); }

  /* ── سجلّ القوالب ── */
  const templates = {};
  let content = null, current = null;

  function register(name, def) { templates[name] = def; }

  function setProgress(done, total) {
    $('#bar').style.width = (total ? (done / total) * 100 : 0) + '%';
  }
  function setScore(text) { $('#score').textContent = text; }

  /** شاشة النهاية مشتركة: النجوم من النسبة، وزرّا الإعادة وتبديل القالب. */
  function finish(right, total, note) {
    sfx.win();
    const pct = total ? right / total : 0;
    const stars = pct >= .9 ? 3 : pct >= .6 ? 2 : pct > 0 ? 1 : 0;
    const other = Object.keys(templates).find(k => k !== current);
    const st = $('#stage'); st.innerHTML = '';
    const box = el('div', 'end rise', `
      <div class="stars" aria-label="${AR(stars)} من ٣ نجوم">${'★'.repeat(stars)}${'☆'.repeat(3 - stars)}</div>
      <div class="big">${AR(right)} من ${AR(total)}</div>
      <p>${esc(note || (stars === 3 ? 'ممتاز! أتقنتَ الدرس.' : stars === 2 ? 'أحسنت! راجع ما أخطأتَ فيه.' : 'لا بأس، جرّب مرة أخرى.'))}</p>
      <div class="row">
        <button class="btn" id="again">العب مرة أخرى</button>
        ${other ? `<button class="btn alt" id="swap">جرّب ${esc(templates[other].label)}</button>` : ''}
      </div>`);
    st.appendChild(box);
    setProgress(1, 1);
    $('#again').onclick = () => start(current);
    if (other) $('#swap').onclick = () => start(other);
  }

  function start(name) {
    if (!templates[name]) name = Object.keys(templates)[0];
    current = name;
    document.querySelectorAll('.switch button').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.t === name)));
    try { history.replaceState(null, '', '#' + name); } catch (e) {}
    const st = $('#stage'); st.innerHTML = '';
    setProgress(0, 1); setScore('');
    templates[name].build({ content, stage: st, el, esc, AR, LETTERS, shuffle, sfx, anim, setProgress, setScore, finish });
  }

  function mount(c, opts) {
    const errs = validate(c);
    $('#title').textContent = (c && c.title) || 'لعبة';
    document.title = ((c && c.title) || 'لعبة') + ' | خُطّتي';
    if (errs.length) {
      $('#stage').innerHTML = `<div class="end"><div class="big" style="font-size:32px">المحتوى يحتاج تصحيحاً</div>
        <p>${errs.map(esc).join('<br>')}</p></div>`;
      return;
    }
    content = c;
    const sw = $('#switch'); sw.innerHTML = '';
    Object.entries(templates).forEach(([k, t]) => {
      const b = el('button', '', esc(t.label)); b.dataset.t = k; b.type = 'button';
      b.onclick = () => start(k); sw.appendChild(b);
    });
    start((opts && opts.template) || location.hash.slice(1));
  }

  global.Games = { register, mount, start, validate, shuffle };
})(window);


/* ═══════════════════════════════════════════════════════════════════
   القالب ١: الاختبار — سؤال وخيارات، تغذية راجعة فورية
   ═══════════════════════════════════════════════════════════════════ */
Games.register('quiz', {
  label: 'اختبار',
  build(api) {
    const { content, stage, el, esc, AR, LETTERS, shuffle, sfx, anim, setProgress, setScore, finish } = api;
    const s = content.settings || {};
    const items = s.shuffle === false ? content.items.slice() : shuffle(content.items);
    let i = 0, right = 0;

    function show() {
      if (i >= items.length) return finish(right, items.length);
      const it = items[i];
      setProgress(i, items.length);
      setScore(`${AR(right)} ✓`);
      stage.innerHTML = '';
      stage.appendChild(el('div', 'q rise', `<small>السؤال ${AR(i + 1)} من ${AR(items.length)}</small>${esc(it.q)}`));
      const opts = el('div', 'opts');
      shuffle([it.a, ...(it.wrong || [])]).forEach((txt, k) => {
        const b = el('button', 'opt rise', `<span class="k">${LETTERS[k]}</span><span>${esc(txt)}</span>`);
        b.type = 'button'; b.style.animationDelay = (k * 60) + 'ms';
        b.onclick = () => choose(b, txt === it.a, opts);
        opts.appendChild(b);
      });
      stage.appendChild(opts);
    }

    function choose(btn, ok, opts) {
      opts.querySelectorAll('.opt').forEach(b => { b.disabled = true; });
      if (ok) { right++; btn.classList.add('right'); anim(btn, 'pop'); sfx.ok(); }
      else {
        btn.classList.add('wrong'); anim(btn, 'buzz'); sfx.bad();
        // نُظهر الإجابة الصحيحة: الخطأ بلا تصحيح لا يعلّم شيئاً.
        const correct = items[i].a;
        opts.querySelectorAll('.opt').forEach(b => {
          if (b.lastChild.textContent === correct) b.classList.add('right'); else if (b !== btn) b.classList.add('dim');
        });
      }
      setScore(`${AR(right)} ✓`);
      setTimeout(() => { i++; show(); }, ok ? 900 : 1700);
    }

    show();
  }
});


/* ═══════════════════════════════════════════════════════════════════
   القالب ٢: المطابقة — يقرأ المحتوى نفسه: كل سؤال يُطابَق بإجابته الصحيحة
   ───────────────────────────────────────────────────────────────────
   نقرة على سؤال ثم نقرة على إجابة، بدل السحب والإفلات: السحب صعب على
   الهاتف وعلى السبّورة التفاعلية، والنقر يعمل في الحالتين.
   ═══════════════════════════════════════════════════════════════════ */
Games.register('match', {
  label: 'مطابقة',
  build(api) {
    const { content, stage, el, esc, AR, shuffle, sfx, anim, setProgress, setScore, finish } = api;
    const s = content.settings || {};
    const per = Math.max(3, Math.min(6, s.perRound || 5));
    const all = s.shuffle === false ? content.items.slice() : shuffle(content.items);
    const rounds = [];
    for (let k = 0; k < all.length; k += per) rounds.push(all.slice(k, k + per));
    // جولة أخيرة من عنصر أو عنصرين لا تصلح للمطابقة: نضمّها إلى ما قبلها.
    if (rounds.length > 1 && rounds[rounds.length - 1].length < 3) rounds[rounds.length - 2].push(...rounds.pop());

    let r = 0, matched = 0, mistakes = 0, firstTry = 0;
    const total = all.length;

    function round() {
      if (r >= rounds.length) return finish(firstTry, total, mistakes ? `طابقتَ ${AR(firstTry)} من المحاولة الأولى.` : 'كل المطابقات صحيحة من المحاولة الأولى!');
      const set = rounds[r];
      const missed = new Set();
      let sel = null, left = set.length;
      stage.innerHTML = '';
      stage.appendChild(el('p', 'hint', rounds.length > 1 ? `الجولة ${AR(r + 1)} من ${AR(rounds.length)}: اختر سؤالاً ثم إجابته` : 'اختر سؤالاً ثم إجابته'));
      const board = el('div', 'board');
      const qs = el('div', 'col', '<h2>السؤال</h2>'), as = el('div', 'col', '<h2>الإجابة</h2>');

      set.forEach((it, k) => {
        const c = el('button', 'card rise', `${esc(it.q)}<span class="tag">✓</span>`);
        c.type = 'button'; c.dataset.id = k; c.style.animationDelay = (k * 50) + 'ms';
        c.onclick = () => { if (c.classList.contains('done')) return; if (sel) sel.classList.remove('sel'); sel = c; c.classList.add('sel'); sfx.pick(); };
        qs.appendChild(c);
      });
      shuffle(set.map((it, k) => ({ it, k }))).forEach(({ it, k }, n) => {
        const c = el('button', 'card ans rise', `${esc(it.a)}<span class="tag">✓</span>`);
        c.type = 'button'; c.dataset.id = k; c.style.animationDelay = (n * 50 + 120) + 'ms';
        c.onclick = () => {
          if (c.classList.contains('done')) return;
          if (!sel) { anim(qs, 'buzz'); return; }
          if (sel.dataset.id === c.dataset.id) {
            [sel, c].forEach(x => { x.classList.remove('sel'); x.classList.add('done'); x.disabled = true; anim(x, 'pop'); });
            sfx.ok(); matched++; left--;
            if (!missed.has(c.dataset.id)) firstTry++;
            sel = null;
            setProgress(matched, total); setScore(`${AR(matched)} / ${AR(total)}`);
            if (!left) setTimeout(() => { r++; round(); }, 800);
          } else {
            mistakes++; missed.add(sel.dataset.id); sfx.bad();
            c.classList.add('wrong'); anim(c, 'buzz');
            setTimeout(() => c.classList.remove('wrong'), 600);
          }
        };
        as.appendChild(c);
      });
      board.append(qs, as);
      stage.appendChild(board);
      setProgress(matched, total); setScore(`${AR(matched)} / ${AR(total)}`);
    }

    round();
  }
});
