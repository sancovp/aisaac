"""Replace the exit popup JS with a clean simple version."""
import re

path = '/Users/isaacwr/Desktop/claude_code/aisaac/cinematic-plumbing.html'
with open(path) as f:
    html = f.read()

# Old JS block
old_js = '''// Exit popup
(function() {
  var bg = document.getElementById('exitPopupBg');
  var cd = document.getElementById('ep-cd');
  var STORAGE = 'aisaac_exit_offer';
  var SESSION = 'aisaac_exit_shown';
  var OFFER_MS = 24 * 60 * 60 * 1000;

  function getState() {
    try { return JSON.parse(localStorage.getItem(STORAGE)) || { started: 0, expired: true }; }
    catch(e) { return { started: 0, expired: true }; }
  }
  function isExpired() {
    var s = getState();
    if (s.expired) return true;
    if (Date.now() - s.started > OFFER_MS) {
      try { localStorage.setItem(STORAGE, JSON.stringify({ started: 0, expired: true })); } catch(e){}
      return true;
    }
    return false;
  }
  function fmt(ms) {
    if (ms < 0) ms = 0;
    var s = Math.floor(ms / 1000);
    function p(n) { return n < 10 ? '0' + n : '' + n; }
    return p(Math.floor(s / 3600)) + ':' + p(Math.floor((s % 3600) / 60)) + ':' + p(s % 60);
  }
  function open() {
    if (bg.dataset.open) return;
    bg.dataset.open = '1';
    bg.classList.add('open');
    document.body.style.overflow = 'hidden';
    if (!isExpired()) {
      try { localStorage.setItem(STORAGE, JSON.stringify({ started: Date.now(), expired: false })); } catch(e){}
      startCountdown();
    }
  }
  function close() {
    bg.classList.remove('open');
    bg.dataset.open = '';
    document.body.style.overflow = '';
  }
  function startCountdown() {
    var s = getState();
    var remaining = (s.started + OFFER_MS) - Date.now();
    if (cd) cd.textContent = fmt(remaining);
    var iv = setInterval(function() {
      if (!bg.classList.contains('open')) { clearInterval(iv); return; }
      var remaining = (s.started + OFFER_MS) - Date.now();
      if (remaining <= 0) {
        clearInterval(iv);
        try { localStorage.setItem(STORAGE, JSON.stringify({ started: 0, expired: true })); } catch(e){}
        setTimeout(function() { location.reload(); }, 2000);
        return;
      }
      if (cd) cd.textContent = fmt(remaining);
    }, 1000);
  }
  document.getElementById('exitPopupClose').addEventListener('click', close);
  bg.addEventListener('click', function(e) { if (e.target === bg) close(); });
  document.addEventListener('keydown', function(e) { if (e.key === 'Escape') close(); });

  var triggered = false;
  document.addEventListener('mousemove', function(e) {
    if (triggered) return;
    if (e.clientY <= 8) { triggered = true; open(); }
  });
  document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden' && !triggered) {
      triggered = true;
      setTimeout(function() { if (document.visibilityState === 'visible') open(); }, 200);
    }
  });
})();'''

new_js = '''// Exit popup — plumber-specific 24/7 dispatch CTA
(function() {
  var bg = document.getElementById('exitPopupBg');
  if (!bg) return;
  function open() {
    if (bg.dataset.open) return;
    bg.dataset.open = '1';
    bg.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function close() {
    bg.classList.remove('open');
    bg.dataset.open = '';
    document.body.style.overflow = '';
  }
  document.getElementById('exitPopupClose').addEventListener('click', close);
  bg.addEventListener('click', function(e) { if (e.target === bg) close(); });
  document.addEventListener('keydown', function(e) { if (e.key === 'Escape') close(); });

  var triggered = false;
  document.addEventListener('mousemove', function(e) {
    if (triggered) return;
    if (e.clientY <= 8) { triggered = true; open(); }
  });
  document.addEventListener('visibilitychange', function() {
    if (document.visibilityState === 'hidden' && !triggered) {
      triggered = true;
      setTimeout(function() { if (document.visibilityState === 'visible') open(); }, 200);
    }
  });
})();'''

if old_js not in html:
    print("ERROR: old JS block not found", flush=True)
    raise SystemExit(1)

html = html.replace(old_js, new_js)

with open(path, 'w') as f:
    f.write(html)
print("DONE: replaced exit popup JS with plumber-specific version (no localStorage, no countdown)", flush=True)
