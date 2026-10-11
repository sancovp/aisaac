# gnome-lasso — the gnome who lassos the booking form (a sample, kept for the JobWorld app; not on the site)

Open `gnome.html` (from disk is fine — its data is inside the page) and click Book a call: a door opens in the
button's right end, a bearded gnome walks out, hops down, spins a lasso, throws it off the top of the screen,
hauls the REAL form in on the rope a tug at a time, lets go as it lands centred (first field focused), nods,
hops back in, and the door closes. ~3 s.

- `gnome.blend` — Kenney mini-character `character-male-b` (CC0, texture packed inside) ×0.82 with a red cone hat on
  its head bone; the door (frame · dark hole · white panel on a hinge) set into the right end of a 2.2 × 0.7-unit
  button plane; ortho camera pitched 22°; Workbench TEXTURE colour + inverted-shell outline. One timeline, frames
  1–74, sampled from his own clips (walk · jump · attack-melee-right 3/6 · holding-both · emote-yes · idle); an
  empty `hand` on the arm-right bone marks the rope's start.
- `pack.py` → `gnome-sheet.webp` + `gnome.json` (cell, the button's box in it, his hand position every frame, the
  beats: spin 20–29 · throw 30–32 · haul 33–46 · release 47). Re-render frames 1–74 to `frames/g_NNN.png` and record
  `hand` per frame with the camera projection into `frames/render.json`, then run `pack.py`.
- `lasso.js` — the sprite over the button, the rope + loop drawn in a full-screen SVG from his hand to the form's
  corner, the real form moved along it. Reduced motion: the form opens at once.
