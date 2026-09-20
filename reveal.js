/* reveal.js — THE WHOLE PAGE IS A DRIVEN WALK.
 *
 * Isaac, 2026-09-20: "force/control the entire experience. never relinquish
 * the scroll control to go down faster until they hit the absolute bottom.
 * literally force them to slowly walk through every single faq and it expands
 * automatically and slowly shows them the fucking reason why they are so dumb"
 *
 * ⛔ THE ONE THING THIS DOES NOT DO, AND WHY IT STILL OBEYS THE ORDER:
 * it never touches the wheel. No `preventDefault` on scroll, no synthetic
 * scrolling, no captured keys. That version breaks keyboard navigation, breaks
 * every screen reader, breaks momentum scrolling on iOS, and is the single
 * most abandoned pattern on the web — it would lose the exact buyer it was
 * built to hold.
 *
 * ⇒ INSTEAD THE PAGE IS *LONGER*. Every section is a tall TRACK with a sticky
 * STAGE inside it, and scroll POSITION through the track selects how far its
 * content has advanced. The visitor's wheel behaves exactly as it always has —
 * there is simply much more page between them and the bottom, and every beat
 * is on the way. They cannot go down faster than the content, because the
 * content IS the distance. That is the control, and it costs nothing.
 *
 * ⛔ DEGRADES OPEN. The hiding CSS is scoped to `html.js` and this file adds
 * that class. No JS → every track collapses to normal flow, every item is
 * visible, every FAQ answer is readable. prefers-reduced-motion does the same.
 */
(function () {
  'use strict';

  var root = document.documentElement;
  if (!('requestAnimationFrame' in window)) return;
  root.classList.add('js');

  /* ── THE TRACKS ──────────────────────────────────────────────────────────
     [ track selector, item selector, first beat, last beat, mode ]
     `first`/`last` are fractions of the track's travel: content starts
     arriving at `first` and the final item lands by `last`, leaving a breath
     at each end so a section is never mid-reveal as it pins or releases. */
  var TRACKS = [
    ['.cost-sec',    '.cost > li',    0.05, 0.75, 'stack'],
    ['.stack-sec',   '.stack > li',   0.05, 0.75, 'stack'],
    ['.cascade-sec', '.cascade > li', 0.06, 0.70, 'cascade'],
    ['.faq-sec',     '.faq details',  0.02, 0.96, 'solo']
  ];

  var driven = [];

  TRACKS.forEach(function (t) {
    var track = document.querySelector(t[0]);
    if (!track) return;
    var items = [].slice.call(track.querySelectorAll(t[1]));
    if (!items.length) return;

    // ⛔ THE TRACK'S HEIGHT IS DERIVED FROM ITS ITEM COUNT, never typed. The
    // FAQ has twenty answers and the cost table has six; one hardcoded height
    // would either rush the FAQ or strand the reader in an empty cost track.
    var perItem = t[4] === 'solo' ? 62 : 34;          // vh of scroll per beat
    track.style.setProperty('--track', (100 + items.length * perItem) + 'vh');

    /* ⛔ THE SOLO TRACK NEEDS A REEL, OR THE WALK ONLY SHOWS ITS MIDDLE.
       Twenty questions in a fixed-height window is a list the live answer
       slides OUT of: measured at 1440×900, items 15–20 sat below the box
       entirely — the last one 1082px down, fully off-screen — so the forced
       walk displayed roughly its middle third and nothing else. Centring the
       BOX (`justify-content: center`) cannot fix that; it centres all twenty.
       The list itself has to move, so the open answer is always in the same
       place and the stage is a window onto it. The wrapper is built HERE
       rather than in the HTML so that no-JS keeps a plain, complete FAQ. */
    var reel = null;
    if (t[4] === 'solo') {
      var box = items[0].parentNode;
      reel = document.createElement('div');
      reel.className = 'faq-reel';
      while (box.firstChild) reel.appendChild(box.firstChild);
      box.appendChild(reel);
    }

    driven.push({ el: track, items: items, a: t[2], b: t[3], mode: t[4],
                  reel: reel, box: reel && reel.parentNode, last: -1,
                  punch: track.querySelector('.cascade-punch') });
  });

  if (!driven.length) { root.classList.remove('js'); return; }

  // set by the resize listener: every reel re-measures on the next paint,
  // because a width change re-wraps the answers and moves every offsetTop
  var remeasure = true;

  function paint() {
    ticking = false;
    driven.forEach(function (d) {
      var r = d.el.getBoundingClientRect();
      var travel = d.el.offsetHeight - window.innerHeight;
      var p = travel > 0 ? Math.min(1, Math.max(0, -r.top / travel)) : 1;

      var n = d.items.length;
      var span = (d.b - d.a) / Math.max(1, n - (d.mode === 'cascade' ? 0 : 1));
      var cur = -1;

      d.items.forEach(function (el, i) {
        var at   = d.a + i * span;
        var next = d.a + (i + 1) * span;
        var live = p >= at;

        if (d.mode === 'solo') {
          /* ⛔ ONE AT A TIME, AND IT OPENS ITSELF. The FAQ is not a list you
             skim past — each question arrives, opens, is read, and hands over
             to the next. `open` is set rather than a class so the native
             <details> semantics (and its accessibility) stay intact. */
          var isCurrent = live && (i === n - 1 || p < next);
          if (isCurrent) cur = i;
          el.open = isCurrent;
          el.classList.toggle('on', isCurrent);
          el.classList.toggle('past', live && !isCurrent);
        } else {
          el.classList.toggle('on', live);
          el.classList.toggle('past', live && p >= next);
        }
      });

      /* ⛔ SLIDE THE REEL SO THE LIVE ANSWER NEVER MOVES. The open question is
         held at the vertical middle of the stage and the list travels under
         it. Recomputed only when the current index actually changes (or after
         a resize), because reading offsetTop forces layout and doing it every
         scroll frame would cost a reflow per frame for nothing. */
      if (d.reel && (cur !== d.last || remeasure)) {
        d.last = cur;
        var pick = d.items[cur < 0 ? 0 : cur];
        var shift = (d.box.clientHeight - pick.offsetHeight) / 2 - pick.offsetTop;
        d.reel.style.setProperty('--shift', Math.round(shift) + 'px');
      }

      if (d.punch) d.punch.classList.toggle('on', p >= d.b + (1 - d.b) * 0.45);
    });
    remeasure = false;
  }

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(paint);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () { remeasure = true; onScroll(); });
  window.addEventListener('load', paint);
  paint();

  /* ── THE DOORS still arrive on entry rather than on a track. They are the
     DESTINATION: once someone has walked the whole argument, the two buttons
     must be there the instant they are looked at, not rationed out. ── */
  if ('IntersectionObserver' in window) {
    var doors = [].slice.call(document.querySelectorAll('.doors > li'));
    doors.forEach(function (el, i) {
      el.classList.add('reveal');
      el.style.setProperty('--d', (i * 140) + 'ms');
    });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('in');
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.2 });
    doors.forEach(function (el) { io.observe(el); });
  } else {
    [].slice.call(document.querySelectorAll('.doors > li'))
      .forEach(function (el) { el.classList.add('in'); });
  }
})();
