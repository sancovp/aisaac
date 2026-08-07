# RULE 02 — THE STYLE (Mercury Glass // Living Instrument)

**The ruling (2026-08-07, CEO-decided per Isaac's delegation "come up with whatever
style this should be"):** the site keeps and ELEVATES Builder A's Mercurial-cyberglass
base. The look is **a living instrument, not a brochure** — the visual register of an
observatory reading a running world. Nothing here is decoration; every visual choice
serves RULE 01's deducibility mechanics.

## The language

1. **Base (KEEP, already law in style.css):** `--void` near-black · glass panels ·
   ONE accent (`--mercury-blue`) · JetBrains Mono for receipts/labels · Inter for UI ·
   self-hosted fonts, zero external requests · three breakpoints declared once.
2. **Display voice (ADD):** one OFL display serif (Fraunces preferred; Spectral
   acceptable), self-hosted woff2, used ONLY for: h1/h2 claims, the myth-register
   lines, pull-quotes. Everything else stays Inter/Mono. This is the single biggest
   de-generic move; it separates the voice of the claims from the voice of the chrome.
3. **The density gradient (ADD — depth made visible):** the DOOR is spacious (huge
   type, few elements, one action); each descent level gets visually denser (tighter
   leading, more mono, more hairline rules, data-table energy at the code-adjacent
   depths). A visitor FEELS the descent. Implement as a per-page `data-depth="0|1|2|3"`
   attribute on <body> with token overrides — no per-page CSS.
4. **Instrument details:** hairline rules (`--glass-border`) as the structural line
   language · mono micro-labels (already in use: "THE RECEIPT") · live-data styling
   (pulse/glow) is RESERVED for genuinely live/running things — a static element
   styled as live is the fake-dashboard sin in CSS form.
5. **Restraint laws:** no new colors, ever, without editing THIS rule · no gradients
   beyond the existing glass shine · no stock imagery, no emoji in chrome · motion
   ONLY inside the world engine + micro-transitions ≤200ms; `prefers-reduced-motion`
   respected everywhere · diagrams are inline SVG in token colors only.

## Mechanical quality gates (tools/style_qa.py — run before any style commit)

- WCAG AA contrast computed from the actual token values for every text/bg pair.
- Zero inline `style=` attributes; zero page `<style>` over 20 lines (existing law).
- Single h1 per page; every `<img>` has width/height; og:image exists per page-type.
- No font-family declarations outside style.css; no hex colors outside the token block.

## What "high-end" means here, testably

A stranger screenshots any page: it reads as one designed object with the door's
signature (void + glass + serif claims + mono receipts). No page could be mistaken for
a template default, a Notion export, or a generic SaaS landing page. The door's first
viewport contains: the running world, one serif claim, one Enter. Nothing else.
