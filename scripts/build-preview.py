#!/usr/bin/env python3
"""Generate preview.html — the standalone design-system gallery.

Opens straight from disk (file://) against assets/built/screen.css, so you can
see every component and variant without Ghost running.
"""
import html as H
import pathlib

SECTIONS = []


def section(id_, title, note, *blocks):
    SECTIONS.append((id_, title, note, list(blocks)))


def spec(label, markup, wide=False):
    """One specimen: the rendered thing plus the class string under it."""
    return ("spec", label, markup, wide)


def row(*specs):
    return ("row", specs)


def note(text):
    return ("note", text)


# ── Buttons ──────────────────────────────────────────────────────────────────
section("button", "Button", "One solid button per screen. Press dims instantly — never a lift.",
    row(*[spec(f".ns-btn--{v}", f'<button class="ns-btn ns-btn--{v}">Enrol now</button>')
          for v in ("primary", "accent", "outline", "ghost")]),
    row(spec(".ns-btn--success", '<button class="ns-btn ns-btn--success">Complete</button>'),
        spec(".ns-btn--warning", '<button class="ns-btn ns-btn--warning">Review</button>'),
        spec(".ns-btn--danger", '<button class="ns-btn ns-btn--danger">Delete</button>'),
        spec(":disabled", '<button class="ns-btn ns-btn--primary" disabled>Disabled</button>')),
    row(*[spec(f"--{s}" if s else "(default)",
               f'<button class="ns-btn ns-btn--primary{" ns-btn--" + s if s else ""}">Size {s or "md"}</button>')
          for s in ("xs", "sm", "", "lg", "xl")]),
    row(spec("--pill", '<button class="ns-btn ns-btn--outline ns-btn--pill">Pill</button>'),
        spec("--sharp", '<button class="ns-btn ns-btn--outline ns-btn--sharp">Sharp</button>'),
        spec("--square", '<button class="ns-btn ns-btn--outline ns-btn--square"><i class="ph ph-arrow-right"></i></button>'),
        spec(".is-loading", '<button class="ns-btn ns-btn--primary is-loading">Saving</button>')),
    row(spec(".ns-btn-group",
             '<div class="ns-btn-group"><button class="ns-btn ns-btn--outline ns-btn--sm">Day</button>'
             '<button class="ns-btn ns-btn--outline ns-btn--sm">Week</button>'
             '<button class="ns-btn ns-btn--outline ns-btn--sm">Month</button></div>')),
    note("On dark grounds: <code>--white</code> and <code>--glass</code> — see the page header below."),
)

# ── Badge / chip / tag / kicker ──────────────────────────────────────────────
section("badge", "Badge", "Status is DATA: mono, uppercase, hairline-ringed — never a filled pastel wash.",
    row(*[spec(f"--{v}" if v else "(brand)",
               f'<span class="ns-badge{" ns-badge--" + v if v else ""}">{v or "brand"}</span>')
          for v in ("", "accent", "success", "warning", "danger", "neutral")]),
    row(spec("--dot", '<span class="ns-badge ns-badge--dot ns-badge--success">Live</span>'),
        spec("--solid", '<span class="ns-badge ns-badge--solid">Featured</span>'),
        spec("--pill", '<span class="ns-badge ns-badge--pill">Preview</span>'),
        spec("--sm / --lg", '<span class="ns-badge ns-badge--sm">sm</span> <span class="ns-badge ns-badge--lg">lg</span>')),
)

section("chip", "Chip", "The icon tile — the one place a faint brand wash is allowed, because it reads as a surface.",
    row(*[spec(f"--{s}" if s else "(default)",
               f'<span class="ns-chip{" ns-chip--" + s if s else ""}"><i class="ph-fill ph-code"></i></span>')
          for s in ("xs", "sm", "", "lg", "xl")]),
    row(*[spec(f"--{v}", f'<span class="ns-chip ns-chip--{v}"><i class="ph-fill ph-lightning"></i></span>')
          for v in ("accent", "neutral", "success", "warning", "danger", "solid")]),
    row(spec("--round", '<span class="ns-chip ns-chip--round"><i class="ph-fill ph-user"></i></span>'),
        spec("--sharp", '<span class="ns-chip ns-chip--sharp"><i class="ph-fill ph-terminal-window"></i></span>')),
)

