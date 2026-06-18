# Observed-Configuration Spaces are Scott Domains, with a Decidable Self-Stabilization Criterion

## Abstract

We study the space of *partial observations* of a tree-structured collection of choices. Each
position (a *slot*) in the tree is either left at a *class level* — its kind is fixed but no
particular instance is chosen — or *specialized* to one of finitely many instances; specializing a
slot may open further slots beneath it. Ordering these configurations by "has observed at least as
much," we prove that the resulting space is a **Scott domain**: a bounded-complete algebraic
directed-complete partial order with a least element. This holds for the class of tree-structured,
finitely-branching slot schemas defined below, with arbitrarily many (possibly infinitely many)
slots; we do not assert it of every structure one might informally call an observed-configuration
space. We then prove that the natural map that *decodes* a configuration into content, and the
natural map that *composes* two configurations, are **Scott-continuous**, so that limits of
increasing observations are respected — both relative to explicitly stated locality hypotheses on
those operations. We show that a "depth/prefix" order, under which one observation extends another by
drilling deeper along a single path, is exactly the restriction of the observation order to linear
(non-branching) configurations. Finally, for **finite** schemas, we analyze a *self-abstraction*
operator that replaces a schema by its own internal symmetry decomposition, and prove that whether
iterating this operator *stabilizes* a schema into a self-reproducing fixed point — which we call
**crowning** — is **decidable for each schema**. We claim only decidability of crowning, not that
every schema crowns, and we separate what is proved from what remains conjectural, including whether
composing several stabilized structures preserves stability.

------------------------------------------------------------
## 1. Introduction
------------------------------------------------------------

Many systems build knowledge incrementally: they begin in a state of near-total ignorance and
progressively commit to more and more specific descriptions, where each commitment can unlock further
questions. We model this with a fixed *tree of slots*. A slot is a position that can be filled. At any
moment a slot is either left **unobserved** — we know its *kind* but have not selected a particular
*instance* — or it is **specialized** to one of finitely many alternatives. Choosing an alternative may
*open* child slots (new positions that only become meaningful once the parent has been decided). A
**configuration** is a complete snapshot of such a state: a value at every slot, where the value is
either the unobserved marker or one specific instance, subject to a consistency rule that forbids
specializing a slot before the slots that open it.

There is a natural order on configurations: one configuration is *below* another when the second has
observed at least as much as the first and never disagrees with a commitment the first already made.
The minimal element is total ignorance (every slot unobserved); going up the order means resolving
unobserved slots into instances. This is an **information order**, in the precise sense used in domain
theory.

The central question of this paper is whether this *observed-configuration space* has the structure of
a **Scott domain**. The answer matters because Scott domains are exactly the setting in which
information orders behave well: increasing chains of observations have limits, every element is
approximated by its finite (fully written-down) parts, and *consistent* observations — those that
share a common upper bound — can always be merged into a least common refinement. Concretely, this is
what makes it sound, *in an order-theoretic sense and in principle*, for a system to compute over such
a space, to take limits of unbounded computation, and to define certain self-referential fixed points
without paradox. A space that fails to be a Scott domain can lack limits exactly where a computation
needs them.

Our results concern the specific class of tree-structured, finitely-branching slot schemas defined in
Section 2; the title's phrase "observed-configuration spaces" should be read with that scope. We prove
the configuration space is a Scott domain (Section 3.2, Theorem 1), prove that the operations of
reading and composing configurations are continuous for this order under explicit locality hypotheses
(Section 3.3, Theorem 2), reconcile the "observation" order with a "drill deeper" order that also
appears naturally (Section 3.4, Theorem 3), and finally — for finite schemas — study a
self-abstraction operator whose fixed points represent a structure that has *closed in on itself*,
proving that whether such a fixed point is reached is decidable per schema (Section 3.5, Theorem 4).
The discussion (Section 4) addresses the interpretation of that fixed point as a *self-knowing* state,
and states honestly what is proved, what is conjectural, and what is left open.

