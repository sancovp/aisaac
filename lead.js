/* lead.js — carry what they typed into the booking page.
 *
 * THE PROBLEM THIS SOLVES: the form captures the lead (Formspree stores and
 * emails it BEFORE any booking, so someone who fills it in and never picks a
 * time is still a lead) and then hands them to cal.com — where cal's own
 * booking form asks for name and email AGAIN. Typing the same two things
 * twice is friction on the last step before the booking, which is the
 * worst place on the page to put any.
 *
 * So on submit this rewrites the `_next` redirect to carry name and email as
 * cal.com prefill params. Formspree still stores the full submission; cal.com
 * just arrives already filled in.
 *
 * ⛔ THE DIVISION OF LABOUR, so nobody "simplifies" this later:
 *     the page form  → asks everything, captures EVERYONE who submits
 *     cal.com        → asks only name/email/notes, captures only COMPLETED
 *                      bookings, and gets its name/email from here
 *   Qualification answers (company, revenue, focus) live in Formspree only.
 *   Do not duplicate them onto cal as booking questions — that is a third
 *   round of typing for data already captured.
 *
 * Degrades honestly: no JS means `_next` keeps its static value and the
 * booking still works, they just retype two fields.
 */
(function () {
  var form = document.querySelector('.lead-form');
  if (!form) return;
  var next = form.querySelector('input[name="_next"]');
  if (!next) return;
  var base = next.value;

  form.addEventListener('submit', function () {
    var name  = (form.elements.name  && form.elements.name.value  || '').trim();
    var email = (form.elements.email && form.elements.email.value || '').trim();
    var q = [];
    if (name)  q.push('name='  + encodeURIComponent(name));
    if (email) q.push('email=' + encodeURIComponent(email));
    next.value = q.length ? base + (base.indexOf('?') === -1 ? '?' : '&') + q.join('&') : base;
  });
})();