section("tag", "Tag", "A tag IS a true pill — the one legitimate pill shape in a sharp system.",
    row(spec(".ns-tagchip", '<a class="ns-tagchip" href="#!">apex <b>12</b></a>'),
        spec("--sm", '<a class="ns-tagchip ns-tagchip--sm" href="#!">flow <b>7</b></a>'),
        spec("--lg", '<a class="ns-tagchip ns-tagchip--lg" href="#!">lwc <b>21</b></a>'),
        spec(".is-active", '<a class="ns-tagchip is-active" href="#!">integration <b>4</b></a>')),
)

section("kicker", "Kicker", "The section eyebrow written as a code comment — this is what replaces the pastel pill.",
    row(spec("(default)", '<span class="ns-kicker">Getting started</span>'),
        spec("--brand", '<span class="ns-kicker ns-kicker--brand">New</span>'),
        spec("--muted", '<span class="ns-kicker ns-kicker--muted">Archive</span>')),
    row(spec("--plain", '<span class="ns-kicker ns-kicker--plain">No slashes</span>'),
        spec("--dot", '<span class="ns-kicker ns-kicker--dot">Live now</span>'),
        spec("--sm / --lg", '<span class="ns-kicker ns-kicker--sm">small</span> &nbsp; <span class="ns-kicker ns-kicker--lg">large</span>')),
    row(spec("--rule", '<span class="ns-kicker ns-kicker--rule" style="width:min(28rem,100%)">Curriculum</span>', wide=True)),
)

# ── Card family ──────────────────────────────────────────────────────────────
CARD_BODY = ('<div class="ns-card__header"><h3 class="ns-card__title">Apex Programming</h3>'
             '<span class="ns-badge">Paid</span></div>'
             '<p class="ns-card__body" style="margin-top:.5rem;color:var(--color-muted);font-size:var(--size-small)">'
             'Bulk-safe patterns, governor limits, and tests that mean something.</p>'
             '<div class="ns-card__meta" style="margin-top:.85rem">12 lessons · 6h</div>')

section("card", "Card", "The system's box: a hairline border on a raised surface. No default shadow, no hover lift.",
    row(spec(".ns-card", f'<div class="ns-card" style="width:19rem">{CARD_BODY}</div>', wide=True),
        spec("--interactive", f'<div class="ns-card ns-card--interactive" style="width:19rem">{CARD_BODY}</div>', wide=True)),
    note("Hover the second one: the border goes brand and an accent line draws across the top."),
    row(spec("--sunken", f'<div class="ns-card ns-card--sunken" style="width:15rem">{CARD_BODY}</div>', wide=True),
        spec("--dark", f'<div class="ns-card ns-card--dark" style="width:15rem">{CARD_BODY}</div>', wide=True),
        spec("--dashed", f'<div class="ns-card ns-card--dashed" style="width:15rem">{CARD_BODY}</div>', wide=True)),
    row(spec("--grid", f'<div class="ns-card ns-card--grid" style="width:15rem">{CARD_BODY}</div>', wide=True),
        spec("--dots", f'<div class="ns-card ns-card--dots" style="width:15rem">{CARD_BODY}</div>', wide=True),
        spec("--lines", f'<div class="ns-card ns-card--lines" style="width:15rem">{CARD_BODY}</div>', wide=True)),
    row(spec("--rail", f'<div class="ns-card ns-card--rail" style="width:15rem">{CARD_BODY}</div>', wide=True),
        spec("--strong", f'<div class="ns-card ns-card--strong" style="width:15rem">{CARD_BODY}</div>', wide=True),
        spec("--interactive --row",
             '<div class="ns-card ns-card--interactive ns-card--row ns-card--sm" style="width:15rem">'
             '<div class="ns-card__title">Row card</div>'
             '<div class="ns-card__meta" style="margin-top:.35rem">accent on the left edge</div></div>', wide=True)),
    row(spec("--xs / --sm / --lg / --xl",
             "".join(f'<div class="ns-card ns-card--{s}" style="width:8rem"><span class="ns-card__meta">{s}</span></div>'
                     for s in ("xs", "sm", "lg", "xl")), wide=True)),
)

