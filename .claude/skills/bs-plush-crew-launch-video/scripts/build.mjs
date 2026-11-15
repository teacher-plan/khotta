#!/usr/bin/env node
// Builds a previewable film folder from a storyboard (film.json).
//
//   node build.mjs --storyboard film.json --out film [--beats beats.json] [--offline]
//
// It validates the storyboard, fills the fixed workspace copy for the language, picks the five
// plush crew members from the brand colors, copies and downsizes the media, bundles fonts
// (a Google Fonts brand face is fetched and subset unless --offline) and the Lucide icons it
// needs, and writes index.html + storyboard.json + beats.json next to the engine.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';
import { highlighter, parse } from './lib/color.mjs';
import { STYLES, castDir as styleDir, loadCast, pickCrew } from './lib/crew.mjs';
import { fetchGoogleFont } from './lib/fonts.mjs';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const ENGINE = path.resolve(HERE, '..', 'references', 'engine');
const args = parseArgs(process.argv.slice(2));
if (!args.storyboard || !args.out) {
  console.error('Usage: node build.mjs --storyboard <film.json> --out <film-dir> [--beats beats.json] [--offline]');
  process.exit(2);
}
const sbPath = path.resolve(args.storyboard);
const sbDir = path.dirname(sbPath);
const OUT = path.resolve(args.out);
const sb = JSON.parse(fs.readFileSync(sbPath, 'utf8'));
const problems = [];
const warnings = [];
const need = (cond, msg) => { if (!cond) problems.push(msg); };

const lang = String(sb.lang || 'en').toLowerCase();
const english = /^en\b/.test(lang);
const L = 'en';
const cjk = /^(zh|ja|ko)/.test(lang);
const P = sb.product || {};
const S = sb.scenes || {};
const E = sb.end || {};
need(P.name, 'product.name is required');
need(P.mark, 'product.mark (a square logo mark image) is required');
need(sb.palette && sb.palette.brand, 'palette.brand is required');
for (const k of ['brand', 'what', 'fit', 'how', 'proof']) need(S[k], `scenes.${k} is required`);
need(E.headline && E.headline.length === 2, 'end.headline must be two lines');
need(E.url, 'end.url is required');
if (problems.length) fail();

// ---------- defaults for the language ----------
const DEF = {
  en: {
    ui: { share: 'Share', render: 'Render', play: 'Play', preview: 'Preview', timeline: 'Timeline', online: '5 online', composer: 'Write a reply…', dropZone: 'Drop a shot here',
      tracks: ['Shots', 'Titles', 'Motion', 'Music', 'SFX'], clips: { logo_rise: 'Logo rise', logo_strip: 'Logo strip', music: 'Score · {bpm} BPM', sfx: 'UI ticks' } },
    workspace: { projectTitle: '{name} in 40 seconds', channel: '#explain-{slug}', conceptLabel: 'Concept film', sticker: 'Literally magic!!!' },
    human: { name: 'Lin', role: '{name} team' },
    chat: { open: ['Who can explain {name} in 40 seconds?'], bite: ['Oops. I bit the beat.', 'audio-lines'], slot_q: ['Is there room for me in that slot?', 'bot'], sticker: ['Adding one tiny sticker.', 'sticker'],
      source: ['Source?', 'search'], fair: ['Fair.'], tagline: ["It's literally the tagline.", 'quote'], taste: ['Tasted the render. Delicious.', 'chef-hat'], close: ['Okay. Now I can explain it.'] },
  },
}[L];
const fillName = (s) => String(s).replace(/\{name\}/g, P.name).replace(/\{slug\}/g, slugify(P.name));

// ---------- beats ----------
let beats = { beat: 0.5, offset: 1.0, duration: 39.6 };
if (args.beats) beats = JSON.parse(fs.readFileSync(path.resolve(args.beats), 'utf8'));
else warnings.push('no --beats: using a 120 BPM grid for preview; run soundtrack.mjs on the music before the final build');
const bpm = Math.round(60 / beats.beat);

