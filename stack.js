/* stack.js — THE PINNED STACK on ai-transformation.html (RULE 02 §10).
 *
 * What I do → What you get → What it becomes → Who helps you. THE HOLD IS WHILE YOU READ, never
 * after: each `.pin` sticks under the nav the moment its top reaches it, and from then the
 * reader's scroll moves its content at 1/SLOW speed until its last line is on screen — so a
 * section cannot be flicked past. The slow read moves the STICKY POINT itself (--pin-top rises
 * from the nav to nav − overflow), never a transform: the browser releases a sticky section by
 * its real box, so a transformed one was released while the sheet meant to cover it was still
 * below it, and the section under it showed through the gap. The next sheet is timed to arrive exactly then (its top margin
 * is the extra scroll the slowdown costs), so it slides up over a section that has just been
 * read, and nothing ever sits frozen waiting to be covered. A section that fits the screen has
 * nothing to slow; the next sheet simply slides over it. --nav-h also lets every sheet be at
 * least a screen tall, so when the stack ends the covered sections are already off screen.
 *
 * Degrades honestly: the stack goes live (`.is-live`, which is what makes the pins sticky) only
 * when this runs, so with JS off the sections simply scroll top to bottom, nothing covered.
 */
(function () {
  var stack = document.querySelector('.pin-stack');
  if (!stack) return;
  var kids = stack.children;
  var nav = document.querySelector('.nav-glass');
  var SLOW = 2;            // px of scroll per px of reading travel, while a section is being read
  var runs = [], navH = 0, queued = false;

  function measure() {
    navH = nav ? nav.offsetHeight : 0;
    document.documentElement.style.setProperty('--nav-h', navH + 'px');
    var room = window.innerHeight - navH;
    runs = [];
    for (var i = 0; i < kids.length; i++) {
      var el = kids[i];
      if (!el.classList.contains('pin')) continue;
      el.style.setProperty('--pin-top', navH + 'px');
      var over = Math.max(0, el.offsetHeight - room);   // what is below the fold when it pins
      if (el.nextElementSibling) el.nextElementSibling.style.marginTop = ((SLOW - 1) * over) + 'px';
      runs.push({ el: el, over: over });
    }
    // flow tops, from the (unpinned) stack down — a sticky element's own offsets move with it
    var top = stack.getBoundingClientRect().top + window.scrollY, r = 0;
    for (var k = 0; k < kids.length; k++) {
      top += parseFloat(getComputedStyle(kids[k]).marginTop) || 0;
      if (runs[r] && runs[r].el === kids[k]) { runs[r].top = top; r++; }
      top += kids[k].offsetHeight;
    }
    update();
  }
  function update() {
    queued = false;
    for (var i = 0; i < runs.length; i++) {
      var run = runs[i];
      var s = window.scrollY - (run.top - navH);         // scroll since it pinned
      var shift = Math.min(run.over, Math.max(0, s / SLOW));
      run.el.style.setProperty('--pin-top', (navH - shift) + 'px');
    }
  }
  stack.classList.add('is-live');
  measure();
  window.addEventListener('scroll', function () {
    if (!queued) { queued = true; requestAnimationFrame(update); }
  }, { passive: true });
  window.addEventListener('resize', measure);
  window.addEventListener('load', measure);
  // a pinned section changes height when a reader opens one of its trees (<details>) —
  // re-measure then too, or its slowed read ends before what just opened is on screen
  if (window.ResizeObserver) {
    var ro = new ResizeObserver(measure);
    for (var j = 0; j < runs.length; j++) ro.observe(runs[j].el);
  }
})();

/* THE LEAK TREES OPEN ON HOVER (*USER*'s ruling) — with a mouse only (a touch screen keeps the tap), and
   UNHURRIED: a tree opens only when the pointer RESTS on its row (OPEN_AFTER), so a cursor passing over
   the list opens nothing, and it closes a moment after the pointer leaves (CLOSE_AFTER), so a pass
   through the gap between rows does not snap it shut. Every open grows (the height, GROW ms, eased),
   whether hover or click opened it; a hover close shrinks. A click PINS a hover-opened tree open (a
   second click closes it, the native toggle). A tree that was already open is never closed by hover.
   Reduced motion: no growing, the delays stay. */
