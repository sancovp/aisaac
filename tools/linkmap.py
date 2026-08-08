"""The one link-rewrite map: every killed/renamed URL -> its live target.

Single source of truth for (a) rewriting in-body links inside salvaged content,
(b) generating the redirect table, (c) generating KILLS.md. If a URL is retired,
it gets a row here and nowhere else.

NOTE the rename that is easy to get wrong (§2.2): `build.html` CHANGES MEANING.
Old build.html = the Jobworld autopilot page = rung 4 = now `run.html`.
New build.html = rung 3 = "run your work inside one" (from promptworld.html).
Every legacy link to build.html therefore points at /run.html, NOT /build.html.
"""

# old page (basename) -> new root-absolute target
REDIRECTS = {
    # --- renamed / merged offers (Builder B's sources) ---
    "build.html": "/run.html",             # old Jobworld page -> rung 4
    "transform.html": "/run.html",
    "soma.html": "/run.html",
    "promptworld.html": "/build.html",     # -> rung 3
    "school.html": "/learn.html",
    "free.html": "/learn.html",
    "apply.html": "/pricing.html",
    "sancrev.html": "/pricing.html",
    "soma-start.html": "/pricing.html",
    # --- unlisted canon (moved into inside/) ---
    "opera.html": "/inside/engine.html",
    "gnosys.html": "/inside/gnosys.html",
    "sanctuary-system.html": "/inside/sanctuary-system.html",
    "completely-fake-dharma.html": "/inside/fake-dharma.html",
    "business-buddhism.html": "/inside/why.html",
    "vajra-value-shop.html": "/inside/why.html",
    # --- killed outright ---
    "agents.html": "/notes/",
    "frameworks.html": "/notes/",
    "advertorial.html": "/notes/the-ten-minute-product-priced-like-magic.html",
    "sanctuary-nexus.html": "/",
    "dharma-concierge.html": "/inside/fake-dharma.html",
    "how_i.html": "/learn.html",
    "join.html": "/learn.html",
    "level10.html": "/learn.html",
    "dr-capitalism.html": "/learn.html",
    "jobworld-premium.html": "/run.html",
    "phone-agent.html": "/run.html",
    "ralph.html": "/build.html",
    # --- blog: duplicate-claim pairs collapse onto the canonical slug ---
    "blog/admissibility-engineering.html": "/blog/admissibility.html",
    "blog/concentration-engineering.html": "/blog/l6-concentration.html",
    "blog/doctor.html": "/notes/",
}

# Pages that survive but whose links must not be rewritten.
KEEP = {
    "index.html", "system.html", "watch.html", "learn.html", "pricing.html",
    "run.html", "notes/", "blog/", "404.html",
}


def rewrite_href(href, up=""):
    """Map one href onto its live target, expressed RELATIVE to the calling
    page (A's path law: the site sits on a GitHub Pages project subpath, so
    root-absolute paths 404). `up` is "" at the repo root, "../" one level down.

    Returns the href unchanged if it is external, an anchor, or already points
    at something that survives."""
    if not href or href.startswith(("http://", "https://", "#", "mailto:")):
        return href
    # normalise ./ and ../ away so the comparison is on the site-relative path
    probe = href
    while probe.startswith(("./", "../")):
        probe = probe[2:] if probe.startswith("./") else probe[3:]
    frag = ""
    if "#" in probe:
        probe, frag = probe.split("#", 1)
        frag = "#" + frag
    if probe in ("index.html", ""):
        return up + "index.html" + frag
    target = REDIRECTS.get(probe)
    if target is None:
        return href
    return up + target.lstrip("/") + frag

# Idempotency note: this is safe to run over its own output because after one
# pass no body still contains a REDIRECTS *key*. The one key that is also a
# target is `build.html` (legacy Jobworld page -> run.html; new rung 3 ->
# build.html), and the only sources that resolve TO build.html are
# promptworld.html and ralph.html, which zero blog bodies reference
# (verified against git HEAD). If that ever changes, split this into a
# body-map and a redirect-map rather than letting the two meanings collide.
