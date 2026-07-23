/* ============================================================================
   training-video.js — video-module hero player + timestamp deep links
   ----------------------------------------------------------------------------
   On #training-type-video modules, post-training.hbs renders a hero media slot
   `[data-video-hero]` (poster image / gradient fallback). This script:
   1. Moves the FIRST embedded video found in `.gh-content` (YouTube/Vimeo
      iframe or a native <video>) up into that hero slot, replacing the poster
      — so the video always plays from the hero, not mid-article.
   2. Turns timestamps in content tables (e.g. a "chapters" table with 0:00 /
      12:34 / 1:02:03 cells) into buttons that SEEK the hero video and play it
      (YouTube via postMessage — enablejsapi is appended; native <video> via
      currentTime). Clicking also scrolls the hero into view.
   ========================================================================== */
(function () {
  'use strict';

  var hero = document.querySelector('[data-video-hero]');
  var content = document.querySelector('.gh-content');
  if (!hero || !content) return;

  // ── 1. adopt the first embedded video ──────────────────────────────────
  var embed = content.querySelector(
    'iframe[src*="youtube.com"], iframe[src*="youtube-nocookie.com"], iframe[src*="youtu.be"], iframe[src*="vimeo.com"], video'
  );
  var player = null;   // { kind: 'yt' | 'video', el }

  if (embed) {
    if (embed.tagName === 'IFRAME' && /youtu/.test(embed.src)) {
      // enable the JS API so timestamps can seek
      try {
        var u = new URL(embed.src, location.href);
        u.searchParams.set('enablejsapi', '1');
        u.searchParams.set('origin', location.origin);
        embed.src = u.toString();
      } catch (e) {}
      player = { kind: 'yt', el: embed };
    } else if (embed.tagName === 'VIDEO') {
      player = { kind: 'video', el: embed };
    } else {
      player = { kind: 'iframe', el: embed }; // vimeo etc — moved, no seeking
    }

    // Remove the (possibly figure-wrapped) embed from the flow, mount in hero.
    var wrapper = embed.closest('figure, .kg-card') || embed;
    hero.innerHTML = '';
    hero.appendChild(embed);
    embed.className = 'absolute inset-0 h-full w-full';
    embed.removeAttribute('width');
    embed.removeAttribute('height');
    if (wrapper !== embed && wrapper.parentNode) wrapper.parentNode.removeChild(wrapper);
  }

  // ── 2. timestamp → seek buttons ────────────────────────────────────────
  if (!player || player.kind === 'iframe') return;

  var TS = /^\(?(\d{1,2}):(\d{2})(?::(\d{2}))?\)?$/;

  function toSeconds(m) {
    return m[3] !== undefined
      ? (+m[1]) * 3600 + (+m[2]) * 60 + (+m[3])
      : (+m[1]) * 60 + (+m[2]);
  }

  function seek(sec) {
    if (player.kind === 'video') {
      player.el.currentTime = sec;
      player.el.play();
    } else {
      player.el.contentWindow.postMessage(JSON.stringify({
        event: 'command', func: 'seekTo', args: [sec, true]
      }), '*');
      player.el.contentWindow.postMessage(JSON.stringify({
        event: 'command', func: 'playVideo', args: []
      }), '*');
    }
    hero.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  content.querySelectorAll('table td, table th, li').forEach(function (cell) {
    var m = cell.textContent.trim().match(TS);
    if (!m) return;
    var sec = toSeconds(m);
    var label = cell.textContent.trim().replace(/[()]/g, ''); // capture before DOM mutation
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'js-ts';
    btn.innerHTML = '<i class="ph-fill ph-play-circle" aria-hidden="true"></i>' + label;
    btn.addEventListener('click', function () {
      seek(sec);
      if (window.posthog) window.posthog.capture('training video timestamp clicked', {
        timestamp_seconds: sec,
        timestamp_label:   label,
        video_kind:        player.kind,
        page_url:          window.location.href
      });
    });
    cell.textContent = '';
    cell.appendChild(btn);
  });
})();
