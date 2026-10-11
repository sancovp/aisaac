/* door.js — THE DOOR (docs/the-door.md): the avatar picks itself, then its own CLOSER conversation (the hormozi-closer
 * skill) runs as screens in the glass panel and ends at the cart. Its bones are the survey the site had on 2026-06-10
 * (`git show 9b26f427:index.html`): screens, dots, Back, the answers kept in localStorage.
 *
 * A card either opens a screen (`data-step`), leaves for its page (`data-go`), or opens the booking dialog (`data-buy`,
 * capture.js's). A list marked `data-multi="<key>"` is pick-many (its Next moves on); a list marked `data-concerns` opens
 * each card's answer in place. Each avatar's conversation keeps its answers under its own prefix (own · fnd · lrn · ent ·
 * agc): its destination screen (`[data-vacation="<prefix>"]`) is drawn from what the visitor said — what they tried
 * (`<prefix>_tried`), said back; every pain they ticked (`[data-multi="<prefix>_pains"]`), with how JobWorld ends it;
 * their seats or clients; where it ends if nothing changes (`[data-consequence]`, each ticked pain's `data-cost`);
 * the reveal (`video[data-reveal]`, the real JobWorld working, played when its screen opens) — and its cart card (`data-cart="<prefix>"`, `data-tier`) carries those to the plans page.
 * The arm presses first (arm.js replays
 * the click on its press frame), then this moves on. Each screen slides in (CSS); reduced motion: no slide. */
