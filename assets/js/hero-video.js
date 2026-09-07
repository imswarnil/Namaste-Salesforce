/*  hero-video.js — the hero square opens into the film.

    The card ships as a 1:1 publication cover. On the first press it
    morphs to 16:9 and an embed is BUILT AND INSERTED — one control
    handles both directions — before that press the page has
    requested nothing from YouTube, so a visitor who never plays
    the film never meets a third-party frame, script or cookie.
    Closing tears the iframe back out, which is also what stops
    playback: there is no player API to call, and none is loaded.

    The URL comes from the `hero_video` theme setting, so it is
    whatever the author pasted. Every YouTube address shape is
    accepted rather than asking them to hand-make an /embed/ one.

    ES5 on purpose — gulp-uglify 3 cannot parse newer syntax.     */

(function () {
    'use strict';

    var cards = document.querySelectorAll('[data-hero-video]');
    if (!cards.length) {
        return;
    }

    /*  Pull the eleven-character id out of any YouTube address:
        watch?v= · youtu.be/ · /embed/ · /shorts/ · /live/ · or a
        bare id already. Returns null for anything else, and the
        caller then leaves the poster alone rather than mounting a
        frame that would render as a YouTube error page. */
    function videoId(raw) {
        var url = String(raw || '').trim();
        if (!url) {
            return null;
        }

        if (/^[\w-]{11}$/.test(url)) {
            return url;
        }

        var patterns = [
            /[?&]v=([\w-]{11})/,
            /youtu\.be\/([\w-]{11})/,
            /\/embed\/([\w-]{11})/,
            /\/shorts\/([\w-]{11})/,
            /\/live\/([\w-]{11})/,
            /\/v\/([\w-]{11})/
        ];

        for (var i = 0; i < patterns.length; i++) {
            var hit = url.match(patterns[i]);
            if (hit) {
                return hit[1];
            }
        }
        return null;
    }

    /*  Carry a start time across if the pasted link had one —
        ?t=90, ?t=1m30s and ?start=90 all survive. */
    function startSeconds(raw) {
        var url = String(raw || '');
        var hit = url.match(/[?&](?:t|start)=([^&#]+)/);
        if (!hit) {
            return 0;
        }

        var value = hit[1];
        if (/^\d+$/.test(value)) {
            return parseInt(value, 10);
        }

        var clock = value.match(/^(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?$/);
        if (!clock) {
            return 0;
        }
        return (parseInt(clock[1] || 0, 10) * 3600) +
            (parseInt(clock[2] || 0, 10) * 60) +
            parseInt(clock[3] || 0, 10);
    }

    Array.prototype.forEach.call(cards, function (card) {
        var raw = card.getAttribute('data-hero-video');
        var id = videoId(raw);
        var stage = card.querySelector('[data-hero-stage]');
        var toggle = card.querySelector('[data-hero-toggle]');

        /*  An unparseable URL is an authoring mistake, not a visitor's
            problem: drop the play affordance so the card stays an
            honest brand square instead of offering a broken button. */
        if (!id || !stage || !toggle) {
            if (toggle) {
                toggle.parentNode.removeChild(toggle);
            }
            card.classList.remove('has-video');
            return;
        }

        var open = false;

        function mount() {
            if (open) {
                return;
            }
            open = true;

            var src = 'https://www.youtube-nocookie.com/embed/' + id +
                '?autoplay=1&rel=0&modestbranding=1&playsinline=1';

            var begin = startSeconds(raw);
            if (begin > 0) {
                src += '&start=' + begin;
            }

            var frame = document.createElement('iframe');
            frame.setAttribute('src', src);
            frame.setAttribute('title', document.title);
            frame.setAttribute('frameborder', '0');
            frame.setAttribute('allow',
                'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share');
            frame.setAttribute('allowfullscreen', 'allowfullscreen');
            stage.appendChild(frame);

            card.classList.add('is-playing');
            toggle.setAttribute('aria-expanded', 'true');
        }

        function unmount() {
            if (!open) {
                return;
            }
            open = false;

            /*  Removing the iframe IS the stop: no player API needed,
                and the browser releases the video and its network. */
            while (stage.firstChild) {
                stage.removeChild(stage.firstChild);
            }

            card.classList.remove('is-playing');
            toggle.setAttribute('aria-expanded', 'false');
            toggle.focus();
        }

        /*  One control, both directions — the button IS the state. */
        toggle.addEventListener('click', function () {
            if (open) {
                unmount();
            } else {
                mount();
            }
        });

        document.addEventListener('keydown', function (e) {
            if (open && (e.key === 'Escape' || e.key === 'Esc')) {
                unmount();
            }
        });
    });
})();

/*  hero-chips.js — the floating keyword chips.

    Labels arrive as one comma-separated attribute (Ghost custom
    settings are single text fields and Handlebars has no split), so
    the cutting up happens here — along with the two things that make
    the chips read well:

      · SHORT ONLY. Tag names include course titles like "Apex for
        Absolute Beginners", which is a sentence, not a keyword. Long
        labels are dropped rather than ellipsised.
      · AN ICON PER WORD, matched on the word itself. Anything with no
        match gets the neutral spark, so a new keyword never renders
        bare.

    If the site's own tags leave fewer than three usable keywords the
    AI-era defaults top it up, so the hero always reads as current
    instead of half-empty.

    Icons follow partials/icons/: 24-box, 1.8 stroke, currentColor.  */

(function () {
    'use strict';

    var MAX_LABEL = 14;
    var SLOTS = 5;

    var DEFAULTS = ['Agentforce', 'AI', 'Apex', 'Flow', 'LWC'];

    var PATHS = {
        spark: '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.3 6.3l2.8 2.8M14.9 14.9l2.8 2.8M17.7 6.3l-2.8 2.8M9.1 14.9l-2.8 2.8"/>',
        ai: '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M18 15l.8 2.2L21 18l-2.2.8L18 21l-.8-2.2L15 18l2.2-.8z"/>',
        code: '<path d="M9 18l-6-6 6-6M15 6l6 6-6 6"/>',
        flow: '<path d="M6 3v6a3 3 0 003 3h6a3 3 0 013 3v6"/><circle cx="6" cy="3" r="1.6"/><circle cx="18" cy="21" r="1.6"/>',
        layers: '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
        admin: '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M16.9 16.9l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/>',
        data: '<ellipse cx="12" cy="6" rx="8" ry="3"/><path d="M4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6"/><path d="M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6"/>',
        learn: '<path d="M12 4L2 9l10 5 10-5-10-5z"/><path d="M6 11.5V17c0 1.7 2.7 3 6 3s6-1.3 6-3v-5.5"/>',
        git: '<circle cx="6" cy="6" r="2.4"/><circle cx="6" cy="18" r="2.4"/><circle cx="18" cy="12" r="2.4"/><path d="M6 8.4v7.2M8.4 6H13a3 3 0 013 3v.6"/>'
    };

    /*  Matched longest-first so "data cloud" beats "data". */
    var MATCHERS = [
        [/agentforce|claude|copilot|\bai\b|einstein|prompt|agent/i, 'ai'],
        [/apex|code|snippet|develop|trigger/i, 'code'],
        [/flow|automat|process/i, 'flow'],
        [/lwc|component|lightning/i, 'layers'],
        [/admin|setup|config|permission/i, 'admin'],
        [/data|schema|model|integration/i, 'data'],
        [/devops|deploy|\bgit\b|ci\b/i, 'git'],
        [/learn|course|train|career|beginner|study/i, 'learn']
    ];

    function iconFor(label) {
        for (var i = 0; i < MATCHERS.length; i++) {
            if (MATCHERS[i][0].test(label)) {
                return PATHS[MATCHERS[i][1]];
            }
        }
        return PATHS.spark;
    }

    var lists = document.querySelectorAll('[data-hero-chips]');

    Array.prototype.forEach.call(lists, function (list) {
        /*  Typed labels ride the attribute; tag-derived ones ride a
            hidden span, because gscan rejects a block helper inside
            an HTML attribute value. */
        var src = list.querySelector('.hero-chips-src');
        var raw = src ? src.textContent : list.getAttribute('data-hero-chips');
        if (src) {
            src.parentNode.removeChild(src);
        }

        var seen = {};
        var labels = String(raw || '')
            .split(',')
            .map(function (part) { return part.trim(); })
            .filter(function (part) {
                if (!part || part.length > MAX_LABEL) {
                    return false;
                }
                var key = part.toLowerCase();
                if (seen[key]) {
                    return false;
                }
                seen[key] = true;
                return true;
            });

        /*  Top up rather than render a lopsided two-chip hero. */
        DEFAULTS.forEach(function (word) {
            if (labels.length >= 3 && labels.length >= SLOTS) {
                return;
            }
            if (!seen[word.toLowerCase()]) {
                seen[word.toLowerCase()] = true;
                labels.push(word);
            }
        });

        labels.slice(0, SLOTS).forEach(function (label, i) {
            var li = document.createElement('li');
            li.className = 'hero-chip is-c' + (i + 1);
            li.innerHTML =
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
                'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" ' +
                'aria-hidden="true">' + iconFor(label) + '</svg>';
            li.appendChild(document.createTextNode(label));
            list.appendChild(li);
        });
    });
})();
