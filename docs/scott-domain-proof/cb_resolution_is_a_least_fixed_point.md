# Crystal Ball's instantiation is a least fixed point — the resolution operator on `D`, proved

**A theorem turning the standing remark "instantiation = collapsing all 0s = ⊔ₙ rⁿ(⊥)"
into a proof: Crystal Ball's `resolve` operation, read from code, is a monotone
inflationary self-map of the Scott domain `D`, whose iteration from `⊥` is exactly the
instantiation process and converges to its least fixed point.**

---

## Abstract

**The standing remark.** Two prior papers — the Platform Theorem
(`cb_encoding_is_a_scott_domain.md`, §5) and the Equipment paper
(`cb_equipment_of_an_encoded_space.md`, A7) — *observe*, without proving it as a theorem
about the actual code, that Crystal Ball's instantiation ("collapsing all `0`s to
selections") is the Kleene supremum `⊔ₙ rⁿ(⊥)` of a climb from `⊥`. The Equipment paper
also proves, as free structure, that the function space `[D→D]` is a Scott domain (A6) and
that every Scott-continuous self-map has a least fixed point `⊔ₙ fⁿ(⊥)` (A7, Kleene). What
was **not** done is to read CB's `resolve` operation and prove that *it* is such a self-map,
so that "instantiation = least fixed point" is a theorem about Crystal Ball rather than an
analogy.

**This paper does that.** We read `resolve` (`index.ts:1336-1462`) and the FLOW/compile
iteration. We define, for a fixed **fill policy** `π`, the one-round resolution operator
`r_π : D → D`, and prove:

1. **`r_π` is inflationary — unconditionally.** `σ ⊑ r_π(σ)` always, because `resolve` is
   **append-only**: it only ever adds a new child to a parent's spectrum (gated on
   `!alreadyExists`), never deletes or overwrites a commitment (`index.ts:1382-1396`,
   `index.ts:1430-1437`; lock idempotent `index.ts:1655-1670`; Platform Invariant D).
   **PROVED.**
2. **`r_π` is monotone — on the π-coherent subdomain `D_π`.** Monotonicity is **false on all
   of `D`** (an arbitrary configuration may commit a slot to a non-`π` value); it holds on
   `D_π = {σ : every committed slot s has σ(s) = value(s)}`, which is itself a **Scott
   domain**, is `r_π`-closed, and contains `⊥` and the whole instantiation climb. **PROVED on
   `D_π`** (for a consistent policy). This is a **domain restriction**, not merely a policy
   condition.
3. **Instantiation IS the fixed-point climb (Bourbaki–Witt).** The instantiation process is
   the ascending chain `⊥ ⊑ r_π(⊥) ⊑ r_π²(⊥) ⊑ …`; its supremum `σ*` is a **fixed point**
   of `r_π` (the state with no `0`s left, `resolve` mode `complete`,
   `index.ts:1449-1453`), and for a **finite-depth** space it is reached in **finitely many
   rounds**. For an infinite-depth space `σ*` is the limit `⊔ₙ r_πⁿ(⊥)`. **PROVED** (finite
   depth) **/ PROVED under ω-continuity** (infinite depth).
4. **It is the *Kleene least* fixed point — on `D_π`, under a finitary, consistent policy.**
   When `π` is consistent (item 2) and **finitary** (each round fills the finitely many
   currently-exposed slots, each from a finite local context), `r_π` is ω-Scott-continuous on
   the Scott domain `D_π`, so by Kleene (Equipment A7) `σ* = ⊔ₙ r_πⁿ(⊥)` is the **least**
   fixed point of `r_π` **on `D_π`** (the least *among π-coherent configurations*). **PROVED
   on `D_π`.** Over all of `D`, `σ*` is **not** least — every totally-resolved coordinate
   (including incoherent ones) is a fixed point; those lie outside `D_π` and the restriction
   excludes exactly them.

