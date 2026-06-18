# Crystal Ball's slot-orbit symmetry group acts on `D` by order-automorphisms

**A proof that Crystal Ball's canonical-fingerprint orbit structure is not merely an
equivalence-and-a-group but a genuine group of Scott-domain automorphisms of the
configuration domain — concretely realizing the architecture's `Aut` — with the
fingerprint as its complete invariant, and the full-automorphism and quotient-domain
questions left precisely OPEN.**

---

## Abstract

**The prior status.** The Equipment paper
(`cb_equipment_of_an_encoded_space.md`, item B5) established that each slot's spectrum
carries an **orbit equivalence** (children with identical subtree fingerprint) and a
**symmetry group** `∏_o S_{|o|}` per slot, with the **canonical fingerprint** (an
Aho–Hopcroft–Ullman tree canonical form) as the kernel ID — but it explicitly left as
**OPEN** whether this group is the *full* automorphism group of the configuration domain
`D`, treating only the structural invariant.

**This paper** upgrades B5's "an equivalence and a group exist" to a structural theorem:

1. **The action.** The slot-orbit group `G = ∏_{slots} ∏_{orbits} S_{|o|}` (read from
   `findSlotOrbits`, `kernel-v2.ts:348-413`) **acts on the configuration domain `D`** by
   permuting, within each slot, the selection indices of structurally-identical sibling
   subtrees. **PROVED.**
2. **By automorphisms.** Every `g ∈ G` is an **order-automorphism** of `(D, ⊑)` that is
   Scott-continuous and fixes `⊥` — so `G ≤ Aut(D, ⊑)`, a subgroup of the Scott-domain's
   automorphism group. This is the architecture's `Aut` realized concretely on the carrier
   we built. **PROVED.**
3. **The fingerprint is the complete invariant.** The canonical fingerprint
   (`subtreeFingerprint`, `kernel-v2.ts:317-335`) is a **complete invariant of the
   `G`-action on subtree shapes**: two committed subtrees have equal fingerprint **iff**
   they are related by a `G`-permutation. So the fingerprint map *is* the orbit-quotient
   projection on shapes. **PROVED.**
4. **The quotient.** `⊥` is the unique `G`-fixed least element, and the orbit space `D/G`
   is a **poset with least element `[⊥]`** and a **monotone surjection** `D ↠ D/G` — the
   "shape up to symmetry." **PROVED.**

**The honest OPENs (held throughout).** (i) Whether `G` is the **full** `Aut(D, ⊑)` —
i.e. whether *every* order-automorphism of `D` arises from slot-orbit permutations — is
**OPEN** (we prove only `G ≤ Aut(D)`). (ii) Whether the quotient `D/G` is itself a **Scott
domain** (directed-complete + algebraic, not merely a pointed poset) is **OPEN** (the
finite-group quotient-of-a-dcpo argument is not carried out here). (iii) The architecture's
§9 reading "`Aut(Sanctuary)` closes ⇒ programs Reality" is **VISION** and is not touched:
we identify a concrete `Aut` subgroup on `D`, not a closure condition on a Sanctuary domain.

---

## Part 0 — Preliminaries (self-contained; carrier reused)

Reuse the Platform Theorem's carrier: a **configuration** `σ` of a fixed CB space assigns
each reachable position either `⊥` (uncommitted, digit `0`) or a finite **selection index**
(a spectrum value, digit `1–7`); `com(σ)` = its `(position, value)` commitments;
`(D, ⊑)` is a **Scott domain** with `σ ⊑ τ ⇔ com(σ) ⊆ com(τ)`, `⊥ = ∅`, directed sups =
unions, compacts = finite configurations (Platform Theorem).

- A **group action** of `G` on a set `X` is a homomorphism `G → Sym(X)`; we write `g·x`.
- An **order-automorphism** of a poset `(P, ⊑)` is a bijection `f : P → P` with
  `x ⊑ y ⇔ f(x) ⊑ f(y)`. `Aut(P, ⊑)` = the group of these under composition.
- `f` is **Scott-continuous** if monotone and directed-sup-preserving; an order-
  automorphism whose inverse is also monotone automatically preserves all sups/infs it can.
