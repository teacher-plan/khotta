#!/usr/bin/env node
// Fits one continuous stretch of a music track to the film's 76-beat choreography and mixes the
// interface foley on the same beats.
//
//   node soundtrack.mjs --music assets/music.mp3 --out-dir . [--start 12.4] [--bpm 120]
//        [--music-gain -2] [--foley-gain 0] [--sfx-dir sfx] [--bite-drop] [--lufs -16]
//
// Writes <out-dir>/beats.json (beat, offset, duration: what build.mjs --beats reads) and
// <out-dir>/soundtrack.wav (what render.mjs --audio reads). The track is never cut and spliced:
// one stretch plays from the pickup to the end card and fades out. --start picks the stretch by
// hand (seconds into the track, at the pickup two beats before a downbeat); without it the script
// scores every downbeat and keeps the stretch whose accents land hardest on the film's hits.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const HERE = path.dirname(new URL(import.meta.url).pathname);
const args = parseArgs(process.argv.slice(2));
if (!args.music || !args['out-dir']) {
  console.error('Usage: node soundtrack.mjs --music <track> --out-dir <dir> [--start s] [--bpm 120] [--music-gain dB] [--foley-gain dB] [--bite-drop] [--lufs -16]');
  process.exit(2);
}
const OUT = path.resolve(args['out-dir']);
fs.mkdirSync(OUT, { recursive: true });
const SR = 44100;
const END_BEAT = Number(args['tail-beats'] ? 74 + Number(args['tail-beats']) : 80);   // the crew jump on b74; the end card holds while the music fades
const HITS = [8, 16, 20, 28, 36, 45, 48, 56.5, 68, 74];

// ---------- beat analysis ----------
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'plush-score-'));
const an = spawnSync(process.execPath, [path.join(HERE, 'beats.mjs'), args.music, '--out', path.join(tmp, 'b.json'), '--bpm', String(args.bpm || 120), '--min', '90', '--max', '150'], { encoding: 'utf8' });
if (an.status !== 0) { console.error(an.stderr || an.stdout); process.exit(1); }
const A = JSON.parse(fs.readFileSync(path.join(tmp, 'b.json'), 'utf8'));
const P0 = A.beatPeriod;
if (A.bpm < 95 || A.bpm > 145) console.log(`WARN the track is ${A.bpm} BPM; the choreography is designed for 100-140 BPM (motion will feel ${A.bpm < 95 ? 'slow' : 'rushed'})`);

// ---------- decode ----------
const dec = spawnSync('ffmpeg', ['-v', 'error', '-i', args.music, '-ac', '2', '-ar', String(SR), '-f', 'f32le', '-'], { maxBuffer: 1 << 30 });
if (dec.status !== 0) { console.error(dec.stderr.toString()); process.exit(1); }
const pcm = new Float32Array(dec.stdout.buffer, dec.stdout.byteOffset, Math.floor(dec.stdout.byteLength / 4));
const frames = pcm.length / 2;
const trackDur = frames / SR;
// short-window energy (10 ms) for scoring accents
const HOP = 441;
const env = new Float32Array(Math.floor(frames / HOP));
for (let i = 0; i < env.length; i += 1) { let s = 0; for (let j = i * HOP; j < (i + 1) * HOP; j += 1) s += pcm[2 * j] ** 2 + pcm[2 * j + 1] ** 2; env[i] = Math.sqrt(s / HOP); }
const at = (t) => env[Math.max(0, Math.min(env.length - 1, Math.round(t * 100)))] || 0;
const accent = (t) => { let pk = 0; for (let d = -0.04; d <= 0.05; d += 0.01) pk = Math.max(pk, at(t + d)); let base = 0; for (let d = -0.35; d <= -0.15; d += 0.01) base += at(t + d); return pk / (base / 21 + 1e-4); };
const sorted = [...env].sort((a, b) => a - b), median = sorted[Math.floor(sorted.length / 2)];

