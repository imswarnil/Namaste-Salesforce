/* Namaste UI — navbar behaviour.
   =========================================================================
   The progressive-enhancement half of components/css/navbar.css. Everything
   VISUAL is already handled by CSS reading aria-expanded / aria-checked /
   data-scrolled through :has(). This file's entire job is to put the right
   value in those attributes, plus the keyboard behaviour the WAI-ARIA
   disclosure pattern requires and markup alone cannot express.

   That division matters: it means a menu is never half-open because a class
   and an attribute disagreed, and the Next.js app can skip this file
   entirely — components/navigation/Navbar.jsx sets the same attributes from
   React state and gets the same CSS for free.

   Drop-in for the Ghost theme:
     <script src="{{asset "js/nav.js"}}" defer></script>

   Nothing here is required for the bar to WORK — with JS off the links,
   the brand and the buttons are all still real links and buttons, the
   dropdowns simply do not open, and every destination in them is also
   reachable from the footer sitemap. That is the deal: JS makes it nicer,
   never possible.

   Hooks it looks for:
     [data-ns-menu]        a <button aria-expanded aria-controls> inside a
                           .ns-navitem / .ns-usermenu wrapper
     [data-ns-sheet="id"]  the hamburger; toggles <dialog id> (.ns-navsheet)
     [data-ns-theme]       the segmented theme radiogroup
     [data-ns-theme-toggle] the one-button theme switch
     [data-ns-scrolled]    a bar that goes solid once the page moves
     [data-ns-progress]    the reading-progress line, gets --p */
