# Gradient-Guided Annealing: Steering a Stochastic Generator with an Instantiated Scott-Domain Backdrop

## Abstract

We describe a type of computation we call **gradient-guided annealing**. A stochastic generator — a large
language model (LLM) — produces content, but it produces it *inside* a structure (a **configurator**) whose
execution **instantiates** a mathematical gradient: an information-order with limits and a well-founded
notion of closure, formally a **Scott domain**. The configurator does not *compute* the order; it
*instantiates* it — the way making a decision instantiates a directed acyclic graph, or a crowd standing in
formation instantiates a geometric figure whose properties then constrain those inside it. Because the
gradient is instantiated rather than computed, it is *real for the generation*: it acts as a logic-backdrop
that steers the generator's stochastic output toward coherent, closed forms. We support the thesis with two
pillars, both already established. The **empirical pillar**: an LLM generating against a real structural
backdrop, with the goal of producing a structure-preserving correspondence, is measurably steered by it,
yielding a controllable configurator whose knobs are the open positions and whose target is structural fit.
The **mathematical pillar**: the backdrop is a sound gradient — we prove (for the class of tree-structured,
finitely-branching slot schemas defined here) that the configuration space is a Scott domain, that the
read and compose operations are Scott-continuous under explicit locality hypotheses, that the natural
"depth/prefix" order is the linear restriction of the information order, and that a closing operator's
**crowning** (closing cleanly into a self-reproducing form) is a decidable one-step property — with three
genuinely distinct, concretely-witnessed outcomes (crown, stable-but-obstructed, no-closure). We close by
delimiting scope honestly: the generator is steered toward **structural coherence ("effective-truth")** —
that is **Phase 1**, the subject of this document — whereas being **true about the world** is a separate,
sequential **Phase 2** in which the same generate-against-backdrop paradigm runs on a *social* backdrop.

------------------------------------------------------------
## 1. The type of computation, and an opening exhibit
------------------------------------------------------------

### 1.1 An opening exhibit: a mathematically-structured knowledge object

Consider a concrete run of a configurator. The user wants a structured knowledge object — say, a map of the
ways one might organize an argument. The configurator presents a tree of positions. At the top, three
structurally-parallel **branches** are available; one branch drills into two structurally-parallel
**sub-options**. A large language model fills in what each branch and sub-option *means* — the semantic
labels, the prose, the domain content. Around that generated content, the configurator computes, exactly:

