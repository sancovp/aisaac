# When is `D_consistent` a Scott domain? — The admissibility-closure conditions, and Crystal Ball's actual (upward-closed) admissibility

**A proof that resolves the standing OPEN of the Platform Theorem — by reading what
Crystal Ball's admissibility check actually IS, and deducing exactly which
Scott-domain axioms survive the restriction to the externally-validated subspace.**

---

## Abstract

**The standing OPEN.** The Platform Theorem
(`cb_encoding_is_a_scott_domain.md`) proves that Crystal Ball's coordinate
encoding instantiates a **Scott domain** `(D, ⊑)` on its **syntactic carrier** —
the configurations constrained only to be functional (no position holds two values)
and tree-respecting. It then explicitly leaves OPEN whether the **externally-validated
subspace** `D_consistent = {σ ∈ D : Adm(σ)}` — the configurations an out-of-process
`youknow()`/Griess reasoner accepts — is *itself* a Scott domain, and flags
**downward-closed admissibility** as the conjectured "clean sufficient condition"
(its §7 warns that a non-downward-closed predicate could break bounded-completeness).

**This paper.** We do two things.

1. **The abstract menu (Part I).** For an arbitrary admissible subset `A ⊆ D` of a
   Scott domain `D`, defined by a predicate `Adm`, we deduce exactly which Scott-domain
   axioms survive the restriction to `A` under each closure assumption on `Adm`
   (upward-closed, downward-closed, neither), each with a proof and, for each failure,
   a concrete witness. The clean result: **upward-closure preserves directed- and
   bounded-completeness but can destroy the least element and algebraicity; downward-
   closure preserves the least element, bounded-completeness, and algebraic approximants
   but can destroy directed-completeness; an arbitrary predicate can destroy any of
   them.** This *corrects and completes* the Platform Theorem's §7: bounded-completeness
   is preserved by **either** closure direction, and fails only for a predicate closed
   in neither.

2. **Crystal Ball's actual admissibility (Part II).** We READ the code. CB's
   admissibility is **not an arbitrary predicate and not downward-closed** — it is an
   **upward-closed monotone PRESENCE check**: `verifyKappa` (`griess.ts`, read in full)
   accepts a configuration iff, for every declared invariant, there **exists a *locked*
   matching node** (`griess.ts` verifyKappa body); and the per-node `youknow()` gate is
   applied one statement at a time to the *completed* kernel (`engine.ts:1201-1209`), a
   per-node completeness requirement of the same monotone shape. Locking is permanent
   (`index.ts:1655-1670`; Platform Invariant D), so committing more can only turn a
   requirement from unmet to met — **`Adm` is monotone w.r.t. `⊑`, i.e. upward-closed.**

   **The verdict.** Applying Part I's upward-closed case to CB's finitely-many-presence-
   requirements admissibility: `D_consistent` is a **directed-complete, consistent-
   complete (bounded-complete on nonempty bounded sets), ALGEBRAIC** poset — it satisfies
   **every** Scott-domain axiom **except possibly the least-element axiom**. It is a Scott
   domain **iff** it has a least element, equivalently **iff there is a unique minimal
   admissible configuration** (which is then automatically compact/finite). In general
   there are several minimal admissible configurations (several ways to satisfy the
   presence requirements), so `D_consistent` is a **bounded-complete algebraic dcpo
   without bottom**, and **adjoining a fresh ⊥ (lifting) makes `(D_consistent)_⊥` a Scott
   domain.** **PROVED.**

So the standing OPEN is discharged with a *correction*: the obstruction the prior papers
feared (bounded-completeness) is **not** the real one for CB; CB's real and only
obstruction is the **absence of a least element**, and it is fully repairable by lifting.

---

## Part 0 — Preliminaries (self-contained)

We reuse the carrier and order of the Platform Theorem. A **configuration** `σ` of a
fixed CB space is a partial assignment of reachable positions to ⊥ (uncommitted, digit
`0`) or a finite spectrum value (digit `1–7`); `com(σ)` is its set of `(position, value)`
commitments; `D` = all configurations (partial, total, idealized limits);
`σ ⊑ τ ⇔ com(σ) ⊆ com(τ)`. The Platform Theorem proves `(D, ⊑)` is a **Scott domain**:
least element `⊥ = ∅`, directed sups `⊔A = ⋃_{σ∈A} com(σ)`, compact elements `K(D)` =
the finite (finitely-committed) configurations, algebraic, bounded-complete.