**The honest boundary (held hard).** This proves **instantiation-as-least-fixed-point for
the resolution operator on the carrier `D` we actually built** — the rigorous core of "a
decision is a climb to a fixed point." It does **NOT** establish the architecture's §9
vision that *GNOSYS = `fix(Φ)`* of a **reflexive** domain `D ≅ [D→D]` with a continuous
`Φ` over the *Sanctuary* domain: `r_π` is a self-map of `D`, not a witness that `D` is
reflexive, and `π` is supplied **externally** (by an LLM/user), so `r_π` is deterministic
only **after fixing `π`** — the theorem is about the resolution *dynamics given a policy*,
never about the policy-source being deterministic. Those §9 claims remain **VISION**; this
paper proves only what the code's resolution operator does on `D`.

---

## Part 0 — Preliminaries (self-contained; carrier reused)

We reuse the Platform Theorem's carrier. A **configuration** `σ` of a fixed CB space is a
partial assignment of reachable positions to `⊥` (uncommitted, digit `0`) or a finite
spectrum value (digit `1–7`); `com(σ)` = its `(position,value)` commitments; `D` = all
configurations (partial, total, idealized limits); `σ ⊑ τ ⇔ com(σ) ⊆ com(τ)`. The Platform
Theorem proves `(D, ⊑)` is a **Scott domain** (least element `⊥ = ∅`, directed sups
`⊔A = ⋃ com(σ)`, compacts = finite configurations, algebraic, bounded-complete).

- A map `f : D → D` is **monotone** if `σ ⊑ τ ⇒ f(σ) ⊑ f(τ)`; **inflationary**
  (a.k.a. *increasing/progressive*) if `σ ⊑ f(σ)` for all `σ`; **Scott-continuous** if
  monotone and `f(⊔A) = ⊔ f(A)` for every directed `A`; **ω-continuous** if it preserves
  the sups of ascending `ω`-chains (`f(⊔ₙ xₙ) = ⊔ₙ f(xₙ)` for `x₀ ⊑ x₁ ⊑ …`).
- A **fixed point** of `f` is `x` with `f(x) = x`; the **least fixed point above `⊥`** is
  the `⊑`-least fixed point `≥ ⊥`.
- **Bourbaki–Witt theorem (used as a cited classical result):** an inflationary map on a
  chain-complete poset (every chain has a sup) has a fixed point; iterating from any point
  (transfinitely) reaches one. **Pataraia's theorem:** a monotone map on a pointed dcpo has
  a *least* fixed point. **Kleene (Equipment A7, reproved there):** a Scott-continuous map
  `f` on a dcpo with `⊥` has least fixed point `⊔ₙ fⁿ(⊥)`.

`D` is a Scott domain, hence a pointed dcpo and chain-complete, so all three theorems apply
to self-maps of `D`.

---

## Part 1 — What `resolve` IS (invariants mined from the code)

We read `resolve(registry, spaceName, coordinate, fills)` (`index.ts:1336-1462`) and the
surrounding FLOW.

### 1.1 `resolve` scrys, then commits provided fills into exposed `0`-slots, append-only.

`resolve` first `scry`s the coordinate to obtain the **generation slots** — the positions
currently at `0` (`scry` fans a `0` to its children and records a `GenerationSlot`,
`index.ts:935-1006`, returned as `scryResult.slots`). Then, for each slot, **if `fills`
supplies a value**, it commits that value:

- if the value is a new label, it **appends a new child** to the parent's spectrum —
  `parentNode.children.push(newId)` after checking `!alreadyExists` (`index.ts:1377-1396`),
  or `addNode(targetSpace, node.id, …)` again gated on `!alreadyExists`
  (`index.ts:1430-1437`); `newValuesCommitted++` each time;
- if no fill is supplied for a slot, the slot is returned in `remainingSlots`
  (`index.ts:1400-1402`).

Crucially, every write is an **append guarded by `!alreadyExists`**: a value already
present is never re-added, and **no branch ever deletes a child or overwrites an existing
commitment.** Locking is idempotent and never un-commits (`index.ts:1655-1670`). This is
Platform Invariant D (extension is conservative) localized to `resolve`.