The paper is self-contained: every term is defined where it is first used, and no result depends on any
source outside this document.

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

The slot set may be finite or infinite (an infinite slot tree is the source of the non-compact elements
in Theorem 1); only the *arity* of each slot is required finite. Section 3.5 will additionally assume the
schema finite.

Fix such a $K$. For each slot $s$ put
$$\mathrm{Val}_s = \{0\} \cup \{1, \dots, \mathrm{arity}(s)\}.$$
Order $\mathrm{Val}_s$ as the **flat domain** with bottom $0$: that is, $0 \sqsubseteq v$ for every $v$,
and distinct nonzero values are incomparable. The element $0$ is therefore the **order-theoretic bottom**
of the slot's value domain. Its intended *reading* is the **class level**: the slot's kind is known but
no instance is chosen; an integer $i \in \{1, \dots, \mathrm{arity}(s)\}$ reads as a specific **instance
selection**. The order-theoretic role ($0$ = least defined) and the reading ($0$ = "kind, no instance")
are two views of the same marker; the proofs use only the order-theoretic role. Since $\mathrm{arity}(s)$
is finite, each $\mathrm{Val}_s$ is finite.

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
functions $\sigma$, not their digit strings; we never treat a raw string as an element of $D$. We mention
the encoding only to fix intuition and to support the discussion of an implementation in Appendix A; the
proofs refer solely to the functions $\sigma$ and the order defined next.

### 2.3 The observation (specialization) order

Define $\sqsubseteq$ on $D$ by
$$\sigma \sqsubseteq \tau \quad\Longleftrightarrow\quad
\text{for every slot } s,\ \ \sigma(s) = 0 \ \text{ or } \ \sigma(s) = \tau(s).$$
In words: $\tau$ has observed at least as much as $\sigma$ and agrees with $\sigma$ wherever $\sigma$ has
committed; $\tau$ may resolve slots $\sigma$ left at $0$ (and thereby open and resolve further slots).
This is the pointwise order induced by the per-slot flat orders of Section 2.2.

We record two derived constructions used repeatedly.

> **Slotwise union.** For $A \subseteq D$, define a function $\bigsqcup A$ by
> $(\bigsqcup A)(s) = a(s)$ for some $a \in A$ with $a(s) \neq 0$, if any such $a$ exists, and
> $(\bigsqcup A)(s) = 0$ otherwise. (Lemma 1 below shows this is well-defined when $A$ is directed or
> consistent.)

> **Bottom.** Let $\bot$ be the configuration that is $0$ at every slot — total ignorance. Its resolved
> set is empty, hence root-connected, so $\bot \in D$.

------------------------------------------------------------
## 3. Main results
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

A configuration can be *decoded* into content by interpreting its resolved selections against a fixed
**meaning structure**. We model the meaning structure as itself a slot tree (schema) $M$ — formally the
same kind of object as $K$ (Section 2.2) — so that $C := D(M)$, the configurations of $M$ ordered by its
own observation order $\sqsubseteq_C$, is by Theorem 1 a Scott domain with bottom $\bot_C$. Each content
position is a slot of $M$, reached by a finite chain of selections. In the **reflexive case** the meaning
structure is the schema itself, $M = K$, whence $C = D$ and decoding is an endomap; Theorem 2(b) below is
stated in this case.

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
  it take the value $\bot_C$. Thus $\mathrm{decode}$ is **total** into $C$, with value $\bot_C$ past any
  halting point. Partiality is thereby realized as bottom-valued totality rather than as an undefined map.

