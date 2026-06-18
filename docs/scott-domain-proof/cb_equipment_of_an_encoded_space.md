# The Equipment of a Crystal Ball–Encoded Space

**A catalogue, with proofs, of the mathematical structure a CB-encoded space
provably carries — in two layers: what is free from the Scott-domain property,
and what is specific to Crystal Ball's code.**

---

## Abstract

**The standing result.** A companion paper — *"Does Crystal Ball's coordinate
encoding abstractly instantiate a Scott domain?"*
(`cb_encoding_is_a_scott_domain.md`, hereafter **the Platform Theorem**) — proves
that the carrier `D` of all coordinates of a fixed Crystal Ball (CB) space, ordered
by the specialization order `σ ⊑ τ ⇔ com(σ) ⊆ com(τ)`, is a **Scott domain**: a
bounded-complete algebraic dcpo with a least element. That proof is conducted on
the **syntactic carrier** — the configurations constrained only to be *functional*
(no position holds two values) and *tree-respecting* (a deep position's governing
shallower position is committed). The Platform Theorem explicitly scopes itself to
that carrier and leaves OPEN whether the externally-validated subspace
`D_consistent ⊆ D` (the configurations an out-of-process `youknow()` reasoner
accepts) is itself a Scott domain.

**This paper.** Taking the Platform Theorem as given, we **catalogue the equipment**
the encoding thereby carries, item by item, each marked **PROVED** (deduced here or
in the Platform Theorem), **OPEN** (a precisely-stated unproven proposition),
**CONDITIONAL** (proved under an explicitly-named restriction, false/unknown without
it), **PROVED-conditional** (proved given a stated side-condition the construction
guarantees), or **VISION** (a stated aspiration with no proof). We separate two layers:

- **Layer A — free equipment.** Structure that *any* Scott domain carries; we derive
  each item as a consequence of the Platform Theorem's four axioms, define every
  notion self-containedly, and state its transfer status to `D_consistent`.
- **Layer B — CB-specific equipment.** Structure carried by the *particular* encoding,
  read from the code (`lib/crystal-ball/`, citations `file:line`) and proved-or-opened:
  the real-line address `coordToReal` and its decodability lemma; the class/instance
  specialization; drill/bloom dependent sub-spaces; the product kernel as a similarity
  layer; the canonical fingerprint / orbit quotient as symmetry structure; the EWS
  boundary / `kernelComplete` as maximal elements; and `heat` as a definedness grading.

**Scope, held throughout.** Every Layer-A item is proved **on the syntactic carrier
`D`**. The items whose proof *uses bounded-completeness* (bounded joins, the function
space `[D→D]` being a Scott domain, closure under products/sums preserving
bounded-completeness) **inherit OPEN on `D_consistent`**, because an external
admissibility predicate that is not downward-closed can destroy bounded-completeness
(Platform Theorem §7). We mark each transfer explicitly and never assert across the
boundary.

---

## Part 0 — Preliminaries (every notion defined; self-contained)

We reproduce the definitions the catalogue uses so the paper verifies with no outside
context.

- A **partial order** `(D, ⊑)` is a set with a reflexive, antisymmetric, transitive
  relation.
- `⊥ ∈ D` is a **least element** if `⊥ ⊑ d` for all `d`.
- `A ⊆ D` is **directed** if nonempty and any two of its elements have an upper bound
  *in* `A`. `(D,⊑)` is a **dcpo** if every directed `A` has a least upper bound `⊔A`.
- `c ∈ D` is **compact** (finite) if for every directed `A` with `c ⊑ ⊔A`, already
  `c ⊑ a` for some `a ∈ A`. `K(D)` = the compacts.
- `(D,⊑)` is **algebraic** if every `d = ⊔{c ∈ K(D) : c ⊑ d}` and that set is directed.
- `(D,⊑)` is **bounded-complete** if every subset with an upper bound has a *least*
  upper bound (equivalently: every pair with an upper bound has a join).
- A **Scott domain** = a bounded-complete algebraic dcpo with `⊥`.
- The **way-below** relation: `x ≪ y` iff for every directed `A` with `y ⊑ ⊔A`, already
  `x ⊑ a` for some `a ∈ A`. (So `c` is compact iff `c ≪ c`.)
- A set `U ⊆ D` is **Scott-open** if (i) it is upward-closed (`x ∈ U, x ⊑ y ⇒ y ∈ U`)
  and (ii) inaccessible by directed sups (`⊔A ∈ U ⇒ A ∩ U ≠ ∅` for directed `A`). The
  **Scott topology** is the collection of Scott-open sets.
- A map `f : D → E` between dcpos is **Scott-continuous** iff monotone and
  directed-sup-preserving: `f(⊔A) = ⊔ f(A)` for directed `A` (equivalently, continuous
  for the Scott topologies).
- `[D→E]` = the set of Scott-continuous maps, ordered pointwise (`f ⊑ g` iff
  `f(x) ⊑ g(x)` for all `x`).
- For `f : D → D` on a dcpo with `⊥`, a **fixed point** is `x` with `f(x)=x`; the
  **least fixed point** `lfp(f)` is the ⊑-least such.