// ---------- palette ----------
const pal = sb.palette;
try { parse(pal.brand); } catch { problems.push(`palette.brand is not a color: ${pal.brand}`); fail(); }
const palette = {
  brand: pal.brand,
  accents: pal.accents || [],
  highlight: pal.highlight || highlighter(pal.brand),
  ink: pal.ink || '#121313',
  bg: pal.bg || '#F4F1E9',
};

// ---------- crew ----------
const style = sb.style || 'felt';
if (!STYLES[style]) { problems.push(`style must be one of: ${Object.keys(STYLES).join(', ')}`); fail(); }
const crewRoot = path.join(ENGINE, 'crew');
const cast = loadCast(styleDir(crewRoot, style));
const crew = pickCrew({ cast, brand: palette.brand, accents: palette.accents, overrides: sb.crew || [] });

// ---------- media ----------
fs.rmSync(path.join(OUT, 'assets'), { recursive: true, force: true });
fs.mkdirSync(path.join(OUT, 'assets'), { recursive: true });
fs.mkdirSync(path.join(OUT, 'fonts'), { recursive: true });
const copied = new Map();
const KEEP = new Set(['mark', 'wordmark', 'logo']);          // keep transparency and vectors as they are
function asset(ref, key) {
  if (!ref) return ref;
  if (/^(https?:|data:)/.test(ref)) { problems.push(`download remote media first (${key}): ${ref}`); return ref; }
  const abs = path.isAbsolute(ref) ? ref : path.resolve(sbDir, ref);
  if (!fs.existsSync(abs)) { problems.push(`missing file (${key}): ${ref}`); return ref; }
  const id = `${abs}|${KEEP.has(key)}`;
  if (copied.has(id)) return copied.get(id);
  const buf = fs.readFileSync(abs);
  const digest = crypto.createHash('sha1').update(buf).digest('hex').slice(0, 8);
  const base = path.basename(abs, path.extname(abs)).replace(/[^a-z0-9._-]+/gi, '-').slice(0, 40);
  const ext = path.extname(abs).toLowerCase();
  let rel;
  if (!KEEP.has(key) && /\.(png|jpe?g|webp|avif)$/.test(ext) && buf.length > 900 * 1024) {
    rel = `assets/${base}-${digest}.jpg`;
    const r = spawnSync('ffmpeg', ['-v', 'error', '-y', '-i', abs, '-vf', "scale='min(2560,iw)':-2", '-q:v', '2', path.join(OUT, rel)]);
    if (r.status !== 0) { rel = `assets/${base}-${digest}${ext}`; fs.writeFileSync(path.join(OUT, rel), buf); }
  } else {
    rel = `assets/${base}-${digest}${ext}`;
    fs.writeFileSync(path.join(OUT, rel), buf);
  }
  copied.set(id, rel);
  return rel;
}
const list = (v, n, label, min = 1) => { const a = Array.isArray(v) ? v.filter(Boolean) : []; if (a.length < min) problems.push(`${label} needs at least ${min} item(s)`); else if (n && a.length < n) warnings.push(`${label} has ${a.length} of ${n} recommended items; images will repeat`); return a; };

const product = { name: P.name, url: P.url || E.url, mark: asset(P.mark, 'mark'), markBg: P.markBg || '#FFFFFF', markPad: P.markPad ?? (P.markFill ? 0 : 0.18), wordmark: P.wordmark ? asset(P.wordmark, 'wordmark') : null };
const B = S.brand, W = S.what, F = S.fit, H = S.how, R = S.proof;