**Invariant R1 (append-only).** `resolve` transforms a configuration `σ` into a
configuration `σ'` with `com(σ) ⊆ com(σ')`: it only adds `(position,value)` commitments
(the filled slots), never removes or changes one.

### 1.2 The mode signals the fixed point.

`resolve` returns `mode = "complete"` iff `scryResult.unresolvedZeros === 0` — no `0`s
remain at the coordinate (`index.ts:1449-1453`). In `complete` mode there are no slots to
fill, so `resolve` commits nothing (`newValuesCommitted` stays 0, `output` is the existing
resolution). The FLOW (the lock→auto-scry→auto-mine compile loop, `engine.ts:1190-1232`,
and the `scry`/`compile` iteration drivers) repeats resolution rounds until this `complete`
state.

**Invariant R2 (completion is a no-growth state).** When a configuration has no exposed
`0`s within the space's boundary, a resolution round adds nothing: it is a state `σ*` with
`r(σ*) = σ*` for the round operator `r` (a fixed point).

### 1.3 Resolution exposes deeper positions (drill/bloom), so rounds form a chain.

Committing a selection can expose a node's sub-space: `scry` follows a selected node into
its produced space / children for the next level (`index.ts:1009-1061`), and drilling (`8`)
opens a selected node's sub-space (`index.ts:768-790`) — the dependent-product structure
(Equipment B3). So filling the `0`s exposed at round `n` can expose **new** `0`s at round
`n+1` (one level deeper), which the next round fills.

**Invariant R3 (rounds descend the tree).** Successive resolution rounds commit
successively deeper positions; the exposed-slot set at round `n+1` consists of positions
governed by commitments made at round `n` (tree-respecting, Platform Invariant E).

---

## Part 2 — The resolution operator `r_π` and its order properties

### 2.1 Definition.

A **fill policy** `π` is a function that, given a configuration `σ` and its exposed slots
`Slots(σ)` (the positions at `0` reachable in `σ`), supplies a value `π(σ, s)` (a spectrum
selection) for each `s ∈ Slots(σ)` it chooses to fill. (In the running code, `π` is realized
by the `fills` record assembled from an LLM/user; here we **fix** a policy `π` to study the
dynamics, see the boundary.) Define the **one-round resolution operator**

> `r_π : D → D`, `r_π(σ) = σ` with each chosen exposed slot `s` committed to `π(σ, s)`,

i.e. `com(r_π(σ)) = com(σ) ∪ { (s, π(σ,s)) : s ∈ Slots(σ), π fills s }`. By Invariant R1
this union is a legitimate configuration (it only adds commitments; functionality holds
because a slot at `0` had no prior value, and `π` commits it to one value).

### 2.2 `r_π` is inflationary — unconditionally. **PROVED.**

By construction `com(σ) ⊆ com(r_π(σ))` (R1: only additions). Hence `σ ⊑ r_π(σ)` for **every**
`σ ∈ D` and **every** policy `π`. ∎ (This needs nothing of `π` — it is the append-only
invariant. It is the one property that holds even when the external policy is arbitrary.)

### 2.3 The π-coherent subdomain `D_π`, and monotonicity ON it. **PROVED on `D_π`.**

Monotonicity is **false on all of `D`**, and saying so honestly is the point. Call `π`
**consistent** if for each slot `s` the value it assigns is a well-defined `value(s)`
depending only on `s`'s local context (the parent node and its spectrum), not on commitments
elsewhere — the shape `resolve` supports, since it reads each slot from `scryResult.slots`
as an independent local `GenerationSlot` (`index.ts:860-867`). Even for a consistent `π`,
`r_π` is **not** monotone on the whole carrier `D`:

> **Counterexample (monotonicity fails on `D`).** Let `value(s) = 2`. Let `σ` expose `s`
> (leave it at `0`), and let `τ = σ ∪ {(s, 5)}` (some *other* configuration that already
> committed `s` to `5`). Then `σ ⊑ τ`, but `r_π(σ)` commits `s` to `2` while `r_π(τ)` keeps
> `s` at `5`, so `r_π(σ) ⋢ r_π(τ)`. Monotonicity fails — because `τ` is an arbitrary element
> of `D` (Part 0: *all* configurations), free to commit `s` to a value `π` would not choose.