We recall the carrier and order from the Platform Theorem (its §2): a **configuration**
`σ` is a partial assignment of *reachable* positions of a fixed space `S` to either ⊥
(uncommitted, the digit `0`) or one of that position's finite spectrum values (a digit
`1–7` selection); `com(σ)` is its set of `(position, value)` commitments;
`D` = all configurations (partial, total, and idealized infinite limits);
`σ ⊑ τ ⇔ com(σ) ⊆ com(τ)`. The Platform Theorem proves `(D,⊑)` is a Scott domain with
`⊥ = ∅` (the all-`0` coordinate), `⊔` = union of commitments, and `K(D)` = the finite
(finitely-committed) configurations.

---

## Part A — Free equipment (consequences of the Platform Theorem)

Each item is a property the Platform Theorem's structure carries *because it is a Scott
domain*. We give the derivation, then the transfer status to `D_consistent`.

### A1. Least element and information order. **PROVED.**

`⊥ = ∅` (no position committed) satisfies `⊥ ⊑ σ` for all `σ` because `∅ ⊆ com(σ)`
(Platform §4.2). The order `⊑` is `⊆` on commitment-sets, a partial order (Platform
§4.1). This is the **information / specialization order**: `σ ⊑ τ` means τ commits
everything σ does (and possibly more) — "more resolved extends less resolved." Free,
identically, from the Platform Theorem.

*Transfer to `D_consistent`.* `⊥ = ∅` is admissible iff the all-`0` coordinate is
accepted by the reasoner; the encoding tags it `CB_Entity`, the top type
(Platform §1.2), and the per-node validator is fed one node at a time
(`engine.ts:1205-1208`), so the empty configuration raises no joint constraint. Thus
`⊥ ∈ D_consistent` is **PROVED-conditional** on the reasoner accepting the all-class
coordinate (it does, by construction of the per-node query); the order restricts to
`D_consistent` as a sub-poset unconditionally (a subset of a poset is a poset).

### A2. Directed limits (dcpo). **PROVED on `D`; OPEN on `D_consistent`.**

Every directed `A ⊆ D` has `⊔A = ⋃_{σ∈A} com(σ)`, which is a legitimate configuration
because directedness forces the union functional and tree-respecting (Platform §4.3).
So define-by-limit is available: an ascending family of partial resolutions has a
genuine least upper bound, including the idealized infinite ones.

*Transfer.* On `D_consistent`, `⊔A` is the same union, but its **admissibility is not
guaranteed**: a reasoner that inspects joint configurations may reject the union even
when every finite member is admissible. So directed-completeness of `D_consistent`
requires the admissibility predicate to be **closed under directed unions** — an OPEN
condition (it is the dcpo half of the separate "is `D_consistent` a Scott domain"
proposition). **OPEN on `D_consistent`.**

### A3. A basis of compact (finitely-resolved) elements + algebraicity. **PROVED on `D`.**

`K(D)` = the **finite** configurations — those committing only finitely many positions
(Platform §4.4). Two facts hold: (i) each finite configuration is compact; (ii) every
`d` is the directed sup of the finite configurations below it,
`d = ⊔{c ∈ K(D) : c ⊑ d}`. So the finitely-resolved coordinates form a **basis**: every
object, including an infinite limit coordinate, is approximated from below by its finite
truncations, and the climb of finite resolutions reaches it in the limit. This is the
formal content of "resolution climbs from `⊥`, fanning out the `0`s."

*Transfer.* Compactness is defined via directed sups, so it presupposes A2. On
`D_consistent`, algebraicity additionally requires that the admissible finite
approximants below an admissible `d` be (a) admissible themselves and (b) directed
within `D_consistent` — i.e. the admissibility predicate **downward-closed enough** that
truncating commitments preserves admissibility. **OPEN on `D_consistent`** (inherits the
downward-closure condition).

### A4. Way-below `≪` and the Scott topology. **PROVED on `D`.**

In any algebraic dcpo the way-below relation is determined by the compacts: for the
configurations,

> `x ≪ y` **iff** there is a finite configuration `c ∈ K(D)` with `x ⊑ c ⊑ y`,

and in particular **`c ≪ c` exactly for the finite configurations** (so "compact" and
"way-below-itself" coincide, as required). We prove the displayed characterization. (⇐)
If `x ⊑ c ⊑ y` with `c` finite and `y ⊑ ⊔A` for directed `A`, then `c ⊑ ⊔A`; by
compactness of `c` (A3) `c ⊑ a` for some `a ∈ A`, hence `x ⊑ c ⊑ a`. So `x ≪ y`. (⇒) If
`x ≪ y`, then since `y = ⊔{c ∈ K(D): c ⊑ y}` is a directed sup (A3) and `y ⊑ y`, the
way-below definition gives `x ⊑ c` for some finite `c ⊑ y`; that `c` witnesses
`x ⊑ c ⊑ y`. ∎ The **interpolation property** `x ≪ y ⇒ ∃ c (x ≪ c ≪ y)` follows: take
the finite `c` from `x ⊑ c ⊑ y`; `c` is compact so `c ≪ c`, and `x ⊑ c` gives `x ≪ c`,
and `c ⊑ y` gives `c ≪ y`. Hence `D` is a **continuous** (indeed algebraic) domain.

