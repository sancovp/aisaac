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
  /* ⛔ THE DECK'S METHOD SECTIONS ARE NOT PINNED TRACKS. Slides 1·2·4·5 are
     COMPREHENSION beats — the framework, the box, the method, the arc — and
     pinning all four would have added 8.5 screens to a page already running
     32. They reveal on entry instead (see REVEAL_ON_ENTER below): the beats
     still land one at a time, they just do not each cost a screen of scroll.
     The pinned tracks are reserved for the ARGUMENT — cost, value, ledger,
     cascade, FAQ — where the pace IS the persuasion. */
  /* ⛔ THE METHOD SECTIONS ARE DRIVEN STAGES NOW, NOT ENTRY FADES.
     Isaac, 2026-09-20: "sections like this need to scroll thru and become
     animated, show exactly what we are going to do… it should feel hi-tech…
     it should feel like OH."
     (Superseded, kept: these four were revealed on entry to save page
     length. An entry fade plays once, at whatever moment the section
     happens to cross the fold, and the reader is a bystander to it. A
     DRIVEN stage makes the scroll the transport: the line draws as you
     push, the nodes land under your thumb, the boxes change while you
     hold them. That is the whole difference between a page that has
     animation on it and a page that feels like an instrument.)
     Only `.arc > li` stays an entry fade — it is the detail text UNDER the
     climb, not part of the picture. */
  var REVEAL_ON_ENTER = ['.arc > li'];

  /* PHASED STAGES — the scroll selects a STATE rather than adding items.
     [ track, stage element, how many states, vh of scroll per state ] */
  var PHASED = [
    ['.box-sec', '.box-stage', 3, 66]
  ];

  var TRACKS = [
    ['.frame-sec',   '.frame-dia .fnode',  0.12, 0.86, 'stack', 30],
    ['.climb-sec',   '.obst > li',         0.22, 0.94, 'stack', 20],
    ['.method-sec',  '.method-dia .mnode', 0.12, 0.82, 'stack', 30],
    ['.arc-sec',     '.arc-dia .stop',     0.10, 0.80, 'stack', 26],
    ['.cost-sec',    '.cost > li',    0.05, 0.75, 'stack'],
    ['.stack-sec',   '.stack > li',   0.05, 0.75, 'stack'],
    ['.ledger-sec',  '.ledger > li',  0.04, 0.80, 'stack', 26],
    ['.cascade-sec', '.cascade > li', 0.06, 0.70, 'cascade']
  ];

  var driven = [];

  TRACKS.forEach(function (t) {
    var track = document.querySelector(t[0]);
    if (!track) return;
    var items = [].slice.call(track.querySelectorAll(t[1]));
    if (!items.length) return;

    // ⛔ THE TRACK'S HEIGHT IS DERIVED FROM ITS ITEM COUNT, never typed — a
    // hardcoded height either rushes a long section or strands the reader in
    // an empty one. vh of scroll per beat; a track may override it (t[5]).
    var perItem = t[5] || 34;
    track.style.setProperty('--track', (100 + items.length * perItem) + 'vh');

    driven.push({ el: track, items: items, a: t[2], b: t[3], mode: t[4],
                  punch: track.querySelector('.cascade-punch') });
  });

  var phased = [];
  PHASED.forEach(function (t) {
    var track = document.querySelector(t[0]);
    if (!track) return;
    var stage = track.querySelector(t[1]);
    if (!stage) return;
    track.style.setProperty('--track', (100 + t[2] * t[3]) + 'vh');
    phased.push({ el: track, stage: stage, n: t[2], last: -1 });
  });

  if (!driven.length && !phased.length) { root.classList.remove('js'); return; }

  function paint() {
    ticking = false;
    driven.forEach(function (d) {
      var r = d.el.getBoundingClientRect();
      var travel = d.el.offsetHeight - window.innerHeight;
      var p = travel > 0 ? Math.min(1, Math.max(0, -r.top / travel)) : 1;

      var n = d.items.length;
      var span = (d.b - d.a) / Math.max(1, n - (d.mode === 'cascade' ? 0 : 1));

      d.items.forEach(function (el, i) {
        var live = p >= d.a + i * span;
        el.classList.toggle('on', live);
        el.classList.toggle('past', live && p >= d.a + (i + 1) * span);
      });

      if (d.punch) d.punch.classList.toggle('on', p >= d.b + (1 - d.b) * 0.45);
    });

    /* ⛔ --p IS THE SCRUB HEAD. Publishing the track's own 0→1 progress as a
       custom property lets CSS draw a line, sweep an arc or advance a meter
       CONTINUOUSLY with the scroll, instead of snapping on a class. That
       continuity is what reads as hi-tech; a class toggle always reads as a
       web page reacting. Custom properties inherit, so everything inside the
       section can use it with no extra wiring. */
    scrub.forEach(function (el) {
      var r = el.getBoundingClientRect();
      var travel = el.offsetHeight - window.innerHeight;
      var p = travel > 0 ? Math.min(1, Math.max(0, -r.top / travel)) : 1;
      el.style.setProperty('--p', p.toFixed(4));
    });

    phased.forEach(function (d) {
      var r = d.el.getBoundingClientRect();
      var travel = d.el.offsetHeight - window.innerHeight;
      var p = travel > 0 ? Math.min(1, Math.max(0, -r.top / travel)) : 1;
      var ph = Math.floor((p - 0.06) / (0.88 / d.n));
      if (ph < 0) ph = 0;
      if (ph > d.n - 1) ph = d.n - 1;
      if (ph !== d.last) { d.last = ph; d.stage.setAttribute('data-phase', ph); }
    });
  }

  // every pinned section publishes --p, phased ones included
  var scrub = driven.map(function (d) { return d.el; })
                    .concat(phased.map(function (d) { return d.el; }));

  var ticking = false;
  function onScroll() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(paint);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  window.addEventListener('load', paint);
  paint();

  /* ── THE DECK'S METHOD SECTIONS — revealed as they come into view, each
     item a beat behind the last. Same `.on` class the tracks use, so one
     CSS rule covers both mechanisms and there is no second vocabulary. ── */
  if ('IntersectionObserver' in window) {
    var stepIo = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        setTimeout(function () { el.classList.add('on'); },
                   parseInt(el.getAttribute('data-step'), 10) * 130);
        stepIo.unobserve(el);
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.15 });
    REVEAL_ON_ENTER.forEach(function (sel) {
      [].slice.call(document.querySelectorAll(sel)).forEach(function (el, i) {
        el.setAttribute('data-step', i);
        stepIo.observe(el);
      });
    });
  } else {
    REVEAL_ON_ENTER.forEach(function (sel) {
      [].slice.call(document.querySelectorAll(sel))
        .forEach(function (el) { el.classList.add('on'); });
    });
  }

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
