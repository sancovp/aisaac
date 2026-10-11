/* arm.js — THE ARM PRESS (RULE 02 §8b): a robot arm hidden behind the hero's Book a call. Nothing shows until
 * the button is clicked; then it comes up from behind, reaches over the top, presses the button, and drops back
 * out of sight. The booking form opens on the frame it presses: this script holds the click, plays the arm, then
 * re-sends the click, which capture.js answers as it always does. The button stays a real <button>.
 * The arm is two sprite sheets cut from one Blender render (docs/arm-press/): `back` (the whole arm) under the
 * button, `front` (forearm, head, claws) over it on the frames where the claw is in front of its face; both are
 * clipped at the button's bottom edge. `data-arm-press="down"` mirrors it top to bottom — for a button with no room
 * above it (the top bar's): the arm comes down from behind, pops out of the button's bottom edge and curls up to
 * press its face, clipped at the button's top edge. Reduced motion: no arm; the click goes straight through. */
(function () {
  'use strict';
  var META = {"cell":[264,270],"cols":12,"fps":24,"clips":{"strike":[0,24]},"front":[8,9,10,11,12,13,14,15,16,17,18],"button":{"top":193.9,"bottom":270.2,"left":2.6,"right":261.4}};
  var HIT = 12;   // the frame the claw lands
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  document.querySelectorAll('[data-arm-press]').forEach(function (wrap) {
    // a <button> (Book a call: capture.js answers the replayed click) or an <a> (Get JobWorld: the replayed click follows its href)
    var button = wrap.querySelector('button, a'), down = wrap.getAttribute('data-arm-press') === 'down';
    var back = document.createElement('span'), front = document.createElement('span');
    var clipB = document.createElement('span'), clipF = document.createElement('span');
    clipB.className = 'arm-clip'; clipF.className = 'arm-clip arm-clip-front';
    back.className = 'arm-sprite'; front.className = 'arm-sprite';
    clipB.setAttribute('aria-hidden', 'true'); clipF.setAttribute('aria-hidden', 'true');
    clipB.appendChild(back); clipF.appendChild(front);
    wrap.insertBefore(clipB, button); wrap.appendChild(clipF);

    var cw = META.cell[0], ch = META.cell[1], cols = META.cols, clip = META.clips.strike;
    var rows = Math.ceil(clip[1] / cols), s = 1, frontSet = {};
    META.front.forEach(function (i) { frontSet[i] = true; });
    back.style.backgroundImage = 'url(assets/arm-press-back.webp)';
    front.style.backgroundImage = 'url(assets/arm-press-front.webp)';

    function place() {
      var b = META.button; s = button.offsetHeight / (b.bottom - b.top);
      var left = button.offsetLeft + button.offsetWidth / 2 - (b.left + b.right) / 2 * s;
      var top = down ? button.offsetTop : button.offsetTop + button.offsetHeight - ch * s;
      [clipB, clipF].forEach(function (c) {
        c.style.left = left + 'px'; c.style.top = top + 'px';
        c.style.transform = down ? 'scaleY(-1)' : '';
        c.style.width = cw * s + 'px'; c.style.height = ch * s + 'px';
      });
      [back, front].forEach(function (el) {
        el.style.width = cw * s + 'px'; el.style.height = ch * s + 'px';
        el.style.backgroundSize = cols * cw * s + 'px ' + rows * ch * s + 'px';
      });
    }
    function show(i) {
      var on = i >= 0, pos = on ? -(i % cols) * cw * s + 'px ' + -Math.floor(i / cols) * ch * s + 'px' : '0 0';
      back.style.opacity = on ? 1 : 0;
      front.style.opacity = on && frontSet[i] ? 1 : 0;
      back.style.backgroundPosition = front.style.backgroundPosition = pos;
    }

    var playing = false, passing = false, frame = 0, last = 0;
    function tick(t) {
      if (!playing) return;
      if (t - last >= 1000 / META.fps) {
        last = t;
        if (frame >= clip[1]) { playing = false; show(-1); return; }
        show(clip[0] + frame);
        if (frame === HIT) {
          button.classList.add('is-pressed');
          setTimeout(function () { button.classList.remove('is-pressed'); }, 170);
          passing = true; button.click(); passing = false;   // capture.js opens the booking form now, or the link is followed
        }
        frame++;
      }
      requestAnimationFrame(tick);
    }
    // capture phase on the button: it runs before capture.js's page-wide listener sees the click
    button.addEventListener('click', function (e) {
      if (passing) return;
      e.preventDefault(); e.stopImmediatePropagation();
      if (playing) return;
      playing = true; frame = 0; last = 0; requestAnimationFrame(tick);
    }, true);

    place(); show(-1);
    window.addEventListener('resize', place);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(place);
  });
})();