The **Scott topology** is then well-defined (Part 0): its basic opens are the
**principal up-sets of compacts** `↑c = {d : c ⊑ d}` for `c ∈ K(D)` — each is Scott-open
(upward-closed by transitivity; inaccessible because `c ⊑ ⊔A ⇒ c ⊑ a ∈ A` by
compactness), and they form a basis because `d ∈ U` Scott-open implies (by algebraicity
+ inaccessibility) some compact `c ⊑ d` has `c ∈ U`, so `d ∈ ↑c ⊆ U`. Concretely, a
basic Scott-open neighbourhood of a configuration is "all configurations that commit at
least this finite set of positions to these values." This is the topology in which
`resolve` is continuous (A7 / Platform §5).

*Transfer.* `≪` and the Scott topology are defined from `⊑` and directed sups, so they
restrict to `D_consistent` as the subspace structure; their *algebraic* characterization
(basis of compacts) inherits A3's downward-closure condition. **PROVED on `D`; the
algebraic-basis form is OPEN on `D_consistent`.**

### A5. Bounded-complete joins (consistent partials combine). **PROVED on `D`; OPEN on `D_consistent`.**

Any family `A ⊆ D` with *some* upper bound `τ` has a least upper bound `⊔A = ⋃ com(σ)`
(Platform §4.5): boundedness forces the union functional (a subset of the functional
`com(τ)`), hence a configuration. So **any consistent set of partial commitments
combines into a single configuration** — the join of compatible partial knowledge. With
`⊥` (A1), `D` is bounded-complete; equivalently it has all *finite* meets of bounded
families and is a **bounded-complete domain** (a Scott domain).

*Transfer.* This is the **load-bearing item the boundary is about.** On `D_consistent`,
two admissible configurations σ, τ may have an admissible common upper bound (so they are
"bounded" inside `D_consistent`) while their union `σ ⊔ τ` is **inadmissible** — an
external reasoner can couple positions the encoding never couples (Platform §7). Then the
bounded pair has *no least upper bound inside `D_consistent`*, and bounded-completeness
**fails**. So bounded-completeness transfers **iff** the admissibility predicate is
closed under bounded joins (downward-closed admissibility suffices). **OPEN on
`D_consistent`** — this is precisely the separate proposition the Platform Theorem flags.

### A6. The function space `[D→D]` is itself a Scott domain. **PROVED on `D` (classical); OPEN on `D_consistent`.**

This is a classical theorem of domain theory, which we state and justify for `D`. Order
`[D→D]` pointwise. Then:

- **`[D→D]` is a dcpo with `⊥`.** The constant map `x ↦ ⊥` is least. A directed family
  `F ⊆ [D→D]` has pointwise sup `(⊔F)(x) := ⊔_{f∈F} f(x)` (each `{f(x)}` is directed in
  `D` because `F` is directed and evaluation is monotone, so the sup exists by A2). This
  pointwise sup is itself Scott-continuous: for directed `B ⊆ D`,
  `(⊔F)(⊔B) = ⊔_{f} f(⊔B) = ⊔_{f} ⊔_{b} f(b) = ⊔_{b} ⊔_{f} f(b) = ⊔_{b} (⊔F)(b)`, where
  the middle equality is the **interchange of two directed sups** — valid in any dcpo
  because the doubly-indexed family `{f(b)}_{f∈F, b∈B}` is directed (both `F` and `B` are
  directed and `f`-evaluation is monotone), so both iterated sups equal the single sup of
  the joint family. And `⊔F` is the least pointwise upper bound by construction. So
  `[D→D]` is a dcpo with least element.
- **Compacts and algebraicity.** Because `D` is a **bounded-complete algebraic** dcpo,
  the **step functions** `(c ↘ e)` — sending `x` to `e` if `c ⊑ x` and to `⊥` otherwise,
  for compact `c,e ∈ K(D)` — are Scott-continuous: the up-set `↑c = {x : c ⊑ x}` is
  Scott-open (A4), so for directed `B`, if `c ⊑ ⊔B` then `c ⊑ b` for some `b ∈ B` (by
  compactness of `c`, A3), giving `(c↘e)(⊔B) = e = ⊔_{b}(c↘e)(b)`, and if `c ⋢ ⊔B` then
  `c ⋢ b` for all `b` and both sides are `⊥`; monotonicity is immediate. Every
  Scott-continuous `f` is the directed sup of the finite suprema of step functions below
  it (a standard fact for algebraic `D`: for each compact `c` and each compact
  `e ⊑ f(c)`, `(c↘e) ⊑ f`, and these step functions' directed joins recover `f` pointwise
  by algebraicity of `D` applied to each `f(c)`). The joinable finite families of step
  functions are the compacts of `[D→D]`; bounded-completeness of `D` is exactly what makes
  a *bounded* family of step functions have a least upper bound that is again continuous.
  Hence `[D→D]` is algebraic and bounded-complete. ∎ (This reproduces, for our `D`, the
  classical theorem that the category **BCD** of bounded-complete algebraic dcpos and
  Scott-continuous maps is cartesian closed — Scott 1972; Plotkin, *Pisa Notes on Domains*
  — so the exponential `[D→D]` is again an object of **BCD**; we use only that `D` is such
  an object.)

