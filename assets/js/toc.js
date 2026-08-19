/* ============================================================================
   toc.js — the table of contents (no library)
   ----------------------------------------------------------------------------
   Builds the outline from the headings inside `.gh-content`, then keeps the
   active item in step with the scroll position.

   THE MARKUP IT WRITES is the design system's .ns-toc (ds/components/css/
   toc.css), and two details of that contract are load-bearing:

     · Links are DIRECT CHILDREN of the [data-toc] element. .ns-toc is a flex
       column, not a list — wrapping each link in an <li> breaks the rail's
       leading hairline and the active item's brand bar. So this appends <a>
       straight onto the container.

     · Active state is aria-current="true", NOT a class. The CSS keys off the
       attribute the screen reader already announces, so the highlighted item
       and the announced item cannot drift apart.

   Fills EVERY [data-toc] on the page — components/toc.hbs renders two (a
   sticky rail for lg and up, a <details> disclosure below it), and a lesson
   page may add a third inside the player.

   Only h2 and h3 are listed; h3s get --sub. Two levels is the limit: an
   outline that needs three is a page that needs splitting.

   A post with fewer than two headings gets no TOC — every container stays
   without `.is-ready` and CSS keeps it display:none, so nothing flashes in
   and back out.
   ========================================================================== */
(function () {
  'use strict';

  var navs = Array.prototype.slice.call(document.querySelectorAll('[data-toc]'));
  var content = document.querySelector('.gh-content');
  if (!content) return;

  var headings = Array.prototype.slice.call(content.querySelectorAll('h2, h3'));
  // Fewer than two headings is not worth an outline — but the reading
  // progress at the foot of this file still is, so this skips the TOC rather
  // than returning out of the script.
  var worthIt = navs.length > 0 && headings.length >= 2;
  if (worthIt) buildToc();

  function buildToc() {

  function slugify(text) {
    return text.toLowerCase().trim()
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-');
  }

  var used = {};
  headings.forEach(function (h) {
    if (!h.id) {
      var base = slugify(h.textContent) || 'section';
      var id = base, n = 2;
      while (used[id] || document.getElementById(id)) { id = base + '-' + n++; }
      h.id = id;
    }
    used[h.id] = true;
  });

  var links = []; // across all TOC instances

  navs.forEach(function (nav) {
    headings.forEach(function (h) {
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      a.className = 'ns-toc__link' + (h.tagName === 'H3' ? ' ns-toc__link--sub' : '');
      a.addEventListener('click', function () {
        if (window.posthog) window.posthog.capture('toc section clicked', {
          section_id:    h.id,
          section_title: h.textContent,
          section_level: h.tagName.toLowerCase(),
          page_url:      window.location.href
        });
      });
      nav.appendChild(a);
      links.push(a);
    });
    nav.classList.add('is-ready'); // reveal now that it has content
  });

  // ── Scroll-spy: mark the link for the heading nearest the top ────────────
  function setActive(id) {
    links.forEach(function (a) {
      if (a.getAttribute('href') === '#' + id) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  }

  if ('IntersectionObserver' in window) {
    var visible = {};
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        visible[e.target.id] = e.isIntersecting;
      });
      // Pick the first heading (in document order) currently visible.
      for (var i = 0; i < headings.length; i++) {
        if (visible[headings[i].id]) { setActive(headings[i].id); break; }
      }
    }, { rootMargin: '0px 0px -75% 0px', threshold: 0 });

    headings.forEach(function (h) { observer.observe(h); });
  }
  } /* end buildToc */

  // ── Reading progress ─────────────────────────────────────────────────────
  // Two consumers, one measurement:
  //   .ns-toc__progress   the hairline at the top of the outline rail
  //   .ns-lprogress--article  the 2px line under the lesson header
  // Both are decoration in the honest sense — the outline already says where
  // you are — so both are aria-hidden and neither is the only indicator.
  //
  // The design system drives .ns-lprogress from its own assets/js/lms.js,
  // which this theme does not vendor. Rather than pull in a second script for
  // one custom property, it is computed here: the measurement is identical and
  // it is already being taken.
  var railBars = Array.prototype.slice.call(document.querySelectorAll('.ns-toc__progress'));
  var lineBars = Array.prototype.slice.call(document.querySelectorAll('.ns-lprogress[data-target]'));
  if (railBars.length || lineBars.length) {
    var tick = false;
    var update = function () {
      tick = false;
      var box = content.getBoundingClientRect();
      var span = box.height - window.innerHeight;
      var pct = span > 0 ? Math.min(100, Math.max(0, (-box.top / span) * 100)) : 0;
      var value = pct.toFixed(1) + '%';
      railBars.forEach(function (b) { b.style.setProperty('--ns-toc-progress', value); });
      lineBars.forEach(function (b) { b.style.setProperty('--fx-progress', value); });
    };
    window.addEventListener('scroll', function () {
      if (!tick) { tick = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }
})();
