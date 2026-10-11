/* rigbutton.js — the Rive-style state machine for a rendered character beside a real button.
 * The character is a sprite sheet rendered in Blender (exoblend); this file only plays clips.
 *   idle    loops while nothing is happening
 *   hover   plays once on pointer-enter or focus, holds its last frame
 *   press   plays once on click; the button dips on the frame the claw lands (`hitFrame`)
 *   release plays once on pointer-leave or blur, then idle resumes
 * The button stays a real <button>: its text, its focus ring and its click are the browser's.
 * Reduced motion: the first idle frame, still, and nothing plays. */
(function () {
  'use strict';
  function RigButton(root, meta, opts) {
    var sprite = root.querySelector('.rig-sprite');
    var button = root.querySelector('button');
    var cw = meta.cell[0], ch = meta.cell[1], cols = meta.cols;
    var scale = opts.scale || 1, hitFrame = opts.hitFrame == null ? 5 : opts.hitFrame;
    var total = Object.keys(meta.clips).reduce(function (n, k) { return n + meta.clips[k][1]; }, 0);
    var rows = Math.ceil(total / cols);
    sprite.style.width = cw * scale + 'px';
    sprite.style.height = ch * scale + 'px';
    sprite.style.backgroundImage = 'url(' + opts.sheet + ')';
    sprite.style.backgroundSize = cols * cw * scale + 'px ' + rows * ch * scale + 'px';

    // stand the character on the button's floor line, `gap` px right of it; its claw then lands on the
    // button because the press pose was solved to reach one button-height up and left of the base
    function place() {
      var gap = opts.gap == null ? 6 : opts.gap;
      sprite.style.left = button.offsetLeft + button.offsetWidth + gap - meta.base.left * scale + 'px';
      sprite.style.top = button.offsetTop + button.offsetHeight - meta.base.bottom * scale + 'px';
    }
    place();
    window.addEventListener('resize', place);

    function show(i) {
      sprite.style.backgroundPosition = -(i % cols) * cw * scale + 'px ' + -Math.floor(i / cols) * ch * scale + 'px';
    }
    var state = 'idle', frame = 0, last = 0, held = false, hovering = false;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function go(next) { state = next; frame = 0; held = false; root.dataset.state = next; }
    function step() {
      var clip = meta.clips[state], first = clip[0], len = clip[1];
      if (state === 'idle') { show(first + (frame % len)); frame++; return; }
      if (frame < len) {
        show(first + frame);
        if (state === 'press' && frame === hitFrame) {
          button.classList.add('is-hit');
          setTimeout(function () { button.classList.remove('is-hit'); }, 160);
        }
        frame++;
        return;
      }
      if (state === 'press') return go(hovering ? 'hover-hold' : 'release');
      if (state === 'release') return go('idle');
      held = true; // hover: hold the last frame
    }
    meta.clips['hover-hold'] = [meta.clips.hover[0] + meta.clips.hover[1] - 1, 1];

    function loop(t) {
      if (t - last >= 1000 / meta.fps) { last = t; if (!held) step(); }
      requestAnimationFrame(loop);
    }
    if (reduce) { show(meta.clips.idle[0]); return; }

    function enter() { hovering = true; if (state === 'idle' || state === 'release') go('hover'); }
    function leave() { hovering = false; if (state !== 'press') go('release'); }
    button.addEventListener('pointerenter', enter);
    button.addEventListener('pointerleave', leave);
    button.addEventListener('focus', enter);
    button.addEventListener('blur', leave);
    button.addEventListener('click', function () { go('press'); });
    go('idle');
    requestAnimationFrame(loop);
  }
  window.RigButton = RigButton;
})();