The missing hypothesis is therefore **not** about the policy but about the **domain**: we
must work where every commitment already agrees with `π`. Define the **π-coherent
subdomain**

> **`D_π = { σ ∈ D : every committed slot s of σ has σ(s) = value(s) }`**

— the configurations all of whose commitments are the ones `π` would make. Three facts:

- **`D_π` is a sub-Scott-domain.** It contains `⊥` (no commitments, vacuously coherent). It
  is **downward-closed** (a sub-configuration of a coherent configuration is coherent — it
  drops commitments, never adds a wrong one) and **closed under directed sups and bounded
  joins** (a union of coherent configurations is coherent: every commitment in the union
  matches `value(·)`, and functionality holds since all agree on `value(s)`). A sub-poset of
  a Scott domain that contains `⊥` and is closed under directed sups and bounded joins, with
  compacts = its finite members, is itself a Scott domain — `D_π` is order-isomorphic to the
  inclusion order of tree-respecting sets of *committed slots* (each slot's value forced to
  `value(s)`), an algebraic bounded-complete dcpo with `⊥`. So `(D_π, ⊑)` is a **Scott
  domain**.
- **`D_π` is `r_π`-closed.** `r_π(σ)` adds only commitments `(s, value(s))` (§2.1), so if `σ`
  is coherent so is `r_π(σ)`. Hence `r_π` restricts to `r_π : D_π → D_π`.
- **The climb lives in `D_π`.** `⊥ ∈ D_π` and `D_π` is `r_π`-closed, so every iterate
  `r_πⁿ(⊥) ∈ D_π` (Part 3).

> **Lemma R (monotone on `D_π`).** For a consistent `π`, `r_π : D_π → D_π` is monotone.