(function () {
  'use strict';
  var door = document.querySelector('[data-door]');
  if (!door) return;
  var steps = [].slice.call(door.querySelectorAll('.door-step'));
  var back = door.querySelector('[data-back]');
  var dotsBox = door.querySelector('[data-dots]');
  var trail = ['start'];
  var answers = {};
  try { answers = JSON.parse(localStorage.getItem('twi_door') || '{}') || {}; } catch (e) { answers = {}; }

  function keep() { answers.at = new Date().toISOString(); try { localStorage.setItem('twi_door', JSON.stringify(answers)); } catch (e) {} }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function stepEl(id) { return door.querySelector('.door-step[data-step-id="' + id + '"]'); }

  function drawDots(n, of) {
    var h = '';
    for (var k = 1; k <= of; k++) h += '<span class="' + (k < n ? 'done' : k === n ? 'now' : '') + '"></span>';
    dotsBox.innerHTML = h;
  }

  // the size a conversation asked for: the owner's seats, the agency's clients; the founder is one seat
  function sizeOf(p) {
    if (p === 'own' && answers.own_seats) return answers.own_seats === '1' ? 'one seat' : answers.own_seats + ' seats';
    if (p === 'agc' && answers.agc_clients) return answers.agc_clients + ' clients';
    if (p === 'fnd') return 'one seat';
    return '';
  }
  var SIZE_LINE = {
    own: ' — one JobWorld for each person who runs part of the business.',
    agc: ' — each its own JobWorld, under your name.',
    fnd: ' — you, with an AI CEO and its departments.'
  };
  function pickedPains(p) {
    var picked = [].slice.call(door.querySelectorAll('[data-multi="' + p + '_pains"] .door-pick.is-picked'));
    return picked.length ? picked : [].slice.call(door.querySelectorAll('[data-multi="' + p + '_pains"] .door-pick'));
  }

  // THE VACATION (S): what they tried said back, every pain they ticked with how JobWorld ends it, and their size
  function drawVacation(box, p) {
    var out = '';
    var tried = door.querySelector('.door-card[data-key="' + p + '_tried"][data-val="' + answers[p + '_tried'] + '"]');
    if (tried) out += '<p class="door-vac-reply">' + esc(tried.getAttribute('data-reply')) + '</p>';
    out += '<ul class="door-vac-list">' + pickedPains(p).map(function (c) {
      return '<li><span class="door-vac-was">' + esc(c.querySelector('.door-card-k').textContent) + '</span>' +
             '<span class="door-vac-now">' + esc(c.getAttribute('data-solve')) + '</span></li>';
    }).join('') + '</ul>';
    var size = sizeOf(p);
    if (size) out += '<p class="door-vac-seats"><strong>' + esc(size.charAt(0).toUpperCase() + size.slice(1)) + '</strong>' +
      esc(SIZE_LINE[p] || '') + '</p>';
    box.innerHTML = out;
  }
  // WHERE IT ENDS (DOCTOR's Consequences): each pain they ticked, carried to where it goes if nothing changes
  function drawConsequence(box, p) {
    box.innerHTML = '<ul class="door-vac-list door-cost-list">' + pickedPains(p).map(function (c) {
      return '<li><span class="door-vac-was">' + esc(c.querySelector('.door-card-k').textContent) + '</span>' +
             '<span class="door-vac-now">' + esc(c.getAttribute('data-cost')) + '</span></li>';
    }).join('') + '</ul>';
  }
  function drawCartSum(box, p) {
    var n = door.querySelectorAll('[data-multi="' + p + '_pains"] .door-pick.is-picked').length;
    var size = sizeOf(p);
    var what = { lrn: [' thing', ' it changes for you'], ent: [' stall', ' it clears'] }[p] || [' thing', ' it takes off your plate'];
    box.innerHTML = '<p>' + (n ? n + what[0] + (n > 1 ? 's' : '') + what[1] : 'All of it, running') +
      (size ? ' · ' + esc(size) : '') + '.</p>';
  }

  function show(id) {
    var on = null;
    steps.forEach(function (s) {
      var is = s.getAttribute('data-step-id') === id;
      s.classList.toggle('is-on', is);
      if (is) on = s;
    });
    if (!on) return;
    drawDots(Number(on.getAttribute('data-dot')) || 1, Number(on.getAttribute('data-of')) || 3);
    back.hidden = trail.length < 2;
    var vac = on.querySelector('[data-vacation]'); if (vac) drawVacation(vac, vac.getAttribute('data-vacation'));
    var sum = on.querySelector('[data-cart-sum]'); if (sum) drawCartSum(sum, sum.getAttribute('data-cart-sum'));
    var cost = on.querySelector('[data-consequence]'); if (cost) drawConsequence(cost, cost.getAttribute('data-consequence'));
    // THE REVEAL: the real JobWorld plays the moment its screen opens, and stops when it closes
    [].slice.call(door.querySelectorAll('video[data-reveal]')).forEach(function (v) {
      if (on.contains(v) && !matchMedia('(prefers-reduced-motion: reduce)').matches) { v.play().catch(function () {}); }
      else { v.pause(); }
    });
    // the arm measures its button when shown: a screen that was hidden had no size
    window.dispatchEvent(new Event('resize'));
    var q = on.querySelector('.door-q');
    if (q) { q.setAttribute('tabindex', '-1'); q.focus({ preventScroll: true }); }
  }

  door.addEventListener('click', function (e) {
    var next = e.target.closest('.door-next');
    if (next && door.contains(next)) {
      var multi = next.closest('.door-step').querySelector('[data-multi]');
      if (multi) {
        answers[multi.getAttribute('data-multi')] = [].slice.call(multi.querySelectorAll('.is-picked')).map(function (p) { return p.getAttribute('data-val'); });
        keep();
      }
      trail.push(next.getAttribute('data-step')); show(next.getAttribute('data-step'));
      return;
    }
    var b = e.target.closest('.door-card');
    if (!b || !door.contains(b)) return;
    var list = b.closest('.door-opts');
    if (list && list.hasAttribute('data-multi')) { b.classList.toggle('is-picked'); b.setAttribute('aria-pressed', b.classList.contains('is-picked')); return; }
    if (list && list.hasAttribute('data-concerns')) {
      b.classList.toggle('is-open'); b.setAttribute('aria-expanded', b.classList.contains('is-open'));
      answers[list.getAttribute('data-concerns')] = [].slice.call(list.querySelectorAll('.is-open')).map(function (p) { return p.getAttribute('data-val'); });
      keep(); return;
    }
    var key = b.getAttribute('data-key'), val = b.getAttribute('data-val');
    if (key) { answers[key] = val; keep(); }
    if (key === 'lrn_for') {
      var f = door.querySelector('input[name="learn_for"]');
      if (f) f.value = val;
    }
    var go = b.getAttribute('data-go'), to = b.getAttribute('data-step');
    if (go) {
      // the cart: what the conversation decided rides along (the plans page ignores what it does not read)
      if (b.hasAttribute('data-cart')) {
        var p = b.getAttribute('data-cart');
        var q = new URLSearchParams({ from: 'door', avatar: answers.why || '' });
        if (answers[p + '_seats']) q.set('seats', answers[p + '_seats']);
        if (p === 'fnd') q.set('seats', '1');
        if (answers[p + '_clients']) q.set('clients', answers[p + '_clients']);
        if (b.getAttribute('data-tier')) q.set('tier', b.getAttribute('data-tier'));
        go += (go.indexOf('?') < 0 ? '?' : '&') + q.toString();
      }
      location.href = go; return;
    }
    if (to) { trail.push(to); show(to); }
    // data-buy: capture.js opens the booking dialog on the same click
  });

  back.addEventListener('click', function () {
    if (trail.length < 2) return;
    trail.pop();
    show(trail[trail.length - 1]);
  });

  show('start');
})();
