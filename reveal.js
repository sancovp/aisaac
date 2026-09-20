/* reveal.js — THE PROGRESSIVE REVEAL.
 *
 * Isaac, 2026-09-20: "Use scroll effects to make sure that the intended value
 * stack happens. Animate it. Its so simple dude. Make the experience."
 *
 * The deck this page is built from is called Progressive Reveal, and slides
 * 8→13 exist because each rung of the cascade ARRIVES ON ITS OWN. A page that
 * prints $38,000 / $19,000 / $9,000 all at once has kept the text and thrown
 * away the mechanism. This gives the rungs back their arrival.
 *
 * ⛔ IT DEGRADES OPEN. The CSS that hides a `.reveal` is scoped to `html.js`,
 * and this file is what adds `js`. No script, no IntersectionObserver, a
 * thrown error before line 1 finishes → nothing is ever hidden and the page
 * renders complete. A reveal that hides content when its own script fails is
 * a page that ships blank, which is the worst failure available here.
 *
 * ⛔ IT NEVER TOUCHES THE SCROLL. No scroll-jacking, no pinning, no hijacked
 * wheel. The page scrolls exactly as the browser intends; this only decides
 * when a thing has arrived.
 *
 * ⛔ ONCE ONLY. Each element unobserves after it fires — re-animating on every
 * scroll past is the cheap-template tell, and it makes the cascade feel like a
 * toy rather than a reveal.
 */
(function () {
  'use strict';

  var root = document.documentElement;

  // Bail BEFORE marking `js` if the browser cannot observe — that way the
  // hiding CSS never applies and everything renders normally.
  if (!('IntersectionObserver' in window)) return;

  root.classList.add('js');

  // GROUPS: [selector for the container, selector for the items, ms between]
  // The stagger is per-GROUP so a row's delay is its index in its own list;
  // nothing depends on a hardcoded nth-child ladder that breaks when a row
  // is added or removed.
  var GROUPS = [
    // ⛔ THE CASCADE IS NOT HERE. It is SCROLL-DRIVEN below, not triggered.
    ['.cost',    'li', 140],  // the five costs, then the total lands last
    ['.stack',   'li', 110],  // the six things they end up holding
    ['.doors',   'li', 160]
  ];

  var items = [];

  GROUPS.forEach(function (g) {
    var host = document.querySelector(g[0]);
    if (!host) return;
    var kids = host.querySelectorAll(g[1]);
    Array.prototype.forEach.call(kids, function (el, i) {
      el.classList.add('reveal');
      el.style.setProperty('--d', (i * g[2]) + 'ms');
      items.push(el);
    });
  });

  if (!items.length) { root.classList.remove('js'); return; }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('in');
      io.unobserve(e.target);          // once only
    });
  }, {
    // fire a little before the element's top edge reaches the fold, so the
    // row is already arriving as it comes into view rather than after
    rootMargin: '0px 0px -12% 0px',
    threshold: 0.15
  });

  items.forEach(function (el) { io.observe(el); });

  // ⛔ ANYTHING ALREADY ON SCREEN AT LOAD MUST NOT WAIT FOR A SCROLL.
  // A visitor who lands deep-linked, or on a short viewport where two sections
  // are visible at once, would otherwise sit looking at invisible rows until
  // they happened to scroll. IntersectionObserver does fire for already-
  // intersecting targets on observe, but this is the belt for the case where
  // layout settles late (web fonts, the poster image) and the first callback
  // measured a pre-layout position.
  window.addEventListener('load', function () {
    items.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) {
        el.classList.add('in');
        io.unobserve(el);
      }
    });
  });

  /* ══════════════════════════════════════════════════════════════════════
     THE CASCADE — SCROLL-DRIVEN. Isaac: "force the experience exactly.
     control. CONTROL."

     ⛔ NOT A TRIGGER AND NOT A TIMER. The rungs above fire once on entry and
     then play themselves; a visitor scrolling fast sees none of them land.
     Here the section is a tall TRACK and the stage inside it is sticky, so
     scroll POSITION through the track selects how many rungs have arrived.
     The viewer still drives — we never intercept the wheel, never pin them
     against their input, never animate the scroll. They simply cannot reach
     the price without passing the three numbers it is measured against.

     ⛔ THE SUPERSEDED RUNGS DIM (`.past`). Without it three lit numbers read
     as a price LIST; with it they read as a DESCENT, which is the argument.
     ══════════════════════════════════════════════════════════════════════ */
  var track = document.querySelector('.cascade-sec');
  var rungs = track ? [].slice.call(track.querySelectorAll('.cascade > li')) : [];
  var punch = track ? track.querySelector('.cascade-punch') : null;

  if (track && rungs.length) {
    // where in the track each beat lands. Tuned so the first rung is already
    // there as the stage settles, and the punch line is the last thing that
    // happens before the track releases into the doors.
    var BEATS = [0.06, 0.34, 0.60, 0.82];   // rung1 · rung2 · rung3 · punch
    var ticking = false;

    function paint() {
      ticking = false;
      var r = track.getBoundingClientRect();
      var travel = track.offsetHeight - window.innerHeight;
      if (travel <= 0) {                 // track shorter than the viewport —
        rungs.forEach(function (el) { el.classList.add('on'); });
        if (punch) punch.classList.add('on');
        return;
      }
      var p = Math.min(1, Math.max(0, -r.top / travel));

      rungs.forEach(function (el, i) {
        var live = p >= BEATS[i];
        el.classList.toggle('on', live);
        // dim once the NEXT rung has arrived — superseded, not gone
        el.classList.toggle('past', live && p >= BEATS[i + 1]);
      });
      if (punch) punch.classList.toggle('on', p >= BEATS[3]);
    }

    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(paint);
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    window.addEventListener('load', paint);
    paint();
  }
})();
