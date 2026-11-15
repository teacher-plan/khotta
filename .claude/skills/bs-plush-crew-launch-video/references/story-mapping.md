# Mapping a product onto the film

The film is about 41 seconds at 120 BPM (76 beats, then the end card holds while the music eases out). A
human asks in the team chat who can explain the product in 40 seconds; five
crew characters (in the style the user picked) hop onto their cursors and build the film live in a
collaborative editor. The preview panel plays the film-in-film; the timeline,
chat and cursors react on the beat. At the end the camera pushes into the
preview and the end card fills the frame.

The beat grid is fixed. Only words, colors and images change, so every
product gets the same polished choreography.

| Beats | Seconds at 120 BPM | What happens | Storyboard |
|---|---|---|---|
| -2 to 8 | 0-5 | Chat opens, the crew hop onto cursors, drop clips onto the timeline | `chat.open`, `chat.hero_joke` |
| 8-16 | 5-9 | **brand**: tile drops, mark draws, wordmark wipes in, two-line hero, peeks | `scenes.brand` |
| 12.75 | 7.4 | The audio crew bites the music clip on screen (a chomp sound; the music keeps playing) | `chat.bite` |
| 16-28 | 9-15 | **what**: product card with 3 chips bursts into a wall of real outputs, 4 categories light up, plate | `scenes.what`, `chat.wall_q/a` |
| 28-36 | 15-19 | **fit**: three tiles with check chips, a dashed 4th tile the animator jumps into | `scenes.fit`, `chat.slot_q` |
| 36-48 | 19-25 | **how**: button click, paste, send, dialog confirm, results with checks, three slammed words | `scenes.how`, `chat.how_q/a` |
| 44-49 | 23-25 | The human drags a hype sticker in; the fact-checker strikes it out | `workspace.sticker` |
| 48-56 | 25-29 | **proof**: six cards get stamped, then stack into the product tile | `scenes.proof`, `chat.proof_joke` |
| 56-66 | 29-34 | Render button bitten and filled, timeline replays, crew cheer | `chat.taste`, `chat.close` |
| 66-80 | 34-41 | Push-in, end card: mark, wordmark, headline, URL pill, crew jump on the final hit; the music eases out | `end` |

## What each scene should say

Work only from what the product says about itself (site, docs, pricing,
changelog). Never invent numbers, prices, customers, reviews or features.

- **brand**: the product's own hero line, split into two lines; highlight the
  one word that carries the promise. `sub` is the plain one-sentence
  description. `peeks` are four of the most recognisable screens or outputs.
- **what**: what the product *is* and what comes out of it. Line 1 sits over
  the product card (the input or the kind of thing); line 2 lands on the plate
  after the wall (the outcome). Three chips name the three core ingredients or
  capabilities. The wall is real outputs or real screens grouped into four
  categories (output types, use cases or tools).
- **fit**: where it works or who it is for: integrations, platforms, formats or
  audiences. Real logos only when the product itself shows them, with
  `finePrint`; otherwise Lucide icons and plain labels.
- **how**: the shortest true path from start to result: the first click, what
  the user types, one confirm step that really exists (connect, choose a
  setting, approve), and what comes back. `resultLine` and `resultValues`
  should be real commands, settings, file types or destinations.
- **proof**: one reason to trust it that the product states itself (reviewed,
  open source, consistent characters, privacy, uptime it publishes...). The six
  cards show that proof.
- **end**: a call to action in the product's voice, the real URL, and one
  factual line about what the product does.

## Pricing words need the pricing page

Never write "free", "unlimited", "included", "no card" or any price unless
the pricing page states exactly that, for exactly that scope. A "Try for
free" button, a free trial, a free tier of some items or "free templates" in
a feature list are not a free product: name only the scope the pricing page
confirms ("3-day free trial", "free Skills"), and when in doubt show the
feature instead. Open the pricing page during research and quote it in
`sources` for every pricing claim.

Keep the scope words of the source in the line itself: "3-day free trial on
every plan", "direct connections remain free", "free for personal use". A
shortened line that drops them ("free trial", "free") reads as a different,
broader claim. Translate the scope too. During QA, write a short
`factcheck.md` next to the storyboard: every on-screen claim, its source and
its status, so the user can check it at a glance.

## Crew jokes

The crew are cute, not snarky. Jokes are about the film being made (biting the
beat, a sticker that gets fact-checked, tasting the render), never at the
product's or anyone else's expense. `hero_joke` and `proof_joke` may play on a
word from the headline; `wall_a`, `how_a` are always facts.

## Choosing images

- 16:10 to 16:9 crops work best; portrait images are cropped from the top.
- Prefer the product's own outputs and UI over marketing illustrations.
- Never use stock photos of people, other companies' screenshots, or anything
  the product does not own.
- Reuse is fine (the wall repeats images), but `peeks`, `results` and `cards`
  read best with distinct images.
