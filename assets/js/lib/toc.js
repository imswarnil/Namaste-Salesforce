/**
 * toc.js — Namaste Salesforce Ghost Theme
 * Universal Table of Contents
 *
 * Responsibilities:
 *  1. Find all headings (h2–h4) inside the post content.
 *  2. Build the <li> tree inside #ns-toc-list.
 *  3. Hide the TOC aside if no headings found.
 *  4. Highlight the active heading on scroll (IntersectionObserver).
 *  5. Update the reading-progress bar.
 *  6. Handle the collapse/expand toggle (ARIA-compliant).
 *
 * No dependencies. No inline styles. All state is expressed via
 * CSS classes (.is-active, .is-collapsed) and aria-* attributes.
 *
 * Designed to run once on DOMContentLoaded.
 * Safe to import in a <script type="module"> or a classic <script defer>.
 */

(function () {
  'use strict';

  // ─── Config ───────────────────────────────────────────────────────────────
  const CONFIG = {
    /** CSS selector for the article body Ghost renders post HTML into. */
    contentSelector: '.gh-content, .post-content, .entry-content, article .content',

    /** Heading levels to include in the TOC. */
    headingSelector: 'h2, h3, h4',

    /** Minimum headings required before the TOC is shown. */
    minHeadings: 2,

    /** IntersectionObserver rootMargin — negative top pushes threshold below navbar. */
    observerRootMargin: '-80px 0px -70% 0px',

    /** localStorage key to persist collapse state. */
    storageKey: 'ns-toc-collapsed',
  };

  // ─── Utility: slug-safe ID ────────────────────────────────────────────────
  function slugify(text) {
    return text
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .trim()
      .replace(/[\s_]+/g, '-')
      .replace(/-+/g, '-');
  }

  // Ensures each heading has a unique id, adding a numeric suffix if needed.
  function ensureId(el, usedIds) {
    if (!el.id) {
      let base = slugify(el.textContent || 'heading');
      if (!base) base = 'heading';
      let id = base;
      let counter = 2;
      while (usedIds.has(id)) {
        id = `${base}-${counter++}`;
      }
      el.id = id;
    }
    usedIds.add(el.id);
    return el.id;
  }

  // ─── Utility: depth from tag name ─────────────────────────────────────────
  function depthOf(tagName) {
    // h2 → 1, h3 → 2, h4 → 3, h5 → 4
    return parseInt(tagName.slice(1), 10) - 1;
  }

  // ─── Build the TOC list ───────────────────────────────────────────────────
  function buildList(headings) {
    const root = document.getElementById('ns-toc-list');
    if (!root) return [];

    const usedIds = new Set();
    const linkMap = []; // { el, linkEl }

    // Snapshot the base heading level for relative depth calculation.
    const baseLevel = headings.length
      ? parseInt(headings[0].tagName.slice(1), 10)
      : 2;

    headings.forEach(function (heading) {
      const id = ensureId(heading, usedIds);
      const depth = Math.max(1, parseInt(heading.tagName.slice(1), 10) - baseLevel + 1);

      const li = document.createElement('li');
      li.className = 'ns-toc__item';

      const a = document.createElement('a');
      a.href = `#${id}`;
      a.className = `ns-toc__link ns-toc__link--depth-${depth}`;
      a.textContent = heading.textContent;

      // Smooth-scroll and close mobile TOC
      a.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.getElementById(id);
        if (!target) return;
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Update URL hash without jumping
        history.pushState(null, '', `#${id}`);
        // On mobile, collapse the TOC after navigation
        if (window.innerWidth < 1024) {
          collapseBody(true);
        }
      });

      li.appendChild(a);
      root.appendChild(li);
      linkMap.push({ el: heading, linkEl: a });
    });

    return linkMap;
  }

  // ─── Active-link tracking (IntersectionObserver) ──────────────────────────
  function initObserver(linkMap) {
    if (!linkMap.length) return;

    const activeClass = 'is-active';
    let activeLink = null;

    function setActive(linkEl) {
      if (activeLink) activeLink.classList.remove(activeClass);
      activeLink = linkEl;
      if (activeLink) {
        activeLink.classList.add(activeClass);
        // Scroll the TOC so the active item stays visible
        scrollTocToActive(activeLink);
      }
    }

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            const match = linkMap.find(function (m) {
              return m.el === entry.target;
            });
            if (match) setActive(match.linkEl);
          }
        });
      },
      { rootMargin: CONFIG.observerRootMargin }
    );

    linkMap.forEach(function (m) {
      observer.observe(m.el);
    });
  }

  // Keeps the active TOC link within the scrollable sidebar viewport.
  function scrollTocToActive(linkEl) {
    const aside = document.getElementById('ns-toc');
    if (!aside) return;
    const tocRect = aside.getBoundingClientRect();
    const linkRect = linkEl.getBoundingClientRect();
    if (linkRect.top < tocRect.top || linkRect.bottom > tocRect.bottom) {
      linkEl.scrollIntoView({ block: 'nearest' });
    }
  }

  // ─── Reading progress bar ─────────────────────────────────────────────────
  function initProgressBar(contentEl) {
    const bar = document.getElementById('ns-toc-progress');
    if (!bar || !contentEl) return;

    function update() {
      const rect = contentEl.getBoundingClientRect();
      const total = rect.height - window.innerHeight;
      if (total <= 0) {
        bar.style.width = '100%';
        return;
      }
      const scrolled = Math.max(0, -rect.top);
      const pct = Math.min(100, (scrolled / total) * 100);
      bar.style.width = pct + '%';
    }

    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  // ─── Collapse / Expand ───────────────────────────────────────────────────
  function collapseBody(collapsed) {
    const body = document.getElementById('ns-toc-body');
    const btn = document.getElementById('ns-toc-toggle');
    if (!body || !btn) return;

    if (collapsed) {
      body.classList.add('is-collapsed');
      btn.setAttribute('aria-expanded', 'false');
    } else {
      body.classList.remove('is-collapsed');
      btn.setAttribute('aria-expanded', 'true');
    }

    try {
      localStorage.setItem(CONFIG.storageKey, collapsed ? '1' : '0');
    } catch (_) {
      // localStorage unavailable — continue silently
    }
  }

  function initToggle() {
    const btn = document.getElementById('ns-toc-toggle');
    if (!btn) return;

    // Restore persisted state
    let persisted = null;
    try {
      persisted = localStorage.getItem(CONFIG.storageKey);
    } catch (_) {}

    // Default: collapsed on mobile, expanded on desktop
    if (persisted !== null) {
      collapseBody(persisted === '1');
    } else if (window.innerWidth < 1024) {
      collapseBody(true);
    }

    btn.addEventListener('click', function () {
      const isExpanded = btn.getAttribute('aria-expanded') === 'true';
      collapseBody(isExpanded);  // toggle
    });
  }

  // ─── Main init ────────────────────────────────────────────────────────────
  function init() {
    const aside = document.getElementById('ns-toc');
    if (!aside) return;  // #hide-toc tag → partial not rendered → nothing to do

    // Find the post content container
    const contentEl = document.querySelector(CONFIG.contentSelector);
    if (!contentEl) {
      aside.classList.add('ns-toc--empty');
      return;
    }

    // Collect headings
    const headings = Array.from(
      contentEl.querySelectorAll(CONFIG.headingSelector)
    );

    if (headings.length < CONFIG.minHeadings) {
      aside.classList.add('ns-toc--empty');
      return;
    }

    // Build list → returns [{el, linkEl}]
    const linkMap = buildList(headings);

    // Wire up IntersectionObserver
    initObserver(linkMap);

    // Wire up progress bar
    initProgressBar(contentEl);

    // Wire up toggle button
    initToggle();
  }

  // ─── Boot ─────────────────────────────────────────────────────────────────
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();