// a break: about half a second far below the track's typical level (a short stop-hit is musical, a longer hole is not)
function hasGap(t0, t1) {
  for (let t = Math.max(0, t0); t < t1; t += 0.05) {
    let acc = 0; for (let d = 0; d < 0.45; d += 0.01) acc += at(t + d);
    if (acc / 45 < median * 0.12) return true;
  }
  return false;
}

function shortStops(t0, t1) {
  let n = 0;
  for (let t = Math.max(0, t0); t < t1; t += 0.05) {
    let acc = 0; for (let d = 0; d < 0.2; d += 0.01) acc += at(t + d);
    if (acc / 20 < median * 0.12) { n += 1; t += 0.5; }
  }
  return n;
}

// ---------- pick the stretch ----------
function fit(t0) {
  // regress the detected beats inside the window to one straight grid
  const win = A.beats.filter((b) => b >= t0 - 0.05 && b <= t0 + (END_BEAT + 2) * P0);
  if (win.length < 40) return null;
  const idx = win.map((b) => Math.round((b - win[0]) / P0));
  const n = win.length, mx = idx.reduce((a, b) => a + b) / n, my = win.reduce((a, b) => a + b) / n;
  let sxy = 0, sxx = 0; for (let i = 0; i < n; i += 1) { sxy += (idx[i] - mx) * (win[i] - my); sxx += (idx[i] - mx) ** 2; }
  const P = sxy / sxx, a = my - P * mx;
  const k0 = Math.round((t0 + 2 * P - a) / P);           // grid index of film beat 0
  const zero = a + k0 * P;                                // track time of film beat 0
  return { P, zero, start: zero - 2 * P };
}
// the track's own ending: its last strong beat before the music dies away
function trackEnding() {
  let tEnd = trackDur;
  while (tEnd > 5 && at(tEnd - 0.1) < median * 0.12) tEnd -= 0.05;   // trailing silence
  const last = A.beats.filter((b) => b < tEnd - 0.2 && b > tEnd - 6);
  if (!last.length) return null;
  const hit = last.reduce((best, b) => (accent(b) > accent(best) ? b : best), last[last.length - 1]);
  return { hit, tEnd };
}
let choice, ending = null;
if (args.start === undefined && !args['no-track-ending']) {
  const e = trackEnding();
  if (e) {
    const g = fit(e.hit - 76 * P0);
    if (g && g.start >= 0 && Math.abs(g.zero + 74 * g.P - e.hit) < 0.08 && !hasGap(g.start, g.zero + 74 * g.P) && shortStops(g.start, g.zero + 74 * g.P) === 0) {
      choice = g; ending = e;
      console.log(`Ending on the track's own final hit (${e.hit.toFixed(2)} s)`);
    }
  }
}
if (choice) {
  // chosen above: the track's ending lands on the crew's final jump
} else if (args.start !== undefined) {
  choice = fit(Number(args.start));
  if (!choice) { console.error('not enough beats after --start; pick an earlier point'); process.exit(1); }
  if (hasGap(choice.start, choice.zero + 75 * choice.P)) console.log('WARN the chosen stretch contains a stop or silent break; it will sound like a bad edit');
} else {
  let best = null;
  for (const d of A.downbeats) {
    const g = fit(d - 2 * P0);
    if (!g || g.start < 0 || g.start + (2 + END_BEAT) * g.P > trackDur - 0.2) continue;
    const score = HITS.reduce((s, h) => s + Math.log(1 + accent(g.zero + h * g.P)), 0);
    // stay out of quiet breaks: the energy across the film must hold up
    let quiet = 0; for (let b = 0; b < 76; b += 1) if (at(g.zero + b * g.P) < median * 0.25) quiet += 1;
    if (hasGap(g.start, g.zero + 75 * g.P)) continue;      // generated tracks sometimes stop dead for a moment
    const total = score - quiet * 0.4 - shortStops(g.start, g.zero + 75 * g.P) * 3;   // even a short stop-hit reads as a glitch here
    if (!best || total > best.total) best = { ...g, total };
  }
  if (!best) { console.error(`the track is too short: it needs about ${((END_BEAT + 3) * P0).toFixed(1)} s after the first downbeat`); process.exit(1); }
  choice = best;
}
const { P, start } = choice;
const offset = 2 * P;                                       // film b0 sits two beats after the pickup
const duration = +(ending ? Math.min(ending.tEnd - start + 0.05, offset + (74 + 8) * P) : offset + END_BEAT * P).toFixed(3);
const T = (b) => offset + b * P;
console.log(`Track ${A.bpm} BPM, stretch ${start.toFixed(2)}–${(start + duration).toFixed(2)} s of ${trackDur.toFixed(1)} s, film ${duration.toFixed(2)} s`);

