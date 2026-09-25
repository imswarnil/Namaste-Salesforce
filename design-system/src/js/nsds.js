/*  nsds.js — the optional runtime (~3 KB)
    ============================================================
    The system is CSS-first; this file only does what CSS cannot:
      · theme toggle        [data-theme-toggle]  → html[data-theme]
      · reader rail toggle  [data-rail-toggle]   → html[data-rail]
      · table of contents   [data-toc]           ← article h2/h3, scroll-spy
      · copy buttons        [data-copy]          ← nearest <pre>
      · quiz tally          .quiz-score          ← .quiz answers
      · toast               nsds.toast("…")
    Every feature checks for its markup and exits quietly.
    Apply the stored theme BEFORE paint with the inline snippet in
    <head>; this file only handles the click.
    ------------------------------------------------------------ */
(function () {
  "use strict";
  var doc = document, root = doc.documentElement;

  /* Theme */
  doc.querySelectorAll("[data-theme-toggle], .theme-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var cur = root.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      var next = cur === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("nsds-theme", next); } catch (e) {}
    });
  });

  /* Reader rail */
  doc.querySelectorAll("[data-rail-toggle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var closed = root.dataset.rail === "closed";
      root.dataset.rail = closed ? "open" : "closed";
      btn.setAttribute("aria-expanded", String(closed));
      try { localStorage.setItem("nsds-rail", root.dataset.rail); } catch (e) {}
    });
  });

  /* Table of contents + scroll-spy */
  var tocHost = doc.querySelector("[data-toc]");
  if (tocHost) {
    var article = doc.querySelector(tocHost.getAttribute("data-toc") || ".gh-content");
    var heads = article ? article.querySelectorAll("h2, h3") : [];
    if (!heads.length) {
      var w = tocHost.closest(".widget, .toc-inline, .player-toc, .docs-rail-group");
      (w || tocHost).remove();
    } else {
      var list = doc.createElement("ul");
      list.className = "toc-list";
      var links = [];
      heads.forEach(function (h) {
        if (!h.id) h.id = h.textContent.trim().toLowerCase().replace(/[^\w]+/g, "-").replace(/^-|-$/g, "");
        var li = doc.createElement("li");
        li.className = "toc-" + h.tagName.toLowerCase();
        var a = doc.createElement("a");
        a.href = "#" + h.id;
        a.textContent = h.textContent;
        li.appendChild(a);
        list.appendChild(li);
        links.push(a);
      });
      tocHost.appendChild(list);
      if ("IntersectionObserver" in window) {
        var current;
        var io = new IntersectionObserver(function (entries) {
          entries.forEach(function (en) {
            if (en.isIntersecting) {
              current = en.target.id;
              links.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === "#" + current); });
            }
          });
        }, { rootMargin: "-20% 0px -70% 0px", threshold: 0 });
        heads.forEach(function (h) { io.observe(h); });
      }
    }
  }

  /* Copy buttons */
  doc.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var sel = btn.getAttribute("data-copy");
      var src = sel ? doc.querySelector(sel) : (btn.closest(".specimen, .code-head, .browser") || btn.parentNode).querySelector("pre, .code, code");
      if (!src || !navigator.clipboard) return;
      navigator.clipboard.writeText(src.innerText).then(function () {
        var label = btn.innerHTML;
        btn.classList.add("is-copied");
        btn.innerHTML = "Copied";
        setTimeout(function () { btn.classList.remove("is-copied"); btn.innerHTML = label; }, 1600);
      });
    });
  });

  /* Quiz tally */
  doc.querySelectorAll(".quiz").forEach(function (quiz) {
    var score = quiz.querySelector(".quiz-score strong");
    if (!score) return;
    var qs = quiz.querySelectorAll(".quiz-q");
    var update = function () {
      var right = 0, answered = 0;
      qs.forEach(function (q) {
        var picked = q.querySelector("input:checked");
        if (picked) { answered++; if (picked.hasAttribute("data-correct")) right++; }
      });
      score.textContent = right + " / " + qs.length;
      quiz.dataset.answered = answered;
    };
    quiz.addEventListener("change", update);
    update();
  });

  /* Toast */
  var toastEl;
  window.nsds = window.nsds || {};
  window.nsds.toast = function (msg, ms) {
    if (!toastEl) {
      toastEl = doc.createElement("div");
      toastEl.className = "toast";
      toastEl.setAttribute("role", "status");
      doc.body.appendChild(toastEl);
    }
    toastEl.textContent = msg;
    toastEl.classList.add("is-open");
    clearTimeout(toastEl._t);
    toastEl._t = setTimeout(function () { toastEl.classList.remove("is-open"); }, ms || 2400);
  };

  /* Docs rail: a <details open> that closes itself below 992px */
  doc.querySelectorAll(".docs-rail details").forEach(function (d) {
    var mq = matchMedia("(min-width: 992px)");
    var sync = function () { d.open = mq.matches; };
    sync();
    mq.addEventListener("change", sync);
  });

  /* Close the mobile drawer on navigation / Escape */
  var navBox = doc.getElementById("nav-open");
  if (navBox) {
    doc.querySelectorAll(".site-head-nav a").forEach(function (a) { a.addEventListener("click", function () { navBox.checked = false; }); });
    doc.addEventListener("keydown", function (e) { if (e.key === "Escape") navBox.checked = false; });
  }
})();