- **Per-position orbits.** The three top branches have the same shape (each opens the same kind of
  sub-structure), so they form one **orbit** — a class of structurally-interchangeable positions; the two
  sub-options form another. The grouping is computed from the *structure* (a recursive fingerprint of each
  position's subtree), not from the meanings.
- **A symmetry group.** The structural interchangeability is a group action: the symmetric group on the
  three branches times the symmetric group on the two sub-options, a group of order $3! \cdot 2! = 12$.
- **The orbit–stabilizer relation.** For any one branch, (size of its orbit) $\times$ (size of the subgroup
  fixing it) $=$ the order of the whole group: $3 \times 4 = 12$. The arithmetic is exact.
- **A real-number address.** The digit encoding places each fully-specified configuration at a definite
  point of the real line, so configurations can be named, compared, and enumerated as numbers.
- **A total count.** The number of distinct fully-specified configurations is computed and reported.

Every one of these quantities is computed and correct. None of them generated the content: the *meanings*
came from the language model. But the mathematics **held the shape** — it grouped the structurally-parallel
items into orbits, typed them by their symmetry, placed each configuration on the line, and counted the
whole space. The result is a *mathematically-structured knowledge object*: stochastically-generated content
sitting in an exact combinatorial-geometric frame. (The specific content here is illustrative; the point is
the relationship — mathematics structuring language-model output — not any particular subject matter.)

### 1.2 The thesis: gradient-guided annealing

The exhibit displays a *type of computation*. A stochastic generator emits content, but inside a structure
that supplies an exact frame for that content; the generation is then *steered* by the frame toward forms
that fit it. We call this **gradient-guided annealing**: the structure presents a gradient (an order with a
direction of "more resolved / more closed"), and generation proceeds by settling — annealing — along that
gradient toward a closed configuration, the way a physical system settles toward a low-energy state.

The crucial point is *how* the structure relates to the gradient. **The structure does not compute the
gradient; it instantiates it.** Two everyday analogies fix the distinction:

- *Deciding instantiates a graph.* When you make a sequence of dependent choices, you do not first compute a
  directed acyclic graph and then consult it; the act of deciding *is* the instantiation of that graph. The
  graph is real — it has a topology, a reachability structure — and that structure constrains what can come
  next, even though nothing ever "computed" it as an object.
- *A formation instantiates a figure.* A crowd standing in rows instantiates a rectangle. No one computed
  the rectangle; yet the rectangle is there, with definite properties (rows, columns, a perimeter), and
  those properties constrain the people inside it (where the corners are, who is adjacent to whom).

The configurator is like that. Its execution — opening positions, grouping them by structure, recording
selections — *instantiates* an information-order over configurations. Nothing in it compares two
configurations or "evaluates the order"; the order is simply *present in the structure the way the
rectangle is present in the formation*. And because it is present, it is **real for the generation**: it
constrains and directs what the generator can coherently produce next. *That the gradient is
instantiated-not-computed is the point of this type of computation, not a caveat about it.* An instantiated
gradient steers without being run.

### 1.3 The two pillars

The thesis rests on two supports, developed below.

- **Pillar A — the steering is real (empirical), Section 4.** A language model generating against a *real
  structural backdrop*, with the goal of producing a structure-preserving correspondence, is measurably
  steered by that backdrop. The interaction is a *configurator*: the open positions are knobs, and the
  generator fills them toward structural fit. The requirement — established by what fails — is that the
  backdrop must consist of *real structural analogies that cover every condition*; an instruction to "match
  this abstract piece of mathematics" gives nothing to settle toward, whereas a real structural backdrop
  does.
- **Pillar B — the backdrop is a sound gradient (mathematical), Sections 2–3.** The information-order the
  configurator instantiates is genuinely a Scott domain: it has limits, finite approximants, and a
  well-founded notion of closure. The configurator's knobs are the slots; the gradient is the information
  order; the "click into place" is closure (crowning). We prove the order-theoretic facts that make the
  backdrop a sound gradient, and we make precise, and decide, when a structure closes cleanly.

We present Pillar B (Sections 2–3) before Pillar A (Section 4) so that the precise object — the Scott domain
and its closing operator — is in hand when we describe the empirical steering; the reader who prefers the
motivation first may read Section 4 immediately after this introduction.

------------------------------------------------------------
## 2. Preliminaries (Pillar B)
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

> **Terminology.** The word *finite* does double duty in this area. We reserve **compact** for the
> order-theoretic finite elements just defined, and we say **finite schema** (Section 2.2) for a schema
> with finitely many slots. Where confusion is possible we write "compact element" or "finitely-resolved
> configuration" for the former and "finite schema" for the latter.

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
1); only the *arity* of each slot is required finite. Section 3.5 will additionally assume the schema finite.

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

A remark on representation. Each configuration $\sigma$ may be *encoded* as a finite or infinite string of
digits $\mathrm{enc}(\sigma)$ recording the selections along $\mathrm{res}(\sigma)$, with reserved
digit-patterns serving as structural punctuation (marking where a slot is drilled into, where a subtree
closes, and so on). Only the marker $0$ and the instance digits carry order-theoretic content; the
punctuation patterns *build* the tree and the values and are not themselves elements of $D$. The encoding
is faithful — $\sigma$ is recoverable from $\mathrm{enc}(\sigma)$ — but the configurations *are* the
functions $\sigma$, not their digit strings; we never treat a raw string as an element of $D$. The encoding
is what places each configuration at a point of the real line (the opening exhibit); the proofs refer
solely to the functions $\sigma$ and the order defined next.

### 2.3 The observation (specialization) order

Define $\sqsubseteq$ on $D$ by
$$\sigma \sqsubseteq \tau \quad\Longleftrightarrow\quad
\text{for every slot } s,\ \ \sigma(s) = 0 \ \text{ or } \ \sigma(s) = \tau(s).$$
In words: $\tau$ has observed at least as much as $\sigma$ and agrees with $\sigma$ wherever $\sigma$ has
committed; $\tau$ may resolve slots $\sigma$ left at $0$ (and thereby open and resolve further slots).
This is the pointwise order induced by the per-slot flat orders of Section 2.2. It is the gradient the
configurator instantiates: "less resolved" below "more resolved."