*Proof.* Let `σ ⊑ τ` with `σ, τ ∈ D_π`. A slot `s` exposed in `σ` is either (a) still
exposed in `τ`, or (b) already committed in `τ`. For (a), both `r_π(σ)` and `r_π(τ)` commit
`s` to the same `value(s)` (consistency), agreeing on `s`. For (b), `τ ∈ D_π` so its
commitment of `s` **is** `value(s)` by coherence — exactly the value `r_π(σ)` commits — so
again they agree on `s`. All other commitments of `σ` are in `τ` (since `σ ⊑ τ`) and are
preserved by `r_π` (R1). Hence `com(r_π(σ)) ⊆ com(r_π(τ))`, i.e. `r_π(σ) ⊑ r_π(τ)`. ∎ (Case
(b), which fails on `D`, is exactly what `D_π`'s coherence makes valid.)

(The honest status: monotonicity is a **domain-restricted** result — it holds on the
π-coherent Scott domain `D_π`, which contains `⊥` and the entire instantiation climb, and is
where the fixed-point theory below operates. On the full `D`, with an inconsistent or
adversarial configuration, `r_π` is only **inflationary** (§2.2, unconditional).)

---

## Part 3 — Instantiation is the fixed-point climb

### 3.1 The instantiation chain. **PROVED.**

Iterate `r_π` from `⊥` (the all-`0` coordinate): `x₀ = ⊥`, `xₙ₊₁ = r_π(xₙ)`. By §2.2
(inflationary), `xₙ ⊑ xₙ₊₁` for all `n`, so `{xₙ}_{n≥0}` is an **ascending chain** in `D`.
This chain **is** the instantiation process: `x₁` commits the top-level positions exposed at
`⊥`; `x₂` commits the positions those expose (R3); and so on, descending the tree — exactly
"collapsing all `0`s to specific selections" (`index.ts:11`), performed level by level.

### 3.2 Its supremum is a fixed point. **PROVED.**

Because `D` is a dcpo (Platform §4.3) and `{xₙ}` is a chain (hence directed), the supremum
`σ* := ⊔ₙ xₙ` exists in `D`. Two cases:

- **Finite-depth space** (the tree has bounded depth `≤ d`; the generic CB kernel). Each
  round commits the positions of one more level (R3) and each level is filled at most once
  (append-only, a committed slot is never re-exposed), so after at most `d` rounds every
  position within the boundary is committed: `x_N` (for some `N ≤ d`) has **no exposed
  `0`s** — `resolve` returns `mode = "complete"` (R2, `index.ts:1449-1453`) — and
  `r_π(x_N) = x_N`.
  Then `σ* = x_N` is reached in finitely many rounds and **is a fixed point**. **PROVED.**
- **Infinite-depth space** (drill/bloom unbounded). `σ*` is the infinite limit `⊔ₙ xₙ`. It is
  a fixed point provided `r_π` preserves this chain's sup (ω-continuity, §4): then
  `r_π(σ*) = r_π(⊔ₙ xₙ) = ⊔ₙ r_π(xₙ) = ⊔ₙ xₙ₊₁ = σ*`. **PROVED under ω-continuity** (§4).

Either way, **the fully-instantiated coordinate `σ*` is a fixed point of the resolution
operator, reached by climbing from `⊥`.** This is the precise sense in which "instantiation =
collapsing all `0`s" is a fixed-point computation — now a theorem about `resolve`, not an
analogy.

### 3.3 Existence without continuity (Bourbaki–Witt). **PROVED.**

Even dropping every assumption on `π` beyond inflationarity (§2.2, unconditional), `D` is
chain-complete (a dcpo, so every chain has a sup), so **Bourbaki–Witt** guarantees `r_π` has
a fixed point, and transfinite iteration from `⊥` reaches one. So a fully-resolved
coordinate **exists** for any policy; the chain `{xₙ}` reaches it in `≤ ω` steps when the
depth is finite, and transfinitely otherwise. **PROVED** (the bare existence needs only
inflationarity + chain-completeness).

---

## Part 4 — It is the *least* fixed point (Kleene), under a finitary consistent policy

To upgrade "a fixed point reached by the climb" to "**the least** fixed point `⊔ₙ r_πⁿ(⊥)`"
— the exact Kleene form both prior papers asserted — we use Equipment A6/A7.

### 4.1 `r_π` is ω-continuous on `D_π` under a finitary consistent policy. **PROVED on `D_π`.**

Call `π` **finitary** if each round it fills only the **finitely many** currently-exposed
slots, and the value of each slot depends only on a **finite** local context (its parent +
spectrum) — both true of `resolve`, which enumerates `scryResult.slots` (a finite list at
any finite configuration) and fills each from its local `GenerationSlot` (`index.ts:1354-1403`).

*Claim:* a consistent (§2.3) + finitary `π` makes `r_π : D_π → D_π` ω-continuous (all data
below lie in the Scott domain `D_π`, where `r_π` is monotone by Lemma R). *Proof.* Let
`y₀ ⊑ y₁ ⊑ …` be an ascending chain in `D_π` with sup `y = ⊔ₙ yₙ` (in `D_π`, which is closed
under directed sups, §2.3).
Monotonicity (§2.3) gives `⊔ₙ r_π(yₙ) ⊑ r_π(y)`. For the reverse: a commitment
`(s, value(s)) ∈ com(r_π(y)) \ com(y)` is the fill of a slot `s` exposed at `y`. Since the
exposed-slot relation is **finitary** (`s` is exposed at `y` iff a *finite* prefix of `y`'s
commitments — the path to `s`'s parent — is present **and** `s ∉ com(y)`, i.e. `s` is still
at `0`), and that finite prefix is already present in some `yₙ` (a finite set of commitments
in a directed/ascending union appears at a finite stage, Platform §4.4 compactness) — while
`s ∉ com(yₙ)` too, since `yₙ ⊑ y` and `s ∉ com(y)` — so `s` is exposed at that `yₙ`, giving
`(s, value(s)) ∈ com(r_π(yₙ))` (consistency: same `value(s)`). Hence every commitment of
`r_π(y)` is in some `r_π(yₙ)`, giving `r_π(y) ⊑ ⊔ₙ r_π(yₙ)`. So `r_π(⊔ₙ yₙ) = ⊔ₙ r_π(yₙ)`.
∎ (The load-bearing facts are *finitary exposure* — slot-exposure depends on a finite
prefix — and *compactness* of finite commitments, both established: the former from the
tree-local `GenerationSlot`, the latter from Platform §4.4.)

### 4.2 Kleene least fixed point — on `D_π`. **PROVED on `D_π` (finitary consistent `π`).**

`r_π : D_π → D_π` is then a monotone (Lemma R), ω-continuous (§4.1) self-map of the **Scott
domain `D_π`** (§2.3) with least element `⊥`. By **Kleene's theorem** — proved in Equipment
A7 for any such carrier, and `D_π` is one — `r_π` has a **least fixed point in `D_π`** given
by

> **`lfp_{D_π}(r_π) = ⊔ₙ r_πⁿ(⊥) = σ*`**  (the least fixed point *among π-coherent
> configurations*).

So the instantiation `σ*` (Part 3) is **the least fixed point of `r_π` on the π-coherent
domain `D_π`**, and it is the Kleene supremum of the finite-resolution climb — the precise
statement Platform §5 and Equipment A7 asserted as a remark, now proved about CB's `resolve`,
**scoped to `D_π`**. (Equivalently, since `D_π` is a pointed dcpo and `r_π` monotone,
**Pataraia's theorem** already gives a least fixed point in `D_π`; ω-continuity additionally
identifies it as the `ω`-supremum `⊔ₙ r_πⁿ(⊥)`.) The instantiation is *least within `D_π`*
because the climb starts at `⊥` and adds only forced commitments: any π-coherent fixed point
`z ∈ D_π` has `⊥ ⊑ z` and, by monotonicity on `D_π` (Lemma R), `r_πⁿ(⊥) ⊑ r_πⁿ(z) = z`, so
`σ* = ⊔ₙ r_πⁿ(⊥) ⊑ z`. ∎

**The scope is essential and honest.** `σ*` is **not** the least fixed point over all of `D`:
any totally-resolved coordinate is a fixed point of `r_π` (no exposed `0`s ⇒ `r_π` adds
nothing), including incoherent ones like the `s ↦ 5` configuration with `value(s)=2`, which
`σ*` is **not** below. Those spurious fixed points lie **outside `D_π`** (they commit a slot
to a non-`π` value) and outside the image of the climb; restricting to `D_π` excludes exactly
them, leaving `σ*` as the genuine least fixed point of the resolution dynamics. This
domain-restriction — not a mere policy condition — is what makes the Kleene identity true.

### 4.3 Status summary.

| Property of `r_π` | Domain / hypothesis | Status |
|---|---|---|
| inflationary `σ ⊑ r_π(σ)` | all of `D`, any `π` (append-only code) | **PROVED** |
| fixed point exists (Bourbaki–Witt) | all of `D`, inflationary only | **PROVED** |
| instantiation = the climb `{r_πⁿ(⊥)}` | all of `D`, any `π` | **PROVED** |
| `σ*` reached in finitely many rounds | finite-depth space | **PROVED** |
| `D_π` is a Scott domain, `r_π`-closed, contains the climb | consistent `π` | **PROVED** |
| monotone | **on `D_π`**, consistent `π` (false on `D`) | **PROVED on `D_π`** |
| ω-continuous | **on `D_π`**, consistent + finitary `π` | **PROVED on `D_π`** |
| `σ* = ⊔ₙ r_πⁿ(⊥)` = **least** fixed point (Kleene/Pataraia) | **on `D_π`**, consistent + finitary `π` (false on `D`) | **PROVED on `D_π`** |

---

## Part 5 — The boundary: what this does and does NOT establish

This theorem is about **the resolution operator on the carrier `D` we built.** Held hard:

- **PROVED:** Crystal Ball's `resolve`, for a fixed policy, is an **inflationary** (always)
  self-map of the Scott domain `D` — and **monotone + ω-continuous on the π-coherent Scott
  subdomain `D_π`** (consistent `π`); instantiation is its climb from `⊥`; the fully-resolved
  coordinate is its **least fixed point `⊔ₙ r_πⁿ(⊥)` on `D_π`** (finitary consistent `π`), or
  at least a Bourbaki–Witt fixed point on `D` (any `π`). "A decision/resolution is a climb to
  a fixed point" is thereby a theorem about the code, on the carrier `D` (with leastness on
  `D_π`).