// ---------- non-English films: the agent supplies every workspace label in the film's language ----------
if (!english) {
  const miss = [];
  const u = sb.ui || {}, c = u.clips || {}, w = sb.workspace || {};
  for (const k of ['share', 'render', 'play', 'preview', 'timeline', 'online', 'composer', 'dropZone']) if (!u[k]) miss.push(`ui.${k}`);
  if (!Array.isArray(u.tracks) || u.tracks.length !== 5) miss.push('ui.tracks (5 lane names)');
  for (const k of ['logo_rise', 'logo_strip', 'music', 'sfx']) if (!c[k]) miss.push(`ui.clips.${k}`);
  for (const k of ['projectTitle', 'channel', 'sticker']) if (!w[k]) miss.push(`workspace.${k}`);
  if (w.conceptLabel === undefined) miss.push('workspace.conceptLabel');
  if (!sb.human || !sb.human.role) miss.push('human.role');
  for (const id of ['c1', 'c2', 'c3', 'c4', 'c5']) { const o = (sb.crew || []).find((x) => x.id === id); if (!o || !o.name || !o.role) miss.push(`crew ${id} name and role`); }
  for (const slot of ['open', 'bite', 'slot_q', 'sticker', 'source', 'fair', 'tagline', 'taste', 'close']) if (!sb.chat || !sb.chat[slot]) miss.push(`chat.${slot}`);
  if (!W.kind) miss.push('scenes.what.kind'); if (!F.chip) miss.push('scenes.fit.chip'); if (!H.buttonDone) miss.push('scenes.how.buttonDone');
  if (miss.length) problems.push(`a ${lang} film needs these labels in ${lang} (see "Other languages" in references/storyboard-schema.md): ${miss.join(', ')}`);
}
const scenes = {
  brand: { label: B.label, headline: two(B.headline, 'scenes.brand.headline'), highlight: B.highlight || '', sub: B.sub || '', peeks: list(B.peeks, 4, 'scenes.brand.peeks').map((x) => asset(x, 'peek')) },
  what: {
    label: W.label, kind: W.kind || 'PRODUCT', headline: two(W.headline, 'scenes.what.headline'), highlight: W.highlight || ['', ''], sub: W.sub || '',
    chips: list(W.chips, 3, 'scenes.what.chips', 3).slice(0, 3).map((c) => (typeof c === 'string' ? { text: c } : c)),
    categories: list(W.categories, 4, 'scenes.what.categories', 4).slice(0, 4),
    wall: list(W.wall, 8, 'scenes.what.wall', 4).map((x, i) => (typeof x === 'string' ? { src: asset(x, 'wall'), cat: i % 4 } : { ...x, src: asset(x.src, 'wall') })),
  },
  fit: {
    label: F.label, headline: two(F.headline, 'scenes.fit.headline'), chip: F.chip || 'Works', more: F.more || '', finePrint: F.finePrint || '',
    items: list(F.items, 3, 'scenes.fit.items', 3).slice(0, 3).map((it) => ({ ...it, logo: it.logo ? asset(it.logo, 'logo') : null })),
  },
  how: {
    label: H.label, steps: list(H.steps, 3, 'scenes.how.steps', 3).slice(0, 3), button: H.button, buttonDone: H.buttonDone || 'Done', buttonIcon: H.buttonIcon,
    cardTitle: H.cardTitle || P.name, input: H.input, inputHighlight: H.inputHighlight || '', dialog: H.dialog || {}, sub: H.sub || '',
    results: list(H.results, 3, 'scenes.how.results').map((x) => asset(x, 'result')), resultLine: H.resultLine || '{x}', resultPrefix: H.resultPrefix || '', resultValues: list(H.resultValues, 3, 'scenes.how.resultValues'),
  },
  proof: { label: R.label, headline: two(R.headline, 'scenes.proof.headline'), sub: R.sub || '', stamp: R.stamp, stampIcon: R.stampIcon, cards: list(R.cards, 6, 'scenes.proof.cards').map((x) => asset(x, 'card')) },
};
need(H.button, 'scenes.how.button is required');
need(H.input, 'scenes.how.input is required');
for (const k of ['title', 'label', 'value', 'approve', 'deny']) need(H.dialog && H.dialog[k], `scenes.how.dialog.${k} is required`);
need(R.stamp, 'scenes.proof.stamp is required');
for (const k of ['brand', 'what', 'fit', 'how', 'proof']) need(S[k].label, `scenes.${k}.label is required (the clip name in the timeline)`);
const media = {
  thumbs: (sb.media && sb.media.thumbs ? sb.media.thumbs.map((x) => asset(x, 'thumb')) : [scenes.brand.peeks[0], scenes.what.wall[0]?.src, scenes.fit.items[0]?.logo || scenes.brand.peeks[1 % scenes.brand.peeks.length], scenes.how.results[0], scenes.proof.cards[0]]).filter(Boolean),
  gutter: (sb.media && sb.media.gutter ? sb.media.gutter.map((x) => asset(x, 'gutter')) : [scenes.what.wall[1 % scenes.what.wall.length]?.src, scenes.proof.cards[1 % scenes.proof.cards.length]]).filter(Boolean),
};

