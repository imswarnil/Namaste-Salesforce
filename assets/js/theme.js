// theme.js — the three-state theme switcher.
//
// States: no data-theme (follow system) → "light" → "dark". The
// toggle cycles light/dark and stores the choice; the inline
// script in default.hbs re-applies it before first paint. A
// stored choice matching the system preference is dropped back
// to "auto" so the site keeps following the OS from then on.
(function () {
    var KEY = 'ns-theme';
    var root = document.documentElement;
    var media = window.matchMedia('(prefers-color-scheme: dark)');

    function current() {
        return root.getAttribute('data-theme') || (media.matches ? 'dark' : 'light');
    }

    document.querySelectorAll('[data-theme-toggle]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            var next = current() === 'dark' ? 'light' : 'dark';
            var system = media.matches ? 'dark' : 'light';

            if (next === system) {
                root.removeAttribute('data-theme');
                localStorage.removeItem(KEY);
            } else {
                root.setAttribute('data-theme', next);
                localStorage.setItem(KEY, next);
            }
        });
    });

    // If the OS flips while a matching explicit choice is stored,
    // the stored value has become meaningless — let it go.
    media.addEventListener('change', function () {
        if (localStorage.getItem(KEY) === (media.matches ? 'dark' : 'light')) {
            root.removeAttribute('data-theme');
            localStorage.removeItem(KEY);
        }
    });
})();
