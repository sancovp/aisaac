/*!
 * aisaac explainer lab — scroll-scrub driver (v3, after a full read of the
 * scroll-world skill).
 *
 * Scroll mechanics adapted from oso95/scroll-world, references/scrub-engine.js
 * (MIT License, Copyright (c) 2026 cyw): segment scroll-range layout, the
 * smoothstep copy-opacity curves (first section greets on landing, last holds,
 * middle peaks mid-range), lingerEase (time settles mid-section exactly where
 * the copy peaks, quicker at the seams; f(0)=0, f(1)=1), the damped lerp
 * toward the scrub target, route rail + dots, top scrollbar, scroll hint,
 * width-gated mobile resize, prefers-reduced-motion. The <video>.currentTime
 * core of that engine is replaced by seekTo() on LIVE @remotion/player mounts
 * — there are no video files on this page; scroll drives the composition
 * clock. Scroll-world's seam/connector discipline is structurally unnecessary
 * here: the whole excerpt is ONE continuous composition.
 *
 * Two modes:
 *   SCRUB (default) — scroll position -> frame; silent.
 *   PLAY            — normal timed playback with the narration mp3 through
 *                     the composition's own <Audio>; scroll suspended; the
 *                     presenter and copy cards follow the player's
 *                     frameupdate events. Exiting play syncs scroll back to
 *                     the current frame.
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

  /**
   * scroll-world's lingerEase: monotone remap of a section's local progress so
   * time settles mid-section (where the copy peaks) and moves quicker at the
   * edges. L=0 linear, L=1 full mid pause; f(0)=0, f(1)=1 always.
   */
  var lingerEase = function (x, L) {
    L = clamp(L); var c = x - 0.5;
    return (1 - L) * x + L * (4 * c * c * c + 0.5);
  };

  /**
   * Scroll progress 0..1 -> composition frame (float), beat-aware: the linear
   * frame position is linger-remapped WITHIN the beat it falls in, so the
   * film dwells mid-sentence (where the copy peaks) and moves quicker at the
   * beat seams. Beat boundary frames are fixed points, so the map is
   * continuous and monotone; endpoints exact.
   */
  function frameForProgress(p, duration, beats) {
    p = clamp(p);
    var f = p * (duration - 1);
    if (!beats || !beats.length) return f;
    for (var i = 0; i < beats.length; i++) {
      var b = beats[i], end = b.start + b.frames;
      if (f >= b.start && f <= end) {
        var x = (f - b.start) / b.frames;
        return b.start + lingerEase(x, b.linger || 0) * b.frames;
      }
    }
    return f;
  }

  /** Inverse of frameForProgress (binary search — the map is monotone). */
  function progressForFrame(frame, duration, beats) {
    var lo = 0, hi = 1;
    for (var i = 0; i < 40; i++) {
      var mid = (lo + hi) / 2;
      if (frameForProgress(mid, duration, beats) < frame) lo = mid; else hi = mid;
    }
    return (lo + hi) / 2;
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
  function lerpStep(cur, target, k) { return cur + (target - cur) * k; }

  /** Local progress of beat {start, frames} at global float frame f. */
  function beatProgress(f, beat) { return (f - beat.start) / beat.frames; }

  var API = {
    clamp: clamp, smooth: smooth, lingerEase: lingerEase,
    frameForProgress: frameForProgress, progressForFrame: progressForFrame,
    copyOpacity: copyOpacity, lerpStep: lerpStep, beatProgress: beatProgress,
  };
  if (typeof module !== 'undefined' && module.exports) { module.exports = API; return; }

  // ---- browser mount --------------------------------------------------------
  var VH_PER_BEAT = 1.35;  // viewport-heights of scroll per sentence (diveScroll)
  var LERP_K = 0.16;       // damped scrub factor per rAF
  var LINGER = 0.35;       // per-beat dwell (scroll-world keeps <= 0.6)
  var LINGER_LAST = 0.5;   // the payoff sentence dwells longer
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var coarse = window.matchMedia('(hover: none) and (pointer: coarse)').matches;

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
    var scrollbar = document.getElementById('scrub-progress');
    var modeBtn = document.getElementById('mode-toggle');
    if (!world || !copylayer) return;

    var N = B.beats.length;
    var DUR = B.duration;
    var totalVh = VH_PER_BEAT * N;
    var beats = B.beats.map(function (b, i) {
      return { start: b.start, frames: b.frames, line: b.line, eyebrow: b.eyebrow,
               linger: i === N - 1 ? LINGER_LAST : LINGER };
    });

    // copy cards + route dots from the SAME beats the composition runs on
    var cards = [], dots = [];
    beats.forEach(function (b, i) {
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

    var vh = window.innerHeight, laidOutW = window.innerWidth;
    var worldTop = 0, scrollRange = 1;
    var target = 0, cur = 0, lastSent = -1, activeDot = -1, ticking = false;
    var mode = 'scrub';

    function layout() {
      vh = window.innerHeight;
      laidOutW = window.innerWidth;
      world.style.height = Math.round((totalVh + 1) * vh) + 'px';
      var r = world.getBoundingClientRect();
      worldTop = r.top + (window.scrollY || window.pageYOffset);
      scrollRange = totalVh * vh;
      if (mode === 'scrub') read();
    }

    function scrollForFrame(f) {
      return worldTop + progressForFrame(f, DUR, beats) * scrollRange;
    }

    function jumpTo(i) {
      if (mode === 'play') exitPlay();
      var b = beats[i];
      window.scrollTo({
        top: scrollForFrame(b.start + b.frames * 0.5),
        behavior: reduce ? 'auto' : 'smooth',
      });
    }

    /** Drive cards/dots/scrollbar from a float frame (used by both modes). */
    function paintFrame(f, scrollP) {
      var near = 0;
      for (var i = 0; i < N; i++) {
        var pr = beatProgress(f, beats[i]);
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
      if (scrollbar) scrollbar.style.transform = 'scaleX(' + clamp(scrollP) + ')';
    }

    function read() {
      var y = clamp((window.scrollY || window.pageYOffset) - worldTop, 0, scrollRange);
      var p = y / scrollRange;
      target = frameForProgress(p, DUR, beats);
      paintFrame(target, p);
      if (hint) hint.style.opacity = clamp(1 - y / (0.5 * vh));
      ticking = false;
    }

    function raf() {
      if (mode === 'scrub') {
        cur = reduce ? target : lerpStep(cur, target, LERP_K);
        var f = Math.round(cur);
        if (f !== lastSent) {
          lastSent = f;
          B.setFrame(f);
          if (P) P.setFrame(f);
        }
      }
      requestAnimationFrame(raf);
    }

    // ---- PLAY mode: timed playback with narration --------------------------
    function enterPlay() {
      mode = 'play';
      if (modeBtn) { modeBtn.textContent = '↕ back to scroll'; modeBtn.classList.add('is-playing'); }
      if (hint) hint.style.opacity = 0;
      B.play();
    }
    function exitPlay(atFrame) {
      var f = atFrame != null ? atFrame : cur;
      B.pause();
      mode = 'scrub';
      if (modeBtn) { modeBtn.textContent = '▶ play with narration'; modeBtn.classList.remove('is-playing'); }
      cur = target = f;
      lastSent = -1; // force a re-send so both players land exactly on f
      window.scrollTo(0, scrollForFrame(f));
      read();
      B.setFrame(Math.round(f)); if (P) P.setFrame(Math.round(f));
      lastSent = Math.round(f);
    }
    if (modeBtn) {
      modeBtn.addEventListener('click', function () {
        if (mode === 'scrub') enterPlay(); else exitPlay();
      });
    }
    B.on('frameupdate', function (f) {
      if (mode !== 'play') return;
      cur = f;
      if (P) P.setFrame(f);
      paintFrame(f, progressForFrame(f, DUR, beats));
    });
    B.on('ended', function () { if (mode === 'play') exitPlay(DUR - 1); });

    window.addEventListener('scroll', function () {
      if (mode !== 'scrub') return;
      if (!ticking) { ticking = true; requestAnimationFrame(read); }
    }, { passive: true });
    // scroll-world: on touch, the URL bar fires height-only resizes — relaying
    // out there would rebuild the track and yank the scroll. Gate on width.
    window.addEventListener('resize', function () {
      if (coarse && window.innerWidth === laidOutW) return;
      layout();
    });
    window.addEventListener('orientationchange', layout);

    layout();

    // dev/screenshot hook: ?p=0.42 previews the page STATE at 42% scrub
    // progress without scrolling — frame + copy cards are set directly, once,
    // and the rAF loop never starts, so a headless screenshot is deterministic
    // (old-headless screenshot passes don't honor position:sticky, so a real
    // scroll would show the empty track). Production path: no param.
    var q = new URLSearchParams(location.search);
    var pq = Number(q.get('p'));
    if (Number.isFinite(pq) && pq > 0) {
      cur = target = frameForProgress(clamp(pq), DUR, beats);
      var pf = Math.round(cur);
      paintFrame(pf, clamp(pq));
      if (hint) hint.style.opacity = 0;
      B.setFrame(pf); if (P) P.setFrame(pf);
      return;
    }

    // deep link: ?f=623 opens scrolled to that frame's scroll position.
    var fq = Number(q.get('f'));
    if (Number.isFinite(fq) && fq > 0) {
      fq = clamp(fq, 0, DUR - 1);
      window.scrollTo(0, scrollForFrame(fq));
      cur = target = fq;
      read();
    }

    B.setFrame(Math.round(cur)); if (P) P.setFrame(Math.round(cur));
    lastSent = Math.round(cur);
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
