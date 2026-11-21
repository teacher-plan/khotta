# Music

The choreography is written in beats, so the film needs one instrumental
track with a steady pulse between 100 and 140 BPM (120 is ideal) and at least
45 seconds of the same groove. A slower track makes the film longer and
softer; a faster one makes it rushed. Every generation route is paid by its
provider: tell the user which route, which account or key, and wait for a yes
before submitting.

## Prompt

> Playful, bouncy product-launch track at a steady 120 BPM in 4/4. Punchy kick
> and claps on every beat, plucky marimba and synth bass, bright toy-like bell
> accents, cheerful and confident like a cartoon studio at work. Keep the same
> groove from start to finish with no slow intro and no breakdowns, add small
> fills every eight bars, and end on one big final hit with a short ring-out.
> Instrumental, no vocals.

Adjust instruments and mood to the brand (warmer and acoustic for consumer
products, tighter and more electronic for developer tools); keep the tempo,
the steady groove and the final hit.

## Route 1: ChatCut (default)

Use the ChatCut Desktop tools with the user's ChatCut account:

1. Keep the music out of the user's open editing project: `create_project`
   with a name like "<Product> launch music" (or `list_projects` and
   `target_project` to reuse one), and confirm with `get_active_project`.
2. `submit_music` with `generationType: "instrumental"`, the prompt and a
   `name`.
3. `track_progress` with `target: "generation"`, `action: "wait"` and the
   `jobId`; the result gives `outputAssetId`.
4. `pull_asset` with that id and `outputPath: "<project>/assets/music.mp3"`.

ChatCut picks the length itself, often two to three minutes. That is fine:
`soundtrack.mjs` chooses one continuous stretch. ChatCut tracks often contain
stop-time hits (the whole band stops for 0.2-1 s); the script refuses
stretches with a break and avoids even short stops. If every stretch is
rejected ("the track is too short"), generate another track: ask for drums
that "play continuously, with no stops, no drops and no breaks". Generating
two candidates at once and keeping the most continuous one works well.

## Route 2: ElevenLabs API key

```bash
export ELEVENLABS_API_KEY=...
node <skill>/scripts/music.mjs --provider elevenlabs --seconds 75 --out assets/music.mp3
```

## Route 3: FAL

```bash
export FAL_KEY=...
node <skill>/scripts/music.mjs --provider fal --seconds 75 --out assets/music.mp3
```

The request id is kept in `assets/music.mp3.fal.json`; running the same
command again polls the same job instead of paying twice.

## Route 4: the user's own track

Any MP3, WAV or M4A the user owns or has licensed.

## Fit and mix

```bash
node <skill>/scripts/soundtrack.mjs --music assets/music.mp3 --out-dir .
```

It detects the beats, scores every downbeat as a possible start and keeps the
stretch whose accents land hardest on the film's hits (the logo drop, the
wall, the stamps, the end-card jump) while avoiding quiet breaks. It writes:

- `beats.json` - the beat period, the offset of film beat 0 and the duration;
  `build.mjs --beats beats.json` uses it.
- `soundtrack.wav` - that stretch of the music, playing continuously from
  the first frame to the fade-out, with the synthesized interface foley (chat
  pops, crew hops, clicks, stamps, the chomp, a chime), normalised to
  -16 LUFS; `render.mjs --audio soundtrack.wav` uses it.

| option | default | meaning |
|---|---|---|
| `--start` | auto | seconds into the track where the film's pickup starts |
| `--bpm` | 120 | tempo hint for the beat tracker |
| `--music-gain` / `--foley-gain` | -2 / 0 | dB |
| `--bite-drop` | off | cut a short hole in the music where the crew bites the clip (usually sounds like a bad edit; leave it off) |
| `--lufs` | -16 | integrated loudness target |
| `--sfx-dir` | none | folder of real sound effects named after the cues below; each replaces its synthesized fallback |

Never splice two parts of a track or switch tracks mid-film. If the automatic
start sounds wrong, listen and pass `--start` by hand.

## Sound effects

Every interface moment has a named cue. Without `--sfx-dir` the Skill
synthesizes simple placeholders; for a finished film, collect real sounds
into `sfx/` (one short file per cue: `.wav`, `.mp3`, `.m4a`) and pass
`--sfx-dir sfx`. Files are trimmed of leading silence and peak-matched.

| Cue | Where it plays |
|---|---|
| `typing` | soft keyboard taps while the human types a chat message |
| `send` | the human's message is sent; the prompt is sent in the how scene |
| `receive` | a crew member's message appears |
| `hop` | the crew hop onto their cursors |
| `drop` | a clip lands on the timeline |
| `tick` | placeholders, keyframes and result checks |
| `click` | button clicks (Play, the scene button, the dialog confirm) |
| `chomp` | the bite on the music clip and on the Render button |
| `whoosh` | fast moves and the push-in |
| `slap` | the sticker lands; the animator lands in the slot |
| `boing` | the animator jumps in and out of the slot |
| `stamp` | the big check and the six proof stamps |
| `scribble` | the fact-checker strikes the sticker |
| `poof` | the sticker disappears |
| `pop` | the dialog pops open; the render finishes |
| `riser` | the render fills |
| `chime` | the render is done |

Sources, in order of preference: the ChatCut sound effects library or ChatCut
custom sound effects (the user's ChatCut account), ElevenLabs sound effects
with the user's key, or sounds the user owns.

With ChatCut, use the music project from Route 1. Library sounds become files
once added to that project's timeline: `edit_item` adds one
`{type:"audio", assetId:"library:sound:<id>", trackId, startFrame}` per call
(never a batch; a timed-out batch rolls back), spaced so they do not overlap
(the typing loop is about 68 s long). Then copy each file from the project's
`assets/audio/` folder, or `pull_asset` it, into `sfx/<cue>.mp3`. Library ids
that fit: `slow-dell-keyboard-typing` (typing), `sent-message-ping` (send),
`new-notification-ping` (receive), `tiny-bubble-pop` (hop),
`synthetic-bubble-pop` (drop), `gear-turn-click` (tick), `mouse-click`
(click), `airy-short-whoosh` (whoosh), `ui-pop-up-alert` (pop),
`fast-suspense-riser` (riser), `clean-ding` (chime). Generate the rest with
`submit_sound` (`chomp`, `slap`, `boing`, `stamp`, `scribble`, `poof`, about
0.6-0.8 s each), wait with `track_progress`, and `pull_asset` them. Check
every file's level: a generated sound that comes back nearly silent (peak
below -30 dBFS) should be generated again. Keep each under one second
except `riser` (about two) and `chime`.
