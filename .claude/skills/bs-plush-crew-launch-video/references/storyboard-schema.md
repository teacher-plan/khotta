# Storyboard schema (`film.json`)

One file per language. Paths are relative to the storyboard file. Every image is
copied into the built film; large screenshots are downsized to 2560 px wide (sharp at 4K).
`build.mjs` fills everything marked *default* and stops with an `ERROR` line
for anything required that is missing. A complete example is
`references/example-storyboard.json`.

```jsonc
{
  "lang": "en",                       // BCP 47 tag; non-English films need the labels under "Other languages"
  "style": "felt",                    // crew characters: "bots" | "faces" | "felt" (asked in the opening dialog)
  "product": {
    "name": "Acme",                   // the wordmark text, as the brand writes it
    "url": "acme.com",                // shown in the end-card pill; no https://
    "mark": "brand/mark.svg",         // square logo mark (SVG or PNG, transparent or full-bleed)
    "markBg": "#FFFFFF",              // tile color behind the mark (default white)
    "markPad": 0.18,                  // padding inside the tile, 0-0.3 (default 0.18)
    "markFill": false,                // true when the mark is a full-bleed app icon (padding 0)
    "wordmark": null                  // optional wide logo image; replaces the text wordmark
  },
  "palette": {
    "brand": "#22A848",               // required: the main brand color
    "accents": ["#F4FF71"],           // optional secondary brand colors (steer the crew colors)
    "highlight": null,                // optional highlighter; default: a vivid tint of brand
    "ink": "#121313", "bg": "#F4F1E9" // optional; keep the defaults unless the brand needs otherwise
  },
  "fonts": { "display": "Bricolage Grotesque", "ui": "Geist" },  // optional Google Fonts families
  "crew": [ { "id": "c4", "name": "Blip", "role": "Animator", "file": "felt/felt-03-star-sky.webp" } ],  // optional overrides; files from references/engine/crew/<style>/crew.json
  "human": { "name": "Lin", "role": "Acme team" },               // default: Lin / "<name> team"
  "workspace": {
    "projectTitle": "Acme in 40 seconds",                        // default shown
    "channel": "#explain-acme",                                  // default shown
    "conceptLabel": "Concept film",   // default; set null only for a film about the user's own product
    "sticker": "Literally magic!!!"   // the hype sticker the fact-checker strikes out
  },
  "chat": { "<slot>": { "text": "...", "icon": "lucide-name" } },  // see the slot table below
  "media": { "thumbs": [5 images], "gutter": [2 images] },          // optional; default picks from the scenes
  "scenes": {
    "brand": {
      "label": "Acme",                         // timeline clip name and preview tag
      "headline": ["Line one", "line two."],   // the product's own hero line, split in two
      "highlight": "two",                      // a word or phrase in one of the lines
      "sub": "One factual sentence.",
      "peeks": [4 images]                      // cards that peek up under the headline
    },
    "what": {
      "label": "What it is",
      "kind": "App",                           // the chip on the product card (APP, API, SKILL, TOOL...)
      "headline": ["Line over the card.", "Line on the plate."],
      "highlight": ["word in line 1", "word in line 2"],
      "sub": "One line under the plate.",
      "chips": [ { "icon": "file-text", "text": "1-3 words" } x3 ],
      "categories": ["Four", "short", "group", "names"],   // light up one per beat over the wall
      "wall": [ { "src": "image", "cat": 0-3, "video": false } x8+ ]  // or plain image paths (cat round-robin)
    },
    "fit": {
      "label": "Works with",
      "headline": ["Half one", "half two."],   // read as one line
      "items": [ { "name": "Label", "logo": "image" | null, "icon": "lucide-name" } x3 ],
      "chip": "Works",                         // check chip under each tile (per item: "chip")
      "more": "+ more integrations",           // the dashed fourth tile
      "finePrint": ""                          // trademark notice whenever a logo belongs to someone else
    },
    "how": {
      "label": "How it works",
      "steps": ["Write.", "Pick.", "Done."],   // three slammed words, about 1-2 words each
      "button": "Start a project",             // the pill clicked at the start
      "buttonDone": "Started",  "buttonIcon": "mouse-pointer-click",
      "cardTitle": "Acme",                     // the window title
      "input": "What a real user would type…", // pasted, sent, shown as a bubble
      "inputHighlight": "a phrase from input",
      "dialog": { "title": "Confirm step", "label": "Field", "value": "Value", "approve": "Go", "deny": "Cancel" },
      "results": [3 images],                   // what the product gives back
      "resultPrefix": "",                      // e.g. "$" for a CLI line
      "resultLine": "Exported {x}",            // {x} becomes each value in turn
      "resultValues": ["three", "short", "values"],
      "sub": "One line about the flow."
    },
    "proof": {
      "label": "Why trust it",
      "headline": ["Short.", "Second line."],  // narrow column: about 12 Latin or 6 CJK characters per line
      "sub": "One or two short lines.",
      "stamp": "Real",                         // the stamp pressed on each card (1-2 words)
      "stampIcon": "badge-check",
      "cards": [6 images]
    }
  },
  "end": { "headline": ["Line one", "line two."], "highlight": "two", "sub": "One line.", "url": "acme.com" },
  "sources": [ { "fact": "what the film claims", "url": "where it says so" } ]
}
```

