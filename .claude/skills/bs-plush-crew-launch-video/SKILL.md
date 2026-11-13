---
name: bs-plush-crew-launch-video
description: "Turn any product link into a 40-second launch film where five cute characters, in the style you pick (geometric bots, expressive shapes or felt plush), build your product's promo live in a playful team editor: chat, cursors, a beat-synced timeline and a preview that plays your logo, real screenshots, key features and URL. The Skill reads the site, checks every claim against it, matches the crew's colors to your brand and delivers an editable film plus a 4K or 1080p MP4 in English, Chinese or both. Use it for launch posts, product announcements and social clips."
---

# Plush Crew Launch Video

A human asks the team chat "Who can explain <product> in 40 seconds?" Five
crew characters hop onto their cursors and make the film live: they drop
clips on the timeline, bite the beat, jump into an empty slot and fact-check
a hype sticker, while the preview plays the product's own film: logo, hero
line, real outputs, where it works, how it works, why to trust it. The camera
pushes into the preview for the end card and the crew jump on the final hit.

The choreography is fixed and beat-timed; the product supplies the words,
colors, logo and images. Read `references/story-mapping.md` once before the
first film: it shows the whole timeline.

## What you deliver

- `film/` - an editable, previewable HTML film (`node <skill>/scripts/serve.mjs film`).
- `soundtrack.wav` - the fitted music with the interface foley.
- `<name>-<lang>-<res>.mp4` - about 41 s, 30 fps H.264 + AAC, at the
  resolution picked in the opening dialog (4K or 1080p; 2K on request).
- `factcheck.md` - every on-screen claim with its source page and status.
- A short report: the images used, the music route and job ids, and anything
  the user should check.

## Inputs

- A link to the product (required): its website, or a product page such as
  an App Store, Google Play, Chrome Web Store or Product Hunt listing. Product
  material (screenshots, a logo, a press kit, docs) can replace or add to it;
  the film still needs a URL to show on the end card.
- Chosen in the opening dialog: the character style and the language(s).
- Optional: resolution, a music track the user owns, brand colors, a better
  logo file.

## Requirements

- Node.js 20+ and FFmpeg on PATH.
- In the project folder: `npm install playwright-core`, plus Google Chrome
  (preferred) or `npx playwright install chromium`.
- Music, one of (see `references/music.md`): ChatCut Desktop tools (default),
  `ELEVENLABS_API_KEY`, `FAL_KEY`, or a track the user owns.
- Internet for the capture (and for a Google Fonts brand face; `--offline`
  builds with the bundled fonts).

Run every script with the project folder as the working directory, so
Playwright resolves: `cd <project> && node <skill>/scripts/<script>.mjs ...`.

## Workflow

1. **Ask first: style, language and resolution.** Before any other work,
   ask all three in one dialog with the host's question tool (for example `AskUserQuestion`;
   without one, a short numbered list in chat) and wait for the answers. If
   the host can show images, show the three preview strips first.

   - **Character style** (`style` in the storyboard). Use these three option
     labels; the names Grok Bot, Manus Cue and ChatGPT Dots are the terms
     users know these looks by, so never translate or paraphrase them (only
     the word "style" is written in the dialog language, after the name):
     - **Grok Bot style** -> `bots`: flat vivid geometric shapes with two
       simple eyes (`references/engine/crew/bots/preview.webp`)
     - **Manus Cue style** -> `faces`: muted flat shapes with cartoon faces,
       eyebrows and winks (`references/engine/crew/faces/preview.webp`)
     - **ChatGPT Dots style** -> `felt`: fuzzy felted characters with tiny
       accessories (`references/engine/crew/felt/preview.webp`)

     All eight characters of each style are original designs drawn for this
     Skill; the labels only name the look they follow.
   - **Language**: the first option, marked as the default, is the language
     the user wrote the request in; then English, Simplified Chinese, and
     "English + Chinese" (two films on the same music). Offer the user's
     language first even when it is neither of these.

   - **Resolution**: 4K (3840x2160) or 1080p (1920x1080). 2K stays available
     on request.

   Skip a question only when the request already answers it. Then set up
   `<project>/`, install `playwright-core`, and confirm the URL and the music
   route. Music generation is billed by its
   provider: say so and wait for a yes before submitting.
