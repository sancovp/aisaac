# RULE 00 — THE SITE CANON (nobody edits this site without reading their sources)

**The law (Isaac, 2026-08-07, verbatim intent): NOBODY MAY EDIT THE SITE WITHOUT BEING
TOLD WHAT TO READ TO PUT THERE.** An agent editing any page reads that page's canonical
sources FIRST and puts THEIR content there — never its own summary, never an
orchestrator's paraphrase, never invented copy. If a surface's source row below is
missing or stale, that is a BLOCKER to report, not a gap to fill with judgment.

## Hard laws (apply to every page, before any source)

1. **OFFERS ARE FROZEN.** Prices, products, tiers, session lengths, guarantees,
   paid-CTA wording: Isaac only. Source of truth = `main:pricing.html` verbatim.
   Discrepancies (arithmetic, collisions) are EVIDENCE for a `FOR ISAAC` report block —
   never resolved by an agent. (Order of 2026-08-07: "STOP CHANGING MY OFFERS.")
2. **Lore firewall at the door.** Top-of-funnel pages: zero canon-internal vocabulary.
   The inner register lives in `inside/` only (reachable from system.html, never from
   the door). Isaac's PERSONAL pages may carry his real register — plain statement
   first, flavor after, never as prerequisite vocabulary.
3. **No uncashed claims.** A claim ships with its receipt or ships as a labeled IOU.
   No fabricated numbers, no uptime claims nobody verified, no fake dashboards
   (world-slots stay empty until real footage exists).
4. **Voice** = `~/aios-research/GARAGE-LAB-LAUNCH-STRATEGY.md` §1c: scoreboard readings
   not verdicts ("is losing, not is a loser"); shown never claimed; punch at the
   discourse never at names; arrogance budget == receipt balance.
5. Layout system = the `_templates/` + `style.css` skeleton; relative in-page paths;
   absolute SITE_ORIGIN (`https://sancovp.github.io/aisaac`) only in canonical/og.

## THE SOURCE MAP — per surface, what you READ to know what goes there

| surface | canonical sources (READ THESE, in order) |
|---|---|
| **the whole funnel** (IA, what sells, the ladder) | `~/aios-research/FLYWHEEL.md` (THE SPINE) · `~/aios-research/THE-CLINIC-MAP.md` (Isaac's operating-structure ruling) · `~/aios-research/THE-OFFER-AND-FUNNEL.md` (the concrete money offer) · `~/aios-research/ME2C-FUNNEL.md` (creator side) |
| **positioning / category** | `~/aios-research/GARAGE-LAB-LAUNCH-STRATEGY.md` §0 (simulations-and-world-loops ruling: "iteration doesn't compound; worlds compound"), §1 (legibility grammar), §1b (content pipeline), §1c (voice) |
| **index.html / the door** | the two rows above + `~/aios-research/SITE-CEO-BRANCH-REVIEW.md` (live decisions incl. hero-first) |
| **isaac.html (the hero site)** | `GARAGE-LAB-LAUNCH-STRATEGY.md` §1c · `~/aios-research/HJ-GAUGE-SPEC.md` (the theses) · `~/repo/garage-lab/CATALOG.md` + `INDEX.md` (the receipts) · `~/repo/garage-lab/CLAIM-AUDIT.md` (the honest claim board) · myth flavor ONLY from `~/repo/sra-git/research/ssri/SANCTUARY-MYTH-ORIGIN.md` Part V |
| **pricing.html** | `main:pricing.html` VERBATIM + Isaac. No other source exists. |
| **rung pages (learn/build/run)** | the funnel row (FLYWHEEL/CLINIC-MAP/OFFER-AND-FUNNEL) for what each rung IS; product truth for jobworld surfaces from `~/aios-research/SYSTEM-ROLLUP.md` + the avi-jw rules (`/agent/.claude/rules/00,05,07`) — honest grades only |
| **watch.html / world demos** | real run receipts ONLY: cave-teams live tests (`test_live_skillcraft.py` runs), future footage per `GARAGE-LAB-LAUNCH-STRATEGY.md` §1b. Never generated numbers. |
| **blog/ + notes/ (field notes)** | the posts' own content (conform layout only) · new notes draw from `~/repo/garage-lab/CATALOG.md` entries (receipted patterns) · **the tag vocabulary + every post's tags = `tools/tags.py`, the single source both generators read — a new post is TAGGED THERE or the build fails** |
| **inside/ (the lored register)** | `SANCTUARY-MYTH-ORIGIN.md` · `HJ-GAUGE-SPEC.md` · the train doc — this is the ONE place the inner register ships |
| **audience/market claims** | `~/aios-research/WAVE-STATE-BRIEF.md` · `~/aios-research/reports/` — cite or omit |
| **archetype/rung strategy** (why the site is shaped this way) | `~/repo/sra-git/research/ssri/ship/SANCTUARY-WASTELAND-BATTLESPACE.md` §7m/§7m-bis (Dudjom→Hormozi transition; Mipham-with-a-door = free-the-WHAT / paid-the-how-I) |

## Decision log (rulings that bind edits; newest first)

- 2026-08-08 (Isaac, verbatim — the buyer's five questions; every surface answers its
  own): "most of marketing is actually organization and if it feels like the organized
  thing is the occurrence of 'you finding the organized treasure trove of xyz' then you
  go 'omg omg omg'... a) does it LOOK LIKE the information isnt bullshit, is useful, is
  what i need? b) is there a lot? is it really organized? am i going to get everything
  i need even tho i dont know what that means? c) so what should i expect? is this what
  i expect i should expect? d) ok what are the guarantees e) can i afford this relative
  to the way the guarantees change my life?" — a/b/c = the free surfaces' job (door,
  blog/tags, repos, notes); d/e = the OFFER layer (pricing — Isaac authors, frozen).

