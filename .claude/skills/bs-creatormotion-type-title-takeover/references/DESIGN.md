# B-roll visual system

## Style Prompt

An editorial motion toolkit for creator explanations. Strong typographic hierarchy, generous margins, precise diagrams, and confident short transitions. A viewer should understand the changing relationship before reading every label. A real presenter is framed as a participant in the composition. Content occupies the frame; there are no decorative dashboards or boilerplate title cards wrapped around every effect.

## Colors

| Style | Canvas | Text | Muted text | Accent | Accent ink | Grid lines |
|---|---|---|---|---|---|---|
| white-yellow (default) | #FAFAF8 | #18201D | #58615A | #F4CE36 | #18201D | light grey, 5.5% / 8.5% ink |
| charcoal-lime | #0A0D0B | #F6F8EF | #AEBBAE | #CAED79 | #18201D | light grey, 6% / 10% |
| midnight-ice (Black & White) | #09090A | #F5F5F5 | #ADADAD | #F0F0F0 | #141414 | light grey, 6% / 10% |

Accents identify the changing element, not every element, and never fill a large background. White-yellow is the default. The Paper & Orange palette was retired in 2.0.0; `--style paper-orange` stops with an error that lists the three styles. User colour overrides replace semantic tokens (`bg`, `surface`, `ink`, `muted`, `accent`, `accent-ink`, `rule`, `radius`, `shadow`, `glass`, `glass-strong`, `glass-border`, `glass-edge`, `glass-hi`, `glass-shadow`, `grid`, `grid-major`), with contrast checked before delivery.

Every canvas carries the same static light-grey grid: a 60 px minor grid and a 240 px major grid (`var(--canvas-bg)`). There are no gradient glows or colour fields behind content.

Frosted glass (`.glass`: translucent fill, backdrop blur, a light hairline border and a soft shadow) is reserved for text that sits on top of footage and must stay legible. Everything else sits directly on the grid.

## Typography

- Smiley Sans (Deyi Hei) v2.0.1, SIL OFL, is the default face for every language: titles, copy, labels and diagram text, Latin and Chinese alike. It is a single slanted display weight, so hierarchy comes from size, colour and spacing, not weight; synthetic bold is disabled.
- IBM Plex Mono, 400/500: axis ticks, ordinals, counters and other tabular numbers, and small eyebrow labels only. Numbers that count up use it so their width stays stable.
- Noto Sans SC stays behind Smiley Sans for rare Chinese characters. `--zh-font noto-sans-sc` switches Chinese content to Noto Sans SC; `--font` (or an `overrides.font` token) always wins, with Smiley Sans kept as the CJK fallback.
- Headlines 72–176 px on the design canvas depending on aspect and role; portrait headlines are larger relative to the frame width. Labels at least 28 px, small mono labels at least 22 px.
- All fonts are bundled locally with their SIL Open Font Licenses; rendering never fetches a font.

## Layout and Motion

- Four aspect ratios, each laid out natively rather than scaled: 16:9 (1920×1080 design canvas), 4:3 (1440×1080), 3:4 (1080×1440) and 9:16 (1080×1920). Effects read `ctx.aspect`, `ctx.width`, `ctx.height`, `ctx.portrait` and `ctx.safe` and choose their arrangement from a per-aspect table; portrait usually stacks what landscape places side by side.
- Output resolution is a zoom of the same layout: 1080P keeps the 1080 short side, 2K uses 1440 and 4K (the default) uses 2160, so a 4K 9:16 segment is 2160×3840 and a 4K 4:3 segment is 2880×2160. 30 fps.
- Layout settled states with grid/flex and gap before authoring motion. Canvas-bound positioned elements are allowed for spatial diagrams, camera planes, masks and presenter frames when their geometry is deliberate.
- Start entrances after 0.16 seconds. Use power3.out for confident movement, expo.out for decisive reveals, sine.inOut for reading-time travel, back.out(1.15) only for physical pops.
- Timeline beats communicate structure. Draw before label, reveal before compare, move before resolve. A meaningful settled reading interval is required.
- Preserve the defining movement of each effect. A new palette or aspect never justifies replacing it with a generic card animation.
- Thin dividers, simple abstract symbols and sparse diagrams; 1.5–3 px rules and 3–5 px diagram strokes on the design canvas; essential moving paths may be stronger. Shadows are restrained and palette-aware.
- The three styles keep the same motion, content and type metrics so they can be compared directly.

