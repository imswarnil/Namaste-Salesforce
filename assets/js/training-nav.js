/* ============================================================================
   training-nav.js — cross-section Prev/Next for training modules
   ----------------------------------------------------------------------------
   Ghost's {{next_post}} can't reliably hop across tags, so module navigation is
   driven from the full ordered curriculum in the sidebar (#training-curriculum,
   which lists every track's modules in published order). We match the current
   URL to a curriculum link, then point the Prev / Next / Finish buttons at the
   adjacent links — so the last module of a track flows into the next track's
   first module automatically.

   Buttons in post-training.hbs start hidden (style="display:none") and carry:
     .js-train-prev  .js-train-next  .js-train-finish
   plus an optional .js-train-label span that we fill with the target title.
   ========================================================================== */
(function () {
  'use strict';

  var nav = document.getElementById('training-curriculum');
  if (!nav) return;

  var links = Array.prototype.slice.call(nav.querySelectorAll('a.doc-nav-link'));
  if (!links.length) return;

  function normalise(href) {
    return (href || '')
      .replace(/^https?:\/\/[^/]+/, '') // strip origin
      .replace(/[?#].*$/, '')           // strip query/hash
      .replace(/\/+$/, '');             // strip trailing slash
  }

  var here = normalise(window.location.pathname);
  var idx = -1;
  for (var i = 0; i < links.length; i++) {
    if (normalise(links[i].getAttribute('href')) === here) { idx = i; break; }
  }
  if (idx < 0) return;

  // Make sure the matched item is highlighted (independent of server-side match).
  links[idx].classList.add('is-doc-active');

  var prev = links[idx - 1] || null;
  var next = links[idx + 1] || null;

  function labelOf(a) {
    var t = a.querySelector('.truncate');
    return (t ? t.textContent : a.textContent).trim();
  }

  function apply(selector, link) {
    if (!link) return;
    document.querySelectorAll(selector).forEach(function (el) {
      el.setAttribute('href', link.getAttribute('href'));
      el.style.display = '';
      var lab = el.querySelector('.js-train-label');
      if (lab) lab.textContent = labelOf(link);
    });
  }

  apply('.js-train-prev', prev);
  apply('.js-train-next', next);

  // No next module anywhere → reveal the Finish button.
  if (!next) {
    document.querySelectorAll('.js-train-finish').forEach(function (el) { el.style.display = ''; });
  }
})();
