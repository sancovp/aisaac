# Bounded-Arity Annealing: How a Kernelized Generator Drives an Approximate Model to Checkable Identity

> **DRAFT — re-aimed sections.** Sections 2–3 (the carrier, the observation order, and Theorems 1–3:
> the configuration space is a Scott domain; decoding/application are Scott-continuous; the depth order
> is the linear restriction of the observation order) are **retained unchanged** from the verified version
> and are only referenced here. Everything else — the abstract, the framing, and the old "closing operator
> / crowning" material — is replaced by what follows.

------------------------------------------------------------
## Abstract
------------------------------------------------------------

We describe a type of computation in which a stochastic generator — a large language model — operating one
fixed way inside a structured space, drives an initially **approximate** model of a domain toward **literal
coincidence** with a checkable formal structure. The space is a configuration space we prove to be a Scott
domain (Sections 2–3). Over it runs a **single** operation — a specialization recursion we call **FLOW** —
that progressively constrains the space (a descending chain of sub-domains) while **accumulating symmetry**.
We identify symmetry-accumulation with **arity-reduction**: it keeps each generative decision near the arity
at which the generator collapses a relation **reliably** — empirically, around four. Because the generator
never does anything else — the system is **kernelized** — the system's improvement *is* exactly this one
process, iterated, **composed** for depth and **distributed across a team** for breadth. Each configuration
decodes to a web of typed relational statements (a foundation ontology of `is-a`, `has-part`, `produces`),
and an **external mereological reasoner** checks them. The central claim — which we frame precisely and make
**falsifiable** rather than assume — is that as the recursion reduces arity, the fraction of the decoded
structure that passes the external check **rises toward identity**: the generator's approximate
("metaphorical") model becomes the formal structure itself. We prove the structural facts (the Scott domain;
the encoding-to-ontology; the specialization recursion), state the empirical convergence as a measurable
hypothesis with an explicit observable, and argue that the mechanism is **domain-blind** — nothing in it is
specific to any one domain — so a result on a single instance generalizes to anything that can be abstractly
structured.

------------------------------------------------------------
## 1. The type of computation
------------------------------------------------------------

A familiar picture of a language model is a generator that emits plausible text. The picture here is
different: the generator emits content **inside a structure**, and the structure is doing two things at
once. First, it is a **configuration space** with an exact order — a Scott domain (Section 3) — so partial
work has a precise meaning and limits exist. Second, every point of it **decodes to a typed claim about a
domain** — an ontological statement — so the structure is simultaneously a piece of mathematics and a piece
of meaning.

The computation has one move, applied over and over. Call it **FLOW**: choose a point, **fix it** (impose
it as a constraint), and re-enter the now-smaller space of everything consistent with that choice. Each fix
is a step down a chain of ever-more-specialized sub-spaces. As the chain descends, the structure **gains
symmetry** — repeated, interchangeable parts get grouped — and that gain is the engine of the whole thing.

Two supports carry the account, and we keep them rigorously apart:

- **The structural support (proved).** The configuration space is a Scott domain (Theorem 1); reading a
  configuration into content and composing configurations are Scott-continuous (Theorem 2); the naive
  "depth" order is just the linear case of the real information order (Theorem 3). Each specialized
  sub-space along FLOW is again a Scott domain. These are theorems.

- **The empirical support (measured, and here stated as a falsifiable claim — not assumed).** A language
  model collapses a relation among a *small* number of things **accurately**, and the accuracy degrades as
  that number grows; in our use the reliable band sits around four. Symmetry-accumulation is precisely what
  keeps each collapse inside that band. The claim the computation rests on is that, as FLOW drives the
  structure toward symmetry (hence toward low-arity collapses), the decoded ontology passes an **external**
  consistency check at a **rising rate, toward identity**. That is an observable about a running system, and
  Section 7 states exactly what to measure.

The payoff of separating them is the payoff of the whole paper: the structural support is settled, and the
empirical support is reduced to **one** measurable quantity — because the system is kernelized, there is only
one process to validate.

------------------------------------------------------------
## 2–3. The configuration space is a Scott domain  *(retained — see the verified version)*
------------------------------------------------------------

Sections 2 and 3 are unchanged. In brief, for the recall of the sections that follow: a **schema** is a
tree of slots, each slot carrying finitely many alternatives plus a marker `0` for "not yet chosen"; a
**configuration** assigns each slot either `0` or one alternative, consistently with the tree; the
**observation order** puts one configuration below another when the second has resolved at least as much and
agrees wherever the first committed. Theorem 1 establishes that this ordered space `D` is a **Scott domain**
(a bounded-complete algebraic dcpo with least element). Theorem 2 establishes that **decoding** a
configuration into content, and **composing** configurations, are Scott-continuous under explicit locality
hypotheses. Theorem 3 establishes that the linear "depth/prefix" order is exactly the restriction of the
observation order to single root-to-leaf chains. Nothing below modifies these results; they are the static
substrate on which FLOW runs.

------------------------------------------------------------
## 4. FLOW: the specialization recursion
------------------------------------------------------------

