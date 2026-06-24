/* ============================================================================
   effects.js — Aceternity-style pointer spotlight
   ----------------------------------------------------------------------------
   For every `.js-spotlight` element, tracks the pointer and writes its position
   to --spot-x / --spot-y. The glow itself is a CSS ::before in screen.css that
   fades in on hover. Honours prefers-reduced-motion (the CSS disables it too).
   Uncoupled from any framework; safe to run on every page.
   ========================================================================== */
(function () {
  'use strict';

  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var els = document.querySelectorAll('.js-spotlight');
  if (!els.length) return;

  els.forEach(function (el) {
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty('--spot-x', (e.clientX - r.left) + 'px');
      el.style.setProperty('--spot-y', (e.clientY - r.top) + 'px');
    });
  });
})();
