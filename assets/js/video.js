// video.js — chapter navigation for video posts.
//
// AUTHOR CONVENTION: put a table anywhere in the post whose FIRST
// column is timestamps (0:45, 12:30, 1:02:15) — a markdown card
// works fine. This script lifts it into the [data-chapters]
// sidebar, hides the original, and wires each entry to seek the
// page's YouTube embed. No table, no widget; non-YouTube embeds
// degrade to plain text chapters.
(function () {
    var list = document.querySelector('[data-chapters]');
    var content = document.querySelector('.gh-content');
    if (!list || !content) return;

    var STAMP = /^(\d{1,2}):(\d{2})(?::(\d{2}))?$/;

    function seconds(stamp) {
        var m = STAMP.exec(stamp.trim());
        if (!m) return null;
        return m[3] !== undefined
            ? (+m[1]) * 3600 + (+m[2]) * 60 + (+m[3])
            : (+m[1]) * 60 + (+m[2]);
    }

    // Find the first table whose data rows all lead with a timestamp
    var table = null;
    var rows = [];
    Array.prototype.some.call(content.querySelectorAll('table'), function (t) {
        var body = Array.prototype.filter.call(t.querySelectorAll('tr'), function (tr) {
            return tr.querySelector('td');
        });
        if (!body.length) return false;
        var parsed = body.map(function (tr) {
            var cells = tr.querySelectorAll('td');
            return {
                time: cells[0] ? cells[0].textContent.trim() : '',
                label: cells[1] ? cells[1].textContent.trim() : '',
                secs: cells[0] ? seconds(cells[0].textContent) : null
            };
        });
        if (parsed.every(function (r) { return r.secs !== null; })) {
            table = t;
            rows = parsed;
            return true;
        }
        return false;
    });
    if (!table) return;

    // The player. Seeking needs enablejsapi=1 in the iframe URL —
    // rewrite it once now, before anyone clicks.
    var iframe = content.querySelector('iframe[src*="youtube.com/embed/"], iframe[src*="youtube-nocookie.com/embed/"]');
    if (iframe && iframe.src.indexOf('enablejsapi=1') === -1) {
        iframe.src += (iframe.src.indexOf('?') === -1 ? '?' : '&') +
            'enablejsapi=1&origin=' + encodeURIComponent(window.location.origin);
    }

    function command(func, args) {
        if (!iframe) return;
        iframe.contentWindow.postMessage(JSON.stringify({
            event: 'command', func: func, args: args || []
        }), '*');
    }

    rows.forEach(function (row) {
        var li = document.createElement('li');
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'chapter-btn';
        btn.innerHTML = '<span class="chapter-time">' + row.time + '</span>' +
            '<span class="chapter-label"></span>';
        btn.querySelector('.chapter-label').textContent = row.label || row.time;
        btn.addEventListener('click', function () {
            command('seekTo', [row.secs, true]);
            command('playVideo');
            if (iframe) iframe.scrollIntoView({ behavior: 'smooth', block: 'center' });
        });
        li.appendChild(btn);
        list.appendChild(li);
    });

    // The table's job is done; the sidebar owns the chapters now.
    var card = table.closest('.kg-card') || table;
    card.style.display = 'none';

    var widget = list.closest('[data-chapters-widget]');
    if (widget) widget.hidden = false;
})();
