// animate.js — scroll choreography for the homepage (and anything
// else that opts in with data-animate).
//
// Four systems, all opt-in via data attributes so templates stay
// declarative:
//
//   data-animate            reveal on scroll (fade/slide, CSS-driven)
//   data-animate-stagger    reveal children with a per-child delay
//   data-count              count a stat up from 0 when it enters
//   data-draw               an SVG path that draws itself as its
//                           section scrolls through the viewport
//   data-parallax="0.08"    drifts with scroll at the given speed
//
// The initial hidden state only exists under `html.anim`, which the
// inline head script sets ONLY when the visitor allows motion — so
// with JS off, reduced motion on, or a failed script load nothing is
// ever hidden. This file is the only writer of `.is-in`.
(function () {
    var root = document.documentElement;
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');

    if (reduce.matches || !('IntersectionObserver' in window)) {
        root.classList.remove('anim');
        return;
    }
    root.classList.add('anim');

    /* Reveal on scroll ------------------------------------------- */

    var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-in');
                io.unobserve(entry.target);
            }
        });
    }, {rootMargin: '0px 0px -8% 0px', threshold: 0.05});

    document.querySelectorAll('[data-animate]').forEach(function (el) {
        io.observe(el);
    });

    // Stagger containers: each child gets its index as --i, the CSS
    // turns that into a transition-delay. The container is observed,
    // not the children, so a row lands as one choreographed wave.
    document.querySelectorAll('[data-animate-stagger]').forEach(function (group) {
        Array.prototype.forEach.call(group.children, function (child, i) {
            child.style.setProperty('--i', i);
        });
        io.observe(group);
    });

    /* Stat count-up ---------------------------------------------- */

    var easeOut = function (t) {
        return 1 - Math.pow(1 - t, 3);
    };

    var counters = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (!entry.isIntersecting) {
                return;
            }
            counters.unobserve(entry.target);

            var el = entry.target;
            var target = parseInt(el.getAttribute('data-count') || el.textContent, 10);
            if (isNaN(target)) {
                return;
            }
            var start = null;
            var duration = 1400;

            function tick(now) {
                if (start === null) {
                    start = now;
                }
                var p = Math.min((now - start) / duration, 1);
                el.textContent = Math.round(easeOut(p) * target);
                if (p < 1) {
                    requestAnimationFrame(tick);
                }
            }
            requestAnimationFrame(tick);
        });
    }, {threshold: 0.6});

    document.querySelectorAll('[data-count]').forEach(function (el) {
        counters.observe(el);
    });

    /* Scroll-linked work: path drawing + parallax ----------------
       One passive scroll listener, one rAF — never more. */

    var drawn = [];
    document.querySelectorAll('svg [data-draw]').forEach(function (path) {
        var len = path.getTotalLength();
        path.style.strokeDasharray = len + ' ' + len;
        path.style.strokeDashoffset = len;
        drawn.push({path: path, len: len});
    });

    var floaters = [];
    document.querySelectorAll('[data-parallax]').forEach(function (el) {
        var speed = parseFloat(el.getAttribute('data-parallax'));
        if (!isNaN(speed)) {
            floaters.push({el: el, speed: speed});
        }
    });

    /* Pointer tilt — [data-tilt] leans its .card toward the cursor.
       CSS reads the --rx/--ry vars; fine pointers only. */
    if (window.matchMedia('(pointer: fine)').matches) {
        document.querySelectorAll('[data-tilt]').forEach(function (panel) {
            panel.addEventListener('mousemove', function (e) {
                var rect = panel.getBoundingClientRect();
                var x = (e.clientX - rect.left) / rect.width - 0.5;
                var y = (e.clientY - rect.top) / rect.height - 0.5;
                panel.style.setProperty('--ry', (x * 6).toFixed(2) + 'deg');
                panel.style.setProperty('--rx', (-y * 6).toFixed(2) + 'deg');
            });
            panel.addEventListener('mouseleave', function () {
                panel.style.setProperty('--rx', '0deg');
                panel.style.setProperty('--ry', '0deg');
            });
        });
    }

    if (!drawn.length && !floaters.length) {
        return;
    }

    var ticking = false;

    function update() {
        ticking = false;
        var vh = window.innerHeight;

        drawn.forEach(function (d) {
            var rect = d.path.ownerSVGElement.getBoundingClientRect();
            // 0 when the svg's top reaches the lower third of the
            // viewport, 1 when its bottom clears the upper third —
            // the line's tip roughly tracks the reader's eye.
            var p = (vh * 0.72 - rect.top) / (rect.height + vh * 0.2);
            p = Math.max(0, Math.min(1, p));
            d.path.style.strokeDashoffset = d.len * (1 - p);
        });

        floaters.forEach(function (f) {
            var rect = f.el.getBoundingClientRect();
            var fromCenter = rect.top + rect.height / 2 - vh / 2;
            f.el.style.transform = 'translateY(' + (-fromCenter * f.speed).toFixed(1) + 'px)';
        });
    }

    function onScroll() {
        if (!ticking) {
            ticking = true;
            requestAnimationFrame(update);
        }
    }

    window.addEventListener('scroll', onScroll, {passive: true});
    window.addEventListener('resize', onScroll);
    update();
})();