## Caption safe area and presenter framing

Every segment is cut into a video that will carry the creator's own subtitles, so the bottom band of the frame belongs to captions. On Shorts, Reels and TikTok the same band also holds the platform's caption and buttons.

| Aspect | Design canvas | Keep clear at the top | Caption band at the bottom |
|---|---|---|---|
| 16:9 | 1920×1080 | 72 px | 250 px (lowest 23%) |
| 4:3 | 1440×1080 | 64 px | 250 px (lowest 23%) |
| 3:4 | 1080×1440 | 72 px | 360 px (lowest 25%) |
| 9:16 | 1080×1920 | 170 px | 560 px (lowest 29%) |

The generator passes these values to every effect as `safe.top` and `safe.bottom` (`scripts/themes.mjs`, `safeAreas`). These bands apply to segments that show footage. A graphics-only segment (no `--media`) is centred in the whole frame with natural proportions and keeps only the lowest tenth of the frame clear, because its subtitles sit over plain graphics; the generator then passes `safe.bottom` as 10 % of the height.

- Cards, panels, labels, chart axes and any readable text sit between the two bands. Place them toward the top of the frame; never anchor a card to the bottom edge. Only footage, the presenter's body and background planes may enter the caption band.
- Text over footage goes beside or above the face, never across it and never in the caption band. Landscape: a panel in the top-left or top-right corner beside the subject. Portrait: a short horizontal strip above the head.
- Split layouts are hard splits. The presenter fills one half edge to edge, with no card, frame or rounded window around the footage. Landscape (16:9, 4:3) splits left/right with the head centred in its half; portrait (9:16, 3:4) puts the content on top and the presenter below, with the face raised above the caption band.
- Landscape footage serves 16:9 and 4:3; portrait footage serves 9:16 and 3:4.
- The presenter's head is centred horizontally in the region the presenter occupies and, in landscape, vertically too. In a portrait split (presenter in the lower half) the face is raised so the chin stays above the caption band; the generator does this automatically for wide regions at the bottom of a portrait canvas, at the cost of a slightly tighter crop at the top of the head. Effects compute the crop with `ctx.frame(w, h)` from the real footage size and the face position passed with `--focus x,y` (fractions of the footage frame); never hand-tune `object-position` and never scale the head out of the region.
- Full-frame B-roll without footage (charts, chapter cards, diagrams) is centred in the whole frame with natural proportions; only the lowest tenth stays clear.
- No decorative cards. Charts, chapter titles, lists and diagrams sit directly on the canvas grid; do not wrap them in a card, panel or rounded box. A frosted-glass panel is used only where text has to stay legible on top of footage, and the presenter half of a split never has a frame.

## What NOT to Do

- No source creator names, copied titles, logos, watermarks or recognizable proprietary interface skins in generated examples.
- No fake photos from CSS polygons. Use supplied media or ImageGen when a visual truly needs imagery.
- No repeated full-screen presenter loops with visible jump seams. Cut away, choose a long-enough take, or generate a longer take when needed.
- No all-purpose animated card template that merely changes its heading for different Skills.
- No unreadable mini-labels, decorative cards or panels around content, frosted glass away from footage, gradient blobs, or jitter on settled text.
- No blur that stays on screen: no defocused footage or presenters, no depth-of-field blur on images, no blurred rows. Separate layers with scale, position, opacity, a light desaturation or dimming instead. Brief entrance or exit transitions (0.6 s or less) may animate through blur; frosted glass behind text over footage is the only lasting blur.
- Default images follow the clean modern studio look: bright, cool, neutral white and grey, soft daylight, generous negative space, at most one small yellow accent; interfaces are white with a crisp sans-serif. No warm beige, sepia or cosy-cottage styling.
- No original reference media in installable Skill packages.
