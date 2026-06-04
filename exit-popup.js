/* exit-popup.js
 * Exit-intent modal: shows once per session when cursor leaves viewport top.
 * Lifetime $150/hr offer with real 24-hour expiry stored in localStorage.
 * After expiry: shows different "saved this for you" offer.
 *
 * Placeholders (TODO: replace before launch):
 *   - CAL_LINK_ONE_TIME      — cal.com link for one-time $150 45-min meeting
 *   - CAL_LINK_LIFETIME      — cal.com link for lifetime $150/hr rate signup
 *   - CAL_LINK_EXPIRED       — cal.com link for the "saved this for you" offer
 *   - EXPIRED_OFFER_LABEL    — display name of the offer shown after expiry
 *   - EXPIRED_OFFER_HREF     — link to the offer page (e.g. /school.html)
 *   - SLOTS_REMAINING_TEXT   — marketing copy for the "spots left" counter
 */
(function() {
  var CAL_LINK_ONE_TIME = 'https://cal.com/aisaac/PLACEHOLDER_45MIN_150';        // TODO
  var CAL_LINK_LIFETIME = 'https://cal.com/aisaac/PLACEHOLDER_LIFETIME_150HR';   // TODO
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
      + '#exit-popup-backdrop{position:fixed;inset:0;z-index:99999;background:rgba(4,4,14,0.94);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);display:none;align-items:center;justify-content:center;animation:ep-in .25s ease-out;}'
      + '#exit-popup-backdrop.open{display:flex;}'
      + '@keyframes ep-in{from{opacity:0;transform:scale(0.97)}to{opacity:1;transform:scale(1)}}'
      + '#exit-popup-box{max-width:560px;width:100%;margin:1.5rem;padding:2.5rem 2rem;position:relative;text-align:center;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:16px;}'
      + '#exit-popup-close{position:absolute;top:1rem;right:1.2rem;background:none;border:none;color:rgba(255,255,255,0.4);font-size:1.6rem;cursor:pointer;line-height:1;}'
      + '#exit-popup-close:hover{color:rgba(255,255,255,0.9);}'
      + '.ep-tag{font-family:var(--mono);font-size:0.6rem;letter-spacing:0.14em;text-transform:uppercase;color:#5eead4;margin-bottom:1.2rem;}'
      + '.ep-h{font-weight:700;font-size:1.7rem;line-height:1.2;margin-bottom:0.8rem;background:linear-gradient(135deg,#7dd3fc,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}'
      + '.ep-sub{font-size:0.9rem;line-height:1.7;color:rgba(255,255,255,0.7);margin-bottom:1.6rem;}'
      + '.ep-countdown{font-family:var(--mono);font-size:0.75rem;letter-spacing:0.1em;color:#fda4af;margin-bottom:1.4rem;}'
      + '.ep-countdown b{color:#fff;font-weight:700;}'
      + '.ep-offers{display:grid;grid-template-columns:1fr 1fr;gap:0.8rem;margin-bottom:1rem;}'
      + '.ep-offer{padding:1.1rem 0.8rem;border:1px solid rgba(255,255,255,0.08);border-radius:10px;background:rgba(255,255,255,0.02);text-decoration:none;color:#fff;display:block;transition:all .2s;}'
      + '.ep-offer:hover{border-color:rgba(125,211,252,0.3);transform:translateY(-2px);}'
      + '.ep-offer.ep-feature{border-color:rgba(253,164,175,0.25);background:rgba(253,164,175,0.04);}'
      + '.ep-offer-label{font-family:var(--mono);font-size:0.55rem;letter-spacing:0.12em;text-transform:uppercase;color:#5eead4;margin-bottom:0.4rem;display:block;}'
      + '.ep-offer-name{font-weight:700;font-size:0.95rem;margin-bottom:0.3rem;}'
      + '.ep-offer-price{font-family:var(--mono);font-size:0.7rem;color:rgba(255,255,255,0.6);margin-bottom:0.5rem;}'
      + '.ep-offer-cta{font-family:var(--mono);font-size:0.55rem;letter-spacing:0.1em;text-transform:uppercase;color:#7dd3fc;}'
      + '.ep-scarcity{font-size:0.7rem;color:#fda4af;margin-top:0.5rem;font-style:italic;}'
      + '.ep-search{display:inline-block;margin-top:1.2rem;font-size:0.75rem;color:rgba(255,255,255,0.5);text-decoration:none;border-bottom:1px solid rgba(255,255,255,0.2);padding-bottom:0.1rem;}'
      + '.ep-search:hover{color:rgba(255,255,255,0.8);border-color:rgba(125,211,252,0.4);}'
      + '@media (max-width:560px){.ep-offers{grid-template-columns:1fr;}}'
    document.head.appendChild(style);
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
    return ''
      + '<div id="exit-popup-box">'
      +   '<button id="exit-popup-close" type="button">&times;</button>'
      +   '<div class="ep-tag">Wait &mdash; before you go</div>'
      +   '<div class="ep-h">Didn&rsquo;t find what you were looking for?</div>'
      +   '<p class="ep-sub">I promise I can help. Book a 1-on-1 with me and I&rsquo;ll go through your AI strategy with you, your business, your project &mdash; whatever you need to think through.</p>'
      +   '<div class="ep-countdown">Lifetime rate expires in <b id="ep-cd">' + fmt(remaining) + '</b></div>'
      +   '<div class="ep-offers">'
      +     '<a class="ep-offer" href="' + CAL_LINK_ONE_TIME + '">'
      +       '<span class="ep-offer-label">One-time</span>'
      +       '<div class="ep-offer-name">1 Meeting</div>'
      +       '<div class="ep-offer-price">$150 &middot; 45 min</div>'
      +       '<div class="ep-offer-cta">Book once &rarr;</div>'
      +     '</a>'
      +     '<a class="ep-offer ep-feature" href="' + CAL_LINK_LIFETIME + '">'
      +       '<span class="ep-offer-label">Lifetime rate</span>'
      +       '<div class="ep-offer-name">Pay-as-you-go</div>'
      +       '<div class="ep-offer-price">$150/hr &middot; forever</div>'
      +       '<div class="ep-offer-cta">Lock in &rarr;</div>'
      +     '</a>'
      +   '</div>'
      +   '<p class="ep-scarcity">' + SLOTS_REMAINING_TEXT + ' at this rate</p>'
      +   '<a class="ep-search" href="blog/">Or just search the content &rarr;</a>'
      + '</div>';
  }

  function buildExpiredModal() {
    return ''
      + '<div id="exit-popup-box">'
      +   '<button id="exit-popup-close" type="button">&times;</button>'
      +   '<div class="ep-tag">Sorry &mdash; this offer expired</div>'
      +   '<div class="ep-h">I saved this for you.</div>'
      +   '<p class="ep-sub">If you really, really want to work with me, and you&rsquo;re really ready to take action to transform your life or business with AI collaboration, I saved <a href="' + EXPIRED_OFFER_HREF + '" style="color:#7dd3fc;">' + EXPIRED_OFFER_LABEL + '</a> for you.</p>'
      +   '<a class="ep-offer ep-feature" href="' + CAL_LINK_EXPIRED + '" style="max-width:280px;margin:1.2rem auto 0;">'
      +     '<div class="ep-offer-cta">See what I saved &rarr;</div>'
      +   '</a>'
      +   '<a class="ep-search" href="blog/">Or search the content &rarr;</a>'
      + '</div>';
  }

  function open() {
    if (alreadyShownThisSession()) return;
    var existing = document.getElementById('exit-popup-backdrop');
    if (existing) existing.remove();
    var backdrop = document.createElement('div');
    backdrop.id = 'exit-popup-backdrop';
    backdrop.innerHTML = isExpired() ? buildExpiredModal() : buildActiveModal();
    document.body.appendChild(backdrop);
    requestAnimationFrame(function() { backdrop.classList.add('open'); });
    document.body.style.overflow = 'hidden';
    markShownThisSession();

    backdrop.addEventListener('click', function(e) {
      if (e.target.id === 'exit-popup-backdrop') close();
    });
    document.getElementById('exit-popup-close').addEventListener('click', close);
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
    var el = document.getElementById('ep-cd');
    if (!el) return;
    var iv = setInterval(function() {
      if (!document.getElementById('ep-cd')) { clearInterval(iv); return; }
      var s = getOfferState();
      var rem = (s.started + OFFER_MS) - Date.now();
      if (rem <= 0) {
        el.textContent = '00:00:00';
        markExpired();
        clearInterval(iv);
        // Auto-rotate to expired offer after 2s
        setTimeout(function() {
          var b = document.getElementById('exit-popup-backdrop');
          if (b) {
            b.innerHTML = buildExpiredModal();
            document.getElementById('exit-popup-close').addEventListener('click', close);
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