// ---------- chat ----------
const REQUIRED = ['hero_joke', 'wall_q', 'wall_a', 'how_q', 'how_a', 'proof_joke'];
const chat = {};
for (const slot of ['open', 'hero_joke', 'bite', 'wall_q', 'wall_a', 'slot_q', 'how_q', 'how_a', 'sticker', 'source', 'fair', 'proof_joke', 'tagline', 'taste', 'close']) {
  const given = sb.chat && sb.chat[slot];
  const m = typeof given === 'string' ? { text: given } : given || null;
  if (m && m.text) chat[slot] = { text: fillName(m.text), icon: m.icon };
  else if (DEF.chat[slot]) chat[slot] = { text: fillName(DEF.chat[slot][0]), icon: DEF.chat[slot][1] };
  else problems.push(`chat.${slot} is required (see references/storyboard-schema.md)`);
  // CJK glyphs are about twice as wide as Latin ones: count Latin as half
  const t = chat[slot]?.text || '';
  const w = [...t].reduce((a, ch) => a + (/[\u3000-\u9fff\uff00-\uffef]/.test(ch) ? 1 : 0.5), 0);
  const max = 21;
  if (w > max) warnings.push(`chat.${slot} "${t}" is long; keep chat lines to about 42 Latin or 20 CJK characters so the bubble stays at two lines`);
}

// ---------- copy checks ----------
const lim = cjk ? { head: 12, chip: 10, cat: 8, step: 6 } : { head: 24, chip: 22, cat: 16, step: 12 };
const check = (s, max, label) => { if (s && s.length > max) warnings.push(`${label} "${s}" is ${s.length} chars (aim for ${max} or fewer)`); };
for (const [k, v] of Object.entries({ brand: scenes.brand.headline, what: scenes.what.headline, fit: scenes.fit.headline, proof: scenes.proof.headline, end: E.headline })) v.forEach((x, i) => check(x, lim.head, `${k} headline line ${i + 1}`));
scenes.what.chips.forEach((c) => check(c.text, lim.chip, 'what chip'));
scenes.what.categories.forEach((c) => check(c, lim.cat, 'what category'));
scenes.how.steps.forEach((c) => check(c, lim.step, 'how step'));
if (scenes.brand.highlight && !scenes.brand.headline.join(' ').includes(scenes.brand.highlight)) warnings.push(`brand.highlight "${scenes.brand.highlight}" is not in the brand headline`);
if (E.highlight && !E.headline.join(' ').includes(E.highlight)) warnings.push(`end.highlight "${E.highlight}" is not in the end headline`);
const thirdParty = scenes.fit.items.some((x) => x.logo);
if (thirdParty && !scenes.fit.finePrint) warnings.push('fit.items use logos: if any belongs to another company, add fit.finePrint with the trademark notice');