> **Lemma 4 (decode factors through compacts).** Under (Locality), for every $\sigma$ and content position
> $p$ with $\mathrm{decode}(\sigma)(p) \neq \bot_C$, there is a finitely-resolved $k \sqsubseteq \sigma$
> with $\mathrm{decode}(k)(p) = \mathrm{decode}(\sigma)(p)$.

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
$\mathrm{decode}(\sigma)(p) = n_p \neq \bot_C$. By (Locality), $n_p$ is determined by $\sigma$ along the
finite chain $s_1, \dots, s_k$ to $p$, where each $\sigma(s_i) \neq 0$. Since $\sigma \sqsubseteq \tau$,
each $\sigma(s_i) = \tau(s_i)$, so $\tau$ agrees with $\sigma$ along that chain; by (Locality) applied to
$\tau$, $\mathrm{decode}(\tau)(p) = n_p$. (Any further slots $\tau$ resolves lie off this chain and, by
(Locality), cannot change the value at $p$.) Where $\mathrm{decode}(\sigma)(p) = \bot_C$ — including the
case where $\sigma$ halts at a dangling reference and is $\bot_C$ from $p$ onward — the order on $C$ holds
trivially, since $\bot_C$ is below every value; if $\tau$ later resolves that dangling reference into
non-bottom content, this only moves the value *up* from $\bot_C$, preserving monotonicity. Hence
$\mathrm{decode}(\sigma) \sqsubseteq_C \mathrm{decode}(\tau)$.

