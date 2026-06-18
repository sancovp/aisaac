# Does Crystal Ball's coordinate encoding abstractly instantiate a Scott domain?

**A proof by invariant deduction from what the encoding IS.**

---

## Abstract

**The construct.** Crystal Ball (CB) is a coordinate-ontology engine. Its central
construct is a coordinate *encoding*: a finite digit string, parsed level-by-level,
in which the digit `0` denotes a *superposition* (an unfilled position / a class slot
that knows its kind but not its value) and the digits `1`–`7` (with `9` as a `+7`
"wrap" and `8`/`88` as structural drill/close) denote a *committed selection* (an
instance value within a slot's spectrum of children). A space is a tree of nodes; a
coordinate names a path of selections through it; positions left at `0` are the
positions not yet resolved.

**The property.** "Crystal Ball's coordinate encoding abstractly instantiates a
**Scott domain**" — i.e. a *bounded-complete algebraic dcpo with a least element*:
a partial order that (1) has a least element ⊥, (2) is directed-complete (every
directed subset has a least upper bound), (3) is algebraic (every element is the
directed supremum of the compact elements below it), and (4) is bounded-complete
(every subset with an upper bound has a least upper bound).

**The verdict: PROVED.** The encoding's invariants — what a coordinate *is* and what
its resolution *does* — entail exactly the structure of a Scott domain. The carrier is
the set of all coordinates of a fixed space, partial and total, including the idealized
infinite (fully-resolved limit) coordinates; the order is the specialization order
that the `0`-vs-`1–7` semantics imposes (σ ⊑ τ iff τ commits a value at every position
σ commits, with the same value, and may additionally resolve positions σ left at `0`);
and under that order every Scott-domain axiom is an invariant deduction. The absence of
any `cbLeq()`/`lub()` function in the source is **not** an obstruction — that the order
is mathematics-over-the-coordinates rather than a runtime operation is precisely the
thesis (a decision *is* a DAG-on-time though nothing "computes the DAG"). No invariant
obstruction exists.

---

## Part 1 — What the construct IS (invariants mined from the code)

All facts below are about *what a coordinate is and what resolution does*; file:line
citations are for the facts, not for an audit of which functions exist.

### 1.1 A coordinate is a finite digit string parsed positionally; `0` = superposition, `1–7` = selection.

The header states the encoding directly: *"A COORDINATE is dot-separated segments
crossing between spaces … Each segment selects a node within its respective space …
`0` in any segment means superposition (not yet selected) … INSTANTIATION = collapsing
all 0s to specific selections"* (`index.ts:6-12`). The token grammar is implemented in
`parseCoordinate`: the digit `0` emits a `superposition` token (`index.ts:758-767`);
`1`–`7` emit a `select` token with a 1-based value (`index.ts:795-802`); `9` is a wrap
that adds `+7` to the accumulator (`index.ts:791-794`); `8`/`88` are structural
drill/close into/out of a selected node's produced sub-space (`index.ts:768-790`). The
digit semantics are documented at `index.ts:662-678`:

```
0     = SUPERPOSITION — spectrum not chosen
1-7   = EXACT SELECTION — primacy of childspace from parent
8     = DRILL ; 88 = CLOSE DRILL ; 9 = WRAP (+7)
```

**Invariant A (positional commitment).** A coordinate is a finite sequence of
*positions* (slots, separated by dots, each a token sequence). Each position is in
exactly one of two states: **uncommitted** (`0`/superposition) or **committed** to a
specific 1-based selection index (`1–7`, possibly wrap-extended). This is a *partial
function from positions to selection-indices*: `parseSlots` decodes every slot to either
`{isSuperposition: true, selectionIndex: 0}` or a concrete `selectionIndex ≥ 1`
(`kernel-v2.ts:88-110`).

### 1.2 The `0` ⇄ `1–7` duality is the class⇄instance duality, and it is in the encoding itself.

`0` does not mean "absent value"; it means *the kind/class is known, the value is not*.
The strata header: *"classOrInstance per the ENCODING (0=class/superposition-slot,
1-7=instance/filled)"* (`index.ts:40-43`). `buildUARL` reads the *coordinate digit* to
tag a node `class` (last segment `0`) vs `instance` (otherwise) (`index.ts:2468-2475`).
The `Y_LAYER_SEMANTICS` map carries `classOrInstance: 'class' | 'instance'` keyed to the
same `0`/`1–7` reading (`index.ts:2337-2381`). So a position at `0` *is a class-level
position* (least-specialized at that slot); committing it to `1–7` is *specialization*.