We record two derived constructions used repeatedly.

> **Slotwise union.** For $A \subseteq D$, define a function $\bigsqcup A$ by
> $(\bigsqcup A)(s) = a(s)$ for some $a \in A$ with $a(s) \neq 0$, if any such $a$ exists, and
> $(\bigsqcup A)(s) = 0$ otherwise. (Lemma 1 below shows this is well-defined when $A$ is directed or
> consistent.)

> **Bottom.** Let $\bot$ be the configuration that is $0$ at every slot — total ignorance. Its resolved
> set is empty, hence root-connected, so $\bot \in D$.

------------------------------------------------------------
## 3. The instantiated gradient is a sound Scott domain (Pillar B)
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
> slots, which the base model already allows). Replacing each per-slot flat factor by the lattice of
> *subsets* of $\{1, \dots, \mathrm{arity}(s)\}$ ordered by inclusion keeps $D$ a Scott domain, because
> each such lattice is *finite* (the arity is finite), hence trivially a bounded-complete algebraic dcpo.
> (If a slot's choice space were infinite, "finite subsets ordered by inclusion" would fail to be
> directed-complete; the correct fix would then be the ideal completion with finite subsets as the compact
> elements. We do not need it, since all arities are finite.)

### 3.3 Reading and composing configurations are continuous

The configurator must *read* a configuration into content and *compose* configurations (one supplies
context to another). We show both operations respect the gradient — they are Scott-continuous — under
explicit locality hypotheses.

A configuration is *decoded* into content by interpreting its resolved selections against a fixed **meaning
structure**, which we model as itself a slot tree $M$ — formally the same kind of object as $K$ (Section
2.2) — so that $C := D(M)$, the configurations of $M$ ordered by its own observation order $\sqsubseteq_C$,
is by Theorem 1 a Scott domain with bottom the all-$0$ configuration. Each content position is a slot of
$M$, reached by a finite chain of selections. In the **reflexive case** the meaning structure is the schema
itself, $M = K$, whence $C = D$ and decoding is an endomap; Theorem 2(b) below is stated in this case.

We define $\mathrm{decode} : D \to C$ to be any map satisfying the following two stipulated properties,
which fix how a configuration is read and how partiality is handled. (These are *defining properties* of
the read map, not consequences of the carrier alone; the continuity results are stated relative to them.)

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
> implementation's read/compose operations satisfy them is the faithfulness question of Appendix A; the
> dependence of (b) on the exact composition is the most delicate point and is flagged there.

We emphasize what Theorem 2(b) does *not* assert: $\mathrm{app}$ is a continuous *map*, not necessarily an
*order-embedding* of $D$ into its own function space. We return to this in Section 6.

### 3.4 The depth order is the linear restriction of the observation order

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
*not* the per-slot set enrichment of Remark 1, which is a different generalization). Consider two
coordinates that share a prefix and then descend into two **different child slots** opened by that prefix —
sibling *slots*, not two selections of the same slot. They are prefix-incomparable, yet under $\sqsubseteq$
they are **consistent**: the configuration resolving both sibling branches is a common upper bound, so by
bounded-completeness (Theorem 1(vi)) they have a join in $D$, which no single coordinate names. (Two
coordinates that instead pick *different selections at the same slot* are inconsistent — no configuration
can carry two values at one slot — and correctly have no upper bound; the join claim is only for divergence
into distinct sibling slots.) Thus $\sqsubseteq$ is the bounded-complete generalization of the depth order,
and reduces to it exactly in the non-branching case.

### 3.5 The closing operator and a decidable one-step closure criterion

**Standing assumption for this subsection.** The schema $K$ is **finite**: finitely many slots (hence, with
finite arity, finitely many configurations, and finite subtrees). Theorems 1–3 above need no such
restriction — in particular they cover infinite slot trees, where the non-compact elements of Theorem 1(iv)
live — but the closure analysis below is a statement about finite schemas only.

The configurator's "click into place" — the moment a partially-built structure *closes* into a finished,
self-consistent whole — is enacted by a **self-abstraction operator** $R$. We describe the real operator
faithfully.