We separate two notions usually fused under "bounded-complete," because the distinction
is the whole content of Part II:

- `(P, ⊑)` is **consistent-complete** if every **nonempty** subset that has an upper
  bound has a least upper bound. (Equivalently: every nonempty bounded pair has a join.)
- `(P, ⊑)` **has a least element** `⊥` if `⊥ ⊑ x` for all `x`.
- The textbook "**bounded-complete**" = consistent-complete **and** has `⊥` (the empty
  set is "bounded" by everything, so its lub is `⊥`). We keep them separate so we can say
  precisely which one CB loses.
- A **Scott domain** = a dcpo that is consistent-complete, algebraic, and **has `⊥`**.
- A subset `A ⊆ D` is **upward-closed** (an *up-set*) if `a ∈ A, a ⊑ b ⇒ b ∈ A`;
  **downward-closed** (a *down-set*) if `a ∈ A, b ⊑ a ⇒ b ∈ A`.
- A predicate `Adm : D → {T,F}` is **monotone** iff its truth-set `A = {σ : Adm(σ)}` is
  upward-closed (`σ ⊑ τ ∧ Adm(σ) ⇒ Adm(τ)`); **antitone** iff `A` is downward-closed.

Throughout, `A = D_consistent = {σ ∈ D : Adm(σ)}`, with the order inherited from `D`.
Restriction of a partial order to a subset is always a partial order, so `(A, ⊑)` is a
poset; the only questions are which **completeness/least-element/algebraicity** properties
survive.

---

## Part I — The abstract menu (which axioms survive each closure)

We fix a Scott domain `D` and an admissible subset `A ⊆ D` with predicate `Adm`. For each
property we state whether it transfers to `A`, under which closure of `Adm`, with proof
and (for failures) a witness. All sups/joins below are computed in `D` (as commitment-set
unions, Platform §4.3/4.5); the question is always "does the `D`-sup/join land back in
`A`, and is it the lub *within* `A`?"

### I.1 Directed-completeness.

> **Lemma 1 (up-sets are sub-dcpos).** If `A` is **upward-closed**, then `A` is closed
> under directed sups: for directed `B ⊆ A`, `⊔B ∈ A`, and `⊔B` is the lub of `B` in `A`.

*Proof.* `B` is directed and nonempty, so `⊔B = ⋃_{σ∈B} com(σ)` exists in `D` (Platform
§4.3). Pick any `σ₀ ∈ B`; then `σ₀ ⊑ ⊔B`, and `Adm(σ₀)` holds, so by upward-closure
`Adm(⊔B)`, i.e. `⊔B ∈ A`. It is the lub *in `A`* because it is the lub in `D` (a smaller
order) and lies in `A`. ∎

> **Non-transfer 1 (down-sets need not be sub-dcpos).** If `A` is only **downward-closed**,
> directed-completeness can FAIL.

*Witness.* Let `D` be the domain of the configurations of a space with one position of
spectrum size 1 reachable at every depth `n` (a single infinite chain
`⊥ ⊏ c₁ ⊏ c₂ ⊏ …`, `cₙ` committing the first `n` positions). Let `Adm(σ) ⇔ σ` is finite
(commits finitely many positions). `Adm` is downward-closed (a sub-configuration of a
finite config is finite). The chain `{cₙ}` is directed, all `cₙ ∈ A`, but its sup
`c_∞ = ⊔ₙ cₙ` is the infinite limit, which is **not** finite, so `c_∞ ∉ A`. Directed-
completeness fails. ∎

### I.2 Consistent-completeness (joins of nonempty bounded families).

> **Lemma 2 (either closure preserves consistent-completeness).** If `A` is **upward-
> closed OR downward-closed**, then `A` is consistent-complete: every nonempty `B ⊆ A`
> with an upper bound in `A` has a lub in `A`, namely `⊔B` (the `D`-join).