**Invariant B (commitment is specialization).** Replacing a position's `0` by a concrete
selection `1–7` is a monotone *increase in information / specialization*: it adds a
commitment and removes none. The all-`0` coordinate is the least-specialized object —
the kernel-v2/RKHS reading makes `0` "uniform over the spectrum," i.e. "any value"
(`kernel-v2.ts:6-9`, `kernel-v2.ts:135-143`), and the architecture note names the all-`0`
object the top type `CB_Entity` (the maximally-general class). Thus there is a *bottom of
information*: commit nothing anywhere.

### 1.3 Resolution *enumerates* a fixed abstract space — it does not change the carrier.

`scry` walks a coordinate against a space; a `superposition` (`0`) fans out to *all
children at that position* (`index.ts:935-1006`); a `select` descends into the chosen
child and, if more levels remain, into its produced space or its own children
(`index.ts:1009-1061`). `mine`/`computeMinePlane` *enumerate every valid coordinate path
through the fixed child tree* — *"Given one locked kernel, what are ALL the valid
coordinates?"* (`mine.ts:6-9`, `mine.ts:90-105`). `resolve` fills `0`s with provided
values and *commits them back* as new children when they did not already exist
(`index.ts:1336-1462`, esp. the append at `index.ts:1382-1396`).

**Invariant C (the carrier is fixed; running enumerates it).** The set of objects the
encoding ranges over — the carrier — is *the set of all coordinates of a space*. A
coordinate that "grows as it resolves" is enumerating elements of this fixed set, not
mutating the set; `resolve` appending a child is realizing a position that the abstract
domain already *contained as a possible commitment*. (This is exactly the prompt's
warning: a runtime structure that grows is enumerating a fixed abstract domain. The
carrier therefore includes the *limit/idealized* coordinates — the fully- and even
infinitely-resolved ones — even though no finite `resolve` call reaches an infinite one,
just as a decision-process instantiates the whole DAG, not only the nodes already
visited.)

### 1.4 Commitment is permanent and consistent (lock/freeze; no overwrite).

A committed slot is locked: `lockNode` commits a node's spectrum and is *idempotent —
"Already locked"* — it never un-commits (`index.ts:1655-1670`). The deserialize
invariant-repair encodes the same rule: *"if a node has children, it was defined.
Defined = locked"* (`index.ts:1599-1608`). `resolve` only ever *adds* a child when one
with that value does not already exist — it never replaces a committed value
(`index.ts:1377-1396`, `index.ts:1430-1438`). A coordinate's committed positions are
therefore *stable*: extension adds commitments, never alters or removes them.

**Invariant D (extension is conservative).** If τ extends σ, then τ agrees with σ on
every position σ committed; extension is "fill more `0`s," never "change a `1–7`." Two
coordinates are *consistent* iff they agree wherever both commit.

### 1.5 There is a notion of completeness / terminal boundary (the maximal elements).

`isKernelComplete` is true when every slotted node is locked (`index.ts:642-660`); the
EWS forward chain exposes `kernelComplete` and `heat` (`heat = computeSpaceHeat`,
the unfilled ratio, `index.ts:577-589`, `ews.ts:186-194`); a node may be `terminal` —
*"this level is the end of this view — the space changes beyond this point"*
(`index.ts:111`); the boundary computation reports `interior`/`frontier` and per-depth
`canExpand` (`ews.ts:225-291`); `mine` flags `Ш` (full coherence) when `frozenRatio ===
1.0` (`mine.ts:111-114`). So the structure distinguishes *not-yet-complete* objects from
*complete/terminal* objects: the complete objects are the ones with nothing left at `0`
within the view's boundary.

### 1.6 Each position has its own finite, ordered spectrum (slots are independent).

