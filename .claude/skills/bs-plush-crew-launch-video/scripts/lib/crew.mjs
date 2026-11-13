// Picks the five crew members from the chosen character style so their colors follow the brand:
// the director (c1) wears the color closest to the brand, the audio crew (c5) the next closest
// (or the first accent), and the other three spread out for variety. Each character appears once.
import fs from 'node:fs';
import path from 'node:path';
import { distance, forWhiteText } from './color.mjs';

export const STYLES = {
  bots: 'Geometric bots: flat vivid shapes with two simple eyes',
  faces: 'Expressive shapes: muted flat shapes with cartoon faces',
  felt: 'Felt plush: fuzzy felted characters with tiny accessories',
};
const DIRS = { bots: 'bots', faces: 'faces', felt: 'felt' };

export const CREW_DEFAULTS = {
  en: { c1: ['Sunny', 'Director'], c2: ['Footnote', 'Fact-check'], c3: ['Doodle', 'Layout'], c4: ['Blip', 'Animator'], c5: ['Rumble', 'Audio'] },
};

export function castDir(engineCrewDir, style) {
  if (!DIRS[style]) throw new Error(`unknown style "${style}" (${Object.keys(STYLES).join(' | ')})`);
  return path.join(engineCrewDir, DIRS[style]);
}

export function loadCast(dir) {
  return JSON.parse(fs.readFileSync(path.join(dir, 'crew.json'), 'utf8'));
}

export function pickCrew({ cast, brand, accents = [], overrides = [] }) {
  const left = [...cast];
  const take = (target) => { left.sort((a, b) => distance(a.color, target) - distance(b.color, target)); return left.shift(); };
  const chosen = [take(brand)];
  for (const a of accents) { if (chosen.length >= 2) break; chosen.push(take(a)); }
  if (chosen.length < 2) chosen.push(take(brand));
  // fill the rest by farthest-point sampling so the line-up stays varied
  while (chosen.length < 5) {
    left.sort((a, b) => Math.min(...chosen.map((x) => distance(b.color, x.color))) - Math.min(...chosen.map((x) => distance(a.color, x.color))));
    chosen.push(left.shift());
  }
  // director c1 = brand family, audio c5 = second color, the rest in order
  const order = { c1: chosen[0], c5: chosen[1], c3: chosen[2], c2: chosen[3], c4: chosen[4] };
  const names = CREW_DEFAULTS.en;
  return ['c1', 'c2', 'c3', 'c4', 'c5'].map((id) => {
    const o = overrides.find((x) => x.id === id) || {};
    const item = (o.file && cast.find((c) => path.basename(c.file) === path.basename(o.file))) || order[id];
    return { id, name: o.name || names[id][0], role: o.role || names[id][1], file: item.file, swatch: item.color, color: forWhiteText(item.color), shape: item.shape };
  });
}
