# THE PARTNERS HERO IMAGE — the image-generation prompt

**What it has to say, in one look:** the partner makes ONE introduction; the business behind it gets
transformed by someone else; one gold coin comes back to the partner. *"You make the introduction.
I do everything after it."* — the page says the $1,000; the image never shows text.

**How the page uses it:** `partners.html`'s hero, at the card's full width between the lede and the
application (where the framework page carries its film). Wide and short, so it reads as one strip left
to right: partner → owner → the business wired up → the coin back. The card is pure white, so the
image's background must be pure white too.

**Attach both references** (from the "What it becomes" loop, so the characters match the films):
`docs/hero-refs/ref-ceo.png` (the owner) · `docs/hero-refs/ref-org.png` (the workers, the cyan
agents, the black lines).

---

## PROMPT

```
A clean 3D render in the exact style and with the exact characters of the reference images:
chunky low-poly toy figures with big heads and simple friendly faces, soft matte plastic, small
navy-blue desks, grey laptops. Isometric three-quarter view from above, orthographic camera.
One continuous scene read LEFT to RIGHT, like a sentence.

LEFT: THE PARTNER — a new toy figure in the same style: a woman with a dark ponytail, a violet
blazer over a white shirt, holding a small grey tablet under one arm. With her free hand she
gestures warmly to the right, introducing the person beside her.

Beside her, a step to the right: THE OWNER from the first reference (dark skin, short black hair,
round glasses, green shirt, a small glowing gold orb floating just above his head), mid-stride,
walking to the right, looking back at her with a smile.

CENTRE and RIGHT: the owner's business, being transformed — a small cluster of navy desks where
worker figures (blue caps, yellow shirts or grey suits) sit beside several AGENTS: the same toy
body but entirely smooth matte sky-cyan with no hair and no clothing detail. Thin solid black
lines, like ink on a technical drawing, wire the agents and workers together into one clean,
even web.

THE RETURN: exactly ONE thin black line leaves that web on the far right, runs back along the
bottom of the scene under everyone, and ends at the partner's feet. Travelling along it, near
her, is ONE chunky gold coin — a thick flat disc, plain raised rim, no symbol — rolling on its
edge toward her. No other line touches her.

Keep generous empty white space above everyone and along all four edges; nothing touches an
edge. The three groups are clearly separate, with white space between them.

Background: PURE WHITE (#FFFFFF), seamless, no floor line, no horizon, no room. Only soft light
grey contact shadows under the desks and figures. Bright even studio light. Calm, orderly,
premium, uncluttered.

Wide landscape, 21:9, at least 2520 x 1080.
```

## NEGATIVE

```
text, letters, numbers, dollar signs, currency symbols, logos, watermark, badges, speech
bubbles, floating cards or icons (the gold orb above the owner and the one coin are the only
extra objects), piles of coins, cash, money bags, handshake close-ups, UI panels, holograms,
floating screens, glow except the gold orb, neon, dark or grey background, a visible floor edge,
a room, walls, chrome or metal robots, sci-fi, particles, plexus, lens flare, depth-of-field
blur, photoreal humans, identical overlapping clones, figures cut off at any edge, extra limbs,
distorted faces
```
