/* ============================================================================
   training-nav.js — cross-section Prev/Next for training modules
   ----------------------------------------------------------------------------
   Ghost's {{next_post}} can't reliably hop across tags, so module navigation is
   driven from the full ordered curriculum in the sidebar (#training-curriculum,
   which lists every track's modules in published order). We match the current
   URL to a curriculum link, then point the Prev / Next / Finish buttons at the
   adjacent links — so the last module of a track flows into the next track's
   first module automatically.

   Buttons in post-training.hbs start hidden — with the CLASS .is-hidden, not
   an inline style: no CSS may live in a template, including the two words of
   it that an inline `style` attribute is. They carry:
     .js-train-prev  .js-train-next  .js-train-finish
   plus an optional .js-train-label span that we fill with the target title.

   The rail is the .ns-sidenav component, so every row is `a.ns-sidenav__link`
   and titles are `.ns-sidenav__text`. Overview rows are KEPT in the sequence:
   finishing the last lesson of a section should land on the next section's
   OVERVIEW — you want to know what the next section is about before its first
   lesson drops you into it. Within a section, "previous" from lesson 1 goes
   back to that section's own overview for the same reason.
   ========================================================================== */
(function () {
  'use strict';

  var nav = document.getElementById('training-curriculum');
  if (!nav) return;

  // Every row, overviews included — the sequence a reader actually walks is
  // overview, lessons, next overview, its lessons, and so on.
  var links = Array.prototype.slice.call(nav.querySelectorAll('a.ns-sidenav__link'));
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
  links[idx].classList.add('is-current');

  var prev = links[idx - 1] || null;
  var next = links[idx + 1] || null;

  function labelOf(a) {
    // An overview row reads "Overview" in the rail, where its section heading
    // is directly above it. In the pager there is no such context, so the row
    // carries an explicit label naming the section.
    if (a.dataset.navLabel) return a.dataset.navLabel.trim();
    var t = a.querySelector('.ns-sidenav__text');
    return (t ? t.textContent : a.textContent).trim();
  }

  function apply(selector, link, direction) {
    if (!link) return;
    document.querySelectorAll(selector).forEach(function (el) {
      el.setAttribute('href', link.getAttribute('href'));
      el.classList.remove('is-hidden');
      var lab = el.querySelector('.js-train-label');
      if (lab) lab.textContent = labelOf(link);
      // Carry the target's TYPE glyph across from the rail row, so the pager
      // says what you are about to open — a video, an exercise, a section
      // overview — rather than just naming it. The rail already worked this
      // out; copying it means the two can never disagree.
      var src = link.querySelector('.ns-sidenav__type');
      var dst = el.querySelector('.js-train-icon');
      if (dst) {
        // Keep only the ph-* classes: the rail's own layout classes mean
        // nothing here, and .ns-sidenav__type--lock would drag the rail's
        // colour rule along with it.
        var glyph = src ? src.className.split(/\s+/).filter(function (c) {
          return c.indexOf('ph') === 0 || c.indexOf('ph-') === 0;
        }).join(' ') : '';
        dst.className = 'js-train-icon ' + (glyph || 'ph-fill ph-squares-four');
      }
      el.addEventListener('click', function () {
        if (window.posthog) window.posthog.capture('training module navigated', {
          direction:        direction,
          target_title:     labelOf(link),
          target_url:       link.getAttribute('href'),
          current_url:      window.location.href,
          module_index:     idx,
          total_modules:    links.length
        });
      });
    });
  }

  apply('.js-train-prev', prev, 'prev');
  apply('.js-train-next', next, 'next');

  // With a previous link present the pair fills both columns, so the no-JS
  // spacer would push "next" onto a second row — drop it.
  if (prev) {
    document.querySelectorAll('.ns-reader__foot').forEach(function (el) {
      el.classList.add('has-prev');
    });
  }

  // No next module anywhere → reveal the Finish button.
  if (!next) {
    document.querySelectorAll('.js-train-finish').forEach(function (el) {
      el.classList.remove('is-hidden');
      el.addEventListener('click', function () {
        if (window.posthog) window.posthog.capture('training curriculum completed', {
          current_url:   window.location.href,
          total_modules: links.length
        });
      });
    });
  }
})();