section("feature", "Feature", "Icon, title, one paragraph — a card preset for the &ldquo;what you get&rdquo; grids.",
    row(spec(".ns-feature",
             '<div class="ns-feature" style="width:17rem"><span class="ns-chip"><i class="ph-fill ph-graduation-cap"></i></span>'
             '<h3 class="ns-feature__title">Project-led</h3>'
             '<p class="ns-feature__body">Every lesson ends with something you built, not something you watched.</p>'
             '<a class="ns-feature__link" href="#!">Start learning <i class="ph ph-arrow-right"></i></a></div>', wide=True),
        spec("--row",
             '<div class="ns-feature ns-feature--row" style="width:19rem"><span class="ns-chip ns-chip--sm"><i class="ph-fill ph-users-three"></i></span>'
             '<div><h3 class="ns-feature__title">Community reviewed</h3>'
             '<p class="ns-feature__body">Drafts get a technical review before they go live.</p></div></div>', wide=True)),
)

section("quote", "Quote", "The testimonial card — distinct from the <code>&lt;blockquote&gt;</code> element inside article content.",
    row(spec(".ns-quote",
             '<figure class="ns-quote" style="width:19rem"><div class="ns-quote__stars">'
             + '<i class="ph-fill ph-star"></i>' * 5 + '</div>'
             '<blockquote class="ns-quote__body">&ldquo;I went from never having opened Setup to shipping my first Flow in a fortnight.&rdquo;</blockquote>'
             '<figcaption class="ns-quote__author"><span class="ns-chip ns-chip--sm ns-chip--round"><i class="ph-fill ph-user"></i></span>'
             '<div><p class="ns-quote__name">Priya R.</p><p class="ns-quote__role">Admin, Bengaluru</p></div></figcaption></figure>', wide=True),
        spec("--dark",
             '<figure class="ns-quote ns-quote--dark" style="width:19rem"><div class="ns-quote__stars">'
             + '<i class="ph-fill ph-star"></i>' * 5 + '</div>'
             '<blockquote class="ns-quote__body">&ldquo;The governor-limits lesson alone paid for the year.&rdquo;</blockquote>'
             '<figcaption class="ns-quote__author"><span class="ns-chip ns-chip--sm ns-chip--round"><i class="ph-fill ph-user"></i></span>'
             '<div><p class="ns-quote__name">Marcus T.</p><p class="ns-quote__role">Developer</p></div></figcaption></figure>', wide=True)),
)

section("widget", "Widget", "The boxes that stack in a sidebar — a card with a mono heading and a hairline under it.",
    row(spec(".ns-widget",
             '<div class="ns-widget" style="width:15rem"><div class="ns-widget__head"><span class="ns-widget__title">Explore</span></div>'
             '<a class="nav-link nav-link--block nav-link--sm" href="#!"><i class="ph ph-graduation-cap"></i>Courses</a>'
             '<a class="nav-link nav-link--block nav-link--sm" href="#!"><i class="ph ph-flow-arrow"></i>Training</a>'
             '<a class="nav-link nav-link--block nav-link--sm" href="#!"><i class="ph ph-books"></i>Docs</a></div>', wide=True),
        spec("--brand",
             '<div class="ns-widget ns-widget--brand" style="width:15rem"><div class="ns-widget__head"><span class="ns-widget__title">Newsletter</span></div>'
             '<input class="ns-input ns-input--sm" placeholder="you@email.com">'
             '<button class="ns-btn ns-btn--primary ns-btn--sm ns-btn--block" style="margin-top:.5rem">Subscribe</button></div>', wide=True),
        spec("--sunken",
             '<div class="ns-widget ns-widget--sunken" style="width:15rem"><div class="ns-widget__head"><span class="ns-widget__title">Popular</span></div>'
             '<div style="display:flex;flex-wrap:wrap;gap:.4rem">'
             '<a class="ns-tagchip ns-tagchip--sm" href="#!">apex</a><a class="ns-tagchip ns-tagchip--sm" href="#!">flow</a>'
             '<a class="ns-tagchip ns-tagchip--sm" href="#!">lwc</a></div></div>', wide=True)),
)

# ── Feedback ─────────────────────────────────────────────────────────────────
section("note", "Note", "The inline callout. A note is a BLOCK the reader should stop at, so it gets the one allowed tint — held at 4–6%.",
    *[row(spec(f"--{v}" if v else "(brand)",
               f'<div class="ns-note{" ns-note--" + v if v else ""}" style="width:min(34rem,100%)">'
               f'<i class="ns-note__icon ph-fill ph-{icon}"></i>'
               f'<div class="ns-note__body"><span class="ns-note__title">{title}</span> — {body}</div></div>', wide=True))
      for v, icon, title, body in (
          ("", "info", "Heads up", "this course assumes you've finished Admin Foundations."),
          ("success", "check-circle", "Section complete", "nice work — the next one unlocks automatically."),
          ("warning", "lock-simple", "Members only", "sign in to read the rest of this lesson."),
          ("danger", "warning-circle", "Deprecated", "this API version retires in Summer '26."),
          ("neutral", "note", "Note", "you can change this later in Setup."))],
)