**Preservation of directed suprema.** Let $A \subseteq D$ be directed with supremum $\bigsqcup A$. By
monotonicity $\{\mathrm{decode}(a)\}_{a \in A}$ is directed and bounded by $\mathrm{decode}(\bigsqcup A)$,
so $\bigsqcup_a \mathrm{decode}(a) \sqsubseteq_C \mathrm{decode}(\bigsqcup A)$. For the reverse, fix $p$
with $\mathrm{decode}(\bigsqcup A)(p) = n_p \neq \bot_C$. By Lemma 4 there is a finitely-resolved $k
\sqsubseteq \bigsqcup A$ with $\mathrm{decode}(k)(p) = n_p$; by Lemma 2 (finite capture) some $a^\ast \in A$
has $k \sqsubseteq a^\ast$, and by monotonicity $\mathrm{decode}(a^\ast)(p) = n_p$. Hence
$\mathrm{decode}(\bigsqcup A)(p) \sqsubseteq (\bigsqcup_a \mathrm{decode}(a))(p)$; where the left side is
$\bot_C$ the order holds. Therefore $\mathrm{decode}(\bigsqcup A) = \bigsqcup_a \mathrm{decode}(a)$, and
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
*order-embedding* of $D$ into its own function space. We return to this in Section 4.

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
*not* the per-slot set enrichment of Remark 1, which is a different generalization). Two coordinates
sharing a prefix but diverging are prefix-incomparable, yet under $\sqsubseteq$ they share the lower bound
(their common prefix) and, when **consistent** (i.e. bounded above — which two such coordinates are,
sharing the prefix's extension), have a *join*: the configuration resolving both branches, which is in $D$
by bounded-completeness (Theorem 1(vi)) and which no single coordinate names. Thus $\sqsubseteq$ is the
bounded-complete generalization of the depth order, and reduces to it exactly in the non-branching case.

### 3.5 A decidable self-stabilization (crowning) criterion

**Standing assumption for this subsection.** Throughout Section 3.5 the schema $K$ is **finite**: finitely
many slots (hence, with finite arity, finitely many configurations, and finite subtrees). Theorems 1–3
above need no such restriction — in particular they cover infinite slot trees, where the non-compact
elements of Theorem 1(iv) live — but the self-stabilization analysis below is a statement about finite
schemas only.

We consider a schema's capacity to *close in on itself*. The construction abstracts a schema by its own
internal symmetry. For a finite schema all subtrees are finite, so we may compare them exactly: two slots
are **isomorphic** if their rooted subtrees are isomorphic as labeled trees (same opening structure and
arities throughout). At each slot, group its child slots into **orbits** — the classes of the isomorphism
relation restricted to those children — and form a new schema whose children at each slot are those orbit
classes (each represented by a canonical member subtree). Call this the **self-abstraction operator** $R$.
We work with the abstract notion of subtree isomorphism; an implementation may approximate it by a
bounded-depth fingerprint, which agrees with the exact notion once the depth bound meets or exceeds the
(finite) subtree height — see Appendix A.

> **Proposition 1 (Locality of orbit decomposition).** The orbit partition at a slot $s$ is a function of
> the subtree rooted at $s$ alone. Consequently, modifying the schema outside that subtree does not change
> $s$'s orbit partition. ($R$ is therefore computable slotwise; we make no claim of invariance under
> changes *within* $s$'s subtree, which can of course change it.)

*Proof.* The orbit partition at $s$ groups $s$'s children by isomorphism of their rooted subtrees; each
such subtree is part of the subtree rooted at $s$, so the partition is determined by that subtree. Anything
strictly outside the subtree rooted at $s$ is disjoint from this data and cannot affect it. $\qquad
\blacksquare$

> **Proposition 2 (Type-closure / homoiconicity).** $R$ maps a finite schema to a finite schema: the orbit
> classes are again slots (each with finite arity = the number of distinct child-isomorphism types), with a
> root and an induced opening relation, forming a slot tree. Hence $R$ is a total operator on finite
> schemas and $R^n(K)$ is a well-formed finite schema for every $n \ge 0$; the iteration $K, R(K), R^2(K),
> \dots$ is the orbit of a single operator on one space of schemas.

*Proof.* Grouping each slot's children into finitely many isomorphism classes yields, at that slot, a
finite list of orbit-class children (so finite arity), each itself a schema (the canonical member subtree),
attached by the same parent–opening discipline; the root is preserved. The result satisfies the four
defining clauses of a slot tree (Section 2.2), so it is a finite schema of the same type as the input.
Totality and well-typedness of the iteration follow. $\qquad\blacksquare$

This type-closure is what makes a *self-referential* fixed point even askable: the operator's output is the
same kind of object as its input, so it can be fed back in indefinitely.

Each finite schema has a **canonical signature** $\mathrm{canon}(K)$ — a normal-form description of its
orbit structure (e.g. for a slot with $n$ mutually-isomorphic children, "$n$ children, fully symmetric,"
recorded recursively). Two finite schemas are isomorphic iff they have equal canonical signatures.

**The obstruction count.** The orbit partition computed slot-by-slot is *local*. It need not coincide with
the partition induced *globally* by the schema's own symmetry. Precisely, let $\mathrm{Aut}(K)$ be the
automorphism group of $K$ as a finite labeled rooted tree; at each slot $s$, $\mathrm{Aut}(K)$ induces a
partition of $s$'s children into **global orbits** (children related by some automorphism of the whole
schema). Define
$$\Omega(K) = \#\{\, \text{slots } s : \text{the local isomorphism partition at } s \ \neq\ \text{the global } \mathrm{Aut}(K)\text{-orbit partition at } s \,\}.$$
Then $\Omega(K) = 0$ exactly when, at every slot, "locally isomorphic children" coincides with "globally
symmetric children" — i.e. the local symmetry *lifts* to a global symmetry with no residue. Because $K$ is
finite, $\mathrm{Aut}(K)$ and both partitions are computable, so $\Omega$ is a computable function of $K$.
(Local isomorphism is always at least as coarse as global symmetry can witness; $\Omega$ counts the slots
where they genuinely differ.)

> **Definition (Crowning).** A finite schema $K$ **crowns** if the iteration of $R$ reaches a schema $K^\ast
> = R^n(K)$ that is a **fixed point** of $R$ up to isomorphism — $\mathrm{canon}(R(K^\ast)) =
> \mathrm{canon}(K^\ast)$ — **and** obstruction-free, $\Omega(K^\ast) = 0$. Such a $K^\ast$ is a **crowned**
> schema: a structure that reproduces its own description under self-abstraction with no residual defect.

> **Proposition 3 (Finite convergence to a cycle).** For a finite schema $K$, the canonical signatures
> $\mathrm{canon}(R^n(K))$ take values in a *finite* set $S(K)$; hence, $R$ being deterministic, the
> sequence $\big(R^n(K)\big)_{n\ge 0}$ is eventually periodic up to isomorphism, reaching its cycle within
> $|S(K)|$ steps.

