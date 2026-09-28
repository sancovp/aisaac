/* vsl.js — the pages' film player, the way a sales video plays in a funnel (*USER*'s ruling): the viewer
 * can turn the SOUND on and off and do nothing else — no clock, no runtime, no scrub bar, no pause, no
 * fullscreen. The film runs start to finish; the only control is mute, one round button in the corner,
 * and a click on the film toggles the sound too.
 *
 * The native <video controls> bar prints the runtime and no attribute suppresses it (controlsList has no
 * token for the time display), so with JS the native bar is removed and this draws the one control.
 *
 * Degrades honestly: if JS is off, the <video> keeps its `controls` attribute (set in the HTML) and the
 * YouTube embed is YouTube's own click-to-play — a film nobody can play is a worse failure than one whose
 * length shows.
 */
/* The silent loops (`video[data-loop]`) autoplay muted and carry no controls.
 * A visitor who asked for reduced motion gets them stopped on their poster,
 * with the native controls handed back so they can still choose to play. */
(function () {
  if (!window.matchMedia || !window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.querySelectorAll('video[data-loop]').forEach(function (v) {
    v.removeAttribute('autoplay');
    v.pause();
    v.setAttribute('controls', '');
  });
})();

/* THE PLAYER drives `v` — the page's <video>, or a YouTube embed behind the same face (youtube(), below):
 * the VSL is hosted on YouTube, unlisted, and plays here with YouTube's own controls hidden, so the
 * runtime is never shown there either. */
function drive(frame, v) {
  v.removeAttribute('controls');          // JS is here, so take the clock away
  frame.classList.add('vsl-custom');

  var ui = document.createElement('div');
  ui.className = 'vsl-ui';
  ui.innerHTML =
    '<button class="vsl-mute" type="button" aria-label="Mute">' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path class="vsl-icon-loud" d="M4 9v6h4l5 5V4L8 9H4z"/>' +
      '<path class="vsl-icon-quiet" d="M4 9v6h4l5 5V4L8 9H4zm14.5 3l2.5 2.5-1 1L17.5 13 15 15.5l-1-1L16.5 12 14 9.5l1-1L17.5 11 20 8.5l1 1z"/></svg></button>';
  frame.appendChild(ui);

  var muteBtn = ui.querySelector('.vsl-mute');

  v.addEventListener('play',  function () { frame.classList.add('is-playing'); });
  v.addEventListener('pause', function () { frame.classList.remove('is-playing'); });

  // the one thing the viewer controls is the sound — the button, or a click on the film
  function toggleSound() { setMuted(!v.muted); }
  muteBtn.addEventListener('click', toggleSound);
  v.addEventListener('click', function () { if (!frame.classList.contains('is-preview')) toggleSound(); });

  /* THE FILM STARTS WITH SOUND (*USER*'s ruling) — as far as a browser allows.
   * Chrome and Safari refuse sound before the visitor's first click, tap or
   * key press (the autoplay policy; no page can override it). So: ask for
   * sound first. If the browser refuses, the film plays silently while it is
   * on screen, and the visitor's FIRST gesture anywhere on the page — or
   * "Watch with sound" on the film — turns the sound on and starts it from
   * the top. A click that opens the booking form is not taken for it (the
   * film would talk over the form). After that the film runs to the end and
   * scrolling never pauses it. Reduced motion: no autoplay at all — the film
   * waits on its first frame under one "Play the video" button, which starts
   * it with sound, once; from then it plays like any other visitor's. */
  function setMuted(m) {
    v.muted = m;
    frame.classList.toggle('is-muted', m);
    muteBtn.setAttribute('aria-label', m ? 'Unmute' : 'Mute');
  }
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) {
    v.removeAttribute('autoplay');
    v.pause();
    setMuted(false);
    var start = document.createElement('button');
    start.type = 'button';
    start.className = 'vsl-sound';
    start.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>Play the video';
    frame.appendChild(start);
    start.addEventListener('click', function () { start.remove(); v.play(); });
    return;
  }

  var sound, gestures = ['pointerup', 'touchend', 'keydown'];
  function withSound(e) {
    if (e && e.currentTarget !== document) { e.preventDefault(); e.stopImmediatePropagation(); }
    if (!frame.classList.contains('is-preview')) return;
    frame.classList.remove('is-preview');
    if (sound) sound.remove();
    v.removeEventListener('click', withSound, true);
    gestures.forEach(function (g) { document.removeEventListener(g, onGesture, true); });
    setMuted(false);
    v.currentTime = 0;
    v.play();
  }
  function onGesture(e) {
    if (e.target.closest && e.target.closest('[data-buy], dialog, .vsl-sound')) return;
    withSound();
  }
  function silentPreview() {
    setMuted(true);
    frame.classList.add('is-preview');
    sound = document.createElement('button');
    sound.type = 'button';
    sound.className = 'vsl-sound';
    sound.innerHTML =
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 5V4L8 9H4zm12.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4z"/></svg>' +
      'Watch with sound';
    frame.appendChild(sound);
    sound.addEventListener('click', withSound);
    v.addEventListener('click', withSound, true);   // a click on the silent film = the same way in
    gestures.forEach(function (g) { document.addEventListener(g, onGesture, true); });

    var p = v.play(); if (p && p.catch) p.catch(function () {});
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        if (!frame.classList.contains('is-preview')) return;
        entries.forEach(function (en) {
          if (en.isIntersecting) { var q = v.play(); if (q && q.catch) q.catch(function () {}); }
          else v.pause();
        });
      }, { threshold: 0.35 }).observe(frame);
    }
  }

  setMuted(false);
  var tried = v.play();
  if (tried && tried.then) tried.then(function () {}, silentPreview);
  else if (v.paused) silentPreview();
}

