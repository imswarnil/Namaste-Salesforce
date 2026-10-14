// trail.js — the training trail arrives on load (training.hbs,
// partials/training-trail.hbs), choreographed with anime.js
// (vendored as assets/js/anime.js, concatenated ahead of this
// file).
//
// Every module is a Salesforce-style window on the rail. The
// windows in the first viewport play as one timeline the moment
// the page is ready — window rises, app bar slides in, tabs fade,
// the rows of the related list cascade, the waypoint on the rail
// pops — and every window further down plays the same timeline
// when it scrolls into view. The hidden starting state lives in
// CSS behind `html.anim` AND `[data-trail]` (the attribute this
// script owns), so with JS off, reduced motion on, or anime.js
// missing nothing is ever hidden: the attribute is removed and the
// trail simply shows.
(function () {
    var trail = document.querySelector('[data-trail]');
    if (!trail) {
        return;
    }

    var root = document.documentElement;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    var modules = Array.prototype.slice.call(trail.querySelectorAll('[data-trail-module]'));

    function showAll() {
        trail.removeAttribute('data-trail');
        modules.forEach(function (m) {
            m.classList.add('is-in');
        });
    }

    if (!window.anime || reduce.matches || !root.classList.contains('anim')
        || !('IntersectionObserver' in window)) {
        showAll();
        return;
    }

    var anime = window.anime;

    function play(mod, delay) {
        if (mod.getAttribute('data-played')) {
            return;
        }
        mod.setAttribute('data-played', '1');

        var bar = mod.querySelector('[data-trail-bar]');
        var tabs = mod.querySelectorAll('[data-trail-tabs] > *');
        var head = mod.querySelector('[data-trail-head]');
        var rows = mod.querySelectorAll('[data-trail-row]');
        var node = mod.querySelector('.trail-node');

        var tl = anime.timeline({
            easing: 'easeOutExpo',
            delay: delay || 0
        });

        tl.add({
            targets: mod,
            opacity: [0, 1],
            translateY: [36, 0],
            scale: [0.985, 1],
            duration: 620,
            begin: function () {
                mod.classList.add('is-playing');
            },
            complete: function () {
                mod.classList.add('is-in');
                // hand the element back to CSS (hover lifts etc.)
                mod.style.transform = '';
                mod.style.opacity = '';
                mod.classList.remove('is-playing');
            }
        });

        if (bar) {
            tl.add({
                targets: bar,
                translateX: [-24, 0],
                opacity: [0, 1],
                duration: 460
            }, '-=420');
        }

        if (tabs.length) {
            tl.add({
                targets: tabs,
                opacity: [0, 1],
                translateY: [8, 0],
                duration: 360,
                delay: anime.stagger(60)
            }, '-=320');
        }

        if (head) {
            tl.add({
                targets: head,
                opacity: [0, 1],
                translateY: [12, 0],
                duration: 420
            }, '-=300');
        }

        if (rows.length) {
            tl.add({
                targets: rows,
                opacity: [0, 1],
                translateX: [-14, 0],
                duration: 380,
                delay: anime.stagger(45)
            }, '-=300');
        }

        if (node) {
            tl.add({
                targets: node,
                scale: [0.4, 1],
                opacity: [0, 1],
                duration: 520,
                easing: 'easeOutElastic(1, .6)'
            }, '-=' + Math.min(600, 200 + rows.length * 45));
        }
    }

    // Windows already on screen play as one sequence on load; the
    // rest wait for the reader.
    var vh = window.innerHeight;
    var above = [];
    var below = [];
    modules.forEach(function (m) {
        var r = m.getBoundingClientRect();
        (r.top < vh * 0.9 ? above : below).push(m);
    });

    // Set the hidden state in JS, not CSS, for every child the
    // timeline moves — so a module that never plays (observer never
    // fires) is still readable once showAll-style fallback kicks in.
    modules.forEach(function (m) {
        m.querySelectorAll('[data-trail-bar], [data-trail-tabs] > *, [data-trail-head], [data-trail-row], .trail-node').forEach(function (el) {
            el.style.opacity = '0';
        });
    });

    above.forEach(function (m, i) {
        play(m, 120 + i * 180);
    });

    var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                play(entry.target, 0);
                io.unobserve(entry.target);
            }
        });
    }, {rootMargin: '0px 0px -10% 0px', threshold: 0.05});

    below.forEach(function (m) {
        io.observe(m);
    });

    // Safety: whatever happens, nothing stays hidden for long.
    setTimeout(function () {
        modules.forEach(function (m) {
            if (!m.getAttribute('data-played')) {
                m.querySelectorAll('[style]').forEach(function (el) {
                    el.style.opacity = '';
                });
                m.style.opacity = '';
                m.classList.add('is-in');
            }
        });
        trail.removeAttribute('data-trail');
    }, 6000);
})();