The one operation is **fix-and-descend**. Begin with the unconstrained space — every schema's
configurations, the whole Scott domain `D`. To **fix** a configuration is to impose it as a constraint `P`,
which selects the sub-space `D_P` of configurations consistent with it. By construction `D_P ⊆ D`, and `D_P`
is again a Scott domain (it is a configuration space in its own right, so Theorem 1 applies to it
unchanged). Iterating produces a descending chain

$$D \;=\; D_0 \;\supseteq\; D_1 \;\supseteq\; D_2 \;\supseteq\; \cdots,$$

each `D_{n+1}` obtained from `D_n` by fixing one more choice. This is FLOW. The base of the chain — `D`,
with no constraint — is the most general space; each step specializes.

It is convenient to read the chain through a small ladder of **levels**, indexed so that the base lineage is
*foundation → domain → instance* and the steps past an instance are **generators** that lift an instance back
up an order (the generator that takes an instance to its subtypes; the one that takes a subtype-level object
to a new domain; the one that takes that to a new instance). The generators are **level-typed**: each is
defined by the *level* of object it consumes, not by which generator produced that object — so they compose
freely. The reader needs only this: **FLOW is a self-similar descent in which fixing a point opens the next,
more specialized configuration space, and the levels recur.**

Two facts about the chain matter downstream. (i) Each `D_n` being a Scott domain means every stage has
limits and a well-defined notion of "more resolved," so partial descent is always meaningful. (ii) The
descent is **monotone in information** (each step resolves strictly more), so the chain is a directed path in
the order of Section 3 — FLOW moves *up* the observation order while moving *down* the chain of generality.

------------------------------------------------------------
## 5. The carrier is a foundation ontology
------------------------------------------------------------

The configurations are not bare numbers. Each one **decodes to a web of typed relational statements** — a
fragment of a *foundation ontology* built from a fixed, small vocabulary of relations: `is-a`, `has-part`,
`produces`, and the class/instance distinction. The decoding is purely structural: a node's parent gives its
`is-a`; a node's children give its `has-part` (its mereology); a node that opens a further space gives its
`produces`; the "not-yet-chosen" marker `0` reads as the **class** level and a committed choice as an
**instance**. Reading out the whole schema yields the entire ontology the configuration represents.

Two consequences fix the meaning of "convergence" used later.

- **Every level of structure stays an ontological statement.** However far FLOW descends, and however much
  symmetry accumulates, the object never stops being a web of `is-a`/`has-part`/`produces` claims that decode
  to ordinary sentences. There is no point at which the structure becomes "pure mathematics with the meaning
  stripped off"; the mathematics is *of* the meaning throughout.

- **The ontology is externally checkable.** Because the decoded statements are `is-a`/`has-part`/`produces`
  claims, an **external mereological reasoner** — a logical validator independent of the generator — can
  decide whether a decoded fragment is consistent (its parts cohere; its `is-a` chain closes). This external
  check is the **ground truth** against which everything that follows is measured. It is not the generator
  grading its own work: the validator is a separate system, and the check is mediated through a shared store
  of the decoded statements.

This is the crucial reframing of what the mathematics over the carrier *is*. The symmetry structure, the
orbit decompositions, and the like are, at any finite stage, **real mathematics that is approximately about
the ontology** — a structure-preserving correspondence that need not yet be exact. The target of the
computation is the state in which that correspondence becomes **exact**: the mathematical structure the
generator builds and the foundation-ontology structure the validator checks **coincide**.

------------------------------------------------------------
## 6. The empirical engine: bounded-arity collapse
------------------------------------------------------------

What makes FLOW *work*, rather than merely be well-defined, is a measured property of the generator.

**The bounded-arity fact (empirical).** A language model, asked to resolve a relation among a small number
of items into a definite choice, does so **reliably when that number is small** and with degrading accuracy
as it grows. In practice the reliable band sits around **four** (a heuristic centre, not an exact threshold).
This is the empirically-observed regularity the rest of the construction is engineered around; the canonical
demonstration is the stacking of a handful of cross-domain analogies into a single shared invariant, which a
generator performs accurately at that size and unreliably past it.

**Symmetry is arity-reduction.** Grouping `k` structurally-interchangeable alternatives into a single orbit
replaces a `k`-way choice with a 1-way one: the effective arity of the decision drops. So FLOW's
symmetry-accumulation is not decoration — it is the mechanism that **keeps each collapse inside the reliable
band**. As the descent of Section 4 piles up interchangeable structure, the arity of the choices the
generator must make falls toward the band where it is accurate.

**Scaling without leaving the band.** Arbitrary complexity is handled by two moves that never raise the
arity of any single collapse:

- **Compose (depth).** Collapse a small group to one object; treat that object as one item of the next small
  group; recurse. This is exactly FLOW's level recursion: each generator consumes a bounded number of
  level-`n` objects and emits a level-`(n{+}1)` one.
- **Team (breadth).** Partition a large set of independent choices into bounded groups and resolve the
  groups in parallel — by batching, or by distributing them across multiple generator instances. Each member
  still faces only a bounded-arity collapse.

