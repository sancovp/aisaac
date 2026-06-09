"""Fix the exit popup to be plumber-specific (remove Isaac's personal offer)."""
import re

path = '/Users/isaacwr/Desktop/claude_code/aisaac/cinematic-plumbing.html'
with open(path) as f:
    html = f.read()

old = '''    <div class="exit-popup-tag">// Master Plumber · Direct Access</div>
    <div class="exit-popup-h">Skip the call center.<br/>Talk to Isaac directamente.</div>
    <p class="exit-popup-sub">I take on a very small number of 1-on-1 calls each week. No sales rep, no dispatcher — you, me, and your actual problem.</p>
    <div class="exit-popup-countdown" id="exitPopupCountdown">This rate expires in <b id="ep-cd">00:00:00</b></div>
    <div class="exit-popup-offers">
      <a class="exit-popup-offer" id="epOneTime" href="https://cal.com/aisaac/PLACEHOLDER_45_MIN_150">
        <span class="exit-popup-offer-label">One meeting</span>
        <div class="exit-popup-offer-name">45 min · 1 call</div>
        <div class="exit-popup-offer-price">$150 · one-time</div>
        <div class="exit-popup-offer-cta">Book once →</div>
      </a>
      <a class="exit-popup-offer feature" id="epLifetime" href="https://cal.com/aisaac/PLACEHOLDER_LIFETIME_150HR">
        <span class="exit-popup-offer-label">Lifetime rate</span>
        <div class="exit-popup-offer-name">$150/meeting, forever</div>
        <div class="exit-popup-offer-price">45 min · pay as you go</div>
        <div class="exit-popup-offer-cta">Lock in →</div>
      </a>
    </div>
    <p class="exit-popup-scarcity">2 more students at this rate</p>
    <a href="blog/" class="exit-popup-search">Or just search the content →</a>'''

new = '''    <div class="exit-popup-tag">// 24/7 · Master Plumber · Direct Access</div>
    <div class="exit-popup-h">Pipe burst at 2AM?<br/>Skip the wait. Call us now.</div>
    <p class="exit-popup-sub">One call connects you directly to a licensed master plumber. No answering service. No call center. The person who picks up is the person who shows up.</p>
    <div class="exit-popup-countdown">Average on-site time: <b>under 60 minutes</b></div>
    <div class="exit-popup-offers">
      <a class="exit-popup-offer" id="epOneTime" href="tel:+17704276389">
        <span class="exit-popup-offer-label">Call now</span>
        <div class="exit-popup-offer-name">24/7 dispatch</div>
        <div class="exit-popup-offer-price">Cobb County, GA</div>
        <div class="exit-popup-offer-cta">Call (770) 427-6389 →</div>
      </a>
      <a class="exit-popup-offer feature" id="epLifetime" href="#services">
        <span class="exit-popup-offer-label">$50 service call</span>
        <div class="exit-popup-offer-name">Waived with work</div>
        <div class="exit-popup-offer-price">No obligation. 24/7.</div>
        <div class="exit-popup-offer-cta">See services →</div>
      </a>
    </div>
    <p class="exit-popup-scarcity">Family-owned. Master Plumber #MP007570.</p>
    <a href="#reviews" class="exit-popup-search">Or read reviews →</a>'''

if old not in html:
    print("ERROR: old block not found", flush=True)
    raise SystemExit(1)

html = html.replace(old, new)

# Also clean up the JS that uses #ep-cd and countdown — these don't exist anymore
js_old = '''    <div class="exit-popup-countdown">Average on-site time: <b>under 60 minutes</b></div>'''
# Actually the new countdown div doesn't have id, so we need to update the JS too

# Update JS to remove references to countdown that no longer exist
js_section_old = '''    var cd = document.getElementById('ep-cd');
    var STORAGE = 'aisaac_exit_offer';'''

js_section_new = '''    var STORAGE = 'aisaac_exit_offer';'''

html = html.replace(js_section_old, js_section_new)

js_start_old = '''    function startCountdown() {
    var s = getState();'''
# This is fine, no change needed for startCountdown

# Remove startCountdown() call from open() since we don't need it
js_call_old = '''    if (!isExpired()) {
      try { localStorage.setItem(STORAGE, JSON.stringify({ started: Date.now(), expired: false })); } catch(e){}
      startCountdown();
    }'''

js_call_new = '''    if (!isExpired()) {
      try { localStorage.setItem(STORAGE, JSON.stringify({ started: Date.now(), expired: false })); } catch(e){}
    }'''

html = html.replace(js_call_old, js_call_new)

# Remove the entire startCountdown function and the interval
# (since we removed the #ep-cd element, the function would just no-op)
# Better: just remove the function entirely
start_cd_old = '''  function startCountdown() {
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
  '''

if start_cd_old in html:
    html = html.replace(start_cd_old, '')

# Also remove the fmt() function since it's no longer used
fmt_old = '''  function fmt(ms) {
    if (ms < 0) ms = 0;
    var s = Math.floor(ms / 1000);
    function p(n) { return n < 10 ? '0' + n : '' + n; }
    return p(Math.floor(s / 3600)) + ':' + p(Math.floor((s % 3600) / 60)) + ':' + p(s % 60);
  }
  '''
if fmt_old in html:
    html = html.replace(fmt_old, '')

# Remove localStorage entirely (no countdown now)
js_storage_old = '''  function getState() {
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
  '''
if js_storage_old in html:
    html = html.replace(js_storage_old, '')

# Remove the localStorage write in open()
js_open_storage_old = '''    if (!isExpired()) {
      try { localStorage.setItem(STORAGE, JSON.stringify({ started: Date.now(), expired: false })); } catch(e){}
    }'''
if js_open_storage_old in html:
    html = html.replace(js_open_storage_old, '')

with open(path, 'w') as f:
    f.write(html)
print("DONE: exit popup cleaned of Isaac personal offer, now plumber-specific", flush=True)