section("empty", "Empty state", "A dashed edge says &ldquo;this will fill in&rdquo;; a solid one would say &ldquo;this is broken&rdquo;.",
    row(spec(".ns-empty",
             '<div class="ns-empty" style="width:min(34rem,100%)"><i class="ns-empty__icon ph ph-folder-open"></i>'
             '<p class="ns-empty__title">No lessons yet</p>'
             '<p class="ns-empty__body">Lessons for this section are being written.</p></div>', wide=True)),
    row(spec("--sm", '<div class="ns-empty ns-empty--sm" style="width:min(20rem,100%)">No results.</div>', wide=True),
        spec("--solid", '<div class="ns-empty ns-empty--solid ns-empty--sm" style="width:min(20rem,100%)">Nothing here.</div>', wide=True)),
)

section("stat", "Stat", "The spec-sheet readout. The value is always mono and tabular, so a row of them lines up.",
    row(spec(".ns-stats",
             '<div class="ns-stats">'
             + "".join(f'<div class="ns-stat"><span class="ns-stat__value">{v}</span><span class="ns-stat__label">{l}</span></div>'
                       for v, l in (("24", "courses"), ("312", "lessons"), ("9", "roadmaps"), ("100%", "free"))) +
             '</div>', wide=True)),
    row(spec("--lg --brand",
             '<div class="ns-stats"><div class="ns-stat ns-stat--lg ns-stat--brand"><span class="ns-stat__value">312</span>'
             '<span class="ns-stat__label">lessons</span></div></div>', wide=True),
        spec("--inline",
             '<div class="ns-stats ns-stats--tight"><div class="ns-stat ns-stat--inline"><i class="ns-stat__icon ph-fill ph-clock"></i>'
             '<b class="ns-stat__value" style="font-size:1.15rem">6h</b><span class="ns-stat__label">total</span></div></div>', wide=True)),
)

section("progress", "Progress", "A flat brand fill on a sunken track. Pair it with a mono readout — the number is the information.",
    row(spec(".ns-progress",
             '<div style="width:min(24rem,100%)"><div class="ns-progress"><span class="ns-progress__bar" style="width:70%"></span></div>'
             '<div class="ns-progress__label" style="margin-top:.4rem">7 / 10 · 70%</div></div>', wide=True)),
    row(*[spec(f"--{s}" if s else "(default)",
               f'<div style="width:9rem"><div class="ns-progress{" ns-progress--" + s if s else ""}">'
               f'<span class="ns-progress__bar" style="width:60%"></span></div></div>', wide=True)
          for s in ("xs", "sm", "", "lg")]),
    row(spec("--success", '<div style="width:9rem"><div class="ns-progress ns-progress--success"><span class="ns-progress__bar" style="width:100%"></span></div></div>', wide=True),
        spec("--warning", '<div style="width:9rem"><div class="ns-progress ns-progress--warning"><span class="ns-progress__bar" style="width:35%"></span></div></div>', wide=True)),
)

# ── Forms ────────────────────────────────────────────────────────────────────
section("input", "Input", "Sharp geometry, hairline border, a quiet brand focus ring. Works on input, textarea and select alike.",
    row(spec(".ns-input", '<input class="ns-input" placeholder="you@email.com" style="width:15rem">', wide=True),
        spec("--sm", '<input class="ns-input ns-input--sm" placeholder="small" style="width:11rem">', wide=True),
        spec("--lg", '<input class="ns-input ns-input--lg" placeholder="large" style="width:15rem">', wide=True)),
    row(spec("--error", '<input class="ns-input ns-input--error" value="not-an-email" style="width:15rem">', wide=True),
        spec("--success", '<input class="ns-input ns-input--success" value="you@email.com" style="width:15rem">', wide=True),
        spec(":disabled", '<input class="ns-input" value="Locked" disabled style="width:15rem">', wide=True)),
    row(spec(".ns-field",
             '<label class="ns-field" style="width:17rem"><span class="ns-field__label">Email address</span>'
             '<input class="ns-input" placeholder="you@email.com">'
             '<span class="ns-field__hint">We only use this for the sign-in link.</span></label>', wide=True),
        spec(".ns-input-icon",
             '<label class="ns-input-icon" style="width:17rem"><i class="ph ph-magnifying-glass"></i>'
             '<input class="ns-input" placeholder="Search lessons…"></label>', wide=True)),
    row(spec(".ns-input-group",
             '<div class="ns-input-group" style="width:19rem"><span class="ns-input-group__affix">/courses/</span>'
             '<input class="ns-input" placeholder="apex"></div>', wide=True),
        spec(".ns-check",
             '<label class="ns-check"><input type="checkbox" checked> Beginner</label> '
             '<label class="ns-check"><input type="checkbox"> Advanced</label>', wide=True)),
)

