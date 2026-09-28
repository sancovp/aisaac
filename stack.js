/* stack.js — THE PINNED STACK on ai-transformation.html (RULE 02 §10).
 *
 * What I do → What you get → What it becomes → Who helps you. THE HOLD IS WHILE YOU READ, never
 * after: each `.pin` sticks under the nav the moment its top reaches it, and from then the
 * reader's scroll moves its content at 1/SLOW speed until its last line is on screen — so a
 * section cannot be flicked past. The next sheet is timed to arrive exactly then (its top margin
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
      run.el.style.transform = shift ? 'translateY(' + (-shift) + 'px)' : '';
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

/* THE LEAK TREES OPEN ON HOVER (*USER*'s ruling) — with a mouse only (a touch screen keeps the tap):
   pointing at a row opens its tree, leaving closes a tree hover opened; a click PINS it open (and a
   second click closes it, the native toggle). A tree that was already open is never closed by hover. */
(function () {
  if (!window.matchMedia || !window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  document.querySelectorAll('details.leak').forEach(function (d) {
    d.addEventListener('mouseenter', function () {
      if (!d.open) { d.open = true; d.dataset.hoverOpen = '1'; }
    });
    d.addEventListener('mouseleave', function () {
      if (d.dataset.hoverOpen) { d.open = false; delete d.dataset.hoverOpen; }
    });
    var s = d.querySelector('summary');
    if (s) s.addEventListener('click', function (e) {
      if (d.dataset.hoverOpen) { e.preventDefault(); delete d.dataset.hoverOpen; }
    });
  });
})();
