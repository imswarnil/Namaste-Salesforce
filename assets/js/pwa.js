/* ============================================================================
   pwa.js — service-worker registration + install prompt
   ----------------------------------------------------------------------------
   • Registers /assets/pwa/sw.js. Tries site-wide scope ('/') first — that
     needs a `Service-Worker-Allowed: /` response header on the sw file (set
     it at your proxy/CDN); otherwise falls back to the default /assets/
     scope so registration never hard-fails.
   • Custom install popup (components/pwa-install.hbs): shown ~4s after the
     browser says the site is installable, for first-time visitors; "Not now"
     snoozes it — it reappears on a visit 3+ days later. Never shows when
     already installed / running standalone.
   ========================================================================== */
(function () {
  'use strict';

  // ── service worker ───────────────────────────────────────────────────────
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/assets/pwa/sw.js', { scope: '/' })
        .catch(function () {
          // no Service-Worker-Allowed header → settle for the /assets/ scope
          return navigator.serviceWorker.register('/assets/pwa/sw.js');
        })
        .catch(function () { /* SW unsupported/blocked — never break the page */ });
    });
  }

  // ── install prompt ───────────────────────────────────────────────────────
  var KEY = 'ns-pwa-snooze';                 // timestamp of last dismissal
  var SNOOZE = 3 * 24 * 60 * 60 * 1000;      // 3 days
  var box = document.getElementById('ns-pwa-install');
  if (!box) return;

  // already running as an app → nothing to sell
  if (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) return;
  if (navigator.standalone) return; // iOS

  function snoozed() {
    try {
      var t = parseInt(localStorage.getItem(KEY), 10);
      return t && (Date.now() - t) < SNOOZE;
    } catch (e) { return false; }
  }
  function snooze() {
    try { localStorage.setItem(KEY, String(Date.now())); } catch (e) {}
    box.classList.add('hidden');
  }

  var deferred = null;

  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferred = e;
    if (snoozed()) return;
    setTimeout(function () { box.classList.remove('hidden'); }, 4000);
  });

  box.querySelectorAll('[data-pwa-dismiss]').forEach(function (b) {
    b.addEventListener('click', snooze);
  });

  var installBtn = box.querySelector('[data-pwa-install]');
  if (installBtn) {
    installBtn.addEventListener('click', function () {
      box.classList.add('hidden');
      if (!deferred) return;
      deferred.prompt();
      deferred.userChoice.then(function (choice) {
        if (choice && choice.outcome === 'accepted') {
          try { localStorage.setItem(KEY, String(Date.now() + 3650 * 864e5)); } catch (e) {}
        } else {
          snooze();
        }
        deferred = null;
      });
    });
  }

  window.addEventListener('appinstalled', function () {
    box.classList.add('hidden');
    try { localStorage.setItem(KEY, String(Date.now() + 3650 * 864e5)); } catch (e) {}
  });
})();
