/* ============================================================================
   toc.js — Custom Table of Contents (no library)
   ----------------------------------------------------------------------------
   Builds the TOC from the headings inside `.gh-content` and adds scroll-spy
   highlighting. Works with components/toc.hbs:
     <nav class="js-toc hidden"> … <ul data-toc></ul> </nav>
   - Only h2 and h3 are listed (h3 indented).
   - Headings missing an id get a slug so they can be anchored.
   - The TOC nav stays hidden if the post has fewer than 2 headings.
   ========================================================================== */
(function () {
  'use strict';

  var nav = document.querySelector('.js-toc');
  var list = nav && nav.querySelector('[data-toc]');
  var content = document.querySelector('.gh-content');
  if (!nav || !list || !content) return;

  var headings = Array.prototype.slice.call(content.querySelectorAll('h2, h3'));
  if (headings.length < 2) return; // not worth a TOC

  function slugify(text) {
    return text.toLowerCase().trim()
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-');
  }

  var used = {};
  var links = [];

  headings.forEach(function (h) {
    if (!h.id) {
      var base = slugify(h.textContent) || 'section';
      var id = base, n = 2;
      while (used[id] || document.getElementById(id)) { id = base + '-' + n++; }
      h.id = id;
    }
    used[h.id] = true;

    var li = document.createElement('li');
    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent;
    a.className = 'toc-link' + (h.tagName === 'H3' ? ' is-h3' : '');
    li.appendChild(a);
    list.appendChild(li);
    links.push(a);
  });

  // Reveal the TOC now that it has content.
  nav.classList.remove('hidden');

  // ── Scroll-spy: highlight the link for the heading nearest the top ──
  var byId = {};
  links.forEach(function (a) { byId[a.getAttribute('href').slice(1)] = a; });

  function setActive(id) {
    links.forEach(function (a) { a.classList.remove('is-active'); });
    if (byId[id]) byId[id].classList.add('is-active');
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
