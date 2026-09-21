# The page fork, and what the video on the site actually is — 2026-09-20

## THE FORK

Isaac: *"i feel like the site is becoming too complicated… make it only the video and
about section and the only option is to book a call… fork it and keep a simplified one
which is only the hormozi style landing page which just goes to discovery call. And
then we can also have this other one saved."*

| file | what it is | linked? |
|---|---|---|
| `ai-transformation.html` | **THE LIVE PAGE.** Claim · video · who you'd be talking to · book a call. One action. | yes |
| `ai-transformation-full.html` | **THE FULL FUNNEL, PRESERVED WHOLE.** All 13 deck slides, the driven diagrams, the cost anchor, the 8-line ledger, the price cascade, both checkout doors, the FAQ. | no — nothing points at it |

Moved with `git mv`, so the full page keeps its entire history. Both share
`style.css`, `capture.js` and `vsl.js` untouched; the simple page does not load
`reveal.js` (nothing to drive). **To put the full funnel back, swap the two
filenames — nothing else has to change.**

## THE VIDEO AUDIT — three findings, all measured

Isaac: *"This video is fucking awful. is this still the wrong video here? … I dont
think we ever finished writing the new script?"*

**1. THE SITE IS SERVING THE WRONG FILM.** `assets/vsl.mp4` is **560.17s** and
`video-aios/out/the-climb.mp4` is **560.167s** — the same film, re-encoded (98MB vs
286MB). The film named after the deck, `draw-the-box.mp4`, is **365.13s** and has
never been on the site.

**2. THE DECK-BASED SCRIPT WAS WRITTEN BUT NEVER RECORDED.** File times:

| artifact | when |
|---|---|
| `scripts/draw-the-box.md` (the deck rewrite) | **Sep 20 17:12** |
| `audio/draw-the-box/timing.json` + `transcript.txt` | Sep 19 15:39 |
| `out/draw-the-box.mp4` | Sep 19 15:51 |

The audio and the render PREDATE the script by a day. The recorded transcript opens
*"If you are here then you own a business that is actually making money…"* — the old
script. So the rendered `draw-the-box` is the OLD words, and the deck-based rewrite
has never been spoken aloud.

**3. ⇒ NEITHER EXISTING FILM IS THE VSL THE DECK DESCRIBES.** `the-climb` (on the
site) is a different film entirely; `draw-the-box` (rendered) carries a superseded
script. Getting the intended VSL costs a re-record of `scripts/draw-the-box.md` and a
re-render — it is not a matter of copying a different file into `assets/`.

⏸ **OPEN, AND ISAAC'S CALL:** which film ships on the simple page while that is true.
The page currently keeps `assets/vsl.mp4` (the-climb) because swapping in
`draw-the-box` would replace one wrong film with another.
