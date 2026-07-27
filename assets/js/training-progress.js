/* ============================================================================
   training-progress.js — the rail's progress readout and search behaviour
   ----------------------------------------------------------------------------
   Lifted out of partials/training/curriculum.hbs, where it was an inline
   <script>. A template should describe what is on the page, not carry the
   behaviour of it: inline scripts cannot be cached, cannot be minified with
   the rest of the bundle, and are invisible to anyone reading assets/js/ to
   find out what runs on this site.

   TWO JOBS.

   1. PROGRESS. Everything before the current lesson counts as done — the only
      thing a static site can honestly know without a member record. The
      readout is written into the rail's sticky foot.

   2. SEARCH. The rail is an exclusive accordion (every <details> shares one
      `name`), which is exactly right while navigating and exactly wrong while
      searching: matches in three sections cannot all be visible if only one
      section may be open. So `name` is dropped for the duration of a query and
      restored, with the current section reopened, when the query clears.
   ========================================================================== */
(function () {
  'use strict';
  var panel = document.querySelector('#training-curriculum');
  if (!panel) return;

  var links = Array.prototype.slice.call(panel.querySelectorAll('.ns-sidenav__link'));
  var current = panel.querySelector('.ns-sidenav__link.is-current');

  if (current) {
    for (var i = 0; i < links.length; i++) {
      if (links[i] === current) break;
      // the section overview rows are not lessons — don't count them
      if (links[i].querySelector('.ns-sidenav__num > span')) links[i].classList.add('is-done');
    }
    var done = panel.querySelectorAll('.ns-sidenav__link.is-done').length;
    var total = panel.querySelectorAll('.ns-sidenav__num > span').length;
    // The readout lives in the sub bar above, not in this rail.
    var bar = document.querySelector('.js-train-progress');
    var out = document.querySelector('.js-train-done');
    // The floating button carries the same fact in its shortest form.
    document.querySelectorAll('.js-train-count').forEach(function (el) {
      el.textContent = done + '/' + total;
    });
    if (bar && total) bar.style.width = Math.round((done / total) * 100) + '%';
    if (out) out.textContent = done + ' / ' + total + ' done';
  } else {
    var out0 = document.querySelector('.js-train-done');
    var tot0 = panel.querySelectorAll('.ns-sidenav__num > span').length;
    if (out0) out0.textContent = '0 / ' + tot0 + ' done';
    document.querySelectorAll('.js-train-count').forEach(function (el) {
      el.textContent = '0/' + tot0;
    });
  }

  // Searching needs every section open at once, which is exactly what the
  // exclusive `name` prevents — so drop it while a query is active.
  var search = panel.querySelector('input[type="search"]');
  if (!search) return;
  var groups = Array.prototype.slice.call(panel.querySelectorAll('.ns-sidenav__group'));
  search.addEventListener('input', function () {
    var searching = search.value.trim() !== '';
    groups.forEach(function (g) {
      if (searching) { g.removeAttribute('name'); g.open = true; }
      else { g.setAttribute('name', 'ns-training-nav'); g.open = g.dataset.sec === panel.dataset.cur; }
    });
  });
})();
