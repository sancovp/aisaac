# THE HERO IMAGE — the image-generation prompt

**What it has to say:** the headline, *"Turn your business into software that runs without you."*
The owner sits back while the company runs itself, wired together, and exactly ONE line reaches
him: the one call that needs a human.

**How the page uses it:** the right half of the hero card. The page shows the LEFT part of the
image in full and lets the right part run off the card's edge. So the owner goes in the left
third, and the rows of desks keep going past the right edge. The card is pure white, so the
image's background must be pure white too, or it shows as a grey box.

**Attach both references** (from the "What it becomes" loop, so the characters match the film):
`docs/hero-refs/ref-ceo.png` (the owner) · `docs/hero-refs/ref-org.png` (the workers, the cyan
agents, the black lines).

---

## PROMPT

```
A clean 3D render in the exact style and with the exact characters of the reference images:
chunky low-poly toy figures with big heads and simple friendly faces, soft matte plastic, small
navy-blue desks, grey laptops. Isometric three-quarter view from above, orthographic camera.

In the LEFT THIRD of the frame, closest to the camera and larger than everyone else: THE OWNER
from the first reference (dark skin, short black hair, round glasses, green shirt, a small
glowing gold orb floating just above his head), leaning back in his chair at his own tidy desk
with his hands behind his head, relaxed and smiling. His desk is empty except for one laptop.

Behind him and spreading out to the RIGHT: his whole company at work on its own. Rows of worker
figures in blue caps with yellow shirts or grey suits, typing at laptops, and among them several
AGENTS: the same toy body but entirely smooth matte sky-cyan with no hair and no clothing detail,
also working at desks. Thin solid black lines, like ink on a technical drawing, connect the
agents to the workers around them and to each other in one clean even web across the floor.
Exactly ONE thin black line leaves that web and runs to the owner's desk, ending in a tiny white
square with a black outline. No other line touches him.

The rows of desks continue past the RIGHT edge of the frame, as if the company keeps going.
Keep generous empty white space above the owner and along the top and left edges; nothing
touches the top, left or bottom edge.

Background: PURE WHITE (#FFFFFF), seamless, no floor line, no horizon, no room. Only soft light
grey contact shadows under the desks and figures. Bright even studio light. Calm, orderly,
premium, uncluttered.

Wide landscape, 16:9, at least 2400 x 1350.
```

## NEGATIVE

```
floating coloured squares, badges, cards or icons over heads (the gold orb is the only thing
above anyone), text, letters, numbers, logos, watermark, UI panels, holograms, floating screens,
glow except the gold orb, neon, dark or grey background, a visible floor edge, a room, walls,
chrome or metal robots, sci-fi, particles, plexus, lens flare, depth-of-field blur, photoreal
humans, identical overlapping clones, figures cut off at the left edge, extra limbs, distorted
faces
```

---

**When it comes back:** save it into this repo, and it replaces `assets/hero-business.webp`. The
agent flattens it on white, checks the corners read #FFFFFF, crops to the content, and places it
so the owner is fully in view on desktop and on a phone.
