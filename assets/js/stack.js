/*  stack.js — the Products-I-Use page, grouped by category.

    The page is written in the editor as plain sections: an h2 per
    category, then a line of copy and a bullet list of products.
    That is the right way to author it and the wrong way to read
    it, so this script re-shapes the rendered content, in place:

      · every h2 and everything after it up to the next h2 becomes
        one SHELF (a card with an icon matched to the category's
        name and a count of what is on it);
      · a bullet list under a shelf becomes a grid of product TILES.
        "**Name** — one honest line" is the shape a bullet is
        expected to take; a bare bullet still tiles, just untitled;
      · the category rail on the left is built from the same h2s,
        and lights the shelf currently in view.

    Nothing is added that the author did not write. Without JS the
    page renders exactly as the editor produced it.

    Icons follow partials/icons/: 24-box, 1.8 stroke, currentColor.
    ES5 on purpose — gulp-uglify 3 cannot parse newer syntax.        */

(function () {
    'use strict';

    var root = document.querySelector('[data-stack]');
    var content = root && root.querySelector('[data-stack-content]');
    var navList = root && root.querySelector('[data-stack-nav-list]');
    if (!content) {
        return;
    }

    var PATHS = {
        spark:    '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.3 6.3l2.8 2.8M14.9 14.9l2.8 2.8M17.7 6.3l-2.8 2.8M9.1 14.9l-2.8 2.8"/>',
        hardware: '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
        software: '<path d="M9 18l-6-6 6-6M15 6l6 6-6 6"/>',
        cloud:    '<path d="M7 18a4 4 0 01-.6-7.95A6 6 0 0118.4 9 4.5 4.5 0 0117 18H7z"/>',
        ai:       '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/>',
        video:    '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3z"/>',
        audio:    '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0014 0M12 18v3M9 21h6"/>',
        learn:    '<path d="M12 4L2 9l10 5 10-5-10-5z"/><path d="M6 11.5V17c0 1.7 2.7 3 6 3s6-1.3 6-3v-5.5"/>',
        book:     '<path d="M4 5a2 2 0 012-2h13v16H6a2 2 0 00-2 2V5z"/><path d="M4 19a2 2 0 012-2h13"/>'
    };

    var MATCHERS = [
        [/salesforce|org|cli|inspector|trail/i, 'cloud'],
        [/\bai\b|agentforce|claude|copilot|gpt|model/i, 'ai'],
        [/hardware|desk|laptop|mac|monitor|keyboard|mouse|gear/i, 'hardware'],
        [/camera|video|studio|light|stream|record/i, 'video'],
        [/mic|audio|sound|headphone/i, 'audio'],
        [/software|app|editor|terminal|tool|design/i, 'software'],
        [/learn|course|book|read/i, 'learn']
    ];

    function iconFor(label) {
        for (var i = 0; i < MATCHERS.length; i++) {
            if (MATCHERS[i][0].test(label)) {
                return PATHS[MATCHERS[i][1]];
            }
        }
        return PATHS.spark;
    }

    function svg(path, cls) {
        return '<svg class="' + (cls || '') + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + path + '</svg>';
    }

    function slugify(text) {
        return String(text).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    }

    /* ── 1. group the flat content into shelves ─────────────────────── */
    var nodes = Array.prototype.slice.call(content.childNodes);
    var shelves = [];
    var current = null;
    var intro = document.createDocumentFragment();

    nodes.forEach(function (node) {
        var isH2 = node.nodeType === 1 && node.tagName === 'H2';
        if (isH2) {
            current = {heading: node, body: []};
            shelves.push(current);
        } else if (current) {
            current.body.push(node);
        } else {
            intro.appendChild(node);
        }
    });

    if (!shelves.length) {
        return;
    }

    content.innerHTML = '';
    if (intro.childNodes.length) {
        var lead = document.createElement('div');
        lead.className = 'stack-intro';
        lead.appendChild(intro);
        content.appendChild(lead);
    }

    shelves.forEach(function (shelf, i) {
        var title = shelf.heading.textContent.trim();
        var id = shelf.heading.id || ('shelf-' + slugify(title));
        shelf.heading.id = id;

        var section = document.createElement('section');
        section.className = 'stack-shelf';
        section.id = id;
        section.setAttribute('data-stack-shelf', id);

        var head = document.createElement('header');
        head.className = 'stack-shelf-head';
        head.innerHTML = '<span class="stack-shelf-icon" aria-hidden="true">' + svg(iconFor(title)) + '</span>';
        shelf.heading.removeAttribute('id');
        shelf.heading.className = 'stack-shelf-title';
        head.appendChild(shelf.heading);

        var count = document.createElement('span');
        count.className = 'stack-shelf-count';
        head.appendChild(count);

        section.appendChild(head);

        var body = document.createElement('div');
        body.className = 'stack-shelf-body';
        var products = 0;

        shelf.body.forEach(function (node) {
            if (node.nodeType === 1 && (node.tagName === 'UL' || node.tagName === 'OL')) {
                /* ── 2. a list becomes product tiles ──────────────────── */
                var grid = document.createElement('ul');
                grid.className = 'stack-products';
                Array.prototype.forEach.call(node.querySelectorAll(':scope > li'), function (li) {
                    var tile = document.createElement('li');
                    tile.className = 'stack-product';

                    var strong = li.querySelector('strong, b, a');
                    var name = strong ? strong.textContent.trim() : '';
                    var link = li.querySelector('a');
                    var note = li.cloneNode(true);
                    if (strong && note.contains(note.querySelector('strong, b, a'))) {
                        var first = note.querySelector('strong, b, a');
                        first.parentNode.removeChild(first);
                    }
                    var noteText = note.textContent.replace(/^[\s—–:-]+/, '').trim();

                    var html = '';
                    if (name) {
                        html += link
                            ? '<a class="stack-product-name" href="' + link.getAttribute('href') + '" target="_blank" rel="noopener">' + name + '</a>'
                            : '<span class="stack-product-name">' + name + '</span>';
                    }
                    if (noteText) {
                        html += '<span class="stack-product-note">' + noteText + '</span>';
                    }
                    if (!html) {
                        html = '<span class="stack-product-name">' + li.textContent.trim() + '</span>';
                    }
                    tile.innerHTML = html;
                    grid.appendChild(tile);
                    products++;
                });
                body.appendChild(grid);
            } else {
                body.appendChild(node);
            }
        });

        count.textContent = products ? products + (products === 1 ? ' item' : ' items') : '';
        if (!products) {
            count.hidden = true;
        }

        section.appendChild(body);
        content.appendChild(section);

        /* ── 3. the rail ───────────────────────────────────────────── */
        if (navList) {
            var item = document.createElement('li');
            item.innerHTML = '<a href="#' + id + '" data-stack-link="' + id + '">' +
                svg(iconFor(title), 'stack-nav-icon') +
                '<span>' + title + '</span>' +
                (products ? '<b>' + products + '</b>' : '') + '</a>';
            navList.appendChild(item);
        }
    });

    /* light the shelf in view */
    if (navList && 'IntersectionObserver' in window) {
        var links = navList.querySelectorAll('[data-stack-link]');
        var visible = [];
        var paint = function () {
            if (!visible.length) {
                return;
            }
            var mid = window.innerHeight * 0.4;
            var best = null, gap = Infinity;
            visible.forEach(function (el) {
                var b = el.getBoundingClientRect();
                var d = Math.abs(b.top - mid);
                if (d < gap) { gap = d; best = el; }
            });
            var id = best && best.getAttribute('data-stack-shelf');
            Array.prototype.forEach.call(links, function (a) {
                a.classList.toggle('is-active', a.getAttribute('data-stack-link') === id);
            });
        };
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (e) {
                var at = visible.indexOf(e.target);
                if (e.isIntersecting && at === -1) { visible.push(e.target); }
                if (!e.isIntersecting && at !== -1) { visible.splice(at, 1); }
            });
            paint();
        }, {threshold: 0});
        Array.prototype.forEach.call(content.querySelectorAll('[data-stack-shelf]'), function (s) { io.observe(s); });
        window.addEventListener('scroll', function () { requestAnimationFrame(paint); }, {passive: true});
    }
})();
