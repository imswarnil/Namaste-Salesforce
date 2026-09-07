/*  drawer.js — manners for the mobile drawer.

    The drawer itself is pure CSS (a checkbox, #nav-open, and sibling
    selectors — see 2-layout/_header.css). CSS cannot do three things
    a phone expects, and they live here:

      · a tap on a link closes the drawer. Without this an in-page
        anchor (or a link to the page you are already on) left the
        drawer sitting open over the content it had just navigated to;
      · Escape closes it, and focus goes back to the burger, so a
        keyboard user is not stranded inside an invisible panel;
      · growing the viewport past the phone breakpoint with the drawer
        open closes it, or the checked state would silently scroll-lock
        the desktop page (body:has(#nav-open:checked) is overflow:hidden).

    The burger also mirrors the state onto aria-expanded, which a
    <label> cannot do on its own.

    ES5 on purpose — gulp-uglify 3 cannot parse newer syntax.        */

(function () {
    'use strict';

    var box = document.getElementById('nav-open');
    if (!box) {
        return;
    }

    var nav = document.querySelector('.site-head-nav');
    var burger = document.querySelector('.nav-burger');

    function reflect() {
        if (burger) {
            burger.setAttribute('aria-expanded', box.checked ? 'true' : 'false');
        }
    }

    function close(returnFocus) {
        if (!box.checked) {
            return;
        }
        box.checked = false;
        reflect();
        if (returnFocus && burger) {
            burger.focus();
        }
    }

    box.addEventListener('change', reflect);
    reflect();

    if (nav) {
        nav.addEventListener('click', function (e) {
            if (e.target.closest('a')) {
                close(false);
            }
        });
    }

    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' || e.key === 'Esc') {
            close(true);
        }
    });

    var wide = window.matchMedia('(min-width: 901px)');
    var onWide = function () {
        if (wide.matches) {
            close(false);
        }
    };
    if (wide.addEventListener) {
        wide.addEventListener('change', onWide);
    } else if (wide.addListener) {
        wide.addListener(onWide);
    }
})();
