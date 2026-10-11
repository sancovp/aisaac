/* door.js — THE DOOR (docs/the-door.md): one question, five cards, a short flow under two of them. Its logic is the
 * survey the site had on 2026-06-10 (`git show 9b26f427:index.html`): steps, dots, a back button, the answers kept in
 * localStorage. An option either opens a step (`data-step`), leaves for its part (`data-go`), or opens the booking
 * dialog (`data-buy`, capture.js's). The arm presses first (arm.js replays the click on its press frame), then this
 * moves on. Each step slides in (CSS, `.door-step.is-on`); reduced motion: no slide. */
(function () {
  'use strict';
  var door = document.querySelector('[data-door]');
  if (!door) return;
  var steps = [].slice.call(door.querySelectorAll('.door-step'));
  var back = door.querySelector('[data-back]');
  var dots = [].slice.call(door.querySelectorAll('[data-dot-n]'));
  var trail = ['start'];
  var answers = {};
  try { answers = JSON.parse(localStorage.getItem('twi_door') || '{}') || {}; } catch (e) { answers = {}; }

  function keep() { try { localStorage.setItem('twi_door', JSON.stringify(answers)); } catch (e) {} }

  function show(id) {
    var on = null;
    steps.forEach(function (s) {
      var is = s.getAttribute('data-step-id') === id;
      s.classList.toggle('is-on', is);
      if (is) on = s;
    });
    var n = on ? Number(on.getAttribute('data-dot')) : 1;
    dots.forEach(function (d) {
      var k = Number(d.getAttribute('data-dot-n'));
      d.className = k < n ? 'done' : k === n ? 'now' : '';
    });
    back.hidden = trail.length < 2;
    // the arm measures its button when shown: a step that was hidden had no size
    window.dispatchEvent(new Event('resize'));
    var q = on && on.querySelector('.door-q');
    if (q) { q.setAttribute('tabindex', '-1'); q.focus({ preventScroll: true }); }
  }

  door.addEventListener('click', function (e) {
    var b = e.target.closest('.door-card');
    if (!b || !door.contains(b)) return;
    var key = b.getAttribute('data-key'), val = b.getAttribute('data-val');
    if (key) { answers[key] = val; answers.at = new Date().toISOString(); keep(); }
    if (key === 'for') {
      var f = door.querySelector('input[name="learn_for"]');
      if (f) f.value = val;
    }
    var go = b.getAttribute('data-go'), next = b.getAttribute('data-step');
    if (go) { location.href = go; return; }
    if (next) { trail.push(next); show(next); }
    // data-buy: capture.js opens the booking dialog on the same click
  });

  back.addEventListener('click', function () {
    if (trail.length < 2) return;
    trail.pop();
    show(trail[trail.length - 1]);
  });

  show('start');
})();