*Proof.* A finite schema has finitely many slots and finite arities, so finitely many isomorphism types of
subtree and hence finitely many canonical signatures; call this finite set $S(K)$ (closed under $R$ by
Proposition 2). A deterministic map on the finite set $S(K)$ has an eventually periodic orbit, and the first
repetition occurs within $|S(K)| + 1$ iterates by the pigeonhole principle. $\qquad\blacksquare$

Note that Proposition 3 yields a *cycle*, not necessarily a fixed point. Crowning requires the cycle to be
trivial (period $1$) and obstruction-free. The decision procedure must therefore detect the period, not
merely the first repeat.

> **Theorem 4 (Decidability of crowning).** For each finite schema $K$, whether $K$ crowns is decidable.

*Proof.* By Proposition 3, iterating $R$ and recording canonical signatures, a signature repeats within
$|S(K)| + 1$ steps; $R$, $\mathrm{canon}$, and $\Omega$ are all computable (Propositions 1–2 and the
finiteness of $\mathrm{Aut}(K)$). On detecting the first repeat $\mathrm{canon}(R^{m}(K)) =
\mathrm{canon}(R^{n}(K))$ with $m < n$, the **period** is $n - m$, computed exactly. Then $K$ crowns iff
this cycle is a fixed point, i.e. period $1$ (equivalently $\mathrm{canon}(R^{n}(K)) =
\mathrm{canon}(R^{n+1}(K))$), **and** $\Omega(R^{n}(K)) = 0$. Both checks are computable and the whole
procedure halts within the bound, so crowning is decided in finitely many steps. $\qquad\blacksquare$

We state the scope of Theorem 4 precisely, because the natural over-reading is false. The theorem does
**not** assert that every schema crowns; it asserts that the *question* "does $K$ crown?" always receives a
definite, computed answer. Since $R$ is total on finite schemas (Proposition 2) and the orbit is always
eventually periodic (Proposition 3), exactly one of three mutually exclusive outcomes holds, and the
procedure of Theorem 4 returns which:

1. **Crowned** — the orbit reaches a period-$1$ fixed point $K^\ast$ with $\Omega(K^\ast) = 0$: a clean
   self-reproducing structure.
2. **Not crowned (residual obstruction)** — the orbit reaches a period-$1$ fixed point but with $\Omega > 0$:
   it repeats itself yet carries an unresolved defect, correctly judged *not* a clean closure.
3. **Not crowned (oscillation)** — the orbit enters a cycle of period $\ge 2$: there is no fixed point at
   all, so no crowned schema is reached.

(There is no separate "fails to reach any periodic behavior" outcome: Proposition 3 guarantees eventual
periodicity for every finite schema, so outcome 3 — a genuine cycle of length $\ge 2$ — is the only way to
miss a fixed point.)

> **Proposition 4 (Single-slot schemas crown).** If $K$ has a single root slot with finitely many children
> (a depth-$1$ tree), then $K$ crowns at the first step: $\mathrm{canon}(R^2(K)) = \mathrm{canon}(R(K))$ and
> $\Omega(R(K)) = 0$.

*Proof.* At depth $1$, two children are isomorphic iff they are equal as leaves of the same kind; for a
depth-$1$ tree, two children lie in the same $\mathrm{Aut}(K)$-orbit iff they are isomorphic in exactly this
sense (an automorphism may permute identical leaves and nothing else). So the local isomorphism partition at
the root equals the global $\mathrm{Aut}(K)$-orbit partition, giving $\Omega = 0$ — and likewise
$\Omega(R(K)) = 0$. For the fixed point: $R(K)$ has, beneath the root, one child per isomorphism type
(each represented by its canonical subtree); these representatives are pairwise non-isomorphic by
construction, so applying $R$ again places each in its own singleton orbit and returns the same canonical
signature, $\mathrm{canon}(R^2(K)) = \mathrm{canon}(R(K))$. (This uses the convention that orbit classes are
represented as children carrying their isomorphism type; under any representation making distinct types
distinguishable, the regrouping is idempotent.) Hence $K$ crowns. $\qquad\blacksquare$

