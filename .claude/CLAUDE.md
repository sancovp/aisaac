# AIsaac Site — TWI

Static site at sancovp.github.io/aisaac/. GitHub Pages. Mercurial Cyberglass theme.

## Structure
- `style.css` — main site CSS (all non-blog pages)
- `blog/blog-style.css` — blog post CSS
- `sticky-cta.js` — injected on all pages: sticky bottom bar + qualification modal
- `pricing.html` — hidden one-sheet, NOT linked from nav, sent during calls only
- `docs/` — design docs (not served, reference only)

## Funnels
- B2B: index survey → transform.html → demo consent → AI cascade (Vapi TBD)
- B2C: school.html (Dr Capitalism MIFGE, wantrepreneur path)
- Free: free.html (bento grid of tools, repos, frameworks)
- All CTAs route through qualification — no direct cal.com links on public pages except inside apply.html fallback and pricing.html

## Content Rules
- No dollar amounts on public B2B pages (transform.html). Numbers are on pricing.html only.
- Blog posts have category CTAs (transform/build/learn) before the footer.
- 81 AI-IMAGE placeholders across blogs — each must install a belief or overcome an objection.
- The joke (L1 voice agent = 10 min setup) is NEVER on the site. It's structural, discovered by the client.

## Deploy
```bash
git add . && git commit -m "message" && git push
```
GitHub Pages deploys automatically from main branch.
