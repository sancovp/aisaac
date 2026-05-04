// Sticky CTA bar — auto-injected on all pages
(function() {
  if (location.pathname.indexOf('apply') !== -1) return;
  var bar = document.createElement('div');
  bar.className = 'sticky-cta-bar';
  var applyUrl = location.pathname.indexOf('/blog/') !== -1 ? '../apply.html' : 'apply.html';
  bar.innerHTML =
    '<span class="sticky-cta-text">AI automation for your business — guaranteed results in 30 days.</span>' +
    '<a href="' + applyUrl + '" class="sticky-cta-btn">Apply</a>';
  document.body.appendChild(bar);

  var style = document.createElement('style');
  style.textContent =
    '.sticky-cta-bar{' +
      'position:fixed;bottom:0;left:0;right:0;z-index:999;' +
      'display:flex;align-items:center;justify-content:center;gap:1.5rem;' +
      'padding:0.7rem 2rem;' +
      'background:rgba(4,4,14,0.85);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);' +
      'border-top:1px solid rgba(125,211,252,0.12);' +
      'box-shadow:0 -4px 24px rgba(0,0,0,0.4);' +
    '}' +
    '.sticky-cta-text{' +
      'font-size:0.8rem;color:#94a3b8;' +
    '}' +
    '.sticky-cta-btn{' +
      "font-family:'JetBrains Mono','SF Mono',monospace;" +
      'font-size:0.65rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;' +
      'color:#000;background:linear-gradient(135deg,#7dd3fc,#a78bfa);' +
      'padding:0.45rem 1.2rem;border-radius:8px;text-decoration:none;' +
      'transition:all 0.3s;white-space:nowrap;' +
    '}' +
    '.sticky-cta-btn:hover{filter:brightness(1.2);transform:translateY(-1px);}' +
    '@media(max-width:600px){' +
      '.sticky-cta-bar{flex-direction:column;gap:0.5rem;padding:0.6rem 1rem;padding-bottom:max(0.6rem,env(safe-area-inset-bottom));}' +
      '.sticky-cta-text{font-size:0.7rem;text-align:center;}' +
    '}';
  document.head.appendChild(style);
})();
