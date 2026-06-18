# Bounded-Arity Annealing: How a Kernelized Generator Drives an Approximate Model to Checkable Identity

------------------------------------------------------------
## Abstract
------------------------------------------------------------

We describe a type of computation in which a stochastic generator — a large language model — operating one
fixed way inside a structured space, drives an initially **approximate** model of a domain **measurably
closer** to a checkable formal structure. The space is a configuration space we prove to be a Scott
domain (Sections 2–3). Over it runs a **single** operation — a specialization recursion we call **FLOW** —
that progressively constrains the space (a descending chain of sub-domains) while **accumulating symmetry**.
We identify symmetry-accumulation with **arity-reduction**: it keeps each generative decision near the small
arity at which the generator collapses a relation reliably — a free parameter $k$ we treat as an anecdotal
working size (Section 6), not a measured constant. Because the generator never does anything else — the
system is **kernelized**: every act it performs is one instance of the same single operation, so there is
only one process to validate — the system's improvement *is* exactly this one process, iterated, **composed**
for depth and **distributed across a team** for breadth. Each configuration
decodes to a web of typed relational statements (a foundation ontology of `is-a`, `has-part`, `produces`),
and an **external mereological reasoner** checks them. The central claim — which we frame precisely and make
**falsifiable** rather than assume — is that as the recursion reduces arity, the fraction of the decoded
structure that passes the external check **rises toward 1 (its measured asymptote)**: the gap between the
generator's approximate ("metaphorical") model and the formal structure shrinks toward zero. We do not claim
the descent *attains* identity in finitely many steps (Section 9); "rises toward 1" names the asymptote of an
empirical agreement rate, not a proved attained limit. We prove the structural facts (the Scott domain;
the encoding-to-ontology; the specialization recursion), state the empirical convergence as a measurable
hypothesis with an explicit observable, and argue that the **mechanism** is **domain-blind** — nothing in it
is specific to any one domain. Whether the *empirical* convergence transfers from one encoded domain to
another is, accordingly, a conjecture (subject to each domain's own irreducible-arity obstruction, Sections
7–8), not a corollary of that domain-blindness: a single measured instance tests the mechanism and is
suggestive evidence, not a certification of the general empirical claim.

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
  that number grows; in our own use a comfortable working size is a handful of items (a free parameter $k$,
  not a measured constant — Section 6). Symmetry-accumulation is precisely what keeps each collapse near that
  small working size. The claim the computation rests on is that, as FLOW drives the structure toward symmetry
  (hence toward low-arity collapses), the decoded ontology passes an **external** consistency check at a
  **rising rate, toward 1**. That is an observable about a running system, and Section 7 states exactly what
  to measure.

The payoff of separating them is the payoff of the whole paper: the structural support is settled, and the
empirical support is reduced to **one** measurable quantity — because the system is kernelized, there is only
one process to validate.

------------------------------------------------------------
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

We record one structural lemma here, at the point where configurations are defined; it is used repeatedly
in §3 (including in the slotwise-union and bottom constructions introduced in §2.3, which rely on its
root-connectedness facts) — a forward reference the reader may keep in mind.

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
> elements of $D$. The encoding is faithful — $\sigma$ is recoverable from $\mathrm{enc}(\sigma)$ — but the
> configurations *are* the functions $\sigma$, not their digit strings; we never treat a raw string as an
> element of $D$. The encoding is what places each configuration at a point of the real line. **Nothing
> downstream uses this:** no metric, real-line, or digit-string structure does any proof work — the proofs
> refer solely to the functions $\sigma$ and the order defined next. This remark is included only to connect
> the configurations to their string/real-line representation, and may be skipped without loss.

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
## 3. The instantiated gradient is a sound Scott domain
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

And, for the reflexive composition $\oplus : D \times D \to D$ of Theorem 2(b), the following three
**composition hypotheses**, on which part (b) is conditional (they are restated where they are used in the
proof of Theorem 2(b), and hold for the intended construction in which $\psi$ supplies the selections that
$\varphi$ leaves open below its resolved frontier):

- **(C1) Closure.** $\varphi \oplus \psi \in D$ for all $\varphi, \psi \in D$.
- **(C2) Finite determinacy.** For each content position $p$, the value $\mathrm{decode}(\varphi \oplus
  \psi)(p)$ depends only on finitely-resolved restrictions of $\varphi$ and of $\psi$ (so that, with
  $\varphi$ or $\psi$ fixed, the resulting map satisfies (Locality) in the other argument).