(function () {
  "use strict";

  var doc = document;
  var ITEM = ".ns-navmenu__item, .ns-menu__item";

  /* ---- Disclosure menus (dropdown, mega, account) ---------------------- */

  /* One place that writes the state, so "open" is a single fact. */
  function setOpen(trigger, open) {
    trigger.setAttribute("aria-expanded", String(open));
  }

  function panelOf(trigger) {
    var id = trigger.getAttribute("aria-controls");
    return id ? doc.getElementById(id) : trigger.parentElement.querySelector(".ns-navmenu, .ns-megamenu, .ns-usermenu__panel");
  }

  function closeAll(except) {
    doc.querySelectorAll('[data-ns-menu][aria-expanded="true"]').forEach(function (t) {
      if (t !== except) setOpen(t, false);
    });
  }

  doc.addEventListener("click", function (e) {
    var trigger = e.target.closest("[data-ns-menu]");
    if (!trigger) {
      /* Outside click closes everything. A click INSIDE a panel also closes
         it — every row in these menus navigates, and leaving the panel open
         over the new page is the classic "did my click register?" bug. */
      var inPanel = e.target.closest(".ns-navmenu, .ns-megamenu, .ns-usermenu__panel");
      if (!inPanel || e.target.closest(ITEM)) closeAll();
      return;
    }
    e.preventDefault();
    var open = trigger.getAttribute("aria-expanded") === "true";
    closeAll(trigger);
    setOpen(trigger, !open);
  });

  doc.addEventListener("keydown", function (e) {
    var open = doc.querySelector('[data-ns-menu][aria-expanded="true"]');

    if (e.key === "Escape" && open) {
      setOpen(open, false);
      /* Focus MUST come back to the trigger. Without this, Esc drops the
         keyboard user at the top of the document and they have to tab the
         whole bar again. */
      open.focus();
      return;
    }

    var trigger = e.target.closest && e.target.closest("[data-ns-menu]");
    if (trigger && (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ")) {
      /* ArrowDown opens and moves into the panel — the disclosure pattern's
         one keyboard affordance beyond Enter. */
      if (e.key === "ArrowDown") {
        e.preventDefault();
        closeAll(trigger);
        setOpen(trigger, true);
        var panel = panelOf(trigger);
        var first = panel && panel.querySelector(ITEM);
        if (first) first.focus();
      }
      return;
    }

    /* Arrow keys walk the rows once inside a panel. */
    if (!open || (e.key !== "ArrowDown" && e.key !== "ArrowUp")) return;
    var host = panelOf(open);
    if (!host || !host.contains(e.target)) return;
    var rows = Array.prototype.slice.call(host.querySelectorAll(ITEM));
    var i = rows.indexOf(e.target);
    if (i < 0) return;
    e.preventDefault();
    rows[(i + (e.key === "ArrowDown" ? 1 : -1) + rows.length) % rows.length].focus();
  });

  /* Tabbing past the last row closes the menu, because the panel is
     visually gone the moment focus leaves it and a menu that is open but
     invisible steals the next Esc. */
  doc.addEventListener("focusout", function (e) {
    var wrap = e.target.closest && e.target.closest(".ns-navitem, .ns-usermenu");
    if (!wrap) return;
    /* relatedTarget is where focus is GOING; null means it left the page. */
    if (e.relatedTarget && wrap.contains(e.relatedTarget)) return;
    var trigger = wrap.querySelector("[data-ns-menu]");
    if (trigger) setOpen(trigger, false);
  });

  /* ---- Mobile sheet ----------------------------------------------------- */

  doc.querySelectorAll("[data-ns-sheet]").forEach(function (burger) {
    var sheet = doc.getElementById(burger.getAttribute("data-ns-sheet"));
    if (!sheet) return;

    burger.addEventListener("click", function () {
      if (sheet.open) { sheet.close(); return; }
      closeAll();
      /* showModal(), never a class or the open attribute: it is what grants
         the focus trap, the inert background and the top layer. */
      sheet.showModal();
      burger.setAttribute("aria-expanded", "true");
      /* The page behind must not scroll under the sheet. */
      doc.documentElement.style.overflow = "hidden";
    });

    /* One handler for every way it can close — Esc, the X, the backdrop,
       a link — so the burger's arrow can never be left pointing the wrong
       way. */
    sheet.addEventListener("close", function () {
      burger.setAttribute("aria-expanded", "false");
      doc.documentElement.style.overflow = "";
      burger.focus();
    });
    sheet.addEventListener("click", function (e) {
      if (e.target === sheet) sheet.close();           // backdrop
      if (e.target.closest("a[href]") || e.target.closest("[data-ns-sheet-close]")) sheet.close();
    });
  });

  /* Resizing past lg hides the burger, so a sheet left open would be a
     full-screen dialog with no visible way back. Close it instead of hiding
     it: a display:none'd modal still traps focus. */
  if (doc.querySelector(".ns-navsheet[open]") || doc.querySelector("[data-ns-sheet]")) {
    window.addEventListener("resize", function () {
      if (window.innerWidth < 1024) return;
      doc.querySelectorAll(".ns-navsheet[open]").forEach(function (sheet) { sheet.close(); });
    });
  }

  /* ---- Theme ------------------------------------------------------------
     Both forms delegate to window.nsTheme (assets/js/theme-init.js) so
     persistence and color-scheme are decided in exactly one place. If the
     init script was not inlined, the toggles still flip the attribute —
     they just cannot remember, which is a better failure than a dead
     button. */

  function currentChoice() {
    /* "system" is stored as the ABSENCE of a value, so that a reader who
       never chose keeps following their OS. */
    try {
      var stored = localStorage.getItem((window.nsTheme && window.nsTheme.key) || "ns-theme");
      return stored === "light" || stored === "dark" ? stored : "system";
    } catch (e) { return "system"; }
  }

  var groups = doc.querySelectorAll("[data-ns-theme]");
  var singles = doc.querySelectorAll("[data-ns-theme-toggle]");

  function syncTheme() {
    var choice = currentChoice();
    groups.forEach(function (group) {
      group.querySelectorAll("[data-ns-theme-value]").forEach(function (opt) {
        opt.setAttribute("aria-checked", String(opt.getAttribute("data-ns-theme-value") === choice));
        /* Roving tabindex: the group is one tab stop, arrows move inside. */
        opt.tabIndex = opt.getAttribute("data-ns-theme-value") === choice ? 0 : -1;
      });
    });
    var dark = doc.documentElement.getAttribute("data-theme") === "dark";
    singles.forEach(function (btn) { btn.setAttribute("aria-checked", String(dark)); });
  }

  groups.forEach(function (group) {
    group.addEventListener("click", function (e) {
      var opt = e.target.closest("[data-ns-theme-value]");
      if (!opt) return;
      var value = opt.getAttribute("data-ns-theme-value");
      if (!window.nsTheme) { doc.documentElement.setAttribute("data-theme", value === "system" ? "light" : value); syncTheme(); return; }
      if (value === "system") window.nsTheme.useSystem();
      else window.nsTheme.set(value);
      syncTheme();
    });
    group.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
      var opts = Array.prototype.slice.call(group.querySelectorAll("[data-ns-theme-value]"));
      var i = opts.indexOf(doc.activeElement);
      if (i < 0) return;
      e.preventDefault();
      var next = opts[(i + (e.key === "ArrowRight" ? 1 : -1) + opts.length) % opts.length];
      next.focus();
      next.click();
    });
  });

  singles.forEach(function (btn) {
    btn.addEventListener("click", function () {
      if (window.nsTheme) window.nsTheme.toggle();
      else doc.documentElement.setAttribute("data-theme", doc.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  });

  if (groups.length || singles.length) {
    syncTheme();
    /* The OS can flip underneath us (macOS at sunset) and theme-init.js
       updates the attribute when it does; this keeps the controls honest. */
    new MutationObserver(syncTheme).observe(doc.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  }

  /* ---- Scroll state & reading progress ---------------------------------
     One listener for both, passive, and it only ever writes when the value
     actually changed — a scroll handler that touches the DOM on every frame
     is how a calm page starts to feel expensive. */
  var scrollBars = doc.querySelectorAll("[data-ns-scrolled]");
  var progressBars = doc.querySelectorAll("[data-ns-progress]");

  if (scrollBars.length || progressBars.length) {
    var lastScrolled = null;
    var lastPercent = -1;
    var ticking = false;

    var measure = function () {
      ticking = false;
      var y = window.scrollY || 0;

      var scrolled = y > 8;
      if (scrolled !== lastScrolled) {
        lastScrolled = scrolled;
        scrollBars.forEach(function (bar) { bar.setAttribute("data-scrolled", String(scrolled)); });
      }

      if (progressBars.length) {
        var max = doc.documentElement.scrollHeight - window.innerHeight;
        var pct = max > 0 ? Math.min(100, Math.round((y / max) * 100)) : 0;
        if (pct !== lastPercent) {
          lastPercent = pct;
          progressBars.forEach(function (bar) {
            bar.style.setProperty("--p", pct);
            /* The bar is decorative chrome, but the number is real
               information — expose it once, on the element that has it. */
            if (bar.hasAttribute("aria-valuenow")) bar.setAttribute("aria-valuenow", String(pct));
          });
        }
      }
    };

    window.addEventListener("scroll", function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(measure);
    }, { passive: true });
    measure();
  }
})();

/* NS Design System — table of contents.
   =========================================================================
   Two jobs, both progressive enhancement:

     Used by the blog, the docs pages and any long prose surface — the TOC is
     its own module, not a blog feature, because a lesson and a doc page need
     exactly the same outline.

     1. The table of contents' scroll-spy. The TOC is a real <nav> of real
        anchor links that works with JS off; this only marks which heading is
        currently on screen with [aria-current], which is the same attribute
        the CSS already styles for the navbar and the lesson row.

     2. Building that TOC from the article's own headings, for a CMS that
        emits a post body but no outline. Opt in with [data-toc-from]; a
        hand-authored TOC is left exactly as it is.

   Reading progress lives in assets/js/lms.js (.ns-lprogress--article) — it
   is the same control on a lesson and on a post, so it has one
   implementation.

   Include with: <script src="assets/js/blog.js" defer></script> */
(function () {
  "use strict";

  var doc = document;

  /* ---- Build a TOC from the article -------------------------------------
     Only h2 and h3. Two levels is the limit: an outline that needs three is
     an outline for a page that needs splitting. A heading with no id gets
     one derived from its text, because an anchor link to nothing is worse
     than no anchor link. */
  function slug(text, taken) {
    var base = text.toLowerCase().trim()
      .replace(/[^\w\s-]/g, "")
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-") || "section";
    var id = base, n = 2;
    while (taken[id]) { id = base + "-" + n++; }
    taken[id] = true;
    return id;
  }

  /* data-toc-from must point at the PROSE, not at the whole article: a post
     footer carrying "Related" and four card titles will otherwise put five
     entries in the outline that are not sections of the post. */
  function build(nav) {
    var article = doc.querySelector(nav.getAttribute("data-toc-from"));
    if (!article) return;
    var headings = article.querySelectorAll("h2, h3");
    if (!headings.length) { nav.hidden = true; return; }

    var taken = {};
    Array.prototype.forEach.call(doc.querySelectorAll("[id]"), function (el) { taken[el.id] = true; });

    var list = doc.createElement("div");
    Array.prototype.forEach.call(headings, function (h) {
      if (!h.id) h.id = slug(h.textContent, taken);
      var a = doc.createElement("a");
      a.className = "ns-toc__link" + (h.tagName === "H3" ? " ns-toc__link--sub" : "");
      a.href = "#" + h.id;
      a.textContent = h.textContent;
      list.appendChild(a);
    });
    nav.appendChild(list);
  }

  /* ---- Scroll-spy -------------------------------------------------------
     A rAF-throttled scroll read rather than an IntersectionObserver, and
     deliberately so: the question is not "which headings are visible" but
     "which was the LAST one to cross the line", and a section taller than
     the viewport has NO heading on screen at all. An observer answers the
     first question; this answers the one a reader is actually asking.

     The line sits at 30% of the viewport height — high enough that the
     marked item changes as a heading settles into reading position, not the
     moment it appears at the bottom edge. */
  function spy(nav) {
    /* init() is exposed for apps that render a post after load, so it can be
       called more than once on the same TOC — without this guard each call
       adds another scroll listener that never comes off. */
    if (nav.hasAttribute("data-toc-spied")) return;
    var links = nav.querySelectorAll(".ns-toc__link");
    if (!links.length) return;
    nav.setAttribute("data-toc-spied", "");

    var targets = [];
    Array.prototype.forEach.call(links, function (a) {
      var id = decodeURIComponent((a.getAttribute("href") || "").slice(1));
      var el = id && doc.getElementById(id);
      if (el) targets.push({ el: el, link: a, seen: false });
    });
    if (!targets.length) return;

    function mark() {
      var current = null;
      for (var i = 0; i < targets.length; i++) {
        /* Above the line, or the first one when the reader is still above
           all of them — a TOC with nothing marked reads as broken. */
        if (targets[i].el.getBoundingClientRect().top <= window.innerHeight * 0.3) current = targets[i];
      }
      if (!current) current = targets[0];
      targets.forEach(function (t) {
        if (t.link === current.link) t.link.setAttribute("aria-current", "true");
        else t.link.removeAttribute("aria-current");
      });
      /* Keep the marked item inside a scrolling rail. Only when the rail
         actually scrolls — otherwise this fights the page. */
      var rail = nav.closest(".ns-post__rail") || nav;
      if (rail.scrollHeight > rail.clientHeight + 4) {
        var r = current.link.getBoundingClientRect(), b = rail.getBoundingClientRect();
        if (r.top < b.top || r.bottom > b.bottom) current.link.scrollIntoView({ block: "nearest" });
      }
    }

    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () { mark(); ticking = false; });
    }
    /* Capture on the document, not a listener on window: `scroll` does not
       bubble, so on any surface whose text scrolls inside its own pane rather
       than with the page — the course player's lesson column — a window
       listener never fires and the outline marks nothing for the whole
       lesson. mark() is viewport-relative already, so catching the event from
       whichever element scrolled is the entire fix. */
    document.addEventListener("scroll", onScroll, { passive: true, capture: true });
    window.addEventListener("resize", onScroll, { passive: true });
    mark();
  }

  function init(root) {
    Array.prototype.forEach.call((root || doc).querySelectorAll(".ns-toc[data-toc-from]:not([data-toc-built])"), function (nav) {
      build(nav);
      nav.setAttribute("data-toc-built", "");
    });
    Array.prototype.forEach.call((root || doc).querySelectorAll(".ns-toc"), spy);
  }

  if (doc.readyState === "loading") {
    doc.addEventListener("DOMContentLoaded", function () { init(doc); });
  } else {
    init(doc);
  }

  window.nsBlog = { init: init };
})();

