# Crystal Ball's Real-Line Coordinate Encoding Is a Scott Domain

------------------------------------------------------------
## Abstract
------------------------------------------------------------

Crystal Ball encodes structured knowledge as **coordinates over a fixed digit grammar** that address points
of the half-open interval $[0,1)$. Within each level of a coordinate, a position carries either the marker `0` — a
**class-level** slot, a kind that is known but not yet specialized — or a selection in `1`-`7` — an
**instance**, a specific child chosen at that slot; `9` is a *wrap* that extends the selection range, `8` and
`88` open and close a *drill* into the subspace of the currently selected node, and reserved digit sequences
(`8988`, `90`, `900`) serve as structural delimiters. Collapsing a `0` into a selection is the single act of
*observing* (specializing) the structure, and the function `coordToReal` places each coordinate at a point of
the half-open interval $[0,1)$. We prove that **the set of these coordinates, ordered by specialization — one
coordinate is below another when the second agrees with it wherever it has committed and may additionally
resolve positions the first left at `0` — is a Scott domain**: a bounded-complete algebraic dcpo with a least
element (Theorem 1). We further prove that reading a coordinate into content and composing two coordinates are
Scott-continuous (Theorem 2), and that the *linear* coordinates (a single root-to-leaf chain of selections)
carry exactly the prefix/depth order (Theorem 3). The result is about the encoding's own mechanics — the
class-versus-instance digit structure and its drill nesting — and nothing more. `coordToReal` is shown to be an
injective address of each coordinate into $[0,1)$ (Section 3.5); it is the specialization order, not the
numeric order $\le$ of the reals, that carries the domain structure. We make no claim here beyond this
structural one; richer constructions over these coordinate spaces are deliberately out of scope (Section 4).

------------------------------------------------------------
## 1. The encoding
------------------------------------------------------------

Crystal Ball represents structured knowledge as a chain of **spaces**. A space is a finite tree (more
generally a DAG) of nodes; each node *necessitates* the nodes below it, and a node may **produce** a child
space into which resolution continues. A **coordinate** is a dot-separated sequence of **levels**; each level
is a string over a small digit grammar that selects, within the current space, which node is meant and
whether to drill into it. The grammar (parsed character by character within a level) is:

- **`0` — superposition.** The slot is *not yet chosen*: its kind is fixed by position but no instance is
  selected. This is the **class** reading.
