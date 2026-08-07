# REDIRECTS — the full table (Builder C)

Every killed or renamed URL and where it goes. Builder B hands its six merged source
files to this table at B5 (§5, cross-builder contract #3); those rows are marked **[B]**.

## Hosting reality — read before implementing

The site is served from **GitHub Pages** (`origin` = `github.com/sancovp/aisaac`, no
`CNAME` file). GitHub Pages **cannot issue a 301** for a path it serves statically:
there is no `.htaccess`, no `_redirects`, no config file it honours. So "301" here means
one of two things, in preference order:

1. **If the site moves behind a host that can redirect** (Cloudflare Pages/Workers,
   Netlify, an nginx front) — implement these as real `301`s. That is the correct end
   state; it preserves link equity and costs one config file.
2. **On GitHub Pages as it stands today** — each row ships as a *redirect stub*: a file
   at the old path containing `<meta http-equiv="refresh" content="0;url=…">`,
   `<link rel="canonical">` pointing at the destination, **and a real visible link**.
   `content` must be `0` — a timed refresh with a visible delay is a WCAG 2.2.1 failure
   and is exactly why `agents.html` was killed.

`frameworks.html` is already built as a compliant stub (43 historical inbound links) and
is the template for every other row. Everything else in the table still needs its stub
written — **that is the one piece of C5 the integrator must generate**, mechanically,
from this table.

## Internal links are already fixed

No stub is load-bearing for internal navigation. Builder C rewrote every internal link to
a killed surface across the 54 blog notes at C1 (`LINK_MAP` in the renderer patch), and
the rebuilt `blog/index.html`, `notes/**`, `inside/**`, `404.html` are written against the
final URL set. The stubs exist for **external** inbound links and bookmarks.

## The table

### Killed root pages

| Old URL | → | Destination | Why |
|---|---|---|---|
| `/agents.html` | 301 | `/notes/` | Empty forced-refresh page. |
| `/frameworks.html` | 301 | `/notes/` | ✅ stub written. 43 inbound links. |
| `/advertorial.html` | 301 | `/notes/the-ten-minute-product-priced-like-magic.html` | Headline salvaged onto that note. |
| `/sanctuary-nexus.html` | 301 | `/system.html` | Orphaned broken shell. |
| `/dharma-concierge.html` | 301 | the property's new home (off-domain) | Dead loop; name-collided with `/dharma-concierge/`. |
| `/dharma-concierge/*` | 301 | the property's new domain | Whole brand moves off this domain (KILLS §D). |
| `/how_i.html` | 301 | `/learn.html` | Stub. |
| `/join.html` | 301 | `/learn.html` | Community becomes a priced line. **[B]** |
| `/level10.html` | 301 | `/learn.html` | Origin-story stub. |
| `/dr-capitalism.html` | 301 | `/learn.html` | Competing category. |
| `/jobworld-premium.html` | 301 | `/run.html` | Tombstone. |
| `/soma-start.html` | 301 | `/pricing.html` | Third price surface. **[B]** |
| `/phone-agent.html` | 301 | `/run.html` | Wrong category. |
| `/ralph.html` | 301 | `/build.html` | Internal tool page. |
| `/vajra-value-shop.html` | 301 | `/inside/why.html` | Two lines salvaged there. |
| `/business-buddhism.html` | 301 | `/inside/why.html` | Its one real claim lives there. |

### Moved to `inside/` (unlisted, `noindex`)

| Old URL | → | Destination |
|---|---|---|
| `/opera.html` | 301 | `/inside/engine.html` |
| `/gnosys.html` | 301 | `/inside/gnosys.html` |
| `/sanctuary-system.html` | 301 | `/inside/sanctuary-system.html` |
| `/completely-fake-dharma.html` | 301 | `/inside/fake-dharma.html` |

### Merged by Builder B **[B]**

> **Do not delete these six before their stubs exist.** Builder B has finished all four
> rung pages and handed the sources over; they must be removed **atomically with the
> redirects landing**, in one commit. `apply.html` alone still has 26 inbound links
> site-wide, so deleting it a commit early turns 26 live links into 404s. Order:
> generate stubs → verify with the block at the bottom of this file → delete the sources.

`build.html` changes meaning — it is rung 3 now, not rung 4. The old `build.html`
content became `run.html`. Any external link to `/build.html` expecting the Jobworld
autopilot demo now lands on the open-source rung, so this row is a **redirect of
meaning, not of path**, and B must confirm the trade is acceptable.

| Old URL | → | Destination | Note |
|---|---|---|---|
| `/apply.html` | 301 | `/pricing.html` | 26 pages linked here. Its email capture silently dropped every address. |
| `/transform.html` | 301 | `/run.html` | Merged. |
| `/school.html` | 301 | `/learn.html` | Merged. |
| `/free.html` | 301 | `/learn.html` | Offer half → learn; library half → `/notes/`. |
| `/promptworld.html` | 301 | `/build.html` | Renamed to rung 3. |
| `/soma.html` | 301 | `/run.html` | Became a tier. |
| `/sancrev.html` | 301 | `/system.html` | Map half → system; price half → pricing. |
| `/build.html` (old meaning) | — | `/run.html` | Meaning change, not a path redirect. See note above. |

### Blog merges

| Old URL | → | Destination |
|---|---|---|
| `/blog/admissibility-engineering.html` | 301 | `/blog/admissibility.html` |
| `/blog/concentration-engineering.html` | 301 | `/blog/l6-concentration.html` |
| `/blog/doctor.html` | 301 | `/pricing.html` |

### Not redirected

| URL | Disposition |
|---|---|
| `/builds/edwards-heating-air/*` | **410 / plain removal.** A live third party's identity on a domain they never agreed to — do not redirect it anywhere, remove it. |
| `/b2b-bootcamp/*`, `/content-engine/*`, `/ai-operating-system-positioning/*`, `/docs/*`, `/books/*`, `/free-layer/*.md` | Plain removal. Internal `.md` corpora; nothing should have been linking to them. |

## Verification after the stubs are generated

```bash
# every killed path resolves (stub exists or host rule covers it)
# every stub is content="0" — a timed delay is a WCAG 2.2.1 failure
grep -rl 'http-equiv="refresh"' --include=*.html . \
  | xargs grep -L 'content="0;' ; echo "^ must be empty"

# no surviving internal link points at a killed surface
grep -rEo 'href="[^"]*(apply|transform|school|free|promptworld|soma|sancrev|opera|gnosys|join|level10|ralph|phone-agent|agents|advertorial|vajra-value-shop|business-buddhism|dr-capitalism|jobworld-premium|soma-start|how_i|sanctuary-nexus|dharma-concierge)\.html"' \
  --include=*.html . ; echo "^ must be empty"
```