The kernel factors *per slot*: `K(x,y) = ∏_k K_k(x_k, y_k)` (`kernel-v2.ts:9`,
`kernel-v2.ts:150-217`); each slot has a spectrum (the parent's children) with a finite
size (`getSpectrumSizeAtLevel`, `kernel-v2.ts:223-256`), and `0` at a slot means "this
slot doesn't discriminate" — uniform over that slot's spectrum (`kernel-v2.ts:135-143`).
Positions are thus **independent coordinates of a product structure**: a configuration is
a choice (or non-choice `0`) at each position, and positions do not constrain each
other's *committability* (drilling opens a position's sub-space, but that only adds
positions; it never makes two sibling commitments mutually exclusive).

**Invariant E (product of independent per-position spectra).** The space of coordinates
of a fixed tree is (isomorphic to) a product over positions of "either uncommitted, or
one of finitely many committed values," where deeper positions become available once a
shallower position is committed (the tree/dependent-product shape). Crucially, *no
two positions' commitments are mutually exclusive* — you can always commit any
still-uncommitted position to any of its spectrum values regardless of what other
positions hold.

---

## Part 2 — The instantiated structure (carrier + order, deduced)

From Invariants A–E we read off, by abstract implication, the mathematical object the
encoding instantiates.

### 2.1 The carrier `D`.

Fix a space `S` (its tree of positions, each with its finite spectrum, possibly growing
deeper via drill). Define a **configuration** to be a partial assignment that maps each
*reachable* position to either ⊥ (uncommitted, the `0`) or one of that position's
spectrum values (a `1–7` selection), subject to the tree dependency: a position deeper
than position *p* is "reachable" only once *p* is committed (you can only drill into a
selected node). Let

> **D = the set of all such configurations of S, partial and total, including the
> idealized limit configurations (those that commit infinitely deep where the tree
> permits).**

By Invariant C this is the fixed abstract domain the runtime enumerates; by Invariant A
each element *is* a partial-commitment function; by Invariant B "⊥ everywhere" is a
legitimate element (the all-`0` coordinate, `CB_Entity`).

### 2.2 The order `⊑`.

Define, by Invariants B and D, the **specialization (information) order**:

> **σ ⊑ τ  ⇔  for every position p, if σ commits p to value v then τ commits p to the
> same value v.**