- **`1`-`7` — selection.** An exact choice of child (its primacy among the parent's children). This is the
  **instance** reading. `9` is a **wrap** that adds `7` to the running selection, so selections beyond seven
  are expressible; the digit value alone never exceeds the alphabet.
- **`8` — drill** into the subspace of the currently selected node; **`88` — close drill**, returning to the
  parent level. Drills nest, and every open drill must be closed.
- **reserved sequences** — `8988` encodes the level-separating dot, and `90` / `900` delimit a kernel
  reference; these are digit sequences the selection grammar can never itself produce, so they are
  unambiguous structural punctuation.

Collapsing the `0`s of a coordinate into selections — **instantiation** — is the only act the encoding
models. A coordinate's numeric **address** is `coordToReal(c)`, the real number whose decimal expansion is
`0.` followed by the coordinate's digits (with each dot encoded as `8988`); `root` addresses `0`. Thus every
coordinate names a point of $[0,1)$.

We put on the coordinates the **specialization (observation) order**: a coordinate $\sigma$ is *below* a
coordinate $\tau$ when, at every position, either $\sigma$ is still `0` there or $\sigma$ and $\tau$ agree —
$\tau$ may have specialized slots that $\sigma$ left open, but never disagrees with a commitment $\sigma$ has
made. "Less resolved" sits below "more resolved." The whole of this paper establishes one fact about that
ordered set: **it is a Scott domain**, and the two natural operations on it (reading a coordinate into
content, and composing coordinates) respect the order. Everything is structural; there is no empirical content
and no appeal to anything outside the encoding's own digit mechanics. Constructions that run *over* these
spaces — a generative recursion, a read-off into a typed ontology, and the like — are not part of this result
and are deliberately deferred (Section 4).

One orientation for the reader before the proofs begin: the specific punctuation digits of the grammar above
(the `9` wrap, the `8`/`88` drill markers, and the reserved sequences `8988`/`90`/`900`) play no role in the
order-theoretic results; only the `0`-versus-selection distinction does. They build the tree but never enter
a proof.

## 2. Preliminaries
------------------------------------------------------------

### 2.1 Order-theoretic background

Throughout, a **partial order** on a set $P$ is a binary relation $\sqsubseteq$ that is *reflexive*
($x \sqsubseteq x$), *antisymmetric* ($x \sqsubseteq y$ and $y \sqsubseteq x$ imply $x = y$), and
*transitive* ($x \sqsubseteq y$ and $y \sqsubseteq z$ imply $x \sqsubseteq z$). We read $x \sqsubseteq y$
as "$x$ is below $y$" or "$y$ extends $x$."

An **upper bound** of a subset $A \subseteq P$ is an element $u$ with $a \sqsubseteq u$ for all $a \in A$.
A subset is **consistent** (or **bounded**) if it *has* an upper bound. A **least upper bound** (or
**supremum**, written $\bigsqcup A$) is an upper bound below every upper bound; suprema are unique when
they exist. Throughout, "consistent" means precisely "bounded above" — never anything weaker.

A subset $A \subseteq P$ is **directed** if it is nonempty and every two elements $a, b \in A$ have an
upper bound $c \in A$ (so $a \sqsubseteq c$ and $b \sqsubseteq c$). Intuitively, a directed set is a
collection of mutually compatible, ever-more-informative observations.

$P$ is a **directed-complete partial order** (**dcpo**) if every directed subset has a supremum in $P$.
$P$ is **pointed** if it has a least element $\bot$ (a *bottom*), satisfying $\bot \sqsubseteq x$ for all
$x$.

An element $k \in P$ is **compact** (synonym: an order-theoretically *finite* element) if, whenever $k$
is below the supremum of a directed set, it is already below a member of that set:
$$k \sqsubseteq \textstyle\bigsqcup A \ \Longrightarrow\ \exists\, a \in A,\ k \sqsubseteq a .$$
Compact elements are those that can be "fully written down" — they cannot be reached only as a genuine
limit. We write $K(P)$ for the set of compact elements.

$P$ is **algebraic** if every element is the directed supremum of the compact elements below it:
$x = \bigsqcup\{ k \in K(P) : k \sqsubseteq x \}$ for all $x$, with the set on the right directed.

$P$ is **bounded-complete** if every consistent (bounded) subset has a least upper bound. (Equivalently,
every pair with a common upper bound has a supremum.)

A **Scott domain** is a bounded-complete algebraic dcpo with a least element.

A map $f : P \to Q$ between dcpos is **monotone** if $x \sqsubseteq y$ implies $f(x) \sqsubseteq f(y)$,
and **Scott-continuous** if it is monotone and preserves directed suprema: for every directed
$A \subseteq P$, $f(\bigsqcup A) = \bigsqcup_{a \in A} f(a)$. Scott-continuity is the order-theoretic
form of "computable up to taking limits": the output of a limit is the limit of the outputs.

> **Terminology.** The word *finite* wears several hats in this area. We reserve **compact** for the
> order-theoretic finite elements just defined; we say **finite schema** (Section 2.2) for a schema
> with finitely many slots; we say **finite arity** (Section 2.2) for the requirement that each slot have
> finitely many alternative instances; and we say **finitely-resolved configuration** for a configuration
> that resolves only finitely many slots. Where confusion is possible we write "compact element" or
> "finitely-resolved configuration" for the order-theoretic sense and keep "finite schema" / "finite arity"
> for the schema senses.

### 2.2 The carrier: configurations over a slot tree

A **slot tree** (or **schema**) $K$ consists of:

1. a distinguished **root**;
2. a set $\mathrm{Slots}(K)$ of **slots** (positions that may be filled), carrying a tree structure: every
   slot has a unique finite path of *ancestor* slots back to the root (so each non-root slot has a unique
   parent, and the ancestor chain of a slot is unique);
3. a **parent–opening relation** specifying, for each non-root slot, which selection at its parent *opens*
   it (so a slot becomes available only once its parent has been specialized accordingly);
4. for each slot $s$ a finite **arity** $\mathrm{arity}(s) \in \mathbb{N}$, the number of alternative
   instances available at $s$.

A slot's **kind** is its structural type — its arity together with which selections open which child slots,
recursively; "kind" is the arity-and-opening structure, not an extra label imposed on top of it. The slot
set may be finite or infinite (an infinite slot tree is the source of the non-compact elements in Theorem
1); only the *arity* of each slot is required finite.

Fix such a $K$. For each slot $s$ put
$$\mathrm{Val}_s = \{0\} \cup \{1, \dots, \mathrm{arity}(s)\}.$$
Order $\mathrm{Val}_s$ as the **flat domain** with bottom $0$: that is, $0 \sqsubseteq v$ for every $v$,
and distinct nonzero values are incomparable. The value $0$ is the **order-theoretic bottom** of the slot's
value domain. Its intended *reading* is the **class level**: the slot's kind is known but no instance is
chosen; an integer $i \in \{1, \dots, \mathrm{arity}(s)\}$ reads as a specific **instance selection**. The
order-theoretic role ($0$ = least defined) and the reading ($0$ = "kind, no instance") are two views of the
same value; the proofs use only the order-theoretic role. Since $\mathrm{arity}(s)$ is finite, each
$\mathrm{Val}_s$ is finite.

A **configuration** is a *total* function
$$\sigma : \mathrm{Slots}(K) \to \mathrm{Val},\qquad \sigma(s) \in \mathrm{Val}_s,$$
subject to **tree-consistency**: if $\sigma(s) \neq 0$ (the slot is specialized) then every ancestor slot
on $s$'s ancestor chain is also specialized in $\sigma$, each carrying the selection that opens the next
slot on the chain toward $s$. Write
$$\mathrm{res}(\sigma) = \{\, s : \sigma(s) \neq 0 \,\}$$
for the set of **resolved** slots. We call a set $T \subseteq \mathrm{Slots}(K)$ **root-connected** if it
is empty, or it contains the root and, with each slot, all of that slot's ancestors. Tree-consistency says
exactly that $\mathrm{res}(\sigma)$ is root-connected (the empty set qualifies — total ignorance is
consistent) and that the recorded selections along it agree with the opening relation. A slot whose
ancestors are still unobserved simply sits at $0$: partiality is encoded by the value $0$, never by a
missing argument.

Let $D = D(K)$ be the set of all configurations of $K$.

We record one structural lemma here, at the point where configurations are defined. It does not depend on
anything later; it is stated now because it is used in §2.3 and §3 (the slotwise-union and bottom
constructions of §2.3, and the proofs of §3, draw on its root-connectedness facts).

> **Lemma 0 (Restriction and union of resolved sets).** Let $x \in D$.
> (a) If $T \subseteq \mathrm{res}(x)$ is root-connected, then the function $x{\restriction}T$ that equals
> $x$ on $T$ and $0$ elsewhere is a configuration, and $x{\restriction}T \sqsubseteq x$.
> (b) If $T_1, T_2 \subseteq \mathrm{res}(x)$ are root-connected, so is $T_1 \cup T_2$.

*Proof.* (a) For $s \in T$ with $(x{\restriction}T)(s) \neq 0$, every ancestor of $s$ lies on $s$'s unique
ancestor chain; since $T$ is root-connected it contains those ancestors, and $x$ — being tree-consistent —
specializes each with the opening selection, values that $x{\restriction}T$ copies. Hence $x{\restriction}T$
is tree-consistent. It agrees with $x$ on $T$ and is $0$ off $T$, so $x{\restriction}T \sqsubseteq x$.
(b) Each element of $T_1 \cup T_2$ brings its ancestor chain (it lies in $T_1$ or $T_2$, each
root-connected), and if either set is nonempty the union contains the root; the empty case is trivial.
$\qquad\blacksquare$

> **Remark (Representation — not used in any proof).** Each configuration $\sigma$ may be *encoded* as a
> finite or infinite string of digits $\mathrm{enc}(\sigma)$ recording the selections along
> $\mathrm{res}(\sigma)$, with reserved digit-patterns serving as structural punctuation (marking where a
> slot is drilled into, where a subtree closes, and so on). Only the marker $0$ and the instance digits carry
> order-theoretic content; the punctuation patterns *build* the tree and the values and are not themselves
> elements of $D$. The encoding is a **recoverable encoding** — $\sigma$ is recoverable from
> $\mathrm{enc}(\sigma)$ — but the
> configurations *are* the functions $\sigma$, not their digit strings; we never treat a raw string as an
> element of $D$. (We reserve the word *recoverable* for this string-encoding sense; the *injectivity* of
> the real-line address `coordToReal` in §3.6 is a separate property.) The encoding is what places each
> configuration at a point of the real line. **Nothing
> downstream uses this:** no metric, real-line, or digit-string structure does any proof work — the proofs
> refer solely to the functions $\sigma$ and the order defined next. This remark is included only to connect
> the configurations to their string/real-line representation, and may be skipped without loss.

### 2.3 The observation (specialization) order

Define $\sqsubseteq$ on $D$ by
$$\sigma \sqsubseteq \tau \quad\Longleftrightarrow\quad
\text{for every slot } s,\ \ \sigma(s) = 0 \ \text{ or } \ \sigma(s) = \tau(s).$$
In words: $\tau$ has observed at least as much as $\sigma$ and agrees with $\sigma$ wherever $\sigma$ has
committed; $\tau$ may resolve slots $\sigma$ left at $0$ (and thereby open and resolve further slots).
This is the pointwise order induced by the per-slot flat orders of Section 2.2: "less resolved" sits below "more resolved."

We record two derived constructions used repeatedly.

> **Slotwise union.** For $A \subseteq D$, define a function $\bigsqcup A$ by
> $(\bigsqcup A)(s) = a(s)$ for some $a \in A$ with $a(s) \neq 0$, if any such $a$ exists, and
> $(\bigsqcup A)(s) = 0$ otherwise. (Lemma 1 below shows this is well-defined when $A$ is directed or
> consistent.)

> **Bottom.** Let $\bot$ be the configuration that is $0$ at every slot — total ignorance. Its resolved
> set is empty, hence root-connected, so $\bot \in D$.

------------------------------------------------------------
## 3. The encoding, ordered by specialization, is a Scott domain
------------------------------------------------------------

### 3.1 Supporting lemmas

> **Lemma 1 (Well-defined slotwise union).** Let $A \subseteq D$ be directed, or consistent (bounded
> above). Then for every slot $s$, all members of $A$ that resolve $s$ assign it the same value; hence the
> slotwise union $\bigsqcup A$ is well-defined, with resolved set $\bigcup_{a \in A}\mathrm{res}(a)$.

*Proof.* Suppose $a(s) \neq 0$ and $b(s) \neq 0$ for $a, b \in A$. If $A$ is directed, take $c \in A$
with $a \sqsubseteq c$ and $b \sqsubseteq c$; then $a(s) = c(s)$ and $b(s) = c(s)$, so $a(s) = b(s)$. If
instead $A$ is bounded by $u$, then $a \sqsubseteq u$ and $b \sqsubseteq u$ give $a(s) = u(s) = b(s)$.
The assigned value is independent of the witness, so $\bigsqcup A$ is well-defined; its resolved set is the
union of the members' resolved sets by construction. $\qquad\blacksquare$

> **Lemma 2 (Finite capture).** Let $k \in D$ resolve only finitely many slots, let $A \subseteq D$ be
> directed, and suppose $k \sqsubseteq \bigsqcup A$. Then there is $a \in A$ with $k \sqsubseteq a$.

*Proof.* The element $k$ resolves finitely many slots $s_1, \dots, s_m$ (those with $k(s_i) \neq 0$).
For each $i$, $k \sqsubseteq \bigsqcup A$ forces $(\bigsqcup A)(s_i) = k(s_i) \neq 0$, so by the
definition of the slotwise union some $a_i \in A$ has $a_i(s_i) = k(s_i)$. There are finitely many
$a_i$, and $A$ is directed, so there is a single $a \in A$ above all of them. Then $a(s_i) = k(s_i)$ for
every $i$, while $k$ is $0$ elsewhere, so $k \sqsubseteq a$. $\qquad\blacksquare$

> **Lemma 3 (Reconstruction).** For every $x \in D$, $\ x = \bigsqcup\{\, k \in D : k \sqsubseteq x,\
> k \text{ resolves finitely many slots} \,\}$, and this set is directed.

*Proof.* For a resolved slot $s \in \mathrm{res}(x)$, let $C_s$ be the (unique, finite) ancestor chain of
$s$ together with $s$; it is root-connected and contained in $\mathrm{res}(x)$, so by Lemma 0(a)
$x{\restriction}C_s$ is a finitely-resolved configuration below $x$ resolving $s$. Hence every resolved
slot of $x$ is resolved by some finitely-resolved $k \sqsubseteq x$, so the slotwise union of all such $k$
equals $x$. The family is directed: given two such $k_1, k_2$, the set $\mathrm{res}(k_1) \cup
\mathrm{res}(k_2)$ is root-connected (Lemma 0(b)) and contained in $\mathrm{res}(x)$, so by Lemma 0(a)
$x{\restriction}(\mathrm{res}(k_1)\cup\mathrm{res}(k_2))$ is a finitely-resolved configuration below $x$
and above both $k_1$ and $k_2$. $\qquad\blacksquare$

### 3.2 The configuration space is a Scott domain

> **Theorem 1.** $(D, \sqsubseteq)$ is a Scott domain: a bounded-complete algebraic dcpo with least
> element. (No finiteness of the slot set is assumed; only finite arity.)

*Proof.* We verify the constituent properties.

**(i) Partial order.** *Reflexivity:* at each slot $s$, either $x(s) = 0$ or $x(s) = x(s)$, so
$x \sqsubseteq x$. *Antisymmetry:* assume $x \sqsubseteq y$ and $y \sqsubseteq x$. Fix $s$. If
$x(s) \neq 0$, then $x \sqsubseteq y$ gives $x(s) = y(s)$. If $x(s) = 0$, then $y \sqsubseteq x$ gives
$y(s) = 0$ or $y(s) = x(s) = 0$, so $y(s) = 0 = x(s)$. Thus $x(s) = y(s)$ at every slot, i.e. $x = y$.
*Transitivity:* assume $x \sqsubseteq y$ and $y \sqsubseteq z$, and fix $s$. If $x(s) = 0$ the first
disjunct of $x \sqsubseteq z$ holds. If $x(s) \neq 0$, then $x(s) = y(s) \neq 0$ and $y(s) = z(s)$, so
$x(s) = z(s)$. Hence $x \sqsubseteq z$.

**(ii) Least element.** For any $x$ and slot $s$, $\bot(s) = 0$, so the first disjunct of
$\bot \sqsubseteq x$ holds; thus $\bot \sqsubseteq x$.

**(iii) Directed-completeness.** Let $A$ be directed and form $\bigsqcup A$ (well-defined by Lemma 1),
with resolved set $R = \bigcup_{a \in A}\mathrm{res}(a)$. We check $R$ is root-connected and the recorded
selections are consistent, so $\bigsqcup A \in D$. If $R = \varnothing$ then $\bigsqcup A = \bot \in D$.
Otherwise take $s \in R$, say $s \in \mathrm{res}(a)$ for some $a \in A$. Since $a$ is tree-consistent,
$a$ resolves every ancestor of $s$ with the opening selections; those ancestors and selections lie in
$\mathrm{res}(a) \subseteq R$ and, by Lemma 1, every member of $A$ that resolves them does so to the same
values — so $R$ contains $s$'s ancestor chain with the correct opening selections. As this holds for every
$s \in R$, the set $R$ is root-connected and the selections are globally consistent; hence $\bigsqcup A \in
D$. For each $a \in A$ and slot $s$ with $a(s) \neq 0$ we have $(\bigsqcup A)(s) = a(s)$, and where
$a(s) = 0$ the disjunct holds, so $a \sqsubseteq \bigsqcup A$: it is an upper bound. If $u$ is any upper
bound of $A$, then for each $s$ with $(\bigsqcup A)(s) \neq 0$ some $a \in A$ has $a(s) = (\bigsqcup A)(s)$
and $a \sqsubseteq u$, so $u(s) = (\bigsqcup A)(s)$; elsewhere the disjunct holds; hence $\bigsqcup A
\sqsubseteq u$. So $\bigsqcup A$ is the least upper bound and $D$ is a dcpo.

**(iv) Compact elements are exactly the finitely-resolved configurations.** First, every configuration $k$
resolving only finitely many slots is compact: this is precisely Lemma 2. Conversely, suppose $x$ resolves
infinitely many slots; let $A = \{\, k \sqsubseteq x : k \text{ resolves finitely many slots} \,\}$. By
Lemma 3, $A$ is directed and $\bigsqcup A = x$. Each $a \in A$ resolves only finitely many slots while $x$
resolves infinitely many, so there is a slot $s$ with $x(s) \neq 0 = a(s)$; then the order's defining
condition fails at $s$ ($x(s) \neq 0$ and $x(s) \neq a(s)$), so $x \not\sqsubseteq a$. Thus
$x \sqsubseteq \bigsqcup A = x$ yet no member of $A$ is above $x$, so $x$ is not compact. Hence the compact
elements are exactly the finitely-resolved configurations.

**(v) Algebraicity.** Fix $x$ and let $K_x = \{\, k \sqsubseteq x : k \text{ compact} \,\}$, which by (iv)
is the set of finitely-resolved configurations below $x$. By Lemma 3 it is directed with $\bigsqcup K_x =
x$, and the least-upper-bound computation of (iii) shows this is the supremum. Hence
$x = \bigsqcup\{\, k \in K(D) : k \sqsubseteq x \,\}$ for every $x$.

**(vi) Bounded-completeness.** Let $S \subseteq D$ be consistent, with upper bound $u$. By Lemma 1 the
members of $S$ agree on jointly-resolved slots and $\bigsqcup S$ is well-defined; its resolved set
$\bigcup_{\sigma \in S}\mathrm{res}(\sigma)$ is root-connected with consistent selections by the argument
of (iii) (every resolving member is $\sqsubseteq u$, so all ancestor data agree), hence $\bigsqcup S \in
D$. As in (iii), $\bigsqcup S$ is an upper bound of $S$ and below every upper bound. So every consistent
subset has a least upper bound.

By (i)–(vi), $(D, \sqsubseteq)$ is a bounded-complete algebraic dcpo with least element — a Scott
domain. $\qquad\blacksquare$

> **Remark 1 (Sets of selections per slot).** The model above lets a slot carry the marker $0$ or one
> instance. A natural enrichment lets a slot carry a *set* of instances simultaneously (a conjunction of
> selections at the *same* slot — distinct from a configuration *branching* across several different
> slots, which the base model already allows; that contrasting same-slot-vs-sibling-slot distinction is
> discussed again in §3.5). Replacing each per-slot flat factor by the lattice of
> *subsets* of $\{1, \dots, \mathrm{arity}(s)\}$ ordered by inclusion keeps $D$ a Scott domain, because
> each such lattice is *finite* (the arity is finite), hence trivially a bounded-complete algebraic dcpo.
> (If a slot's choice space were infinite, "finite subsets ordered by inclusion" would fail to be
> directed-complete; the correct fix would then be the ideal completion with finite subsets as the compact
> elements. We do not need it, since all arities are finite.)

### 3.3 Operational structure: the hypotheses the continuity results are conditional on

Reading a configuration into content and composing two configurations are **additional operational
structure**, not consequences of the carrier alone. We state all the hypotheses they require up front, in
one place, and flag here that **every continuity result below (Theorem 2(a), (b)) is conditional on them**;
verifying that a particular implementation's read/compose operations satisfy them is a separate faithfulness
question (Remark 2), not undertaken here.

First the meaning structure. A configuration is *decoded* into content by interpreting its resolved
selections against a fixed **meaning structure**, modelled as itself a slot tree $M$ — formally the same kind
of object as $K$ (Section 2.2) — so that $C := D(M)$, the configurations of $M$ ordered by its own
observation order $\sqsubseteq_C$, is by Theorem 1 a Scott domain with bottom the all-$0$ configuration. Each
content position is a slot of $M$, reached by a finite chain of selections. In the **reflexive case** the
meaning structure is the schema itself, $M = K$, whence $C = D$ and decoding is an endomap; Theorem 2(b) is
stated in this case.

We then take $\mathrm{decode} : D \to C$ to be any map satisfying the following two stipulated **read-map
hypotheses** (defining properties of the read map, not derived from the carrier):

- **(Locality)** For each content position $p$, the value $\mathrm{decode}(\sigma)(p)$ depends only on the
  selections $\sigma$ makes along the unique finite chain of slots leading to $p$; selections elsewhere in
  $\sigma$ do not affect it. In particular $\mathrm{decode}(\sigma)(p)$ is determined by a finitely-resolved
  $k \sqsubseteq \sigma$ (the restriction of $\sigma$ to that chain).
- **(Bottom past the boundary)** Resolution proceeds slot by slot along $\sigma$'s resolved chains. At any
  position where $\sigma$ is still at $0$, or at a structural *dangling reference* (a punctuation marker
  whose target slot is undefined), resolution **halts**: that content position and everything downstream of
  it take **the value $0$** (the per-position bottom of $C$). Thus $\mathrm{decode}$ is **total** into $C$,
  with value $0$ past any halting point. Partiality is thereby realized as bottom-valued totality rather
  than as an undefined map.

And, for the reflexive composition $\oplus : D \times D \to D$ of Theorem 2(b), three further
**composition hypotheses** — **(C1) Closure**, **(C2) Finite determinacy**, and **(C3) Monotonicity** — on
which part (b) is conditional. To keep them beside the single argument that uses them, they are stated in
full in the proof of Theorem 2(b) (§3.4); we refer to them there as (C1)–(C3). They hold for the intended
construction in which $\psi$ supplies the selections that $\varphi$ leaves open below its resolved
frontier.

### 3.4 Reading and composing configurations are continuous (conditional on §3.3)

With the hypotheses of §3.3 in place, we show both operations respect the specialization order — they are
Scott-continuous.

> **Lemma 4 (decode factors through compacts).** Under (Locality), for every $\sigma$ and content position
> $p$ with $\mathrm{decode}(\sigma)(p) \neq 0$, there is a finitely-resolved $k \sqsubseteq \sigma$ with
> $\mathrm{decode}(k)(p) = \mathrm{decode}(\sigma)(p)$.

*Proof.* By (Locality) the value at $p$ depends only on $\sigma$ along the finite chain to $p$; take $k$ to
be $\sigma$ restricted to that chain (a configuration by Lemma 0(a)). Then $k \sqsubseteq \sigma$ and, by
(Locality) again applied to $k$ (which agrees with $\sigma$ on the chain), $\mathrm{decode}(k)(p) =
\mathrm{decode}(\sigma)(p)$. $\qquad\blacksquare$

> **Theorem 2 (Continuity of decode and apply).**
> (a) Any $\mathrm{decode} : D \to C$ satisfying (Locality) and (Bottom past the boundary) is
> Scott-continuous.
> (b) In the reflexive case $C = D$, let $\oplus : D \times D \to D$ be a composition operation satisfying
> the hypotheses (C1)–(C3) below. Then the curried map $\mathrm{app} : D \to [D \to D]$,
> $\mathrm{app}(\varphi) = \big(\psi \mapsto \mathrm{decode}(\varphi \oplus \psi)\big)$, is well-defined
> and Scott-continuous, where $[D \to D]$ is the dcpo of Scott-continuous self-maps of $D$ ordered
> pointwise.

*Proof of (a).* **Monotonicity.** Let $\sigma \sqsubseteq \tau$ and fix $p$ with
$\mathrm{decode}(\sigma)(p) = n_p \neq 0$. By (Locality), $n_p$ is determined by $\sigma$ along the
finite chain $s_1, \dots, s_k$ to $p$, where each $\sigma(s_i) \neq 0$. Since $\sigma \sqsubseteq \tau$,
each $\sigma(s_i) = \tau(s_i)$, so $\tau$ agrees with $\sigma$ along that chain; by (Locality) applied to
$\tau$, $\mathrm{decode}(\tau)(p) = n_p$. (Any further slots $\tau$ resolves lie off this chain and, by
(Locality), cannot change the value at $p$.) Where $\mathrm{decode}(\sigma)(p) = 0$ — including the case
where $\sigma$ halts at a dangling reference and is $0$ from $p$ onward — the order on $C$ holds trivially,
since the value $0$ is the per-position bottom; if $\tau$ later resolves that dangling reference into a
nonzero value, this only moves the value *up* from $0$, preserving monotonicity. Hence
$\mathrm{decode}(\sigma) \sqsubseteq_C \mathrm{decode}(\tau)$.

**Preservation of directed suprema.** Let $A \subseteq D$ be directed with supremum $\bigsqcup A$. By
monotonicity $\{\mathrm{decode}(a)\}_{a \in A}$ is directed and bounded by $\mathrm{decode}(\bigsqcup A)$,
so $\bigsqcup_a \mathrm{decode}(a) \sqsubseteq_C \mathrm{decode}(\bigsqcup A)$. For the reverse, fix $p$
with $\mathrm{decode}(\bigsqcup A)(p) = n_p \neq 0$. By Lemma 4 there is a finitely-resolved $k
\sqsubseteq \bigsqcup A$ with $\mathrm{decode}(k)(p) = n_p$; by Lemma 2 (finite capture) some $a^\ast \in A$
has $k \sqsubseteq a^\ast$, and by monotonicity $\mathrm{decode}(a^\ast)(p) = n_p$. Hence
$\mathrm{decode}(\bigsqcup A)(p) \sqsubseteq (\bigsqcup_a \mathrm{decode}(a))(p)$; where the left side is
$0$ the order holds. Therefore $\mathrm{decode}(\bigsqcup A) = \bigsqcup_a \mathrm{decode}(a)$, and
$\mathrm{decode}$ is Scott-continuous.

*Proof of (b).* We use exactly these stipulated properties of the composition $\oplus$ (the **defining
hypotheses on composition**), each of which holds for the intended construction in which $\psi$ supplies
the selections that $\varphi$ leaves open below its resolved frontier:

- **(C1) Closure.** $\varphi \oplus \psi \in D$ for all $\varphi, \psi \in D$.
- **(C2) Finite determinacy.** For each content position $p$, the value $\mathrm{decode}(\varphi \oplus
  \psi)(p)$ depends only on finitely-resolved restrictions of $\varphi$ and of $\psi$ (so that, with
  $\varphi$ or $\psi$ fixed, the resulting map satisfies (Locality) in the other argument).
- **(C3) Monotonicity.** $\oplus$ is monotone in each argument separately.

Fix $\varphi$. The map $\psi \mapsto \mathrm{decode}(\varphi \oplus \psi)$ is monotone by (C3) and (a), and
preserves directed suprema by the argument of (a) using (C2) in place of (Locality); hence it lies in
$[D \to D]$ and $\mathrm{app}(\varphi)$ is well-defined. Finally $\mathrm{app}$ is Scott-continuous: it is
monotone by (C3), and for directed $\Phi \subseteq D$ and any $\psi$,
$$\mathrm{app}\big(\textstyle\bigsqcup \Phi\big)(\psi)
= \mathrm{decode}\big((\textstyle\bigsqcup \Phi) \oplus \psi\big)
= \textstyle\bigsqcup_{\varphi \in \Phi} \mathrm{decode}(\varphi \oplus \psi)
= \big(\textstyle\bigsqcup_{\varphi \in \Phi} \mathrm{app}(\varphi)\big)(\psi),$$
the middle equality by (C2) and finite capture in the first argument. Both sides agree at every $\psi$, and
the suprema in $[D\to D]$ are computed pointwise, so $\mathrm{app}(\bigsqcup \Phi) = \bigsqcup_\Phi
\mathrm{app}(\varphi)$. $\qquad\blacksquare$

> **Remark 2 (scope of Theorem 2).** Part (a) is a theorem about *any* read map with the two stated
> properties; (b) is a theorem about *any* composition with (C1)–(C3) in the reflexive case. We do not
> derive these properties from the carrier alone — reading and composing are *additional operational
> structure*, and the hypotheses make precise what that structure must satisfy. Verifying that a particular
> implementation's read/compose operations satisfy them is a separate faithfulness question, not undertaken here; the
> dependence of (b) on the exact composition is the most delicate point.

We emphasize what Theorem 2(b) does *not* assert: $\mathrm{app}$ is a continuous *map*, not necessarily an
*order-embedding* of $D$ into its own function space. Nothing below relies on a reflexive embedding $D \cong [D \to D]$; the continuous map suffices.

### 3.5 The depth order is the linear restriction of the observation order

In this subsection we use *coordinate* in the narrow linear sense — a single root-to-leaf chain of
selections; elsewhere in the paper it means a (possibly partial, possibly branching) configuration.

Two orders arise naturally and are sometimes treated as distinct "axes":

- a **depth (prefix) order**: one coordinate is below another when its digit-string is a prefix of the
  other's — i.e. the second drills *deeper* along the same path;
- the **observation order** $\sqsubseteq$ of Section 2.3: filling unobserved slots into selections.

They are not competing; the first is the linear special case of the second. By a **coordinate** we mean a
single root-to-leaf chain of selections (one selection at each slot along one path); it determines a
configuration $\mathrm{config}(c) \in D$ resolving exactly that chain and leaving every other slot at $0$
(tree-consistent, the chain being root-connected).

> **Theorem 3.** The map $c \mapsto \mathrm{config}(c)$ is an order-embedding of the coordinates under the
> prefix order into $(D, \sqsubseteq)$: $\ c \preceq_{\mathrm{pre}} d \iff \mathrm{config}(c) \sqsubseteq
> \mathrm{config}(d)$. Its image is exactly the *linear* configurations (those whose resolved set is a
> single root-to-leaf chain). If $K$ is **non-branching** — every slot opens at most one child slot, so no
> resolved set can fork — then every configuration is linear and $\sqsubseteq$ coincides with
> $\preceq_{\mathrm{pre}}$.

*Proof.* If $c$ is a prefix of $d$, then $\mathrm{config}(d)$ resolves every slot $\mathrm{config}(c)$
resolves with the same selection (as $d$ extends $c$), while $\mathrm{config}(c)$ is $0$ on the deeper
slots, so $\mathrm{config}(c) \sqsubseteq \mathrm{config}(d)$. Conversely, if $\mathrm{config}(c)
\sqsubseteq \mathrm{config}(d)$ with both linear, then $\mathrm{config}(c)$'s single chain agrees with
$\mathrm{config}(d)$ within its depth and, being one path, is an initial segment of $\mathrm{config}(d)$'s
chain — i.e. $c$ is a prefix of $d$. The image is the linear configurations by construction. If $K$ is
non-branching, each resolved set, being root-connected with no fork, is a single chain, so every
configuration is linear and the two orders agree. $\qquad\blacksquare$

The point of Theorem 3 is that $\sqsubseteq$ is the correct *general* order. As soon as a slot opens more
than one child slot — so that several sibling slots may be resolved independently — configurations
*branch*. This branching across distinct slots is already present in the base model of Section 2.2 (it is
*not* the per-slot set enrichment of Remark 1, which is a different generalization — the same
same-slot-vs-sibling-slot caution noted there). Consider two
coordinates that share a prefix and then descend into two **different child slots** opened by that prefix —
sibling *slots*, not two selections of the same slot. They are prefix-incomparable, yet under $\sqsubseteq$
they are **consistent**: the configuration resolving both sibling branches is a common upper bound, so by
bounded-completeness (Theorem 1(vi)) they have a join in $D$, which no single coordinate names. (Two
coordinates that instead pick *different selections at the same slot* are inconsistent — no configuration
can carry two values at one slot — and correctly have no upper bound; the join claim is only for divergence
into distinct sibling slots.) Thus $\sqsubseteq$ is the bounded-complete generalization of the depth order,
and reduces to it exactly in the non-branching case.

### 3.6 The carrier is exactly Crystal Ball's coordinate encoding

The configuration space $(D,\sqsubseteq)$ formalized in Section 2.2 is not an analogy for the encoding of
Section 1 — it *is* that encoding, under the following identification:

- a **slot** is a coordinate **level** (a kernel position), reached by the unique chain of selections that
  opens it;
- the slot's value domain $\mathrm{Val}_s = \{0\}\cup\{1,\dots,\mathrm{arity}(s)\}$ is exactly the level's
  digit reading: `0` is superposition (the class marker, the order-theoretic bottom of the slot), and a
  selection $i$ (possibly reached by wrap-accumulation) is an instance;
- **drill** (`8` … `88`) is descent into a selected node's produced subspace — the opening of the child slots
  beneath that selection — and the requirement that every drill be closed is exactly *tree-consistency*: a
  slot is resolved only when the selections that open it are in place;
- the **specialization order** of Section 2.3 is the per-slot digit order $0\sqsubseteq v$ lifted pointwise
  over the levels.

Under this identification the slot tree $K$ is the space's necessitation structure and a configuration is a
(partial) coordinate; the *finite* configurations of Theorem 1(iv) are exactly the finitely-resolved
coordinates. Therefore Theorems 1–3 are statements about Crystal Ball's coordinate encoding directly: **the
encoding, ordered by specialization, is a Scott domain.**

Finally, `coordToReal` addresses this carrier on the real line. On **canonical** coordinates — each selection
written in its minimal digit form (no redundant trailing wrap), with `8988`/`90`/`900` reserved for
punctuation — distinct coordinates have distinct digit strings, so `coordToReal` assigns them distinct decimal
expansions; it is an **injective address** of the carrier into $[0,1)$, which is the precise sense of
"the encoding *into the real line*." Two cautions, stated rather than swept aside: (i) the order that makes the
carrier a Scott domain is the **specialization order**, not the numeric order $\le$ of $[0,1)$ —
`coordToReal` is an address, not an order-isomorphism onto the reals; and (ii) the address is the formal
decimal expansion of the digit string (a coordinate ending in a superposition `0` shares a numeric value with
its `0`-trimmed form — the ordinary decimal-tail degeneracy), a property of the numeric presentation that is
immaterial to the order-theoretic result above.

------------------------------------------------------------
## 4. Conclusion and scope
------------------------------------------------------------

We have shown that Crystal Ball's real-line coordinate encoding — the digit grammar of Section 1, with `0` as
the class/superposition marker and `1`-`7` as instance selections, drill nesting, and the `coordToReal`
address — forms, under the specialization order, a **Scott domain**: bounded-complete, algebraic, with a least
element (Theorem 1); decoding and composition over it are Scott-continuous (Theorem 2); and its linear
coordinates carry exactly the prefix order (Theorem 3). The identification of Section 3.5 makes these results
statements about the encoding itself, and `coordToReal` is a faithful address of that structure into $[0,1)$.

This is the entire claim. The encoding is a sound *platform*: a well-behaved domain of partial observations
with limits, finite approximants, and continuous reading. Constructions that operate over this platform — a
specialization recursion that descends the domain, a read-off of a coordinate into a typed relational
structure, and the convergence behaviour of a generator working inside it — are **out of scope for this
result** and are not asserted here. They are recorded separately as prospective extensions, to be established
on this platform as their own theorems
(`observation_dcpo_proof.GRAFTED-THEORY-EXTENSION-REF-2026-06-06.bak.md`).
