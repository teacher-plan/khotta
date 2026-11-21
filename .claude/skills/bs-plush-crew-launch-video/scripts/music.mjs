#!/usr/bin/env node
// Generates the instrumental music bed with ElevenLabs Music, either directly
// with an ElevenLabs API key or through FAL. (The default route, ChatCut, is
// driven from the agent with ChatCut's own tools; see references/music.md.)
//
//   node music.mjs --provider elevenlabs --seconds 75 --out assets/music.mp3 [--prompt "..."]
//   node music.mjs --provider fal        --seconds 75 --out assets/music.mp3 [--prompt "..."]
//
// ELEVENLABS_API_KEY (or XI_API_KEY) is read for --provider elevenlabs and
// FAL_KEY for --provider fal. Both are paid per job: confirm with the user
// before running. A FAL request is recorded in <out>.fal.json so polling a
// slow job again never submits a second paid job.
import fs from 'node:fs';
import path from 'node:path';
import { Ledger, inputHash, submit, waitFor, download } from './lib/fal.mjs';

const DEFAULT_PROMPT =
  'Playful, bouncy product-launch track at a steady 120 BPM in 4/4. Punchy kick and claps on every beat, plucky marimba and synth bass, bright toy-like bell accents, cheerful and confident like a cartoon studio at work. Keep the same groove from start to finish with no slow intro and no breakdowns, add small fills every eight bars, and end on one big final hit with a short ring-out. Instrumental, no vocals.';

const args = parseArgs(process.argv.slice(2));
if (!args.out || !args.provider) {
  console.error('Usage: node music.mjs --provider elevenlabs|fal --seconds 75 --out music.mp3 [--prompt "..."]');
  process.exit(2);
}
const OUT = path.resolve(args.out);
const seconds = Math.max(10, Math.min(300, Number(args.seconds || 75)));
const prompt = String(args.prompt || DEFAULT_PROMPT);
fs.mkdirSync(path.dirname(OUT), { recursive: true });

if (args.provider === 'elevenlabs') {
  const key = process.env.ELEVENLABS_API_KEY || process.env.XI_API_KEY;
  if (!key) {
    console.error('ELEVENLABS_API_KEY is not set. Export it, or use --provider fal with FAL_KEY, or generate the music in ChatCut.');
    process.exit(1);
  }
  const res = await fetch('https://api.elevenlabs.io/v1/music?output_format=mp3_44100_192', {
    method: 'POST',
    headers: { 'xi-api-key': key, 'Content-Type': 'application/json', Accept: 'audio/mpeg' },
    body: JSON.stringify({ prompt, music_length_ms: Math.round(seconds * 1000), model_id: 'music_v1', force_instrumental: true }),
  });
  if (!res.ok) {
    console.error(`ElevenLabs ${res.status}: ${(await res.text()).slice(0, 500)}`);
    process.exit(1);
  }
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync(OUT, buf);
  const rid = res.headers.get('request-id') || res.headers.get('x-request-id') || '';
  console.log(`Wrote ${OUT} (${(buf.length / 1024).toFixed(0)} KB)${rid ? `  request ${rid}` : ''}`);
} else if (args.provider === 'fal') {
  const model = String(args.model || 'elevenlabs/music/v2.5');
  const input = { prompt, music_length_ms: Math.round(seconds * 1000), force_instrumental: true, output_format: 'mp3_48000_192' };
  const ledger = new Ledger(`${OUT}.fal.json`);
  const hash = inputHash(model, input);
  let job = ledger.get('music');
  if (!job || job.hash !== hash || args.resubmit) {
    const sub = await submit(model, input);
    job = { model, hash, ...sub };
    ledger.set('music', job);
    console.log(`Submitted ${model}  request ${sub.requestId}`);
  } else console.log(`Polling existing request ${job.requestId}`);
  const result = await waitFor(job, { onTick: (st) => process.stdout.write(`\r  ${st.status}   `) });
  process.stdout.write('\n');
  const url = (result.audio && result.audio.url) || (result.audio_file && result.audio_file.url);
  if (!url) throw new Error(`no audio url in result: ${JSON.stringify(result).slice(0, 300)}`);
  const bytes = await download(url, OUT);
  ledger.set('music', { done: true, file: OUT });
  console.log(`Wrote ${OUT} (${(bytes / 1024).toFixed(0)} KB)  request ${job.requestId}`);
} else {
  console.error('--provider must be elevenlabs or fal (ChatCut is driven from the agent, see references/music.md)');
  process.exit(2);
}

function parseArgs(list) {
  const o = {};
  for (let i = 0; i < list.length; i += 1) {
    if (!list[i].startsWith('--')) continue;
    const k = list[i].slice(2);
    const v = list[i + 1];
    if (v === undefined || v.startsWith('--')) o[k] = true;
    else {
      o[k] = v;
      i += 1;
    }
  }
  return o;
}