/* NS Design System — typographic effect wiring.
   =========================================================================
   Four small jobs, none of which CSS can do alone:

     1. [data-fx-in]      an IntersectionObserver flag, so an effect draws
                          when it is read rather than while it is off-screen.
     2. --fx-len          the real path length of a hand-drawn circle, so the
                          stroke-dasharray draw is exact instead of guessed.
     3. .ns-scramble      the matrix-style character settle, on entry and on
                          responsive re-wrap.
     4. .ns-curve         builds the SVG <textPath> for circular text from
                          plain text in the markup.

   The whole file is a progressive enhancement. With JS off: highlights are
   already drawn, circles are already closed, scrambled text is just text,
   and circular text falls back to a readable straight line. Nothing here is
   load-bearing.

   Reduced motion is checked ONCE and honoured by skipping the animation
   entirely rather than by racing it to its end state.

   Include with: <script src="assets/js/type-fx.js" defer></script> */
(function () {
  "use strict";

  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- 1. In-view flag -------------------------------------------------- */
  var FX = "[data-fx], .ns-mark--animate, .ns-strike--animate, .ns-circle--animate, .ns-frame--animate, .ns-scan, .ns-reveal, .ns-scramble";

  function observe(root) {
    var targets = (root || document).querySelectorAll(FX);
    if (!targets.length) return;

    if (reduced || !("IntersectionObserver" in window)) {
      /* No observer, or the reader asked for stillness: mark everything in
         immediately. The CSS end states are the correct rendering, so this
         produces the finished effect with no motion. */
      Array.prototype.forEach.call(targets, function (el) { el.setAttribute("data-fx-in", ""); settle(el); });
      return;
    }

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.setAttribute("data-fx-in", "");
        scramble(entry.target);
        /* Once drawn, done. An effect that re-fires every time you scroll
           past it stops being punctuation and becomes a distraction. */
        io.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0.25 });

    Array.prototype.forEach.call(targets, function (el) { io.observe(el); });
  }

  /* ---- 2. Circle path length ------------------------------------------- */
  /* stroke-dasharray needs the path's own length or the "draw" either stalls
     short or finishes early. getTotalLength is exact and cheap; the CSS
     fallback (1000) only ever applies before this runs. */
  function measure(root) {
    Array.prototype.forEach.call((root || document).querySelectorAll(".ns-circle svg path"), function (path) {
      try {
        var len = Math.ceil(path.getTotalLength());
        path.closest(".ns-circle").style.setProperty("--fx-len", len);
      } catch (e) { /* detached or display:none — it keeps the fallback */ }
    });
  }

  /* ---- 3. Scramble ------------------------------------------------------ */
  var GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#$%&/<>*+=-";

  function settle(el) {
    if (!el.classList.contains("ns-scramble")) return;
    el.setAttribute("data-fx-settled", "");
    if (el.dataset.fxText) el.textContent = el.dataset.fxText;
  }

  function scramble(el) {
    if (!el.classList.contains("ns-scramble")) return;
    if (reduced) return settle(el);

    var final = el.dataset.fxText || (el.dataset.fxText = el.textContent);
    var chars = final.split("");

    /* Driven by ELAPSED TIME, not by a frame counter. rAF is throttled hard
       in a backgrounded tab and in an iframe that is only partly on screen —
       and a frame-counted scramble in that situation does not slow down, it
       stops, leaving a heading reading "D9#M/" indefinitely. Time-based, a
       throttled frame rate costs smoothness and nothing else, and the run
       always finishes in DURATION. */
    var DURATION = 700;
    var STAGGER = 0.55;  /* share of the run spent handing off left→right */
    var start = performance.now();
    /* Each character settles inside its own window; the windows overlap, so
       the reveal has a soft leading edge rather than a hard wipe. The jitter
       is per-character and fixed up front, so a character cannot be re-rolled
       into an earlier finish by a later frame. */
    var n = Math.max(chars.length - 1, 1);
    var plan = chars.map(function (_, i) {
      var from = (i / n) * STAGGER;
      return { from: from, to: from + (1 - STAGGER) * (0.55 + Math.random() * 0.45) };
    });
    el.removeAttribute("data-fx-settled");

    (function tick(now) {
      var t = Math.min((( now || performance.now()) - start) / DURATION, 1);
      var html = "";
      for (var i = 0; i < chars.length; i++) {
        var c = chars[i];
        if (c === " " || t >= plan[i].to) { html += escapeHtml(c); continue; }
        if (t < plan[i].from) { html += '<span data-fx-char>&nbsp;</span>'; continue; }
        html += '<span data-fx-char>' + GLYPHS[Math.floor(Math.random() * GLYPHS.length)] + "</span>";
      }
      el.innerHTML = html;
      if (t < 1) {
        window.requestAnimationFrame(tick);
      } else {
        el.textContent = final;
        el.setAttribute("data-fx-settled", "");
      }
    })();
  }

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  /* Re-scramble on a genuine layout break. This is the responsive half of the
     effect: when a breakpoint re-wraps a heading, the text re-settles instead
     of teleporting, so the reflow reads as deliberate. Bound to the
     breakpoint list rather than to resize — firing on every resize frame
     would be both useless and expensive. */
  ["(max-width: 40rem)", "(max-width: 64rem)"].forEach(function (q) {
    var mq = window.matchMedia(q);
    var on = mq.addEventListener ? "addEventListener" : "addListener";
    mq[on].call(mq, "change", function () {
      if (reduced) return;
      Array.prototype.forEach.call(document.querySelectorAll(".ns-scramble[data-fx-in]"), scramble);
    });
  });

  /* ---- 4. Circular text ------------------------------------------------- */
  /* <textPath> is the only correct way to set type on a curve — it rotates
     each glyph to the tangent, which no amount of per-character CSS rotation
     reproduces. The markup carries plain text; this replaces it with the SVG
     and keeps the original string as the accessible name. */
  var uid = 0;

  function curve(root) {
    Array.prototype.forEach.call((root || document).querySelectorAll(".ns-curve:not([data-fx-built])"), function (el) {
      var text = (el.dataset.fxCurveText || el.textContent || "").trim();
      if (!text) return;
      var center = el.querySelector(".ns-curve__center");
      var repeat = parseInt(el.dataset.fxRepeat || "1", 10);
      var id = "ns-curve-" + ++uid;
      var label = text;

      /* A circle traced from the top, clockwise. r=38 in a 100-unit box
         leaves room for the cap height plus the centre content. */
      var d = "M 50,50 m -38,0 a 38,38 0 1,1 76,0 a 38,38 0 1,1 -76,0";
      var body = new Array(repeat + 1).join(text + " · ");

      el.dataset.fxCurveText = text;
      el.textContent = "";
      el.insertAdjacentHTML("afterbegin",
        '<svg viewBox="0 0 100 100" aria-hidden="true" focusable="false">' +
        '<defs><path id="' + id + '" d="' + d + '"></path></defs>' +
        '<text><textPath href="#' + id + '" startOffset="0">' + escapeHtml(body) + "</textPath></text>" +
        "</svg>");
      if (center) el.appendChild(center);
      /* The ring is decorative once it is a curve — the readable copy is the
         label, announced once, in order. */
      if (!el.hasAttribute("aria-label")) el.setAttribute("aria-label", label);
      el.setAttribute("role", "img");
      el.setAttribute("data-fx-built", "");
    });
  }

  function init(root) {
    curve(root);
    measure(root);
    observe(root);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { init(document); });
  } else {
    init(document);
  }

  /* Exposed for apps that render effects after load (a route change, a lesson
     body arriving over the wire). Idempotent — everything it touches is
     guarded by a flag or an unobserve. */
  window.nsTypeFx = { init: init, scramble: scramble };
})();

