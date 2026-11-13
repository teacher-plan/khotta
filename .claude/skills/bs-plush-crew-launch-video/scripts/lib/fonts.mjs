// Fetches a Google Fonts family as local woff2 files, subset to the exact characters the film uses
// (css2 "text=" parameter), so a brand face can be used without shipping or installing it.
import fs from 'node:fs';
import path from 'node:path';

const UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36';

export async function fetchGoogleFont({ family, weights = [700], text, outDir, alias }) {
  const fam = family.trim().replace(/ /g, '+');
  const url = `https://fonts.googleapis.com/css2?family=${fam}:wght@${weights.join(';')}&display=block${text ? `&text=${encodeURIComponent(text)}` : ''}`;
  const res = await fetch(url, { headers: { 'User-Agent': UA } });
  if (!res.ok) throw new Error(`Google Fonts ${res.status} for "${family}"`);
  let css = await res.text();
  const urls = [...css.matchAll(/url\((https:[^)]+)\)/g)].map((m) => m[1]);
  if (!urls.length) throw new Error(`no font files for "${family}"`);
  fs.mkdirSync(outDir, { recursive: true });
  const slug = family.toLowerCase().replace(/[^a-z0-9]+/g, '-');
  let i = 0;
  for (const u of [...new Set(urls)]) {
    const r = await fetch(u, { headers: { 'User-Agent': UA } });
    if (!r.ok) throw new Error(`font file ${r.status}`);
    const buf = Buffer.from(await r.arrayBuffer());
    const ext = /format\('truetype'\)/.test(css) && !/woff2/.test(css) ? 'ttf' : 'woff2';
    const name = `${slug}-${i++}.${ext}`;
    fs.writeFileSync(path.join(outDir, name), buf);
    css = css.split(u).join(`fonts/${name}`);
  }
  if (alias) css = css.replace(/font-family: '[^']+'/g, `font-family: '${alias}'`);
  return css;
}
