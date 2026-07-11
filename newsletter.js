// Changelog-newsletter exit popup — LAYER-1 capture per the funnel layer model
// (Isaac 2026-07-11): optional, never gates content. DORMANT until
// NEWSLETTER_FORM_URL is set to an ESP form endpoint (e.g. Buttondown:
// https://buttondown.com/api/emails/embed-subscribe/<username>). Empty = no-op.
(function () {
  var NEWSLETTER_FORM_URL = ""; // ← set to the ESP endpoint to arm the popup
  if (!NEWSLETTER_FORM_URL) return;

  var KEY = "changelog_popup";
  var state = {};
  try { state = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) {}
  if (state.done) return;
  if (state.snoozeUntil && Date.now() < state.snoozeUntil) return;

  var shown = false;

  function save(s) { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} }
  function snooze() { save({ snoozeUntil: Date.now() + 30 * 24 * 3600 * 1000 }); }

  function show() {
    if (shown) return;
    shown = true;

    var overlay = document.createElement("div");
    overlay.style.cssText =
      "position:fixed;inset:0;background:rgba(0,0,0,.65);z-index:9999;" +
      "display:flex;align-items:center;justify-content:center;padding:16px;";

    var card = document.createElement("div");
    card.style.cssText =
      "max-width:420px;width:100%;background:#16181d;color:#e8e6e3;" +
      "border:1px solid #333;border-radius:12px;padding:28px;" +
      "font-family:inherit;box-shadow:0 12px 48px rgba(0,0,0,.5);";
    card.innerHTML =
      '<h3 style="margin:0 0 10px;font-size:1.25rem;">Before you leave &mdash;</h3>' +
      '<p style="margin:0 0 16px;line-height:1.5;color:#b8b5b0;">Want to be on the ' +
      "<strong style=\"color:#e8b44f;\">changelog newsletter</strong>? It updates you on all the " +
      "advancements of my projects and research &mdash; before everything else.</p>" +
      '<form style="display:flex;gap:8px;flex-wrap:wrap;">' +
      '<input type="email" required placeholder="you@example.com" ' +
      'style="flex:1;min-width:180px;padding:10px 12px;border-radius:8px;' +
      'border:1px solid #444;background:#0e1013;color:#e8e6e3;font-size:.95rem;">' +
      '<button type="submit" style="padding:10px 18px;border-radius:8px;border:none;' +
      'background:#e8b44f;color:#16181d;font-weight:600;cursor:pointer;">Subscribe</button>' +
      "</form>" +
      '<button type="button" data-dismiss style="margin-top:12px;background:none;border:none;' +
      'color:#777;cursor:pointer;font-size:.85rem;padding:0;">No thanks</button>';

    overlay.appendChild(card);
    document.body.appendChild(overlay);

    function close(mark) {
      mark();
      overlay.remove();
      document.removeEventListener("keydown", onKey);
    }
    function onKey(e) { if (e.key === "Escape") close(snooze); }

    overlay.addEventListener("click", function (e) { if (e.target === overlay) close(snooze); });
    card.querySelector("[data-dismiss]").addEventListener("click", function () { close(snooze); });
    document.addEventListener("keydown", onKey);

    card.querySelector("form").addEventListener("submit", function (e) {
      e.preventDefault();
      var email = card.querySelector("input").value;
      var body = new FormData();
      body.append("email", email);
      fetch(NEWSLETTER_FORM_URL, { method: "POST", body: body, mode: "no-cors" })
        .catch(function () {})
        .finally(function () {
          card.innerHTML = '<p style="margin:0;line-height:1.5;">Done &mdash; you&#39;re on the changelog. ' +
                           "You&#39;ll hear about everything first.</p>";
          save({ done: true });
          setTimeout(function () { overlay.remove(); }, 2200);
        });
    });
  }

  // exit intent (cursor leaves toward the top) or deep scroll — whichever first
  document.addEventListener("mouseleave", function (e) { if (e.clientY <= 0) show(); });
  window.addEventListener("scroll", function () {
    var doc = document.documentElement;
    var depth = (window.scrollY + window.innerHeight) / doc.scrollHeight;
    if (depth > 0.7) show();
  }, { passive: true });
})();
