// reader-video.js — promotes a video-typed reader page's embed into
// the hero.
//
// The author writes the lesson normally, with the video as the
// first card in the body. On a page tagged #lesson-type-video this
// lifts that card into [data-video-stage] at the top of the page
// and reveals the stage, so the player opens the page instead of
// sitting three paragraphs down.
//
// Named to sort before video.js in the concatenated bundle: that
// script wires the timestamp table to the player and has to find
// the iframe where this leaves it.
//
// Finds nothing -> does nothing, and the body keeps its video.
(function () {
    var stage = document.querySelector('[data-video-stage]');
    var content = document.querySelector('.gh-content');
    if (!stage || !content) { return; }

    // The whole embed card, not the bare iframe: Ghost wraps it in
    // sizing markup that the player needs.
    var iframe = content.querySelector(
        'iframe[src*="youtube.com/embed/"], iframe[src*="youtube-nocookie.com/embed/"], iframe[src*="player.vimeo.com"]'
    );
    if (!iframe) { return; }

    var card = iframe.closest('.kg-card') || iframe.closest('figure') || iframe;

    stage.appendChild(card);

    var hero = stage.closest('[data-video-hero]');
    if (hero) { hero.hidden = false; }
})();