# ── Content components ───────────────────────────────────────────────────────
section("code", "Code window", "The Salesforce Developer Console rebuilt in CSS — navy bar, white file tab, all-blue token palette.",
    row(spec(".ns-code",
             '<div class="ns-code" style="width:min(38rem,100%)"><div class="ns-code__bar">'
             '<span class="ns-code__tab"><i class="ph ph-brackets-curly"></i>accounthandler.cls</span>'
             '<button class="ns-code__copy"><i class="ph ph-stack"></i>Copy</button></div>'
             '<pre><code>  <span class="tok-comment">// bulk-safe: one query, one update</span>\n'
             '  <span class="tok-keyword">public static void</span> <span class="tok-function">setRating</span>(<span class="tok-builtin">List</span>&lt;Account&gt; accs) {\n'
             '      <span class="tok-keyword">for</span> (Account a : accs) {\n'
             '          a.Rating = a.AnnualRevenue &gt; <span class="tok-number">1000000</span> ? <span class="tok-string">\'Hot\'</span> : <span class="tok-string">\'Warm\'</span>;\n'
             '      }\n'
             '      <span class="tok-keyword">update</span> accs;\n'
             '  }\n</code></pre></div>', wide=True)),
)

section("steps", "Steps &amp; timeline", "A stepper marks actions; a timeline marks moments. Both ride a hairline rail.",
    row(spec(".ns-steps",
             '<div class="ns-steps" style="width:min(26rem,100%);display:grid;gap:1rem">'
             + "".join(f'<div style="display:flex;gap:1rem;align-items:center"><span class="ns-step-num">{n}</span>'
                       f'<div><div style="font-weight:600">{t}</div>'
                       f'<div class="ns-card__meta">{m}</div></div></div>'
                       for n, t, m in ((1, "Create a free org", "5 min"), (2, "Build your first object", "20 min"), (3, "Automate it", "35 min"))) +
             '</div>', wide=True),
        spec(".ns-timeline",
             '<div class="ns-timeline" style="width:min(20rem,100%);display:grid;gap:1.1rem">'
             + "".join(f'<div style="display:flex;gap:1rem;align-items:center"><span class="ns-timeline__dot{on}"></span>'
                       f'<div><div style="font-weight:600;font-size:var(--size-small)">{t}</div>'
                       f'<div class="ns-card__meta">{d}</div></div></div>'
                       for t, d, on in (("Site launched", "Jan 2026", " is-on"), ("First course", "Mar 2026", " is-on"), ("Certificates", "Soon", ""))) +
             '</div>', wide=True)),
)

section("avatar", "Avatar", "A person is round; everything else in the system is sharp.",
    row(*[spec(f"--{s}" if s else "(default)",
               f'<span class="ns-avatar{" ns-avatar--" + s if s else ""}" style="display:inline-flex;align-items:center;justify-content:center">'
               f'<i class="ph-fill ph-user" style="color:var(--color-muted)"></i></span>')
          for s in ("xs", "sm", "", "lg", "xl")]),
    row(spec(".ns-ring", '<span class="ns-ring"><span class="ns-avatar ns-avatar--lg" style="display:inline-flex;align-items:center;justify-content:center"><i class="ph-fill ph-user" style="color:var(--color-muted)"></i></span></span>'),
        spec("--square", '<span class="ns-avatar ns-avatar--square ns-avatar--lg" style="display:inline-flex;align-items:center;justify-content:center"><i class="ph-fill ph-buildings" style="color:var(--color-muted)"></i></span>'),
        spec(".ns-avatar-stack",
             '<span class="ns-avatar-stack">'
             + '<span class="ns-avatar ns-avatar--sm" style="background:var(--color-brand-100)"></span>' * 3 + '</span>')),
)