- 2026-08-08 (Isaac, verbatim): "in the blog search, we have by tags, but those tags
  are not by extremely important concept in my system so it doesnt feel as branded as
  it could... shouldnt you be able to search for like the 7 levels of agent engineering
  itself as a filter? ... this kind of unbrandedness is rampant." **THE BRANDED-FILTER
  LAW: every browse/filter surface filters by HIS FRAMEWORK CONCEPTS, never by generic
  categories.** The corpus index now files all 64 pieces under the seven levels of
  agent engineering (the flagship framework, `lab/explainer.html` →
  `blog/levels-overview.html`) plus the cross-cutting concepts. Vocabulary and
  assignments: `tools/tags.py`, whose four laws bind — the seven levels are the spine ·
  door register only (law 2 above) · no orphan tags and 1–3 tags per post, both checked
  mechanically at build time · ONE corpus, ONE tag index. Unbrandedness elsewhere is
  the same defect: when a surface sorts, it sorts by the framework.

- 2026-08-08 (Isaac, verbatim, on first seeing the rebuild): "it's this 'okay okay, i
  get it, theres a thing, where do i go next?' thats the mark of a real funnel. Human
  recognition that the info there is safe and they want the next part. They wont go
  back and really read it all unless you put an offer that makes them pause. Either
  they convert or pause and then either convert or leave. Thats it." — every page
  tests against this: safe + where-next.

- 2026-08-07 (later): **THE PRODUCT-LANDING RULING (Isaac): the site's main job is to
  be an AWESOME LANDING PAGE for cave-teams and dark-factory.** The engineer descent
  ends at dark-factory's README (which literally ends in a clone command — the door's
  original promise, now cashable). Source-map addition: **build.html ← dark-factory
  README (github.com/sancovp/dark-factory) + cave-teams README — reuse THEIR copy;
  they are the best zero-lore public text in the ecosystem; do not paraphrase over
  them.** dark-factory's one-liner is wave-answer-grade: "no human is in the loop;
  what stops it shipping garbage is three independent gates ending in a controlled
  experiment."

- 2026-08-07 (late): **THE RATCHET LAW OF NAVIGATION (Isaac, verbatim): "fundamentally
  a funnel is a series of ratcheted options such that the avatar can't figure out how
  to do anything except sanctioned moves."** Consequences: top-left/brand button →
  isaac.html (the hub); index.html = ENTRYPOINT ONLY, one-way — no nav routes back to
  it after first pass (browser-back only); every page's visible exits ARE its
  sanctioned moves — nav is a grammar, design each page's exit set deliberately.

- 2026-08-07: hero site FIRST (Isaac: the site is about him + what he thinks, funnel
  downstream) · offers frozen · funnel category = simulations-and-world-loops ·
  h1 policy: the scoreboard line returns only when a scoreboard page is published.
- Open (SITE-CEO-BRANCH-REVIEW.md §4): custom domain · repo-name L3 exception ·
  watch.html build · merge-source deletions.

## Maintenance

This rule is the unification point. Every new ruling about site content lands HERE the
same session (decision log) or in the source map. An edit made without reading this
file's sources is a defect regardless of how good it looks.
