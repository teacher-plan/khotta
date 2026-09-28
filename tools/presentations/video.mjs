// يحوّل صفحة مشاهد (فيها window.DURS و window.seek) + مقاطع صوت المشاهد إلى MP4 (H.264 + AAC) صالح للواتساب.
// node video.mjs مشاهد.html مجلد_الصوت خرج.mp4 [fps]   — يحتاج: pip install imageio-ffmpeg
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
import { spawn, spawnSync, execSync } from 'child_process';
import fs from 'fs'; import path from 'path';
const [f, audioDir, out, fpsArg] = process.argv.slice(2); const FPS = Number(fpsArg || 25);
const FF = process.env.FFMPEG || execSync(`python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"`).toString().trim();
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
const html = fs.readFileSync(f, 'utf8');
await p.route('http://deck.local/**', r => r.fulfill({ contentType: 'text/html', body: html }));
await p.goto('http://deck.local/x.html'); await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
const DURS = await p.evaluate(() => window.DURS);
const mp3 = fs.readdirSync(audioDir).filter(x => x.endsWith('.mp3')).sort();
const tmp = out.replace(/\.mp4$/, '.video.mp4');
const enc = spawn(FF, ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-loglevel', 'error', '-preset', 'medium', '-crf', '20', tmp], { stdio: ['pipe', 'ignore', 'inherit'] });
let frames = 0;
for (let i = 0; i < DURS.length; i++) {
  const n = Math.round(DURS[i] / 1000 * FPS);
  for (let k = 0; k < n; k++) {
    await p.evaluate(([i, t]) => window.seek(i, t), [i, k * 1000 / FPS]);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once('drain', r));
    frames++;
  }
  process.stdout.write(`مشهد ${i + 1}/${DURS.length}\n`);
}
enc.stdin.end(); await new Promise(r => enc.on('close', r)); await b.close();
// الصوت: كل مقطع يبدأ مع مشهده
let start = 0; const ins = [], flt = [];
mp3.forEach((m, i) => { ins.push('-i', path.join(audioDir, m)); flt.push(`[${i + 1}:a]adelay=${start}|${start}[a${i}]`); start += Math.round(Math.round(DURS[i] / 1000 * FPS) * 1000 / FPS); });
flt.push(mp3.map((_, i) => `[a${i}]`).join('') + `amix=inputs=${mp3.length}:normalize=0[aout]`);
const r = spawnSync(FF, ['-y', '-loglevel', 'error', '-i', tmp, ...ins, '-filter_complex', flt.join(';'), '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], { stdio: 'inherit' });
if (r.status) process.exit(r.status);
fs.unlinkSync(tmp); console.log(out, frames, 'إطار');
