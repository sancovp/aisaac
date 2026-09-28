/* ref.js — remembers a referral partner's code (00-SITE-CANON § REFERRAL PARTNERS).
 *
 * A partner's link carries ?ref=<code>. The code is kept for 90 days, so a visitor who
 * comes back later still counts as theirs, and every form on the page carries it (plus
 * the page it was sent from) to the relay. A newer partner link replaces an older one.
 * Storage can be blocked; the page works the same without it.
 */
(function () {
  var KEY = 'twi_ref', DAYS = 90, RE = /^[a-z0-9_-]{1,40}$/i;
  var now = Date.now(), ref = '';

  try {
    var fromUrl = new URLSearchParams(location.search).get('ref');
    if (fromUrl && RE.test(fromUrl)) {
      ref = fromUrl.toLowerCase();
      localStorage.setItem(KEY, JSON.stringify({ ref: ref, until: now + DAYS * 864e5 }));
    } else {
      var kept = JSON.parse(localStorage.getItem(KEY) || 'null');
      if (kept && kept.until > now && RE.test(kept.ref)) ref = kept.ref;
    }
  } catch (e) {}

  function carry(form, name, value) {
    var el = form.querySelector('input[name="' + name + '"]');
    if (!el) { el = document.createElement('input'); el.type = 'hidden'; el.name = name; form.appendChild(el); }
    if (!el.value) el.value = value;
  }

  document.querySelectorAll('form').forEach(function (form) {
    if (ref) carry(form, 'ref', ref);
    carry(form, 'page', location.pathname);
  });
})();