- **(C3) Monotonicity.** $\oplus$ is monotone in each argument separately.

### 3.4 Reading and composing configurations are continuous (conditional on §3.3)

With the hypotheses of §3.3 in place, we show both operations respect the gradient — they are
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
the ontology** — a structure-preserving correspondence that need not yet be exact. The *target* of the
computation is the state in which that correspondence becomes exact — the mathematical structure the
generator builds and the foundation-ontology structure the validator checks **coinciding**. We name this
state as the limit the empirical agreement rate is measured to approach (Sections 7, 9); we do **not** claim
it is attained in finitely many steps. "Convergence" below means this rate rising toward 1, not a proved
attainment of coincidence.

------------------------------------------------------------
## 6. The empirical engine: bounded-arity collapse
------------------------------------------------------------

What makes FLOW *work*, rather than merely be well-defined, is an operating property of the generator. We
state it as the working premise it is — not as a measurement — and we make explicit that it is **decoupled
from every theorem above**: Theorem 1 requires only that each slot's arity be *finite* (any value), so the
structural results hold whatever the generator's reliable working size turns out to be. The premise below
bears solely on whether FLOW is *practical*, not on whether the gradient it runs along is sound.

**The bounded-arity premise (empirical working assumption).** Let $k$ denote the **collapse arity** — the
number of items folded into a single invariant in one generative step. $k$ is a **free parameter**: the
configuration space imposes no fixed arity, and nothing in Sections 2–4 fixes its value. The premise is
that a language model resolves a relation among $k$ items into a definite choice **reliably when $k$ is
small**, with accuracy degrading as $k$ grows. In our own hands-on use, a comfortable working sweet-spot is
**$k \approx 3\text{–}4$**: extracting a shared invariant from three items in a single pass is reliable, four
is often still clean, and past that the generator begins to drop or blur items. We report this as an
**anecdotal operating choice from practice, not a measured constant** — there is no experiment or datum
behind a specific number, and the optimal $k$ is unknown and immaterial to the claims. Small $k$ is chosen
only for two practical reasons: one collapse is then **fast** (a single response) and **contained enough to
verify by inspection**. Larger $k$ is fully supported — by batching, stashing intermediate results, and
iterating — so the choice of a small working $k$ is a convenience, not a limit. The canonical illustration
of a single low-$k$ collapse is the stacking of a handful of cross-domain analogies into one shared
invariant.

**Symmetry is arity-reduction.** Grouping $k$ structurally-interchangeable alternatives into a single orbit
replaces a $k$-way choice with a 1-way one: the effective arity of the decision drops. So FLOW's
symmetry-accumulation is not decoration — it is the mechanism that **keeps each collapse near the small
working arity**. As the descent of Section 4 piles up interchangeable structure, the arity of the choices the
generator must make falls toward the band where, by the working premise, it is reliable.

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

> **Convergence claim (empirical — settled by measurement, by design; not a proof obligation).** As FLOW
> proceeds and the resolved arity falls toward the generator's small working size, the agreement rate **rises
> monotonically toward 1** — i.e. the fraction of the decoded structure that disagrees with the
> externally-checked foundation ontology shrinks toward zero. The asymptote (rate $\to 1$) is the *measured
> target*; we do not claim it is reached in finitely many steps (Section 9). Equivalently: the discrepancy
> between the generator's approximate model and the formal structure is measured to vanish in the limit.

This claim is **measured, not proved — and that is its complete and correct treatment, not a gap.** A statement
about how a running generator behaves is a claim about the world, and a claim about the world is settled by
observation, never by deduction from the structure. The mathematics above (Sections 2–4) is therefore not an
incomplete proof of the convergence; it is the *finished* proof of the **gradient** — the sound, domain-blind
Scott-domain structure the annealing runs along — and the convergence is the directly-observable signature of
that annealing. There is no outstanding theorem here; there is an experiment.

This is the precise content of "metaphor becomes literal." It is observable: agreement rate and resolved
arity are both measurable on a running system, and the claim is the assertion of a definite trend between
them. It is falsifiable: if the agreement rate fails to climb as arity is reduced — if it plateaus below 1,
or is uncorrelated with arity-reduction — the claim is refuted. We do **not** assert the trend here; we
isolate it as the one quantity whose measurement settles the account.

