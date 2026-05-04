// TWI Funnel — sticky bar + qualification modal
(function() {
  var isApplyPage = location.pathname.indexOf('apply') !== -1;
  var answers = {};

  // ── CSS ──
  var style = document.createElement('style');
  style.textContent =
    // Sticky bar
    '.sticky-cta-bar{position:fixed;bottom:0;left:0;right:0;z-index:999;display:flex;align-items:center;justify-content:center;gap:1.5rem;padding:0.7rem 2rem;background:rgba(4,4,14,0.85);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-top:1px solid rgba(125,211,252,0.12);box-shadow:0 -4px 24px rgba(0,0,0,0.4);}' +
    '.sticky-cta-text{font-size:0.8rem;color:#94a3b8;}' +
    '.sticky-cta-btn{font-family:"JetBrains Mono","SF Mono",monospace;font-size:0.65rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:#000;background:linear-gradient(135deg,#7dd3fc,#a78bfa);padding:0.45rem 1.2rem;border-radius:8px;text-decoration:none;transition:all 0.3s;white-space:nowrap;cursor:pointer;}' +
    '.sticky-cta-btn:hover{filter:brightness(1.2);transform:translateY(-1px);}' +
    '@media(max-width:600px){.sticky-cta-bar{flex-direction:column;gap:0.5rem;padding:0.6rem 1rem;padding-bottom:max(0.6rem,env(safe-area-inset-bottom));}.sticky-cta-text{font-size:0.7rem;text-align:center;}}' +

    // Modal overlay
    '.qual-overlay{display:none;position:fixed;inset:0;z-index:10000;background:rgba(4,4,14,0.92);backdrop-filter:blur(24px);-webkit-backdrop-filter:blur(24px);overflow-y:auto;animation:qual-in .25s ease-out;}' +
    '.qual-overlay.open{display:flex;align-items:center;justify-content:center;}' +
    '@keyframes qual-in{from{opacity:0}to{opacity:1}}' +
    '.qual-box{max-width:520px;width:100%;margin:2rem;padding:2.5rem;position:relative;}' +
    '.qual-close{position:absolute;top:0;right:0;background:none;border:none;color:#64748b;font-size:1.5rem;cursor:pointer;padding:0.5rem;line-height:1;transition:color .2s;}' +
    '.qual-close:hover{color:#e2e8f0;}' +
    '.qual-progress{display:flex;gap:0.5rem;margin-bottom:2rem;}' +
    '.qual-dot{width:2rem;height:3px;border-radius:2px;background:rgba(255,255,255,0.07);transition:background .3s;}' +
    '.qual-dot.done{background:#7dd3fc;}' +
    '.qual-dot.current{background:#a78bfa;}' +
    '.qual-step{display:none;animation:qual-step-in .3s ease-out;}' +
    '.qual-step.active{display:block;}' +
    '@keyframes qual-step-in{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}' +
    '.qual-q{font-weight:600;font-size:1.15rem;color:#e2e8f0;margin-bottom:1.5rem;}' +
    '.qual-opts{display:flex;flex-direction:column;gap:0.7rem;}' +
    '.qual-opt{background:rgba(255,255,255,0.035);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:0.9rem 1.3rem;cursor:pointer;font-size:0.9rem;color:#94a3b8;transition:all .2s;}' +
    '.qual-opt:hover{border-color:rgba(125,211,252,0.25);color:#e2e8f0;transform:translateY(-1px);}' +
    '.qual-opt.selected{border-color:#7dd3fc;color:#e2e8f0;background:rgba(125,211,252,0.06);}' +
    '.qual-result{padding:1.5rem;background:rgba(255,255,255,0.035);border:1px solid rgba(255,255,255,0.07);border-radius:12px;margin-top:1rem;}' +
    '.qual-result h3{font-size:1.05rem;color:#e2e8f0;margin-bottom:0.6rem;}' +
    '.qual-result p{font-size:0.85rem;color:#94a3b8;line-height:1.7;margin-bottom:0.8rem;}' +
    '.qual-cta{display:inline-block;font-family:"JetBrains Mono","SF Mono",monospace;font-size:0.7rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:#000;background:linear-gradient(135deg,#7dd3fc,#a78bfa);padding:0.6rem 1.5rem;border-radius:8px;text-decoration:none;transition:all .3s;margin-top:0.5rem;}' +
    '.qual-cta:hover{filter:brightness(1.2);transform:translateY(-1px);}' +
    '.qual-alt{font-family:"JetBrains Mono","SF Mono",monospace;font-size:0.65rem;letter-spacing:0.06em;color:#7dd3fc;text-decoration:none;margin-left:1rem;}' +
    '.qual-alt:hover{color:#e2e8f0;}' +
    '.qual-escape{margin-top:1.5rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.07);font-size:0.75rem;color:#64748b;}' +
    '.qual-escape a{color:#a78bfa;text-decoration:none;}' +
    '.qual-escape a:hover{color:#e2e8f0;}' +
    '.qual-email-row{display:flex;gap:0.5rem;margin-top:0.5rem;}' +
    '.qual-input{flex:1;max-width:260px;background:rgba(255,255,255,0.035);border:1px solid rgba(255,255,255,0.07);border-radius:8px;padding:0.6rem 1rem;color:#e2e8f0;font-size:0.85rem;outline:none;}' +
    '.qual-input:focus{border-color:#7dd3fc;}' +
    '.qual-input::placeholder{color:#64748b;}' +
    '.qual-small-btn{font-family:"JetBrains Mono","SF Mono",monospace;font-size:0.6rem;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;color:#000;background:linear-gradient(135deg,#7dd3fc,#a78bfa);padding:0.5rem 1rem;border-radius:8px;border:none;cursor:pointer;}';
  document.head.appendChild(style);

  // ── Sticky bar (not on apply page) ──
  if (!isApplyPage) {
    var bar = document.createElement('div');
    bar.className = 'sticky-cta-bar';
    bar.innerHTML =
      '<span class="sticky-cta-text">AI automation for your business — guaranteed results in 30 days.</span>' +
      '<span class="sticky-cta-btn" data-qual-open>Book a Call</span>';
    document.body.appendChild(bar);
  }

  // ── Modal HTML ──
  var overlay = document.createElement('div');
  overlay.className = 'qual-overlay';
  overlay.innerHTML =
    '<div class="qual-box">' +
      '<button class="qual-close" data-qual-close>&times;</button>' +
      '<div class="qual-progress">' +
        '<div class="qual-dot current" data-dot="0"></div>' +
        '<div class="qual-dot" data-dot="1"></div>' +
        '<div class="qual-dot" data-dot="2"></div>' +
        '<div class="qual-dot" data-dot="3"></div>' +
      '</div>' +

      // Step 0
      '<div class="qual-step active" data-qstep="0">' +
        '<div class="qual-q">Are you a business owner?</div>' +
        '<div class="qual-opts">' +
          '<div class="qual-opt" data-val="yes" data-go="1">Yes, I run a business</div>' +
          '<div class="qual-opt" data-val="starting" data-go="1">Starting one — not live yet</div>' +
          '<div class="qual-opt" data-val="exploring" data-go="result-learn">Just exploring what\'s possible</div>' +
        '</div>' +
      '</div>' +

      // Step 1
      '<div class="qual-step" data-qstep="1">' +
        '<div class="qual-q">What\'s your monthly revenue?</div>' +
        '<div class="qual-opts">' +
          '<div class="qual-opt" data-val="pre" data-go="result-school">Pre-revenue / under $5K</div>' +
          '<div class="qual-opt" data-val="5-10k" data-go="result-school">$5K — $10K</div>' +
          '<div class="qual-opt" data-val="10-20k" data-go="2">$10K — $20K</div>' +
          '<div class="qual-opt" data-val="20-50k" data-go="2">$20K — $50K</div>' +
          '<div class="qual-opt" data-val="50k+" data-go="2">$50K+</div>' +
        '</div>' +
      '</div>' +

      // Step 2
      '<div class="qual-step" data-qstep="2">' +
        '<div class="qual-q">What\'s eating your time?</div>' +
        '<div class="qual-opts">' +
          '<div class="qual-opt" data-val="leads" data-go="3">Answering leads / follow-up</div>' +
          '<div class="qual-opt" data-val="content" data-go="3">Creating content consistently</div>' +
          '<div class="qual-opt" data-val="ops" data-go="3">Operations and repetitive tasks</div>' +
          '<div class="qual-opt" data-val="all" data-go="3">All of it — I need the whole system</div>' +
        '</div>' +
      '</div>' +

      // Step 3
      '<div class="qual-step" data-qstep="3">' +
        '<div class="qual-q">How soon do you want AI running?</div>' +
        '<div class="qual-opts">' +
          '<div class="qual-opt" data-val="now" data-go="result-qualified">This week</div>' +
          '<div class="qual-opt" data-val="soon" data-go="result-qualified">This month</div>' +
          '<div class="qual-opt" data-val="later" data-go="result-qualified">Just scoping it out</div>' +
        '</div>' +
      '</div>' +

      // Result: Qualified
      '<div class="qual-step" data-qstep="result-qualified">' +
        '<div class="qual-q">You\'re a fit.</div>' +
        '<div class="qual-result">' +
          '<h3>See it in action:</h3>' +
          '<p>Our AI agent will walk you through exactly what we\'d build for your business — live, right now. No obligation.</p>' +
          '<a href="#" class="qual-cta" data-demo-call>Get a Demo</a>' +
          '<p style="font-size:0.7rem;color:#64748b;margin-top:1rem;">[AI demo launching soon — book a discovery call in the meantime.]<br><a href="https://cal.com/aisaac/ai-agents-for-your-business" style="color:#7dd3fc;font-size:0.75rem;">Book discovery call →</a></p>' +
        '</div>' +
        '<p style="text-align:center;margin-top:1.5rem;"><a href="transform.html" class="qual-alt" style="margin:0;font-size:0.75rem;">Show me more first →</a></p>' +
      '</div>' +

      // Result: School
      '<div class="qual-step" data-qstep="result-school">' +
        '<div class="qual-q">The school is your fastest path.</div>' +
        '<div class="qual-result">' +
          '<h3>Here\'s the honest answer:</h3>' +
          '<p>My builds are for businesses doing $10K+/mo. At your stage, learning to build it yourself will give you the best ROI.</p>' +
          '<p>The 7-stack methodology, the frameworks, the exact system I use — that\'s what the school teaches.</p>' +
          '<a href="school.html" class="qual-cta">Enter the School</a>' +
          '<a href="free.html" class="qual-alt">Or browse free tools →</a>' +
          '<br><br>' +
          '<p style="font-size:0.8rem;">Get notified when the next cohort opens:</p>' +
          '<div class="qual-email-row">' +
            '<input type="email" class="qual-input" id="qual-school-email" placeholder="your@email.com">' +
            '<button class="qual-small-btn" onclick="window._qualCapture(\'school\')">Notify Me</button>' +
          '</div>' +
        '</div>' +
        '<div class="qual-escape"><p>Still want direct access? <a href="https://cal.com/aisaac/paid-session">$500 for 55 min with Isaac.</a></p></div>' +
      '</div>' +

      // Result: Learn
      '<div class="qual-step" data-qstep="result-learn">' +
        '<div class="qual-q">Start here.</div>' +
        '<div class="qual-result">' +
          '<h3>The best way to explore:</h3>' +
          '<p>27 frameworks, real architecture, zero fluff. The blog explains everything — how compound AI systems work and where the industry is headed.</p>' +
          '<a href="blog/" class="qual-cta">Read the Blog</a>' +
          '<a href="learn.html" class="qual-alt">Or browse the curriculum →</a>' +
        '</div>' +
        '<div class="qual-escape"><p>Want a direct conversation? <a href="https://cal.com/aisaac/paid-session">$500 for 55 min with Isaac.</a></p></div>' +
      '</div>' +

    '</div>';
  document.body.appendChild(overlay);

  // ── Fix relative links in modal for blog pages ──
  if (location.pathname.indexOf('/blog/') !== -1) {
    overlay.querySelectorAll('a[href^="learn"], a[href^="blog/"]').forEach(function(a) {
      a.href = '../' + a.getAttribute('href');
    });
  }

  // ── Open modal ──
  function openQual() {
    // Reset to step 0
    answers = {};
    overlay.querySelectorAll('.qual-step').forEach(function(s) { s.classList.remove('active'); });
    overlay.querySelector('.qual-step[data-qstep="0"]').classList.add('active');
    var dots = overlay.querySelectorAll('.qual-dot');
    dots.forEach(function(d, i) { d.className = 'qual-dot' + (i === 0 ? ' current' : ''); });
    overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  // ── Close modal ──
  function closeQual() {
    overlay.classList.remove('open');
    document.body.style.overflow = '';
  }

  // ── Navigate steps ──
  function goStep(id) {
    overlay.querySelectorAll('.qual-step').forEach(function(s) { s.classList.remove('active'); });
    var target = overlay.querySelector('.qual-step[data-qstep="' + id + '"]');
    if (target) target.classList.add('active');
    var num = parseInt(id);
    overlay.querySelectorAll('.qual-dot').forEach(function(d) {
      var ds = parseInt(d.dataset.dot);
      d.className = 'qual-dot';
      if (!isNaN(num)) {
        if (ds < num) d.classList.add('done');
        else if (ds === num) d.classList.add('current');
      } else { d.classList.add('done'); }
    });
    try { localStorage.setItem('twi_qualify', JSON.stringify(answers)); } catch(e) {}
  }

  // ── Email capture ──
  window._qualCapture = function(source) {
    var input = document.getElementById('qual-' + source + '-email');
    if (!input) return;
    var email = input.value.trim();
    if (!email || email.indexOf('@') === -1) { input.focus(); return; }
    answers.email = email;
    answers.source = source;
    try { localStorage.setItem('twi_qualify', JSON.stringify(answers)); } catch(e) {}
    input.value = '';
    input.placeholder = 'Saved — we\'ll be in touch.';
    input.disabled = true;
  };

  // ── Event delegation ──
  document.addEventListener('click', function(e) {
    // Open triggers: any link to apply.html or [data-qual-open]
    if (e.target.closest('[data-qual-open]')) { e.preventDefault(); openQual(); return; }

    var link = e.target.closest('a[href*="apply.html"]');
    if (link) { e.preventDefault(); openQual(); return; }

    // Close
    if (e.target.closest('[data-qual-close]')) { closeQual(); return; }
    if (e.target === overlay) { closeQual(); return; }

    // Option click inside modal
    var opt = e.target.closest('.qual-opt');
    if (opt) {
      opt.parentElement.querySelectorAll('.qual-opt').forEach(function(s) { s.classList.remove('selected'); });
      opt.classList.add('selected');
      var step = opt.closest('.qual-step').dataset.qstep;
      answers['step' + step] = opt.dataset.val;
      var next = opt.dataset.go;
      setTimeout(function() { goStep(next); }, 200);
    }
  });

  // ESC to close
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeQual();
  });
})();