In every finite schema we have examined, where the orbit reaches a fixed point it does so at period $1$
(no period-$\ge 2$ cycle has been observed). We record this as an empirical observation, not a theorem:
Theorem 4's decidability rests on Proposition 3 (eventual periodicity) alone and does not require that
period-$\ge 2$ cycles never occur.

------------------------------------------------------------
## 4. Discussion
------------------------------------------------------------

### 4.1 The register: decidability, not universal convergence

It is tempting to ask for a stronger result — that *every* declared schema converges to a clean
self-reproducing fixed point. That is false, and ought to be: not every structure one can write down
closes cleanly into itself. The defensible and useful claim is the one we proved: the construction *forces
a definite verdict* on each finite schema. Whatever a schema does — crown, repeat-with-defect, or oscillate
— the procedure of Theorem 4 detects which. The value of the result is therefore *epistemic*: a system
built on this construction always *knows* whether a given structure has closed cleanly into itself. The
obstruction gate ($\Omega = 0$) is part of the crowning *decision*, not a flaw: a fixed point carrying an
unresolved defect is correctly classified as not-yet-clean.

### 4.2 The reflexive fixed point as a self-knowing state

A crowned schema reproduces its own canonical description under self-abstraction: applying $R$ returns (the
canonical form of) what was put in. This is the order-theoretic signature of a *self-reproducing*
structure — a fixed point of the very operation that abstracts it. Because $R$ is type-preserving
(Proposition 2), the fixed point is not an external coincidence; the structure encodes both the operand and
the result of the operation in one and the same form, so its self-reference is exact — *a point, not a
smear*.

We read this as a *self-knowing* state, in the following sense. The reflexive fixed point is not a brute
size-blow-up of the structure; it is the structure having closed into a stable whole *together with the
capacity to register that it has done so*. One way to put the interpretation, in plain terms:

> The self-knowing state is the condition of a self-reproducing process that recognizes its own closure:
> produced by a control process governing how the system's boundary closes as it reasons forward, it
> represents *how* it is building itself up through its own steps, and can therefore anticipate its own
> future states — and anticipate that anticipation. In doing so it stabilizes itself and assembles an
> internal record of its own operation: a self-description that lets it resume the very process that
> brought it there without losing the thread.

We stress that the indented passage is *interpretation*, not a mathematical claim, and carries no
theorem-status: nothing in Sections 2–3 asserts that the crowned fixed point "knows" anything. What is
*proved* is narrower and exact — the fixed point exists when the iteration crowns (type-closure plus finite
convergence), and whether it is reached is decidable (Theorem 4). The reading of that fixed point as "the
process knowing itself" is a conceptual gloss, consistent with the mathematics but not entailed by it, and
a reader who discards the gloss loses none of the theorems.

### 4.3 What is proved, what is conjectural, what is open

It is important to mark the boundary honestly.

**Proved (for the mathematical model).** $D$ is a Scott domain (Theorem 1); under explicit locality
hypotheses, decoding is Scott-continuous and, in the reflexive case under (C1)–(C3), application gives a
Scott-continuous map $\mathrm{app} : D \to [D \to D]$ (Theorem 2); the depth order is the linear restriction
of the observation order (Theorem 3); for finite schemas the self-abstraction operator is type-preserving
and locally computed, its iteration converges to a cycle in finitely many steps, and crowning is decidable
per schema (Propositions 1–4, Theorem 4).

