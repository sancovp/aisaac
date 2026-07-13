/* exit-popup.js
 * Exit-intent modal: shows once per session when cursor leaves viewport top.
 * Lifetime $150/meeting offer (forever) with real 24-hour expiry stored in localStorage.
 * After expiry: shows different "saved this for you" offer.
 *
 * Placeholders (TODO: replace before launch):
 *   - CAL_LINK_ONE_TIME      — cal.com link for one-time $150 45-min meeting
 *   - CAL_LINK_LIFETIME      — cal.com link for lifetime $150/meeting signup
 *   - CAL_LINK_EXPIRED       — cal.com link for the "saved this for you" offer
 *   - EXPIRED_OFFER_LABEL    — display name of the offer shown after expiry
 *   - EXPIRED_OFFER_HREF     — link to the offer page (e.g. /school.html)
 *   - SLOTS_REMAINING_TEXT   — marketing copy for the "spots left" counter
 */
(function() {
  var CAL_LINK_ONE_TIME = 'https://cal.com/aisaac/PLACEHOLDER_45MIN_150';        // TODO
  var CAL_LINK_LIFETIME = 'https://cal.com/aisaac/PLACEHOLDER_LIFETIME_150MEET'; // TODO
  var CAL_LINK_EXPIRED  = 'https://cal.com/aisaac/PLACEHOLDER_EXPIRED_OFFER';    // TODO
  var EXPIRED_OFFER_LABEL = 'the mastermind';                                     // TODO
  var EXPIRED_OFFER_HREF  = 'school.html';                                        // TODO
  var SLOTS_REMAINING_TEXT = '2 more students';

  var STORAGE_KEY = 'aisaac_exit_offer';
  var SESSION_KEY = 'aisaac_exit_shown';
  var OFFER_MS = 24 * 60 * 60 * 1000;

  function getOfferState() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return { started: 0, expired: true };
      return JSON.parse(raw);
    } catch (e) { return { started: 0, expired: true }; }
  }
  function startOffer() {
    var state = { started: Date.now(), expired: false };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) {}
  }
  function markExpired() {
    var state = { started: 0, expired: true };
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) {}
  }
  function isExpired() {
    var s = getOfferState();
    if (s.expired) return true;
    if (Date.now() - s.started > OFFER_MS) { markExpired(); return true; }
    return false;
  }
  function alreadyShownThisSession() {
    try { return sessionStorage.getItem(SESSION_KEY) === '1'; } catch (e) { return false; }
  }
  function markShownThisSession() {
    try { sessionStorage.setItem(SESSION_KEY, '1'); } catch (e) {}
  }

  // Inject styles once
  if (!document.getElementById('exit-popup-styles')) {
    var style = document.createElement('style');
    style.id = 'exit-popup-styles';
    style.textContent = ''
      + '#exit-popup-backdrop{position:fixed;inset:0;z-index:99999;background:rgba(250,247,241,0.96);display:none;align-items:center;justify-content:center;animation:ep-in .25s ease-out;}'
      + '#exit-popup-backdrop.open{display:flex;}'
      + '@keyframes ep-in{from{opacity:0;transform:scale(0.97)}to{opacity:1;transform:scale(1)}}'
      + '#exit-popup-box{max-width:560px;width:100%;margin:1.5rem;padding:2.5rem 2rem;position:relative;text-align:center;background:#FFFFFF;border:1px solid rgba(29,26,21,0.14);border-radius:6px;}'
      + '#exit-popup-box .ep-close{position:absolute;top:1rem;right:1.2rem;background:none;border:none;color:#877F6F;font-size:1.6rem;cursor:pointer;line-height:1;}'
      + '#exit-popup-box .ep-close:hover{color:#1D1A15;}'
      + '.ep-tag{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:0.62rem;letter-spacing:0.14em;text-transform:uppercase;color:#1E5A78;margin-bottom:1.2rem;}'
      + '.ep-h{font-family:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;font-weight:600;font-size:1.7rem;line-height:1.2;margin-bottom:0.8rem;color:#1D1A15;}'
      + '.ep-sub{font-size:0.9rem;line-height:1.7;color:#5D564A;margin-bottom:1.6rem;}'
      + '.ep-countdown{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:0.75rem;letter-spacing:0.1em;color:#1E5A78;margin-bottom:1.4rem;}'
      + '.ep-countdown b{color:#1D1A15;font-weight:700;font-variant-numeric:tabular-nums;}'
      + '.ep-offers{display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:1rem;}'
      + '.ep-offer{padding:1.1rem 0.8rem;border:1px solid rgba(29,26,21,0.14);border-radius:4px;background:#FAF7F1;text-decoration:none;color:#1D1A15;display:block;transition:border-color .15s;}'
      + '.ep-offer:hover{border-color:rgba(29,26,21,0.4);}'
      + '.ep-offer.ep-feature{border-color:#1E5A78;background:rgba(30,90,120,0.05);}'
      + '.ep-offer-label{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:0.58rem;letter-spacing:0.12em;text-transform:uppercase;color:#1E5A78;margin-bottom:0.4rem;display:block;}'
      + '.ep-offer-name{font-weight:700;font-size:0.95rem;margin-bottom:0.3rem;}'
      + '.ep-offer-price{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:0.72rem;color:#5D564A;margin-bottom:0.5rem;font-variant-numeric:tabular-nums;}'
      + '.ep-offer-cta{font-family:ui-monospace,"SF Mono",Menlo,monospace;font-size:0.58rem;letter-spacing:0.1em;text-transform:uppercase;color:#1E5A78;}'
      + '.ep-scarcity{font-size:0.72rem;color:#153F55;margin-top:0.5rem;font-style:italic;}'
      + '.ep-search{display:inline-block;margin-top:1.2rem;font-size:0.78rem;color:#5D564A;text-decoration:none;border-bottom:1px solid rgba(29,26,21,0.25);padding-bottom:0.1rem;}'
      + '.ep-search:hover{color:#1D1A15;border-color:#1E5A78;}'
      + '@media (max-width:560px){.ep-offers{grid-template-columns:1fr;}}'
    document.head.appendChild(style);
  }

  // Inject modal templates once
  if (!document.getElementById('exit-popup-templates')) {
    var tpl = document.createElement('div');
    tpl.id = 'exit-popup-templates';
    tpl.style.display = 'none';
    tpl.innerHTML = ''
      // Active offer modal
      + '<div data-tpl="active">'
      +   '<button class="ep-close" type="button">&times;</button>'
      +   '<div class="ep-tag">Wait &mdash; before you go</div>'
      +   '<div class="ep-h">Didn&rsquo;t find what you were looking for?</div>'
      +   '<p class="ep-sub">I promise I can help. Book a 1-on-1 with me and I&rsquo;ll go through your AI strategy with you, your business, your project &mdash; whatever you need to think through.</p>'
      +   '<div class="ep-countdown">Lifetime rate expires in <b class="ep-cd">00:00:00</b></div>'
      +   '<div class="ep-offers">'
      +     '<a class="ep-offer" data-link="one-time">'
      +       '<span class="ep-offer-label">One meeting</span>'
      +       '<div class="ep-offer-name">45 min with Isaac</div>'
      +       '<div class="ep-offer-price">$150 &middot; one-time</div>'
      +       '<div class="ep-offer-cta">Book once &rarr;</div>'
      +     '</a>'
      +     '<a class="ep-offer ep-feature" data-link="lifetime">'
      +       '<span class="ep-offer-label">Lifetime rate</span>'
      +       '<div class="ep-offer-name">$150/meeting, forever</div>'
      +       '<div class="ep-offer-price">45 min &middot; pay as you go</div>'
      +       '<div class="ep-offer-cta">Lock in &rarr;</div>'
      +     '</a>'
      +   '</div>'
      +   '<p class="ep-scarcity" data-slot>2 more students</p>'
      +   '<a class="ep-search" href="blog/">Or just search the content &rarr;</a>'
      + '</div>'
      // Expired offer modal
      + '<div data-tpl="expired">'
      +   '<button class="ep-close" type="button">&times;</button>'
      +   '<div class="ep-tag">Sorry &mdash; this offer expired</div>'
      +   '<div class="ep-h">I saved this for you.</div>'
      +   '<p class="ep-sub">If you really, really want to work with me, and you&rsquo;re really ready to take action to transform your life or business with AI collaboration, I saved <a class="ep-expired-link" href="#" style="color:#1E5A78;">the mastermind</a> for you.</p>'
      +   '<a class="ep-offer ep-feature" data-link="expired" style="max-width:280px;margin:1.2rem auto 0;">'
      +     '<div class="ep-offer-cta">See what I saved &rarr;</div>'
      +   '</a>'
      +   '<a class="ep-search" href="blog/">Or search the content &rarr;</a>'
      + '</div>';
    document.body.appendChild(tpl);
  }

  function fmt(ms) {
    if (ms < 0) ms = 0;
    var s = Math.floor(ms / 1000);
    var h = Math.floor(s / 3600);
    var m = Math.floor((s % 3600) / 60);
    var sec = s % 60;
    function pad(n) { return n < 10 ? '0' + n : '' + n; }
    return pad(h) + ':' + pad(m) + ':' + pad(sec);
  }

  function buildActiveModal() {
    var s = getOfferState();
    if (!s.started) startOffer();
    var remaining = (s.started + OFFER_MS) - Date.now();
    var src = document.querySelector('#exit-popup-templates [data-tpl="active"]');
    var box = document.createElement('div');
    box.id = 'exit-popup-box';
    box.innerHTML = src.innerHTML;
    box.querySelector('.ep-cd').textContent = fmt(remaining);
    box.querySelector('.ep-scarcity').textContent = SLOTS_REMAINING_TEXT + ' at this rate';
    box.querySelector('[data-link="one-time"]').href = CAL_LINK_ONE_TIME;
    box.querySelector('[data-link="lifetime"]').href = CAL_LINK_LIFETIME;
    return box;
  }

  function buildExpiredModal() {
    var src = document.querySelector('#exit-popup-templates [data-tpl="expired"]');
    var box = document.createElement('div');
    box.id = 'exit-popup-box';
    box.innerHTML = src.innerHTML;
    var link = box.querySelector('.ep-expired-link');
    link.href = EXPIRED_OFFER_HREF;
    link.textContent = EXPIRED_OFFER_LABEL;
    box.querySelector('[data-link="expired"]').href = CAL_LINK_EXPIRED;
    return box;
  }

  function open() {
    if (alreadyShownThisSession()) return;
    var existing = document.getElementById('exit-popup-backdrop');
    if (existing) existing.remove();
    var backdrop = document.createElement('div');
    backdrop.id = 'exit-popup-backdrop';
    var modal = isExpired() ? buildExpiredModal() : buildActiveModal();
    backdrop.appendChild(modal);
    document.body.appendChild(backdrop);
    requestAnimationFrame(function() { backdrop.classList.add('open'); });
    document.body.style.overflow = 'hidden';
    markShownThisSession();

    backdrop.addEventListener('click', function(e) {
      if (e.target.id === 'exit-popup-backdrop') close();
    });
    modal.querySelector('.ep-close').addEventListener('click', close);
    document.addEventListener('keydown', escClose);

    if (!isExpired()) startCountdown();
  }
  function escClose(e) { if (e.key === 'Escape') close(); }
  function close() {
    var b = document.getElementById('exit-popup-backdrop');
    if (b) b.remove();
    document.body.style.overflow = '';
    document.removeEventListener('keydown', escClose);
  }

  function startCountdown() {
    var el = document.querySelector('#exit-popup-backdrop .ep-cd');
    if (!el) return;
    var iv = setInterval(function() {
      el = document.querySelector('#exit-popup-backdrop .ep-cd');
      if (!el) { clearInterval(iv); return; }
      var s = getOfferState();
      var rem = (s.started + OFFER_MS) - Date.now();
      if (rem <= 0) {
        el.textContent = '00:00:00';
        markExpired();
        clearInterval(iv);
        setTimeout(function() {
          var b = document.getElementById('exit-popup-backdrop');
          if (b) {
            b.innerHTML = '';
            b.appendChild(buildExpiredModal());
            b.querySelector('.ep-close').addEventListener('click', close);
          }
        }, 2000);
        return;
      }
      el.textContent = fmt(rem);
    }, 1000);
  }

  // Exit intent: cursor leaves viewport top with non-zero velocity
  var armed = true;
  var triggered = false;
  document.addEventListener('mousemove', function(e) {
    if (!armed || triggered) return;
    if (e.clientY <= 8 && e.relatedTarget == null) {
      triggered = true;
      open();
    }
  });
  // Mobile: trigger on back-button or visibility change
  document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden' && armed && !triggered) {
      triggered = true;
      // Queue for when they come back
      setTimeout(function() { if (document.visibilityState === 'visible') open(); }, 200);
    }
  });
})();