*Proof.* Let `B ⊆ A` be nonempty with an upper bound `ρ ∈ A`. In `D`, the join
`j := ⊔B = ⋃_{σ∈B} com(σ)` exists and `j ⊑ ρ` (Platform §4.5: a bounded family's union is
a configuration and is the least upper bound). It remains to show `j ∈ A`.
- If `A` is **upward-closed**: pick `σ₀ ∈ B`; `σ₀ ⊑ j`, `Adm(σ₀)` ⇒ `Adm(j)`.
- If `A` is **downward-closed**: `j ⊑ ρ`, `Adm(ρ)` ⇒ `Adm(j)`.
Either way `j ∈ A`, and it is the lub of `B` in `A` (being the lub in `D`). ∎

> **Non-transfer 2 (a predicate closed in NEITHER direction can break it).** This is the
> Platform §7 scenario, and it requires `Adm` non-monotone-AND-non-antitone.

*Witness.* Four independent positions `p, q, r, s`, each spectrum `{1}`. Let `Adm` accept
`{p:=1}`, `{q:=1}`, `ρ₁ := {p:=1, q:=1, r:=1}`, and `ρ₂ := {p:=1, q:=1, s:=1}`, but
**reject** `{p:=1, q:=1}` (the external reasoner couples `p, q`: "these two may not both be
set unless `r` or `s` is also set"). Consider `B = {{p:=1}, {q:=1}} ⊆ A`. Its upper bounds
in `D` are exactly the configurations committing both `p:=1` and `q:=1`; among these the
**admissible** ones are `ρ₁`, `ρ₂`, and configurations above them. The *minimal* admissible
upper bounds are `ρ₁` and `ρ₂` — and they are **incomparable** (`ρ₁` commits `r`, `ρ₂`
commits `s`, neither below the other), with the only configuration strictly between
`{p:=1,q:=1}` and either `ρᵢ` being `{p:=1,q:=1}` itself, which is rejected. So `B` is
bounded in `A` (e.g. by `ρ₁`) yet has **no least upper bound in `A`**: any `A`-upper-bound
is `⊒ ρ₁` or `⊒ ρ₂`, and there is no single least one. Consistent-completeness fails. Note
`Adm` is neither monotone (accepts `{p:=1}` but rejects the larger `{p:=1,q:=1}`) nor
antitone (accepts `ρ₁` but rejects the smaller `{p:=1,q:=1}`). The `D`-join
`{p:=1}⊔{q:=1} = {p:=1,q:=1}` being inadmissible is what forces the bound *upward* into the
two incomparable `ρᵢ`; rejecting it removed the join, and the coupling left two distinct
minimal admissible bounds in its place. ∎

**Corollary (corrects Platform §7).** Bounded-/consistent-completeness on `D_consistent`
is preserved by **either** an upward-closed **or** a downward-closed `Adm`; it can fail
**only** for an `Adm` closed in neither direction. The Platform Theorem's "downward-closed
is the clean sufficient condition" is **correct but incomplete** — upward-closed is *also*
sufficient (by the opposite half of Lemma 2), and this is the half that matters for CB
(Part II).

### I.3 Least element.

> **Lemma 3 (downward gives ⊥; upward generally does not).**
> (a) If `A` is **downward-closed** and nonempty, then `⊥ ∈ A` and is least in `A`.
> (b) If `A` is **upward-closed** and has the **finite-core property** (every `a ∈ A`
> dominates a finite `m ∈ A`; defined in I.4), then `A` has a least element **iff** `A`
> has a unique minimal element. In general (several minimal elements) it has **no** least
> element.

*Proof.* (a) `A` nonempty ⇒ pick `a ∈ A`; `⊥ ⊑ a` and downward-closure ⇒ `⊥ ∈ A`; `⊥` is
`D`-least hence `A`-least. (b) A least element is in particular *a* minimal element, and it
is below every element, so it is the unique minimal element. Conversely, suppose `A` has a
unique minimal element `m`. First, **every `a ∈ A` dominates a minimal element of `A`:** by
the finite-core property `a` dominates a finite `m_a ∈ A`; the finite admissible elements
`⊑ m_a` form a finite poset (a finite configuration has finitely many sub-configurations),
which has a minimal element `m'` of `A` with `m' ⊑ m_a ⊑ a`. By uniqueness `m' = m`, so
`m ⊑ a`. As `a` was arbitrary, `m` is least. The general failure (no finite-core
restriction needed) is exhibited next. ∎

*Witness for (b) (upward-closed, no least element).* One invariant `X` matchable by either
of two distinct nodes `a` or `b` (incomparable selections of one slot). `Adm(σ) ⇔ σ` locks
a node matching `X`. Then `{a-locked}` and `{b-locked}` are both admissible and **minimal**
(removing the lock makes `X` unmet), and they are incomparable. So `A` has two minimal
elements and no least element. (This is exactly CB's situation, Part II.) ∎

### I.4 Algebraicity.

> **Lemma 4 (algebraicity survives upward-closure when every admissible element has a
> finite admissible core).** Suppose `A` is **upward-closed** and satisfies the
> **finite-core property**: every `d ∈ A` dominates some **finite** `m ∈ A` (`m ⊑ d`,
> `m ∈ K(D) ∩ A`). Then `A` is algebraic, with compacts `K(A) = K(D) ∩ A` (the finite
> admissible configurations), and every `d ∈ A` is the directed sup of
> `{c ∈ K(D) ∩ A : c ⊑ d}`.

*Proof.* Fix `d ∈ A` and let `B_d = {c ∈ K(D) ∩ A : c ⊑ d}`.
- **`B_d` is nonempty:** the finite-core property gives a finite `m ∈ A`, `m ⊑ d`, so
  `m ∈ B_d`.
- **`B_d` is directed:** for `c, c′ ∈ B_d`, `c ⊔ c′ ⊑ d` is finite (union of two finite
  commitment-sets) and `⊒ c` with `c ∈ A`, so upward-closure gives `c ⊔ c′ ∈ A`; hence
  `c ⊔ c′ ∈ B_d` and bounds both.
- **`⊔ B_d = d`:** every `(p,v) ∈ com(d)` lies in some `c ∈ B_d`. Take the finite core
  `m ⊑ d` and adjoin to it the finite tree-path of commitments of `d` from the root down
  to `(p,v)`; call it `c`. Then `c` is finite, `c ⊑ d`, and `c ⊒ m ∈ A` ⇒ `c ∈ A` by
  upward-closure, so `c ∈ B_d` and `(p,v) ∈ com(c)`. Hence
  `com(d) ⊆ ⋃_{c∈B_d} com(c) ⊆ com(d)`, so `⊔ B_d = d`.
- **Compactness in `A`:** each `c ∈ K(D) ∩ A` is compact in `A`: if `c ⊑ ⊔B` for directed
  `B ⊆ A` (sup computed in `A` = sup in `D` by Lemma 1), then by compactness of `c` in `D`,
  `c ⊑ b` for some `b ∈ B`. And no element of `A` outside `K(D)` can be compact in `A`,
  because an infinite `d ∈ A` is the directed sup (just shown) of strictly smaller finite
  elements of `A`, so `d ⊑ ⊔B_d` with `d ∉ B_d`. Hence `K(A) = K(D) ∩ A`. ∎

> **Non-transfer 4 (without the finite-core property, algebraicity fails).**
*Witness.* Upward-closed `Adm` whose minimal admissible elements are all **infinite**
(e.g. "admissible iff infinitely many positions are committed"). Then for an admissible
`d`, every finite `c ⊑ d` is inadmissible, so `K(D) ∩ A` below `d` is empty and cannot sup
to `d`. Algebraicity fails. (This does NOT occur for CB: its requirements are satisfiable
by finitely many locked nodes — Part II.) ∎

### I.5 The menu, assembled.

| Property | upward-closed `Adm` | downward-closed `Adm` | neither |
|---|---|---|---|
| directed-complete (dcpo) | **YES** (Lemma 1) | can FAIL (NT 1) | can fail |
| consistent-complete | **YES** (Lemma 2) | **YES** (Lemma 2) | can FAIL (NT 2) |
| has least element `⊥` | iff unique min (Lemma 3b) | **YES** (Lemma 3a) | varies |
| algebraic | **YES iff finite-core** (Lemma 4) | needs sup-closure too | varies |

**Reading.** No single closure direction alone makes `A` a Scott domain:
- **Downward-closed** gives `⊥` + consistent-completeness + good finite approximants, but
  can lose **directed-completeness** (NT 1) — fatal for being a dcpo.
- **Upward-closed** gives **directed-completeness** + consistent-completeness + (with the
  finite-core property) **algebraicity**, but loses the **least element** (Lemma 3b) — the
  *only* missing axiom when the finite-core property holds.

The clean sufficient condition for `A` to be a **full Scott domain** is therefore: `Adm`
**upward-closed, with the finite-core property, AND a unique minimal admissible element**
(supplying `⊥`); OR `Adm` cutting out a **sub-Scott-domain** in the classical sense
(closed under directed sups *and* nonempty bounded joins, containing `⊥`, generated by its
own compacts). We now show CB realizes the **upward-closed + finite-core** branch, so its
*only* gap is the least element.

---

## Part II — Crystal Ball's actual admissibility is upward-closed (read from code)

We now read what `Adm` *is* in Crystal Ball. There are two admissibility surfaces; both
are **monotone presence checks**, hence upward-closed.

### II.1 `verifyKappa` (Griess) — fully read, provably upward-closed. **PROVED.**

**The fact (whole function read, `griess.ts`).** `verifyKappa(space, nodes, sha)` takes
the declared `κ_user` (a `domain` plus a set of named `invariants`) and, **for each
invariant** `invName`:
- collects `relatedNodes` = the space's nodes whose label fuzzy-matches `invName` (word
  containment, case-insensitive);
- marks the invariant **satisfied** iff there exists a related node that is **locked**
  (`node.locked || node.frozen`) **and** has **amplitude > 0**; otherwise unsatisfied
  (with a reason: "no matching node," "none locked," or "all Born-0 amplitude").

The outcome is `ont` (admissible) iff `failedCount === 0` (every invariant satisfied) and
`sha === 0`. So, writing `σ` for the configuration carried by the space's locked nodes,

> `Adm(σ) ⇔ for every declared invariant i, ∃ a node n with label-match(i, n),
>            locked(n) in σ, and amplitude(n) > 0`   (`griess.ts` verifyKappa body).

**Claim: `Adm` is monotone w.r.t. `⊑` (upward-closed).**

*Proof.* Suppose `Adm(σ)` and `σ ⊑ τ`. By the order, `com(σ) ⊆ com(τ)`: `τ` has **every
commitment `σ` has**, including every lock. Locking is **permanent and append-only** —
`lockNode` is idempotent and never un-commits (`index.ts:1655-1670`), and `resolve` only
adds children/commitments, never altering an existing one (`index.ts:1377-1396`,
`index.ts:1430-1438`; Platform Invariant D). So every node locked in `σ` is still locked in
`τ`, with its label and amplitude unchanged (no operation lowers an existing node's
amplitude; amplitude is a fixed Born weight of an existing node, and `τ` only *adds*
nodes). Hence every witness that made an invariant satisfied in `σ` is still present in
`τ`. Therefore every invariant satisfied in `σ` is satisfied in `τ`, so `Adm(σ) ⇒ Adm(τ)`.
∎ (The one code-fact this rests on is **lock/amplitude stability under extension** —
guaranteed by append-only resolution and idempotent locking.)

**Finite-core property holds.** `κ_user` has **finitely many** invariants
(`Object.entries(invariants)`); satisfying `Adm` requires, per invariant, **one** locked
matching node. So a configuration that locks exactly one matching node per invariant (a
finite set of commitments, plus their finite tree-paths) is a **finite** admissible
configuration `⊑` any admissible `d` that contains those witnesses — i.e. every admissible
`d` dominates a finite admissible core (choose, for each invariant, one of `d`'s witnessing
locked nodes; the finite config of just those is admissible and `⊑ d`). **PROVED.**

### II.2 The per-node `youknow()` gate — upward-closed by its completeness shape. **REASONED FROM INTERFACE.**

**The fact (`engine.ts:1201-1209`).** When the kernel becomes complete, the engine sends
`buildSpaceUARL(crystal)` to the injected `youknowFn`, **looping one statement at a time**
(`for (const uarl of spaceUarl) { youknowFn(uarl.raw) }`) and counting `OK` vs rejected.
`buildSpaceUARL`/`buildUARL` emit **per-node** UARL triples (`uarl-aligner.ts`; one
statement per node/edge with a UARL predicate `is_a`/`part_of`/`instantiates`/…). The
`youknowFn` itself is an **out-of-process** SOMA call (`youknow-bridge.ts` shells out), so
its predicate is not re-derived here; we characterize its **shape** from the interface and
the SOMA architecture.

**Why it is upward-closed (reasoned).** The SOMA `is_ont`/strong-compression gate accepts a
node iff its required **core-sentence predicates are present** and the reachable targets
**close** (a *presence/completeness* requirement — the architecture's "all 8 predicates
present + recursive target-closure"). A completeness requirement is **monotone in
structure**: adding commitments/relations to a configuration can only *add* the
predicates/targets a node needs, never remove them (resolution is append-only, Platform
Invariant D). So a node that passes in `σ` still passes in any `τ ⊒ σ`, and the
conjunction-over-nodes `Adm_youknow(σ) = ⋀_n is_ont(n in σ)` is monotone, i.e. **upward-
closed.** *Status:* the **shape** (per-node completeness ⇒ monotone) is read from the
interface (`engine.ts:1201-1209`) and the SOMA architecture; the full `is_ont` predicate
lives out-of-process and is not reproduced here, so this item is **REASONED FROM
INTERFACE**, not a line-by-line in-code proof like II.1. Its finite-core property holds for
the same reason: passing requires finitely many present predicates over the (finite,
kernel-complete) node set.

### II.3 The verdict for CB. **PROVED (modulo II.2's interface-level status).**

CB's admissibility `Adm` (whether `verifyKappa`, the in-code witness of II.1, or the
per-node gate of II.2) is **upward-closed with the finite-core property**. Apply Part I:

- **Directed-complete (dcpo):** **YES** (Lemma 1). A directed family of admissible
  configurations has its `D`-sup admissible — an ascending chain of valid resolutions
  stays valid in the limit.
- **Consistent-complete:** **YES** (Lemma 2, upward half). Two admissible configurations
  with a common admissible bound have an admissible join (`σ ⊔ τ ⊒ σ` ⇒ admissible). *This
  is the property the Platform Theorem feared losing; it survives, because CB's `Adm` is
  upward- (not arbitrary-) closed.*
- **Algebraic:** **YES** (Lemma 4 + finite-core, II.1/II.2). Compacts = finite admissible
  configurations; every admissible element is their directed sup, built from a finite
  admissible core plus finite extensions.
- **Least element `⊥`:** **NOT in general** (Lemma 3b + the II.1 witness: one invariant
  matchable by two incomparable nodes gives two minimal admissible configurations). The
  all-`0` `⊥` of `D` is **inadmissible** (it locks nothing, so no presence requirement is
  met — unless there are zero requirements).

**Therefore `D_consistent` is a directed-complete, consistent-complete, algebraic poset
that is a Scott domain *iff* it has a least element, i.e. iff there is a unique minimal
admissible configuration.** Equivalently: `D_consistent` is a **bounded-complete algebraic
dcpo without bottom**, and its **lifting `(D_consistent)_⊥`** (adjoin a fresh least
element below everything) **is a Scott domain** — adjoining `⊥` to a consistent-complete
algebraic dcpo yields a consistent-complete algebraic dcpo *with* `⊥`, and the fresh `⊥` is
compact, preserving algebraicity. **PROVED.**

### II.4 Why this is the right characterization, not an artifact.

- *The CB design intends multiple minimal admissible configurations.* A space typically has
  several distinct ways to satisfy its `κ_user` invariants (different node choices
  matching the same invariant), so several incomparable minimal admissible kernels — the
  generic case is **no least element**, exactly Lemma 3b's witness realized.
- *The missing axiom is purely the bottom.* Every *completeness*-flavoured axiom (dcpo,
  consistent-complete, algebraic) survives because the check is **monotone presence**. The
  encoding's own dynamics confirm the direction: resolution only ever **adds** locks
  (append-only, idempotent), so it can only move a configuration from inadmissible toward
  admissible, never the reverse — the hallmark of an up-set.
- *Lifting is the canonical repair.* `(D_consistent)_⊥` is the free way to restore a least
  element; semantically `⊥` = "the validation has not yet been met," sitting below every
  admissible kernel. With it, `D_consistent` becomes a genuine Scott domain and inherits all
  of the Equipment paper's free structure (function space, Kleene `lfp`, products/sums) on
  the *validated* subspace, not merely the syntactic carrier.

---

## Part III — Reconciliation with the Platform Theorem's §7

The Platform Theorem §7 wrote: *"If the admissibility predicate is **not downward-closed**,
bounded-completeness can fail … two admissible σ, τ with an admissible common upper bound
whose union σ ⊔ τ is inadmissible."* Part I.2 (NT 2) confirms this is a **real failure mode
— but only for a predicate closed in NEITHER direction** (the §7 witness is non-monotone:
it accepts the parts and a larger bound yet rejects the middle join). The §7 note implicitly
treated "not downward-closed" as "dangerous," but the precise statement is:

> **Bounded/consistent-completeness fails only when `Adm` is non-monotone AND non-antitone.**
> It is preserved by upward-closed `Adm` (Lemma 2, upward half) just as by downward-closed
> `Adm` (Lemma 2, downward half).

CB's `Adm` is **upward-closed** (Part II), so it lands in the *safe* half: consistent-
completeness is **preserved**, and the §7 worry does not apply to Crystal Ball. The genuine
obstruction Part II surfaces — the **absence of a least element** — was *not* the one §7
named, and it is repairable by lifting rather than fatal. This is the correction the
proposition contributes: **the standing OPEN closes as "almost-yes" — `D_consistent` is a
Scott domain up to a single adjoined ⊥, and is one outright exactly when the admissible
minimum is unique.**

---

## Conclusion

**Verdict: PROVED, with a correction.** Reading Crystal Ball's actual admissibility — the
fully-read `verifyKappa` presence check (`griess.ts`) and the per-node `youknow()`
completeness gate (`engine.ts:1201-1209`), both **upward-closed** because locking is
permanent and resolution append-only (`index.ts:1655-1670`, `:1377-1396`; Platform
Invariant D) — and applying the abstract menu of Part I, the externally-validated subspace
`D_consistent` is a **directed-complete, consistent-complete, algebraic** poset whose
**only** missing Scott-domain axiom is the **least element**. It is a Scott domain **iff**
the minimal admissible configuration is **unique**; in the generic multiple-minima case it
is a **bounded-complete algebraic dcpo without bottom**, and its **lifting
`(D_consistent)_⊥` is a Scott domain**. This **discharges and corrects** the Platform
Theorem's standing OPEN: the feared loss of bounded-completeness does **not** occur for
CB's upward-closed admissibility (Lemma 2 preserves it from the up-side); the real and only
obstruction is the bottom, and it is canonically repairable. The downward-closed condition
the Platform Theorem conjectured is *sufficient* for some axioms but, for Crystal Ball, the
operative condition is the **opposite** closure — and it delivers more (the full
completeness/algebraicity stack), missing only `⊥`.

**Scope honesty.** Part II.1 (`verifyKappa`) is a **line-by-line in-code** proof of
upward-closure. Part II.2 (the out-of-process `youknow()` gate) is **reasoned from the
interface + SOMA's completeness shape**, not reproduced line-by-line (the predicate runs in
Prolog out-of-process via `youknow-bridge.ts`); its upward-closure is marked accordingly.
The abstract menu (Part I) is proved unconditionally. The least-element repair (lifting) is
a standard domain-theoretic fact, proved here for our carrier.