2. **Research** - follow `references/research.md`. Capture the site with
   `capture.mjs` (add `--locale <lang>`, for example `zh-CN` or `ja-JP`, for a
   non-English film; also try the site's own language path such as `/zh`).
   Read `site.json`, every screenshot and the pages that hold the facts
   (features, how it works, pricing, FAQ). Pick the mark, the brand color and
   the images. List each fact you will use with its URL in `sources`.
   - When a company has several products, film the one the link points to.
   - When the site has no copy in the film's language, translate its own
     words faithfully, keeping every scope word, and say so in the report.
   - When the capture is blocked (login wall, bot check, empty app shell) or
     yields too few usable images, stop and ask the user for screenshots, a
     logo file and the key facts instead of guessing. Never invent a
     screenshot or a feature.
3. **Write the storyboard** - `film.json` per `references/storyboard-schema.md`,
   mapped with `references/story-mapping.md`. Start from
   `references/example-storyboard.json`. Every claim comes from the product's
   own pages: no invented numbers, prices, customers, reviews or features.
   Pricing words ("free", "unlimited", prices) need the pricing page itself
   (see "Pricing words" in `references/story-mapping.md`). Before building,
   re-read every line of the storyboard against `sources` and fix or cut any
   line that is not backed.
4. **Music** - generate or collect the track (`references/music.md`), then
   fit and mix it:

   ```bash
   node <skill>/scripts/soundtrack.mjs --music assets/music.mp3 --sfx-dir sfx --out-dir .
   ```

   Collect the interface sound effects into `sfx/` first ("Sound effects" in
   `references/music.md`); without them the film only has thin synthesized
   placeholders.

5. **Build and review**

   ```bash
   node <skill>/scripts/build.mjs --storyboard film.json --out film --beats beats.json
   node <skill>/scripts/qa.mjs film --out qa --per-scene 3
   ```

   Fix every `ERROR` and read every `WARN` and `console.warning` (long text is
   shrunk and reported). Look at every QA sheet: text that is cut or shrunk,
   a mark that is unreadable on its tile, images that crop badly, a highlight
   that is too pale, chat bubbles longer than two lines. Check single moments
   with `qa.mjs film --out qa --times 8.8,24.5`. Rebuild after each change.
   The build prints the crew it picked; to change it, set `crew` overrides or
   `file` from the style's `crew.json` (see the schema).
6. **Render**

   ```bash
   node <skill>/scripts/render.mjs film --out acme-en-4k.mp4 --resolution 4k \
        --workers 6 --audio soundtrack.wav --audio-fade 0.05
   ```

   The stage is laid out at 1920x1080; 2K and 4K render the same frames at a
   higher pixel density.
7. **Verify and deliver** - `ffprobe` the MP4 (resolution, 30 fps, audio,
   duration), make a contact sheet
   (`ffmpeg -i film.mp4 -vf "fps=1/2,scale=480:-1,tile=5x4" -frames:v 1 sheet.jpg`),
   look at it, then deliver the MP4, the `film/` folder, `factcheck.md` and
   the report.

For a second language, write a second storyboard (`film-zh.json`) with the
workspace labels, crew names and default chat lines in that language
("Other languages" in `references/storyboard-schema.md`), build it into its
own folder with the same `beats.json`, and render it with the same
`soundtrack.wav`.

## Quality bar

- It reads as the product: its own mark, colors, hero line, outputs and URL.
  The crew wear the brand's colors; the director wears the closest one.
- Every word in the preview is true and sourced. Chat jokes are about making
  the film, never at anyone's expense.
- No text is cut off or shrunk past the build warnings; every chat line fits
  in two lines.
- Real images only: the product's screens and outputs. No stock people, no
  other companies' screenshots. Third-party logos only when the product shows
  them, with the trademark fine print.
- One continuous piece of music with no stops; the accents land on the logo
  drop, the stamps and the end-card jump, and the music eases out after the
  final hit instead of being cut.
- Every chat send, reply, click and stamp has a real sound effect.

## Rights and limits

- The crew characters (three styles), the engine, the fonts (SIL Open Font License) and the
  Lucide icons (ISC) ship with the Skill. The product's logo, screenshots and
  copy belong to the product owner: make films for products the user owns or
  may promote. For any other product, keep the "Concept film" label, use
  public material only and do not publish the film as official material.
- The editor in the film is a concept workspace, not a real product feature;
  the concept label says so.
- Generated music follows its provider's terms for commercial use.
