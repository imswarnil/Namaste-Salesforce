// changelog.js — on /changelog/{slug}/ the whole changelog renders
// again with that one card open in place (post-changelog.hbs).
// Nothing is fetched; the only job here is to bring the open card
// into view once the document (and its view transition) has
// landed, so the reader is looking at the notes and not at the top
// of the list. The card's scroll-margin keeps it clear of the
// header. With JS off the card is simply further down the page.
(function () {
    var open = document.querySelector('.changelog-entry.is-open');
    if (!open || location.hash) {
        return;
    }
    var jump = function () {
        open.scrollIntoView({block: 'start', behavior: 'auto'});
    };
    // after a cross-document view transition the browser restores
    // scroll first; pageshow is the safe moment on both paths
    if (document.readyState === 'complete') {
        jump();
    } else {
        window.addEventListener('pageshow', jump, {once: true});
    }
})();
