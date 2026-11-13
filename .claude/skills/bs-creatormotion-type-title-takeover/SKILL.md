---
name: bs-creatormotion-type-title-takeover
description: An oversized condensed headline punches in behind a presenter. A clean edit removes the presenter while the same lettering holds its scale and position.
---

# Title Scene Takeover

Use this Skill for a short statement that starts behind a foreground presenter and then takes over the whole frame. This is a 5.4-second HyperFrames composition, built as two edited shots with one persistent title layer. Read `references/motion-spec.md` and `references/DESIGN.md` before adapting it. The reference-specific display typography and timing in the motion specification take precedence over generic small-title defaults.

## Create an editable project

1. Put replacement content in a JSON object using the input names below.
2. Choose `white-yellow` by default, or `charcoal-lime` or `midnight-ice` (Black & White). Dark styles retain fine static grid lines.
3. Run `node scripts/create.mjs --out /absolute/output/path --data /absolute/content.json --style midnight-ice --media /absolute/presenter.mp4 --images /absolute/images.json --aspect 16:9 --resolution 4k`.
4. Render through HyperFrames using the command printed by the generator. Inspect the punch, exact cut and final reading hold.

Supply a continuous presenter/background take at least 1.8 seconds long with `--media`; its aligned cutout follows the Presenter cutout rules below. The generator copies media into the editable project. Never loop shorter footage; keep video muted and provide narration separately if required.

## Aspect ratio, resolution and caption safe area

Settle these with the user before the first build and keep them for the whole series.

- **Aspect ratio**: `--aspect 16:9`, `9:16`, `4:3` or `3:4`. Each has its own native layout. With footage, read its size with ffprobe and use its ratio when it is one of the four; otherwise propose the nearest one (the footage is centre-cropped) and ask the user to confirm. Without footage, ask the user to choose.
- **Resolution**: always ask, recommending 4K. `--resolution 4k` (default, short side 2160), `2k` (1440) or `1080p` (1080): a 4K 9:16 segment is 2160×3840, a 4K 4:3 segment 2880×2160.
- **Caption safe area**: the bottom of the frame is kept free for the creator's subtitles (and the platform's captions and buttons on Shorts, Reels and TikTok). The effect places its text and graphics above it; do not move them into that band.

For footage, pass `--focus x,y`: the centre of the presenter's face as fractions of the footage frame (for example `0.52,0.38`). Extract one frame (`ffmpeg -ss 2 -i <take> -frames:v 1 /tmp/frame.png`), look at it and estimate the face centre. The effect uses it to centre the head in the region the presenter occupies. Use landscape footage for 16:9 and 4:3 and portrait footage for 9:16 and 3:4.

## Inputs

```json
{
  "title": "BUILD WITH US",
  "supportingLine": "One small project every week"
}
```

Prefer 2–4 short English words or 4–8 Chinese characters. The headline is capped at 32 characters. Keep the support concise enough for one line. Change input values rather than animation selectors. If reframing different media, adjust the base and alpha matte together.

## Motion invariants

- A tall, condensed Google-font headline occupies most of the frame width.
- A fast punch and small settle establish the title behind the presenter; there is no slow generic fade-in.
- At 1.8 seconds the presenter shot cuts away. The same headline element remains exactly in place and at the same size.
- A plain subordinate supporting line appears after the cut. It must not become a rounded UI button.
- The final statement has a stable reading hold. Do not add decorative motion to fill the hold.

All type, compositing and motion render inside HyperFrames. No AE, Fusion or external compositing stage is required. A different palette must not turn this movement into a generic card entrance.

## Validation

Run HyperFrames lint, validate and inspect in the generated project. Review exact frames immediately before, on and after the 1.8-second cut. Verify the alpha matte aligns, replacement text remains readable, fonts are local, and the final frame is not empty. Inspect an actual rendered video; technical checks do not replace the user's visual acceptance. See the motion specification for the current SVG text-bounds inspection limitation.

## Presenter cutout

This effect uses a transparent presenter cutout (`presenter-matte`) that shares the frames, duration and framing of the `--media` take. The cutout is required for the first shot, where the headline sits behind the presenter.

1. If the user already has a cutout of the same take, generate directly: pass it with `--matte /absolute/presenter-matte.webm` (or the `presenter-matte` key in `--images`). Footage that already carries an alpha channel (VP9 alpha WebM or ProRes 4444) is detected and used as its own cutout.
2. Otherwise keep the default `--matte auto`. Before building, the generator cuts the presenter out of the `--media` take with HyperFrames: `npx --yes hyperframes@0.8.30 remove-background /absolute/presenter.mp4 -o /absolute/presenter-matte.webm --quality best`. It runs a local human-segmentation model (CoreML on Apple silicon, otherwise CPU or CUDA), downloads the model weights once on first use, and needs roughly 0.1–0.6 seconds per frame depending on resolution. The cutout keeps the source resolution and is cached by source checksum, so other palettes of the same take reuse it. Run the command yourself first when you want to review the cutout, then pass the result with `--matte`.
3. `--matte off` disables automatic cutting.

`build.json` and `image-assets.json` record whether the cutout came from the user, from alpha footage or from `remove-background`, with checksums. Inspect hair, hands and fast motion in the rendered frames; if the automatic edge is not clean enough, supply a better cutout. Output is 4K by default; supply 4K footage so a 4K result stays sharp.

## Typography

Smiley Sans (Deyi Hei) sets titles, copy and labels in every language, Latin and Chinese alike. It is one slanted display weight, so hierarchy comes from size, colour and spacing rather than weight. IBM Plex Mono sets axis ticks, ordinals, counters and small labels so numbers keep a stable width. Noto Sans SC stays behind Smiley Sans for rare Chinese characters; pass `--zh-font noto-sans-sc` to set Chinese content in Noto Sans SC instead. A supplied `--font` always wins. `build.json` records the choice under `typography`.

## Image material contract

Follow [the image policy](references/image-policy.md) before adapting visual content. Photos, covers, document imagery and chat avatars use actual raster assets. Without user references, reuse the generated defaults in [the slot map](references/default-image-slots.md); do not ask for every image. User-specified images replace the corresponding slots first. Keep typography, vector diagrams, masks and movement editable in HyperFrames. New image subjects require the available image-generation tool (image2 when exposed), with actual provider/model provenance; no silent HTML substitute. Presenter video remains a separate input; its aligned cutout is supplied or generated as described in Presenter cutout.
