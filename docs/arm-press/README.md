# arm-press — the robot arm behind the hero's Book a call (the source of `assets/arm-press-*.webp` + `arm.js`)

- `arm-press.blend` — Kenney factory-kit `robot-arm-a` (CC0) behind a 2.2 × 0.7-unit button plane at y −0.1: white
  links · ink joints · cyan claws (the loop palette's cyan) · an inverted-shell ink outline · Workbench render,
  transparent film, ortho camera pitched 22° down. Base at x 0.3, y 0.45, its bend plane turned −35° about Z.
- ONE clip, 24 frames at 24 fps: hidden (base z −2.9) → rising from behind (6) → over the top edge (10) → the press
  (13 = frame index 12, the claw on the button's upper face) → hold (15) → lift (18) → out of sight (24).
- Rendered twice per frame where the claw is in front of the button: the whole arm (`back`) and the forearm, head
  and claws alone (`front`, frames 8–18). `pack.py` crops both to one cell ending at the button's bottom edge and
  records the button's box in the cell; that data is inlined at the top of `arm.js`.
- Re-render: open the .blend, render frames 1–24 to `frames/strike_NNN.png` (+ `front_strike_NNN.png` for 8–18),
  run `pack.py`, copy the two webps to `assets/` under NEW names, paste the new JSON into `arm.js`, bump its `?v=`.

- `arm-press.blend` holds the SHIPPED clip (frames 1–24, keyed as above); its frames 6, 13 and 18 re-render pixel-identical to `assets/arm-press-back.webp`.
- `first-try/` — the superseded first attempt, kept as a record: the arm standing BESIDE the button with idle/hover/press/release clips (`arm-button.blend`, `rigbutton.js`, its sheet and data, `pack.py`). Isaac ruled it wrong: nothing should show until the click.