# ── Chrome ───────────────────────────────────────────────────────────────────
section("nav", "Navigation chrome", "Nav rows, icon actions and the dropdown panel.",
    row(spec(".nav-link",
             '<div style="display:flex;gap:.25rem"><a class="nav-link is-current" href="#!"><i class="ph ph-house"></i>Home</a>'
             '<a class="nav-link" href="#!"><i class="ph ph-graduation-cap"></i>Courses</a>'
             '<a class="nav-link" href="#!"><i class="ph ph-flow-arrow"></i>Training</a></div>', wide=True)),
    row(spec(".icon-btn",
             '<div style="display:flex;gap:.4rem"><button class="icon-btn"><i class="ph ph-magnifying-glass"></i></button>'
             '<button class="icon-btn icon-btn--brand"><i class="ph ph-arrow-right"></i></button>'
             '<button class="icon-btn icon-btn--pink"><i class="ph-fill ph-heart"></i></button>'
             '<button class="icon-btn icon-btn--outline"><i class="ph ph-gear-six"></i></button>'
             '<button class="icon-btn is-active"><i class="ph ph-bell-ringing"></i></button></div>', wide=True),
        spec(".nav-tip (hover)",
             '<span class="group" style="position:relative;display:inline-flex"><button class="icon-btn"><i class="ph ph-info"></i></button>'
             '<span class="nav-tip">Help</span></span>', wide=True)),
    row(spec(".ns-menu",
             '<div style="position:relative;height:12.5rem;width:15rem">'
             '<div class="ns-menu" style="position:static;width:15rem">'
             '<div class="ns-menu__head"><div style="font-weight:700;font-size:var(--size-small)">Swarnil Singhai</div>'
             '<div style="font-size:.75rem;color:var(--color-muted)">member since 2026</div></div>'
             '<div class="ns-menu__group"><a class="ns-menu__item" href="#!"><i class="ph ph-user"></i>Account</a>'
             '<a class="ns-menu__item ns-menu__item--brand" href="#!"><i class="ph ph-user-circle"></i>Become an author</a></div>'
             '<div class="ns-menu__sep"></div>'
             '<a class="ns-menu__item ns-menu__item--quiet" href="#!"><i class="ph ph-x"></i>Sign out</a>'
             '</div></div>', wide=True),
        spec(".toc-link",
             '<nav style="width:14rem"><a class="toc-link is-active" href="#!">Getting started</a>'
             '<a class="toc-link" href="#!">The data model</a>'
             '<a class="toc-link is-h3" href="#!">Objects</a>'
             '<a class="toc-link is-h3" href="#!">Relationships</a></nav>', wide=True)),
)

section("furniture", "Page furniture", "The bands and rails that frame a page.",
    row(spec(".ns-page-header",
             '<div class="ns-page-header" style="border-radius:var(--radius-card)">'
             '<div class="ns-page-header__inner ns-page-header--sm" style="padding-block:2.5rem">'
             '<p class="ns-kicker ns-kicker--light ns-kicker--center"><i class="ph-fill ph-graduation-cap"></i>Courses</p>'
             '<h1 class="ns-page-header__title" style="font-size:2rem">Learn Salesforce properly</h1>'
             '<p class="ns-page-header__sub">Project-led courses, free forever.</p>'
             '<div class="ns-page-header__actions"><a class="ns-btn ns-btn--white" href="#!">Browse courses</a>'
             '<a class="ns-btn ns-btn--glass" href="#!">See the roadmap</a></div></div></div>', wide=True)),
    row(spec(".ns-section-head",
             '<div style="width:min(38rem,100%)"><div class="ns-section-head">'
             '<div><span class="ns-kicker">Catalog</span><h2 class="ns-section-head__title">Latest courses</h2>'
             '<p class="ns-section-head__sub">Everything published so far, newest first.</p></div>'
             '<a class="ns-btn ns-btn--outline ns-btn--sm ns-section-head__action" href="#!">See all</a></div></div>', wide=True)),
    row(spec(".ns-crumbs",
             '<nav class="ns-crumbs"><a class="ns-crumbs__link" href="#!"><i class="ph ph-house"></i>Home</a>'
             '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
             '<a class="ns-crumbs__link" href="#!"><i class="ph ph-tag"></i>Apex</a>'
             '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
             '<span class="ns-crumbs__current"><i class="ph ph-file-text"></i><span>Governor limits and bulk patterns</span></span></nav>', wide=True)),
    row(spec(".ns-pager",
             '<nav class="ns-pager"><a class="ns-pager__link" href="#!"><i class="ph ph-arrow-left"></i>Newer</a>'
             '<span class="ns-pager__count">Page 2 of 7</span>'
             '<a class="ns-pager__link" href="#!">Older<i class="ph ph-arrow-right"></i></a></nav>', wide=True)),
)