- For `g ∈ Aut(P)` acting on `P`, the **orbit** of `x` is `G·x = {g·x : g ∈ G}`; the
  **orbit space** `P/G` is the set of orbits.

We first read the orbit structure from the code, then build the action and prove its
properties.

---

## Part 1 — What the orbit structure IS (mined from the code)

### 1.1 The canonical fingerprint is an AHU tree canonical form.

`subtreeFingerprint(space, nodeId)` (`kernel-v2.ts:317-335`) computes a string for the
subtree rooted at a node: it recursively fingerprints the children, **sorts** the child
fingerprints (so child *order* is irrelevant), and prepends semantic tags (stratum,
kernelRef) that "break equivalence even with same shape" (`kernel-v2.ts:321-334`). This is
the **Aho–Hopcroft–Ullman canonical form** for rooted trees, extended with semantic tags:
two subtrees get the **same fingerprint iff they are isomorphic as tagged rooted trees**
(the sort makes the canonical form invariant under reordering siblings; the recursion makes
it a complete shape invariant; the tags refine it).

**Invariant F (fingerprint = tagged-tree iso class).** `fingerprint(t₁) = fingerprint(t₂)`
iff `t₁` and `t₂` are isomorphic as rooted, sibling-unordered, tag-labelled trees.

### 1.2 An orbit is a set of spectrum values with identical subtree fingerprint.

