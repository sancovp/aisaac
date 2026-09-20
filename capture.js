/* capture.js — the buy-triggered capture modal, and the prefilled hand-off.
 *
 * Isaac, 2026-09-20: "contact form is now unnecessary here, and should be a
 * pop up once they click buy, because we prefill the cart. so its like buy ->
 * ok fill this -> heres the prefilled cart" · "also consent to contact is
 * important right there. 'fill this, sign this' and then we have unlocked AI
 * messaging..."
 *
 * REPLACES lead.js, whose whole job — rewrite `_next` so the destination
 * arrives prefilled — is folded in below and now serves three destinations
 * instead of one.
 *
 * ⛔ THE CAPTURE STILL PRECEDES THE HAND-OFF. Submit posts to Formspree first;
 * `_next` forwards afterwards. Someone who fills this in and abandons the
 * Stripe page is still a lead. That was the original reason the form existed
 * and the redesign does not get to lose it.
 *
 * ⛔ CONSENT IS REQUIRED FOR THE CALL AND OPTIONAL FOR A PURCHASE. Contacting
 * a customer about their own purchase is transactional; conditioning a SALE on
 * marketing consent is what GDPR treats as not freely given. For the call
 * there is no other lawful basis to contact them, so it is required there.
 *
 * ⛔ THE CONSENT STRING IS SUBMITTED WITH THE TICK. A stored boolean with no
 * record of what was agreed to is worth nothing later. The exact sentence goes
 * out in `consent_text`, dated by `consent_version` in the markup.
 *
 * Degrades honestly: no JS → the buttons are inert, but the dialog's form is
 * still a real Formspree form whose static `_next` is the booking page, so a
 * browser that shows the dialog inline still captures and still books.
 */
(function () {
  'use strict';

  var dlg = document.getElementById('capture');
  if (!dlg || typeof dlg.showModal !== 'function') return;

  var form     = dlg.querySelector('.lead-form');
  var next     = form.querySelector('input[name="_next"]');
  var intent   = form.querySelector('input[name="intent"]');
  var cText    = form.querySelector('input[name="consent_text"]');
  var consent  = form.querySelector('input[name="consent"]');
  var cCopy    = document.getElementById('consent-copy');
  var qualify  = dlg.querySelector('.qualify');
  var eyebrow  = document.getElementById('capture-eyebrow');
  var title    = document.getElementById('capture-title');
  var lede     = document.getElementById('capture-lede');
  var submit   = document.getElementById('capture-submit');
  var fine     = document.getElementById('capture-fine');

  /* ⏸ THE TWO STRIPE URLS DO NOT EXIST YET.
     Isaac creates the products; creating live payment objects on his account
     is not an agent's to do. Paste the Payment Link URLs here and nothing else
     needs to change — `prefill` appends Stripe's own `prefilled_email`. */
  var DEST = {
    founding: { url: '', prefill: 'stripe' },
    retainer: { url: '', prefill: 'stripe' },
    call:     { url: 'https://cal.com/aisaac/ai-transformation-discovery-call', prefill: 'cal' }
  };

  var COPY = {
    founding: {
      eyebrow: 'The 90-Day Founding Partnership',
      title:   'Before the checkout',
      lede:    'So the cart arrives filled in and I know whose business it is.',
      submit:  'Continue to checkout →',
      fine:    'You will not be charged on this step. Terms are confirmed at checkout.'
    },
    retainer: {
      eyebrow: 'The Partnership',
      title:   'Before the checkout',
      lede:    'So the cart arrives filled in and I know whose business it is.',
      submit:  'Continue to checkout →',
      fine:    'You will not be charged on this step. Terms are confirmed at checkout.'
    },
    call: {
      eyebrow: 'Book a call',
      title:   'Tell me how the business runs',
      lede:    'And I’ll tell you where the first box goes. No purchase.',
      submit:  'Book a call →',
      fine:    'You pick the time on the next screen.'
    }
  };

  var current = 'call';

  function open(kind) {
    current = DEST[kind] ? kind : 'call';
    var c = COPY[current];

    eyebrow.textContent = c.eyebrow;
    title.textContent   = c.title;
    lede.textContent    = c.lede;
    submit.textContent  = c.submit;
    fine.textContent    = c.fine;
    intent.value        = current;

    // qualification is the CALL's, not the checkout's (funnel-design §4)
    var isCall = current === 'call';
    qualify.hidden = !isCall;
    form.elements.revenue.required = isCall;

    // required for the call, optional for a purchase — see the header
    consent.required = isCall;
    dlg.classList.toggle('consent-required', isCall);

    dlg.showModal();
    var first = form.querySelector('input[name="name"]');
    if (first) first.focus();
  }

  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-buy]');
    if (t) { e.preventDefault(); open(t.getAttribute('data-buy')); return; }
    if (e.target.closest('[data-close]')) { dlg.close(); }
  });

  // click the backdrop to dismiss — the dialog element itself IS the backdrop
  // area, so a click landing on it rather than on the form means outside
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });

  form.addEventListener('submit', function (e) {
    var d = DEST[current];

    // ⛔ record WHAT they agreed to, not just that they did
    cText.value = consent.checked ? (cCopy.textContent || '').replace(/\s+/g, ' ').trim() : '';

    // a checkout with no URL yet must not silently post into nowhere
    if (d.prefill === 'stripe' && !d.url) {
      e.preventDefault();
      window.alert('Checkout is not connected yet — use "Book a call" for now.');
      return;
    }

    var name  = (form.elements.name.value  || '').trim();
    var email = (form.elements.email.value || '').trim();
    var q = [];

    if (d.prefill === 'stripe') {
      // Stripe's own prefill param on a Payment Link
      if (email) q.push('prefilled_email=' + encodeURIComponent(email));
    } else {
      // cal.com asks name/email again; carry both so nobody types twice
      if (name)  q.push('name='  + encodeURIComponent(name));
      if (email) q.push('email=' + encodeURIComponent(email));
    }

    next.value = q.length
      ? d.url + (d.url.indexOf('?') === -1 ? '?' : '&') + q.join('&')
      : d.url;
  });
})();
