// quote-fill.js — the word-by-word scroll fill on [data-word-fill]
// (partials/scroll-quote.hbs).
//
// The heavy lifting is CSS: a named view() timeline on the
// paragraph, and one animation per word taking its own slice of
// that timeline. All this script does is split the text into word
// spans and tell each one which slice it owns — work that cannot
// be done in Handlebars without breaking the string into
// untranslatable fragments.
//
// It bails out completely (leaving the server-rendered paragraph
// untouched, in full colour) when scroll-driven animations are
// unavailable or motion is unwelcome. That ordering matters: the
// CSS fill needs a faint "not yet inked" colour, so a browser that
// could paint the ghost state but not run the timeline would leave
// the quote permanently unreadable.

(function () {
    var nodes = document.querySelectorAll('[data-word-fill]');
    if (!nodes.length) { return; }

    var supported = window.CSS
        && typeof window.CSS.supports === 'function'
        && window.CSS.supports('animation-timeline', 'view()');
    if (!supported) { return; }

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { return; }

    // The fill runs across the middle of the band's pass through
    // the viewport: starting at the very edges reads as a glitch.
    var START = 25;
    var SPAN = 45;

    Array.prototype.forEach.call(nodes, function (el) {
        var words = (el.textContent || '').trim().split(/\s+/);
        if (words.length < 2) { return; }

        var step = SPAN / words.length;
        var frag = document.createDocumentFragment();

        words.forEach(function (word, i) {
            var span = document.createElement('span');
            span.className = 'rq-w';
            // Each word overlaps the next slightly, so the ink
            // flows rather than clicking through in stages.
            span.style.setProperty('--from', (START + i * step).toFixed(2) + '%');
            span.style.setProperty('--to', (START + (i + 1.6) * step).toFixed(2) + '%');
            span.textContent = word;
            frag.appendChild(span);
            if (i < words.length - 1) {
                frag.appendChild(document.createTextNode(' '));
            }
        });

        el.textContent = '';
        el.appendChild(frag);
        el.classList.add('is-split');
    });
})();