`findSlotOrbits(parent, space, slotIndex)` (`kernel-v2.ts:348-413`) groups a parent node's
children (its **spectrum**, the slot's selectable values) by `subtreeFingerprint`: children
with the same fingerprint go in the same **orbit** (`kernel-v2.ts:367-386`). Within an
orbit, members are ordered by selection index ("primacy is a REFINEMENT within orbits, not
a breaking criterion", `kernel-v2.ts:345-346`). The **symmetry group** of the slot is named
`∏_{orbit} S_{|orbit|}` — a product of symmetric groups, one per nontrivial orbit, with
singleton orbits fixed (`kernel-v2.ts:388-395`).

**Invariant O (orbit = interchangeable selections).** Two selection indices `i, j` of one
slot are in the same orbit iff the subtrees they head have the same fingerprint, i.e. iff
they are **structurally interchangeable** (their committed subtrees are tagged-tree-iso).

### 1.3 The whole-space group.

`computeSpaceSlotSignature` (`kernel-v2.ts:417-428`) walks the space level by level and
records the per-slot orbits and the **total symmetry** `totalSymmetry = ∏_{slot} (slot
group)` (`kernel-v2.ts:78`), with `.canonical` = the whole-space fingerprint = the kernel ID
(`kernel-v2.ts:425`). So the space carries a single group

> **`G = ∏_{slots s} ∏_{orbits o of s} S_{|o|}`**,

the product over all slots of the per-slot orbit-symmetric-groups. We now make `G` act on
`D`.

---

## Part 2 — The action of `G` on `D`

### 2.1 The action is by space-tree automorphisms (positions are paths — transport them).

A **position** of a configuration is a *path*: a sequence of selections from the root (a
deep position literally encodes the shallow selections that reach it; reachability is exactly
tree-respecting, Platform Invariant E). So a symmetry cannot "keep a position fixed and
permute its value" — permuting a shallow selection moves the whole subtree beneath it. The
correct object is an **automorphism of the fixed space tree**.

**Definition (the induced tree automorphism).** Fix the space tree `T` (nodes = the
positions of the space; each node's children = its spectrum). For each node `n`, its factor
`G_n = ∏_{o orbit of n} S_{|o|}` (Part 1.2) supplies a permutation of `n`'s children that
moves each child only **within its orbit** (to a structurally-identical sibling). These
assemble into a single automorphism `φ_g : T → T` as follows: at the root apply the root's
permutation; recursively, having mapped a node `n` to `n' = φ_g(n)`, map each child `c` of
`n` (index `i`) to the child `c'` of `n'` at the permuted index, **and map `c`'s subtree
onto `c'`'s subtree by the canonical isomorphism** — which exists and is unique-enough
because `c` and `c'` are in the same orbit, hence have **identical fingerprint**, hence
**isomorphic tagged subtrees** (Invariants O, F), then continue the recursion inside using
that subtree's own per-node factors of `g`. `φ_g` is a **bijection of nodes preserving the
parent–child relation** (a tree automorphism): it is invertible (use `g⁻¹` slot-wise), and
it preserves ancestry because it is built level by level mapping children to children.

**Definition (the action on `D`).** For `σ ∈ D`, let `g·σ` be the **transport** of `σ`
along `φ_g`:

> `com(g·σ) = { (φ_g(p), φ_g\text{-image of the selection at } p) : (p, ·) ∈ com(σ) }`
> — i.e. `g·σ` assigns to node `φ_g(p)` exactly what `σ` assigned at `p`, read through the
> subtree isomorphism. Equivalently, `g·σ = σ ∘ φ_g^{-1}` as partial assignments of `T`.

This is well-defined:

- **`g·σ` is a legitimate configuration.** `φ_g` is a tree automorphism, so it carries
  reachable positions to reachable positions and the parent (governing-commitment) relation
  to itself; hence `g·σ` is **tree-respecting**, and it is **functional** because `φ_g` is a
  bijection on nodes (each image position receives one value). Uncommitted positions (`0`)
  map to uncommitted positions.
- **It is a group action.** `φ_e = id` so `e·σ = σ`; and `φ_{gh} = φ_g ∘ φ_h` (composing the
  level-by-level constructions, using `(g_n h_n) = g_n ∘ h_n`), so
  `(gh)·σ = σ ∘ φ_{gh}^{-1} = σ ∘ φ_h^{-1} ∘ φ_g^{-1} = g·(h·σ)`. So `G → Sym(D)`,
  `g ↦ (σ ↦ g·σ)`, is a homomorphism. ∎

**PROVED:** `G` acts on `D` by transport along space-tree automorphisms `φ_g`. Write
`Φ_g : D → D` for the resulting bijection `σ ↦ g·σ`, and `φ̂_g` for the induced bijection on
the universe of `(position, value)` pairs (so `com(g·σ) = φ̂_g(com(σ))`).

### 2.2 Each `g` is an order-automorphism. **PROVED.**

> **Theorem 1.** For every `g ∈ G`, the map `σ ↦ g·σ` is an order-automorphism of
> `(D, ⊑)`: a bijection with `σ ⊑ τ ⇔ g·σ ⊑ g·τ`.

*Proof.* **Bijection:** `g⁻¹ ∈ G` (slot-wise inverse) gives `Φ_{g⁻¹} = Φ_g^{-1}` (since
`φ_{g⁻¹} = φ_g^{-1}`), so `Φ_g` is invertible. **Order-preserving both ways:** by
construction `com(g·σ) = φ̂_g(com(σ))`, where `φ̂_g` is the bijection on the universe of all
`(position, value)` pairs induced by the tree automorphism `φ_g` (Part 2.1). For any
bijection `φ̂_g` of a universe, `A ⊆ B ⇔ φ̂_g(A) ⊆ φ̂_g(B)`. Hence

> `σ ⊑ τ ⇔ com(σ) ⊆ com(τ) ⇔ φ̂_g(com(σ)) ⊆ φ̂_g(com(τ)) ⇔ com(g·σ) ⊆ com(g·τ) ⇔ g·σ ⊑ g·τ`.

So `Φ_g` is an order-automorphism. ∎

### 2.3 Each `g` is Scott-continuous and fixes `⊥`. **PROVED.**

- **Fixes `⊥`.** `com(⊥) = ∅`, so `com(g·⊥) = φ̂_g(∅) = ∅`, i.e. `g·⊥ = ⊥`. Every `g` fixes
  the least element. ∎
- **Scott-continuous.** `Φ_g` is monotone (Theorem 1). For directed `A ⊆ D` with
  `⊔A = ⋃_{σ∈A} com(σ)` (Platform §4.3),
  `com(g·⊔A) = φ̂_g(⋃ com(σ)) = ⋃ φ̂_g(com(σ)) = ⋃ com(g·σ) = com(⊔ g·A)`
  (a bijection commutes with arbitrary unions), so `g·⊔A = ⊔(g·A)`. Hence `Φ_g` preserves
  directed sups; being also an order-automorphism it preserves the whole Scott structure.
  ∎

> **Corollary (the concrete `Aut`).** `G ≤ Aut(D, ⊑)`, and every element is a `⊥`-fixing
> Scott-continuous order-automorphism. Thus the architecture's `Aut(Domain)` (§3) is, for a
> CB-encoded space, **at least** the slot-orbit group `G`, acting on the configuration Scott
> domain by structure-preserving symmetries. **PROVED** (the "at least" is sharpened — or
> not — by the OPEN below).

---

## Part 3 — The fingerprint is the complete invariant of the action

### 3.1 Statement and proof. **PROVED.**

For a configuration `σ` and a committed position `p` (with `σ(p)` a selection heading a
realized subtree), write `fp_σ(p)` for the fingerprint of that realized subtree.

> **Theorem 2.** Two committed positions head subtrees with **equal fingerprint** iff they
> are related by a `G`-permutation; equivalently, the fingerprint map is **constant on
> `G`-orbits and separates distinct orbits**. Concretely: for selection indices `i, j` of a
> slot `s`, `fingerprint(subtree_i) = fingerprint(subtree_j)` ⇔ `∃ g_s ∈ G_s : g_s(i) = j`.

*Proof.* (⇐) If `g_s(i) = j` for some `g_s ∈ G_s`, then `i, j` lie in the **same orbit** of
`s` (the factors of `G_s` permute *only within orbits*, Part 2.1). By Invariant O, same
orbit ⇔ same subtree fingerprint, so `fingerprint(subtree_i) = fingerprint(subtree_j)`.
(⇒) If the fingerprints are equal, then by Invariant O `i, j` are in the same orbit `o`;
`G_s` contains the full symmetric group `S_{|o|}` on `o`'s indices (Part 1.2,
`kernel-v2.ts:393`), which acts transitively on `o`, so some `g_s ∈ G_s` sends `i ↦ j`. ∎

**Consequence.** The canonical fingerprint (`subtreeFingerprint`) is a **complete invariant**
of the `G`-action on subtree shapes: it is `G`-invariant (Theorem 2 ⇐) and `G`-separating
(Theorem 2 ⇒). Lifting position-wise to whole configurations, the whole-space fingerprint
(`.canonical`, the kernel ID) is invariant under `G` and identifies configurations up to the
`G`-action on each slot — i.e. **the fingerprint map is (a representative of) the orbit-
quotient projection on shapes.** This is exactly the EWS "backward chain = the symmetry/orbit
structure = the canonical fingerprint" (`ews.ts:5-6`, B5) made precise.

---

## Part 4 — The quotient `D/G`

### 4.1 `⊥` is the unique `G`-fixed least element; `D/G` is a pointed poset. **PROVED.**

> **Theorem 3.** `[⊥]` is the least element of the orbit space `D/G` under the quotient order
> `[σ] ≤ [τ] :⇔ ∃ g ∈ G : σ ⊑ g·τ`, and the projection `q : D → D/G`, `σ ↦ [σ]`, is a
> monotone surjection.

*Proof.* **Quotient order is a partial order.** `G` is **finite** (a product of finitely
many finite symmetric groups over the finitely many slots/orbits — a finite tree) and acts
by order-automorphisms (Theorem 1). For such an action the relation `[σ] ≤ [τ] :⇔ ∃ g: σ ⊑
g·τ` is:
- *reflexive* (`g = e`);
- *transitive*: `σ ⊑ g·τ` and `τ ⊑ h·ρ` give `σ ⊑ g·τ ⊑ g·(h·ρ) = (gh)·ρ` (Theorem 1
  monotone), so `[σ] ≤ [ρ]`;
- *antisymmetric*: suppose `σ ⊑ g·τ` and `τ ⊑ h·σ`. Then `σ ⊑ g·τ ⊑ g·(h·σ) = (gh)·σ`. Let
  `m = ord(gh) < ∞` (finite group). Iterating the order-automorphism `(gh)`:
  `σ ⊑ (gh)·σ ⊑ (gh)²·σ ⊑ … ⊑ (gh)^m·σ = e·σ = σ`, forcing equality throughout, so
  `σ = (gh)·σ` and hence `σ = g·τ` (from `σ ⊑ g·τ ⊑ (gh)·σ = σ`). Thus `τ = g⁻¹·σ`, i.e.
  `[τ] = [σ]`. ∎ (well-defined poset.)

**Least element.** For any `σ`, `⊥ ⊑ σ = e·σ`, so `[⊥] ≤ [σ]`; `[⊥]` is least. (And `[⊥] =
{⊥}` is a singleton orbit since every `g` fixes `⊥`, Part 2.3.) **Monotone surjection:** `q`
is onto by definition; `σ ⊑ τ ⇒ σ ⊑ e·τ ⇒ [σ] ≤ [τ]`, so `q` is monotone. ∎

So `D/G` is the **"shape-up-to-symmetry" poset**: configurations that differ only by
swapping structurally-identical selections collapse to one point, and the fingerprint
(Theorem 2) names that point.

### 4.2 What is NOT proved about `D/G`. **OPEN.**

Whether `D/G` is a **Scott domain** (directed-complete + algebraic, not merely a pointed
poset) is **OPEN**. A directed family of orbits need not lift to a directed family of
representatives, so directed-completeness of `D/G` is not immediate from `D`'s; the standard
route (a finite group acting by Scott-continuous automorphisms on a dcpo yields a dcpo
quotient, with compacts the orbits of compacts) is plausible but **not carried out here**.
We claim only the pointed-poset structure (Theorem 3). Marking this honestly: `D/G` is a
poset with least element and a monotone projection — its domain-theoretic completeness is a
separate open proposition.

---

## Part 5 — The boundary (what is OPEN / VISION)

- **`G = Aut(D, ⊑)`? — OPEN.** We proved `G ≤ Aut(D)` (Theorem 1 + Cor). The reverse — that
  *every* order-automorphism of `D` is a slot-orbit permutation — is **not** proved. Plausible
  obstructions: automorphisms permuting *positions* (not just selections within a slot), or
  cross-slot symmetries the per-slot `findSlotOrbits` does not see. Determining `Aut(D)`
  exactly (and whether the code's `G` equals it) is the open completion of Equipment B5.
- **`D/G` a Scott domain — OPEN** (Part 4.2).
- **"`Aut(Sanctuary)` closes ⇒ programs Reality" (§9) — VISION.** This paper exhibits a
  concrete automorphism group on the *coordinate* domain `D`. It does **not** identify `D`
  with a "Sanctuary domain," does not define or verify any "closure" condition on `Aut`, and
  does not establish the "programs Reality" consequence. Those remain VISION; nothing here
  depends on them.

---

## Conclusion

**Verdict: PROVED (with explicit OPEN/VISION boundaries).** Reading Crystal Ball's orbit and
fingerprint code (`findSlotOrbits` + `subtreeFingerprint`, `kernel-v2.ts:317-413`), the
slot-orbit group `G = ∏_{slots} ∏_{orbits} S_{|o|}` **acts on the configuration Scott domain
`D`** by permuting structurally-identical sibling selections (Part 2.1); every `g ∈ G` is a
`⊥`-fixing, Scott-continuous **order-automorphism** (Theorems 1, 2.3), so `G ≤ Aut(D, ⊑)` —
the architecture's `Aut` realized concretely on the carrier we built. The canonical
fingerprint is the **complete invariant** of this action (Theorem 2): equal fingerprint ⇔
`G`-related, so the fingerprint map is the orbit-quotient projection on shapes. The orbit
space `D/G` is a **pointed poset** with least element `[⊥]` and a monotone surjection from
`D` (Theorem 3) — the shape-up-to-symmetry quotient. Held honestly OPEN: whether `G` is the
*full* `Aut(D)`, and whether `D/G` is itself a Scott domain; held as VISION: the §9
"`Aut` closes ⇒ programs" reading, which is untouched. The orbit symmetry is thereby
promoted from "an equivalence and a group" (B5) to a proved group of Scott-domain
automorphisms with a complete fingerprint invariant — the rigorous core of CB's `Aut`,
without the unproven superstructure.
