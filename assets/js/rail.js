// rail.js — collapse/expand for the reader rails (lesson player,
// training reader).
//
// State lives on the documentElement as data-rail="collapsed" and
// is stored per visitor, because the whole point of the player is
// clicking lesson to lesson: a collapse that reset on every
// navigation would be worse than no collapse at all. The inline
// script in default.hbs re-applies the stored value before first
// paint, so the rail never flashes open.
(function () {
    var KEY = 'ns-rail';
    var root = document.documentElement;

    var buttons = document.querySelectorAll('[data-rail-toggle]');
    if (!buttons.length) { return; }

    function collapsed() {
        return root.getAttribute('data-rail') === 'collapsed';
    }

    function label(btn) {
        var text = collapsed() ? btn.getAttribute('data-label-expand') : btn.getAttribute('data-label-collapse');
        if (!text) { return; }
        btn.setAttribute('aria-label', text);
        btn.setAttribute('title', text);
    }

    Array.prototype.forEach.call(buttons, function (btn) {
        // Stash both strings on first run: they are translated in
        // the template, so the script must not invent them.
        btn.setAttribute('data-label-collapse', btn.getAttribute('aria-label') || '');
        btn.setAttribute('data-label-expand', btn.getAttribute('data-expand-label') || btn.getAttribute('aria-label') || '');
        btn.setAttribute('aria-expanded', collapsed() ? 'false' : 'true');
        label(btn);

        btn.addEventListener('click', function () {
            var next = !collapsed();

            if (next) {
                root.setAttribute('data-rail', 'collapsed');
            } else {
                root.removeAttribute('data-rail');
            }

            try {
                if (next) { localStorage.setItem(KEY, 'collapsed'); }
                else { localStorage.removeItem(KEY); }
            } catch (e) { /* storage unavailable — this session only */ }

            Array.prototype.forEach.call(buttons, function (b) {
                b.setAttribute('aria-expanded', next ? 'false' : 'true');
                label(b);
            });
        });
    });
})();