// ---------- labels derived from the beat grid ----------
const labels = ['brand', 'what', 'fit', 'how', 'proof'].map((k) => scenes[k].label);
const starts = [0, 8, 20, 28, 40].map((b) => b * beats.beat);
const mmss = (s) => `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(Math.round(s % 60)).padStart(2, '0')}`;
const sbUi = sb.ui || {};
const clips = { ...DEF.ui.clips, ...(sbUi.clips || {}) };
const ui = {
  ...DEF.ui,
  shotClips: labels.map((l, i) => `0${i + 1} ${l}`),
  sceneTags: labels.map((l, i) => `${mmss(starts[i])} · ${l}`),
  ...sbUi,
  clips: { ...clips, music: String(clips.music).replace('{bpm}', bpm), hero_line: clips.hero_line || `“${scenes.brand.headline.join(cjk ? '' : ' ')}”` },
};
const ws = sb.workspace || {};
const workspace = {
  projectTitle: fillName(ws.projectTitle || DEF.workspace.projectTitle),
  channel: fillName(ws.channel || DEF.workspace.channel),
  conceptLabel: ws.conceptLabel === null || ws.conceptLabel === false ? null : fillName(ws.conceptLabel || DEF.workspace.conceptLabel),
  sticker: ws.sticker || DEF.workspace.sticker,
};
const human = { name: (sb.human && sb.human.name) || DEF.human.name, role: fillName((sb.human && sb.human.role) || DEF.human.role) };
const end = { headline: E.headline, highlight: E.highlight || '', sub: E.sub || '', url: E.url };

// ---------- crew files ----------
fs.rmSync(path.join(OUT, 'crew'), { recursive: true, force: true });
fs.mkdirSync(path.join(OUT, 'crew'), { recursive: true });
for (const c of crew) { const name = path.basename(c.file); fs.copyFileSync(path.join(crewRoot, c.file), path.join(OUT, 'crew', name)); c.file = `crew/${name}`; }