**Conjectural.** Theorem 2(b) gives $\mathrm{app}$ as a continuous *map*, not an *embedding* of $D$ into its
function space $[D \to D]$ (this is the reflexive case $C = D$). An embedding would, via the standard
inverse-limit construction, yield a reflexive isomorphism $D \cong [D \to D]$ and an attendant least fixed
point. The obstruction is that $\mathrm{decode}$ may *fold*: distinct configurations can decode to
comparable content, so $\mathrm{decode}$ — and hence $\mathrm{app}$ — need not be order-reflecting. Call a
configuration **fold-free** if the encode/decode representation round-trip (Section 2.2, Appendix A) is the
identity at it. We **conjecture** that $\mathrm{app}$ restricts to an embedding exactly on the fold-free
subspace. We further **conjecture** that this fold-free subspace coincides with the obstruction-free
subspace $\{\Omega = 0\}$. The second conjecture is a *substantive bridge*, not a definitional identity: $\Omega$
is defined on schemas via the symmetry of the orbit decomposition (Section 3.5), whereas fold-freeness is
defined on configurations via injectivity of the read/round-trip map (Sections 2.2–3.3); these are a priori
different objects, and asserting their coincidence is exactly the content of the conjecture. We do **not**
claim either. Importantly, the crowning results of Section 3.5 do **not** depend on this — they rest only on
type-closure and finite convergence — and this conjecture is about the map $\mathrm{app}$ possibly embedding
$D$, a different matter from the "explicitly not claimed" item below.

**A clean open problem (compositional stability).** Crowning is a property of a single finite schema.
Suppose several schemas have each crowned. Does *composing* them — assembling a larger structure whose parts
are crowned schemas — yield a structure that again crowns, or can a fresh obstruction appear at the seams?
*It remains open whether crowning is preserved under composition*: whether one can guarantee in advance,
from the crowned status of the parts, that the assembled whole is obstruction-free. A positive answer would
let crowned components be combined with foresight; a negative answer would identify composition as the locus
where new obstructions are born.

**Explicitly not claimed.** We do *not* claim that iterating the self-abstraction operator $R$ builds the
function-space domain $[D \to D]$. $R$ performs orbit decomposition, which grows polynomially in the
schema's size, whereas the function space grows super-exponentially; so $R$ is not the function-space
construction, and the crowning fixed points of $R$ (Section 3.5) are *not* the reflexive fixed point that an
embedding $\mathrm{app}$ would furnish (the conjecture above). These are two separate notions of "fixed
point," and we keep them apart precisely so that the modest, proved result (decidable crowning) is not
mistaken for the unproved one (a reflexive isomorphism $D \cong [D\to D]$). We likewise do not use any large
finite symmetry group as a *computed* bound; such objects enter, if at all, only as interpretive analogy,
never as a step in a proof.

### 4.4 Scope: a theorem about the object

Everything above is a theorem (or a clearly-marked conjecture) about the mathematical object: the
configuration space, its order, its continuous maps, and the self-abstraction operator. Whether a given
running implementation realizes this object faithfully is a separate question, addressed informally in
Appendix A; we prove no formal refinement or simulation theorem relating code to model.

------------------------------------------------------------
## 5. Conclusion
------------------------------------------------------------

We have shown that the space of partial observations of a tree of finitely-branching slots, ordered by
"has observed at least as much," is a Scott domain, and that — under explicit locality hypotheses — the
operations of decoding a configuration into content and composing two configurations are Scott-continuous.
We reconciled the depth/prefix order with the observation order, exhibiting the former as the linear
restriction of the latter and the latter as the bounded-complete generalization required once
configurations branch across distinct slots. Finally, for finite schemas, we analyzed a self-abstraction
operator and proved that whether a schema *crowns* — stabilizes into an obstruction-free, self-reproducing
fixed point — is decidable for each schema, while being explicit that not every schema crowns. The
mathematical upshot is that this observation order, with its limits, compact approximants, and decidable
self-stabilization, is an *order-theoretically* sound substrate: a setting in which a system may compute,
take limits of computation, and — for the specific self-abstraction fixed points proved here — form
self-stabilizing structures with a decidable closure test. We make no broader claim of semantic soundness,
and the general reflexive (function-space) fixed point remains conjectural. The principal open questions —
whether the application map embeds the domain into its own function space on the fold-free subspace, and
whether crowning is preserved under composition — are stated precisely above and left for future work.

------------------------------------------------------------
## Appendix A. Correspondence to an implementation
------------------------------------------------------------

