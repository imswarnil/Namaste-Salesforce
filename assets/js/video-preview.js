/* Card video previews — posts tagged #video-preview render their
   content into a <template data-video-preview> inside the card
   media (partials/video-preview.hbs). This script pulls the first
   playable embed out of each template, rewrites it into a muted
   autoplaying loop, and mounts it over the card thumbnail.

   YouTube: autoplay+mute+loop need the playlist param set to the
   video id, and controls/branding go. Vimeo has a dedicated
   background mode. Native video cards just get the attributes. */
(function () {
    'use strict';

    var PROVIDERS = ['youtube.com', 'youtube-nocookie.com', 'player.vimeo.com'];

    function firstPlayable(root) {
        var video = root.querySelector('.kg-video-card video, video');
        if (video) return video;

        var iframes = root.querySelectorAll('iframe');
        for (var i = 0; i < iframes.length; i++) {
            var src = iframes[i].getAttribute('src') || '';
            for (var j = 0; j < PROVIDERS.length; j++) {
                if (src.indexOf(PROVIDERS[j]) !== -1) return iframes[i];
            }
        }
        return null;
    }

    function tuneVideo(el) {
        el.setAttribute('loop', '');
        el.setAttribute('autoplay', '');
        el.setAttribute('playsinline', '');
        el.setAttribute('muted', '');
        el.muted = true;
        el.removeAttribute('controls');
    }

    function tuneYouTube(el) {
        var url = new URL(el.src, window.location.href);
        url.searchParams.set('autoplay', '1');
        url.searchParams.set('mute', '1');
        url.searchParams.set('loop', '1');
        url.searchParams.set('playlist', url.pathname.split('/').pop());
        url.searchParams.set('controls', '0');
        url.searchParams.set('modestbranding', '1');
        url.searchParams.set('rel', '0');
        el.src = url.toString();
    }

    function tuneVimeo(el) {
        var url = new URL(el.src, window.location.href);
        url.searchParams.set('autoplay', '1');
        url.searchParams.set('muted', '1');
        url.searchParams.set('loop', '1');
        url.searchParams.set('background', '1');
        el.src = url.toString();
    }

    function mount(template) {
        var media = template.parentElement;
        var el = firstPlayable(template.content);

        if (el) {
            var preview = el.cloneNode(true);
            try {
                if (preview.tagName === 'VIDEO') {
                    tuneVideo(preview);
                } else {
                    // the browser only honours autoplay inside an
                    // iframe that declares the permission
                    preview.setAttribute('allow', 'autoplay; encrypted-media; picture-in-picture');
                    if (/youtube\.com|youtube-nocookie\.com/.test(preview.src)) {
                        tuneYouTube(preview);
                    } else {
                        tuneVimeo(preview);
                    }
                }
                var wrap = document.createElement('div');
                wrap.className = 'card-video-preview';
                wrap.appendChild(preview);
                media.appendChild(wrap);
                media.classList.add('has-video-preview');
            } catch (e) {
                /* malformed src — leave the thumbnail alone */
            }
        }
        template.remove();
    }

    function init() {
        document.querySelectorAll('.card-media > template[data-video-preview]')
            .forEach(mount);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
