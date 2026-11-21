// Small color helpers: parsing, mixing, luminance, contrast and a perceptual distance.
export function parse(c) {
  const s = String(c || '').trim();
  let m = s.match(/^#?([0-9a-f]{3}|[0-9a-f]{6})$/i);
  if (m) {
    const h = m[1].length === 3 ? m[1].replace(/./g, (x) => x + x) : m[1];
    const n = parseInt(h, 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  m = s.match(/^rgba?\(\s*([\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)/i);
  if (m) return [Number(m[1]), Number(m[2]), Number(m[3])];
  throw new Error(`not a color: ${c}`);
}
export const hex = (rgb) => '#' + rgb.map((v) => Math.round(Math.min(255, Math.max(0, v))).toString(16).padStart(2, '0')).join('').toUpperCase();
export const mix = (a, b, k) => { const A = parse(a), B = parse(b); return hex(A.map((v, i) => v + (B[i] - v) * k)); };
export function luminance(c) {
  const [r, g, b] = parse(c).map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}
export function contrast(a, b) { const x = luminance(a), y = luminance(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); }
export function hsl(c) {
  const [r, g, b] = parse(c).map((v) => v / 255);
  const max = Math.max(r, g, b), min = Math.min(r, g, b), l = (max + min) / 2;
  if (max === min) return [0, 0, l];
  const d = max - min, s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
  let h = max === r ? (g - b) / d + (g < b ? 6 : 0) : max === g ? (b - r) / d + 2 : (r - g) / d + 4;
  return [h * 60, s, l];
}
function lab(c) {
  const [r, g, b] = parse(c).map((v) => { v /= 255; return v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; });
  const f = (t) => (t > 216 / 24389 ? Math.cbrt(t) : (24389 / 27 * t + 16) / 116);
  const x = f((0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047), y = f(0.2126 * r + 0.7152 * g + 0.0722 * b), z = f((0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883);
  return [116 * y - 16, 500 * (x - y), 200 * (y - z)];
}
export function distance(a, b) { const A = lab(a), B = lab(b); return Math.hypot(A[0] - B[0], A[1] - B[1], A[2] - B[2]); }
// darken until white text on it reaches the given contrast (name tags, role chips)
export function forWhiteText(c, min = 3.2) {
  let out = hex(parse(c));
  for (let k = 0; k < 20 && contrast(out, '#ffffff') < min; k += 1) out = mix(out, '#121313', 0.08);
  return out;
}
// a light, saturated highlighter that ink text stays readable on
export function highlighter(brand) {
  const [h, s, l] = hsl(brand);
  if (s < 0.15 || l < 0.08) return '#F4FF71';      // neutral brands keep the default acid highlighter
  if (luminance(brand) > 0.62 && s > 0.45) return hex(parse(brand));
  // same hue, marker-pen vivid: high saturation, then lighten until ink text reads on it
  let L = 0.62, out = fromHsl(h, Math.max(s, 0.85), L);
  for (let k = 0; k < 30 && luminance(out) < 0.45; k += 1) { L += 0.015; out = fromHsl(h, Math.max(s, 0.85), L); }
  return out;
}
export function fromHsl(h, s, l) {
  const c = (1 - Math.abs(2 * l - 1)) * s, x = c * (1 - Math.abs(((h / 60) % 2) - 1)), m = l - c / 2;
  const [r, g, b] = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x] : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x];
  return hex([(r + m) * 255, (g + m) * 255, (b + m) * 255]);
}
