/* ============================================================================
   course.js — count-up for course hero stats (.js-count with data-to).
   Animates 0 → data-to when the stat scrolls into view. Reduced-motion safe.
   ========================================================================== */
(function () {
  'use strict';

  var els = document.querySelectorAll('.js-count');
  if (!els.length) return;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function run(el) {
    var to = parseInt(el.getAttribute('data-to'), 10) || 0;
    if (reduce || to <= 0) { el.textContent = to; return; }
    var start = null, dur = 900;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / dur, 1);
      el.textContent = Math.round(p * to);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  if (!('IntersectionObserver' in window)) { els.forEach(run); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
    });
  }, { threshold: 0.4 });
  els.forEach(function (el) { io.observe(el); });
})();
