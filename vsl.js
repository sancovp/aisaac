/* vsl.js — the landing page's film player.
 *
 * ⛔ IT EXISTS FOR ONE REASON: THE NATIVE <video controls> BAR PRINTS THE
 * RUNTIME. Isaac, 2026-09-18: "why the fuck would you tell them how long the
 * VSL is". The page copy was cleaned of it the same day, and then the browser
 * put it back — the control bar renders "0:00 / 9:20" with no attribute that
 * can suppress it (controlsList has no token for the time display).
 *
 * So the native bar is off and this draws the same controls minus the clock:
 * play/pause, a draggable progress line, mute, fullscreen. Scrubbing is kept
 * deliberately — hiding the scrubber to stop people skipping is hostile, and
 * an 8-minute film that cannot be paused is worse than one whose length is
 * visible.
 *
 * Degrades honestly: if JS is off, the <video> keeps its `controls` attribute
 * (set in the HTML) and everything works, runtime and all. A film nobody can
 * play is a worse failure than a film whose length shows.
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

(function () {
  var frame = document.querySelector('.artifact-frame.vsl');
  if (!frame) return;
  var v = frame.querySelector('video');
  if (!v) return;

  v.removeAttribute('controls');          // JS is here, so take the clock away
  frame.classList.add('vsl-custom');

  var ui = document.createElement('div');
  ui.className = 'vsl-ui';
  ui.innerHTML =
    '<button class="vsl-play" type="button" aria-label="Play">' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path class="vsl-icon-play" d="M8 5v14l11-7z"/>' +
      '<path class="vsl-icon-pause" d="M6 5h4v14H6zm8 0h4v14h-4z"/></svg></button>' +
    '<div class="vsl-track" role="slider" tabindex="0" aria-label="Seek">' +
      '<div class="vsl-fill"></div></div>' +
    '<button class="vsl-mute" type="button" aria-label="Mute">' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path class="vsl-icon-loud" d="M4 9v6h4l5 5V4L8 9H4z"/>' +
      '<path class="vsl-icon-quiet" d="M4 9v6h4l5 5V4L8 9H4zm14.5 3l2.5 2.5-1 1L17.5 13 15 15.5l-1-1L16.5 12 14 9.5l1-1L17.5 11 20 8.5l1 1z"/></svg></button>' +
    '<button class="vsl-full" type="button" aria-label="Fullscreen">' +
      '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4h5v2H6v3zm11-5h5v5h-2V6h-3zM6 15v3h3v2H4v-5zm12 0h2v5h-5v-2h3z"/></svg></button>';
  frame.appendChild(ui);

  var playBtn = ui.querySelector('.vsl-play');
  var track   = ui.querySelector('.vsl-track');
  var fill    = ui.querySelector('.vsl-fill');
  var muteBtn = ui.querySelector('.vsl-mute');
  var fullBtn = ui.querySelector('.vsl-full');

  function toggle() { v.paused ? v.play() : v.pause(); }
  playBtn.addEventListener('click', toggle);
  v.addEventListener('click', toggle);
  v.addEventListener('play',  function () { frame.classList.add('is-playing'); playBtn.setAttribute('aria-label', 'Pause'); });
  v.addEventListener('pause', function () { frame.classList.remove('is-playing'); playBtn.setAttribute('aria-label', 'Play'); });

  v.addEventListener('timeupdate', function () {
    if (!v.duration) return;
    var pct = (v.currentTime / v.duration) * 100;
    fill.style.width = pct + '%';
    track.setAttribute('aria-valuenow', Math.round(pct));   // percent, never seconds
  });

  function seekTo(clientX) {
    var r = track.getBoundingClientRect();
    var p = Math.min(1, Math.max(0, (clientX - r.left) / r.width));
    if (v.duration) v.currentTime = p * v.duration;
  }
  var dragging = false;
  track.addEventListener('pointerdown', function (e) { dragging = true; track.setPointerCapture(e.pointerId); seekTo(e.clientX); });
  track.addEventListener('pointermove', function (e) { if (dragging) seekTo(e.clientX); });
  track.addEventListener('pointerup',   function (e) { dragging = false; track.releasePointerCapture(e.pointerId); });
  track.addEventListener('keydown', function (e) {
    if (!v.duration) return;
    if (e.key === 'ArrowRight') { v.currentTime = Math.min(v.duration, v.currentTime + 10); e.preventDefault(); }
    if (e.key === 'ArrowLeft')  { v.currentTime = Math.max(0, v.currentTime - 10); e.preventDefault(); }
    if (e.key === ' ' || e.key === 'Enter') { toggle(); e.preventDefault(); }
  });

  muteBtn.addEventListener('click', function () {
    v.muted = !v.muted;
    frame.classList.toggle('is-muted', v.muted);
    muteBtn.setAttribute('aria-label', v.muted ? 'Unmute' : 'Mute');
  });

  fullBtn.addEventListener('click', function () {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (frame.requestFullscreen) frame.requestFullscreen();
  });
})();