The dependence on **bounded-completeness of `D`** is essential and is the reason this
item is **A5-conditioned**: it is the bounded-completeness of `D` that makes joins of
step functions land back in `[D→D]`.

*Transfer.* Because the construction uses bounded-completeness and algebraicity of the
base, it **inherits A3+A5's OPEN status on `D_consistent`**: if `D_consistent` is not
bounded-complete, `[D_consistent → D_consistent]` need not be a Scott domain. **PROVED on
`D`; OPEN on `D_consistent`.** (This item is what makes the Kleene/`fix` theory of A7
available — it is the carrier in which higher-order CB transformations live.)

### A7. Least fixed points (Kleene `lfp = ⊔ₙ fⁿ(⊥)`) — define-by-recursion / the convergent climb. **PROVED on `D`.**

**Kleene fixed-point theorem (for `D`).** Let `f : D → D` be Scott-continuous. Then `f`
has a least fixed point, given by `lfp(f) = ⊔_{n≥0} fⁿ(⊥)`.

*Proof.* `⊥ ⊑ f(⊥)` since `⊥` is least; applying the monotone `f` repeatedly,
`fⁿ(⊥) ⊑ f^{n+1}(⊥)`, so `{fⁿ(⊥)}_{n≥0}` is an ascending chain, hence directed; by A2
its sup `μ := ⊔ₙ fⁿ(⊥)` exists in `D`. By Scott-continuity,
`f(μ) = f(⊔ₙ fⁿ(⊥)) = ⊔ₙ f(fⁿ(⊥)) = ⊔ₙ f^{n+1}(⊥) = μ` (the last step drops the `n=0`
term `⊥`, which does not change the sup). So `μ` is a fixed point. If `x = f(x)` is any
fixed point, then `⊥ ⊑ x` and monotonicity give `fⁿ(⊥) ⊑ fⁿ(x) = x` for all `n`, so
`μ = ⊔ₙ fⁿ(⊥) ⊑ x`. Hence `μ` is least. ∎

This equips CB with **define-by-recursion**: any Scott-continuous self-map (the carrier
of which is supplied by A6) has a canonical solution computed by the convergent climb
from `⊥`. The Platform Theorem (§5) already exhibits the *instantiation* operation as
exactly such a climb — `resolve` is monotone and inflationary (`index.ts:1336-1462`,
append-only `index.ts:1377-1396,1430-1438`, idempotent lock `index.ts:1658`), and full
instantiation is `⊔ₙ rⁿ(⊥)`, the Kleene supremum of finite resolutions
(`index.ts:11`). So A7 is not only free structure but the structure CB's own
"collapsing all `0`s" dynamics realizes.

*Transfer.* Kleene's theorem needs only **dcpo + `⊥` + Scott-continuity of `f`**, so it
holds on any sub-dcpo of `D` that contains `⊥` and is closed under `f` — including
`D_consistent` **if** A2 holds there (A2's OPEN condition) and `f` preserves
admissibility. **PROVED on `D`; conditional on A2 for `D_consistent`.**

### A8. Closure under products and sums. **PROVED on `D` (classical); products PROVED, sums PROVED; OPEN on `D_consistent`.**

Scott domains are closed under the standard constructions, which equip CB-encoded spaces
with composite carriers:

- **Product.** `D₁ × D₂` ordered coordinatewise is a Scott domain: `⊥ = (⊥₁,⊥₂)`;
  directed sups, compacts (`(c₁,c₂)` with each `cᵢ` compact), algebraicity, and
  bounded-completeness all compute coordinatewise. *This is exactly the multi-space CB
  configuration:* a coordinate spanning two independent spaces is a pair of
  configurations, and the Platform Theorem's product structure (the configuration count
  is the full product `∏` of per-position spectra, `mine.ts:733`) is this categorical
  product realized inside one space. **PROVED.**
- **Separated sum** `D₁ ⊕ D₂` (disjoint union with a fresh least element) is a Scott
  domain by the same coordinatewise checks restricted to each summand, the new `⊥` below
  both. This models a coordinate that selects *which* space before resolving within it
  (a top-level `select` choosing a child whose produced space is one of several).
  **PROVED.**

*Transfer.* Both constructions preserve the Scott-domain axioms by computing them
factor-wise; on `D_consistent` they preserve only those axioms that hold on each factor,
so the product/sum is a Scott domain **iff each `D_consistent` factor is** — inheriting
A2/A3/A5's OPEN status. **PROVED on `D`; OPEN on `D_consistent`.**

> **Layer-A summary.** On the **syntactic carrier `D`**, a CB-encoded space is fully
> equipped: `⊥` + information order (A1), directed limits (A2), a compact basis +
> algebraicity (A3), way-below + the Scott topology (A4), bounded-complete joins (A5),
> a Scott-domain function space `[D→D]` (A6), Kleene least fixed points (A7), and closure
> under products/sums (A8). On `D_consistent`, the **order, `⊥`, `≪`/Scott-topology as
> raw subspace structure** restrict unconditionally, but every item whose proof uses
> **directed-completeness or bounded-completeness** (A2, A3, A5, A6, A8, and A7 via A2)
> **inherits OPEN**, gated on the external admissibility predicate being closed under the
> relevant sups (downward-closed admissibility being the clean sufficient condition).

