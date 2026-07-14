/* ============================================================================
   sw.js — Namaste Salesforce service worker (offline support)
   ----------------------------------------------------------------------------
   Strategy:
   • install  — precache the app shell (home, compiled CSS/JS, icons)
   • navigate — network-first, falling back to the cached copy of that page,
                then the cached home page (so revisited pages read offline)
   • static   — stale-while-revalidate for same-origin assets
   NOTE: for site-wide scope the server must send
   `Service-Worker-Allowed: /` on this file (it lives under /assets/) — see
   pwa.js, which falls back to the /assets/ scope automatically.
   ========================================================================== */
'use strict';

var VERSION = 'ns-pwa-v1';
var CORE = [
  '/',
  '/assets/built/screen.css',
  '/assets/built/casper.js',
  '/assets/logo/icon-192.png',
  '/assets/logo/icon-512.png',
  '/assets/logo/favicon.svg'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(VERSION).then(function (c) { return c.addAll(CORE); }).then(function () {
      return self.skipWaiting();
    })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== VERSION; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET') return;
  var url = new URL(req.url);
  if (url.origin !== location.origin) return;           // let the CDN stuff pass through
  if (url.pathname.indexOf('/ghost/') === 0 ||          // never cache admin/api/member calls
      url.pathname.indexOf('/members/') === 0) return;

  if (req.mode === 'navigate') {
    // pages: network-first → cached page → cached home
    e.respondWith(
      fetch(req).then(function (res) {
        var copy = res.clone();
        caches.open(VERSION).then(function (c) { c.put(req, copy); });
        return res;
      }).catch(function () {
        return caches.match(req).then(function (hit) { return hit || caches.match('/'); });
      })
    );
    return;
  }

  // assets: stale-while-revalidate
  e.respondWith(
    caches.match(req).then(function (hit) {
      var net = fetch(req).then(function (res) {
        if (res && res.status === 200) {
          var copy = res.clone();
          caches.open(VERSION).then(function (c) { c.put(req, copy); });
        }
        return res;
      }).catch(function () { return hit; });
      return hit || net;
    })
  );
});