**$R$ abstracts a schema by its orbit structure.** Given a finite schema, $R$ groups, at each slot, that
slot's children into **orbits** by structural isomorphism of their subtrees — two children lie in the same
orbit iff their subtrees have the same **kind** (the same arity-and-opening structure, recursively, per
Section 2.2). Iterating $R$ forms a tower $K = R^0(K), R^1(K), R^2(K), \dots$. The operator has two
branches, and is **not uniformly growing**:

- **Single-slot.** If the schema is a single slot together with its children, $R$ records that slot's orbits
  directly beneath the root, producing a one-slot schema whose children are the orbits. When the children
  already form a single orbit (all the same kind), $R$ reproduces the same canonical form — there $R$ is
  **idempotent**.
- **Multi-slot.** If the schema has several slots, $R$ wraps each slot as a node carrying its orbit
  decomposition as an *added* layer — the description **grows**.

So $R$ is idempotent on a clean single-orbit slot and growing on multi-slot structure; it is neither
uniformly idempotent nor uniformly growing. (A decomposition that instead replaced the children by one
representative per kind would trivialize the analysis — every schema would close immediately — and is not
the operator under study.)

> **Type-closure (with the induced opening relation made precise).** $R$ maps a finite schema to a finite
> schema. Each original slot $s$ is retained; beneath it $R$ inserts one **orbit node** per group of $s$'s
> children, and the original children are re-attached beneath their orbit node. The induced opening
> relation is explicit: the parent selection that opened a child $c$ now opens the orbit node containing
> $c$; that orbit node, in turn, opens its member children, indexed within the orbit. Each orbit node has
> finite arity (the number of its members), the root and the finite-arity discipline are preserved, and the
> result satisfies the four defining clauses of a slot tree. Hence $R(K)$ is again a finite schema of the
> same type, $R$ can be applied again, and the tower $K, R(K), R^2(K), \dots$ is well-typed.

**$R$ is a terminal, closing act.** Applying $R$ *declares* a closure: it caps the abstraction at a level
and closes the boundary of the structure. It is not a process that proves an infinite descent halts; the
closure is *enacted* by the act of reifying-and-locking, not established by a convergence theorem. This is
the nature of a terminal operation — it closes by declaration — and it is why, below, the absence of a
proven universal halting bound for an iterative search is *not a hole*: a closing act does not owe a descent
proof.