# ── Elements ─────────────────────────────────────────────────────────────────
section("elements", "Elements (layer 1)", "Bare HTML inside a reading context — no classes on any of these tags.",
    row(spec("prose", '''<div class="ns-prose" style="width:min(38rem,100%)">
<h2>The data model in one sentence</h2>
<p>Objects are tables, fields are columns, records are rows — and <a href="#!">relationships</a> are what make it a CRM rather than a spreadsheet. Press <kbd>Cmd</kbd> + <kbd>K</kbd> to search, or run <code>SELECT Id FROM Account</code>.</p>
<blockquote>A learning site doesn't need to look like the product it teaches.<cite>Namaste Salesforce</cite></blockquote>
<h3>Field types worth knowing</h3>
<ul><li>Picklist — when the set is closed</li><li>Lookup — a soft relationship</li><li>Master-detail — ownership and roll-ups</li></ul>
<ol><li>Create the object</li><li>Add the fields</li><li>Build the layout</li></ol>
<table><caption>Automation tools</caption>
<thead><tr><th>Tool</th><th>Use when</th><th>Cost</th></tr></thead>
<tbody><tr><td>Flow</td><td>Declarative logic</td><td>Low</td></tr>
<tr><td>Apex</td><td>Bulk, callouts, tests</td><td>High</td></tr></tbody></table>
<details><summary>Why not always Apex?</summary><p>Because every line of code is a line somebody has to maintain.</p></details>
<hr>
<p><small>Last reviewed March 2026.</small> <mark>Highlighted</mark> <abbr title="Salesforce Object Query Language">SOQL</abbr></p>
</div>''', wide=True)),
)

# ─────────────────────────────────────────────────────────────────────────────
def render_block(b):
    if b[0] == "note":
        return f'<p class="pv-note">{b[1]}</p>'
    out = ['<div class="pv-row">']
    for _, label, markup, wide in b[1]:
        cls = "pv-spec pv-spec--wide" if wide else "pv-spec"
        out.append(f'<div class="{cls}"><div class="pv-stage">{markup}</div>'
                   f'<code class="pv-label">{H.escape(label)}</code></div>')
    out.append("</div>")
    return "".join(out)


nav = "".join(f'<a href="#{i}">{t}</a>' for i, t, _, _ in SECTIONS)  # titles are already HTML
body = "".join(
    f'<section class="pv-section" id="{i}"><h2 class="pv-h2">{t}</h2>'
    f'<p class="pv-sub">{n}</p>{"".join(render_block(b) for b in bl)}</section>'
    for i, t, n, bl in SECTIONS)

PAGE = f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Developer Console — design system preview</title>
<!-- The theme's real built CSS. Nothing else: what you see here is exactly
     what the site ships. Run `yarn build` to refresh it. -->
<link rel="stylesheet" href="assets/built/screen.css">
<script>
  // Same pre-paint theme script the site uses, so dark mode never flashes.
  try {{
    var t = localStorage.getItem('ns-theme');
    if (t) document.documentElement.setAttribute('data-theme', t);
  }} catch (e) {{}}