/* NS Design System — LMS wiring.
   =========================================================================
   The five things the learner-facing layer needs that CSS cannot do. All of
   it is progressive enhancement: with this file absent the curriculum still
   collapses (native <details>), the filters still filter (native form
   controls), and the price range is still two working sliders — you just
   lose the conveniences.

     1. Expand / collapse all curriculum sections.
     2. The dual price range: keep the two thumbs from crossing, and paint
        the selected band on the track.
     3. Applied-filter chips, mirrored from the checkboxes.
     4. Article reading progress.
     5. Star-rating fills, from the numeric value that is already in the DOM.

   Include with: <script src="assets/js/lms.js" defer></script> */
(function () {
  "use strict";

  var doc = document;
  var pct = function (n) { return Math.max(0, Math.min(100, n)) + "%"; };

  /* ---- 1. Curriculum expand / collapse all ------------------------------
     The button's label is the ACTION, not the state, and it flips once the
     sections do — a control reading "Collapse all" while everything is
     already collapsed is the classic version of this bug. */
  doc.addEventListener("click", function (e) {
    var btn = e.target.closest ? e.target.closest("[data-curriculum-toggle]") : null;
    if (!btn) return;
    var root = btn.closest(".ns-curriculum") || doc;
    var sections = root.querySelectorAll(".ns-curriculum__section");
    if (!sections.length) return;
    var anyClosed = Array.prototype.some.call(sections, function (d) { return !d.open; });
    Array.prototype.forEach.call(sections, function (d) { d.open = anyClosed; });
    btn.setAttribute("aria-expanded", anyClosed ? "true" : "false");
    var label = btn.querySelector("[data-curriculum-label]");
    if (label) label.textContent = anyClosed ? "Collapse all" : "Expand all";
  });

  /* ---- 2. Price range ---------------------------------------------------
     Two native sliders on one track. The clamp is the whole job: without it
     the "from" thumb walks past the "to" thumb and the filter silently
     inverts. Each input keeps its own value — they are two real form
     controls, so the form submits, the keyboard works, and a screen reader
     announces two named sliders rather than one mystery widget. */
  function paint(range) {
    var from = range.querySelector("[data-range=from]");
    var to = range.querySelector("[data-range=to]");
    var fill = range.querySelector(".ns-range__fill");
    if (!from || !to) return;

    var min = Number(from.min || 0);
    var max = Number(from.max || 100);
    var span = max - min || 1;
    var a = Number(from.value);
    var b = Number(to.value);

    /* Clamp rather than swap. Swapping means the thumb you are dragging
       jumps out from under the pointer, which feels broken even though the
       numbers end up right. */
    if (a > b) { if (doc.activeElement === from) { a = b; from.value = a; } else { b = a; to.value = b; } }

    if (fill) {
      range.style.setProperty("--fx-from", pct(((a - min) / span) * 100));
      range.style.setProperty("--fx-to", pct(((b - min) / span) * 100));
    }
    var out = range.querySelectorAll("[data-range-out]");
    if (out[0]) out[0].value = a;
    if (out[1]) out[1].value = b;
  }

  doc.addEventListener("input", function (e) {
    var range = e.target.closest ? e.target.closest(".ns-range") : null;
    if (!range) return;
    /* Typing an exact figure writes back to the slider, so the two halves of
       the control can never disagree about what is filtered. */
    if (e.target.hasAttribute("data-range-out")) {
      var inputs = range.querySelectorAll("[data-range]");
      var i = Array.prototype.indexOf.call(range.querySelectorAll("[data-range-out]"), e.target);
      if (inputs[i]) inputs[i].value = e.target.value;
    }
    paint(range);
  });

  /* ---- 3. Applied-filter chips -----------------------------------------
     Mirrors the checked facets above the grid. The chip is the same control
     as the checkbox, so removing one unchecks the other and fires a real
     change event — whatever listens for filtering does not need to know
     chips exist. */
  function chips(root) {
    var box = root.querySelector("[data-applied]");
    if (!box) return;
    var checked = root.querySelectorAll(".ns-filters input[type=checkbox]:checked");
    box.innerHTML = "";
    Array.prototype.forEach.call(checked, function (input) {
      /* The facet's NAME, not everything in its label: the count sits in the
         same element and would arrive glued to the end ("Beginner24"). A
         clone with the count removed is exact, and survives any markup the
         label happens to carry — a regex on the text does not. */
      var label = input.closest("label");
      var name = input.value;
      if (label) {
        var clone = label.cloneNode(true);
        Array.prototype.forEach.call(clone.querySelectorAll(".ns-filters__count, input"), function (n) { n.remove(); });
        name = clone.textContent.trim() || input.value;
      }
      var chip = doc.createElement("button");
      chip.type = "button";
      chip.className = "ns-tag ns-tag--pill";
      chip.innerHTML = name + ' <i class="ph ph-x" aria-hidden="true"></i>';
      chip.setAttribute("aria-label", "Remove filter: " + name);
      chip.addEventListener("click", function () {
        input.checked = false;
        input.dispatchEvent(new Event("change", { bubbles: true }));
      });
      box.appendChild(chip);
    });
    var clear = root.querySelector("[data-clear-filters]");
    if (clear) clear.hidden = checked.length === 0;
    box.hidden = checked.length === 0;
  }

  doc.addEventListener("change", function (e) {
    var root = e.target.closest ? e.target.closest("[data-filters]") : null;
    if (root) chips(root);
  });

  doc.addEventListener("click", function (e) {
    var clear = e.target.closest ? e.target.closest("[data-clear-filters]") : null;
    if (!clear) return;
    var root = clear.closest("[data-filters]") || doc;
    Array.prototype.forEach.call(root.querySelectorAll(".ns-filters input[type=checkbox]:checked"), function (input) {
      input.checked = false;
      input.dispatchEvent(new Event("change", { bubbles: true }));
    });
  });

  /* ---- 4. Article reading progress --------------------------------------
     Measured against the ARTICLE, not the document: a lesson page with a
     long footer would otherwise report 70% at the end of the text. Read in
     a passive scroll listener and written as one custom property, so the
     work per frame is a single style mutation. */
  function reading() {
    Array.prototype.forEach.call(doc.querySelectorAll(".ns-lprogress--article[data-target]"), function (bar) {
      var article = doc.querySelector(bar.getAttribute("data-target"));
      if (!article) return;
      var box = article.getBoundingClientRect();
      var scrolled = -box.top;
      var scrollable = box.height - window.innerHeight;
      var value = scrollable <= 0 ? 100 : (scrolled / scrollable) * 100;
      bar.style.setProperty("--fx-progress", pct(value));
      bar.setAttribute("aria-valuenow", String(Math.round(Math.max(0, Math.min(100, value)))));
    });
  }

  /* Listened for in the CAPTURE phase on the document rather than on window.
     `scroll` does not bubble, so a window listener never hears the course
     player — whose lesson column is its own scroll region — and the reading
     hairline sat at its server-rendered value for the whole lesson. Capture
     catches the event from any scroller on the page, and the maths above is
     already viewport-relative, so nothing else has to change. */
  var ticking = false;
  document.addEventListener("scroll", function () {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () { reading(); ticking = false; });
  }, { passive: true, capture: true });

  /* ---- 5. Star fills ----------------------------------------------------
     The number is already in the DOM as text — this only turns it into the
     width of the overlay. Nothing here is the source of the rating. */
  function ratings(root) {
    Array.prototype.forEach.call((root || doc).querySelectorAll(".ns-rating[data-value]"), function (el) {
      var value = parseFloat(el.getAttribute("data-value"));
      var outOf = parseFloat(el.getAttribute("data-of") || "5");
      if (isNaN(value) || !outOf) return;
      el.style.setProperty("--fx-rating", pct((value / outOf) * 100));
    });
  }

  /* ---- 6. Lesson rail filter --------------------------------------------
     The answer to the forty-lesson course, where scrolling to find "the one
     about governor limits" is the rail's whole problem.

     It hides ROWS, it does not rebuild the list: the indices, the completion
     states and the current row are all already correct in the markup, and a
     filter that re-renders them is a filter that can get them wrong. Nothing
     here runs until someone types, so the rail is fully usable with the script
     blocked — the input is then a search box that does nothing, which is why
     it is the only part of the rail that is progressive rather than required.

     Section headings go with their rows: a heading left standing over an empty
     section is a heading that lies about what is under it. */
  function railFilter(box) {
    var input = box.querySelector('input[type="search"], input');
    /* The rail and the mobile panel are the same list in two containers, so
       this drives both rather than shipping a second copy of it for the one
       that happens to be a popover. */
    var host = box.closest(".ns-player__side, .ns-lessonmodal");
    var list = host && host.querySelector(".ns-player__list, .ns-lessonmodal__list");
    if (!input || !list) return;

    var empty = doc.createElement("div");
    empty.className = "ns-empty";
    empty.hidden = true;
    empty.innerHTML = '<p class="ns-empty__title"></p><p class="ns-empty__text">Try a word from the lesson’s title.</p>';
    list.appendChild(empty);

    input.addEventListener("input", function () {
      var q = input.value.trim().toLowerCase();
      var shown = 0;

      Array.prototype.forEach.call(list.querySelectorAll(".ns-lesson"), function (row) {
        var title = row.querySelector(".ns-lesson__title");
        var match = !q || (title ? title.textContent.toLowerCase().indexOf(q) > -1 : false);
        row.hidden = !match;
        if (match) shown++;
      });

      /* A section heading is visible only while something under it is. */
      Array.prototype.forEach.call(list.querySelectorAll(".ns-player__section"), function (head) {
        var any = false, el = head.nextElementSibling;
        while (el && !el.classList.contains("ns-player__section")) {
          if (el.classList.contains("ns-lesson") && !el.hidden) { any = true; break; }
          el = el.nextElementSibling;
        }
        head.hidden = !any;
      });

      empty.hidden = !(q && shown === 0);
      if (!empty.hidden) empty.firstChild.textContent = "No lesson matches “" + input.value.trim() + "”";
    });
  }

  /* ---- 7. The curriculum toggle -----------------------------------------
     The course bar's sidebar button, and it had none of this: it shipped
     aria-expanded and aria-controls and nothing listened, so the one control
     named "toggle curriculum" did nothing at any width.

     TWO behaviours, one control, chosen by whether the rail is on screen:

       ≥ lg   collapse and expand the rail in place (data-rail on .ns-player).
       < lg   there IS no rail — it is display:none and the lesson list lives
              in the panel — so the same button opens that panel instead.

     Deciding on computed display rather than on a matchMedia breakpoint means
     the button follows the stylesheet: change where the rail disappears and
     this follows it, with no second copy of the number to keep in step. */
  function curriculumToggle(root) {
    Array.prototype.forEach.call(
      (root || doc).querySelectorAll('[aria-controls="player-rail"]'),
      function (btn) {
        if (btn.hasAttribute("data-ns-rail-wired")) return;
        btn.setAttribute("data-ns-rail-wired", "");
        btn.addEventListener("click", function () {
          var player = doc.querySelector(".ns-player");
          var rail = doc.getElementById("player-rail");
          if (!player || !rail) return;

          if (getComputedStyle(rail).display === "none") {
            var panel = doc.getElementById("lesson-drawer");
            /* showPopover throws if it is already open — which is exactly what
               a second click means, so that is the toggle. */
            if (panel && panel.showPopover) {
              if (panel.matches(":popover-open")) panel.hidePopover();
              else panel.showPopover();
            }
            return;
          }

          var open = player.getAttribute("data-rail") !== "collapsed";
          player.setAttribute("data-rail", open ? "collapsed" : "open");
          /* EVERY control pointed at the rail is updated, not just the one
             that was clicked: the collapse button lives inside the rail and
             the reopen button lives outside it, so exactly one of them is on
             screen at a time and both have to agree about the state. */
          Array.prototype.forEach.call(doc.querySelectorAll('[aria-controls="player-rail"]'), function (other) {
            other.setAttribute("aria-expanded", String(!open));
          });
        });
      }
    );
  }

  /* ---- 8. Ask AI ---------------------------------------------------------
     The lesson's "open this in Claude / ChatGPT / Perplexity" menu.

     What this does NOT do is send anything anywhere. There is no key, no
     proxy and no request from us: each row is an ordinary link with
     target="_blank" rel="noopener", and all this does is compose its href
     from ONE prompt written once on the container, rather than repeating the
     same sentence in three hrefs that then drift apart.

     The prompt carries the lesson's title — the site's own text — and nothing
     about the learner. Where a video is playing it also carries the timestamp,
     because "explain what is happening at 08:03" is a better question than
     "explain this lesson", and the reader can see exactly what is being sent
     before they click: it is in the URL, and the Copy row puts it on the
     clipboard verbatim.

     Composed on OPEN rather than on load, so the timestamp is the one the
     learner is looking at rather than the one the page rendered with. */
  function askAi(menu) {
    var base = menu.getAttribute("data-ns-ask-prompt");
    var field = menu.querySelector("[data-ns-ask-input]");
    if (!base) return;

    /* The prompt the page suggests. The learner's edits win over it — this is
       only what the field starts as, and it is recomputed when the panel opens
       so the timestamp is the one they are looking at rather than the one the
       page rendered with. */
    function suggested() {
      var cur = doc.querySelector("[data-ns-video-current]");
      var at = cur && cur.textContent.trim();
      /* 0:00 means "has not started", which is not a useful thing to ask about. */
      return at && at !== "0:00" ? base + " I am at " + at + " in the video." : base;
    }
    function prompt() {
      return (field && field.value.trim()) || suggested();
    }

    function compose() {
      var q = encodeURIComponent(prompt());
      Array.prototype.forEach.call(menu.querySelectorAll("[data-ns-ask]"), function (a) {
        a.href = a.getAttribute("data-ns-ask") + q;
      });
    }

    var trigger = menu.querySelector("[data-ns-menu]");
    if (trigger) {
      trigger.addEventListener("click", function () {
        /* Refill only while untouched: a reader who has written their own
           question does not want it replaced because they closed the panel to
           check the video. */
        if (field && !field.dataset.touched) field.value = suggested();
        compose();
      });
    }
    if (field) {
      field.value = suggested();
      field.addEventListener("input", function () {
        field.dataset.touched = "1";
        compose();
      });
    }
    compose();

    var copy = menu.querySelector("[data-ns-ask-copy]");
    if (copy) {
      copy.addEventListener("click", function () {
        var text = prompt();
        var done = function () {
          copy.setAttribute("data-copied", "");
          setTimeout(function () { copy.removeAttribute("data-copied"); }, 1200);
        };
        if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {});
        else done();
      });
    }
  }

  function init(root) {
    ratings(root);
    Array.prototype.forEach.call((root || doc).querySelectorAll(".ns-range"), paint);
    Array.prototype.forEach.call((root || doc).querySelectorAll("[data-filters]"), chips);
    Array.prototype.forEach.call((root || doc).querySelectorAll(".ns-player__side-search"), railFilter);
    curriculumToggle(root);
    Array.prototype.forEach.call((root || doc).querySelectorAll("[data-ns-ask-prompt]"), askAi);
    reading();
  }

  if (doc.readyState === "loading") {
    doc.addEventListener("DOMContentLoaded", function () { init(doc); });
  } else {
    init(doc);
  }

  window.nsLms = { init: init };
})();