Each finite schema has a **canonical signature** $\mathrm{canon}(K)$ — a normal-form description of its
orbit structure — with $\mathrm{canon}(K) = \mathrm{canon}(K')$ iff $K, K'$ are isomorphic.

**The obstruction $\mathfrak{o}$.** Each application of $R$ is a *local* symmetrization: it groups, slot by
slot, children that are structurally alike. Track, across consecutive levels of the tower, the **total
number of orbits**. A step **lifts** — its local symmetrization is globally consistent — when it does
**not** reduce the orbit total: it preserves or refines the structure. A step **fails to lift** when the
orbit total strictly **decreases**: the symmetrization has merged distinct orbits into fewer, irreversibly
losing structural dimension. (A repetition of the canonical form accompanied by a change in the
configuration count is likewise non-lifting — a *false* fixed point.) Define
$$\mathfrak{o}(K) = \#\{\, \text{non-lifting steps in the tower of } K \,\}.$$
Then $\mathfrak{o}(K) = 0$ exactly when every symmetrization the closing operator performs is globally
consistent — no step collapses distinct structure into less. This requires **no external node-labels**: the
merged orbits are genuinely distinct subtrees, and the obstruction is the intrinsic, irreversible reduction
in orbit count. Because $K$ is finite, all of the quantities involved — $R$, the canonical form, and the
orbit, configuration, and slot counts — are computable, so $\mathfrak{o}$ is a computable function of $K$.

> **Definition (Crowning).** A finite schema $K$ **crowns** iff the tower reaches a level at which (i) the
> canonical signature repeats (a stable form), (ii) the configuration count and the slot count are also
> stable, **and** (iii) $\mathfrak{o}(K) = 0$ (no non-lifting step occurred up to that level). A crowned
> schema has stabilized into a self-reproducing form, reached without any collapse. Crowning is canonical,
> configuration, and slot stability together with zero obstruction — *not* schema-isomorphism: because $R$
> grows on multi-slot structure, $R(K) \cong K$ need not hold at a crown.

> **Proposition 5 (Crowning is decidable).** For each finite schema $K$, whether $K$ crowns is decidable.

*Proof.* Each tower level is a finite computation on a finite schema: the canonical form, the orbit,
configuration, and slot counts, and hence $\mathfrak{o}$, are all computable. The crown verdict is reached
when the canonical form **first repeats**: at that level one tests the configuration and slot counts for
stability and compares the accumulated non-lifting count to zero. This is a finite comparison, so crowning
is decided in finitely many steps. $\qquad\blacksquare$

**Three genuine outcomes.** Because $R$ is a closing act, applying it to a finite schema yields exactly one
of the following, each with a concrete minimal witness.

1. **Crown** — the canonical, configuration, and slot counts stabilize with $\mathfrak{o} = 0$. *Witness:* a
   root with $N$ structurally-identical leaf children (a single slot, one orbit of size $N$). $R$ groups
   them into one orbit and reproduces the same canonical form; the orbit total goes $1 \to 1$, the
   configurations $N \to N$, and no collapse occurs, so $\mathfrak{o} = 0$ — it crowns. Robust across
   $N = 4, 7, 12$.
2. **Stable-but-obstructed** — the canonical form stabilizes yet $\mathfrak{o} > 0$. *Witness:* a root with
   $k$ structurally-**distinct** children ($k$ different subtrees). At the first level there are $k$
   singleton orbits; the next application of $R$ merges them into one orbit of size $k$ — the orbit total
   drops $k \to 1$, a non-lifting collapse, so $\mathfrak{o} = 1$. The canonical form then repeats (a stable
   signature), but the crown criterion fails because a collapse occurred: the schema does **not** crown
   despite stabilizing. Exhibited at $k = 3$ and $k = 6$, so it is a general pattern, not a one-off. *This is
   the witness that makes the obstruction meaningful* — a stable-signature schema the criterion correctly
   refuses to crown — and it needs no external labels: the children are genuinely distinct subtrees, and the
   obstruction is the intrinsic, irreversible reduction in orbit count.
3. **No closure (halt)** — reification produces a node that cannot close. *Witness:* any genuinely
   multi-slot schema (depth $\ge 2$). Wrapping a single-orbit slot yields a node with exactly one child,
   which the closing discipline forbids (a node that closes must offer at least two alternatives); the
   closing act halts with no stable fixed point.

Hence **"not every schema crowns" is honestly true**: outcomes 2 and 3 are genuine non-crown closures, each
realized by a concrete minimal schema, and the obstruction gate $\mathfrak{o} = 0$ is part of the decision,
not a defect.

> **Proposition 6 (Depth-1 uniform schemas crown).** A single root slot with finitely many
> structurally-identical children crowns: its children form one orbit, $R$ reproduces the canonical form
> (orbit total $1 \to 1$, no collapse), and no non-lifting step occurs, so $\mathfrak{o} = 0$.

*Proof.* The children, being the same kind, form a single orbit; $R$ records that one orbit directly beneath
the root and reproduces the same canonical form. The orbit total goes $1 \to 1$, the configuration and slot
counts are stable, and no step reduces the orbit total, so $\mathfrak{o} = 0$. Hence $K$ crowns.
$\qquad\blacksquare$

**Termination of an iterative search (open, and fine).** The crowning *criterion* is one step (Proposition
5). If one instead *iterates* $R$ in search of a crowned form, the iteration is observed to reach
halt-or-stable within a small number of steps — at most two across every finite schema tried (symmetric,
asymmetric, deep, and distinctly-identified): single-slot uniform schemas are idempotent at the first step,
and multi-slot schemas quickly produce an unclosable node and halt. We do **not** claim a proven universal
bound on the number of growing steps, and we found no unbounded-growth witness; a universal bound is
plausible but is left as a residual obligation, not asserted. This is exactly consistent with $R$ being a
terminal, closing operation: the closure is declared, not proven to be reached by descent, so the absence of
a descent bound is the expected character of the operator, not a gap in the result.

------------------------------------------------------------
## 4. The steering is real (Pillar A)
------------------------------------------------------------

Pillar B established that the configurator instantiates a sound gradient — a Scott domain with limits and a
decidable notion of clean closure. Pillar A is the complementary, empirical fact: a stochastic generator
working against that instantiated backdrop *is measurably steered by it*.

**The configurator as a controllable interaction.** The open positions of a partially-built structure are
**knobs**; the language model fills them with content; the structural backdrop scores the fit. The
generator's goal is not free composition but a **structure-preserving correspondence**: produce content that
*fits the form* — that respects the orbits (structurally-parallel positions get parallel content), the
opening relation (a choice unlocks exactly the sub-positions it should), and closure (the object reproduces
its own shape, $\mathfrak{o} = 0$). The comparison the backdrop affords — "given these orbits, supply more in the
same shape"; "are these really one orbit, given this finer distinction?" — is precisely the signal that
*guides* the next generation. The result is a controllable gradient: turning a knob (resolving a position)
moves the object along the order toward fit, and the generator anneals toward a closed configuration.

**What makes the steering work, established by what fails.** The backdrop must be **real structural
analogies that cover every condition** — a frame against which every position the generator must fill has a
genuine structural counterpart to settle toward. An instruction of the form "make this content equal to
*this abstract piece of mathematics*" does **not** steer: there is nothing to anneal toward, because an
abstract statement supplies no per-position structural target the generator can match against. A real
structural backdrop — one that, like the configurator's orbit/closure structure, presents an actual shape
for every condition — *does* steer, because each open position has a concrete counterpart and the
fit/closure check returns a real gradient signal. The configurator's orbit-decomposition-and-closure loop is
one instance of such a backdrop: it always presents, at every position, an exact structural target (the
orbit a new child must join, the closure the object must reproduce).

In short: Pillar B says the gradient *is sound*; Pillar A says generation *is genuinely steered* by it. The
instantiated order is not an inert description sitting beside the generator — it is a live constraint that
shapes what the generator coherently produces.

------------------------------------------------------------
## 5. How to do it: the configurator loop
------------------------------------------------------------

The method that follows from the two pillars is a single loop.

1. **Present the backdrop.** Build (or expose) the structural frame: the slots, their kinds, the opening
   relation, the orbits. This is the instantiated gradient (Pillar B).
2. **Generate against it.** Have the language model fill the open positions with content aimed at structural
   fit — content that respects the orbits and the opening relation.
3. **Check fit and closure.** Read the result (the decode map) and test it against the backdrop: does it
   reproduce its own form ($\mathrm{canon}(R(K)) = \mathrm{canon}(K)$)? Is it obstruction-free
   ($\mathfrak{o} = 0$)? The crowning criterion (Proposition 5) is a decidable check.
4. **Iterate.** If it does not yet close — there is a residual obstruction, or a position is unfilled or
   ill-fitting — feed that gradient signal back ("supply more in this orbit"; "this distinction breaks the
   symmetry") and generate again. Repeat until the object crowns or the criterion reports a genuine
   non-closure (outcome 2 or 3), which is itself information.

The loop is gradient-guided annealing made operational: generate, check fit/closure against the instantiated
order, settle. The knobs are the slots; the gradient is the information order; the click-into-place is
crowning.

------------------------------------------------------------
## 6. Honest scope, and what is proved, conjectural, or open
------------------------------------------------------------

### 6.1 Effective-truth (Phase 1) versus world-truth (Phase 2)

It is essential to say precisely what the generator is steered *toward*. The gradient of this document
measures **structural coherence**: whether generated content fits the form — respects the orbits, the
opening relation, and closure. Call this **effective-truth**: the content is *internally* coherent and
admissible against the structural backdrop. Effective-truth is **Phase 1**, and it is the entire subject of
this document. Crowning is the Phase-1 success condition: the object has closed cleanly into a
self-consistent whole.

Being **true about the world** is a separate, *sequential* concern — **Phase 2**. A coherent, crowned object
is then put before *other observers* — a market, a community, a body of peers — and judged by them; one
climbs a second gradient, the gradient of *socially-constructed* proof, by the *same* paradigm
(generate-against-backdrop, take the feedback, converge), but now the backdrop is **social** rather than
structural. We name Phase 2 only to delimit Phase 1: nothing in Sections 2–5 establishes world-truth, and we
do not smuggle it into the Phase-1 results. A crowned object is *coherent*, not thereby *correct about the
world*; that is the next phase, on a different backdrop, and is out of scope here.

### 6.2 What is proved

For the class of tree-structured, finitely-branching slot schemas defined here: the configuration space is a
Scott domain (Theorem 1); under explicit locality hypotheses, decoding is Scott-continuous and, in the
reflexive case under (C1)–(C3), application gives a Scott-continuous map $\mathrm{app} : D \to [D \to D]$
(Theorem 2); the depth order is the linear restriction of the observation order (Theorem 3); and for finite
schemas the closing operator's *crowning* is a decidable one-step property with three genuine,
concretely-witnessed outcomes (Section 3.5, Propositions 5–6). Together these say the instantiated backdrop
is a sound gradient with a decidable clean-closure test.

### 6.3 What is conjectural

Theorem 2(b) gives $\mathrm{app}$ as a continuous *map*, not an *embedding* of $D$ into its function space
$[D \to D]$ (the reflexive case $C = D$). An embedding would, via the standard inverse-limit construction,
yield a reflexive isomorphism $D \cong [D \to D]$. The obstruction is that $\mathrm{decode}$ may *fold*:
distinct configurations can decode to comparable content, so $\mathrm{decode}$ — and hence $\mathrm{app}$ —
need not be order-reflecting. Call a configuration **fold-free** if the encode/decode representation
round-trip (Section 2.2, Appendix A) is the identity at it. We **conjecture** that $\mathrm{app}$ restricts
to an embedding exactly on the fold-free subspace, and we further **conjecture** that this fold-free subspace
coincides with the obstruction-free subspace $\{\mathfrak{o} = 0\}$. The second conjecture is a *substantive
bridge*, not a definition: $\mathfrak{o}$ is defined on schemas via the non-lifting (orbit-collapse) count
of the closing operator's tower (Section 3.5), whereas fold-freeness is defined on configurations via
injectivity of the read/round-trip map
(Sections 2.2–3.3); these are a priori different objects, and asserting their coincidence is the content of
the conjecture. We do **not** claim either. The crowning results of Section 3.5 do not depend on this.

### 6.4 What is open, and what is explicitly not claimed

*Open — compositional stability.* Crowning is a property of a single finite schema. Suppose several schemas
have each crowned. Does *composing* them — assembling a larger structure whose parts are crowned schemas —
yield a structure that again crowns, or can a fresh obstruction appear at the seams? *It remains open whether
crowning is preserved under composition.* A positive answer would let crowned components be combined with
foresight; a negative answer would locate composition as where new obstructions are born.

*Open — a universal halting bound for the iterative search.* As noted in Section 3.5, iterating the closing
operator reaches halt-or-stable in a small number of steps in every case tried, but no universal bound is
proven; this is a residual obligation, consistent with the terminal character of the operator.

*Explicitly not claimed.* We do not claim that iterating the closing operator *builds* the function-space
domain $[D \to D]$; it performs orbit decomposition, which grows polynomially in the schema's size, whereas
the function space grows super-exponentially. So the crowning fixed points of the closing operator (Section
3.5) are a *different* notion from the reflexive fixed point an embedding $\mathrm{app}$ would furnish (the
conjecture of 6.3); we keep the two apart so that the proved result (decidable crowning) is not mistaken for
the unproved one (a reflexive isomorphism $D \cong [D \to D]$).

------------------------------------------------------------
## 7. Conclusion
------------------------------------------------------------

We have described a type of computation — **gradient-guided annealing** — in which a stochastic generator
produces content inside a structure whose execution *instantiates* (does not compute) a mathematical
gradient, and is thereby steered toward coherent, closed forms. Two pillars support it. Empirically, a
language model working against a real structural backdrop is measurably steered by it, yielding a
controllable configurator whose knobs are the open positions and whose target is structural fit.
Mathematically, that backdrop is a sound gradient: the configuration space is a Scott domain (limits, finite
approximants, well-founded structure), reading and composing configurations are Scott-continuous, the depth
order is the linear restriction of the information order, and the closing operator's *crowning* is a
decidable one-step property — with three genuinely distinct, concretely-witnessed outcomes, so that "not
every structure closes cleanly" is honestly true and the obstruction gate is meaningful. The instantiated
gradient is real for the generation precisely because it is instantiated rather than computed: like the
graph a decision instantiates or the figure a formation instantiates, it constrains what happens inside it
without ever being run. What this buys is Phase-1 coherence — *effective-truth* — for stochastically
generated knowledge objects; truth about the world is a separate, sequential phase, on a social backdrop,
that we have named but not addressed. The principal open questions — whether the application map embeds the
domain into its own function space on the fold-free subspace, and whether crowning is preserved under
composition — are stated precisely above and left for future work.

------------------------------------------------------------
## Appendix A. Correspondence to an implementation
------------------------------------------------------------

The mathematical object of this paper was abstracted from a concrete configurator. We record, in prose,
which parts of the model correspond to *computations the system performs*, which are *mathematical structure
laid over the system's data*, and which are *intended but not yet built*. This is an informal correspondence;
we prove no refinement or simulation theorem, and the paragraphs below are evidence about the model, not part
of its proofs.

**Realized as computations.** The carrier is real: the configurator constructs configurations (as digit
strings over its slot trees, the encoding of Section 2.2), enforces tree-consistency when it opens child
slots, and enumerates the configurations of a *finite* schema (for an infinite slot tree the full
configuration set is not enumerable — only finite schemas are enumerated, and the infinite configurations of
Theorem 1(iv) are a mathematical, not a computed, object). Decoding is a live operation, and the
*representation round-trip* between a configuration and its digit-string encoding recovers the original; this
representation round-trip is distinct from the content map $\mathrm{decode} : D \to C$ of Section 3.3, and we
use the separate phrase to avoid conflating them. The orbit decomposition, the symmetry group, the
orbit–stabilizer arithmetic, the real-line addressing, and the total configuration count of the opening
exhibit are all computed exactly. The closing operator is real and *type-preserving* (it consumes a schema
and returns a schema of the same type), and it *grows* the description rather than collapsing it. The orbit
decomposition is computed locally per slot; the implementation compares subtrees by a bounded-depth
*fingerprint* as a stand-in for the exact subtree isomorphism of Section 3.5. This stand-in agrees with the
abstract notion once the depth bound meets or exceeds the (finite) subtree height; below that it is an
approximation, which can in principle merge genuinely distinct deep subtrees — a known limitation of the
implementation, not of the model, where (the schema being finite) subtrees are compared in full.

**Mathematical structure over the system's data.** The order $\sqsubseteq$ and the entire
directed-complete-partial-order apparatus (least upper bounds, compact elements, bounded-completeness) are
*not* runtime notions: the system produces the configurations that constitute the carrier, but it never
*compares* two configurations and has no operation that ascends the order — its state-changing operation
mutates a configuration rather than computing a supremum. This is exactly what Theorem 1 requires, and it is
the precise sense of the thesis: the gradient is *instantiated* by the structure the system builds, not
*computed* by it. Any informal claim that the system "respects the order at runtime" should be read as: the
order is well-defined over the system's live data; the system itself does not compare configurations.
Likewise the read map $\mathrm{decode}$ and the composition $\oplus$ are operations whose
locality/composition hypotheses (Section 3.3) are *assumptions the implementation must meet*, not properties
guaranteed by the carrier; checking them against a particular implementation is the faithfulness task and is
not done here.

**Crowning and termination.** The one-step crowning check (Proposition 5) is realized: a single reification,
a canonical comparison, and the obstruction check. The three outcomes are exhibited by concrete minimal
schemas — a uniform single-slot schema crowns; a single-slot schema with structurally-identical but distinct
children is stable yet obstructed (witnessed at widths $3$ and $6$); a multi-slot schema halts without clean
closure. The iterative search reaches halt-or-stable within a small number of steps on every schema tried;
we do not claim the implementation realizes a proven universal bound, because no such bound is proven — the
bound is, appropriately, not owed by a terminal closing operation.

**Intended but not yet surfaced.** Some derived reporting structure — for instance a summary of the sequence
of sub-structures a schema traverses as it closes — exists as a computable function over the live data but
is not currently exposed through the system's interface; surfacing it is a matter of wiring, not new
mathematics.

The net correspondence: the carrier and the computational mechanics (configuration construction and
enumeration for finite schemas, decoding, the exact combinatorial-geometric quantities, the type-preserving
growing closing operator, local orbit computation, one-step crowning, and the representation round-trip) are
realized; the order-theoretic layer and the locality/composition hypotheses are mathematical structure over
(or assumptions on) that realized carrier; and one derived report is intended but not yet exposed. None of
these caveats affects the theorems, which concern the mathematical object.
