# agent-lasso — the agent who lassos the form in (the sample for the JobWorld app's agents popping out)

The recurring character is the AGENTS — the films' AI (`video-aios/framework-videos/DESIGN.md` §3b, Kenney's
platformer `character-oobi`, CC0, `License.txt` here), never the gnome. Open `agent.html` from a local server (its
data is inside the page) and click Book a call: a door opens in the button's right end, the agent walks out, hops
down, spins a lasso, throws it off the top of the screen, hauls the REAL form in on the rope a tug at a time, lets go
as it lands centred (first field focused), nods, hops back in, and the door closes. ~3 s.

- `build.py` — opens `../gnome-lasso/gnome.blend` (the scene: door, camera, the 74-frame timeline sampled from the
  Kenney clips), imports `character-oobi.glb` (same bones as the gnome but no head) in the gnome's place, carries his
  timeline and visibility onto it, scales it to fit the door, records its `arm-right` hand per frame and renders
  frames 1–74 to `frames/a_NNN.png` + `frames/render.json`; saves `agent.blend`.
  Run: `Blender -b ../gnome-lasso/gnome.blend -P build.py`, then `python3 pack.py`.
- `pack.py` → `agent-sheet.webp` + `agent.json` (cell, the button's box in it, the hand every frame, the beats:
  spin 20–29 · throw 30–32 · haul 33–46 · release 47).
- `lasso.js` — the sprite over the button, the rope drawn live in SVG from the hand to the form's corner, the real
  form moved along it. Reduced motion: the form opens at once.

## The pop — the agent arrives where something new appears (the app's spawns)

- `build_pop.py` — the same scene (`agent.blend`): the lasso's frames 1–19 (the door opens, the agent comes out and hops
  down), three hops on its own `jump` clip lifted on an arc with the door held open (the clips' root and torso keys
  dropped, so it keeps facing the camera; at the app's size the limbs move a few pixels and the whole body carries the
  beat), then the lasso's frames 48–74 (the nod, home, the door closes). Writes `frames/p_NNN.png`.
- `pack_pop.py` → `agent-pop.webp` + `agent-pop.json` (cell, the same button box, the beats: out · work · home).
Run: `Blender -b agent.blend -P build_pop.py`, then `python3 pack_pop.py`.