Composition gives unbounded depth and teaming gives unbounded breadth, while **every atomic act stays a
bounded-arity collapse** — the only act the generator is reliable at.

------------------------------------------------------------
## 7. The convergence claim, stated as a measurable
------------------------------------------------------------

We now state the load-bearing claim precisely, and as something to be *measured*, not assumed.

Fix a domain and run FLOW. At each stage, read out the decoded foundation-ontology fragment (Section 5) and
submit it to the external mereological reasoner. Let the **agreement rate** at a stage be the fraction of the
decoded statements that the reasoner judges consistent. Let the **resolved arity** of a stage be the
(effective) arity the generator faced to reach it — high before symmetry has been accumulated, low after.

> **Convergence claim (empirical, falsifiable; NOT proved here).** As FLOW proceeds and the resolved arity
> falls toward the generator's reliable band, the agreement rate **rises monotonically toward 1** — i.e. the
> decoded structure converges to **identity** with the externally-checked foundation ontology. Equivalently:
> the generator's approximate model and the formal structure stop differing.

This is the precise content of "metaphor becomes literal." It is observable: agreement rate and resolved
arity are both measurable on a running system, and the claim is the assertion of a definite trend between
them. It is falsifiable: if the agreement rate fails to climb as arity is reduced — if it plateaus below 1,
or is uncorrelated with arity-reduction — the claim is refuted. We do **not** assert the trend here; we
isolate it as the one quantity whose measurement settles the account.

**The obstruction.** Where the agreement rate fails to climb, the cause is named: a region whose arity
**cannot** be reduced to the reliable band — an **irreducible high-arity** hyperedge, one with no symmetry to
collapse it. Such a region is exactly the "does not cohere, and one can see why" case: the generator cannot
reliably resolve it, and the external check correctly refuses it. The obstruction to convergence is therefore
not mysterious; it is irreducible arity, and it is detectable in advance (a region's reducibility is a
property of its symmetry, computable before the generator is invoked) — which is what lets the good and bad
regions of a configuration space be mapped *up front*.

------------------------------------------------------------
## 8. Generality: the mechanism is domain-blind
------------------------------------------------------------

Nothing in Sections 4–7 uses a property of any particular domain. FLOW fixes points and descends; the carrier
decodes to `is-a`/`has-part`/`produces` statements; symmetry reduces arity; the external reasoner checks
mereological consistency. None of these references mathematics, or law, or biology, or any specific subject —
they reference only *that the domain has been encoded as a structured, decodable ontology*. Consequently the
convergence claim, if it holds for one encoded domain, holds for **any** domain that can be encoded the same
way — anything that can be *abstractly figured out*, in the sense of being given a structured ontology and an
external consistency check. A single instance is not a special case to be re-proved per domain; it is a test
of a **domain-blind** mechanism. This is the reason the one measurable of Section 7 certifies the general
claim: the process that the measurement validates is the only process the system runs, and it does not know
what domain it is running on.

------------------------------------------------------------
## 9. Honest scope: proved, measurable, open
------------------------------------------------------------

**Proved (theorems, Sections 2–3 and 4).** The configuration space is a Scott domain; decoding and
composition are Scott-continuous under explicit locality hypotheses; the depth order is the linear
restriction of the observation order; each specialized sub-space along FLOW is again a Scott domain, so the
descent is well-founded and information-monotone.

**Established by construction (Sections 5–6).** Each configuration decodes structurally to a foundation-
ontology web (`is-a`/`has-part`/`produces`, class/instance); the decoded web is checkable by an external
mereological reasoner; symmetry-accumulation reduces effective arity; composition and teaming scale depth and
breadth without raising any atomic collapse's arity. The bounded-arity reliability of the generator is taken
as an **empirical premise** (observed; not a theorem).

**The measurable claim (Section 7), not yet established.** That the external agreement rate rises toward
identity as resolved arity falls. This is the convergence; it is falsifiable and is settled by measurement on
a running system, not by the mathematics above. The obstruction to it is irreducible arity.

**Open / deliberately out of scope.** The exact functional form of the agreement-rate-versus-arity trend; a
proof (as opposed to a measurement) of the convergence; and the precise correspondence between the foundation-
ontology relations and the level ladder of Section 4 — flagged for separate treatment. We also do not claim
the descent reaches a global fixed point in finitely many steps; we claim only that each step is well-defined
and information-monotone, and that the convergence is a property to be measured along the descent.

------------------------------------------------------------
## 10. Conclusion
------------------------------------------------------------

The computation is one move — fix a point, descend into the space it opens — run by a generator that is
reliable only at low arity, with symmetry accumulation as the device that keeps every move in that reliable
band, composition and teaming as the devices that scale it, and an external mereological reasoner as the
ground truth. Over a configuration space we prove to be a Scott domain, this single kernelized process drives
a decoded foundation ontology toward a state we make precise and measurable: **agreement with the external
check rising toward identity**. Because the process is domain-blind, the one measurement that would establish
the convergence on a single encoded domain would establish it for anything that can be abstractly structured.
The structural half is proved; the empirical half is reduced to one observable; and the two are kept strictly
apart so that neither is mistaken for the other.
