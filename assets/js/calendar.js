// calendar.js — the sent calendar (widgets/sent-calendar.hbs).
//
// The widget ships a hidden list of issue dates; this builds a
// month grid around it: current month first, prev/next to walk
// between the earliest issue and today. Days with an issue become
// links with the title in a data-tip attribute — the tooltip
// itself is CSS (content: attr). Month and weekday names come
// from Intl, so the calendar follows the reader's locale.
// Without JS the widget stays hidden work; with no issues it
// removes itself.
(function () {
    document.querySelectorAll('[data-calendar]').forEach(function (widget) {
        var root = widget.querySelector('[data-cal-root]');
        var rows = widget.querySelectorAll('[data-cal-dates] [data-date]');

        if (!root || !rows.length) {
            widget.remove();
            return;
        }

        // date string "YYYY-MM-DD" → {title, url}
        var sent = {};
        var earliest = null;
        rows.forEach(function (row) {
            var d = row.getAttribute('data-date');
            sent[d] = {
                title: row.getAttribute('data-title') || '',
                url: row.getAttribute('data-url') || ''
            };
            if (!earliest || d < earliest) {
                earliest = d;
            }
        });

        var monthFmt = new Intl.DateTimeFormat(document.documentElement.lang || undefined,
            {month: 'long', year: 'numeric'});
        var dayFmt = new Intl.DateTimeFormat(document.documentElement.lang || undefined,
            {weekday: 'narrow'});

        var today = new Date();
        var view = new Date(today.getFullYear(), today.getMonth(), 1);
        var min = new Date(parseInt(earliest.slice(0, 4), 10),
            parseInt(earliest.slice(5, 7), 10) - 1, 1);
        var max = new Date(today.getFullYear(), today.getMonth(), 1);

        function iso(y, m, d) {
            return y + '-' + String(m + 1).padStart(2, '0') + '-' + String(d).padStart(2, '0');
        }

        function render() {
            var y = view.getFullYear();
            var m = view.getMonth();
            var first = new Date(y, m, 1);
            var days = new Date(y, m + 1, 0).getDate();
            var lead = (first.getDay() + 6) % 7; // Monday-start

            var head = document.createElement('div');
            head.className = 'cal-head';

            var prev = document.createElement('button');
            prev.type = 'button';
            prev.className = 'cal-nav';
            prev.textContent = '‹';
            prev.setAttribute('aria-label', 'Previous month');
            prev.disabled = view <= min;
            prev.addEventListener('click', function () {
                view = new Date(y, m - 1, 1);
                render();
            });

            var next = document.createElement('button');
            next.type = 'button';
            next.className = 'cal-nav';
            next.textContent = '›';
            next.setAttribute('aria-label', 'Next month');
            next.disabled = view >= max;
            next.addEventListener('click', function () {
                view = new Date(y, m + 1, 1);
                render();
            });

            var label = document.createElement('strong');
            label.className = 'cal-label';
            label.textContent = monthFmt.format(first);

            head.appendChild(prev);
            head.appendChild(label);
            head.appendChild(next);

            var grid = document.createElement('div');
            grid.className = 'cal-grid';

            // weekday header, Monday first (2024-01-01 was a Monday)
            for (var w = 0; w < 7; w++) {
                var wd = document.createElement('span');
                wd.className = 'cal-wd';
                wd.textContent = dayFmt.format(new Date(2024, 0, 1 + w));
                grid.appendChild(wd);
            }

            for (var b = 0; b < lead; b++) {
                grid.appendChild(document.createElement('span'));
            }

            for (var d = 1; d <= days; d++) {
                var key = iso(y, m, d);
                var issue = sent[key];
                var cell;
                if (issue) {
                    cell = document.createElement('a');
                    cell.href = issue.url;
                    cell.className = 'cal-day is-sent';
                    cell.setAttribute('data-tip', issue.title);
                    cell.setAttribute('aria-label', issue.title);
                } else {
                    cell = document.createElement('span');
                    cell.className = 'cal-day';
                }
                if (y === today.getFullYear() && m === today.getMonth() && d === today.getDate()) {
                    cell.classList.add('is-today');
                }
                cell.appendChild(document.createTextNode(d));
                grid.appendChild(cell);
            }

            root.textContent = '';
            root.appendChild(head);
            root.appendChild(grid);
        }

        render();
    });
})();
