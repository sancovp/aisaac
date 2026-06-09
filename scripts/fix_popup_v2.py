"""Fix the exit popup - replace the whole exit-popup section with plumber copy."""
import re

path = '/Users/isaacwr/Desktop/claude_code/aisaac/cinematic-plumbing.html'
with open(path) as f:
    html = f.read()

# Find the start of the exit popup body and the end of the closing div
start_marker = '<!-- EXIT POPUP (no TWI/AISAAC attribution) -->'
end_marker = '</div>'  # close of popup-bg
# Find the popup box end
popup_close_marker = 'Or just search the content →</a>'

# Replace ONLY the inner content of the popup box, not the JS
# Pattern: from start_marker through the popup close

# Strategy: split by start_marker, replace everything from there to specific end point
if start_marker in html:
    start_idx = html.index(start_marker)
    # Find the end of the popup div (look for the </div> that closes exit-popup-bg)
    # The structure is: <div class="exit-popup-bg"...> ... <a class="exit-popup-search">...</a> </div></div>
    # Search from start_idx for the search marker
    after_start = html[start_idx:]
    search_idx = after_start.index(popup_close_marker)
    # Find the next </div> after search_idx
    end_search = after_start[search_idx:].index('</div>') + search_idx + len('</div>')
    # The exit-popup-bg closes on the NEXT </div> after that
    # Actually the structure has nested divs. Let me find the next </div> at the end of the </a> line
    full_end_in_after = after_start[end_search:].index('</div>') + end_search + len('</div>')

    new_section = '''<!-- EXIT POPUP (plumber-specific) -->
<div class="exit-popup-bg" id="exitPopupBg">
  <div class="exit-popup-box">
    <button class="exit-popup-close" id="exitPopupClose">&times;</button>
    <div class="exit-popup-tag">// 24/7 · Master Plumber · Direct Access</div>
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
    <a href="#reviews" class="exit-popup-search">Or read reviews →</a>
  </div>
</div>'''

    new_html = html[:start_idx] + new_section + html[start_idx + full_end_in_after:]
    with open(path, 'w') as f:
        f.write(new_html)
    print("DONE: replaced exit popup body", flush=True)
else:
    print("ERROR: start marker not found", flush=True)