</script>
<style>
  /* Preview chrome only — none of this ships with the theme. */
  .pv-wrap {{ max-width: 72rem; margin-inline: auto; padding: 2rem 1.25rem 6rem; }}
  .pv-top {{ position: sticky; top: 0; z-index: 50; background: color-mix(in srgb, var(--color-surface) 92%, transparent);
             backdrop-filter: blur(10px); border-bottom: 1px solid var(--color-border); }}
  .pv-top__bar {{ max-width: 72rem; margin-inline: auto; display: flex; align-items: center; gap: 1rem;
                  padding: .75rem 1.25rem; }}
  .pv-nav {{ display: flex; flex-wrap: wrap; gap: .15rem; margin-left: auto; }}
  .pv-nav a {{ font-family: var(--font-mono); font-size: .7rem; text-transform: uppercase;
               letter-spacing: .06em; color: var(--color-label); padding: .25rem .45rem;
               border-radius: var(--radius-btn); }}
  .pv-nav a:hover {{ color: var(--color-brand-600); background: color-mix(in srgb, var(--color-brand-500) 8%, transparent); }}
  .pv-section {{ padding-top: 3.5rem; scroll-margin-top: 4rem; }}
  .pv-h2 {{ font-family: var(--font-heading); font-size: 1.5rem; font-weight: 800; }}
  .pv-sub {{ margin-top: .35rem; color: var(--color-muted); font-size: var(--size-small); max-width: 46rem; }}
  .pv-note {{ margin-top: .75rem; font-size: var(--size-small); color: var(--color-muted); }}
  .pv-row {{ display: flex; flex-wrap: wrap; gap: 1.25rem 1.5rem; margin-top: 1.25rem; align-items: flex-end; }}
  .pv-spec {{ display: flex; flex-direction: column; gap: .5rem; }}
  .pv-stage {{ display: flex; align-items: center; gap: .5rem; flex-wrap: wrap; min-height: 2.5rem; }}
  .pv-spec--wide .pv-stage {{ display: block; }}
  .pv-label {{ font-family: var(--font-mono); font-size: .65rem; letter-spacing: .05em;
               color: var(--color-label); }}
  .pv-hero {{ padding: 2.5rem 0 1rem; border-bottom: 1px solid var(--color-border); }}
</style>
</head>
<body>

<div class="pv-top"><div class="pv-top__bar">
  <strong style="font-family:var(--font-mono);font-size:.8rem;letter-spacing:.04em">DEVELOPER&nbsp;CONSOLE</strong>
  <button class="ns-theme-toggle icon-btn" aria-label="Toggle dark mode" onclick="
    var h=document.documentElement, n = h.getAttribute('data-theme')==='dark'?'light':'dark';
    h.setAttribute('data-theme', n); try{{localStorage.setItem('ns-theme', n)}}catch(e){{}}">
    <svg class="dark:hidden" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1-9-9Z"/></svg>
    <svg class="hidden dark:block" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10Zm0-5v2m0 16v2M4.2 4.2l1.4 1.4m12.8 12.8 1.4 1.4M2 12h2m16 0h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
  </button>
  <nav class="pv-nav">{nav}</nav>
</div></div>

<div class="pv-wrap">
  <header class="pv-hero">
    <span class="ns-kicker">Design system</span>
    <h1 style="margin:.5rem 0 0;font-family:var(--font-heading);font-size:var(--size-h1);font-weight:800;line-height:var(--leading-tight)">Developer Console</h1>
    <p style="margin:.6rem 0 0;max-width:var(--container-prose);color:var(--color-muted);font-size:var(--size-body-lg);line-height:var(--leading-body)">
      Every component and variant the theme ships, rendered from
      <code>assets/built/screen.css</code>. Toggle dark mode above — the whole
      system flips to the brand navy console.
    </p>
    <div class="ns-stats ns-stats--tight" style="margin-top:1.25rem">
      <div class="ns-stat ns-stat--sm"><span class="ns-stat__value">4</span><span class="ns-stat__label">layers</span></div>
      <div class="ns-stat ns-stat--sm"><span class="ns-stat__value">36</span><span class="ns-stat__label">components</span></div>
      <div class="ns-stat ns-stat--sm"><span class="ns-stat__value">13</span><span class="ns-stat__label">element files</span></div>
      <div class="ns-stat ns-stat--sm"><span class="ns-stat__value">1</span><span class="ns-stat__label">signal colour</span></div>
    </div>
  </header>
  {body}
</div>

</body>
</html>
"""

pathlib.Path("preview.html").write_text(PAGE)

# ── Guard: every ph-* glyph used here must exist in the theme's SUBSETTED font,
#    otherwise it silently renders as a blank box (see CLAUDE.md "Icon font").
import re
subset = set(re.findall(r"\.(ph-[a-z0-9-]+)", pathlib.Path("assets/css/0-foundation/icons.css").read_text()))
used = set(re.findall(r"\b(ph-[a-z0-9-]+)", PAGE)) - {"ph-fill"}
missing = sorted(used - subset)
print(f"preview.html — {len(SECTIONS)} sections, {len(PAGE.splitlines())} lines, {len(used)} glyphs")
if missing:
    raise SystemExit("NOT IN THE ICON SUBSET (would render blank): " + ", ".join(missing)
                     + "\n  → pick another glyph, or add it to CONTENT_SAFELIST in"
                       " scripts/subset-icons.py and re-run it.")
print("all glyphs present in the subset")
