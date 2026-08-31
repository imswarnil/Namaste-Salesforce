/* ════════════════════════════════════════════════════════════════════════════
   lesson-progress.js — read state for training lessons, client-side.
   ----------------------------------------------------------------------------
   GHOST HAS NO PER-MEMBER READ STATE. There is no "has this member read this
   post" anywhere in the Content API, and no position-of-a-post-within-a-tag
   either. So the progress meters on the lesson player had nothing to fill them
   and were rendered at zero against a real maximum — honest, but not useful.

   This fills them from the reader's own browser. It is deliberately NOT an
   account feature: no request, no member required, works signed out, and it
   degrades to the zero state it replaced if scripting is off.

   ── WHAT COUNTS AS READ ──────────────────────────────────────────────────
   Reaching the END of the article body, not opening the page. A lesson marked
   read because it was clicked is a progress bar that lies, and the first time
   it does the reader stops trusting the number. The observer watches a
   sentinel at the foot of #post-body, so the trigger is "the last paragraph
   came into view".

   ── WHERE IT IS STORED ───────────────────────────────────────────────────
   One localStorage key, one JSON object of { "<lesson-path>": epoch-ms }. Keyed
   by PATH rather than post id because the rail only knows hrefs — it is
   rendered from Ghost and carries no ids — and the two have to agree for a
   row to be tickable.

   ⚠ EVERY READ IS GUARDED. localStorage throws in Safari private mode and
   when a browser blocks storage entirely; an unguarded read here would break
   the whole rail rather than just the ticks.
   ═══════════════════════════════════════════════════════════════════════ */
(function () {
    'use strict';

    var KEY = 'ns-lesson-read';

    function read() {
        try { return JSON.parse(localStorage.getItem(KEY)) || {}; }
        catch (e) { return {}; }
    }
    function write(map) {
        try { localStorage.setItem(KEY, JSON.stringify(map)); } catch (e) { /* storage blocked */ }
    }
    /* Trailing slash normalised: Ghost links carry one and location.pathname
       sometimes does not, and two spellings of one lesson is a tick that never
       lines up with the row it belongs to. */
    function norm(href) {
        try {
            var p = new URL(href, location.origin).pathname;
            return p.endsWith('/') ? p : p + '/';
        } catch (e) { return href; }
    }

    var rail = document.querySelector('[data-ns-trainingnav]');
    var body = document.getElementById('post-body');

    /* ── Paint the rail from stored state ─────────────────────────────────
       data-state="done" is upstream's own attribute on .ns-trainingnav__link,
       so ticking a row needs no new CSS — the design system already styles it. */
    function paint() {
        if (!rail) return;
        var map = read();

        rail.querySelectorAll('.ns-trainingnav__link').forEach(function (a) {
            var href = a.getAttribute('href');
            if (href && map[norm(href)]) a.setAttribute('data-state', 'done');
        });

        /* Each section's bar counts its OWN rows, so a section that gains a
           lesson recounts itself with no other change. The Overview row is
           excluded — it is the module page, not a lesson, and counting it
           would make every section report one more than its lesson count. */
        rail.querySelectorAll('.ns-trainingnav__section').forEach(function (sec) {
            var links = [].slice.call(sec.querySelectorAll('.ns-trainingnav__link'))
                .filter(function (a) { return a.querySelector('.ns-trainingnav__time'); });
            var done = links.filter(function (a) { return a.getAttribute('data-state') === 'done'; }).length;
            var bar = sec.querySelector('.ns-progress');
            if (!bar || !links.length) return;
            bar.value = done;
            bar.max = links.length;
            bar.setAttribute('aria-label', done + ' of ' + links.length + ' lessons read');
            if (done === links.length) sec.setAttribute('data-state', 'done');
        });

        /* The topbar meter mirrors whichever section is open — that is the one
           the reader is inside. */
        var openSec = rail.querySelector('.ns-trainingnav__section[open]');
        var topBar = document.querySelector('.ns-tbar__meter .ns-progress');
        var topCount = document.querySelector('.ns-tbar__count');
        if (openSec && topBar) {
            var src = openSec.querySelector('.ns-progress');
            if (src) {
                topBar.value = src.value;
                topBar.max = src.max;
                topBar.setAttribute('aria-label', src.getAttribute('aria-label'));
                if (topCount) topCount.textContent = src.value + ' / ' + src.max;
            }
        }
    }

    /* ── Mark this lesson read when its end comes into view ───────────────── */
    if (body && rail) {
        var sentinel = document.createElement('span');
        sentinel.setAttribute('aria-hidden', 'true');
        /* Not display:none — a hidden element never intersects, so the
           observer would never fire and nothing would ever be marked read. */
        sentinel.style.cssText = 'display:block;height:1px';
        body.appendChild(sentinel);

        var seen = false;
        var io = new IntersectionObserver(function (entries) {
            if (seen || !entries.some(function (e) { return e.isIntersecting; })) return;
            seen = true;
            io.disconnect();
            var map = read();
            map[norm(location.pathname)] = Date.now();
            write(map);
            paint();
        }, { rootMargin: '0px 0px -10% 0px' });
        io.observe(sentinel);
    }

    paint();
}());
