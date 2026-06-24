/* ============================================================================
   theme-toggle.js — light/dark mode switch
   ----------------------------------------------------------------------------
   The PRE-PAINT script in default.hbs <head> applies the saved theme before
   first paint (avoids a flash). This file only wires up user interaction:
   clicking any `.ns-theme-toggle` button flips data-theme on <html>, persists
   it to localStorage('ns-theme'), and swaps the `.ns-theme-icon` glyph.
   Loaded (deferred) as part of built/casper.js, so the DOM is ready.
   ========================================================================== */
(function () {
  'use strict';

  var html = document.documentElement;
  var KEY = 'ns-theme';

  function isDark() {
    return html.getAttribute('data-theme') === 'dark';
  }

  function apply(dark) {
    html.setAttribute('data-theme', dark ? 'dark' : 'light');
    try { localStorage.setItem(KEY, dark ? 'dark' : 'light'); } catch (e) {}

    // Swap Phosphor moon ↔ sun on every toggle button's icon.
    document.querySelectorAll('.ns-theme-icon').forEach(function (el) {
      el.classList.toggle('ph-moon', !dark);
      el.classList.toggle('ph-sun', dark);
    });
  }

  // Sync icon state with the theme the pre-paint script already applied.
  apply(isDark());

  document.querySelectorAll('.ns-theme-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () { apply(!isDark()); });
  });

  // Follow OS changes only while the visitor hasn't made an explicit choice.
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
      try { if (!localStorage.getItem(KEY)) apply(e.matches); } catch (ex) {}
    });
  }
})();