In words: τ extends σ by committing some of σ's `0`s to selections, and never disagreeing
with or undoing a commitment of σ. This is exactly "more-resolved extends less-resolved"
— the arrow the `0`→`1–7` semantics imposes (Invariant B) and the conservative-extension
fact makes well-defined (Invariant D). It is the **information ordering of partial
functions** (Kleene's order), restricted to assignments respecting the per-position
spectra and tree dependency.

This is the order the property is *about*. That the code contains no `cbLeq` function is
immaterial: `⊑` is entailed by what a coordinate *is* (a partial commitment) the same way
a decision's precedence DAG is entailed by what deciding is. We now prove the four
Scott-domain conditions of `(D, ⊑)`.

---

## Part 3 — Preliminaries (the property, defined self-containedly)

- A **partial order** `(D, ⊑)` is a set with a reflexive, antisymmetric, transitive
  relation.
- `⊥ ∈ D` is a **least element** if `⊥ ⊑ d` for all `d ∈ D`.
- A subset `A ⊆ D` is **directed** if it is nonempty and every two elements of `A` have an
  upper bound *in* `A`.
- `(D, ⊑)` is a **dcpo** (directed-complete partial order) if every directed `A ⊆ D` has a
  least upper bound `⊔A ∈ D`.
- `c ∈ D` is **compact** (finite) if whenever `c ⊑ ⊔A` for a directed `A`, then `c ⊑ a`
  for some `a ∈ A`. Write `K(D)` for the compact elements.
- `(D, ⊑)` is **algebraic** if for every `d`, the set `{c ∈ K(D) : c ⊑ d}` is directed
  and `d = ⊔ {c ∈ K(D) : c ⊑ d}`.
- `(D, ⊑)` is **bounded-complete** if every subset that has *some* upper bound has a
  *least* upper bound (equivalently, every pair with an upper bound has a join). Combined
  with a least element this is "every consistent set has a lub."
- A **Scott domain** is a bounded-complete algebraic dcpo with a least element.

---

## Part 4 — The proof, condition by condition

Throughout, a configuration σ is identified with its set of commitments
`com(σ) = {(p, v) : σ commits position p to value v}`. By Invariant E, a *set* C of
position→value pairs is a legitimate configuration iff it is **functional** (no position
appears with two different values) and **tree-respecting** (each committed deep position's
governing shallower position is also committed). Under this identification,
`σ ⊑ τ ⇔ com(σ) ⊆ com(τ)` (Section 2.2). The whole proof reduces to facts about such sets
under ⊆.

### 4.1 `(D, ⊑)` is a partial order.

`⊑` is `⊆` on the commitment-sets (Section 2.2), and `⊆` is reflexive, transitive, and
antisymmetric on sets. Antisymmetry: if `com(σ) ⊆ com(τ)` and `com(τ) ⊆ com(σ)` then the
commitment-sets are equal, hence σ and τ commit exactly the same positions to the same
values, hence are the same configuration. ∎ (Uses Invariants A, D: a configuration *is*
its commitment-set; extension is conservative so ⊑ really is ⊆.)

### 4.2 Least element ⊥.

Let `⊥ = ` the configuration with `com(⊥) = ∅` (every position uncommitted — the all-`0`
coordinate / `CB_Entity`, Invariant B). For any σ, `∅ ⊆ com(σ)`, so `⊥ ⊑ σ`. `⊥ ∈ D`
because the empty assignment is trivially functional and tree-respecting. ∎ (Uses
Invariant B: all-`0` is a genuine element and the least-specialized one.)

### 4.3 Directed-completeness (dcpo).

Let `A ⊆ D` be directed. Define `U = ⋃_{σ∈A} com(σ)` (the union of all commitment-sets).

*Claim: U is a legitimate configuration (i.e. `⊔A := U ∈ D`).*

- **Functional.** Suppose `(p, v) ∈ U` and `(p, w) ∈ U`. Then `(p,v) ∈ com(σ)` and
  `(p,w) ∈ com(σ')` for some σ, σ′ ∈ A. By directedness there is `ρ ∈ A` with `σ ⊑ ρ` and
  `σ′ ⊑ ρ`, so `com(σ) ⊆ com(ρ)` and `com(σ′) ⊆ com(ρ)`; thus `(p,v),(p,w) ∈ com(ρ)`.
  But `com(ρ)` is functional (ρ is a configuration), so `v = w`. Hence U is functional.
  *This is the load-bearing step, and it is supplied directly by Invariant D/E:* two
  configurations in a directed set never disagree on a committed position, because they
  have a common upper bound that commits each position to a single value (commitments are
  permanent and never overwritten, Invariant D; positions are independently committable,
  Invariant E — there is no constraint that could force a conflict).
- **Tree-respecting.** If `(p, v) ∈ U` for a deep position p, then `(p,v) ∈ com(σ)` for
  some σ ∈ A, and σ is tree-respecting, so σ commits p's governing shallower position q;
  hence `(q, ·) ∈ com(σ) ⊆ U`. So U is tree-respecting.

Therefore `U ∈ D`. And `U` is an upper bound of `A` (each `com(σ) ⊆ U`), and it is the
*least* one: any upper bound `τ` has `com(σ) ⊆ com(τ)` for all σ, so
`U = ⋃ com(σ) ⊆ com(τ)`, i.e. `U ⊑ τ`. Hence `⊔A = U` exists in D. ∎

(This `⊔` is the **slotwise/pointwise join** the prompt anticipates — the union of
commitments — and it *exists as the idealized object even when no finite coordinate names
it*: the directed union of finite coordinates can be an infinite/total coordinate, which
is exactly a limit element of the carrier per Invariant C. Nothing in the code needs to
"compute" U for U to be the lub; U is the abstract completion the enumeration approaches.)

### 4.4 Algebraicity.

**Compact elements = the finite configurations** (those committing only finitely many
positions). 

*The finite configurations are compact.* Let `c` be finite, `com(c) = {(p₁,v₁), …,
(pₙ,vₙ)}`, and suppose `c ⊑ ⊔A = U` for directed `A` (with `U = ⋃ com(σ)` as in 4.3). Each
`(pᵢ,vᵢ) ∈ U`, so each lies in some `com(σᵢ)`, σᵢ ∈ A. By directedness (finitely many σᵢ
have a common upper bound `ρ ∈ A`), `com(c) ⊆ com(ρ)`, i.e. `c ⊑ ρ ∈ A`. So `c` is
compact.

*Every element is the directed sup of the finite elements below it.* Fix any `d ∈ D`. Let
`B = {c ∈ K(D) : c ⊑ d}` be the finite configurations below `d` — equivalently, all
finite subsets of `com(d)` that are themselves tree-respecting (any finite "downward-
closed-enough" selection of d's commitments). 
- `B` is **directed**: it is nonempty (`⊥ ∈ B`), and for `c, c′ ∈ B`,
  `com(c) ∪ com(c′)` is a finite subset of `com(d)`, hence functional and (being a union
  of two tree-respecting subsets of the single tree-respecting `com(d)`) tree-respecting,
  so it is a member `c″ ∈ B` with `c ⊑ c″` and `c′ ⊑ c″`.
- `⊔B = d`: `⊔B = ⋃_{c∈B} com(c)`. Every `(p,v) ∈ com(d)` lies in the finite
  configuration consisting of `(p,v)` together with the (finite) chain of shallower
  governing commitments up to the root — that configuration is tree-respecting, finite,
  and ⊑ d, hence in `B`. So `com(d) ⊆ ⋃_{c∈B} com(c) ⊆ com(d)`, giving `⊔B = d`.

Both halves of algebraicity hold. ∎

(The finiteness here is exactly the encoding's: a *finitely-resolved* coordinate — one
with finitely many committed slots — is a compact element, and any element, including an
infinite limit coordinate, is the directed union of its finitely-resolved
approximations. This is the formal content of "resolution climbs from ⊥, fanning out the
`0`s, and the realized object is the limit of the finite climbs.")

### 4.5 Bounded-completeness.

Let `A ⊆ D` have *some* upper bound `τ` (so `com(σ) ⊆ com(τ)` for all σ ∈ A). Define
`U = ⋃_{σ∈A} com(σ)`. Then `U ⊆ com(τ)`, so:
- `U` is **functional** (a subset of the functional `com(τ)` cannot contain `(p,v),(p,w)`
  with `v≠w`);
- `U` is **tree-respecting** (each `(p,v) ∈ U` is in `com(τ)`, whose governing shallower
  commitment is in `com(τ)`; and that shallower commitment is in `com(σ)` for the σ that
  contributed `(p,v)`, because σ is tree-respecting, so it is in `U`).

Hence `U ∈ D`, `U` is an upper bound of `A`, and (as in 4.3) the least one: `⊔A = U`.
So every subset with an upper bound has a least upper bound. ∎

(Note the contrast with 4.3: there, *directedness* of A guaranteed U functional; here, the
*mere existence of a common upper bound* τ guarantees it — both routes use Invariant D/E,
that committed values are permanent, single-valued, and never in forced conflict, so any
consistent family of commitments unions to a configuration. This is precisely why the
structure is bounded-complete and not merely a dcpo.)

### 4.6 Assembling the verdict.

`(D, ⊑)` is a partial order (4.1) with least element ⊥ (4.2), is directed-complete (4.3),
algebraic with the finite/finitely-resolved configurations as its compact elements (4.4),
and bounded-complete (4.5). A bounded-complete algebraic dcpo with a least element **is a
Scott domain**. ∎

---

## Part 5 — On the operations (monotonicity, since the property's spirit invokes a climb)

The Scott-domain *axioms* are fully proved above and do not require any map. For
completeness — and to honor the prompt's "reason about what the operation does to the
structure as an invariant" — the encoding's resolution operation respects the order:

- **`resolve` is monotone and inflationary.** `resolve` fills `0`s with provided values
  and commits them, never altering an existing commitment (`index.ts:1336-1462`,
  append-only at `index.ts:1377-1396`, `index.ts:1430-1438`; lock is idempotent,
  `index.ts:1658`). So if `r` is one `resolve` step, `σ ⊑ r(σ)` (inflationary: it only
  adds commitments) and `σ ⊑ τ ⇒ r(σ) ⊑ r(τ)` when applied to the same slot (monotone:
  adding the same commitment to a larger configuration yields a larger configuration).
- **The full instantiation is a climb from ⊥.** *"INSTANTIATION = collapsing all 0s to
  specific selections"* (`index.ts:11`) is, in the order, the ascent from ⊥ through a
  directed chain of finite (compact) approximations whose lub (4.3) is the
  fully-instantiated coordinate — i.e. the realized object is `⊔ₙ rⁿ(⊥)`, the Kleene
  supremum of finite resolutions. This is the autorealization/“climb the gradient” shape
  realized as an actual directed sup in a Scott domain: the gradient is `⊑`, the climb is
  the directed set of finite resolutions, and the realized state is its least upper bound.

These are invariants of the operation (it adds commitments, never conflicts), not claims
about its type signature; they are not needed for the Scott-domain proof but show the
encoding's dynamics live *inside* the order it instantiates.

---

## Part 6 — Why there is no invariant obstruction (the only way to DISPROVE)

A DISPROVED verdict would require a *deducible contradiction in what the structure is* —
e.g. two configurations that must have a least upper bound but provably cannot. The
candidate obstructions, and why each fails:

1. **"Two configurations could disagree on a slot, so their join might not exist."** They
   cannot disagree *and* still have a common upper bound: a common upper bound would have
   to commit one slot to two distinct values, which Invariant A (a slot is a function to a
   single selection index) forbids. So a *bounded* (consistent) family never conflicts —
   exactly what 4.5 uses. Inconsistent families simply have no upper bound, which
   bounded-completeness does not require them to. No obstruction.
2. **"`resolve` grows the space, so the carrier is mutable — there's no fixed domain to be
   a dcpo."** This conflates the runtime variable with the abstract domain. By Invariant C
   (and `mine`'s explicit enumeration of a *fixed* tree, `mine.ts:6-9`), growth is
   *enumeration* of the fixed carrier D; appending a child realizes a commitment D already
   contained. No obstruction.
3. **"There is no `cbLeq`/`lub` function, so no order/dcpo."** Reification is irrelevant:
   the order is entailed by what a partial-commitment coordinate *is* (Invariant B/D), and
   the lub is the union of commitments (4.3/4.5), which *exists as an abstract object*
   independent of any code computing it — just as a crowd in formation instantiates a
   shape no one calculates. This is the thesis, not a gap.
4. **"Infinite coordinates are never reached, so dcpo limits don't exist."** The carrier
   *includes* the limit (idealized) coordinates by construction (Invariant C, Section
   2.1); a directed sup is one of those limits, and it exists as an element of D whether or
   not any finite run names it. No obstruction.

No invariant obstruction survives. The structure the encoding instantiates is a Scott
domain.

---

## Conclusion

**Verdict: PROVED.** Crystal Ball's coordinate encoding abstractly instantiates a Scott
domain. Reading only *what a coordinate is* (a partial commitment of positions: `0` =
uncommitted/class, `1–7` = a single committed selection/instance; commitments permanent,
single-valued, conservatively extended; positions independently committable over finite
spectra; the carrier the fixed set of all coordinates including idealized limits), the
specialization order `σ ⊑ τ ⇔ com(σ) ⊆ com(τ)` is forced, and under it the four
Scott-domain conditions follow by invariant deduction: it is a partial order (⊆ on
commitment-sets); ⊥ is the all-`0` coordinate; it is directed-complete with lub = union of
commitments (the slotwise join, which is functional precisely because a directed set's
members never overwrite each other); it is algebraic with the finitely-resolved
coordinates as the compact elements; and it is bounded-complete because any consistent
family of commitments unions to a configuration. The lack of an explicit order or
supremum function in the source is the thesis (the domain is mathematics over the
coordinates, not a runtime op), not an obstruction — and no genuine invariant obstruction
exists.
