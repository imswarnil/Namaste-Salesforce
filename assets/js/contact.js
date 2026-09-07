/*  contact.js — the contact page's composer.

    Ghost has no form backend, so the "form" never submits anywhere:
    it assembles a mailto: from the topic, the name and the message,
    and the send button hands that to the visitor's mail app with the
    subject and body already filled in. Nothing leaves the page from
    here and nothing is stored. Without JS the button is the plain
    mailto it was rendered as.

    ES5 on purpose — gulp-uglify 3 cannot parse newer syntax.        */

(function () {
    'use strict';

    var form = document.querySelector('[data-contact-form]');
    if (!form) {
        return;
    }

    var to = form.getAttribute('data-contact-to') || '';
    var topic = form.querySelector('[data-contact-topic]');
    var name = form.querySelector('[data-contact-name]');
    var message = form.querySelector('[data-contact-message]');
    var send = form.querySelector('[data-contact-send]');

    function build() {
        var subject = (topic && topic.value) ? topic.value : 'Hello';
        var who = (name && name.value.trim()) ? name.value.trim() : '';
        var body = (message && message.value.trim()) ? message.value.trim() : '';
        if (who) {
            body += (body ? '\n\n' : '') + '— ' + who;
        }
        return 'mailto:' + to +
            '?subject=' + encodeURIComponent(subject) +
            (body ? '&body=' + encodeURIComponent(body) : '');
    }

    function refresh() {
        if (send) {
            send.setAttribute('href', build());
        }
    }

    [topic, name, message].forEach(function (el) {
        if (el) {
            el.addEventListener('input', refresh);
            el.addEventListener('change', refresh);
        }
    });

    /* Enter in a single-line field would submit the form to nowhere */
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        refresh();
        if (send) {
            window.location.href = send.getAttribute('href');
        }
    });

    refresh();
})();
