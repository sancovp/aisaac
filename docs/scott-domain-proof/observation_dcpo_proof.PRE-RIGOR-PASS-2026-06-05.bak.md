# Observed-Configuration Spaces are Scott Domains, with a Decidable Self-Stabilization Criterion

## Abstract

We study the space of *partial observations* of a tree-structured collection of choices. Each
position (a *slot*) in the tree is either left at a *class level* — its kind is fixed but no
particular instance is chosen — or *specialized* to one of finitely many instances; specializing a
slot may open further slots beneath it. Ordering these configurations by "has observed at least as
much," we prove that the resulting space is a **Scott domain**: a bounded-complete algebraic
directed-complete partial order with a least element. We then prove that the natural map that
*decodes* a configuration into content, and the natural map that *composes* two configurations, are
**Scott-continuous**, so that limits of increasing observations are respected. We show that a
"depth/prefix" order, under which one observation extends another by drilling deeper along a single
path, is exactly the restriction of the observation order to linear (non-branching) configurations.
Finally we analyze a *self-abstraction* operator that replaces a configuration schema by its own
internal symmetry decomposition, and prove that whether iterating this operator *stabilizes* a schema
into a self-reproducing fixed point — which we call **crowning** — is **decidable for each schema**.
We are careful to claim only decidability of crowning, not that every schema crowns, and we separate
what is proved from what remains conjectural, including whether composing several stabilized
structures preserves stability.

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
approximated by its finite (fully written-down) parts, and consistent observations can always be merged
into a least common refinement. Concretely, this is what makes it sound — *in principle* — for a system
to compute over such a space, to take limits of unbounded computation, and to define self-referential
fixed points without paradox. A space that fails to be a Scott domain can lack limits exactly where a
computation needs them.

We prove the configuration space is a Scott domain (Section 3, Theorem 1), prove that the operations of
reading and composing configurations are continuous for this order (Theorem 2), reconcile the
"observation" order with a "drill deeper" order that also appears naturally (Theorem 3), and finally
study a self-abstraction operator whose fixed points represent a structure that has *closed in on
itself* — and prove that whether such a fixed point is reached is decidable per schema (Theorem 4). The
discussion (Section 4) addresses the interpretation of that fixed point as a *self-knowing* state, and
states honestly what is proved, what is conjectural, and what is left open.

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
A **least upper bound** (or **supremum**, written $\bigsqcup A$) is an upper bound below every upper bound.
Suprema are unique when they exist.

A subset $A \subseteq P$ is **directed** if it is nonempty and every two elements $a, b \in A$ have an
upper bound $c \in A$ (so $a \sqsubseteq c$ and $b \sqsubseteq c$). Intuitively, a directed set is a
collection of mutually compatible, ever-more-informative observations.

$P$ is a **directed-complete partial order** (**dcpo**) if every directed subset has a supremum in $P$.
$P$ is **pointed** if it has a least element $\bot$ (a *bottom*), satisfying $\bot \sqsubseteq x$ for all
$x$.

An element $k \in P$ is **finite** (the standard term is **compact**) if, whenever $k$ is below the
supremum of a directed set, it is already below a member of that set:
$$k \sqsubseteq \textstyle\bigsqcup A \ \Longrightarrow\ \exists\, a \in A,\ k \sqsubseteq a .$$
Finite elements are those that can be "fully written down" — they cannot be reached only as a genuine
limit. We write $K(P)$ for the set of finite elements.

$P$ is **algebraic** if every element is the directed supremum of the finite elements below it:
$x = \bigsqcup\{ k \in K(P) : k \sqsubseteq x \}$ for all $x$, with the set on the right directed.

$P$ is **bounded-complete** if every subset that *has* an upper bound has a *least* upper bound.
(Equivalently, every pair with a common upper bound has a supremum.)

A **Scott domain** is a bounded-complete algebraic dcpo with a least element.

A map $f : P \to Q$ between dcpos is **monotone** if $x \sqsubseteq y$ implies $f(x) \sqsubseteq f(y)$,
and **Scott-continuous** if it is monotone and preserves directed suprema: for every directed
$A \subseteq P$, $f(\bigsqcup A) = \bigsqcup_{a \in A} f(a)$. Scott-continuity is the order-theoretic
form of "computable up to taking limits": the output of a limit is the limit of the outputs.

### 2.2 The carrier: configurations over a slot tree

A **slot tree** (or **schema**) $K$ consists of:

1. a distinguished **root**;
2. a set $\mathrm{Slots}(K)$ of **slots** (positions that may be filled);
3. a **parent–opening relation** specifying, for each slot, which selection at its parent *opens* it
   (so a slot becomes available only once its parent has been specialized accordingly);
4. for each slot $s$ a finite **arity** $\mathrm{arity}(s) \in \mathbb{N}$, the number of alternative
   instances available at $s$.