## Chat slots

The chat runs on fixed beats beside the film. Write the starred slots; the
others have defaults (in the film's language) that you may override.

| Slot | Beat | Sender | What it is for |
|---|---|---|---|
| `open` | 0.5 | human | Default "Who can explain {name} in 40 seconds?" |
| `hero_joke`* | 6.5 | audio crew (c5) | A playful pun on the hero line, just before it plays |
| `bite` | 13.5 | c5 | Default "Oops. I bit the beat." (a bite shows on the music clip; the music keeps playing) |
| `wall_q`* | 20.5 | human | Asks whether the wall of outputs is real |
| `wall_a`* | 22.5 | layout crew (c3) | Answers with a fact (where they come from) |
| `slot_q` | 33.5 | animator (c4) | Default "Is there room for me in that slot?" as it jumps into the empty tile |
| `how_q`* | 38.5 | c3 | A real beginner question about the flow |
| `how_a`* | 40.5 | fact-check (c2) | The factual answer, from the product's docs |
| `sticker` | 45 | human | Default "Adding one tiny sticker." |
| `source` | 47 | c2 | Default "Source?" (strikes the sticker) |
| `fair` | 49 | human | Default "Fair." |
| `proof_joke`* | 51.5 | c5 | Wonders out loud about the proof claim |
| `tagline` | 53.5 | c2 | Default "It's literally the tagline." (taps the title clip) |
| `taste` | 61.5 | c5 | Default "Tasted the render. Delicious." |
| `close` | 63.5 | human | Default "Okay. Now I can explain it." |

Keep each line under about 42 Latin or 20 CJK characters. `icon` is any
Lucide icon name (`references/engine/lucide-nodes.json`); never emoji.

## Length guide

The engine shrinks text that does not fit and prints a `console.warn` in QA.
Aim for: headline lines 24 Latin / 12 CJK characters, chips 22 / 10,
categories 16 / 8, steps 12 / 6, proof headline 12 / 6 per line.

## Other languages

English labels are built in. For any other `lang`, write these in the film's
language too (`build.mjs` lists whatever is missing):

```jsonc
"ui": {
  "share": "", "render": "", "play": "", "preview": "", "timeline": "",
  "online": "5 ... online", "composer": "Write a reply...", "dropZone": "Drop a shot here",
  "tracks": ["Shots", "Titles", "Motion", "Music", "SFX"],
  "clips": { "logo_rise": "Logo rise", "logo_strip": "Logo strip", "music": "Score · {bpm} BPM", "sfx": "UI ticks" }
},
"workspace": { "projectTitle": "", "channel": "", "conceptLabel": "", "sticker": "" },
"human": { "name": "Lin", "role": "<product> team" },
"crew": [ { "id": "c1", "name": "", "role": "Director" }, { "id": "c2", "name": "", "role": "Fact-check" },
          { "id": "c3", "name": "", "role": "Layout" }, { "id": "c4", "name": "", "role": "Animator" },
          { "id": "c5", "name": "", "role": "Audio" } ],
"chat": { "open", "bite", "slot_q", "sticker", "source", "fair", "tagline", "taste", "close" },  // plus the starred slots
"scenes": { "what": { "kind" }, "fit": { "chip" }, "how": { "buttonDone" } }
```

Translate the English defaults in the chat table above; give the crew short,
cute names that work in that language. Chinese films use Smiley Sans for
headlines (Latin words inside them keep the display face) and Noto Sans SC
for the interface. Other scripts render with the bundled faces where they
have the glyphs and fall back to system fonts otherwise: check the QA frames.
