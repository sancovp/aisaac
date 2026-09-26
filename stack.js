/* stack.js — THE PINNED PAIR on ai-transformation.html (RULE 02).
 *
 * "What I do" is position:sticky; "What you get" slides up over it. A sticky top of the
 * nav's height would pin a section TALLER than the screen with its bottom off-screen,
 * and the levels list would be covered before anyone read it. So the pin point is
 * measured: min(nav height, viewport − section height) — it pins at the top when it
 * fits, and otherwise at the moment its bottom edge reaches the bottom of the screen.
 * --nav-h also lets "What you get" be at least a screen tall, so when the pin releases
 * the covered section is already off screen.
 *
 * Degrades honestly: with JS off, --pin-top falls back to 0 and the page still reads
 * top to bottom — the sections just scroll normally past each other.
 */
(function () {
  var sec = document.querySelector('.what-sec');
  if (!sec) return;
  var nav = document.querySelector('.nav-glass');
  var root = document.documentElement;
  function measure() {
    var navH = nav ? nav.offsetHeight : 0;
    root.style.setProperty('--nav-h', navH + 'px');
    root.style.setProperty('--pin-top', Math.min(navH, window.innerHeight - sec.offsetHeight) + 'px');
  }
  measure();
  window.addEventListener('resize', measure);
  window.addEventListener('load', measure);
})();
