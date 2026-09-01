// toc.js — table of contents for article bodies.
//
// Stamps ids on h2/h3 inside .gh-content, fills [data-toc] with
// the outline, highlights the section in view, and adds hover
// anchors to the headings. If the article has no headings, the
// TOC widget removes itself entirely.
(function () {
    var toc = document.querySelector('[data-toc]');
    var content = document.querySelector('.gh-content');
    if (!content) return;

    var headings = content.querySelectorAll('h2, h3');

    if (toc && !headings.length) {
        var wrap = toc.closest('[data-toc-wrap], .widget');
        (wrap || toc).remove();
        toc = null;
    }
    if (!headings.length) return;

    var used = {};
    var links = [];

    headings.forEach(function (h) {
        if (!h.id) {
            var slug = h.textContent.trim().toLowerCase()
                .replace(/[^\w\s-]/g, '').replace(/\s+/g, '-').slice(0, 64) || 'section';
            if (used[slug]) slug += '-' + (++used[slug]);
            else used[slug] = 1;
            h.id = slug;
        }

        var anchor = document.createElement('a');
        anchor.className = 'heading-anchor';
        anchor.href = '#' + h.id;
        anchor.setAttribute('aria-label', 'Link to this section');
        anchor.textContent = '#';
        h.appendChild(anchor);

        if (toc) {
            var li = document.createElement('li');
            li.className = 'toc-' + h.tagName.toLowerCase();
            var a = document.createElement('a');
            a.href = '#' + h.id;
            a.textContent = h.textContent.replace(/#$/, '').trim();
            li.appendChild(a);
            toc.appendChild(li);
            links.push(a);
        }
    });

    if (!toc) return;

    // Scroll-spy: the last heading above the fold owns the highlight.
    var active = null;
    function spy() {
        var line = window.scrollY + 120;
        var winner = null;
        headings.forEach(function (h) {
            if (h.offsetTop <= line) winner = h.id;
        });
        if (winner === active) return;
        active = winner;
        links.forEach(function (a) {
            a.classList.toggle('is-active', a.getAttribute('href') === '#' + winner);
        });
    }

    var ticking = false;
    window.addEventListener('scroll', function () {
        if (ticking) return;
        ticking = true;
        requestAnimationFrame(function () { spy(); ticking = false; });
    }, { passive: true });
    spy();
})();