// ---------- fonts ----------
const fontCss = [];
const face = (fam, file, weight, extra = '') => `@font-face { font-family: '${fam}'; src: url('fonts/${file}') format('woff2'); font-weight: ${weight}; font-display: block;${extra} }`;
for (const f of ['bricolage-400.woff2', 'bricolage-600.woff2', 'bricolage-700.woff2', 'geist.woff2', 'jbmono-500.woff2', 'jbmono-700.woff2']) fs.copyFileSync(path.join(ENGINE, 'fonts', f), path.join(OUT, 'fonts', f));
fontCss.push(face('Bricolage', 'bricolage-400.woff2', 400), face('Bricolage', 'bricolage-600.woff2', 600), face('Bricolage', 'bricolage-700.woff2', 700), face('Geist', 'geist.woff2', '100 900'), face('JetBrains Mono', 'jbmono-500.woff2', 500), face('JetBrains Mono', 'jbmono-700.woff2', 700));
let display = "'Bricolage'";
let uiFace = "'Geist'";
const allText = JSON.stringify({ product: P.name, scenes, end, chat, workspace, ui, crew: crew.map((c) => [c.name, c.role]), human }).replace(/[\\"{}[\]:,]/g, ' ');
const latinText = [...new Set(allText.replace(/[^\x20-\x7e\u00a0-\u024f\u2018-\u201f…]/g, ''))].join('') + ' 0123456789';
const fonts = sb.fonts || {};
async function brandFace(family, weights, alias) {
  if (!family || /^(bricolage|bricolage grotesque|geist)$/i.test(family)) return null;
  if (args.offline) { warnings.push(`--offline: "${family}" not fetched; using the bundled face`); return null; }
  try { return await fetchGoogleFont({ family, weights, text: latinText, outDir: path.join(OUT, 'fonts'), alias }); }
  catch (e) { warnings.push(`could not fetch "${family}" from Google Fonts (${e.message}); using the bundled face`); return null; }
}
const dcss = await brandFace(fonts.display, [700], 'Brand Display');
if (dcss) { fontCss.push(dcss); display = "'Brand Display'"; }
const ucss = await brandFace(fonts.ui, [500, 600, 700], 'Brand UI');
if (ucss) { fontCss.push(ucss); uiFace = "'Brand UI'"; }
let notoLink = '';
if (cjk) {
  fs.copyFileSync(path.join(ENGINE, 'fonts', 'smiley-sans-oblique.woff2'), path.join(OUT, 'fonts', 'smiley-sans-oblique.woff2'));
  fontCss.push(face('Smiley Sans', 'smiley-sans-oblique.woff2', 400));
  fs.cpSync(path.join(ENGINE, 'fonts', 'noto-sc'), path.join(OUT, 'fonts', 'noto-sc'), { recursive: true });
  notoLink = '<link rel="stylesheet" href="fonts/noto-sc/noto-sans-sc.css">';
}

// ---------- icons ----------
const lucide = JSON.parse(fs.readFileSync(path.join(ENGINE, 'lucide-nodes.json'), 'utf8'));
const icons = new Set(['film', 'share', 'arrow-up', 'folder', 'sparkles', 'type', 'music', 'check', 'globe', 'badge-check', 'mouse-pointer-click']);
(function walk(n, k) { if (Array.isArray(n)) n.forEach((v) => walk(v, k)); else if (n && typeof n === 'object') for (const [kk, v] of Object.entries(n)) walk(v, kk); else if (typeof n === 'string' && /icon$/i.test(k || '')) icons.add(n); })({ scenes, chat });
const subset = {};
for (const name of icons) { if (lucide[name]) subset[name] = lucide[name]; else warnings.push(`unknown Lucide icon "${name}"`); }

if (problems.length) fail();

// ---------- write ----------
const resolved = { lang, cjk, product, palette, crew, human, workspace, ui, chat, media, scenes, end, sources: sb.sources || [] };
fs.writeFileSync(path.join(OUT, 'storyboard.json'), JSON.stringify(resolved, null, 1));
fs.writeFileSync(path.join(OUT, 'beats.json'), JSON.stringify(beats, null, 1));
fs.writeFileSync(path.join(OUT, 'icons.js'), `window.FILM_ICONS=${JSON.stringify(subset)};\n`);
for (const f of ['film.js', 'scenes.js', 'film.css']) fs.copyFileSync(path.join(ENGINE, f), path.join(OUT, f));
const vars = `:root { --bg: ${palette.bg}; --ink: ${palette.ink}; --hl: ${palette.highlight}; --brand: ${palette.brand}; --mark-bg: ${product.markBg};
  --display: ${display}, 'Bricolage', 'Noto Sans SC', sans-serif; --ui: ${uiFace}, 'Geist', 'Noto Sans SC', system-ui, sans-serif; }`;
fs.writeFileSync(path.join(OUT, 'index.html'), `<!doctype html>
<html lang="${esc(lang)}">
<head>
<meta charset="utf-8">
<title>${esc(P.name)} · launch film</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="film.css">
${notoLink}
<style>
${fontCss.join('\n')}
${vars}
</style>
</head>
<body>
<div id="stage"></div>
<script src="icons.js"></script>
<script src="film.js"></script>
<script src="scenes.js"></script>
</body>
</html>
`);

console.log(`Built ${OUT}`);
console.log(`Language ${lang}  ·  ${bpm} BPM  ·  ${beats.duration.toFixed(2)} s  ·  media ${copied.size}  ·  icons ${Object.keys(subset).length}`);
console.log(`Palette brand ${palette.brand}  highlight ${palette.highlight}`);
console.log(`Style ${style}  ·  crew: ` + crew.map((c) => `${c.id} ${c.name}/${c.role} ${c.shape} ${c.swatch}`).join('  |  '));
for (const w of warnings) console.log(`WARN ${w}`);

function two(v, label) { if (!Array.isArray(v) || v.length !== 2 || !v[0] || !v[1]) { problems.push(`${label} must be two non-empty lines`); return ['', '']; } return v; }
function fail() { for (const p of problems) console.error(`ERROR ${p}`); for (const w of warnings) console.log(`WARN ${w}`); process.exit(1); }
function slugify(s) { return String(s).toLowerCase().replace(/[^a-z0-9\u3400-\u9fff]+/g, '-').replace(/^-|-$/g, ''); }
function esc(s) { return String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]); }
function parseArgs(list) {
  const o = {};
  for (let i = 0; i < list.length; i += 1) {
    if (!list[i].startsWith('--')) continue;
    const k = list[i].slice(2);
    const v = list[i + 1];
    if (v === undefined || v.startsWith('--')) o[k] = true;
    else { o[k] = v; i += 1; }
  }
  return o;
}
