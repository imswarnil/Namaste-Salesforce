// filters.js — card-facet filtering (/courses toolbar, /resources
// sidebar).
//
// The theme cannot query internal tags ({{#get "tags"}} is served
// by Ghost's TagPublic model), so the controls build themselves
// from the cards: each card carries data-{facet} (the internal
// tag slug) and data-{facet}-label (the tag's description).
// Unique values become buttons; a facet with fewer than two
// values stays hidden — a filter that can't change anything is
// noise. The bar declares its facets in data-filter-facets
// (comma-separated; defaults to the courses pair).
(function () {
    var bar = document.querySelector('[data-filter-bar]');
    if (!bar) return;

    var cards = Array.prototype.slice.call(document.querySelectorAll('[data-filter-item]'));
    var empty = document.querySelector('[data-filter-empty]');
    var active = {}; // facet → value

    var facets = (bar.getAttribute('data-filter-facets') || 'level,duration').split(',');

    var anyGroup = false;
    facets.forEach(function (facet) {
        var group = bar.querySelector('[data-filter-group="' + facet + '"]');
        if (!group) return;

        var seen = {};
        var options = [];
        cards.forEach(function (card) {
            var value = card.getAttribute('data-' + facet);
            if (value && !seen[value]) {
                seen[value] = true;
                options.push({
                    value: value,
                    label: card.getAttribute('data-' + facet + '-label') || value
                });
            }
        });

        if (options.length < 2) return;
        options.sort(function (a, b) { return a.label.localeCompare(b.label); });

        options.forEach(function (option) {
            var btn = document.createElement('button');
            btn.className = 'filter-btn';
            btn.setAttribute('data-filter', facet);
            btn.setAttribute('data-value', option.value);
            btn.textContent = option.label;
            group.appendChild(btn);
        });

        group.hidden = false;
        anyGroup = true;
    });

    if (!anyGroup) return;
    bar.hidden = false;

    function apply() {
        var shown = 0;
        cards.forEach(function (card) {
            var visible = Object.keys(active).every(function (facet) {
                return card.getAttribute('data-' + facet) === active[facet];
            });
            card.classList.toggle('is-filter-hidden', !visible);
            if (visible) shown++;
        });
        if (empty) empty.style.display = shown ? 'none' : 'block';
        bar.classList.toggle('has-active', Object.keys(active).length > 0);
    }

    bar.addEventListener('click', function (event) {
        var btn = event.target.closest('[data-filter]');
        if (btn) {
            var facet = btn.getAttribute('data-filter');
            var value = btn.getAttribute('data-value');
            var isActive = active[facet] === value;

            bar.querySelectorAll('[data-filter="' + facet + '"]').forEach(function (b) {
                b.classList.remove('is-active');
            });

            if (isActive) {
                delete active[facet];
            } else {
                active[facet] = value;
                btn.classList.add('is-active');
            }
            apply();
        }

        if (event.target.closest('[data-filter-clear]')) {
            active = {};
            bar.querySelectorAll('.is-active').forEach(function (b) {
                b.classList.remove('is-active');
            });
            apply();
        }
    });
})();