---

## Part B — CB-specific equipment (read from the code, proved-or-opened)

Layer A is what *any* Scott domain carries. Layer B is what *this* encoding carries by
virtue of its particular construction. Each item cites `lib/crystal-ball/` `file:line`
for facts about the code and is marked PROVED / OPEN / VISION.

### B1. The real-line address `coordToReal`, and the decodability lemma. **PROVED (scoped); OPEN (unrestricted injectivity).**

**The fact.** `coordToReal(c)` returns `parseFloat("0." + encodeDot(c))`, where
`encodeDot` replaces every dot by the digit string `8988`
(`index.ts:842-846`, `index.ts:831-834`); `coordToReal("root") = 0`. So a coordinate is
addressed by reading its digits (with dots rewritten to `8988`) as the fractional part
of a base-10 real in `[0,1)`.

**Claim (addressing, scoped).** On the **canonical subspace** `D_canon ⊆ D` defined
below, `coordToReal` is an **injective, order-respecting address** into `[0,1)`: distinct
canonical coordinates get distinct reals, and the embedding respects the *prefix* growth
of resolution.

**The decodability lemma (the delimiter argument), stated honestly.** The dot is encoded
as `8988`, and three digit strings are designated structural delimiters — `DOT = 8988`,
`KERNEL_OPEN = 90`, `KERNEL_CLOSE = 900` (`index.ts:820-828`) — with the *intent*, stated
in the code comment, that they are "impossible token sequences": a wrap (`9`, meaning
`+7`) must be followed by a *selection* `1–7`, not by a superposition `0` or a close, so
`90`, `900`, and the `…9·88` of `8988` "cannot" be emitted by the selection grammar.
**However, the tokenizer does not enforce this intent.** On encountering `0`, `8`/`88`,
or end-of-part with a nonzero wrap accumulator, it **flushes the dangling wrap as a
selection** (`index.ts:761-765`, `index.ts:770-774`, `index.ts:805-810`). Consequently
the digit string `8988` *does* parse — as `drill, select(7), close_drill` — and `90`,
`900` likewise parse (as `superposition` preceded by a flushed `select(7)`). So the
"impossible sequences" are impossible only *semantically* (a well-formed coordinate would
not write them), not *syntactically*; the parser accepts them. The decoder
`decodeDot(s) = s.split("8988").join(".")` (`index.ts:837-838`) therefore round-trips
**only** on coordinates whose parts contain no literal `8988`; a coordinate part that
literally spells `8988` would be mis-split into a spurious dot.

**Definition (`D_canon`).** Let `D_canon` = the configurations whose canonical digit
string (i) contains the substring `8988` **only** at genuine dot boundaries, and (ii) is
**trailing-superposition-normalized** (no trailing `0` digits — a trailing uncommitted
slot is dropped). On `D_canon`:

- *Injectivity.* `encodeDot` is a bijection between dotted coordinate strings and their
  delimiter-rewritten digit strings *when no part contains a raw `8988`* (condition (i)),
  so `decodeDot∘encodeDot = id` there; and `parseFloat("0."+·)` is injective on digit
  strings with **no trailing zeros** (condition (ii)) and no leading-zero ambiguity
  (the fractional reading fixes place value). Hence `c ↦ coordToReal(c)` is injective on
  `D_canon`. **PROVED.**
- *Why trailing-`0` is normalization, not loss.* `coordToReal("1") = 0.1 =
  coordToReal("10")` because `parseFloat` drops the trailing zero. But `"1"` and `"10"`
  denote the **same configuration**: `"10"` commits position 1 to value 1 and leaves
  position 2 at superposition (`0` = uncommitted), which in `⊑` is *the same element* as
  committing position 1 and saying nothing about position 2 (a trailing uncommitted slot
  adds no commitment). So the parseFloat coincidence **identifies equal elements** — a
  degeneracy, not a collision (this is the Platform §3.6 referee point). **PROVED.**