// ---------- music stretch with the bite and the fades ----------
const N = Math.round(duration * SR);
const L = new Float32Array(N), R = new Float32Array(N);
const s0 = Math.round(start * SR);
const mg = 10 ** (Number(args['music-gain'] ?? -2) / 20);
for (let i = 0; i < N; i += 1) { const j = s0 + i; if (j >= 0 && j < frames) { L[i] = pcm[2 * j] * mg; R[i] = pcm[2 * j + 1] * mg; } }
const ramp = (t0, t1, g0, g1) => { const a = Math.round(t0 * SR), z = Math.round(t1 * SR); for (let i = Math.max(0, a); i < Math.min(N, z); i += 1) { const g = g0 + (g1 - g0) * (i - a) / Math.max(1, z - a); L[i] *= g; R[i] *= g; } };
ramp(0, 0.03, 0, 1);
// The audio crew bites the music clip on screen. The music keeps playing by default: a hole in the
// track sounds like a broken edit. --bite-drop restores the old short drop-out.
if (args['bite-drop']) {
  const a = T(12.75), z = T(14.5), floor = 0.03;
  const g = (t) => (t < a || t > z + 0.06 ? 1 : t < a + 0.02 ? 1 - (1 - floor) * (t - a) / 0.02 : t < z ? floor : floor + (1 - floor) * (t - z) / 0.06);
  for (let i = Math.round(a * SR); i < Math.min(N, Math.round((z + 0.06) * SR)); i += 1) { const k = g(i / SR); L[i] *= k; R[i] *= k; }
}
// ending: the track's own ring-out, or a fade that starts after the final hit and falls evenly in dB
{
  // let the final hit ring for a beat, then ease out: slow at first, falling evenly in dB to silence
  const a = Math.round((ending ? duration - 0.08 : T(75)) * SR);
  for (let i = Math.max(0, a); i < N; i += 1) {
    const k = (i - a) / Math.max(1, N - a);
    const db = -48 * k ** 1.6;
    const g = ending ? 1 - k : 10 ** (db / 20) * (k > 0.96 ? (1 - k) / 0.04 : 1);
    L[i] *= g; R[i] *= g;
  }
}

