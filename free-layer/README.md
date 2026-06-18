# free-layer — the honest funnel that converts by giving away the most valuable thing

This directory is a **content-restructure derivation** of the AIsaac blog. It does not replace
or edit any existing site file. It is an additive layer that re-cuts the existing material at a
specific altitude, so the free content delivers genuine value AND creates the exact gap that
makes someone want to ascend.

Everything here was derived from the actual blog posts in `/home/GOD/aisaac/blog/*.html` and the
top-level pages. Every piece cites the source blog(s) it was distilled from. Nothing is invented.

---

## The strategy (read this before editing anything here)

The whole funnel rests on one move: **publish one rung ABOVE where the reader is.**

The blogs describe a 7-level ladder of agent engineering (L1 prompts → L7 emergence) and ~27
named frameworks (SOSEEH, Towering, HALO, HIEL, Admissibility, etc.). Most readers live around
L1–L3 and think they're higher. The free layer does three things with that material:

1. **Derive the deepest invariants** — the maximally generalized class-shapes that *everything*
   in the blogs is an instance of. (Canonical altitude example, straight from the source:
   "an agent is really a context, an identity, and capabilities.") These deepest generalizations
   are the **most valuable** thing on the whole site, and they are FREE. See `INVARIANTS.md`.

2. **Build directional / high-level frameworks** from those invariants (`frameworks/`). Each one
   hands the reader the *class-level SHAPE of how to think* about a problem — real, usable value —
   but stops before the operational instantiation. You learn the shape of the destination. You do
   not get the language to build the path to it.

3. **Recast the advanced material as +1-generalized case studies** (`case-studies/`). Each takes
   an advanced pattern from the blog (e.g. the SANCTOT compiler, the admissibility validator, the
   progressive-disclosure harness) and tells it as an anecdote/pattern that has been **generalized
   one extra time before sharing**. This *leaks that the deeper rung exists* and shows its shape,
   while withholding the operational/instantiation language.

### Why this converts (the mechanism — keep it intact)

After reading the free layer, the reader ends up **holding the class-level shape** of how a real
compound-AI system thinks — but still **lacks the language to forward-chain and fill the args to
instantiate it** (to get from step 1 to step 3 themselves). They can now *see the destination but
cannot build the path to it.* That gap is real, not manufactured: the free invariant genuinely is
the most valuable generalization, and the missing piece — the operational deduction-language — is
genuinely the thing Isaac has and they don't. Seeing the gap → realizing he has the language →
trust → ascend/convert. It is honest because the free thing is the best generalization; it converts
because the gap it reveals (you can SEE it but can't BUILD it) is true.

This is the same mechanism the site's own rule states (`funnel-depth-is-initiation-depth.md`):
the deepest content doesn't sell, it *describes where the reader already is* — because the free
layer already moved them there.

---

## THE EDITORIAL RULE (apply to every single piece, every time)

> **Publish at the class/generalized level, one rung above the reader. NEVER write the
> instantiation rung** (the actual operational steps, the args to fill, the deduction-language
> that turns the shape into a running system).

The structural safeguard is **"+1 generalize before sharing."** Before any piece ships, it must be
generalized one extra step beyond the blog it came from — so that the free content **cannot be
assembled into the paid/operational thing.** If a reader could follow your piece and *build the
operational system*, you wrote the instantiation rung. Generalize it up one more level and remove
the build-able steps.

### The altitude test (run on every file before it ships)
1. Does this state the **class-shape / invariant** the reader was missing? (If it's just tips, raise it.)
2. Could a reader **forward-chain from this into a working operational system**? (If yes, you wrote
   the instantiation rung — generalize +1 and strip the steps.)
3. Does it **reveal that a deeper operational rung exists** and show its shape without handing over
   the language to instantiate it? (If it hides the rung, it won't convert; if it hands over the
   language, it cannibalizes the offer.)
4. Is every claim **grounded in what a real blog post actually says** (cited)? (If invented, cut it.)

### Honesty guardrails (from the site's own rules)
- **Never fake a case study.** Every case study here is a +1-generalized retelling of a pattern the
  blogs say Isaac actually built and uses. The system is the proof; point at it, don't fabricate.
  (`anti-case-study.md`)
- **No dollar amounts / no operational secrets.** The free layer reveals shapes, not prices and not
  build-instructions.
- **Don't paraphrase away the meaning.** Where the blog states an invariant crisply, preserve it.

### How a piece CLOSES — the ascension boundary (apply to every piece's closing section)

The closing section still names the operational rung it withholds (the +1-generalize discipline does
not relax — the withheld list stays). What changes is the **frame**: it must NOT read as a cold gate
("the rung above is hard, pay me"). It closes as a **caring, graduated invitation** — the withhold IS
care. Walk the reader through the sequence: **get it → experience the effects → benefit → ascend.**
First make sure they *get* the shape; once they get it they start *experiencing the effects* of using
it; once they're good at it and *benefiting*, they can check out the next step — the actual ascension.
The ascension then has **two exits**: **buy in now** (for the reader who's ready), or **apply / meet
requirements** (an application, or a prerequisite "do this other cohort first"). This is
`funnel-depth-is-initiation-depth` made *kind*: you're not blocking them from the operational rung,
you're making sure they have the priors + the lived benefit to actually use it before they climb.

### The meta-honesty register rule (the keystone — non-negotiable on every close)

You can literally TELL the reader this is what's happening — but in the **self-transformation /
ascension register, NEVER the marketing register.** Same truth, two registers: said as "here's our
funnel, buy the next tier" it's manipulative; said as "the layers build — just keep thinking like
this, keep applying these simple categories, and your ascension unfolds" it's care + growth, and it's
*funny* precisely because it's openly true. Name the mechanism out loud; code it as ascension, not as
a sale. The transparency DEEPENS trust instead of breaking the spell, because the structure is **real
self-transformation, not a sales mechanic** — which is exactly the `anti-case-study` positioning (the
system is the proof). Keep it tight: a short closing section, not an essay.

---

## Directory contents

```
free-layer/
  README.md          ← you are here: the dir, the strategy, the editorial rule
  INVARIANTS.md      ← the deepest derived invariants (the free layer's source of value)
  ASCEND-MAP.md      ← per-piece: the GAP it leaves open + what ascending gives (the conversion map)
  frameworks/        ← directional/high-level free frameworks (class-shapes, no instantiation)
  case-studies/      ← +1-generalized advanced patterns (leak the deeper rung, withhold the language)
```

## How to maintain the altitude discipline

- A new blog post drops → derive its **invariant** (does it instance one already in `INVARIANTS.md`,
  or is it a new class-shape?), then decide: is it a **directional framework** (a way to *think*) or
  an **advanced pattern** (a thing Isaac *built*)? Directional → `frameworks/`. Advanced → +1-generalize
  → `case-studies/`. Always add its row to `ASCEND-MAP.md` naming the gap it leaves.
- Never let a `case-studies/` file drift down into a build tutorial. The moment it contains the args,
  the literal tool calls, the ontology schema, or the step sequence that *instantiates* the thing —
  it has fallen to the instantiation rung. Generalize it back up.
- The free layer's value must always be the **generalization**, never the **recipe**. If you find
  yourself writing the recipe, you're writing the paid layer. Stop and raise the altitude.
