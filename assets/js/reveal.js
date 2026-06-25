/* ============================================================================
   reveal.js — reveal-on-scroll
   Adds `.is-visible` to `.js-reveal` elements as they enter the viewport.
   CSS handles the transition (and disables it under prefers-reduced-motion).
   ========================================================================== */
(function () {
  'use strict';
  var els = document.querySelectorAll('.js-reveal');
  if (!els.length) return;
  if (!('IntersectionObserver' in window)) {
    els.forEach(function (e) { e.classList.add('is-visible'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.1 });
  els.forEach(function (e) { io.observe(e); });
})();