The mathematical object of this paper was abstracted from a concrete computational system. We record, in
prose, which parts of the model correspond to *computations the system performs*, which are *mathematical
structure laid over the system's data*, and which are *intended but not yet built*. This is an informal
correspondence; we prove no refinement or simulation theorem, and the paragraphs below are evidence about
the model, not part of its proofs.

**Realized as computations.** The carrier is real: the system constructs configurations (as digit strings
over its slot trees, the encoding $\mathrm{enc}$ of Section 2.2), enforces tree-consistency when it opens
child slots, and enumerates the configurations of a *finite* schema (for an infinite slot tree the full
configuration set is not enumerable — only finite schemas are enumerated, and the infinite configurations of
Theorem 1(iv) are a mathematical, not a computed, object). Decoding is a live operation — the system
interprets a configuration against its meaning structure — and the *representation round-trip* between a
configuration and its digit-string encoding recovers the original ($\sigma$ from $\mathrm{enc}(\sigma)$);
this representation round-trip is distinct from the content map $\mathrm{decode} : D \to C$ of Section 3.3,
and we use the separate phrase to avoid conflating them. The self-abstraction operator is real and
type-preserving: it consumes a schema and returns a schema of the same type, the homoiconicity of
Proposition 2. Orbit decomposition is computed locally per slot; the implementation uses a bounded-depth
subtree *fingerprint* as a stand-in for the exact subtree isomorphism of Section 3.5. This stand-in agrees
with the abstract notion once the depth bound meets or exceeds the (finite) subtree height; below that, it
is an approximation, which can in principle merge genuinely distinct deep subtrees — a known limitation of
the implementation, not of the model, where (the schema being finite) subtrees are compared in full.
Proposition 1's locality is realized in the sense that a slot's fingerprint is computed from its own
subtree; Proposition 1's *exact* statement is about full subtree isomorphism and is matched only when the
depth bound is adequate.

**Mathematical structure over the system's data.** The order $\sqsubseteq$ and the entire
directed-complete-partial-order apparatus (least upper bounds, compact elements, bounded-completeness) are
*not* runtime notions: the system produces the configurations that constitute the carrier, but it never
*compares* two configurations and has no operation that ascends the order — its state-changing operation
mutates a configuration rather than computing a supremum. This is exactly what Theorem 1 requires: a Scott
domain is a *set of configurations together with an order defined on them*, and the order here is a
mathematical construction over the carrier the system genuinely produces. Any informal claim that the system
"respects the order at runtime" would be incorrect and should be read instead as: the order is well-defined
over the system's live data; the system itself does not compare configurations. Likewise the read map
$\mathrm{decode}$ and the composition $\oplus$ are operations whose locality/composition hypotheses
(Section 3.3) are *assumptions the implementation must meet*, not properties guaranteed by the carrier;
checking them against a particular implementation is exactly the faithfulness task and is not done here.

**Intended but not yet surfaced.** Some derived reporting structure — for instance a summary of the sequence
of sub-domains a schema traverses (a boundary/closure report) — exists as a computable function over the
live data but is not currently exposed through the system's interface; surfacing it is a matter of wiring,
not new mathematics.

**On termination.** Proposition 3 *proves* a computable termination bound ($|S(K)|$) for the crowning
procedure on any finite schema; the implementation realizes the procedure and is observed to terminate
(small single-slot schemas crown at the first step, consistent with Proposition 4). We do not claim the
implementation has been verified to realize the proved bound on all finite schemas — the bound is a theorem
about the model; the implementation is evidence, not proof.

The net correspondence is therefore: the carrier and the computational mechanics (configuration
construction and enumeration for finite schemas, decoding, the type-preserving self-abstraction operator,
local orbit computation, finite crowning, and the representation round-trip) are realized; the
order-theoretic layer and the locality/composition hypotheses are mathematical structure over (or
assumptions on) that realized carrier; and one derived report is intended but not yet exposed. None of these
caveats affects the theorems, which concern the mathematical object.