/* NS Design System — training rail: filter and drawer.
   =========================================================================
   Two jobs, both progressive enhancement, both specific to a curriculum with
   a hundred and fifty sections in it. The rail's OTHER behaviour — opening the
   section that contains the current post and scrolling it into view — is in
   assets/js/rail.js and is shared with the docs sidebar; it is not repeated
   here.

     1. FILTER. Type in the rail's search box and the tree reduces to the
        sections and lessons that match. This is the whole reason the box exists:
        at fifteen sections a tree is navigable, and at a hundred and fifty it
        is a filing cabinet you have to already know your way around.

        Matching a LESSON reveals its section. Matching a SECTION keeps all of its
        lessons, because "sharing" should show you everything in the Sharing
        section rather than the one lesson whose title happens to repeat the word.

     2. DRAWER, and COLLAPSE. One attribute, data-rail, carries three
        states — "closed" (a normal column), "collapsed" (a hairline spine
        with the reopen control on it, desktop only) and "open" (the phone
        drawer). Two attributes would be two things to keep in step.

        Below the lg breakpoint the fixed rail becomes an off-canvas
        drawer — the stylesheet does the sliding, this sets the state, traps
        nothing, and closes on Escape, on the scrim, and on choosing a post.

   Both degrade correctly. With this file removed the search box is a real
   input in a real <form> pointed at site search, and the rail is a column
   that is simply always open.

   Markup contract
     <div class="ns-training ns-training--fixed" data-ns-training data-rail="closed">
       <button data-ns-training-open>            the panel bar's handle
       <button data-ns-training-collapse>        column -> spine (desktop)
       <button data-ns-training-expand>          spine -> column
       <div class="ns-training__scrim" data-ns-training-close>
       <nav class="ns-trainingnav" data-ns-trainingnav>
         <input data-ns-trainingnav-filter>      the filter box
         <p data-ns-trainingnav-result>          "6 sections · 21 lessons" — written here
         <details class="ns-trainingnav__section"> … </details>

   Include with: <script src="assets/js/training.js" defer></script> */
