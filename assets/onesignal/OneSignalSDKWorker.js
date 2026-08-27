/* OneSignal web-push service worker.

   One line, and it must stay one line: OneSignal's SDK fetches this file and
   expects it to import their worker and nothing else.

   ⚠ IT MUST NOT JOIN THE main.min.js BUNDLE. gulpfile.mjs lists the bundled
   scripts explicitly rather than globbing, which is what keeps this file out
   — a service worker concatenated into a page script registers nothing and
   breaks the page script too.

   ⚠ THE URL IS PERMANENT ONCE SUBSCRIBERS EXIST. A browser ties a push
   subscription to the worker's scope and path; moving this file silently
   orphans every existing subscriber, and they are not re-prompted. See
   partials/services/onesignal.hbs for why it lives under /assets/ rather
   than at the site root, which is where OneSignal's default setup puts it
   and which a Ghost theme cannot serve. */
importScripts("https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.sw.js");
