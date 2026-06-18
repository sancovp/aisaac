# Case study: the validator that won't let the AI be wrong about Susan

**Source pattern (advanced):** the admissibility validator (YOUKNOW + the knowledge graph) that
checks every claim/concept against an ontology and refuses to admit malformed ones — holding them in
a quarantine until they're repaired.
**Derived from:** `admissibility-engineering.html`, `l5-admissibility.html`, `admissibility.html`,
`l6-concentration.html` (traceback-as-instruction).
**+1 generalization applied:** told as the *class* of "compositional validators" and the experience
of being one, not the specific entity-chain syntax, the OWL restrictions, or the SOUP/repair
internals.

---

## The anecdote

Susan processes invoices every Tuesday. She routes them to Jim in procurement first, because of a PO
check. She cares more about the cost-center field than anything else. She takes a chocolate break at
4pm on Wednesdays. Your AI knows *none* of this — and worse, it will happily generate a confident,
plausible workflow for "automate Susan's job" that has *never existed*: invoice goes straight to the
approver, cost-center check skipped, Jim never mentioned. It doesn't know. It *performs* knowing.

The fix that actually works isn't "give it more context." You can paste fifty pages of Susan's
procedures into the window and it'll still contradict page 23, because reading is not the same as
understanding compositionally. The fix is to *constrain how the AI is allowed to talk about Susan.*
Every claim it makes has to decompose into parts that are each individually validated, all the way
down. "Susan's invoices go through Jim for PO validation" is admissible *because* every piece of
that composition is real. "Susan's invoices go straight to the CFO" is *inadmissible* — not because
it sounds wrong, but because the composition doesn't close: there's no validated path from Susan's
invoices to the CFO. The system catches it. Immediately.

## What it reveals (the shape of the deeper rung)

- **There's a thing that sits between the AI and reality and *gates* what gets admitted.** New claims
  are proposed; the gate checks them against a typed model of what's allowed; claims that don't
  compose are *not admitted as knowledge* — they're held aside until repaired or they sit there
  forever, never participating in anything downstream.
- **The model is built up, not declared.** You start with almost nothing ("what *is* an invoice?
  what's a 'Susan'?") and add validated observation on validated observation until you have a model
  the AI must respect. Each layer verified before the next is trusted.
- **An error is an instruction, not a dead end.** When a claim is rejected, the rejection *tells the
  AI exactly what's missing and how to fix it* — "you said X requires Y, and Y has never been
  observed; observe Y first" — and primes it to repair rather than just fail. The failure message is
  the next prompt.

## What you can take from it right now

The distinction is the gift: your AI doesn't *know* your domain, it *performs* knowing it — and the
cure isn't more documents, it's whether claims have to *compose from validated parts.* Just holding
that distinction changes how you evaluate every AI output you depend on, and it's free.

## What this case study deliberately withholds (and where you go next)

This shows you the experience — a compositional validator exists, what it feels like to have one
gating the AI's claims, how rejected claims become repair instructions — but stops before the
operational language to build one: the syntax in which claims/concepts are actually emitted, the
formal ontology and its type restrictions the gate checks against, the mechanics of decomposing and
checking a claim at every depth, how the quarantine-and-repair cycle is implemented so a malformed
claim can never slip through. That withhold is pacing, not a gate. First just *get* the distinction:
your AI doesn't *know* your domain, it *performs* knowing it, and the cure isn't more documents — it's
whether claims have to compose from validated parts. Then carry that distinction into every AI output
you depend on and *experience the effect* — you'll catch the confident, plausible thing that never
existed. Hold the line and you *benefit*: you stop trusting fluent where you needed right, especially
where a wrong answer costs real money. Once that judgment is reflex, the next rung — constructing the
validator that makes wrong claims structurally inadmissible — is there to step into now, or to come
meet the prerequisites for first.

Named in the open, because saying it doesn't make it less true: I'm handing you one clean distinction
and pointing you in its direction. Just keep thinking in composes-from-validated-parts and applying
it, and your own discernment composes upward toward the rung where you could build the gate yourself.
I'm not withholding the apparatus to gate you behind a price; I'm making sure you can *feel* the
difference between right and fluent before you try to engineer it, because you can't build a validator
for a distinction you can't yet make.
