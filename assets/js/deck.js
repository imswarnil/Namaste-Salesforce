// deck.js — the slide deck player (post-slides.hbs), built on the
// NS Slides player grammar (the ../slides app in the monorepo):
//
//   · a slide is a FIXED logical canvas (1280×720) scaled with a
//     CSS transform to fit the stage — never reflowed, so every
//     coordinate means the same pixel on every screen
//   · the rail is a filmstrip: each slide CLONED into a miniature
//     at thumbnail scale — the same renderer at a smaller number
//   · click / → / Space forward, ← back, Home/End jump, a
//     progress bar, a counter, fullscreen for teaching
//
// The server renders the post's content as one normal article
// inside [data-deck-source]; every top-level <hr> (a divider card
// in the editor) ends a slide. Progressive enhancement: with JS
// off (or a single-slide post) the frame falls back to a normal
// scrolling article — this file is the only writer of `is-ready`,
// and CSS keeps ALL player chrome and canvas sizing behind it.
(function () {
    var CANVAS_W = 1280;
    var CANVAS_H = 720;

    var deck = document.querySelector('[data-deck]');
    if (!deck) {
        return;
    }

    var source = deck.querySelector('[data-deck-source]');
    var nav = deck.querySelector('[data-deck-nav]');
    var stage = deck.querySelector('[data-deck-stage]');
    var box = deck.querySelector('[data-deck-box]');
    var canvas = deck.querySelector('[data-deck-canvas]');
    if (!source || !nav || !stage || !box || !canvas) {
        return;
    }

    /* Split the article on <hr> into slide groups — only
       TOP-LEVEL hrs are separators. */
    var groups = [[]];
    Array.prototype.slice.call(source.childNodes).forEach(function (node) {
        if (node.nodeType === 1 && node.tagName === 'HR') {
            groups.push([]);
            return;
        }
        groups[groups.length - 1].push(node);
    });
    groups = groups.filter(function (g) {
        return g.some(function (n) {
            return n.nodeType === 1 || (n.textContent || '').trim();
        });
    });

    if (groups.length < 2) {
        return; // one slide is an article — leave it be
    }

    var slides = groups.map(function (group, i) {
        var section = document.createElement('section');
        // deck-surface carries the shared canvas look — the same
        // class dresses the filmstrip minis
        section.className = 'deck-slide deck-surface';
        section.id = 'slide-' + (i + 1);
        section.setAttribute('data-num', (i + 1) + ' / ' + groups.length);
        group.forEach(function (n) {
            section.appendChild(n);
        });
        // entry stagger: each child a beat behind the last
        Array.prototype.forEach.call(section.children, function (child, k) {
            child.style.setProperty('--i', k);
        });
        source.appendChild(section);
        return section;
    });

    /* The filmstrip: one mini per slide — the slide's own content
       cloned and scaled, exactly how NS Slides' scene rail works. */
    var minis = [];
    var buttons = slides.map(function (slide, i) {
        var li = document.createElement('li');
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'deck-nav-item';

        var head = slide.querySelector('h1, h2, h3, h4');
        btn.setAttribute('aria-label',
            (head ? head.textContent : 'Slide') + ' — ' + (i + 1) + ' / ' + slides.length);

        var mini = document.createElement('span');
        mini.className = 'deck-mini';
        mini.setAttribute('aria-hidden', 'true');
        var inner = slide.cloneNode(true);
        inner.className = 'deck-mini-inner deck-surface';
        inner.removeAttribute('id');
        Array.prototype.forEach.call(inner.querySelectorAll('[id]'), function (el) {
            el.removeAttribute('id');
        });
        // a thumbnail must stay cheap: embeds and players in the
        // clone would load (and play) again at 1/8 scale
        Array.prototype.forEach.call(
            inner.querySelectorAll('iframe, video, audio'),
            function (el) {
                var ph = document.createElement('span');
                ph.className = 'deck-mini-media';
                el.parentNode.replaceChild(ph, el);
            }
        );
        mini.appendChild(inner);

        var num = document.createElement('i');
        num.className = 'deck-nav-num';
        num.textContent = i + 1;

        btn.appendChild(num);
        btn.appendChild(mini);
        btn.addEventListener('click', function () {
            go(i);
        });
        li.appendChild(btn);
        nav.appendChild(li);
        minis.push({el: mini, inner: inner});
        return btn;
    });

    /* Fit-to-stage: the canvas keeps its logical size and only
       the transform changes — SlideView's maths, verbatim. */
    function fit() {
        var pad = 48;
        var w = Math.max(stage.clientWidth - pad, 120);
        var h = Math.max(stage.clientHeight - pad, 120);
        var scale = Math.min(w / CANVAS_W, h / CANVAS_H);
        box.style.width = (CANVAS_W * scale) + 'px';
        box.style.height = (CANVAS_H * scale) + 'px';
        canvas.style.transform = 'scale(' + scale + ')';

        minis.forEach(function (m) {
            var s = m.el.clientWidth / CANVAS_W;
            if (s > 0) {
                m.inner.style.transform = 'scale(' + s + ')';
            }
        });
    }

    if ('ResizeObserver' in window) {
        var ro = new ResizeObserver(fit);
        ro.observe(stage);
        if (minis[0]) {
            ro.observe(minis[0].el);
        }
    }
    window.addEventListener('resize', fit);
    document.addEventListener('fullscreenchange', fit);

    var counter = deck.querySelector('[data-deck-counter]');
    var progress = deck.querySelector('[data-deck-progress]');
    var current = 0;

    function go(i) {
        current = Math.max(0, Math.min(slides.length - 1, i));
        slides.forEach(function (s, k) {
            s.classList.toggle('is-current', k === current);
        });
        buttons.forEach(function (b, k) {
            b.classList.toggle('is-current', k === current);
            b.setAttribute('aria-current', k === current ? 'true' : 'false');
        });
        // keep the current mini in view — scroll ONLY the rail
        // (scrollIntoView would drag the whole page along)
        var railEl = deck.querySelector('[data-deck-rail]');
        var li = buttons[current] && buttons[current].parentElement;
        if (railEl && li) {
            if (li.offsetTop < railEl.scrollTop) {
                railEl.scrollTop = li.offsetTop - 12;
            } else if (li.offsetTop + li.offsetHeight > railEl.scrollTop + railEl.clientHeight) {
                railEl.scrollTop = li.offsetTop + li.offsetHeight - railEl.clientHeight + 12;
            }
            if (li.offsetLeft < railEl.scrollLeft) {
                railEl.scrollLeft = li.offsetLeft - 12;
            } else if (li.offsetLeft + li.offsetWidth > railEl.scrollLeft + railEl.clientWidth) {
                railEl.scrollLeft = li.offsetLeft + li.offsetWidth - railEl.clientWidth + 12;
            }
        }
        if (counter) {
            counter.textContent = (current + 1) + ' / ' + slides.length;
        }
        if (progress) {
            progress.style.width = ((current + 1) / slides.length * 100) + '%';
        }
        // remember the slide in the URL without scrolling the page
        if (history.replaceState) {
            history.replaceState(null, '', '#slide-' + (current + 1));
        }
    }

    var prev = deck.querySelector('[data-deck-prev]');
    var next = deck.querySelector('[data-deck-next]');
    if (prev) {
        prev.addEventListener('click', function () {
            go(current - 1);
        });
    }
    if (next) {
        next.addEventListener('click', function () {
            go(current + 1);
        });
    }

    // click on the stage advances — presentation-remote behaviour;
    // links inside a slide, and text selection, still win
    stage.addEventListener('click', function (e) {
        if (e.target.closest('a, button, video, audio, iframe, summary, input')) {
            return;
        }
        var sel = window.getSelection();
        if (sel && sel.type === 'Range') {
            return;
        }
        go(current + 1);
    });

    document.addEventListener('keydown', function (e) {
        var tag = (document.activeElement || {}).tagName || '';
        if (/^(INPUT|TEXTAREA|SELECT)$/.test(tag) || e.metaKey || e.ctrlKey || e.altKey) {
            return;
        }
        // Space on a focused button belongs to the button
        if (e.key === ' ' && tag === 'BUTTON') {
            return;
        }
        // → / ↓ / Space / PageDown forward · ← / ↑ / PageUp back
        // ('Right'/'Down'/… are legacy/synthesized aliases)
        if (e.key === 'ArrowRight' || e.key === 'Right'
            || e.key === 'ArrowDown' || e.key === 'Down'
            || e.key === 'PageDown' || e.key === ' ' || e.key === 'Spacebar') {
            e.preventDefault();
            go(current + 1);
        } else if (e.key === 'ArrowLeft' || e.key === 'Left'
            || e.key === 'ArrowUp' || e.key === 'Up' || e.key === 'PageUp') {
            e.preventDefault();
            go(current - 1);
        } else if (e.key === 'Home') {
            e.preventDefault();
            go(0);
        } else if (e.key === 'End') {
            e.preventDefault();
            go(slides.length - 1);
        } else if (e.key === 'Escape' && !document.fullscreenElement) {
            // fullscreen Esc is the browser's; bare Esc closes
            // the deck — same door as the topbar's ✕
            var close = deck.querySelector('[data-deck-close]');
            if (close) {
                location.href = close.href;
            }
        }
    });

    // fold the filmstrip away / bring it back
    var railToggle = deck.querySelector('[data-deck-rail-toggle]');
    if (railToggle) {
        railToggle.addEventListener('click', function () {
            var hidden = deck.classList.toggle('is-rail-hidden');
            railToggle.setAttribute('aria-pressed', hidden ? 'false' : 'true');
            fit();
        });
    }

    /* Fullscreen carries the WHOLE frame (topbar + filmstrip) so
       the presenter keeps the controls; Esc exits natively.
       Hidden where unsupported. */
    var full = deck.querySelector('[data-deck-full]');
    if (full) {
        if (deck.requestFullscreen) {
            full.addEventListener('click', function () {
                if (document.fullscreenElement) {
                    document.exitFullscreen();
                } else {
                    deck.requestFullscreen();
                }
            });
        } else {
            full.hidden = true;
        }
    }

    var controls = deck.querySelector('[data-deck-controls]');
    if (controls) {
        controls.hidden = false;
    }
    var rail = deck.querySelector('[data-deck-rail]');
    if (rail) {
        rail.hidden = false;
    }

    deck.classList.add('is-ready');

    // keyboard first: focus the frame so ← / → land immediately,
    // and take it back whenever fullscreen flips or Portal's
    // iframe steals it
    deck.setAttribute('tabindex', '-1');
    deck.focus({preventScroll: true});
    document.addEventListener('fullscreenchange', function () {
        deck.focus({preventScroll: true});
    });

    // arrive on the slide the URL names, if any
    var m = /^#slide-(\d+)$/.exec(location.hash);
    go(m ? parseInt(m[1], 10) - 1 : 0);
    fit();
})();
