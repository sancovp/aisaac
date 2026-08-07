#!/usr/bin/env bash
# Builder C's acceptance gate. Exits non-zero on any failure.
#   bash tools/check-site.sh
#
# Scope: the surfaces C owns (blog/, notes/, inside/, 404.html, redirect stubs)
# plus the two site-wide laws C is responsible for enforcing (no stray markdown,
# no timed meta-refresh). It does NOT check Builder A's or B's pages.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
fail=0
chk() { # chk <description> <expected-count> <actual-count>
  if [ "$2" = "$3" ]; then printf '  ok    %s\n' "$1"
  else printf '  FAIL  %s  (expected %s, got %s)\n' "$1" "$2" "$3"; fail=1; fi
}

PAGES=$(ls blog/*.html notes/*.html inside/*.html 404.html 2>/dev/null)
# CONTENT pages = everything except 404 and the redirect stubs. Only content
# pages carry canonical/og: a 404 must not declare a canonical URL, and a stub
# already points its canonical at the target rather than at itself.
CONTENT=$(for f in $PAGES; do
  case "$f" in 404.html) continue;; esac
  grep -q 'http-equiv="refresh"' "$f" || echo "$f"
done)

echo "── head contract (§2.3) ──"
chk "every page has <!doctype>"  0 "$(grep -Li '<!doctype'  $PAGES | wc -l)"
chk "every page has <title>"     0 "$(grep -Li '<title>'    $PAGES | wc -l)"
chk "every page has viewport"    0 "$(grep -Li 'viewport'   $PAGES | wc -l)"
chk "content pages have canonical" 0 "$(grep -Li 'rel="canonical"' $CONTENT | wc -l)"
chk "content pages have og:title"  0 "$(grep -Li 'og:title'   $CONTENT | wc -l)"

echo "── path law (relative in-page; project subpath deploy) ──"
chk "no root-absolute href" 0 "$(grep -o 'href="/[^"]*"' $PAGES 2>/dev/null | wc -l)"
chk "no root-absolute src"  0 "$(grep -o 'src="/[^"]*"'  $PAGES 2>/dev/null | wc -l)"

echo "── one claim per surface (L1) ──"
chk "exactly one <h1> per page" 0 \
  "$(for f in $PAGES; do [ "$(grep -c '<h1' "$f")" = 1 ] || echo "$f"; done | wc -l)"
# inside/* is TYPE 5 UTILITY: block order is B0 B1 [content] B10 — no B9 CTA
# is required. inside/fake-dharma.html deliberately has ZERO CTAs: it is
# authored lore kept in its own voice, and putting a sales button on it is
# exactly the thing the rebuild is removing. 0 or 1 is legal there; every
# other page must have exactly 1.
chk "exactly one .cta-primary per page" 0 \
  "$(for f in $PAGES; do n=$(grep -c 'class="cta-primary"' "$f")
       case "$f" in inside/*) [ "$n" -le 1 ] || echo "$f";;
                    *)        [ "$n" = 1 ]   || echo "$f";; esac; done | wc -l)"

echo "── one nav, one stylesheet (§2.1, §2.2) ──"
chk "no legacy nav markup"   0 "$(grep -l 'site-header\|isaac-site\|class="nav-link"' $PAGES | wc -l)"
chk "blog-style.css unused"  0 "$(grep -l 'blog-style.css' $PAGES | wc -l)"
chk "no page-local @media"   0 "$(grep -l '@media' $PAGES | wc -l)"
# match the TAG, not the filename — the word appears in an explanatory comment
chk "no dead scripts"        0 "$(grep -lE '<script[^>]*(sticky-cta|exit-popup|newsletter)' $PAGES | wc -l)"

echo "── inside/ is unlisted (§1.2 TYPE 5) ──"
chk "every inside/ page noindex" 0 "$(grep -Li 'robots.*noindex' inside/*.html | wc -l)"

echo "── redirects (§1.2 TYPE 5) ──"
chk "no timed meta-refresh (WCAG 2.2.1)" 0 \
  "$(grep -rl 'refresh" content="[1-9]' --include=*.html . | wc -l)"
chk "every refresh stub has a visible link" 0 \
  "$(for f in $(grep -rl 'http-equiv="refresh"' --include=*.html . 2>/dev/null); do
       grep -q 'cta-primary' "$f" || echo "$f"; done | wc -l)"

echo "── the raw-markdown leak (§2.5) ──"
# .nojekyll makes every .md in the repo publicly fetchable. KEEP .nojekyll,
# REMOVE the markdown. See KILLS.md section B1.
stray=$(find . -name '*.md' -not -path './.git/*' -not -name 'README.md' \
        -not -name 'KILLS.md' | wc -l)
chk "no stray .md ships" 0 "$stray"
if [ "$stray" != "0" ]; then
  echo "        ^ still staged for removal — see KILLS.md section B"
fi

echo
[ "$fail" = 0 ] && echo "PASS" || echo "FAIL"
exit $fail