**The obstruction.** Where the agreement rate fails to climb, the cause is named: a region whose arity
**cannot** be reduced to the small working size — an **irreducible high-arity** hyperedge, one with no
symmetry to collapse it. Such a region is exactly the "does not cohere, and one can see why" case: the generator cannot
reliably resolve it, and the external check correctly refuses it. The obstruction to convergence is therefore
not mysterious; it is irreducible arity, and it is detectable in advance (a region's reducibility is a
property of its symmetry, computable before the generator is invoked) — which is what lets the good and bad
regions of a configuration space be mapped *up front*.

------------------------------------------------------------
## 8. Generality: the mechanism is domain-blind
------------------------------------------------------------

**What is domain-blind (and why that is established).** Nothing in the *mechanism* uses a property of any
particular domain. FLOW fixes points and descends; the carrier decodes to `is-a`/`has-part`/`produces`
statements; symmetry reduces arity; the external reasoner checks mereological consistency. None of these
references mathematics, or law, or biology, or any specific subject — they reference only *that the domain has
been encoded as a structured, decodable ontology*. This domain-blindness is a property of the **gradient and
the process**, and it is exactly what the structural results of Sections 2–4 establish: the Scott-domain
structure, the continuity of decode/compose, and the well-foundedness of the descent hold for any schema,
naming no domain. To that extent the construction is genuinely general — the *apparatus* is the same whatever
it runs on.

**What does NOT follow (the empirical transfer is a conjecture, not a corollary).** Domain-blindness of the
mechanism does **not** entail that the *empirical convergence* of Section 7 transfers from one domain to
another. The convergence depends on the generator's bounded-arity reliability **interacting with a given
domain's symmetry profile**, and Section 7 names precisely where that interaction can fail: an
**irreducible high-arity** region — a hyperedge with no symmetry to collapse it — is exactly a place where the
agreement rate need not climb. A domain whose ontology contains such regions is, by the paper's own Section 7,
a domain where convergence can stall. So "convergence holds for one encoded domain ⟹ it holds for any" does
**not** follow from the structure's domain-blindness; it is a **cross-domain transfer conjecture**, subject to
the same per-domain irreducible-arity obstruction as the single-domain claim. A single measured instance
*tests the domain-blind mechanism* and is suggestive evidence for the conjecture; it does not certify the
general empirical claim. What the one measurable of Section 7 validates is the process — which is indeed the
only process the system runs and does not know what domain it is on — while the *reach* of the empirical
convergence across domains remains bounded by each domain's own reducibility profile.

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
as an **empirical working premise** (an anecdotal operating assumption, with the collapse arity a free
parameter $k$; not a measured constant and not a theorem — Section 6).

**The measurable claim (Section 7) — settled by measurement, by design.** That the external agreement rate
rises toward 1 (its measured asymptote) as resolved arity falls — we do not claim identity is attained in
finitely many steps. This is the convergence; it is falsifiable and is settled by
measurement on a running system. This is **not** a deferred or missing proof: a claim about how a generator
behaves is a claim about the world, and such a claim is established by observation, never by deduction. The
mathematics above proves the *gradient* (the sound Scott-domain structure); the convergence is the observable
signature of annealing along it. Treating it as measurable rather than provable is the **correct** treatment,
not an incomplete one. The obstruction to convergence is named and detectable in advance: irreducible arity.

**Open / deliberately out of scope.** The exact functional form of the agreement-rate-versus-arity trend; and
the precise correspondence between the foundation-ontology relations and the level ladder of Section 4 —
flagged for separate treatment. We also do not claim the descent reaches a global fixed point in finitely many
steps; we claim only that each step is well-defined and information-monotone, and that the convergence is a
property to be measured along the descent. (We do **not** list "a proof of the convergence" as open: by the
preceding paragraph it is not a proof obligation at all.)

------------------------------------------------------------
## 10. Conclusion
------------------------------------------------------------

The computation is one move — fix a point, descend into the space it opens — run by a generator that is
reliable only at low arity, with symmetry accumulation as the device that keeps every move near that small
working arity, composition and teaming as the devices that scale it, and an external mereological reasoner as
the ground truth. Over a configuration space we prove to be a Scott domain, this single kernelized process
drives a decoded foundation ontology toward a state we make precise and measurable: **agreement with the
external check rising toward 1** (its measured asymptote, not a proved attained identity). Because the
*mechanism* is domain-blind — a fact the structural results establish — a single measured instance tests that
mechanism and gives suggestive evidence for cross-domain transfer; whether the *empirical* convergence carries
to another domain remains a conjecture bounded by that domain's own irreducible-arity profile (Section 8), not
a corollary of domain-blindness. The structural half is proved; the empirical half is reduced to one
observable; and the two are kept strictly apart so that neither is mistaken for the other.

