/* ============================================================================
   toc.js — Custom Table of Contents (no library)
   ----------------------------------------------------------------------------
   Builds a TOC from the headings inside `.gh-content` and adds scroll-spy
   highlighting. Works with components/toc.hbs:
     <nav class="js-toc hidden"> … <ul data-toc></ul> </nav>
   - Fills EVERY .js-toc on the page (a page may show one TOC in a desktop
     rail and another in the mobile flow).
   - Only h2 and h3 are listed (h3 indented).
   - Headings missing an id get a slug so they can be anchored.
   - TOC navs stay hidden if the post has fewer than 2 headings.
   ========================================================================== */
(function () {
  'use strict';

  var navs = Array.prototype.slice.call(document.querySelectorAll('.js-toc'));
  var content = document.querySelector('.gh-content');
  if (!navs.length || !content) return;

  var headings = Array.prototype.slice.call(content.querySelectorAll('h2, h3'));
  if (headings.length < 2) return; // not worth a TOC

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
    var list = nav.querySelector('[data-toc]');
    if (!list) return;
    headings.forEach(function (h) {
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.href = '#' + h.id;
      a.textContent = h.textContent;
      a.className = 'toc-link' + (h.tagName === 'H3' ? ' is-h3' : '');
      a.addEventListener('click', function () {
        if (window.posthog) window.posthog.capture('toc section clicked', {
          section_id:    h.id,
          section_title: h.textContent,
          section_level: h.tagName.toLowerCase(),
          page_url:      window.location.href
        });
      });
      li.appendChild(a);
      list.appendChild(li);
      links.push(a);
    });
    nav.classList.remove('hidden'); // reveal now that it has content
  });

  // ── Scroll-spy: highlight the link(s) for the heading nearest the top ──
  function setActive(id) {
    links.forEach(function (a) {
      a.classList.toggle('is-active', a.getAttribute('href') === '#' + id);
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
})();
