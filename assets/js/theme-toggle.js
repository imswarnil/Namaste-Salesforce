/* ============================================================================
   theme-toggle.js — light/dark mode switch
   ----------------------------------------------------------------------------
   The PRE-PAINT script in default.hbs <head> applies the saved theme before
   first paint (avoids a flash). This file only handles clicks on any
   `.ns-theme-toggle` button: it flips data-theme on <html> and persists the
   choice. The sun/moon glyph swap is pure CSS (dark: variant).
   ========================================================================== */
(function () {
  'use strict';

  var html = document.documentElement;
  var KEY = 'ns-theme';

  function isDark() { return html.getAttribute('data-theme') === 'dark'; }

  function apply(dark) {
    html.setAttribute('data-theme', dark ? 'dark' : 'light');
    try { localStorage.setItem(KEY, dark ? 'dark' : 'light'); } catch (e) {}
  }

  document.querySelectorAll('.ns-theme-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var nowDark = !isDark();
      apply(nowDark);
      if (window.posthog) window.posthog.capture('theme toggled', {
        theme: nowDark ? 'dark' : 'light'
      });
    });
  });

  // Follow OS changes only while the visitor hasn't made an explicit choice.
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
      try { if (!localStorage.getItem(KEY)) apply(e.matches); } catch (ex) {}
    });
  }
})();
