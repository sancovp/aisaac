/* lasso.js — click the button: a door opens in its right end, a gnome walks out, hops down, spins a
 * lasso, throws it off-screen, and hauls the REAL booking form in on the rope, then tips his hat and
 * goes home. The gnome is a sprite sheet rendered in Blender (exoblend), drawn over the button; the
 * rope and its loop are drawn live in SVG from his hand (recorded per frame in Blender) to the form's
 * corner, because the form is a real element and can be anywhere on screen.
 * Reduced motion: the form opens at once. */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  function Lasso(root, meta, opts) {
    var button = root.querySelector('button'), sprite = root.querySelector('.gn-sprite');
    var form = document.querySelector(opts.form), closeBtn = form.querySelector('[data-close]');
    var cw = meta.cell[0], ch = meta.cell[1], cols = meta.cols, rows = Math.ceil(meta.frames / cols), s = 1;
    var B = meta.beats;

    // the rope layer: the whole viewport, above everything, never takes a click
    var svg = document.createElementNS(NS, 'svg'); svg.setAttribute('class', 'gn-rope');
    var rope = document.createElementNS(NS, 'path'), loop = document.createElementNS(NS, 'ellipse');
    [rope, loop].forEach(function (el) {
      el.setAttribute('fill', 'none'); el.setAttribute('stroke', '#8a5a2b');
      el.setAttribute('stroke-width', '3.5'); el.setAttribute('stroke-linecap', 'round'); svg.appendChild(el);
    });
    document.body.appendChild(svg);

    function place() {
      var b = meta.button; s = button.offsetHeight / (b.bottom - b.top);
      sprite.style.width = cw * s + 'px'; sprite.style.height = ch * s + 'px';
      sprite.style.left = button.offsetLeft + button.offsetWidth - b.right * s + 'px';
      sprite.style.top = button.offsetTop - b.top * s + 'px';
      sprite.style.backgroundImage = 'url(' + opts.sheet + ')';
      sprite.style.backgroundSize = cols * cw * s + 'px ' + rows * ch * s + 'px';
      svg.setAttribute('viewBox', '0 0 ' + innerWidth + ' ' + innerHeight);
    }
    function show(i) {
      sprite.style.opacity = i < 0 ? 0 : 1;
      if (i >= 0) sprite.style.backgroundPosition = -(i % cols) * cw * s + 'px ' + -Math.floor(i / cols) * ch * s + 'px';
    }
    function handAt(i) {   // the hand, in viewport pixels
      var r = sprite.getBoundingClientRect(), h = meta.hands[Math.min(i, meta.hands.length - 1)];
      return [r.left + h[0] * s, r.top + h[1] * s];
    }
    var ease = function (t) { return t < 0 ? 0 : t > 1 ? 1 : t * t * (3 - 2 * t); };

    // the form's two resting places: centred (where it lands) and above the screen (where it is caught)
    var end, start;
    function targets() {
      form.style.visibility = 'hidden'; form.classList.add('is-out');
      var w = form.offsetWidth, h = form.offsetHeight;
      end = [(innerWidth - w) / 2, Math.max(16, (innerHeight - h) / 2)];
      start = [end[0] - innerWidth * 0.18, -h - 60];
      form.style.visibility = '';
    }
    function putForm(x, y, tilt) {
      form.style.transform = 'translate(' + x + 'px,' + y + 'px) rotate(' + (tilt || 0) + 'deg)';
    }
    function cornerOf(x, y) { return [x + form.offsetWidth - 18, y + form.offsetHeight - 12]; } // bottom-right

    function drawRope(a, c, sag, alpha) {
      var mx = (a[0] + c[0]) / 2, my = (a[1] + c[1]) / 2 + sag;
      rope.setAttribute('d', 'M' + a[0] + ' ' + a[1] + ' Q' + mx + ' ' + my + ' ' + c[0] + ' ' + c[1]);
      rope.style.opacity = alpha;
    }
    function hideRope() { rope.style.opacity = 0; loop.style.opacity = 0; }

    var playing = false, frame = 0, last = 0, t0 = 0;
    function tick(t) {
      if (!playing) return;
      if (!t0) t0 = t;
      if (t - last >= 1000 / meta.fps) {
        last = t;
        if (frame >= meta.frames) { playing = false; show(-1); hideRope(); return; }
        show(frame);
        var hd = handAt(frame), i = frame;
        if (i >= B.spin[0] && i < B.spin[1]) {                       // spin the loop over his head
          var a = (t - t0) / 90, lx = hd[0] + Math.cos(a) * 6, ly = hd[1] - 30;   // the loop circles ABOVE the raised hand
          loop.setAttribute('cx', lx); loop.setAttribute('cy', ly);
          loop.setAttribute('rx', 26); loop.setAttribute('ry', 9 + 3 * Math.sin(a * 2)); loop.style.opacity = 1;
          drawRope(hd, [lx + 22 * Math.cos(a), ly + 8 * Math.sin(a)], 0, 1);
        } else if (i >= B.throw[0] && i < B.throw[1]) {              // throw it off the top of the screen
          var u = (i - B.throw[0] + 1) / (B.throw[1] - B.throw[0]), c0 = cornerOf(start[0], start[1]);
          var lx2 = hd[0] + (c0[0] - hd[0]) * u, ly2 = hd[1] + (c0[1] - hd[1]) * u;
          loop.setAttribute('cx', lx2); loop.setAttribute('cy', ly2); loop.setAttribute('rx', 30); loop.setAttribute('ry', 14);
          drawRope(hd, [lx2, ly2], 40 * (1 - u), 1);
        } else if (i >= B.haul[0] && i < B.haul[1]) {                // haul the form in, a tug at a time
          loop.style.opacity = 0;
          var n = B.haul[1] - B.haul[0], k = i - B.haul[0], tug = Math.floor(k / 3), within = (k % 3) / 3;
          var p = Math.min(1, (tug + ease(within * 1.5)) / Math.ceil(n / 3));
          var x = start[0] + (end[0] - start[0]) * ease(p), y = start[1] + (end[1] - start[1]) * ease(p);
          form.classList.add('is-out'); putForm(x, y, (1 - p) * -9);
          drawRope(hd, cornerOf(x, y), 6 * (1 - within), 1);
        } else if (i >= B.release && i < B.release + 6) {            // let go: the rope falls slack
          var f = (i - B.release) / 6, c1 = cornerOf(end[0], end[1]);
          putForm(end[0], end[1], 0);
          drawRope(hd, [c1[0] + 30 * f, c1[1] + 140 * f], 80 * f, 1 - f);
          if (i === B.release) { form.classList.add('is-landed'); var first = form.querySelector('input'); if (first) first.focus({ preventScroll: true }); }
        } else if (i >= B.release + 6) hideRope();
        frame++;
      }
      requestAnimationFrame(tick);
    }

    place(); show(-1); hideRope();
    addEventListener('resize', place);
    var reduce = matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
    function openNow() { targets(); putForm(end[0], end[1], 0); form.classList.add('is-out', 'is-landed'); }
    button.addEventListener('click', function () {
      if (form.classList.contains('is-out') || playing) return;
      if (reduce) return openNow();
      targets(); putForm(start[0], start[1], -9); form.classList.add('is-out');
      playing = true; frame = 0; last = 0; t0 = 0; requestAnimationFrame(tick);
    });
    closeBtn.addEventListener('click', function () { form.classList.remove('is-out', 'is-landed'); form.style.transform = ''; });
  }
  window.Lasso = Lasso;
})();