/* A YOUTUBE EMBED WEARING THE <video> FACE drive() uses: play · pause · paused · muted · currentTime ·
 * duration · the play/pause/timeupdate events · click (taken by a clear layer over the iframe, which also
 * keeps YouTube's own hover bar and "more videos" off the film). play() resolves when YouTube reports it
 * playing and rejects when the browser refused (sound before a gesture), which is how drive() falls back
 * to the silent preview. Without JS the iframe plays on its own, YouTube's click-to-play. */
function youtube(frame, iframe, ready) {
  // the cover (style.css .vsl-cover): the film's title card over the player whenever it is not playing,
  // so YouTube's pause and end screens never show; the crop in style.css hides its title bar and buttons
  var cover = document.createElement('div');
  cover.className = 'vsl-cover';
  iframe.insertAdjacentElement('afterend', cover);
  var hit = document.createElement('div');
  hit.style.cssText = 'position:absolute;inset:0;z-index:1;cursor:pointer;background:transparent';
  cover.insertAdjacentElement('afterend', hit);
  var on = {}, state = -1, player, lift = 0, CHROME_FADES = 4200;
  // YouTube shows its own shading and a play/pause symbol for ~4 s after EVERY start and seek, so the
  // cover drops back on each one and lifts only after CHROME_FADES of uninterrupted playing
  function veil() {
    clearTimeout(lift); lift = 0;
    frame.classList.remove('is-yt-playing');
    if (state === 1) arm();
  }
  function arm() {
    if (lift || frame.classList.contains('is-yt-playing')) return;
    lift = setTimeout(function () { lift = 0; if (state === 1) frame.classList.add('is-yt-playing'); }, CHROME_FADES);
  }
  var emit = function (t) { (on[t] || []).forEach(function (fn) { fn({ type: t }); }); };
  var v = {
    removeAttribute: function () {}, setAttribute: function () {},
    get paused() { return state !== 1 && state !== 3; },
    get muted() { return player.isMuted(); },
    set muted(m) { if (m) player.mute(); else player.unMute(); },
    get currentTime() { return player.getCurrentTime(); },
    set currentTime(t) { player.seekTo(t, true); veil(); },
    get duration() { return player.getDuration(); },
    pause: function () { player.pauseVideo(); },
    play: function () {
      if (state !== 1) veil();   // a play call on a playing film changes nothing on screen
      player.playVideo();
      return new Promise(function (ok, no) {
        var t0 = Date.now();
        (function check() {
          if (state === 1) return ok();
          if (Date.now() - t0 > 1800) return no(new Error('refused'));
          setTimeout(check, 150);
        })();
      });
    },
    addEventListener: function (t, fn, cap) {
      if (t === 'click') return hit.addEventListener(t, fn, cap);
      (on[t] = on[t] || []).push(fn);
    },
    removeEventListener: function (t, fn, cap) {
      if (t === 'click') return hit.removeEventListener(t, fn, cap);
      on[t] = (on[t] || []).filter(function (x) { return x !== fn; });
    },
  };
  var boot = function () {
    player = new YT.Player(iframe, { events: {
      onReady: function () { setInterval(function () { if (state === 1) emit('timeupdate'); }, 250); ready(v); },
      onStateChange: function (e) {
        state = e.data;
        // playing ⇒ the cover lifts once YouTube's own chrome has faded (veil/arm, above); paused, ended,
        // not started ⇒ it returns; buffering leaves it as it is
        if (state === 1) arm();
        else if (state !== 3) veil();
        // the film burns in its own captions; YouTube's (auto-shown while muted) would double them
        if (state === 1) { try { player.unloadModule('captions'); } catch (err) {} emit('play'); }
        if (state === 2 || state === 0) emit('pause');
      },
    } });
  };
  if (window.YT && window.YT.Player) return boot();
  var prev = window.onYouTubeIframeAPIReady;
  window.onYouTubeIframeAPIReady = function () { if (prev) prev(); boot(); };
  var tag = document.createElement('script');
  tag.src = 'https://www.youtube.com/iframe_api';
  document.head.appendChild(tag);
}

(function () {
  var frame = document.querySelector('.artifact-frame.vsl');
  if (!frame) return;
  var video = frame.querySelector('video');
  if (video) return drive(frame, video);
  var iframe = frame.querySelector('iframe[data-youtube]');
  if (iframe) youtube(frame, iframe, function (v) { drive(frame, v); });
})();
