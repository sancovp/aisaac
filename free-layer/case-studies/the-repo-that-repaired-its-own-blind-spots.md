# Case study: the codebase that got safer to edit every time it was touched

**Source pattern (advanced):** DocMagic — a scanner that detects invisible coupling in a repo and
writes local "admissibility markers" so each pass makes the codebase more self-readable; a concrete
compounding (vs rotting) loop.
**Derived from:** `docmagic-stack.html`, `admissibility-engineering.html`, `seven-disciplines.html`
(emergence), `composition.html`, `l7-emergence.html`.
**+1 generalization applied:** told as the *class* of "self-readability repair loops" and the
compounds-vs-rots fork, not the seven scan categories, the marker syntax, or the install commands.

---

## The anecdote

Here's why AI-written codebases rot. A repo isn't a pile of files — it's overlapping invisible
surfaces: a function quietly called by something three files away, a write that a background process
is watching, a comment claiming behavior the code no longer performs, an import reaching across a
boundary into a subsystem with its own release cycle. A human developer often *feels* these
relationships. An AI agent usually doesn't: it reads a few visible files, infers a local story, and
edits as if the hidden causal system didn't exist. So it breaks something it couldn't see. Then the
next agent trusts the now-stale surface and breaks more. The repo decays while everyone's busy.

The intervention was simple in concept: before editing, *surface the invisible.* A pass over the repo
finds the hidden couplings and leaves a small, local, readable breadcrumb right where each one lives —
"this function participates in a hidden chain; include these edges in your edit boundary or you'll
break something you can't see." The breadcrumb isn't documentation. It's a marker that tells the next
actor what must be known before this can be safely changed.

The effect over time is the whole point: every pass detects new hidden edges and repairs the surfaces
that describe them. Each scan makes the next edit safer. The repo improves its *own* readability. That
is a compounding loop — not vague magic, a concrete one.

## What it reveals (the shape of the deeper rung)

- **The reason AI-coded systems rot is a gap between what's *visible* and what's *actually causal*** —
  and you fix it by repairing the geometry, not by making the agent try harder.
- **Self-readability is a first-class activity, not a someday task.** The difference between a system
  that compounds and one that rots is whether each cycle *repairs its own self-description.* Skip
  that step and you're on the rotting trajectory by default.
- **An invisible-but-real connection should be made visible *at the exact point it matters*** — right
  where the next actor's attention will be — so the right information is present at the moment of the
  decision, not buried in a doc nobody opens.

## What you can take from it right now

The diagnosis transfers far beyond code: any system you run is either getting *more* self-readable
each cycle or *less,* and the rot is silent until it's downstream. Asking "where does this system's
record of itself drift from what it actually does?" is a free, sharp question — and the rot points it
surfaces (the stale doc, the hidden coupling, the "only so-and-so knows how this works") are exactly
where your system is quietly decaying.

## What this case study deliberately withholds (and where you go next)

This shows you the mechanism — AI-coded systems rot from a visible-vs-causal gap, the cure is
repairing self-readability every pass, and doing so flips a system onto the compounding trajectory —
but stops before the operational language to build the loop: the categories of hidden coupling a
scanner must detect, the form and placement of the markers, how a pass automatically finds new edges
and patches the explanatory surfaces, how it's wired so the repair happens without a human
remembering. That withhold is pacing, not a wall. First just *get* this: any system you run is getting
more self-readable each cycle or less, and the rot is silent until it's downstream. Then go ask the
free, sharp question — *where does this system's record of itself drift from what it actually does?* —
and *experience the effect* as the stale doc, the hidden coupling, the "only so-and-so knows how this
works" light up. Repair a few by hand and you *benefit*: the thing gets safer to touch the more you
touch it. Once you've felt a system compound instead of rot, the next rung — building the loop that
performs that repair every cycle on its own — is yours, now or after you come meet what it requires.

Named openly, because the honesty is the proof: this layer is itself a self-readability pass on
*you* — surfacing where your own systems quietly drift, right at the point it matters. Just keep
thinking like this, keep repairing the drift you find, and your own loop compounds toward the rung
where you could automate it. I'm not withholding the scanner to charge for it; I'm making sure you can
*see* the invisible edges yourself first, because a loop that repairs blind spots is only worth
building once you know they're there.
