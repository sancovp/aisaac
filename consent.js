/* consent.js — the consent boxes on every plain form (the booking dialog's are capture.js's).
 *
 * EVERY TIME WE ASK, WE ASK FOR EVERYTHING WE MAY LEGALLY ASK FOR IN THAT INTERACTION: email · texts · calls ·
 * WhatsApp · call recording, each its own box, never ticked for them, none required. What an agent may later do is
 * exactly what these boxes granted (the call door refuses the rest), so a box not offered is a channel lost.
 *
 * On submit this writes `consent_record` — the EXACT SENTENCE of every ticked box, keyed by channel, with the time,
 * the page, the form's intent and the wording's version — which the relay stores on the contact. A ticked box that
 * needs a phone (texts, calls, WhatsApp) reveals the mobile field and makes it required; untick them all and it hides.
 */
(function () {
  'use strict';
  var forms = [].slice.call(document.querySelectorAll('form'));
  forms.forEach(function (form) {
    if (form.closest('#capture')) return;                       // the dialog's record is capture.js's
    var boxes = [].slice.call(form.querySelectorAll('[data-consent]'));
    if (!boxes.length) return;
    var record = form.querySelector('input[name="consent_record"]');
    var version = form.querySelector('input[name="consent_version"]');
    var intent = form.querySelector('input[name="intent"]');
    var phoneField = form.querySelector('.phone-field');
    var phone = phoneField ? phoneField.querySelector('input') : null;

    function needsPhone() {
      return boxes.some(function (b) { return b.checked && b.hasAttribute('data-needs-phone'); });
    }
    function sync() {
      if (!phoneField) return;
      var on = needsPhone();
      phoneField.hidden = !on;
      if (phone) phone.required = on;
    }
    boxes.forEach(function (b) { b.addEventListener('change', sync); });
    sync();

    form.addEventListener('submit', function () {
      var granted = {};
      boxes.forEach(function (b) {
        if (!b.checked) return;
        var span = b.parentNode.querySelector('span');
        granted[b.getAttribute('data-consent')] = (span ? span.textContent : '').replace(/\s+/g, ' ').trim();
      });
      if (record) {
        record.value = JSON.stringify({
          version: version ? version.value : '',
          at: new Date().toISOString(),
          page: location.href.split('#')[0],
          intent: intent ? intent.value : '',
          granted: granted
        });
      }
    });
  });
})();