(function () {
  var OPEN_AFTER = 260, CLOSE_AFTER = 320, GROW = 360;
  var moves = !(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  function tree(d) { return d.querySelector('.leak-tree'); }
  function frames(t, from) {
    var h = t.offsetHeight, mb = getComputedStyle(t).marginBottom;
    var shut = { height: '0px', marginBottom: '0px', opacity: 0, overflow: 'hidden' };
    var full = { height: h + 'px', marginBottom: mb, opacity: 1, overflow: 'hidden' };
    return from === 'shut' ? [shut, full] : [full, shut];
  }
  document.querySelectorAll('details.leak').forEach(function (d) {
    d.addEventListener('toggle', function () {
      var t = tree(d);
      if (d.open && moves && t && t.animate && !d.dataset.shrinking) {
        t.animate(frames(t, 'shut'), { duration: GROW, easing: 'cubic-bezier(.2,.7,.2,1)' });
      }
    });
  });
  if (!window.matchMedia || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  document.querySelectorAll('details.leak').forEach(function (d) {
    var openT, closeT;
    d.addEventListener('mouseenter', function () {
      clearTimeout(closeT);
      if (d.open) return;
      openT = setTimeout(function () { if (!d.open) { d.dataset.hoverOpen = '1'; d.open = true; } }, OPEN_AFTER);
    });
    d.addEventListener('mouseleave', function () {
      clearTimeout(openT);
      if (!d.dataset.hoverOpen) return;
      closeT = setTimeout(function () {
        if (!d.dataset.hoverOpen) return;
        delete d.dataset.hoverOpen;
        var t = tree(d);
        if (!moves || !t || !t.animate) { d.open = false; return; }
        d.dataset.shrinking = '1';
        t.animate(frames(t, 'full'), { duration: GROW * 0.75, easing: 'ease-in' }).onfinish = function () {
          d.open = false; delete d.dataset.shrinking;
        };
      }, CLOSE_AFTER);
    });
    var s = d.querySelector('summary');
    if (s) s.addEventListener('click', function (e) {
      clearTimeout(openT);
      if (d.dataset.hoverOpen) { e.preventDefault(); delete d.dataset.hoverOpen; }
    });
  });
})();

/* THE SCROLL SPEED HAS A CEILING on the landing page (*USER*'s ruling): a wheel or trackpad can move the
   page at most MAX px a second, so nobody can fling past the pinned stack's reading. Below the ceiling it
   is the reader's own scroll, a frame later; above it the travel is spread out, and at most ~0.6 s of it
   is ever banked, so the page never coasts on after the hand stops. A reversal takes effect at once.
   Touch keeps the phone's own scrolling; a pinch-zoom, a sideways scroll and an open dialog are untouched. */
(function () {
  if (!document.querySelector('.pin-stack')) return;
  var MAX = 2200, BANK = MAX * 0.6;
  var pending = 0, last = 0, running = false;
  function tick(now) {
    var dt = last ? Math.min(50, now - last) : 16;
    last = now;
    var cap = MAX * dt / 1000;
    var step = Math.max(-cap, Math.min(cap, pending));
    pending -= step;
    window.scrollBy({ top: step, behavior: 'instant' });
    if (Math.abs(pending) > 0.5) requestAnimationFrame(tick);
    else { pending = 0; last = 0; running = false; }
  }
  window.addEventListener('wheel', function (e) {
    if (e.ctrlKey || e.defaultPrevented || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
    if (e.target.closest && e.target.closest('dialog')) return;
    var d = e.deltaY * (e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? window.innerHeight : 1);
    e.preventDefault();
    if (pending && (d > 0) !== (pending > 0)) pending = 0;
    pending = Math.max(-BANK, Math.min(BANK, pending + d));
    if (!running) { running = true; requestAnimationFrame(tick); }
  }, { passive: false });
})();
