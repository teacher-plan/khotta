# Researching the product

## 1. Capture the site

```bash
cd <project>
node <skill>/scripts/capture.mjs --url https://acme.com --out capture --pages /features,/pricing --max-shots 10
# Chinese film: ask the site for its Chinese copy
node <skill>/scripts/capture.mjs --url https://acme.com --out capture-zh --locale zh-CN --no-mobile
```

`capture/site.json` holds the title, meta description, headings with their
paragraphs, calls to action with their colors, nav links, logo candidates,
fonts and every large image. `capture/shots/` has section screenshots,
`capture/media/` the downloaded images and logos. Overlays are hidden, never
accepted; nothing is clicked.

Read `site.json` and look at every screenshot. Then open the pages that hold
the facts the film needs (features, docs, pricing, changelog, FAQ) in the
browser or with `--pages`. Write the facts you will use, each with its
source URL, into `sources` in the storyboard.

## 2. Pick the brand assets

**Mark** (`product.mark`), in this order:

1. An SVG or transparent PNG logo mark from `logoCandidates` (header logo,
   `logo.svg`, `[class*=logo]`). Open it to check it is the mark, not a
   decorative icon.
2. `apple-touch-icon` (180 px) or a large favicon PNG. These are usually
   full-bleed squares: set `markFill: true` and `markBg` to their background.
3. A wide logo with no separate mark: crop the symbol into its own file, and
   pass the full logo as `product.wordmark`.

Never redraw or recolor a logo. When only a raster mark below 128 px exists,
ask the user for a better file.

**Brand color** (`palette.brand`): the color of the main call-to-action
button (`ctas[].bg`) or the logo's dominant color; `themeColor` is a hint
only. Add a second brand color to `accents` when the brand clearly has one.
The crew are picked from the chosen style so their colors follow these.

**Fonts** (`fonts.display`): when `site.json` shows a Google Fonts family for
headings (for example "Bricolage Grotesque", "Inter", "Instrument Serif"),
name it and `build.mjs` fetches a subset. System stacks and paid fonts fall
back to the bundled Bricolage.

## 3. Collect the images

Use `capture/media/` (the site's own product images and outputs) and
`capture/shots/` (section screenshots). Crop or pick so each image shows one
thing clearly. For `how.results`, the best images are real outputs of the
product. If the site has too few images, take more screenshots of the
product's public pages or ask the user for product screenshots.

## 4. A product the user does not own

Keep `workspace.conceptLabel` on, use only public material, and tell the user
the film is a concept piece that should not be published as official
material without the owner's permission.
