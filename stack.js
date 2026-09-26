/* stack.js — THE PINNED STACK on ai-transformation.html (RULE 02 §10).
 *
 * What I do → What you get → What it becomes → Who helps you: each `.pin` is position:sticky and the next
 * section slides up over it. A sticky top of the nav's height would pin a section TALLER
 * than the screen with its bottom off-screen, covering its last lines before anyone read
 * them. So each pin point is measured: min(nav height, viewport − section height) — it
 * pins at the top when it fits, and otherwise once its bottom edge reaches the bottom of
 * the screen. --nav-h also lets every sheet be at least a screen tall, so when the stack
 * ends the covered sections are already off screen.
 *
 * Degrades honestly: with JS off, --pin-top falls back to 0 and the page still reads top
 * to bottom — the sections scroll past each other with nothing lost.
 */
(function () {
  var pins = document.querySelectorAll('.pin-stack > .pin');
  if (!pins.length) return;
  var nav = document.querySelector('.nav-glass');
  function measure() {
    var navH = nav ? nav.offsetHeight : 0;
    document.documentElement.style.setProperty('--nav-h', navH + 'px');
    for (var i = 0; i < pins.length; i++) {
      pins[i].style.setProperty('--pin-top', Math.min(navH, window.innerHeight - pins[i].offsetHeight) + 'px');
    }
  }
  measure();
  window.addEventListener('resize', measure);
  window.addEventListener('load', measure);
  // a pinned section changes height when a reader opens one of its trees (<details>) —
  // re-measure then too, or it pins against its old height and covers what just opened
  if (window.ResizeObserver) {
    var ro = new ResizeObserver(measure);
    for (var j = 0; j < pins.length; j++) ro.observe(pins[j]);
  }
})();
