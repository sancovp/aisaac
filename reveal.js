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
  var REVEAL_ON_ENTER = [
    '.frame-dia .fnode',   // the rail's five stops
    '.boxes > li',         // the three states of the same four boxes
    '.method-dia .mnode',  // the loop's five nodes
    '.arc-dia .stop',      // the climb's seven stages
    '.arc > li'            // the detail blocks under the climb
  ];

  var TRACKS = [
    ['.cost-sec',    '.cost > li',    0.05, 0.75, 'stack'],
    ['.stack-sec',   '.stack > li',   0.05, 0.75, 'stack'],
    ['.ledger-sec',  '.ledger > li',  0.04, 0.80, 'stack', 26],
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
    // vh of scroll per beat — a track may override it (t[5]); the ledger runs
    // eight beats and would otherwise be the longest section on the page.
    var perItem = t[5] || (t[4] === 'solo' ? 62 : 34);
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
    /* ⛔ SOLO IS A DECK, NOT A LIST.  Isaac, 2026-09-20: "needs to go ONE AT A
       TIME and become the thing on the screen."  A reel that slid twenty
       summaries past a window still showed nine of them, and nine competing
       questions is a list being skimmed — the reader picks what to attend to,
       which is the opposite of controlling what they believe. Every question
       is now stacked in the SAME PLACE and only the live one is rendered, at
       display size, so the current question IS the screen. Built here rather
       than in the HTML so no-JS still gets a plain, complete, readable FAQ. */
    var reel = null, count = null, bar = null;
    if (t[4] === 'solo') {
      var box = items[0].parentNode;
      reel = document.createElement('div');
      reel.className = 'faq-reel';
      while (box.firstChild) reel.appendChild(box.firstChild);
      box.appendChild(reel);

      /* the counter is the WALK made visible: it says how many are left, so
         the reader knows the section ends and keeps going to find out. */
      count = document.createElement('p');
      count.className = 'faq-count';
      count.innerHTML = '<b>01</b><span>/ ' + items.length + '</span>' +
                        '<span class="faq-bar"><i></i></span>';
      box.parentNode.insertBefore(count, box);
      bar = count.querySelector('.faq-bar i');

      /* a click cannot help here and CAN strand the reader on a blank stage:
         toggling `open` off would hide the only visible card until the next
         scroll frame repaints it. The scroll position is the only control. */
      box.addEventListener('click', function (e) {
        if (e.target.closest('summary')) e.preventDefault();
      });
    }

    driven.push({ el: track, items: items, a: t[2], b: t[3], mode: t[4],
                  reel: reel, box: reel && reel.parentNode, last: -1,
                  count: count && count.querySelector('b'), bar: bar,
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
          /* ⛔ THE FIRST QUESTION IS OPEN ON ARRIVAL. With `live` gated on
             `p >= a`, the opening screen of the FAQ showed twenty dim
             summaries, nothing open and a 380px hole — the single worst
             screen on the page, and it was the one that introduced a
             thirteen-screen section. Item 0 is current from the top of the
             track; the walk starts already underway. */
          var isCurrent = i === 0
            ? (p < d.a + span)
            : (live && (i === n - 1 || p < next));
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
      /* ⛔ THE DECK NEEDS A HEIGHT, because every card is absolutely
         positioned and an absolute child cannot size its parent. Measured
         from the TALLEST card with its answer open, so no card is ever
         clipped and the stage never jumps between beats. */
      if (d.reel && remeasure) {
        var tallest = 0;
        d.items.forEach(function (el) {
          var was = el.open;
          el.open = true;
          if (el.scrollHeight > tallest) tallest = el.scrollHeight;
          el.open = was;
        });
        d.reel.style.setProperty('--faq-h', Math.ceil(tallest) + 'px');
      }

      if (d.reel && cur !== d.last) {
        d.last = cur;
        var n1 = (cur < 0 ? 0 : cur) + 1;
        if (d.count) d.count.textContent = n1 < 10 ? '0' + n1 : String(n1);
        if (d.bar) d.bar.style.width = (n1 / d.items.length * 100) + '%';
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