// ---------- foley ----------
const fx = new Float32Array(N);
let seed = 1;
const rnd = () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647 * 2 - 1; };
const len = (n) => Math.round(SR * n);
const sweep = (f0, f1, n) => { const out = new Float32Array(len(n)); let ph = 0; for (let i = 0; i < out.length; i += 1) { const f = f0 * (f1 / f0) ** (i / out.length); ph += 2 * Math.PI * f / SR; out[i] = Math.sin(ph); } return out; };
const noise = (n) => Float32Array.from({ length: len(n) }, rnd);
const smooth = (x, w) => { const o = new Float32Array(x.length); let acc = 0; for (let i = 0; i < x.length; i += 1) { acc += x[i]; if (i >= w) acc -= x[i - w]; o[i] = acc / Math.min(i + 1, w); } return o; };
const shape = (x, fn) => x.map((v, i) => v * fn(i / SR));
const add = (a, b, g = 1) => { const o = Float32Array.from(a); for (let i = 0; i < Math.min(a.length, b.length); i += 1) o[i] += b[i] * g; return o; };
const pop = (f0, f1, n = 0.07, amp = 0.2) => shape(sweep(f0, f1, n), (t) => (1 - Math.exp(-t / 0.002)) * Math.exp(-t / 0.02) * amp);
const click = (amp = 0.5) => { const n = noise(0.03); const d = n.map((v, i) => (i ? v - n[i - 1] : 0)); return shape(d, (t) => Math.exp(-t / 0.002) * 0.15 * amp).map((v, i) => v + Math.sin(2 * Math.PI * 3000 * i / SR) * Math.exp(-(i / SR) / 0.005) * 0.2 * amp); };
const thock = (amp = 0.8) => add(shape(sweep(420, 180, 0.09), (t) => Math.exp(-t / 0.025) * 0.28 * amp), click(0.4 * amp));
const tick = () => Float32Array.from({ length: len(0.05) }, (_, i) => Math.sin(2 * Math.PI * 2400 * i / SR) * Math.exp(-(i / SR) / 0.012) * 0.16);
const chomp = () => { const n = smooth(noise(0.16), 6); return add(shape(n, (t) => (Math.exp(-t / 0.03) + (t > 0.07 ? 0.6 * Math.exp(-(t - 0.07) / 0.02) : 0)) * 0.5), shape(sweep(260, 90, 0.16), (t) => Math.exp(-t / 0.05) * 0.35)); };
const boing = (f0 = 300, f1 = 700, n = 0.28) => { const o = new Float32Array(len(n)); let ph = 0; for (let i = 0; i < o.length; i += 1) { const t = i / SR; const f = f0 + (f1 - f0) * (1 - Math.exp(-t * 18)) + 40 * Math.sin(2 * Math.PI * 14 * t); ph += 2 * Math.PI * f / SR; o[i] = Math.sin(ph) * Math.exp(-t / 0.09) * 0.22; } return o; };
const whoosh = (n = 0.5, amp = 0.3) => { const z = noise(n), a = smooth(z, 24), b = smooth(z, 160); return a.map((v, i) => (v - b[i]) * Math.sin(Math.PI * i / a.length) ** 2 * amp * 3); };
const slap = () => add(shape(smooth(noise(0.08), 3), (t) => Math.exp(-t / 0.012) * 0.4), shape(sweep(180, 120, 0.08), (t) => Math.exp(-t / 0.03) * 0.3));
const scribble = (n = 0.2) => { const z = noise(n), a = smooth(z, 4), b = smooth(z, 40); return a.map((v, i) => (v - b[i]) * (0.6 + 0.4 * Math.sin(2 * Math.PI * 22 * i / SR)) * 0.35); };
const poof = () => shape(smooth(noise(0.35), 30), (t) => Math.exp(-t / 0.08) * 1.2);
const stamp = () => add(shape(sweep(160, 70, 0.12), (t) => Math.exp(-t / 0.04) * 0.45), click(0.5));
const chime = (notes = [1046.5, 1318.5, 1568], gap = 0.07, amp = 0.12) => { const o = new Float32Array(len(1)); notes.forEach((f, j) => { const s = Math.round(j * gap * SR); for (let i = s; i < o.length; i += 1) { const t = (i - s) / SR; o[i] += Math.sin(2 * Math.PI * f * t) * Math.exp(-t / 0.28) * amp; } }); return o; };
const riser = (n) => { const o = new Float32Array(len(n)); let ph = 0; for (let i = 0; i < o.length; i += 1) { const t = i / SR; const f = 300 + 900 * (t / n) ** 2; ph += 2 * Math.PI * f / SR; o[i] = Math.sin(ph) * (t / n) * 0.06; } return o; };
const put = (snd, b, g = 1) => { const i0 = Math.round(T(b) * SR); for (let i = 0; i < snd.length && i0 + i < N; i += 1) if (i0 + i >= 0) fx[i0 + i] += snd[i] * g; };
// Each cue is a named sound. With --sfx-dir, a file named after the cue (send.wav, receive.mp3, ...)
// replaces the synthesized fallback; files are trimmed of leading silence and peak-matched.
const SFX_DIR = args['sfx-dir'] ? path.resolve(args['sfx-dir']) : null;
const PEAK = { send: 0.5, receive: 0.4, typing: 0.22, hop: 0.35, drop: 0.45, tick: 0.3, click: 0.4, chomp: 0.55, whoosh: 0.35, slap: 0.45, boing: 0.4, stamp: 0.5, scribble: 0.35, poof: 0.4, pop: 0.4, riser: 0.25, chime: 0.4 };
const sampleCache = {};
function sample(name) {
  if (!SFX_DIR) return null;
  if (name in sampleCache) return sampleCache[name];
  const file = ['wav', 'mp3', 'm4a', 'ogg', 'aif'].map((e) => path.join(SFX_DIR, `${name}.${e}`)).find((f) => fs.existsSync(f));
  if (!file) return (sampleCache[name] = null);
  const d = spawnSync('ffmpeg', ['-v', 'error', '-i', file, '-ac', '1', '-ar', String(SR), '-f', 'f32le', '-'], { maxBuffer: 1 << 28 });
  let x = new Float32Array(d.stdout.buffer, d.stdout.byteOffset, Math.floor(d.stdout.byteLength / 4));
  let pk = 0; for (const v of x) pk = Math.max(pk, Math.abs(v));
  let i0 = 0; while (i0 < x.length && Math.abs(x[i0]) < pk * 0.05) i0 += 1;
  x = x.slice(Math.max(0, i0 - Math.round(SR * 0.003)), Math.min(x.length, i0 + SR * 2.5));
  const g = pk > 0 ? (PEAK[name] || 0.4) / pk : 0;
  return (sampleCache[name] = x.map((v) => v * g));
}
const synth = {
  send: () => pop(520, 900, 0.08, 0.2), receive: (who) => pop((pitch[who] || 800) + 260, pitch[who] || 800, 0.07, 0.16),
  typing: () => click(0.35), hop: (k = 0) => boing(260 + k * 40, 560 + k * 60, 0.22), drop: (a = 0.8) => thock(a), tick: () => tick(),
  click: (a = 0.8) => click(a), chomp: () => chomp(), whoosh: (n = 0.4, a = 0.2) => whoosh(n, a), slap: () => slap(), boing: (up = true) => (up ? boing(300, 800, 0.3) : boing(700, 250, 0.3)),
  stamp: () => stamp(), scribble: () => scribble(0.35), poof: () => poof(), pop: () => pop(500, 900, 0.1, 0.16), riser: () => riser(2.0), chime: () => chime(),
};
const pitch = { c1: 680, c2: 760, c3: 840, c4: 920, c5: 1000 };
const cue = (name, b, g = 1, ...a) => put(sample(name) || synth[name](...a), b, g);
const CHAT = [['human', 0.5, 1], ['c5', 6.5, 0.5], ['c5', 13.5, 0.5], ['human', 20.5, 0.5], ['c3', 22.5, 1], ['c4', 33.5, 0.5], ['c3', 38.5, 1], ['c2', 40.5, 1], ['human', 45, 0.5], ['c2', 47, 0.5], ['human', 49, 0.5], ['c5', 51.5, 1], ['c2', 53.5, 1], ['c5', 61.5, 1], ['human', 63.5, 1]];
for (const [who, b, typing] of CHAT) {
  if (who === 'human') {
    const loop = sample('typing');
    if (loop && loop.length > SR * 0.6) {                // a recorded typing run: play the slice that fits, faded out
      const n = Math.min(loop.length, Math.round((typing * P - 0.12) * SR)), f = Math.round(SR * 0.04);
      put(loop.slice(0, n).map((v, i) => v * Math.min(1, (n - i) / f)), b - typing + 0.06, 0.8);
    } else for (let t = b - typing + 0.12; t < b - 0.1; t += 0.23) cue('typing', t, 0.8);
    cue('send', b);
  }
  else cue('receive', b, 1, who);
}
[3.25, 3.5, 3.75, 4.0, 4.25].forEach((b, k) => cue('hop', b, 0.7, k));          // crew hop onto their cursors
cue('click', 53.5, 0.7);
cue('drop', 4.75); cue('drop', 5.45);
for (let i = 0; i < 5; i += 1) cue('tick', 5.5 + i * 0.5, 1.1);                  // shot placeholders
cue('drop', 7.05); cue('click', 7.5);
cue('chomp', 12.75, 0.8);
cue('click', 15.5, 0.7);
for (let i = 0; i < 4; i += 1) cue('tick', 21 + i, 1.2);                         // keyframe diamonds
cue('whoosh', 23, 0.9, 0.35, 0.2); cue('drop', 28.4, 0.8, 0.6);
cue('boing', 33.5, 0.9, true); cue('slap', 34, 0.7); cue('boing', 35, 0.9, false); cue('drop', 36, 0.8, 0.7);
cue('click', 36.5); cue('whoosh', 37, 0.8, 0.4, 0.18); cue('send', 38.5); cue('pop', 39.5); cue('click', 40.5);
for (const b of [42.5, 43.5, 44.5]) cue('tick', b, 1.3);                          // a check per result
cue('stamp', 45); cue('whoosh', 47.5, 0.7, 0.35, 0.15);
cue('slap', 44.5, 0.8); cue('scribble', 47.5); cue('poof', 48, 0.8);           // sticker, strike, poof
for (let i = 0; i < 6; i += 1) cue('stamp', 50.5 + i * 0.5, 0.75);              // proof stamps
cue('pop', 55.5); cue('chomp', 56.5, 0.9); cue('riser', 57); cue('chime', 61);
cue('boing', 62, 0.5, true);
cue('whoosh', 66, 1, 0.9, 0.3);
const fg = 10 ** (Number(args['foley-gain'] ?? 0) / 20) * 0.8;

