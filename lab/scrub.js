/*!
 * aisaac explainer lab — scroll-scrub driver.
 *
 * Scroll mechanics adapted from oso95/scroll-world, references/scrub-engine.js
 * (MIT License, Copyright (c) 2026 cyw): segment scroll-range layout, the
 * smoothstep copy-opacity curves (first section greets, last holds, middle
 * peaks mid-range), the damped lerp toward the scrub target, route dots,
 * reduced-motion behavior. The <video>.currentTime scrubbing at that engine's
 * core is replaced here by seekTo() on LIVE @remotion/player mounts — there
 * are no media files on this page; scroll drives the composition clock.
 *
 * Pure math is exported for node tests when require()d; the browser side
 * mounts on DOMContentLoaded.
 */
(function () {
  'use strict';

  // ---- pure math (node-testable) ------------------------------------------
  var clamp = function (x, a, b) {
    a = a == null ? 0 : a; b = b == null ? 1 : b;
    return Math.min(b, Math.max(a, x));
  };
  var smooth = function (x) { x = clamp(x); return x * x * (3 - 2 * x); };

  /** Scroll progress 0..1 -> composition frame (float, caller rounds). */
  function frameForProgress(p, duration) {
    return clamp(p) * (duration - 1);
  }

  /**
   * Copy-card opacity for section i of N at its local progress pr
   * (pr < 0 => before its range, pr > 1 => after). scroll-world's read() curves.
   */
  function copyOpacity(i, N, pr) {
    var before = pr < 0, after = pr > 1;
    if (i === 0) return after ? 0 : smooth(1 - clamp(pr) / 0.62);
    if (i === N - 1) return before ? 0 : smooth(clamp(pr) / 0.4);
    return (before || after) ? 0 : smooth(1 - Math.abs(pr - 0.5) / 0.5);
  }

  /** One damped lerp step toward target (scroll-world's raf smoothing). */
  function lerpStep(cur, target, k) {
    return cur + (target - cur) * k;
  }

  /** Local progress of beat {start, frames} at global float frame f. */
  function beatProgress(f, beat) {
    return (f - beat.start) / beat.frames;
  }

  var API = {
    clamp: clamp, smooth: smooth, frameForProgress: frameForProgress,
    copyOpacity: copyOpacity, lerpStep: lerpStep, beatProgress: beatProgress,
  };
  if (typeof module !== 'undefined' && module.exports) { module.exports = API; return; }

  // ---- browser mount --------------------------------------------------------
  var VH_PER_BEAT = 1.35;  // viewport-heights of scroll per sentence (diveScroll)
  var LERP_K = 0.16;       // damped scrub factor per rAF
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function boot(tries) {
    var B = window.AisaacBackdrop;
    // The presenter bundle is heavier; give it a beat, then proceed without it
    // (backdrop-only degrade) rather than blocking the page.
    var P = window.AisaacPresenter;
    if (!B || (!P && (tries || 0) < 75)) {
      return setTimeout(function () { boot((tries || 0) + 1); }, 40);
    }
    mount(B, P || null);
  }

  function mount(B, P) {
    var world = document.getElementById('scrub-world');
    var copylayer = document.getElementById('copylayer');
    var route = document.getElementById('route');
    var hint = document.getElementById('scroll-hint');
    if (!world || !copylayer) return;

    var N = B.beats.length;
    var DUR = B.duration;
    var totalVh = VH_PER_BEAT * N;   // scroll distance in viewport-heights

    // copy cards + route dots from the SAME beats the composition runs on
    var cards = [], dots = [];
    B.beats.forEach(function (b, i) {
      var c = document.createElement('article');
      c.className = 'copy-card';
      c.innerHTML =
        '<span class="copy-card__num">' + pad(i + 1) + ' / ' + pad(N) + '</span>' +
        (b.eyebrow ? '<span class="copy-card__eyebrow">' + esc(b.eyebrow) + '</span>' : '') +
        '<p class="copy-card__line">' + esc(b.line) + '</p>';
      copylayer.appendChild(c); cards.push(c);
      if (route) {
        var d = document.createElement('button');
        d.className = 'route-dot';
        d.setAttribute('aria-label', b.eyebrow || ('sentence ' + (i + 1)));
        d.innerHTML = '<span>' + esc(b.eyebrow || '') + '</span><i></i>';
        d.addEventListener('click', function () { jumpTo(i); });
        route.appendChild(d); dots.push(d);
      }
    });

    var vh = window.innerHeight, worldTop = 0, scrollRange = 1;
    var target = 0, cur = 0, lastSent = -1, activeDot = -1, ticking = false;

    function layout() {
      vh = window.innerHeight;
      world.style.height = Math.round((totalVh + 1) * vh) + 'px';
      var r = world.getBoundingClientRect();
      worldTop = r.top + (window.scrollY || window.pageYOffset);
      scrollRange = totalVh * vh;
      read();
    }

    function jumpTo(i) {
      var b = B.beats[i];
      var mid = (b.start + b.frames * 0.5) / (DUR - 1);
      window.scrollTo({
        top: worldTop + mid * scrollRange,
        behavior: reduce ? 'auto' : 'smooth',
      });
    }

    function read() {
      var y = clamp((window.scrollY || window.pageYOffset) - worldTop, 0, scrollRange);
      var p = y / scrollRange;
      target = frameForProgress(p, DUR);

      var f = target;
      var near = 0;
      for (var i = 0; i < N; i++) {
        var pr = beatProgress(f, B.beats[i]);
        var op = copyOpacity(i, N, pr);
        cards[i].style.opacity = op;
        cards[i].style.transform =
          'translateY(calc(-50% + ' + (reduce ? 0 : (0.5 - clamp(pr)) * 4) + 'vh))';
        cards[i].style.pointerEvents = op > 0.5 ? 'auto' : 'none';
        if (pr >= 0) near = i;
      }
      if (near !== activeDot) {
        activeDot = near;
        dots.forEach(function (d, k) { d.classList.toggle('is-active', k === near); });
      }
      if (hint) hint.style.opacity = clamp(1 - y / (0.5 * vh));
      ticking = false;
    }

    function raf() {
      cur = reduce ? target : lerpStep(cur, target, LERP_K);
      var f = Math.round(cur);
      if (f !== lastSent) {
        lastSent = f;
        B.setFrame(f);
        if (P) P.setFrame(f);
      }
      requestAnimationFrame(raf);
    }

    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(read); }
    }, { passive: true });
    window.addEventListener('resize', layout);

    layout();

    // dev/screenshot hook: ?p=0.42 previews the page STATE at 42% scrub
    // progress without scrolling — frame + copy cards are set directly, once,
    // and the rAF loop never starts, so a headless screenshot is deterministic
    // (old-headless screenshot passes don't honor position:sticky, so a real
    // scroll would show the empty track). Production path: no param.
    var pq = Number(new URLSearchParams(location.search).get('p'));
    if (Number.isFinite(pq) && pq > 0) {
      cur = target = frameForProgress(clamp(pq), DUR);
      var f = Math.round(cur);
      for (var i = 0; i < N; i++) {
        var pr = beatProgress(f, B.beats[i]);
        var op = copyOpacity(i, N, pr);
        cards[i].style.opacity = op;
        cards[i].style.transform =
          'translateY(calc(-50% + ' + ((0.5 - clamp(pr)) * 4) + 'vh))';
        if (pr >= 0) { dots.forEach(function (d, k) { d.classList.toggle('is-active', k === i); }); }
      }
      B.setFrame(f); if (P) P.setFrame(f);
      return;
    }

    B.setFrame(0); if (P) P.setFrame(0);
    requestAnimationFrame(raf);
  }

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (ch) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[ch];
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { boot(0); });
  } else {
    boot(0);
  }
})();
