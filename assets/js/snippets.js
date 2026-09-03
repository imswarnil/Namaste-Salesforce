// snippets.js — the code-block upgrade, site-wide.
//
// Every Ghost code card (pre > code) becomes a small editor
// window: a header bar with the language name and a COPY button,
// Prism syntax colouring under our own token theme (_code.css).
// Loads after prism.js in the bundle; Prism.manual is set up
// front (animate.js), so aliases are remapped BEFORE the one
// explicit highlight pass. Apex rides the Java grammar, SOQL
// rides SQL.
(function () {
    var ALIASES = {
        apex: 'java',
        soql: 'sql',
        trigger: 'java',
        flow: 'markup',
        html: 'markup',
        hbs: 'markup',
        handlebars: 'markup',
        shell: 'bash',
        js: 'javascript'
    };

    function labelOf(code) {
        var match = (code.className || '').match(/language-([\w-]+)/);
        return match ? match[1] : '';
    }

    function init() {
        document.querySelectorAll('pre > code').forEach(function (code) {
            var pre = code.parentElement;
            if (pre.closest('.code-window')) return;

            var lang = labelOf(code);
            if (ALIASES[lang]) {
                code.classList.remove('language-' + lang);
                code.classList.add('language-' + ALIASES[lang]);
            }

            // the window: header (dots · language · copy) + the pre
            var win = document.createElement('figure');
            win.className = 'code-window';

            var bar = document.createElement('div');
            bar.className = 'code-window-bar';

            var dots = document.createElement('span');
            dots.className = 'code-window-dots';
            dots.innerHTML = '<i></i><i></i><i></i>';

            var label = document.createElement('span');
            label.className = 'code-window-lang';
            label.textContent = lang || 'code';

            var copy = document.createElement('button');
            copy.type = 'button';
            copy.className = 'code-copy';
            copy.textContent = 'Copy';
            copy.addEventListener('click', function () {
                var text = code.textContent;
                var done = function () {
                    copy.textContent = 'Copied!';
                    copy.classList.add('is-done');
                    setTimeout(function () {
                        copy.textContent = 'Copy';
                        copy.classList.remove('is-done');
                    }, 1600);
                };
                if (navigator.clipboard && navigator.clipboard.writeText) {
                    navigator.clipboard.writeText(text).then(done);
                } else {
                    var ta = document.createElement('textarea');
                    ta.value = text;
                    document.body.appendChild(ta);
                    ta.select();
                    try { document.execCommand('copy'); done(); } catch (e) { /* no-op */ }
                    ta.remove();
                }
            });

            bar.appendChild(dots);
            bar.appendChild(label);
            bar.appendChild(copy);

            pre.parentNode.insertBefore(win, pre);
            win.appendChild(bar);
            win.appendChild(pre);
        });

        if (window.Prism && window.Prism.highlightAll) {
            window.Prism.highlightAll();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