// ---------- mix, write, loudness ----------
const raw = path.join(tmp, 'mix.wav');
const buf = Buffer.alloc(44 + N * 4);
buf.write('RIFF', 0); buf.writeUInt32LE(36 + N * 4, 4); buf.write('WAVEfmt ', 8); buf.writeUInt32LE(16, 16); buf.writeUInt16LE(1, 20); buf.writeUInt16LE(2, 22);
buf.writeUInt32LE(SR, 24); buf.writeUInt32LE(SR * 4, 28); buf.writeUInt16LE(4, 32); buf.writeUInt16LE(16, 34); buf.write('data', 36); buf.writeUInt32LE(N * 4, 40);
let peak = 0; for (let i = 0; i < N; i += 1) peak = Math.max(peak, Math.abs(L[i] + fx[i] * fg), Math.abs(R[i] + fx[i] * fg));
const norm = peak > 0.97 ? 0.97 / peak : 1;
for (let i = 0; i < N; i += 1) { buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, (L[i] + fx[i] * fg) * norm)) * 32767), 44 + i * 4); buf.writeInt16LE(Math.round(Math.max(-1, Math.min(1, (R[i] + fx[i] * fg) * norm)) * 32767), 46 + i * 4); }
fs.writeFileSync(raw, buf);
const lufs = Number(args.lufs ?? -16);
const out = path.join(OUT, 'soundtrack.wav');
const ln = spawnSync('ffmpeg', ['-v', 'error', '-y', '-i', raw, '-af', `loudnorm=I=${lufs}:TP=-1.5:LRA=11`, '-ar', String(SR), '-c:a', 'pcm_s16le', out]);
if (ln.status !== 0) { fs.copyFileSync(raw, out); console.log('WARN loudnorm failed; wrote the peak-normalised mix'); }
const beats = { beat: +P.toFixed(6), offset: +offset.toFixed(4), duration, bpm: +(60 / P).toFixed(2), source: path.resolve(args.music), start: +start.toFixed(3), final_hit: +T(74).toFixed(3) };
fs.writeFileSync(path.join(OUT, 'beats.json'), JSON.stringify(beats, null, 1));
fs.rmSync(tmp, { recursive: true, force: true });
console.log(`Wrote ${path.join(OUT, 'beats.json')} and ${out}`);
console.log(JSON.stringify(beats));

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