(function () {
  "use strict";

  var doc = document;

  /* ---- the filter -------------------------------------------------------- */
  function wireFilter(rail) {
    var input = rail.querySelector("[data-ns-trainingnav-filter]");
    if (!input) return;
    var result = rail.querySelector("[data-ns-trainingnav-result]");

    /* QUERIED ON EVERY PASS, NOT CACHED ONCE.
       This used to read the sections into an array at wire time. That is
       correct for a server-rendered rail and silently wrong for a rail whose
       sections arrive from data — which is the Next.js LMS, and which is how
       a 100-section curriculum is actually going to be built. Sections added
       after init were unknown to the filter, so they were never hidden, while
       the result line counted only the ones present at startup: the rail
       claimed "1 section" above ninety-two visible ones.

       Re-querying costs one querySelectorAll per keystroke against a debounce
       that already exists. At 100 sections that is not measurable, and it
       removes a whole class of "works in the styleguide, breaks in the app". */
    function all() {
      return [].slice.call(rail.querySelectorAll(".ns-trainingnav__section"));
    }
    if (!all().length) return;

    /* The open/closed state the reader chose, remembered before the first
       search so clearing the box puts the rail back exactly as it was. A
       filter that leaves forty sections expanded behind it has not finished
       the job it started.

       Stored ON each section rather than in a positional array, because the
       set is no longer fixed: an index into a snapshot points at the wrong
       section the moment one is inserted. */
    var restoring = false;

    function text(el) {
      return (el.textContent || "").toLowerCase();
    }

    function apply(q) {
      q = q.trim().toLowerCase();
      var sections = all();

      if (!q) {
        sections.forEach(function (m) {
          m.hidden = false;
          [].slice.call(m.querySelectorAll("li")).forEach(function (li) { li.hidden = false; });
          if (restoring && m.nsWasOpen !== undefined) { m.open = m.nsWasOpen; }
          delete m.nsWasOpen;
        });
        restoring = false;
        if (result) result.textContent = "";
        return;
      }

      if (!restoring) {
        restoring = true;
        sections.forEach(function (m) { m.nsWasOpen = m.open; });
      }

      var shownSections = 0;
      var shownLessons = 0;

      sections.forEach(function (m) {
        var summary = m.querySelector("summary");
        var sectionHit = summary ? text(summary).indexOf(q) !== -1 : false;
        var lessons = [].slice.call(m.querySelectorAll(".ns-trainingnav__list > li"));
        var hits = 0;

        lessons.forEach(function (li) {
          /* A section-level match keeps everything under it — "sharing" should
             open the Sharing section, not reduce it to the one post whose
             title repeats the word. */
          var hit = sectionHit || text(li).indexOf(q) !== -1;
          li.hidden = !hit;
          if (hit) hits++;
        });

        var keep = sectionHit || hits > 0;
        m.hidden = !keep;
        /* Everything that survives is opened: the point of searching is to
           see the results, and a match hidden inside a collapsed section is a
           match the reader has to go looking for twice. */
        if (keep) { m.open = true; shownSections++; shownLessons += hits; }
      });

      /* Say what happened. A rail showing three of a hundred and fifty
         sections with no explanation looks broken rather than filtered — and
         zero results has to be a sentence, never an empty column. */
      if (result) {
        result.textContent = shownSections
          ? shownSections + " section" + (shownSections === 1 ? "" : "s") + " · " + shownLessons + " lesson" + (shownLessons === 1 ? "" : "s")
          : "Nothing matches “" + input.value.trim() + "”";
      }
    }

    var timer = null;
    input.addEventListener("input", function () {
      /* A hundred and fifty <details> re-laid-out on every keystroke is a
         rail that stutters while you type. One frame's worth of debounce is
         invisible to a person and removes the thrash entirely. */
      clearTimeout(timer);
      timer = setTimeout(function () { apply(input.value); }, 120);
    });
    /* Escape clears the filter before it closes the drawer — the innermost
       thing first, which is what Escape means everywhere else in the system. */
    input.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && input.value) {
        e.stopPropagation();
        input.value = "";
        apply("");
      }
    });
    /* The box lives in a <form> so it works with no JS. With JS it must not
       navigate. */
    var form = input.closest("form");
    if (form) form.addEventListener("submit", function (e) { e.preventDefault(); });
  }

  /* ---- the drawer -------------------------------------------------------- */
  function wireDrawer(root) {
    var rail = root.querySelector(".ns-trainingnav");
    if (!rail) return;

    function set(open) {
      root.setAttribute("data-rail", open ? "open" : "closed");
      root.querySelectorAll("[data-ns-training-open]").forEach(function (b) {
        b.setAttribute("aria-expanded", open ? "true" : "false");
      });
      if (open) {
        var first = rail.querySelector("[data-ns-trainingnav-filter], a, button");
        if (first) first.focus();
      }
    }

    /* COLLAPSE is the desktop state and OPEN is the phone state, and they are
       the same attribute on purpose: a rail is a column, a spine or a drawer,
       never two of those at once. Collapsing keeps the rail in the DOM, so
       the filter text and the scroll position survive the round trip. */
    function collapse(on) {
      root.setAttribute("data-rail", on ? "collapsed" : "closed");
      var reopen = root.querySelector("[data-ns-training-expand]");
      if (on && reopen) reopen.focus();
      else {
        var back = root.querySelector("[data-ns-training-collapse]");
        if (back) back.focus();
      }
    }

    doc.addEventListener("click", function (e) {
      if (e.target.closest("[data-ns-training-collapse]")) { collapse(true); return; }
      if (e.target.closest("[data-ns-training-expand]")) { collapse(false); return; }
      if (e.target.closest("[data-ns-training-open]")) { set(root.getAttribute("data-rail") !== "open"); return; }
      if (e.target.closest("[data-ns-training-close]")) { set(false); return; }
      /* Choosing a post closes the drawer: the reader asked to go somewhere,
         and leaving the navigation covering the thing they just chose is the
         classic mobile-drawer bug. Only inside the rail, and only for a real
         link — the filter box and the twisties are not navigation. */
      var link = e.target.closest(".ns-trainingnav__link");
      if (link && rail.contains(link)) set(false);
    });

    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && root.getAttribute("data-rail") === "open") set(false);
    });
  }

  /* SHOW THE READER WHERE THEY ARE, on load.
     The curriculum this rail is built for runs to ~100 sections and ~500
     lessons, and every section but the current one is shut — which is what
     keeps it a list rather than a document. The cost is that the rail can
     open scrolled to row 1 while the lesson being read is row 340, so it
     opens on somebody else's curriculum.

     So: open the section that owns [aria-current], then bring the current
     lesson into view. Two details matter.

     `block: "center"` rather than the default, because the useful thing is
     the lesson WITH ITS NEIGHBOURS — what comes next is half the reason to
     look at a curriculum, and a row scrolled to the top edge has no next.

     `behavior: "auto"`, never smooth. This fires on load; a rail that visibly
     races through 340 rows before settling is motion nobody asked for, and
     tokens/effects.css is explicit that a response is not a gesture. It also
     means prefers-reduced-motion needs no special case here — there is no
     motion to reduce.

     If the markup ships no [aria-current] — an index page, a preview — this
     does nothing at all, which is the correct amount. */
  function revealCurrent(rail) {
    var current = rail.querySelector("[aria-current='page']");
    if (!current) return;
    var section = current.closest("details");
    if (section) section.open = true;
    var scroller = rail.querySelector(".ns-trainingnav__scroll") || rail;
    /* Only scroll the RAIL, not the page. scrollIntoView walks every
       scrollable ancestor, so on a phone — where the rail is a fixed drawer
       over the article — it would drag the article down behind the drawer
       too. Compute the offset against the scroller and set scrollTop. */
    if (!scroller.scrollHeight || scroller.scrollHeight <= scroller.clientHeight) return;
    var top = current.offsetTop - scroller.offsetTop;
    scroller.scrollTop = Math.max(0, top - (scroller.clientHeight / 2) + (current.offsetHeight / 2));
  }

  function init(scope) {
    (scope || doc).querySelectorAll("[data-ns-trainingnav]").forEach(function (rail) {
      if (rail.nsTrainingFilter) return;
      rail.nsTrainingFilter = true;
      wireFilter(rail);
      revealCurrent(rail);
    });
    (scope || doc).querySelectorAll("[data-ns-training]").forEach(function (root) {
      if (root.nsTrainingDrawer) return;
      root.nsTrainingDrawer = true;
      wireDrawer(root);
    });
  }

  if (doc.readyState === "loading") doc.addEventListener("DOMContentLoaded", function () { init(); });
  else init();
  window.nsTrainingInit = init;
})();