- *Order respect (prefix monotonicity).* If `σ ⊑ τ` by τ committing *additional deeper*
  positions (appending digits to σ's canonical string), then `coordToReal(τ)` extends
  `coordToReal(σ)`'s decimal expansion to the right, so the two reals share a prefix and
  the embedding tracks resolution depth. It is **NOT** a full order-isomorphism: `⊑` is a
  *partial* order while `<` on `[0,1)` is total, and committing a *shallower* position to
  a larger selection can move the real either way. So `coordToReal` is a **faithful
  address (injective code), not an order-embedding** (Platform §3.6, confirmed). **PROVED
  (as an address); the only-prefix-monotone caveat is explicit.**

**OPEN.** Unrestricted injectivity of `coordToReal` on *all* of `D` is **false** as a
literal statement of the code (the `8988`-in-a-part and trailing-`0` cases above), and a
*clean* canonicalization theorem — "every configuration has a unique `D_canon`
representative, and `coordToReal` is injective on representatives" — is **OPEN**: it
requires proving the normalizer (avoid raw `8988`; strip trailing `0`) is well-defined
and total on `D`. We have proved injectivity *on* `D_canon`; that `D_canon` is a faithful
set of representatives for all of `D` is the open completion.

### B2. Class/instance specialization (the `0 ⇄ 1–7` duality). **PROVED.**

The encoding carries the class/instance distinction *in the digit itself*: a position at
`0` is a **class-level** slot ("kind known, value not"), a position at `1–7` is an
**instance** (a committed value) (`index.ts:40-43`, `index.ts:2468-2475`,
`index.ts:2337-2381`). Committing `0 → 1–7` is **specialization** — a monotone increase
of information, the order arrow `⊑` itself (Platform §1.2, Invariant B). So CB-encoded
spaces are equipped with a **two-level (class/instance) carrier in one coordinate**: the
all-`0` coordinate is the top class `CB_Entity`; downward in `⊑` (more `1–7`s) is
specialization toward instances. This is the Platform Theorem's Invariant B re-read as
equipment: **PROVED** (it *is* the order's semantic content).

### B3. Drill / bloom dependent sub-spaces (the tree / dependent product). **PROVED.**

Two mechanisms open deeper positions, both realizing the **tree-dependency** of
Invariant E:

- **Drill** (`8` / close `88`): within a single level, `8` drills into the
  *currently-selected* node's sub-space and `88` closes it (`index.ts:768-790`); drilling
  is only meaningful after a selection (it operates on the active selected node). So a
  drilled position becomes reachable **only once its governing selection is committed.**
- **Bloom** (`producedSpace`): a selected node may carry a *produced space*, and
  resolution follows the dot into it (`index.ts:855-858`); `computeTowerDepth` walks this
  **bloom chain** of produced spaces (`index.ts:599-627`).

In both cases the deeper spectrum is **conditional on a shallower commitment** — exactly
the "reachable only once `p` is committed" clause of the carrier (Platform §2.1, Invariant
E). So the carrier is a **dependent product** (a tree of products where deeper factors
appear after shallower selections), not a flat product. This is the structure the
Platform Theorem's "tree-respecting" condition encodes, and it is what makes A8's product
a *dependent* product. **PROVED** (the dependency is the drill/bloom mechanism, read from
the code, and is the carrier's tree shape).

### B4. The product kernel as a similarity / metric layer (independent of the order). **PROVED (kernel + pseudometric); OPEN (positive-definiteness of the superposition-augmented slot kernel).**

**The fact.** `tensorKernel(x,y) = ∏_k K_k(x_k, y_k)` factors over slots
(`kernel-v2.ts:153-217`); each per-slot kernel is a Gaussian RBF on primacy distance,
`K_k(x,y) = exp(-α·|real(x_k)-real(y_k)|²)`, with `K_k(x,x)=1`, and superposition handled
as `K_k(0,0)=1`, `K_k(0,y)=K_k(x,0)=1/√n` (`kernel-v2.ts:128-148`). It is **symmetric**
(`K_k(x,y)=K_k(y,x)`, since `|·|²` and the superposition cases are symmetric) and
**normalized** (`K(x,x)=∏_k 1 = 1`).

**What it equips, PROVED.** A CB-encoded space carries a **similarity layer**: a
symmetric, unit-diagonal kernel `K : D×D → (0,1]`. Wherever `K` is positive-definite (see
OPEN), it is the reproducing kernel of an RKHS with feature map `φ`, and induces the
canonical **pseudometric**
`d(x,y) = √(K(x,x)+K(y,y)−2K(x,y)) = √(2−2K(x,y))` (using normalization). The pure-RBF
restriction — coordinates with **no** superposition slots — is a genuine product of
Gaussian RBF kernels, which is **positive-definite** (each RBF is p.d.; a product of p.d.
kernels is p.d. by the Schur product theorem), hence a genuine RKHS kernel and `d` a
genuine metric on that subset. **PROVED on the no-superposition (fully-instantiated)
subset.**

**Crucial independence (PROVED).** This metric layer is **logically independent of the
order `⊑` and of admissibility.** The kernel decomposes a *similarity function over
already-valid coordinates*; it is **not** monotone w.r.t. `⊑` (two configurations close
in `⊑` need not be `K`-similar and vice versa), and it does **not** couple positions in
the carrier (Platform §1.6 makes exactly this point: the product *kernel* is the wrong
evidence for carrier independence and is logically separate from it). So B4 is **orthogonal
equipment** — a geometry layered *on top of* the domain, not part of its order structure.
This is the honest status: CB carries *both* a Scott-domain order *and* a similarity
metric, and they are different structures on the same carrier.

**OPEN.** Whether the **full** slot kernel — including the superposition rows/columns
`K_k(0,·)=1/√n`, `K_k(0,0)=1` — is positive-definite (hence whether `K` is a true RKHS
kernel and `d` a true metric on **all** of `D`, not just the no-superposition subset) is
**OPEN**: it requires checking that the augmented per-slot Gram matrix (RBF block bordered
by the constant `1/√n` superposition row/column with corner `1`) is PSD for every
spectrum, which is not established by the code or here. Until then, the metric claim is
PROVED only on the fully-instantiated subset and OPEN on configurations with superposed
slots.

### B5. The canonical fingerprint / orbit quotient as symmetry structure. **PROVED (orbit equivalence + symmetry group); OPEN (full automorphism-group claim).**

**The fact.** `subtreeFingerprint` computes an **Aho–Hopcroft–Ullman canonical form** of
a node's subtree (children's fingerprints sorted so order is irrelevant, plus semantic
stratum/kernel tags) (`kernel-v2.ts:317-335`). `findSlotOrbits` groups a slot's spectrum
values into **orbits** — maximal sets of children with *identical subtree fingerprint* —
and names a **symmetry group** `∏_o S_{|o|}` (a product of symmetric groups, one per
nontrivial orbit) (`kernel-v2.ts:348-413`). `computeSpaceSlotSignature` assembles these
per-slot into a whole-space signature whose `.canonical` field **is the kernel ID** = the
EWS backward chain (`kernel-v2.ts:425-428`, `ews.ts:199-218`).

**What it equips, PROVED.** Each slot's spectrum carries a **well-defined equivalence
relation** (same fingerprint) partitioning it into orbits, and a **group**
`G_slot = ∏_o S_{|o|}` acting on the spectrum by permuting structurally-identical children
within each orbit (the symmetric group on each orbit; fixed points for singleton orbits).
The whole-space **total symmetry** is the product `∏_slot G_slot`
(`kernel-v2.ts:78`, `ews.ts:216`), and the **canonical fingerprint** is the
order-invariant (orbit-quotient) identity of the shape — two spaces with the same
fingerprint are subtree-isomorphic. The fingerprint being the orbit quotient is a genuine
invariant: the sort in `subtreeFingerprint` (`kernel-v2.ts:332`) is exactly quotienting by
child reordering, i.e. by the symmetry group's action. So a CB-encoded space is equipped
with **(orbit equivalence, a symmetry group, a canonical orbit-quotient fingerprint)** —
this is the §3 `Aut` notion realized in code, as a structural invariant. **PROVED.**

**OPEN.** That this `∏_slot ∏_o S_{|o|}` is the **full automorphism group of the domain**
`D` (every order-automorphism arises from these slot permutations, and conversely each
preserves `⊑` *and* admissibility) is a **stronger claim** not proved here: it would
require showing (a) slot-orbit permutations extend to order-automorphisms of `(D,⊑)` and
(b) they exhaust `Aut(D)`. We have proved the orbit/fingerprint **is a** symmetry
structure (an equivalence + a group + an invariant), **not** that it is the complete
automorphism group. **OPEN** (the `Aut(Sanctuary) closes ⇒ programs` reading from the
architecture remains VISION; the coded part is the orbit invariant).

### B6. EWS boundary / `kernelComplete` = maximal elements + closure. **PROVED (within a fixed view-boundary).**

**The fact.** `isKernelComplete(space)` is true iff there is at least one slotted node and
**every slotted node is locked** (`index.ts:642-660`). The EWS boundary computation
reports `interior` vs `frontier` nodes and a per-depth `canExpand` flag, where
`canExpand = (slotCount === 0) || (children.length < slotCount)` — i.e. a position can
still receive a new commitment (`ews.ts:225-291`, esp. `:250`, `:262`). The forward chain
exposes `kernelComplete` and `heat` (`ews.ts:186-194`).

**What it equips, PROVED.** Relative to a fixed **view boundary** `B` (the space's
declared slot structure — `slotCount` per node, the "fiat boundary" beyond which the space
changes, `index.ts:111`), define `D_B` = configurations confined to `B`. Then:

- A **`kernelComplete`** configuration — every slotted node locked, nothing at `0` within
  `B` — is a **maximal element of `D_B`**: there is no `B`-position left with `canExpand`
  true (every slotted node has `children.length === slotCount`), so no commitment can be
  added without leaving `B`; in `⊑` it has no proper extension inside `D_B`. **PROVED** (it
  is maximal by the `canExpand` exhaustion).
- The **`frontier` / `canExpand` positions** are exactly the directions of non-maximality
  — the still-extendable positions; a configuration is `kernelComplete` iff its frontier
  (within `B`) is empty. So `kernelComplete` characterizes the **top boundary (maximal
  elements)** of the view-subdomain, and the boundary computation is the **closure
  information** (interior = fully-determined, frontier = extendable). **PROVED.**

This equips the encoding with an explicit, computed handle on the **maximal elements** of
each bounded view — the "complete kernels" — and on the closure (interior/frontier)
relative to the fiat boundary. (The boundary `B` is *fiat*: a different declared
`slotCount`/`terminal` structure gives a different `D_B` and different maximal elements.
The result is "maximal within the declared boundary," not "maximal in the unbounded `D`,"
which has no maximal finite elements at all — its tops are the idealized infinite limits.)
**PROVED, scoped to the declared view-boundary.**

### B7. `heat` = definedness grading. **PROVED (graded measure); CONDITIONAL (monotonicity along `⊑`).**

**The fact.** `computeSpaceHeat(space) = max(0, min(1, 1 − totalFilled/totalSlots))`,
where `totalSlots` sums `slotCount` over slotted nodes and `totalFilled` sums
`min(children.length, slotCount)`; `0` slotted nodes returns the neutral `0.5`
(`index.ts:578-589`). So `heat ∈ [0,1]`: `heat = 0` when every slot is filled
(fully-defined / locked), `heat = 1` when none are (fully-open).

**What it equips, PROVED.** A CB-encoded space carries a **definedness grading** — a real
number in `[0,1]` measuring how far a configuration is from total. It is the *unfilled
fraction*: `heat = 1 − (filled/total)`. As a **graded measure of incompleteness** it is
well-defined and exactly tracks "distance from a `kernelComplete` (maximal) element"
(B6): `heat = 0 ⟺ kernelComplete` (all slots filled ⟹ all maximal-fillable, modulo the
locked-vs-filled distinction below). **PROVED** as a grading.

**CONDITIONAL — monotonicity along `⊑`.** Intuitively "more committed ⇒ lower heat," i.e.
`heat` should be **anti-tone** w.r.t. `⊑`. This holds **at fixed slot structure**:
committing a `0`→`1–7` within a fixed set of slots increases `totalFilled` without
changing `totalSlots`, so `heat` weakly decreases. But **drilling/blooming adds new
slots** (B3): opening a sub-space raises `totalSlots` with the new positions initially
unfilled, which can **raise** `heat` even though the configuration moved **up** in `⊑`
(more committed overall, but newly-exposed `0`s). So `heat` is anti-tone along `⊑`
**only on order-increases that do not open new slots**; under drilling it is not monotone.
Additionally `computeSpaceHeat` counts *filled* (`children.length`) while `kernelComplete`
counts *locked* (`index.ts:642-660`) — a node can be filled-but-unlocked, so `heat = 0`
does not strictly imply `kernelComplete` unless filled ⟹ locked. **PROVED as a grading;
its monotonicity along the domain order is CONDITIONAL (fixed-depth only) and its exact
relation to `kernelComplete` carries the filled-vs-locked caveat.**

---

## Part C — The equipment table

| # | Equipment | Layer | Status on `D` (syntactic) | Status on `D_consistent` |
|---|-----------|-------|---------------------------|--------------------------|
| A1 | `⊥` + information order | free | **PROVED** | restricts; `⊥` PROVED-conditional |
| A2 | directed limits (dcpo) | free | **PROVED** | **OPEN** (dir-union closure) |
| A3 | compact basis + algebraicity | free | **PROVED** | **OPEN** (downward closure) |
| A4 | way-below `≪` + Scott topology | free | **PROVED** | subspace yes; basis OPEN |
| A5 | bounded-complete joins | free | **PROVED** | **OPEN** (bounded-join closure) |
| A6 | `[D→D]` is a Scott domain | free | **PROVED** (classical) | **OPEN** (needs A5) |
| A7 | Kleene least fixed points | free | **PROVED** | conditional on A2 |
| A8 | closure under products/sums | free | **PROVED** | **OPEN** (needs factors) |
| B1 | `coordToReal` real-line address + decodability | CB | **PROVED** on `D_canon`; OPEN unrestricted | (addressing, order-orthogonal) |
| B2 | class/instance specialization | CB | **PROVED** | = the order's content |
| B3 | drill/bloom dependent product | CB | **PROVED** | = tree-respecting carrier |
| B4 | product kernel similarity/metric | CB | **PROVED** (no-superpos subset); OPEN (PSD w/ superpos) | order-orthogonal |
| B5 | orbit quotient / canonical fingerprint = symmetry | CB | **PROVED** (orbit group); OPEN (full `Aut`) | structural invariant |
| B6 | `kernelComplete` = maximal + closure | CB | **PROVED** (within fiat view-boundary) | n/a — orthogonal to admissibility |
| B7 | `heat` = definedness grading | CB | **PROVED** (grading); CONDITIONAL (monotonicity) | n/a — orthogonal to admissibility |

---

## Conclusion

A Crystal Ball–encoded space, on its **syntactic carrier**, is a Scott domain (the
Platform Theorem) and therefore comes **fully equipped**: a least element and information
order, directed limits, a basis of finitely-resolved compact elements with algebraicity,
the way-below relation and the Scott topology, bounded-complete joins of consistent
partials, a Scott-domain function space `[D→D]`, Kleene least fixed points (the convergent
climb `⊔ₙ fⁿ(⊥)` that CB's own "collapse all `0`s" instantiation realizes), and closure
under products and sums. On top of — and **orthogonal to** — this order, the *particular*
encoding carries: a faithful real-line address `coordToReal` (injective on the canonical
subspace, with an honestly-bounded decodability lemma, **not** an order-isomorphism); the
class/instance specialization in the digit; drill/bloom dependent sub-spaces realizing the
tree-dependent product; a product RBF kernel inducing a similarity geometry (a genuine
metric on the fully-instantiated subset, PSD-with-superposition OPEN); a canonical
fingerprint / orbit quotient giving a symmetry group (the full-`Aut` identification OPEN);
the `kernelComplete` predicate marking the maximal elements of each fiat view-boundary;
and `heat` grading definedness (anti-tone only at fixed depth).

**The boundary is held throughout.** Every order-theoretic item is **PROVED on the
syntactic carrier**; each item whose proof uses directed- or bounded-completeness
(A2, A3, A5, A6, A8, and A7 via A2) **inherits OPEN on the externally-validated subspace
`D_consistent`**, gated on the external admissibility predicate being closed under the
relevant suprema. Whether `D_consistent` is itself a Scott domain — the downward-closed-
admissibility question — remains the next proposition, separate and open.