- **NOT established (remains VISION — §9 of the architecture map):**
  1. **Reflexivity `D ≅ [D→D]`.** `r_π` is *a* self-map of `D`; this says nothing about `D`
     being isomorphic to its own function space (Scott's `D∞`). The reflexive-domain claim is
     untouched here and remains VISION.
  2. **`GNOSYS = fix(Φ)` of the *Sanctuary* domain with a continuous `Φ`.** Our `Φ` is the
     concrete `r_π` on the *coordinate* carrier, not an abstract `Φ` on a *Sanctuary* domain;
     the identification of CB's `D` with "the Sanctuary domain" and of `r_π` with the
     architecture's `Φ` is **not** proved. VISION.
  3. **Policy determinism.** `π` is supplied **externally** (an LLM/user via `fills`). The
     theorem fixes `π` to study dynamics; it does **not** claim the external policy source is
     deterministic or that the LLM realizes a *consistent/finitary* policy. Whether a given
     LLM run yields a consistent `π` (hence a monotone `r_π` and a *least* fixed point, vs.
     merely a Bourbaki–Witt fixed point) is an empirical property of the run, **OPEN**.

So the rigorous core of the "instantiation is a fixed point / a decision is a climb"
intuition is **PROVED on `D`**; the reflexive-domain and Sanctuary-`fix(Φ)` superstructure
is **VISION**; and the consistency/finitarity of any real LLM policy is **OPEN**. Marking
these apart is the point: the fixed-point *shape* of CB resolution is real and proved; the
grand identification it is meant to support is not, and this paper does not smuggle it in.

---

## Conclusion

**Verdict: PROVED (with explicit domain-restriction, conditional, and VISION boundaries).**
Reading CB's `resolve` (`index.ts:1336-1462`) — append-only, per-slot, completing when no
`0`s remain — the one-round resolution operator `r_π` is **inflationary unconditionally** on
the Scott domain `D` (Platform Theorem), so the instantiation process is the ascending climb
`⊥ ⊑ r_π(⊥) ⊑ r_π²(⊥) ⊑ …`, whose supremum is a **fixed point** for any policy
(Bourbaki–Witt), reached in finitely many rounds for a finite-depth space. To get *the least*
fixed point one must restrict to the **π-coherent subdomain `D_π`** — itself a Scott domain,
`r_π`-closed, containing `⊥` and the entire climb — on which (for a consistent, finitary `π`)
`r_π` is monotone and ω-continuous, so by Kleene/Pataraia (Equipment A7)
`σ* = ⊔ₙ r_πⁿ(⊥)` is the **least fixed point on `D_π`** (least among π-coherent
configurations). This domain restriction is essential and honest: over all of `D`, `σ*` is
**not** least (incoherent totally-resolved coordinates are also fixed points, excluded by
`D_π`). The result turns the prior papers' remark "instantiation = collapsing all `0`s =
⊔ₙ rⁿ(⊥)" into a theorem about the actual resolution operator — on the carrier we built,
scoped to `D_π` — while holding the line that the reflexive `D ≅ [D→D]`, the Sanctuary
`fix(Φ)`, and the determinism/consistency of any real LLM policy are **not** thereby
established (VISION / OPEN). The fixed-point *shape* of CB resolution is proved; its grand
identification is left where it honestly sits.
