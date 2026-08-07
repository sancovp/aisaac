/* nav.js — the ONE permitted site-wide script (rebuild spec §2.4).
   Job: the mobile nav disclosure. Nothing else. No tracking, no popups,
   no injected CTAs, no email capture.

   Progressive enhancement in the SAFE direction: the collapsed state only
   exists once this file has run. With JS off, no data-nav attribute is ever
   set, the toggle button stays display:none and the nav links stay visible
   (wrapping to a second row). The menu is never unreachable. */
(function () {
  'use strict';

  var bar = document.querySelector('.nav, .header');
  if (!bar) return;

  var toggle = bar.querySelector('.nav-toggle');
  var links = bar.querySelector('.nav-links');
  if (!toggle || !links) return;

  if (!links.id) links.id = 'navlinks';
  toggle.setAttribute('aria-controls', links.id);
  toggle.setAttribute('aria-expanded', 'false');
  bar.setAttribute('data-nav', 'collapsed');

  function set(open) {
    bar.setAttribute('data-nav', open ? 'open' : 'collapsed');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  toggle.addEventListener('click', function () {
    set(bar.getAttribute('data-nav') !== 'open');
  });

  // Escape closes; following a link closes.
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && bar.getAttribute('data-nav') === 'open') {
      set(false);
      toggle.focus();
    }
  });
  links.addEventListener('click', function (e) {
    if (e.target.closest('a')) set(false);
  });
})();
