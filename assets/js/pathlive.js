/*  pathlive.js — the sticky training-path rail.

    The rail reports where the reader is on the path: which module
    card is currently in front of them, and how far down the path
    that is. It is driven by an IntersectionObserver on the cards
    rather than by scroll position, because on a short viewport with
    tall cards those two are not the same thing — scroll percentage
    would say "60% down the section" while the reader is still
    looking at module two.

    The active card is whichever intersecting card is nearest the
    viewport's middle, so passing a boundary swaps cleanly instead of
    flickering between two cards that both qualify.

    Everything here is progressive: with no JS the rail still renders
    the full path, just without a position marker.

    ES5 on purpose — gulp-uglify 3 cannot parse newer syntax.       */

(function () {
    'use strict';

    var sections = document.querySelectorAll('[data-pathlive]');

    Array.prototype.forEach.call(sections, function (section) {
        var cards = section.querySelectorAll('[data-pl-card]');
        var items = section.querySelectorAll('[data-pl-item]');
        var fill = section.querySelector('[data-pl-fill]');
        var pct = section.querySelector('[data-pl-pct]');

        if (!cards.length || !items.length) {
            return;
        }

        var bySlug = {};
        Array.prototype.forEach.call(items, function (item) {
            bySlug[item.getAttribute('data-pl-item')] = item;
        });

        var visible = [];
        var activeSlug = null;

        function paint() {
            if (!visible.length) {
                return;
            }

            /* nearest the viewport's middle wins */
            var mid = window.innerHeight / 2;
            var best = null;
            var bestGap = Infinity;

            visible.forEach(function (card) {
                var box = card.getBoundingClientRect();
                var gap = Math.abs(box.top + box.height / 2 - mid);
                if (gap < bestGap) {
                    bestGap = gap;
                    best = card;
                }
            });

            if (!best) {
                return;
            }

            var slug = best.getAttribute('data-pl-slug');
            if (slug === activeSlug) {
                return;
            }
            activeSlug = slug;

            var index = Array.prototype.indexOf.call(cards, best);

            Array.prototype.forEach.call(items, function (item, i) {
                item.classList.toggle('is-active', i === index);
                item.classList.toggle('is-done', i < index);
            });

            /* the reader has reached this module, so it counts as
               covered — hence index + 1 over the total */
            var ratio = (index + 1) / cards.length;

            if (fill) {
                fill.style.width = (ratio * 100).toFixed(1) + '%';
            }
            if (pct) {
                pct.textContent = Math.round(ratio * 100);
            }
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                var at = visible.indexOf(entry.target);
                if (entry.isIntersecting && at === -1) {
                    visible.push(entry.target);
                } else if (!entry.isIntersecting && at !== -1) {
                    visible.splice(at, 1);
                }
            });
            paint();
        }, {threshold: 0});

        Array.prototype.forEach.call(cards, function (card) {
            observer.observe(card);
        });

        /* the middle-nearest test depends on scroll position, so it is
           re-run on scroll — cheaply, one rAF at a time */
        var queued = false;
        window.addEventListener('scroll', function () {
            if (queued) {
                return;
            }
            queued = true;
            requestAnimationFrame(function () {
                queued = false;
                paint();
            });
        }, {passive: true});

        /* clicking a rail entry jumps to its card */
        Array.prototype.forEach.call(items, function (item, i) {
            item.addEventListener('click', function () {
                if (cards[i]) {
                    cards[i].scrollIntoView({block: 'center', behavior: 'smooth'});
                }
            });
        });
    });
})();