/* NS Design System — navigation rail.
   =========================================================================
   One job, shared by every long scrolling nav in the system: the training
   curriculum (.ns-trainingnav) and the docs sidebar (.ns-sidebar).

   On load it finds the link marked aria-current="page", opens the <details>
   section containing it, closes the others, and scrolls it into view INSIDE
   THE RAIL. That last part is the whole trick: scrollIntoView on a sticky rail
   scrolls the nearest scrollable ancestor, which is usually the document, so
   the page jumps and the reader loses their place.

   Everything is progressive. The markup ships every section `open`, so with
   JS off nothing is hidden — the rail is only longer. Building it the other
   way round means a JS failure hides the entire navigation.

   And once the reader opens a section themselves we stop managing state. A nav
   that re-collapses what you just opened is a nav that is fighting you. */
(function () {
  var rails = document.querySelectorAll("[data-ns-rail], [data-ns-trainingnav]");
  if (!rails.length) return;

  rails.forEach(function (rail) {
    var current = rail.querySelector('[aria-current="page"]');
    var sections = rail.querySelectorAll("details");
    if (!current) return;

    var active = current.closest("details");

    /* Collapse to the section holding the current page.
       When the current page is NOT inside a section — the foundations links at
       the top of the docs rail — every section closes, which is the same
       promise kept: exactly the part of the tree you are in is open, and
       nothing else. Scoped to the docs rail, because a curriculum whose
       current lesson somehow sits outside a module must not collapse to
       nothing; there the old behaviour (leave it alone) is the safe one. */
    if (sections.length && (active || rail.hasAttribute("data-ns-rail"))) {
      sections.forEach(function (s) { s.open = s === active; });
    }

    /* User intent is a CLICK on a summary — never the `toggle` event.
       <details> queues `toggle` asynchronously, so the collapse above fires
       one per section AFTER this task and BEFORE the rAF below. Reading those
       as "the reader opened something" is what silently disabled the
       scroll-into-view on every page for the entire life of this file: the
       rail collapsed correctly and then never moved. A programmatic .open
       cannot produce a click, so this cannot make the same mistake. */
    var userDriven = false;
    sections.forEach(function (s) {
      var summary = s.querySelector("summary");
      if (summary) summary.addEventListener("click", function () { userDriven = true; });
    });

    /* The element carrying [data-ns-rail] is not necessarily the one that
       scrolls — in the styleguide the marker sits on the <nav> while the
       overflow lives on its .side wrapper, so scrolling the nav did precisely
       nothing. Walk up to whatever actually has a scrollbar. */
    var scroller = rail;
    while (scroller && scroller !== document.body) {
      var oy = getComputedStyle(scroller).overflowY;
      if ((oy === "auto" || oy === "scroll") && scroller.scrollHeight > scroller.clientHeight) break;
      scroller = scroller.parentElement;
    }
    if (!scroller || scroller === document.body) return;

    /* Only scroll when the active link is actually out of view — moving a rail
       whose current item was already visible reads as a glitch, not a help. */
    function centre() {
      if (userDriven) return;
      var boxRect = scroller.getBoundingClientRect();
      var linkRect = current.getBoundingClientRect();
      if (linkRect.top >= boxRect.top && linkRect.bottom <= boxRect.bottom) return;
      /* Centre it: context above and below is what makes a long list
         navigable. Landing it flush at the top hides everything before it. */
      scroller.scrollTop += (linkRect.top - boxRect.top) - (boxRect.height / 2) + (linkRect.height / 2);
    }

    /* Synchronously, NOT in a requestAnimationFrame. Reading
       getBoundingClientRect above flushes layout, so the geometry is already
       correct the moment the sections have been collapsed — and rAF does not
       fire at all in a background tab, so a styleguide page opened with
       cmd-click used to load with its rail parked at the top until something
       else forced a frame. Doing the work synchronously means the rail is
       already in the right place in the first painted frame, on every tab. */
    centre();

    /* Then once more after the first frame. Switzer and Roboto Mono load with
       font-display: swap, and a swap above the active link changes every
       offset below it — this is the pass that catches that. Harmless when
       nothing moved (the in-view test above short-circuits), and it cannot
       fight the reader: a summary click sets userDriven, and no human clicks
       inside the 16ms before it runs. */
    requestAnimationFrame(centre);
  });
})();

/* NS Design System — tabs.
   =========================================================================
   The CSS documented the ARIA contract from the start and nothing implemented
   it, so tabs looked selectable and were not. This is that implementation.

     - Click or arrow to select. ArrowLeft/Right for a horizontal tablist,
       ArrowUp/Down for aria-orientation="vertical", Home/End to the ends.
     - Roving tabindex: only the selected tab is in the tab order, so Tab moves
       OUT of the tablist and into the panel, which is the whole point of the
       pattern. Landing on eight tabs one at a time is the bug it avoids.
     - Selection is aria-selected plus [hidden] on the panels. No classes, so
       the CSS, the assistive layer and this script read one source.

   Progressive: with no JS every panel is visible, which is worse to scroll but
   never hides content. That is why the panels are NOT hidden in the markup —
   this script hides the inactive ones on init. Building it the other way round
   means a JS failure hides everything but the first panel. */