Fix such a $K$. For each slot $s$ put
$$\mathrm{Val}_s = \{0\} \cup \{1, \dots, \mathrm{arity}(s)\},$$
where the marker $0$ denotes the **class level** (the slot's kind is known but no instance is chosen),
and an integer $i \in \{1, \dots, \mathrm{arity}(s)\}$ denotes a specific **instance selection**. Since
$\mathrm{arity}(s)$ is finite, each $\mathrm{Val}_s$ is finite.

A **configuration** is a *total* function
$$\sigma : \mathrm{Slots}(K) \to \mathrm{Val},\qquad \sigma(s) \in \mathrm{Val}_s,$$
subject to **tree-consistency**: if $\sigma(s) \neq 0$ (the slot is specialized) then every ancestor
slot that must be opened to reach $s$ is also specialized in $\sigma$, carrying the selection that opens
$s$. Equivalently, the set
$$\mathrm{res}(\sigma) = \{\, s : \sigma(s) \neq 0 \,\}$$
of **resolved** slots is *root-connected* (a subtree containing the root). Partiality is encoded by the
value $0$, never by a missing argument: a slot whose ancestors are still unobserved simply sits at $0$.

Let $D = D(K)$ be the set of all configurations of $K$.

A remark on representation. Each configuration can be encoded as a finite string of digits recording the
selections along its resolved subtree; the marker $0$ and the instance digits are the only values that
carry order-theoretic content, while additional reserved digit-patterns serve purely as structural
punctuation (marking where a slot is drilled into, where a sub-tree closes, and so on). These structural
markers *build* the tree and the values; they are not themselves elements of $D$ nor points of its order.
We mention this only to fix intuition; the proofs below refer solely to the functions $\sigma$ and the
order defined next.

### 2.3 The observation (specialization) order

Define $\sqsubseteq$ on $D$ by
$$\sigma \sqsubseteq \tau \quad\Longleftrightarrow\quad
\text{for every slot } s,\ \ \sigma(s) = 0 \ \text{ or } \ \sigma(s) = \tau(s).$$
In words: $\tau$ has observed at least as much as $\sigma$ and agrees with $\sigma$ wherever $\sigma$ has
committed; $\tau$ may resolve slots $\sigma$ left at $0$ (and thereby open and resolve further slots).
The marker $0$ is the "less defined" direction; an instance selection is "more defined." This is the
pointwise order induced by the per-slot **flat** order in which $0$ lies strictly below each instance and
distinct instances are incomparable.

We record two derived constructions used repeatedly.

> **Slotwise union.** For $A \subseteq D$, define a function $\bigsqcup A$ by
> $(\bigsqcup A)(s) = a(s)$ for some $a \in A$ with $a(s) \neq 0$, if any such $a$ exists, and
> $(\bigsqcup A)(s) = 0$ otherwise. (Lemma 1 below shows this is well-defined when $A$ is directed or
> bounded.)

> **Bottom.** Let $\bot$ be the configuration that is $0$ at every slot — total ignorance. It is
> tree-consistent (its resolved set is empty, hence trivially root-connected).

------------------------------------------------------------
## 3. Main results
------------------------------------------------------------

### 3.1 Supporting lemmas

> **Lemma 1 (Well-defined slotwise union).** Let $A \subseteq D$ be directed, or bounded above. Then for
> every slot $s$, all members of $A$ that resolve $s$ assign it the same value; hence the slotwise union
> $\bigsqcup A$ is well-defined, and its resolved set is $\bigcup_{a \in A}\mathrm{res}(a)$.

*Proof.* Suppose $a(s) \neq 0$ and $b(s) \neq 0$ for $a, b \in A$. If $A$ is directed, take $c \in A$
with $a \sqsubseteq c$ and $b \sqsubseteq c$; then $a(s) = c(s)$ and $b(s) = c(s)$, so $a(s) = b(s)$. If
instead $A$ is bounded by $u$, then $a \sqsubseteq u$ and $b \sqsubseteq u$ give $a(s) = u(s) = b(s)$.
The assigned value is independent of the witness, so $\bigsqcup A$ is well-defined. Its resolved set is
the union of the members' resolved sets by construction. $\qquad\blacksquare$

> **Lemma 2 (Finite capture).** Let $k \in D$ resolve only finitely many slots, let $A \subseteq D$ be
> directed, and suppose $k \sqsubseteq \bigsqcup A$. Then there is $a \in A$ with $k \sqsubseteq a$.

*Proof.* The element $k$ resolves finitely many slots $s_1, \dots, s_m$ (those with $k(s_i) \neq 0$).
For each $i$, $k \sqsubseteq \bigsqcup A$ forces $(\bigsqcup A)(s_i) = k(s_i) \neq 0$, so by the
definition of the slotwise union some $a_i \in A$ has $a_i(s_i) = k(s_i)$. There are finitely many
$a_i$, and $A$ is directed, so there is a single $a \in A$ above all of them. Then $a(s_i) = k(s_i)$ for
every $i$, while $k$ is $0$ elsewhere, so $k \sqsubseteq a$. $\qquad\blacksquare$

> **Lemma 3 (Reconstruction).** For every $x \in D$, $\ x = \bigsqcup\{\, k \in D : k \sqsubseteq x,\
> k \text{ finite} \,\}$.

*Proof.* Every resolved slot of $x$ belongs to some finite configuration $k \sqsubseteq x$ (take $k$ to
resolve just the chain from the root to that slot, with $x$'s values). The slotwise union of all such
finite $k$ resolves exactly the slots $x$ resolves, to $x$'s values; hence it equals $x$. The family is
directed: the union of the resolved sets of two finite approximants, filled with $x$'s values, is again
a finite approximant above both. $\qquad\blacksquare$

### 3.2 The configuration space is a Scott domain

> **Theorem 1.** $(D, \sqsubseteq)$ is a Scott domain: a bounded-complete algebraic dcpo with least
> element.

*Proof.* We verify the five constituent properties.

**(i) Partial order.** *Reflexivity:* at each slot $s$, either $x(s) = 0$ or $x(s) = x(s)$, so
$x \sqsubseteq x$. *Antisymmetry:* assume $x \sqsubseteq y$ and $y \sqsubseteq x$. Fix $s$. If
$x(s) \neq 0$, then $x \sqsubseteq y$ gives $x(s) = y(s)$. If $x(s) = 0$, then $y \sqsubseteq x$ gives
$y(s) = 0$ or $y(s) = x(s) = 0$, so $y(s) = 0 = x(s)$. Thus $x(s) = y(s)$ at every slot, i.e. $x = y$.
*Transitivity:* assume $x \sqsubseteq y$ and $y \sqsubseteq z$, and fix $s$. If $x(s) = 0$ the first
disjunct of $x \sqsubseteq z$ holds. If $x(s) \neq 0$, then $x(s) = y(s) \neq 0$ and $y(s) = z(s)$, so
$x(s) = z(s)$. Hence $x \sqsubseteq z$.

**(ii) Least element.** For any $x$ and any slot $s$, $\bot(s) = 0$, so the first disjunct of
$\bot \sqsubseteq x$ holds; thus $\bot \sqsubseteq x$.

**(iii) Directed-completeness.** Let $A$ be directed and form $\bigsqcup A$ (well-defined by Lemma 1).
Its resolved set $\bigcup_{a \in A}\mathrm{res}(a)$ is root-connected: each $\mathrm{res}(a)$ is, all
share the root, and any two are consistent (directedness), so their union is a root-connected subtree;
hence $\bigsqcup A \in D$. For each $a \in A$ and slot $s$ with $a(s) \neq 0$ we have
$(\bigsqcup A)(s) = a(s)$, and where $a(s) = 0$ the disjunct holds, so $a \sqsubseteq \bigsqcup A$: it is
an upper bound. If $u$ is any upper bound of $A$, then for each $s$ with $(\bigsqcup A)(s) \neq 0$ some
$a \in A$ has $a(s) = (\bigsqcup A)(s)$ and $a \sqsubseteq u$, so $u(s) = (\bigsqcup A)(s)$; elsewhere the
disjunct holds; hence $\bigsqcup A \sqsubseteq u$. So $\bigsqcup A$ is the least upper bound and $D$ is a
dcpo.

**(iv) Finite elements are exactly the finite configurations.** First, every configuration $k$
resolving only finitely many slots is finite in the order: this is precisely Lemma 2. Conversely,
suppose $x$ resolves infinitely many slots; let $A = \{\, k \sqsubseteq x : k \text{ resolves finitely
many slots} \,\}$. By the proof of Lemma 3, $A$ is directed and $\bigsqcup A = x$. But each $a \in A$ is
finite while $x$ is not, so $x$ resolves some slot $a$ leaves at $0$, whence $x \not\sqsubseteq a$. Thus
$x \sqsubseteq \bigsqcup A = x$ yet no member of $A$ is above $x$, so $x$ is not finite. Hence the finite
elements are exactly the finitely-resolved configurations.

**(v) Algebraicity.** Fix $x$ and let $K_x = \{\, k \sqsubseteq x : k \text{ finite} \,\}$. It is
nonempty ($\bot \in K_x$) and directed (the slotwise union of two members, filled with $x$'s values, is
finite, tree-consistent, $\sqsubseteq x$, and above both). By Lemma 3, $\bigsqcup K_x = x$, and the
least-upper-bound computation of (iii) shows this is the supremum. Hence
$x = \bigsqcup\{\, k \in K(D) : k \sqsubseteq x \,\}$ for every $x$.

**(vi) Bounded-completeness.** Let $S \subseteq D$ have an upper bound $u$. By Lemma 1 the members of
$S$ agree on jointly-resolved slots and $\bigsqcup S$ is well-defined; its resolved set
$\bigcup_{s \in S}\mathrm{res}(s)$ is root-connected and consistent because all members lie under $u$, so
$\bigsqcup S \in D$. As in (iii), $\bigsqcup S$ is an upper bound of $S$ and below every upper bound.
Hence every bounded subset has a least upper bound.

By (i)–(vi), $(D, \sqsubseteq)$ is a bounded-complete algebraic dcpo with least element — a Scott
domain. $\qquad\blacksquare$

> **Remark 1 (Sets of selections per slot).** The model above lets a slot carry the marker $0$ or one
> instance. A common enrichment lets a slot carry a *set* of instances simultaneously (a conjunction of
> selections). Replacing each per-slot flat factor by the lattice of *subsets* of $\{1, \dots,
> \mathrm{arity}(s)\}$ ordered by inclusion keeps $D$ a Scott domain, because each such lattice is
> *finite* (the arity is finite), hence trivially a bounded-complete algebraic dcpo. (If a slot's choice
> space were infinite, "finite subsets ordered by inclusion" would fail to be directed-complete; the
> correct fix would then be the ideal completion with finite subsets as the finite elements. We do not
> need this, since all arities are finite.)

### 3.3 Reading and composing configurations are continuous

A configuration can be *decoded* into content by interpreting its resolved selections against a fixed
**meaning structure** $M$ — a directed acyclic graph of content nodes, each reachable by a finite chain
of selections. Let $C$ be the observation domain built from $M$ by the same construction as $D$ (Section
2.2); $C$ is again a Scott domain, with its own bottom $\bot_C$ and order $\sqsubseteq_C$. In the
self-referential case where the meaning structure *is* the schema, $C = D$ and decoding is an endomap.

Define $\mathrm{decode} : D \to C$ by letting $\mathrm{decode}(\sigma)$ be the content obtained by
resolving $\sigma$ against $M$ slot by slot along $\sigma$'s resolved chains. We adopt one explicit
modeling convention for partial inputs: at any position $\sigma$ leaves unobserved, or at any structural
*dangling reference* (a punctuation marker whose target is undefined), resolution **halts**, and that
content position together with everything downstream of it is set to $\bot_C$. Thus $\mathrm{decode}$ is
*total* into $C$ (always defined, and equal to $\bot_C$ past a halting point). This realizes partiality
as bottom-valued totality rather than as an undefined map.

> **Lemma 4 (decode factors through finite elements).** Every content position with a value above
> $\bot_C$ is produced by interpreting a *finite* chain of selections; hence $\mathrm{decode}(\sigma)(p)$
> is determined by some finite $k \sqsubseteq \sigma$.

This is immediate from the definition: a content node is reached by a finite chain, and that chain is a
finite sub-configuration of $\sigma$.

> **Theorem 2 (Continuity of decode and apply).**
> (a) $\mathrm{decode} : D \to C$ is Scott-continuous.
> (b) The currying of configuration-composition is a Scott-continuous map
> $\mathrm{app} : D \to [D \to D]$, where $[D \to D]$ is the dcpo of Scott-continuous self-maps of $D$
> ordered pointwise.

*Proof.* **(a) Monotonicity.** Let $\sigma \sqsubseteq \tau$ and fix a content position $p$ with
$\mathrm{decode}(\sigma)(p) = n_p \neq \bot_C$. By Lemma 4 this is produced by a finite chain of slots
$s_1, \dots, s_k$ with $\sigma(s_i) \neq 0$. Since $\sigma \sqsubseteq \tau$, each such $\sigma(s_i)$
equals $\tau(s_i)$; as $M$ is fixed, $\tau$ follows the same chain and produces the same $n_p$, so
$\mathrm{decode}(\tau)(p) = n_p$. (Any new slots $\tau$ resolves open *new* subtrees and cannot alter a
node already fixed by the prefix $s_1 \dots s_k$, because the content at $p$ is a local function of the
resolved prefix down to $p$.) Where $\mathrm{decode}(\sigma)(p) = \bot_C$, the order on $C$ holds
trivially. If $\sigma$ halts at a dangling reference, $\mathrm{decode}(\sigma)$ is $\bot_C$ from that
point on, and $\tau \sqsupseteq \sigma$ reproduces the earlier content; either way
$\mathrm{decode}(\sigma) \sqsubseteq_C \mathrm{decode}(\tau)$.

**Preservation of directed suprema.** Let $A \subseteq D$ be directed with supremum $\bigsqcup A$. By
monotonicity $\{\mathrm{decode}(a)\}_{a \in A}$ is directed and bounded above by
$\mathrm{decode}(\bigsqcup A)$, so $\bigsqcup_a \mathrm{decode}(a) \sqsubseteq_C
\mathrm{decode}(\bigsqcup A)$. For the reverse, fix $p$ with $\mathrm{decode}(\bigsqcup A)(p) = n_p \neq
\bot_C$, produced by a finite chain $s_1, \dots, s_k$ with $(\bigsqcup A)(s_i) \neq 0$. By Lemma 2, a
single $a^\ast \in A$ resolves all $s_i$ to those values, so $\mathrm{decode}(a^\ast)(p) = n_p$. Hence
$\mathrm{decode}(\bigsqcup A)(p) \sqsubseteq (\bigsqcup_a \mathrm{decode}(a))(p)$; where the left side is
$\bot_C$ the order holds. Therefore $\mathrm{decode}(\bigsqcup A) = \bigsqcup_a \mathrm{decode}(a)$, and
$\mathrm{decode}$ is Scott-continuous.

**(b)** Configuration-composition $\varphi \oplus \psi$ concatenates $\varphi$ and $\psi$ (resolving any
references that $\varphi$ leaves for $\psi$ to supply), and $\mathrm{app}(\varphi) = (\psi \mapsto
\mathrm{decode}(\varphi \oplus \psi))$. For fixed $\varphi$, the map $\psi \mapsto \mathrm{decode}(\varphi
\oplus \psi)$ is Scott-continuous by the same argument as (a) applied in the second argument (each
resolved content position depends on a finite prefix of $\psi$; finite capture). Thus
$\mathrm{app}(\varphi) \in [D \to D]$. Finally $\mathrm{app}$ is itself Scott-continuous: for directed
$\Phi \subseteq D$ and any $\psi$,
$$\mathrm{app}\big(\textstyle\bigsqcup \Phi\big)(\psi)
= \mathrm{decode}\big((\textstyle\bigsqcup \Phi) \oplus \psi\big)
= \textstyle\bigsqcup_{\varphi} \mathrm{decode}(\varphi \oplus \psi)
= \big(\textstyle\bigsqcup_{\varphi} \mathrm{app}(\varphi)\big)(\psi),$$
using finite capture in the first argument. $\qquad\blacksquare$

We emphasize what Theorem 2(b) does *not* assert: $\mathrm{app}$ is a continuous *map*, not necessarily
an *order-embedding* of $D$ into its own function space. We return to this in Section 4.

### 3.4 The depth order is the linear restriction of the observation order

Two orders arise naturally and are sometimes treated as distinct "axes":

- a **depth (prefix) order**: one coordinate is below another when its digit-string is a prefix of the
  other's — i.e. the second drills *deeper* along the same path;
- the **observation order** $\sqsubseteq$ of Section 2.3: filling unobserved slots into selections.

They are not competing; the first is the linear special case of the second. A *coordinate* is a single
root-to-leaf chain of selections; it determines a configuration $\mathrm{config}(c) \in D$ resolving
exactly that chain and leaving every other slot at $0$ (tree-consistency is automatic, a chain being
root-connected).

> **Theorem 3.** The map $c \mapsto \mathrm{config}(c)$ is an order-embedding of the coordinates under
> the prefix order into $(D, \sqsubseteq)$: $\ c \preceq_{\mathrm{pre}} d \iff \mathrm{config}(c)
> \sqsubseteq \mathrm{config}(d)$. Its image is exactly the *linear* configurations (those whose resolved
> set is a single root-to-leaf chain). On a schema in which each selection opens exactly one further
> slot, every configuration is linear, so $\sqsubseteq$ and $\preceq_{\mathrm{pre}}$ coincide.

*Proof.* If $c$ is a prefix of $d$, then $\mathrm{config}(d)$ resolves every slot $\mathrm{config}(c)$
resolves with the same selection (since $d$ extends $c$), and $\mathrm{config}(c)$ is $0$ on the deeper
slots, so $\mathrm{config}(c) \sqsubseteq \mathrm{config}(d)$. Conversely, if $\mathrm{config}(c)
\sqsubseteq \mathrm{config}(d)$ with both linear, then $\mathrm{config}(c)$'s single chain agrees with
$\mathrm{config}(d)$ within its depth and, being one path, is an initial segment of $\mathrm{config}(d)$'s
chain — i.e. $c$ is a prefix of $d$. The image is the linear configurations by construction. On a
single-spectrum schema every configuration is one chain, so the orders agree. $\qquad\blacksquare$

The point of Theorem 3 is that $\sqsubseteq$ is the correct *general* order. As soon as a node has
several slots that may be resolved independently (or a slot may carry a set of selections, Remark 1),
configurations *branch*: two coordinates sharing a prefix but diverging are prefix-incomparable, yet
under $\sqsubseteq$ they share the lower bound (their common prefix) and, when consistent, have a
*join* — the configuration resolving both branches — which no single coordinate names. Bounded-
completeness (Theorem 1(vi)) is exactly what supplies those joins; the prefix order alone yields only a
tree, which is not bounded-complete across branches. Thus the observation order is the bounded-complete
generalization of the depth order, and reduces to it precisely in the non-branching case.

### 3.5 A decidable self-stabilization (crowning) criterion

We now consider a schema's capacity to *close in on itself*. Given a fully specialized schema, one can
abstract it by its own internal symmetry: group the sibling selections at each slot into **orbits** —
equivalence classes of selections that have identical subtree shape — and form a new schema whose
children are those orbit classes. Call this the **self-abstraction operator** $R$, mapping a schema to
the schema of its per-slot orbit decomposition.

Two structural facts drive the analysis.

> **Proposition 1 (Locality of orbit decomposition).** The orbit class of a slot is determined by a
> finite, local part of the schema — that slot's own subtree, compared up to a fixed bounded depth — and
> is stable under deeper resolution: resolving additional slots elsewhere never retroactively changes an
> already-computed slot's orbits.

*Proof sketch.* Orbits are computed by grouping a slot's children by a *subtree fingerprint* — a
recursive normal form of the child's own subtree (its level, kind, and the sorted fingerprints of its
children, truncated at a fixed depth). This fingerprint depends only on the subtree rooted at the slot,
so adding or resolving slots outside that subtree leaves it unchanged. $\qquad\blacksquare$

> **Proposition 2 (Type-closure / homoiconicity).** $R$ returns a schema of the same type it consumes.
> Consequently $R^n(K)$ is a well-formed schema for every $n \ge 0$, and the iteration $K, R(K), R^2(K),
> \dots$ is a genuine orbit of a single operator on a single space of schemas.

This is the property that makes a *self-referential* fixed point even askable: the operator's output is
the same kind of object as its input, so it can be fed back in indefinitely.

Each schema has a **canonical signature** — a normal-form description of its orbit structure (for a slot
with $n$ structurally-symmetric children this is the pair "$n$ children with full symmetry," and so on).
We say a schema is **locked** when it is fully specialized and admits this canonicalization. Define an
**obstruction count** $\Omega(K) \ge 0$ measuring the failure of the *local* orbit decomposition to lift
to a *globally* consistent one (each unresolved local-to-global conflict contributes to $\Omega$); a
clean decomposition has $\Omega = 0$.

> **Definition (Crowning).** A schema $K$ **crowns** if the iteration $R^n(K)$ reaches an index $n$ with
> $\mathrm{canon}(R^{n+1}(K)) = \mathrm{canon}(R^n(K))$ **and** $\Omega(R^n(K)) = 0$ — a stable canonical
> form that is, moreover, obstruction-free. We call such a fixed point a **crowned** schema: a structure
> that reproduces its own description under self-abstraction without residual defect.

> **Proposition 3 (Finite convergence).** For a fixed finite schema $K$ (finitely many slots, finite
> arity, canonicalization to a fixed bounded depth), the canonical signatures of the iterates $R^n(K)$
> take values in a *finite* set $S(K)$. Since $R$ is deterministic, the sequence $\big(\mathrm{canon}
> (R^n(K))\big)_n$ is eventually periodic and is reached within $|S(K)|$ steps.

*Proof.* Finite slot set, finite arity, and depth-bounded canonicalization yield finitely many possible
subtree fingerprints, hence finitely many canonical signatures; this finite set is $S(K)$. A
deterministic map on a finite set produces an eventually periodic orbit, and a repeat must occur within
$|S(K)| + 1$ iterates by the pigeonhole principle. $\qquad\blacksquare$

> **Theorem 4 (Decidability of crowning).** For each finite schema $K$, whether $K$ crowns is decidable.

*Proof.* By Proposition 3 the canonical signatures of the iterates repeat within a computable bound
$|S(K)|$. Run $R$ until the canonical signature first repeats (guaranteed to occur within that bound; $R$
and $\mathrm{canon}$ are computable by Propositions 1–2). At the repeat, evaluate the obstruction count
$\Omega$, a computable predicate. The schema crowns precisely when the repeat is a fixed point
($\mathrm{canon}(R^{n+1}(K)) = \mathrm{canon}(R^n(K))$) with $\Omega = 0$. Each step of this procedure
terminates, so the property is decided in finitely many steps. $\qquad\blacksquare$

We state the scope of Theorem 4 precisely, because the natural over-reading is false. The theorem does
**not** assert that every schema crowns. It asserts that the *question* "does $K$ crown?" always receives
a definite, computed answer. There are three mutually exclusive outcomes, and the procedure of Theorem 4
returns exactly one for each $K$:

1. **Crowned** — the iteration reaches a stable canonical form with $\Omega = 0$: a clean self-reproducing
   fixed point.
2. **Not crowned (residual obstruction)** — the iteration reaches a stable canonical form but with
   $\Omega > 0$: the structure repeats itself but carries an unresolved defect, so it is correctly judged
   *not* a clean closure.
3. **Not crowned (no closure)** — the iteration never reaches a stably lockable canonical form.

> **Proposition 4 (Single-slot schemas crown).** If $K$ has a single root slot with finitely many
> children, then $R$ adds exactly the orbit classes of those children beneath the root, and $R$ is
> idempotent on the result: $\mathrm{canon}(R^2(K)) = \mathrm{canon}(R(K))$ with $\Omega = 0$. Hence $K$
> crowns at the first step.

*Proof.* With one slot, the orbit decomposition groups the root's children by their (leaf) fingerprints;
applying $R$ again regroups identical leaves, returning the same canonical signature. No local-to-global
conflict can arise across a single slot, so $\Omega = 0$. $\qquad\blacksquare$

In every case we have examined, where the iteration converges it converges to a *fixed point* (a period-1
cycle), never a longer oscillation; we have observed no two-cycle. We state this as an observation rather
than a theorem: Theorem 4's decidability follows from finite convergence (eventual periodicity) alone and
does not require period one.

------------------------------------------------------------
## 4. Discussion
------------------------------------------------------------

### 4.1 The register: decidability, not universal convergence

It is tempting to ask for a stronger result — that *every* declared schema converges to a clean
self-reproducing fixed point. That is simply false, and ought to be: not every structure one can write
down closes cleanly into itself. The defensible and useful claim is the one we proved: the construction
*forces a definite verdict* on each schema. Whatever a schema does — crown, repeat-with-defect, or fail
to close — the procedure of Theorem 4 detects which. The value of the result is therefore *epistemic*: a
system built on this construction always *knows* whether a given structure has closed cleanly into
itself. The obstruction gate ($\Omega = 0$) is part of the crowning *decision*, not a flaw: a fixed point
carrying an unresolved defect is correctly classified as not-yet-clean.

### 4.2 The reflexive fixed point as a self-knowing state

A crowned schema reproduces its own canonical description under self-abstraction: applying the operator
$R$ returns (the canonical form of) what was put in. This is the order-theoretic signature of a
*self-reproducing* structure — a structure that is a fixed point of the very operation that abstracts it.
Because the operator is type-preserving (Proposition 2), the fixed point is not merely an external
coincidence; the structure literally encodes both the operand and the result of the operation in one and
the same form, so its self-reference is exact — *a point, not a smear*.

We read this as a *self-knowing* state, in the following sense. The reflexive fixed point is not a
brute size-blow-up of the structure; it is the structure having closed into a stable whole *together with
the system's capacity to register that it has done so*. One way to put the interpretation, in plain terms:

> The self-knowing state is the condition of a self-reproducing process that recognizes its own closure:
> produced by a control process governing how the system's boundary closes as it reasons forward, it
> represents *how* it is building itself up through its own steps, and can therefore anticipate its own
> future states — and anticipate that anticipation. In doing so it stabilizes itself and assembles an
> internal record of its own operation: a self-description that lets it resume the very process that
> brought it there without losing the thread.

This is offered as interpretation, not as a theorem. What is *proved* is narrower and exact: the fixed
point exists when the iteration crowns (type-closure plus finite convergence), and whether it is reached
is decidable (Theorem 4). The reading of that fixed point as "the process knowing itself" is a conceptual
gloss on the mathematics, consistent with it but not entailed by it.

### 4.3 What is proved, what is conjectural, what is open

It is important to mark the boundary honestly.

**Proved (for the mathematical model):** $D$ is a Scott domain (Theorem 1); decoding and application are
Scott-continuous, giving a continuous map $\mathrm{app} : D \to [D \to D]$ (Theorem 2); the depth order is
the linear restriction of the observation order (Theorem 3); the self-abstraction operator is
type-preserving and locally computed, the iteration converges in finitely many steps, and crowning is
decidable per schema (Propositions 1–4, Theorem 4).

**Conjectural.** Theorem 2 gives $\mathrm{app}$ as a continuous *map* but not as an *embedding* of $D$
into its function space $[D \to D]$. An embedding would, via the standard inverse-limit construction,
yield a reflexive isomorphism $D \cong [D \to D]$ and an attendant least fixed point. The obstruction is
that $\mathrm{decode}$ *folds*: distinct configurations may decode to comparable content, so
$\mathrm{decode}$ — and hence $\mathrm{app}$ — is not order-reflecting in general. We **conjecture** that
$\mathrm{app}$ becomes an embedding exactly on the *fold-free* subspace — the configurations on which the
decode/encode round-trip is the identity — and we further conjecture that this fold-free subspace
coincides with the obstruction-free ($\Omega = 0$) subspace. We do **not** claim this; it is the natural
remaining question, and it is the precise sense in which "self-reference is a point, not a smear" might
be made rigorous. Importantly, the crowning results (Section 3.5) do **not** depend on this conjecture:
they rest only on type-closure and finite convergence.

**A clean open problem (compositional stability).** Crowning is a property of a single schema. Suppose
several schemas have each crowned. Does *composing* them — assembling a larger structure whose parts are
crowned schemas — yield a structure that again crowns, or can a fresh obstruction appear at the seams?
We leave this open: *it remains open whether crowning is preserved under composition*, i.e. whether one
can guarantee in advance, from the crowned status of the parts, that the assembled whole is
obstruction-free. A positive answer would let crowned components be combined with foresight; a negative
answer would identify composition as the locus where new obstructions are born.

**Explicitly not claimed.** We have *not* claimed that an iteration of the self-abstraction operator
builds the function-space domain $[D \to D]$; the operator performs orbit decomposition, which grows
polynomially in the schema's size, whereas the function space grows super-exponentially, so the two are
not isomorphic and the operator is not the function-space construction. We have likewise *not* used any
large finite symmetry group as a *computed* bound; any such object enters, if at all, only as an
interpretive analogy, never as a step in a proof.

### 4.4 Scope: a theorem about the object

Everything above is a theorem (or a clearly-marked conjecture) about the mathematical object: the
configuration space, its order, its continuous maps, and the self-abstraction operator. Whether a given
running implementation realizes this object faithfully is a separate question, addressed in Appendix A.

------------------------------------------------------------
## 5. Conclusion
------------------------------------------------------------

We have shown that the space of partial observations of a tree of finitely-branching slots, ordered by
"has observed at least as much," is a Scott domain, and that the operations of decoding a configuration
into content and composing two configurations are Scott-continuous for this order. We reconciled the
depth/prefix order with the observation order, exhibiting the former as the linear restriction of the
latter and the latter as the bounded-complete generalization required once configurations branch.
Finally, we analyzed a self-abstraction operator and proved that whether a schema *crowns* — stabilizes
into an obstruction-free, self-reproducing fixed point — is decidable for each schema, while being honest
that not every schema crowns. The mathematical upshot is that this observation order, with its limits,
finite approximants, and decidable self-stabilization, is a sound substrate over which a system may
compute, take limits of computation, and form self-referential fixed points without paradox. The
principal open questions — whether the application map embeds the domain into its own function space on
the fold-free subspace, and whether crowning is preserved under composition — are stated precisely above
and left for future work.

------------------------------------------------------------
## Appendix A. Correspondence to an implementation
------------------------------------------------------------

The mathematical object of this paper was abstracted from a concrete computational system, and it is
worth recording, in prose, which parts of the model correspond to *computations the system performs*,
which are *mathematical structure laid over the system's data*, and which are *intended but not yet
built*. This separation is itself a faithfulness statement: it says exactly how far the implementation
is evidence for the model.

**Realized as computations.** The carrier is real: the system constructs configurations (as digit
strings over its slot trees), enforces tree-consistency when it opens child slots, and enumerates
configurations. Decoding is a live operation — the system interprets a configuration against its meaning
structure — and the round-trip between a configuration and its decoded form is verifiable (encoding then
decoding returns the original). The self-abstraction operator is real and *type-preserving*: it consumes
a schema and returns a schema of the same type, which is the homoiconicity used in Proposition 2.
Orbit decomposition is computed locally per slot from a bounded-depth subtree fingerprint, matching
Proposition 1, and the iteration that detects a stable canonical form (the crowning check, including the
obstruction gate) runs and terminates, consistent with Theorem 4 and Proposition 4 (small single-slot
schemas are observed to crown at the first step).

**Mathematical structure over the system's data.** The order $\sqsubseteq$ and the entire
directed-complete-partial-order apparatus (least upper bounds, finite elements, bounded-completeness) are
*not* runtime notions: the system produces the configurations that constitute the carrier, but it never
*compares* two configurations and has no operation that ascends the order — its state-changing operation
mutates a configuration rather than computing a supremum. This is exactly what Theorem 1 requires: a
Scott domain is a *set of configurations together with an order defined on them*, and the order here is a
mathematical construction over the carrier the system genuinely produces. Any informal claim that the
system "respects the order at runtime" would be incorrect and should be read instead as: the order is
well-defined over the system's live data; the system itself does not compare configurations.

**Intended but not yet surfaced.** Some derived reporting structure — for instance a summary of the
sequence of sub-domains a schema traverses (a boundary/closure report) — exists as a computable function
over the live data but is not currently exposed through the system's interface; surfacing it is a matter
of wiring, not new mathematics. We flag this so that the gap between "the structure exists in the data"
and "the system reports it" is not mistaken for a gap in the model.

The net correspondence is therefore: the carrier and the computational mechanics (configuration
construction and enumeration, decoding, the type-preserving self-abstraction operator, local orbit
computation, finite crowning, and the encode/decode round-trip) are realized; the order-theoretic layer
is mathematical structure over that realized carrier; and one derived report is intended but not yet
exposed. None of these caveats affects the theorems, which concern the mathematical object.
