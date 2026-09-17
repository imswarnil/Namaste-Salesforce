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
