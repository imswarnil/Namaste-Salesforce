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
// Prism (vendored later in the bundle) must not auto-run — the
// snippets script remaps language aliases first, then highlights.
window.Prism = window.Prism || {};
window.Prism.manual = true;

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

    /* Hero gravity + the web ------------------------------------
       The hub photo lifts away as you scroll and every orbiting
       window chases it on its own easing — heavier pieces lag
       behind (inertia). One thin line per screen ties the collage
       to the hub; the lines are redrawn every frame so the web
       stretches as the pieces drift apart. Desktop only; the whole
       system idles (no rAF) once the hero leaves the viewport. */

    var stack = document.querySelector('.hero-stack');
    var wideMq = window.matchMedia('(min-width: 992px)');

    if (stack && wideMq.matches) {
        var hub = stack.querySelector('.hero-hub');
        var web = stack.querySelector('.hero-web');
        var gravNodes = [];

        Array.prototype.forEach.call(
            stack.querySelectorAll('.hero-shot'),
            function (el, i) {
                gravNodes.push({
                    el: el,
                    speed: 0.16 + (i % 5) * 0.08,
                    ease: 0.05 + (i % 4) * 0.035,
                    drag: 1.8 + (i % 4) * 1.1,
                    cur: 0
                });
            }
        );

        var hubCur = 0;
        var lastY = window.scrollY || 0;
        var vel = 0;
        var webLines = [];

        if (web && hub) {
            var svgNS = 'http://www.w3.org/2000/svg';
            gravNodes.forEach(function (n) {
                var ln = document.createElementNS(svgNS, 'line');
                web.appendChild(ln);
                webLines.push({ln: ln, node: n});
            });
        }

        var heroRunning = false;

        var heroFrame = function () {
            if (!heroRunning) {
                return;
            }
            if (!wideMq.matches) {
                if (hub) {
                    hub.style.translate = '';
                }
                gravNodes.forEach(function (n) {
                    n.el.style.translate = '';
                });
                requestAnimationFrame(heroFrame);
                return;
            }

            var rawY = window.scrollY || window.pageYOffset || 0;

            // smoothed scroll velocity (px/frame): fast flicks add a
            // strong impulse, slow scrolling still reads clearly via
            // the position term below.
            vel += (rawY - lastY - vel) * 0.2;
            lastY = rawY;

            var y = Math.min(rawY, 1400);

            // the hub leads: over half of scroll speed, plus a
            // velocity kick so it visibly pulls away on fast flicks
            hubCur += (y * -0.6 - vel * 1.2 - hubCur) * 0.16;
            if (hub) {
                hub.style.translate = '-50% calc(-50% + ' + hubCur.toFixed(2) + 'px)';
            }

            // the windows trail: slower position ramp, and velocity
            // pushes them the OTHER way while you scroll — the web
            // stretches, then snaps back when you stop (inertia).
            gravNodes.forEach(function (n) {
                n.cur += (y * -n.speed + vel * n.drag - n.cur) * n.ease;
                n.el.style.translate = '0 ' + n.cur.toFixed(2) + 'px';
            });

            if (web && hub) {
                var sr = stack.getBoundingClientRect();
                var hr = hub.getBoundingClientRect();
                var hx = hr.left + hr.width / 2 - sr.left;
                var hy = hr.top + hr.height / 2 - sr.top;
                web.setAttribute('viewBox', '0 0 ' + sr.width + ' ' + sr.height);
                webLines.forEach(function (l) {
                    var r = l.node.el.getBoundingClientRect();
                    l.ln.setAttribute('x1', hx.toFixed(1));
                    l.ln.setAttribute('y1', hy.toFixed(1));
                    l.ln.setAttribute('x2', (r.left + r.width / 2 - sr.left).toFixed(1));
                    l.ln.setAttribute('y2', (r.top + r.height / 2 - sr.top).toFixed(1));
                });
            }

            requestAnimationFrame(heroFrame);
        };

        var heroGate = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting && !heroRunning) {
                    heroRunning = true;
                    requestAnimationFrame(heroFrame);
                } else if (!entry.isIntersecting) {
                    heroRunning = false;
                }
            });
        }, {rootMargin: '200px 0px'});
        heroGate.observe(stack);
    }

    /* The story timeline ------------------------------------------
       [data-story] scrolls sideways; the rail fill chases the
       reader's position and each stop lights up as the fill edge
       passes its node. */

    document.querySelectorAll('[data-story]').forEach(function (strip) {
        var fill = strip.querySelector('[data-story-fill]');
        var stops = strip.querySelectorAll('.story-stop');
        if (!fill) {
            return;
        }

        function paintStory() {
            var head = strip.scrollLeft + strip.clientWidth * 0.62;
            fill.style.width = Math.min(head, strip.scrollWidth) + 'px';
            Array.prototype.forEach.call(stops, function (stop) {
                stop.classList.toggle('is-lit', stop.offsetLeft + stop.offsetWidth * 0.4 < head);
            });
        }

        strip.addEventListener('scroll', function () {
            requestAnimationFrame(paintStory);
        }, {passive: true});
        window.addEventListener('resize', paintStory);
        paintStory();
    });

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
