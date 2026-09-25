// quote-fill.js — the word-by-word scroll fill on [data-word-fill]
// (partials/scroll-quote.hbs).
//
// The paragraph is split into word spans and each word inks in —
// colour, weight of blur, a small rise — as the band crosses the
// viewport. Progress is computed here on scroll (one passive
// listener, one rAF) rather than with CSS scroll-driven animations,
// which Safari still lacks: the same motion everywhere, or, with
// motion unwelcome, the paragraph stays exactly as Ghost rendered
// it, in full colour.
(function () {
    var nodes = document.querySelectorAll('[data-word-fill]');
    if (!nodes.length) { return; }
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { return; }

    var items = [];
    Array.prototype.forEach.call(nodes, function (el) {
        var words = (el.textContent || '').trim().split(/\s+/);
        if (words.length < 2) { return; }
        var frag = document.createDocumentFragment();
        var spans = [];
        words.forEach(function (word, i) {
            var span = document.createElement('span');
            span.className = 'rq-w';
            span.style.setProperty('--w', i);
            span.textContent = word;
            frag.appendChild(span);
            spans.push(span);
            if (i < words.length - 1) { frag.appendChild(document.createTextNode(' ')); }
        });
        el.textContent = '';
        el.appendChild(frag);
        el.classList.add('is-split');
        items.push({ el: el, band: el.closest('.scroll-quote') || el, spans: spans, lit: -1 });
    });
    if (!items.length) { return; }

    // The fill runs while the band travels from 80% down the
    // viewport to 30%: starting at the very edges reads as a glitch.
    var START = 0.8, END = 0.3;
    var ticking = false;

    function update() {
        ticking = false;
        var vh = window.innerHeight || 1;
        items.forEach(function (it) {
            var r = it.band.getBoundingClientRect();
            // position of the band's centre as a fraction of the viewport
            var centre = (r.top + r.height / 2) / vh;
            var p = (START - centre) / (START - END);
            p = Math.max(0, Math.min(1, p));
            var n = it.spans.length;
            var lit = Math.round(p * n);
            if (lit === it.lit) { return; }
            it.lit = lit;
            it.spans.forEach(function (s, i) { s.classList.toggle('is-on', i < lit); });
            it.el.style.setProperty('--p', p.toFixed(3));
        });
    }

    function onScroll() {
        if (!ticking) { ticking = true; requestAnimationFrame(update); }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    update();
})();
