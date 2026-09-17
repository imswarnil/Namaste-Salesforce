// share.js — the "Copy link" button in widgets/share-links.hbs.
// Delegated on the document, so it works for every share row on
// the page (the boxed sidebar widget AND the bare post-footer row)
// without a per-instance listener.
(function () {
    document.addEventListener('click', function (event) {
        var btn = event.target.closest('[data-copy-link]');
        if (!btn) return;

        var url = btn.getAttribute('data-copy-link') || window.location.href;
        var done = function () {
            // Icon-only button — the "Copied!" state is a CSS class
            // (_widgets.css swaps the icon and the border colour),
            // never a textContent write that would blank the SVG.
            btn.classList.add('is-done');
            setTimeout(function () {
                btn.classList.remove('is-done');
            }, 1600);
        };
        var fallback = function () {
            var ta = document.createElement('textarea');
            ta.value = url;
            ta.style.position = 'fixed';
            ta.style.opacity = '0';
            document.body.appendChild(ta);
            ta.select();
            try { document.execCommand('copy'); done(); } catch (e) { /* no-op */ }
            ta.remove();
        };

        // A permissions policy can silently reject writeText (no
        // user gesture as far as the browser is concerned, an
        // iframe without clipboard-write, …) — always land on the
        // execCommand fallback rather than leaving the click inert.
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(url).then(done, fallback);
        } else {
            fallback();
        }
    });
})();
