/* ============================================================================
   navbar.js — header scroll behaviour
   ----------------------------------------------------------------------------
   Reads the `data-nav-behavior` attribute on `.ns-nav` (set from the
   @custom.navbar_behavior Ghost setting) and toggles state classes on scroll:
     • "Sticky"  / "Static"          → no JS (pure CSS position)
     • "Fixed on scroll"             → adds .is-fixed  past the threshold
     • "Island on scroll"            → adds .is-island past the threshold
   Both also get .is-scrolled for a subtle shadow. Passive listener + rAF.
   ========================================================================== */
(function () {
  'use strict';

  var nav = document.querySelector('.ns-nav[data-nav-behavior]');
  if (!nav) return;

  var mode = nav.getAttribute('data-nav-behavior') || 'Sticky';
  if (mode === 'Static' || mode === 'Sticky') return;

  var THRESHOLD = 48;
  var ticking = false;

  function update() {
    var scrolled = window.scrollY > THRESHOLD;
    nav.classList.toggle('is-scrolled', scrolled);
    nav.classList.toggle('is-island', scrolled && mode === 'Island on scroll');
    nav.classList.toggle('is-fixed', scrolled && mode === 'Fixed on scroll');
    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(update);
      ticking = true;
    }
  }

  update();
  window.addEventListener('scroll', onScroll, { passive: true });
})();
