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
 * ⛔ ONE CONSENT PER CHANNEL, AND NOT ONE OF THEM IS REQUIRED.
 * (Superseded, kept: this said "required for the call, optional for a
 * purchase" until the channels were split out. It is now optional everywhere,
 * for two reasons that both bind: "not a condition of purchase" is a REQUIRED
 * element of US prior-express-written consent, and a sale gated on marketing
 * consent is not freely given under GDPR. Replying to somebody's own enquiry
 * is transactional and needs no permission at all.)
 *
 * ⛔ THE AUDIT RECORD IS THE POINT, NOT THE TICK. `consent_record` submits the
 * EXACT SENTENCE of every box they ticked, with a timestamp, the page and the
 * wording version, as JSON. A stored boolean that cannot say what was agreed
 * to is worth nothing in a dispute — and for SMS and voice, where damages are
 * per message, that record is the entire evidentiary position.
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
  var cRecord  = form.querySelector('input[name="consent_record"]');
  var cVersion = form.querySelector('input[name="consent_version"]');
  var boxes    = [].slice.call(form.querySelectorAll('[data-consent]'));
  var phoneFld = form.querySelector('.phone-field');
  var phone    = form.querySelector('input[name="phone"]');
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

    // ⛔ NO CONSENT IS EVER REQUIRED, ON EITHER PATH. "Not a condition of
    //    purchase" is a required element of US prior-express-written consent,
    //    and a sale gated on marketing consent is not freely given under GDPR.
    //    Replying to someone's own enquiry is transactional and needs none.

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

  /* ⛔ THE PHONE FIELD EXISTS ONLY WHEN A PHONE CONSENT IS TICKED, and is
     required only then. Asking for a mobile nobody consented to use is
     collecting data with no basis; asking for none while they tick "text me"
     is a consent that names no number, which under US rules is not one. */
  function syncPhone() {
    var wanted = boxes.some(function (b) {
      return b.checked && b.hasAttribute('data-needs-phone');
    });
    phoneFld.hidden = !wanted;
    phone.required = wanted;
    if (!wanted) phone.value = '';
  }
  form.addEventListener('change', function (e) {
    if (e.target.hasAttribute && e.target.hasAttribute('data-consent')) syncPhone();
  });

  form.addEventListener('submit', function (e) {
    var d = DEST[current];

    /* ⛔ THE AUDIT RECORD — the exact sentence of every ticked box, dated.
       A stored "yes" that cannot say what was agreed to is worth nothing in a
       dispute, and for SMS and voice it is the whole evidentiary point. */
    var granted = {};
    boxes.forEach(function (b) {
      if (!b.checked) return;
      var span = b.parentNode.querySelector('span');
      granted[b.getAttribute('data-consent')] =
        (span ? span.textContent : '').replace(/\s+/g, ' ').trim();
    });
    cRecord.value = JSON.stringify({
      version: cVersion ? cVersion.value : '',
      at: new Date().toISOString(),
      page: location.href.split('#')[0],
      intent: current,
      granted: granted
    });

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
