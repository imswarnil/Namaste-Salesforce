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

  var links = Array.prototype.slice.call(panel.querySelectorAll('.ns-trainingnav__link'));
  var current = panel.querySelector('.ns-trainingnav__link[aria-current="page"]');

  if (current) {
    for (var i = 0; i < links.length; i++) {
      if (links[i] === current) break;
      // The section OVERVIEW row is not a lesson, so it must not count. It is
      // the only row without a __time, which is what distinguishes it now that
      // the rail is NSDS's .ns-trainingnav.
      if (links[i].querySelector('.ns-trainingnav__time')) links[i].setAttribute('data-state', 'done');
    }
    var done = panel.querySelectorAll('.ns-trainingnav__link[data-state="done"]').length;
    var total = panel.querySelectorAll('.ns-trainingnav__time').length;
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
    var tot0 = panel.querySelectorAll('.ns-trainingnav__time').length;
    if (out0) out0.textContent = '0 / ' + tot0 + ' done';
    document.querySelectorAll('.js-train-count').forEach(function (el) {
      el.textContent = '0/' + tot0;
    });
  }

  // SEARCH. NSDS's modules are NOT an exclusive accordion — the system
  // deliberately does not `name` them, because closing the module you just
  // navigated out of loses your place. That removes the whole dance the theme
  // used to do here (drop `name` while querying, restore it after), so this is
  // now just: hide the rows that do not match, and hide a module with no
  // surviving rows.
  var search = panel.querySelector('input[type="search"]');
  if (!search) return;
  var modules = Array.prototype.slice.call(panel.querySelectorAll('.ns-trainingnav__module'));

  search.addEventListener('input', function () {
    var q = search.value.trim().toLowerCase();
    modules.forEach(function (m) {
      var any = false;
      m.querySelectorAll('.ns-trainingnav__link').forEach(function (a) {
        var hit = !q || (a.dataset.title || a.textContent).toLowerCase().indexOf(q) !== -1;
        a.hidden = !hit;
        if (hit) any = true;
      });
      m.hidden = !any;
      if (q && any) m.open = true;
    });
  });
})();