(function () {
  function wire(list) {
    var tabs = [].slice.call(list.querySelectorAll('[role="tab"]'));
    if (!tabs.length) return;
    var vertical = list.getAttribute("aria-orientation") === "vertical";

    var panels = tabs.map(function (t) {
      var id = t.getAttribute("aria-controls");
      return id ? document.getElementById(id) : null;
    });

    function select(i, focus) {
      tabs.forEach(function (t, n) {
        var on = n === i;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        if (panels[n]) panels[n].hidden = !on;
      });
      if (focus && tabs[i]) tabs[i].focus();
    }

    var start = tabs.findIndex(function (t) { return t.getAttribute("aria-selected") === "true"; });
    select(start < 0 ? 0 : start, false);

    list.addEventListener("click", function (e) {
      var tab = e.target.closest('[role="tab"]');
      if (tab) select(tabs.indexOf(tab), true);
    });

    list.addEventListener("keydown", function (e) {
      var i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      var prev = vertical ? "ArrowUp" : "ArrowLeft";
      var next = vertical ? "ArrowDown" : "ArrowRight";
      var to = null;
      if (e.key === prev) to = (i - 1 + tabs.length) % tabs.length;
      else if (e.key === next) to = (i + 1) % tabs.length;
      else if (e.key === "Home") to = 0;
      else if (e.key === "End") to = tabs.length - 1;
      if (to === null) return;
      e.preventDefault();
      select(to, true);
    });
  }

  [].forEach.call(document.querySelectorAll('[role="tablist"]'), wire);
})();

/* NS Design System — code block wiring.
   =========================================================================
   Everything .ns-code needs that CSS cannot do, and nothing else. Delegated
   from the document, so blocks rendered after load (a lesson body, a docs
   route change) work with no re-init.

   Deliberately NOT here:
   - The Ask AI and Share menus. They are native popovers — popovertarget
     gives light-dismiss, Esc and top-layer placement for free, and every
     line of JS that reimplements that is a focus-trap bug waiting to happen.
   - Syntax highlighting. The markup arrives already tokenised (server-side,
     or by the React component). Highlighting on the client means shipping a
     grammar to every reader to re-derive something the build already knew.

   Include with: <script src="assets/js/code.js" defer></script> */
(function () {
  "use strict";

  var doc = document;

  /* The source of truth for "what is in this block" is the rendered text, not
     a data attribute — a copy button that copies a stale attribute instead of
     what is on screen is worse than no copy button. Line numbers live in a
     separate aria-hidden gutter, so they cannot end up in the clipboard. */
  function sourceOf(block) {
    var pre = block.querySelector(".ns-code__pre");
    return pre ? pre.innerText.replace(/\n$/, "") : "";
  }

  function flash(btn, ms) {
    btn.setAttribute("data-copied", "true");
    window.setTimeout(function () { btn.removeAttribute("data-copied"); }, ms || 1600);
  }

  function copy(text, btn) {
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { flash(btn); });
      return;
    }
    /* http:// and older Safari. A hidden textarea + execCommand is the only
       fallback that still works, and it has to be visible-ish to be
       selectable, hence the off-screen position rather than display:none. */
    var ta = doc.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.cssText = "position:fixed;top:-9999px;opacity:0";
    doc.body.appendChild(ta);
    ta.select();
    try { doc.execCommand("copy"); flash(btn); } catch (e) { /* nothing sane left to try */ }
    doc.body.removeChild(ta);
  }

  doc.addEventListener("click", function (e) {
    var el = e.target.closest ? e.target.closest("[data-code]") : null;
    if (!el) return;
    var block = el.closest(".ns-code");
    if (!block) return;
    var action = el.getAttribute("data-code");

    if (action === "copy") {
      copy(sourceOf(block), el);
      return;
    }

    if (action === "wrap") {
      var wrapped = block.getAttribute("data-wrap") === "true";
      block.setAttribute("data-wrap", wrapped ? "false" : "true");
      el.setAttribute("aria-pressed", wrapped ? "false" : "true");
      return;
    }

    if (action === "expand") {
      var collapsed = block.getAttribute("data-collapsed") === "true";
      block.setAttribute("data-collapsed", collapsed ? "false" : "true");
      el.setAttribute("aria-expanded", collapsed ? "true" : "false");
      var label = el.querySelector("[data-code-label]");
      if (label) label.textContent = collapsed ? "Collapse" : "Expand";
      return;
    }

    if (action === "run") {
      run(block, el);
      return;
    }

    if (action === "share") {
      var url = el.getAttribute("data-share-url") || window.location.href;
      if (el.getAttribute("data-share") === "native" && navigator.share) {
        navigator.share({ title: doc.title, url: url }).catch(function () {});
      } else {
        copy(url, el);
      }
      var menu = el.closest("[popover]");
      if (menu && menu.hidePopover) menu.hidePopover();
      return;
    }

    if (action === "ask") {
      /* The AI menu items are LINKS in the markup, carrying a real href to
         the chosen assistant with the code prefilled. This branch exists only
         for the in-app case, where the host page listens for the event and
         opens its own panel instead of navigating away. */
      block.dispatchEvent(new CustomEvent("ns:code-ask", {
        bubbles: true,
        detail: { provider: el.getAttribute("data-provider") || "", code: sourceOf(block), language: block.getAttribute("data-lang") || "" },
      }));
      var m = el.closest("[popover]");
      if (m && m.hidePopover) m.hidePopover();
    }
  });

  /* Run is a HOST responsibility — this system does not ship a sandbox, and
     a design system that quietly evaluates the code in its own docs would be
     a remarkable security decision. The button emits an event the product
     handles; the demo path (data-output) just prints a canned result so the
     component can be documented honestly. */
  function run(block, btn) {
    var out = block.querySelector(".ns-code__out");
    var canned = block.getAttribute("data-output");

    btn.setAttribute("data-state", "running");
    block.dispatchEvent(new CustomEvent("ns:code-run", {
      bubbles: true,
      detail: {
        code: sourceOf(block),
        language: block.getAttribute("data-lang") || "",
        /* The host calls this when it has a result. Until it does, the button
           stays in its running state — no fake completion. */
        done: function (result, ok) { finish(block, btn, result, ok !== false); },
      },
    }));

    if (canned !== null && out) {
      window.setTimeout(function () { finish(block, btn, canned, block.getAttribute("data-output-ok") !== "false"); }, 550);
    }
  }

  function finish(block, btn, result, ok) {
    var out = block.querySelector(".ns-code__out");
    btn.removeAttribute("data-state");
    if (!out) return;
    out.hidden = false;
    out.textContent = result == null ? "" : String(result);
    var status = block.querySelector("[data-code-status]");
    if (status) {
      status.innerHTML = '<i class="ph ' + (ok ? "ph-check-circle" : "ph-warning-circle") + '" aria-hidden="true"></i>' + (ok ? "Success" : "Failed");
    }
  }

  /* Tabs — a real tablist, so arrow keys move between files the way they do
     in every other tabbed thing on the page. */
  doc.addEventListener("click", function (e) {
    var tab = e.target.closest ? e.target.closest(".ns-code__tab") : null;
    if (tab) select(tab);
  });

  doc.addEventListener("keydown", function (e) {
    var tab = e.target.closest ? e.target.closest(".ns-code__tab") : null;
    if (!tab) return;
    var keys = { ArrowRight: 1, ArrowLeft: -1, Home: "first", End: "last" };
    if (!(e.key in keys)) return;
    var tabs = Array.prototype.slice.call(tab.parentNode.querySelectorAll(".ns-code__tab"));
    var i = tabs.indexOf(tab);
    var next = keys[e.key] === "first" ? tabs[0]
      : keys[e.key] === "last" ? tabs[tabs.length - 1]
      : tabs[(i + keys[e.key] + tabs.length) % tabs.length];
    e.preventDefault();
    select(next);
    next.focus();
  });

  function select(tab) {
    var strip = tab.parentNode;
    var block = tab.closest(".ns-code");
    if (!block) return;
    Array.prototype.forEach.call(strip.querySelectorAll(".ns-code__tab"), function (t) {
      var on = t === tab;
      t.setAttribute("aria-selected", on ? "true" : "false");
      t.tabIndex = on ? 0 : -1;
    });
    var panelId = tab.getAttribute("aria-controls");
    Array.prototype.forEach.call(block.querySelectorAll("[role='tabpanel']"), function (p) {
      p.hidden = p.id !== panelId;
    });
    var file = block.querySelector(".ns-code__file span");
    if (file) file.textContent = tab.textContent.trim();
  }
})();
