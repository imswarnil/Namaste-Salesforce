#!/usr/bin/env python3
"""build-styleguide.py — generate the Developer Console style guide.

A static site under styleguide/: a home page plus one page per foundation
topic and per component, sharing a sidebar, a theme toggle and prev/next
paging.

TWO RULES THIS GENERATOR ENFORCES, because the theme follows them too:

  1. No <style> blocks and no inline style attributes. Page chrome comes from
     assets/built/styleguide.css; specimen scaffolding uses the `demo-*`
     classes defined there. The build FAILS if a `style="` slips in.
  2. Every icon name must exist in partials/icons.hbs. The theme draws icons
     as INLINE SVG from that one partial — there is no icon font any more — so
     a name with no entry would render as nothing at all. Specimens here are
     still WRITTEN as `<i class="ph ph-name">`, because that is compact to
     type; render_icons() below rewrites them into the same inline SVG the
     theme ships, from the same source, so the guide cannot drift from it.

Edit THIS file, never the generated HTML. `yarn styleguide` regenerates.
"""
import pathlib
import re

OUT = pathlib.Path("styleguide")
PAGES = []

# ── The icon set ─────────────────────────────────────────────────────────────
# Read straight out of the partial the theme renders, so a specimen here IS the
# icon on the site — not a copy of it that has to be kept in step by hand.
ICONS = dict(re.findall(r'\{\{#match name "([a-z0-9-]+)"\}\}(.*?)\{\{/match\}\}',
                        pathlib.Path("partials/icons.hbs").read_text()))

# Specimens are written with Phosphor's old vocabulary because it is terser than
# the markup it stands for. This is the same mapping the templates were migrated
# through, kept only so the generator source stays readable.
ALIASES = {
    "magnifying-glass": "search", "envelope-simple": "mail", "users-three": "users",
    "rocket-launch": "rocket", "lock-simple": "lock", "lock-simple-open": "lock-open",
    "book-open-text": "book-open", "chat-circle-text": "chat", "chats-circle": "chats",
    "chart-line-up": "chart-line", "video-camera": "video", "crown-simple": "crown",
    "gear-six": "gear", "link-simple": "link", "share-network": "share",
    "paper-plane-tilt": "paper-plane", "rss-simple": "rss", "twitter-logo": "x-logo",
    "linkedin-logo": "linkedin", "facebook-logo": "facebook", "rows": "list",
    "globe-hemisphere-east": "globe", "flag-banner-fold": "flag", "strategy": "arrows-clockwise",
    "terminal-window": "terminal", "identification-badge": "user-circle", "note-pencil": "pen-nib",
    "chat-teardrop-text": "chat", "bookmark-simple": "book-bookmark", "list-bullets": "list",
    "dots-three": "list", "caret-up-down": "caret-down", "arrow-square-out": "arrow-up-right",
    "warning-circle": "warning", "bell-ringing": "megaphone", "note": "file-text",
}

WEIGHTS = {"ph", "ph-fill", "ph-bold", "ph-duotone", "ph-thin", "ph-light", "ph-regular"}


def icon(name, cls=""):
    """One inline SVG, drawn exactly as partials/icons.hbs draws it."""
    name = ALIASES.get(name, name)
    body = ICONS.get(name)
    if body is None:
        raise SystemExit(f"NO SUCH ICON: {name!r}\n  \u2192 add it to partials/icons.hbs, "
                         "or use one of: " + ", ".join(sorted(ICONS)))
    klass = "ns-icon" + (" " + cls if cls else "")
    return (f'<svg class="{klass}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true" focusable="false">{body}</svg>')


def render_icons(html):
    """Rewrite every `<i class="… ph-name …"></i>` specimen into inline SVG."""
    def one(m):
        keep, glyph = [], None
        for c in m.group(1).split():
            if c in WEIGHTS:
                continue
            if c.startswith("ph-") and glyph is None:
                glyph = c[3:]
                continue
            keep.append(c)
        if glyph is None:
            return m.group(0)
        return icon(glyph, " ".join(keep))
    return re.sub(r'<i class="([^"]*?)"\s*(?:aria-hidden="true")?\s*></i>', one, html)


# ── Page + block helpers ─────────────────────────────────────────────────────
def page(group, slug, title, blurb, *blocks):
    PAGES.append((group, slug, title, blurb, list(blocks)))


def spec(label, markup, wide=False, dark=False):
    return ("spec", label, markup, wide, dark)


def row(*specs):
    return ("row", specs)


def note(text):
    return ("note", text)


def head(text):
    return ("head", text)


def swatches(names):
    return ("swatches", names)


def tokens(names):
    return ("tokens", names)


# ═════════════════════════════════════════════════════════════════════════════
# FOUNDATION
# ═════════════════════════════════════════════════════════════════════════════
page("Foundation", "colors", "Colour",
     "One working blue carries every interactive meaning. Everything else is a surface, an ink, or a "
     "status — and status never becomes a background wash.",
     head("Brand scale"),
     swatches([f"--color-brand-{s}" for s in (50, 100, 200, 300, 400, 500, 600, 700, 800, 900)]),
     note("<code>--color-brand-500</code> is <code>#0176D3</code>, the one signal colour. 600 is the "
          "hover step; 900 is the navy that grounds dark mode and every hero."),
     head("Accent scale"),
     swatches([f"--color-accent-{s}" for s in (50, 100, 200, 300, 400, 500, 600, 700, 800, 900)]),
     note("Worth knowing: accent is currently a near-duplicate of brand — <code>--color-accent-500</code> "
          "is the same <code>#0176d3</code>. Consistent with &ldquo;one signal colour&rdquo;, but it does mean the "
          "<code>--accent</code> variants read almost identically to the default. Either give accent a "
          "genuinely different hue, or drop those variants."),
     head("Semantic roles"),
     note("These flip under <code>[data-theme=\"dark\"]</code>. Use the ROLE, never a literal — that is what "
          "makes dark mode work without a single <code>dark:</code> in markup."),
     swatches(["--color-surface", "--color-surface-raised", "--color-surface-sunken"]),
     swatches(["--color-ink", "--color-muted", "--color-label", "--color-border", "--color-grid"]),
     head("Status"),
     swatches(["--color-success", "--color-warning", "--color-error"]))

page("Foundation", "typography", "Typography",
     "Two materials on purpose: Inter for prose and headings, Fira Code for every index, label, "
     "duration and status. That is what makes data read as data without colour.",
     head("Prose scale — Inter"),
     *[row(spec(n, f'<span class="demo-type-display demo-type-display--{k}">{t}</span>', wide=True))
       for n, k, t in (("--size-display", "display", "Display"), ("--size-h1", "h1", "Heading 1"),
                       ("--size-h2", "h2", "Heading 2"), ("--size-h3", "h3", "Heading 3"),
                       ("--size-h4", "h4", "Heading 4"), ("--size-h5", "h5", "Heading 5"))],
     row(spec("--size-lead", '<span class="demo-type-lead">Lead paragraph — the sentence under a title.</span>', wide=True)),
     row(spec("--size-body", '<span class="demo-type-body">Body copy at the reading size.</span>', wide=True)),
     row(spec("--size-small", '<span class="demo-type-small">Small — metadata and captions.</span>', wide=True)),
     head("Label scale — Fira Code"),
     note("Uppercase, tracked, 700. Every kicker, index, timestamp, column header and status tag."),
     row(spec("ns-label", '<span class="ns-label">Lesson duration</span>'),
         spec("ns-index", '<span class="ns-index demo-index-lg">04</span>'),
         spec("--size-mono", '<code class="demo-type-mono">SELECT Id FROM Account</code>')),
     head("Weights, leading, tracking"),
     tokens(["--weight-heading", "--weight-semibold", "--weight-medium", "--weight-regular", "--weight-label"]),
     tokens(["--leading-tight", "--leading-heading", "--leading-body", "--tracking-label"]))

page("Foundation", "layout", "Layout &amp; grid",
     "How a page is measured: twelve columns, a gutter that scales with the viewport, and shells that "
     "are one column below <code>lg</code> and split above it.",
     head("The grid"),
     tokens(["--grid-columns", "--grid-gutter", "--grid-gutter-sm", "--grid-gutter-lg",
             "--grid-min", "--grid-min-sm", "--grid-min-lg"]),
     note("Twelve columns, because 12 divides by 2, 3, 4 and 6 — every layout the site needs falls out "
          "of it. The default <code>.ns-grid</code> reflows on CONTENT (<code>auto-fit</code> + "
          "<code>--grid-min</code>) rather than at a breakpoint you guessed."),
     head("Containers"),
     tokens(["--container-prose", "--container-narrow", "--container-page",
             "--layout-sidebar", "--layout-rail"]),
     head("Page rhythm"),
     tokens(["--space-section", "--space-section-sm", "--space-gutter", "--space-navbar"]),
     head("Component rhythm"),
     tokens(["--space-card", "--space-card-lg", "--space-gap", "--space-gap-sm", "--space-row"]),
     head("Breakpoints"),
     note("Tailwind's defaults, documented so custom media queries never invent a new one: "
          "<code>sm</code> 640 · <code>md</code> 768 · <code>lg</code> 1024 · <code>xl</code> 1280 · "
          "<code>2xl</code> 1536. <code>lg</code> is the important one — below it the site is a single "
          "column with drawers, at and above it rails and sidebars are permanent."))

page("Foundation", "borders", "Borders &amp; radii",
     "The hairline IS the structuring device. Geometry is sharp and specific — not "
     "&ldquo;12px and pills everywhere&rdquo;.",
     head("Widths"),
     row(spec("--border-hairline", '<div class="demo-box demo-box--hairline"></div>', wide=True),
         spec("--border-strong", '<div class="demo-box demo-box--strong"></div>', wide=True)),
     head("Radii"),
     row(*[spec(f"--radius-{k}", f'<div class="demo-radius demo-radius--{k}"></div>', wide=True)
           for k in ("card", "btn", "sm", "pill")]),
     note("Cards 6px, buttons and inputs 4px. <code>--radius-pill</code> is reserved for TRUE pills — "
          "tags, pager controls, avatars — never the default button or card."))

page("Foundation", "elevation", "Elevation",
     "Shadows are near-flat. Depth is expressed by a border going brand, not by a card floating off "
     "the page. Only genuinely floating layers — dropdowns, drawers — lift.",
     row(*[spec(f"--shadow-{k}", f'<div class="demo-shadow demo-shadow--{k}"></div>', wide=True)
           for k in ("card", "raised", "brand", "focus")]),
     head("The z-index ladder"),
     tokens(["--z-nav", "--z-subnav", "--z-dropdown", "--z-drawer", "--z-tooltip"]),
     note("Never write a raw z-index in a component — take the next rung, or add one here."))

page("Foundation", "motion", "Motion",
     "Fast and literal: state changes resolve in 120–180ms with a plain ease-out. No spring, no "
     "bounce, no hover lift. Everything is disabled under <code>prefers-reduced-motion</code>.",
     tokens(["--duration-fast", "--duration-base", "--ease-out", "--ease-out-strong"]),
     head("In use"),
     row(spec("ns-transition", '<div class="ns-card ns-card--sm ns-transition demo-w-sm">Hover me</div>', wide=True),
         spec(".ns-card--interactive", '<div class="ns-card ns-card--sm ns-card--interactive demo-w-sm">Hover me</div>', wide=True)),
     note("Keyframes the system ships: <code>fade-up</code>, <code>ns-float</code>, <code>marquee</code>, "
          "<code>ns-spin</code>."))

page("Foundation", "helpers", "Helpers &amp; mixins",
     "Recurring treatments defined once as Tailwind <code>@utility</code> recipes — usable as a class in "
     "markup AND via <code>@apply</code> inside component CSS. Tailwind covers the one-property "
     "utilities; these are the small PATTERNS that would otherwise be retyped every time.",
     head("Labels + markers"),
     row(spec("ns-label", '<span class="ns-label">Section label</span>'),
         spec("ns-index", '<span class="ns-index demo-index-lg">07</span>'),
         spec("ns-hairline", '<div class="ns-hairline demo-box"></div>')),
     head("Flow"),
     row(spec("ns-stack", '<div class="ns-stack demo-w-sm demo-grid-demo"><div>one</div><div>two</div></div>', wide=True),
         spec("ns-cluster", '<div class="ns-cluster demo-grid-demo"><div>tag</div><div>tag</div><div>tag</div></div>', wide=True),
         spec("ns-split", '<div class="ns-split demo-w-md demo-grid-demo"><div>start</div><div>end</div></div>', wide=True)),
     head("Text"),
     row(spec("ns-truncate", '<p class="ns-truncate demo-w-sm">A single line that is far too long to fit in this box and therefore truncates</p>', wide=True),
         spec("ns-clamp-2", '<p class="ns-clamp-2 demo-w-sm">Two lines maximum, after which the text is clipped so that a grid of cards keeps its rhythm no matter how long the copy runs.</p>', wide=True)),
     head("Aspect boxes"),
     row(*[spec(f"ns-aspect-{k}", f'<div class="ns-aspect-{k} demo-media demo-w-xs"><i class="ph ph-image"></i></div>', wide=True)
           for k in ("video", "square", "photo")]),
     note("Also here: <code>ns-center</code>, <code>ns-scroll-x</code>, <code>ns-snap-x</code>, "
          "<code>ns-sr-only</code>, <code>ns-anchor</code>, <code>ns-surface</code>, "
          "<code>ns-divide-y</code>, <code>ns-animate-in</code>, <code>ns-no-print</code>."))

page("Foundation", "icons", "Icons",
     "One partial, one <code>&lt;svg&gt;</code>, no third party. Every icon on the site is inline SVG "
     "drawn from <code>partials/icons.hbs</code> — there is no icon font, no CDN and no request "
     "before an icon paints. Rendered here straight from that file, so this page cannot go stale.",
     head("How to use one"),
     row(spec("default \u2014 1em, inherits colour",
              '<span class="ns-cluster">' + icon("rocket") + icon("graduation-cap") + icon("seal-check") + '</span>'),
         spec("sized with utilities",
              '<span class="ns-cluster">' + icon("rocket", "h-4 w-4") + icon("rocket", "h-6 w-6") + icon("rocket", "h-8 w-8") + '</span>'),
         spec("coloured by its container",
              '<span class="ns-cluster text-brand-600">' + icon("heart") + icon("star") + icon("check-circle") + '</span>')),
     note("<code>{{&gt; icons name=\"arrow-right\"}}</code> is the whole API. The "
          "<code>class</code> parameter adds utilities; <code>title</code> swaps "
          "<code>aria-hidden</code> for a label when the icon carries meaning the text does not. "
          "Every svg also carries <code>.ns-icon</code>, the design system\u2019s icon primitive: "
          "1em square, baseline-aligned, <code>flex: none</code>, <code>currentColor</code> \u2014 "
          "the same contract the app\u2019s sprite icons use."),
     head(f"The set \u2014 {len(ICONS)} icons"),
     row(*[spec(n, '<span class="demo-index-lg">' + icon(n) + '</span>')
           for n in sorted(ICONS)]),
     note("Adding one is adding a <code>{{#match name=\u2026}}</code> line to "
          "<code>partials/icons.hbs</code>: 24\u00d724 viewBox, stroke-width 1.7, round caps and "
          "joins, artwork inside a ~3px margin, <code>currentColor</code>. The brand marks at the "
          "foot of that file are the one exception \u2014 they are drawn solid, because that is how "
          "those marks are specified."))


# ═════════════════════════════════════════════════════════════════════════════
# COMPONENTS — basics
# ═════════════════════════════════════════════════════════════════════════════
page("Components", "button", "Button",
     "One solid button per screen, so the one solid thing reads as the one thing to click. Press is "
     "an instant opacity dim — never a lift.",
     head("Tone"),
     row(*[spec(f"--{v}", f'<button class="ns-btn ns-btn--{v}">Enrol now</button>')
           for v in ("primary", "accent", "outline", "ghost")]),
     row(spec("--success", '<button class="ns-btn ns-btn--success">Complete</button>'),
         spec("--warning", '<button class="ns-btn ns-btn--warning">Review</button>'),
         spec("--danger", '<button class="ns-btn ns-btn--danger">Delete</button>')),
     row(spec("--white", '<button class="ns-btn ns-btn--white">On navy</button>', dark=True),
         spec("--glass", '<button class="ns-btn ns-btn--glass">On navy</button>', dark=True)),
     head("Size"),
     row(*[spec(f"--{s}" if s else "(default)",
                f'<button class="ns-btn ns-btn--primary{" ns-btn--" + s if s else ""}">Size {s or "md"}</button>')
           for s in ("xs", "sm", "", "lg", "xl")]),
     head("Shape"),
     row(spec("--pill", '<button class="ns-btn ns-btn--outline ns-btn--pill">Pill</button>'),
         spec("--sharp", '<button class="ns-btn ns-btn--outline ns-btn--sharp">Sharp</button>'),
         spec("--square", '<button class="ns-btn ns-btn--outline ns-btn--square"><i class="ph ph-arrow-right"></i></button>')),
     row(spec("--block", '<button class="ns-btn ns-btn--outline ns-btn--block demo-w-sm">Full width</button>', wide=True)),
     head("Content"),
     row(spec("__icon", '<button class="ns-btn ns-btn--primary">Start learning <i class="ns-btn__icon ns-btn__icon--nudge ph ph-arrow-right"></i></button>'),
         spec("__media", '<button class="ns-btn ns-btn--outline"><span class="ns-avatar ns-avatar--sm demo-avatar-fill"></span>Swarnil</button>'),
         spec("__meta", '<button class="ns-btn ns-btn--outline">Lessons <span class="ns-btn__meta">12</span></button>')),
     head("State"),
     row(spec(":disabled", '<button class="ns-btn ns-btn--primary" disabled>Disabled</button>'),
         spec(".is-loading", '<button class="ns-btn ns-btn--primary is-loading">Saving</button>')),
     head("Group"),
     row(spec(".ns-btn-group",
              '<div class="ns-btn-group"><button class="ns-btn ns-btn--outline ns-btn--sm">Day</button>'
              '<button class="ns-btn ns-btn--outline ns-btn--sm">Week</button>'
              '<button class="ns-btn ns-btn--outline ns-btn--sm">Month</button></div>')))

page("Components", "badge", "Badge",
     "Status as DATA: mono, uppercase, hairline-ringed. Never a filled pastel wash — the ring carries "
     "the colour so the text stays legible on any surface.",
     head("Tone"),
     row(*[spec(f"--{v}" if v else "(brand)",
                f'<span class="ns-badge{" ns-badge--" + v if v else ""}">{v or "brand"}</span>')
           for v in ("", "accent", "success", "warning", "danger", "neutral")]),
     head("Form"),
     row(spec("--dot", '<span class="ns-badge ns-badge--dot ns-badge--success">Live</span>'),
         spec("--solid", '<span class="ns-badge ns-badge--solid">Featured</span>'),
         spec("--pill", '<span class="ns-badge ns-badge--pill">Preview</span>'),
         spec("--glass", '<span class="ns-badge ns-badge--glass">On media</span>', dark=True)),
     head("Size"),
     row(spec("--sm", '<span class="ns-badge ns-badge--sm">sm</span>'),
         spec("(default)", '<span class="ns-badge">md</span>'),
         spec("--lg", '<span class="ns-badge ns-badge--lg">lg</span>')))

page("Components", "chip", "Chip",
     "The icon tile that fronts a feature card or a list row. The one place a faint brand wash is "
     "allowed, because it reads as a surface rather than a status.",
     head("Size"),
     row(*[spec(f"--{s}" if s else "(default)",
                f'<span class="ns-chip{" ns-chip--" + s if s else ""}"><i class="ph-fill ph-code"></i></span>')
           for s in ("xs", "sm", "", "lg", "xl")]),
     head("Tone"),
     row(*[spec(f"--{v}", f'<span class="ns-chip ns-chip--{v}"><i class="ph-fill ph-lightning"></i></span>')
           for v in ("accent", "neutral", "success", "warning", "danger", "solid")]),
     head("Shape"),
     row(spec("--round", '<span class="ns-chip ns-chip--round"><i class="ph-fill ph-user"></i></span>'),
         spec("--sharp", '<span class="ns-chip ns-chip--sharp"><i class="ph-fill ph-terminal-window"></i></span>')))

page("Components", "tag", "Tag",
     "A tag IS a true pill — the one legitimate pill shape in a system that is otherwise sharp.",
     row(spec(".ns-tagchip", '<a class="ns-tagchip" href="#!">apex <b>12</b></a>'),
         spec("--sm", '<a class="ns-tagchip ns-tagchip--sm" href="#!">flow <b>7</b></a>'),
         spec("--lg", '<a class="ns-tagchip ns-tagchip--lg" href="#!">lwc <b>21</b></a>'),
         spec(".is-active", '<a class="ns-tagchip is-active" href="#!">integration <b>4</b></a>')))

page("Components", "kicker", "Kicker",
     "The section eyebrow written as a code comment: <code>// GETTING STARTED</code>. This is what "
     "replaces the pastel eyebrow pill.",
     head("Tone"),
     row(spec("(default)", '<span class="ns-kicker">Getting started</span>'),
         spec("--brand", '<span class="ns-kicker ns-kicker--brand">New</span>'),
         spec("--muted", '<span class="ns-kicker ns-kicker--muted">Archive</span>')),
     row(spec("--light", '<span class="ns-kicker ns-kicker--light">On navy</span>', dark=True)),
     head("Form"),
     row(spec("--plain", '<span class="ns-kicker ns-kicker--plain">No slashes</span>'),
         spec("--dot", '<span class="ns-kicker ns-kicker--dot">Live now</span>'),
         spec("--sm", '<span class="ns-kicker ns-kicker--sm">small</span>'),
         spec("--lg", '<span class="ns-kicker ns-kicker--lg">large</span>')),
     row(spec("--rule", '<span class="ns-kicker ns-kicker--rule demo-w-xl">Curriculum</span>', wide=True)))

page("Components", "avatar", "Avatar",
     "A person is round; everything else in the system is sharp. The ring marks an author or "
     "instructor, so use it sparingly.",
     head("Size"),
     row(*[spec(f"--{s}" if s else "(default)",
                f'<span class="ns-avatar{" ns-avatar--" + s if s else ""} demo-tile"><i class="ph-fill ph-user"></i></span>')
           for s in ("xs", "sm", "", "lg", "xl")]),
     head("Variants"),
     row(spec(".ns-ring", '<span class="ns-ring"><span class="ns-avatar ns-avatar--lg demo-tile"><i class="ph-fill ph-user"></i></span></span>'),
         spec("--square", '<span class="ns-avatar ns-avatar--square ns-avatar--lg demo-tile"><i class="ph-fill ph-buildings"></i></span>'),
         spec(".ns-avatar-stack", '<span class="ns-avatar-stack">'
              + '<span class="ns-avatar ns-avatar--sm demo-avatar-fill"></span>' * 3 + '</span>')))

# ── Layout ───────────────────────────────────────────────────────────────────
page("Components", "grid", "Grid &amp; shells",
     "The default grid reflows on CONTENT, not at a breakpoint you guessed — a 3-up becomes a 2-up "
     "becomes a 1-up on its own. Shells are the page skeletons: sidebar, rail, or both.",
     head("Content grid"),
     row(spec(".ns-grid (auto-fit)",
              '<div class="ns-grid demo-grid-demo demo-w-full"><div>auto</div><div>auto</div><div>auto</div><div>auto</div></div>', wide=True)),
     row(spec("--2", '<div class="ns-grid ns-grid--2 demo-grid-demo demo-w-full"><div>1</div><div>2</div></div>', wide=True)),
     row(spec("--3", '<div class="ns-grid ns-grid--3 demo-grid-demo demo-w-full"><div>1</div><div>2</div><div>3</div></div>', wide=True)),
     row(spec("--4", '<div class="ns-grid ns-grid--4 demo-grid-demo demo-w-full"><div>1</div><div>2</div><div>3</div><div>4</div></div>', wide=True)),
     head("Page shells"),
     row(spec("--sidebar", '<div class="ns-shell ns-shell--sidebar demo-grid-demo demo-w-full"><div>sidebar</div><div>content</div></div>', wide=True)),
     row(spec("--rail", '<div class="ns-shell ns-shell--rail demo-grid-demo demo-w-full"><div>content</div><div>rail</div></div>', wide=True)),
     row(spec("--both", '<div class="ns-shell ns-shell--both demo-grid-demo demo-w-full"><div>sidebar</div><div>content</div><div>rail</div></div>', wide=True)),
     note("Every shell is ONE column below <code>lg</code> — that rule is why the site has drawers on "
          "mobile. <code>.ns-shell__aside</code> makes a column sticky under the header."),
     head("Container + section"),
     row(spec(".ns-container--prose", '<div class="ns-container ns-container--prose demo-fill"><span class="ns-label">45rem — the reading column</span></div>', wide=True)),
     row(spec(".ns-container--narrow", '<div class="ns-container ns-container--narrow demo-fill"><span class="ns-label">34rem — centred CTAs</span></div>', wide=True)),
     row(spec(".ns-container", '<div class="ns-container demo-fill"><span class="ns-label">80rem — the page shell</span></div>', wide=True)),
     note("<code>.ns-section</code> supplies the vertical rhythm: <code>--sm</code>, <code>--lg</code>, "
          "<code>--flush</code>, plus <code>--sunken</code> / <code>--dark</code> grounds."))

page("Components", "hero", "Hero &amp; page header",
     "The top of a page — a full landing hero or the short band above a collection. The ground is "
     "always SOLID; depth comes from the pattern layer behind the copy, never a gradient.",
     head("Default — navy, centred"),
     row(spec(".ns-hero .ns-hero--sm .ns-hero--grid",
              '<div class="ns-hero ns-hero--sm ns-hero--grid">'
              '<div class="ns-hero__inner">'
              '<p class="ns-kicker ns-kicker--light ns-kicker--center"><i class="ph-fill ph-graduation-cap"></i>Courses</p>'
              '<h1 class="ns-hero__title">Learn Salesforce properly</h1>'
              '<p class="ns-hero__sub">Project-led courses, free forever.</p>'
              '<div class="ns-hero__actions"><a class="ns-btn ns-btn--white" href="#!">Browse courses</a>'
              '<a class="ns-btn ns-btn--glass" href="#!">See the roadmap</a></div></div></div>', wide=True)),
     head("Split — copy and media"),
     row(spec("--split",
              '<div class="ns-hero ns-hero--split ns-hero--sm ns-hero--dots">'
              '<div class="ns-hero__inner">'
              '<div><p class="ns-kicker ns-kicker--light">Training</p>'
              '<h1 class="ns-hero__title">Zero to your first automation</h1>'
              '<p class="ns-hero__sub">One guided path, nine sections, no prior experience.</p>'
              '<div class="ns-hero__actions"><a class="ns-btn ns-btn--white" href="#!">Start</a></div></div>'
              '<div class="ns-hero__media"><div class="ns-media ns-media--frame demo-media"><i class="ph ph-image"></i></div></div>'
              '</div></div>', wide=True)),
     head("A blended image"),
     note("<code>__bleed</code> fades an image into the trailing edge and puts a wash over it, so the "
          "title never lands on busy pixels and the SAME asset works on a navy hero and a light one — "
          "no second image, no dark-mode variant. Below <code>sm</code> it spans the full width at "
          "lower opacity, because there is no room for atmosphere beside the copy."),
     row(spec("__bleed",
              '<div class="ns-hero ns-hero--xs ns-hero--start ns-hero--section">'
              '<div class="ns-hero__bleed"><div class="demo-media demo-w-full" '
              'style-free="1"><i class="ph ph-image"></i></div></div>'
              '<div class="ns-hero__inner">'
              '<nav class="ns-crumbs ns-crumbs--sm ns-crumbs--light">'
              '<a class="ns-crumbs__link" href="#!"><i class="ph ph-house"></i></a>'
              '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
              '<a class="ns-crumbs__link" href="#!">Training</a>'
              '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
              '<span class="ns-crumbs__current"><span>Build Your First App</span></span></nav>'
              '<span class="ns-kicker ns-kicker--light">Training section</span>'
              '<h1 class="ns-hero__title">Build Your First App</h1>'
              '<p class="ns-hero__sub">A custom object, the fields that matter, and a report that '
              'proves it works.</p></div></div>', wide=True)),
     note("The breadcrumb lives HERE now, in the hero, rather than in a bar of its own under the main "
          "menu. One row of chrome fewer, and the crumb sits with the title it belongs to."),
     note("The trail is mono uppercase like every other label in the system, and the separator is a "
          "slash — the same mark the kicker uses, so it needs no icon and never fights the glyphs "
          "either side. The CURRENT page deliberately breaks that pattern, flipping to the sans face "
          "at full weight, so the eye lands on where you are rather than on how you got there."),
     head("Dark mode"),
     note("The navy hero does not invert — it goes DEEPER, and its hairline lifts instead of dropping. "
          "Inverting would collapse the hero and the page behind it into one flat field. The pattern "
          "lifts with it, and the image wash follows the new ground rather than the old navy, which is "
          "how one image keeps working in both themes."),
     note("<code>--flush</code> is what a section header uses: square corners, edge to edge, no gap "
          "above it, and an inner measure matching the reader below so the title lines up with the "
          "content. It sits ABOVE the reader rather than inside one of its columns — a page header "
          "belongs to the page, not to a column of it."),
     head("Light grounds"),
     row(spec("--plain", '<div class="ns-hero ns-hero--plain ns-hero--xs ns-hero--grid"><div class="ns-hero__inner">'
                         '<h1 class="ns-hero__title">On the page surface</h1>'
                         '<p class="ns-hero__sub">For pages that should not open with navy.</p></div></div>', wide=True)),
     row(spec("--sunken --start", '<div class="ns-hero ns-hero--sunken ns-hero--xs ns-hero--start"><div class="ns-hero__inner">'
                                  '<span class="ns-kicker">Docs</span>'
                                  '<h1 class="ns-hero__title">Help centre</h1></div></div>', wide=True)),
     note("Sizes: <code>--xs --sm --lg --xl --screen</code>. Layouts: <code>--center</code> (default), "
          "<code>--start</code>, <code>--split</code>. Patterns: <code>--grid --dots --lines</code>."))

page("Components", "section-head", "Section head",
     "The kicker + title + &ldquo;see all&rdquo; row that opens every band. One component, so the spacing above "
     "a section is identical everywhere — inconsistent rhythm is the fastest way for a page to feel "
     "assembled rather than designed.",
     row(spec(".ns-section-head",
              '<div class="demo-w-xl"><div class="ns-section-head">'
              '<div><span class="ns-kicker">Catalog</span><h2 class="ns-section-head__title">Latest courses</h2>'
              '<p class="ns-section-head__sub">Everything published so far, newest first.</p></div>'
              '<a class="ns-btn ns-btn--outline ns-btn--sm ns-section-head__action" href="#!">See all</a></div></div>', wide=True)),
     row(spec("--center",
              '<div class="demo-w-xl"><div class="ns-section-head ns-section-head--center">'
              '<div><span class="ns-kicker ns-kicker--center">How it works</span>'
              '<h2 class="ns-section-head__title">Three steps to your first app</h2></div></div></div>', wide=True)))

page("Components", "sections", "Content sections",
     "The marketing furniture a landing page is assembled from. Every one is a BAND: full-bleed "
     "ground, content constrained to the page measure, one vertical rhythm. Pages get built by "
     "stacking bands, not by inventing a wrapper each time.",
     head("Split — the workhorse row"),
     row(spec(".ns-split",
              '<div class="ns-band ns-band--sm ns-band--sunken"><div class="ns-band__inner">'
              '<div class="ns-split"><div class="ns-split__body">'
              '<span class="ns-kicker">Project-led</span>'
              '<h2 class="ns-split__title">You finish with something you built</h2>'
              '<p class="ns-split__lede">Every lesson ends in a working org, not a quiz score.</p>'
              '<ul class="ns-list ns-list--check ns-list--sm"><li class="ns-list__item">A real Developer org</li>'
              '<li class="ns-list__item">Code you can read back</li></ul>'
              '<div><a class="ns-btn ns-btn--primary ns-btn--sm" href="#!">Start free</a></div></div>'
              '<div class="ns-split__media"><div class="ns-media ns-media--frame demo-media"><i class="ph ph-image"></i></div></div>'
              '</div></div></div>', wide=True)),
     head("Steps across the page"),
     row(spec(".ns-steps-row",
              '<div class="ns-band ns-band--sm"><div class="ns-band__inner"><div class="ns-steps-row">'
              + "".join(f'<div class="ns-steps-row__item"><h3 class="ns-steps-row__title">{t}</h3>'
                        f'<p class="ns-steps-row__body">{b}</p></div>'
                        for t, b in (("Create a free org", "Five minutes, yours forever."),
                                     ("Build an object", "The data model, hands on."),
                                     ("Automate it", "Flow first, code when it earns it.")))
              + '</div></div></div>', wide=True)),
     head("Metrics"),
     row(spec(".ns-metrics",
              '<div class="ns-band ns-band--sm ns-band--dark ns-band--grid"><div class="ns-band__inner"><div class="ns-metrics">'
              + "".join(f'<div><div class="ns-metrics__value">{v}</div><div class="ns-metrics__label">{l}</div></div>'
                        for v, l in (("24", "courses"), ("312", "lessons"), ("9", "roadmaps"), ("100%", "free")))
              + '</div></div></div>', wide=True)),
     head("Logo strip"),
     row(spec(".ns-logos",
              '<div class="ns-band ns-band--sm ns-band--sunken"><div class="ns-band__inner"><div class="ns-logos">'
              + "".join(f'<span class="ns-logos__item"><i class="ph-fill ph-{i}"></i>{t}</span>'
                        for i, t in (("cloud", "Sales Cloud"), ("headset", "Service"), ("robot", "Agentforce"),
                                     ("database", "Data Cloud"), ("chart-line", "Analytics")))
              + '</div></div></div>', wide=True)),
     head("Comparison"),
     row(spec(".ns-compare",
              '<div class="ns-compare demo-w-full">'
              '<div class="ns-compare__col ns-compare__col--bad"><span class="ns-compare__title">Without a system</span>'
              '<ul class="ns-list ns-list--cross ns-list--sm demo-mt"><li class="ns-list__item">Every page invents its own spacing</li>'
              '<li class="ns-list__item">Six greys, four blues</li></ul></div>'
              '<div class="ns-compare__col ns-compare__col--good"><span class="ns-compare__title">With one</span>'
              '<ul class="ns-list ns-list--check ns-list--sm demo-mt"><li class="ns-list__item">One rhythm, everywhere</li>'
              '<li class="ns-list__item">One signal colour</li></ul></div></div>', wide=True)),
     head("Closing CTA"),
     row(spec(".ns-cta-band--dark",
              '<div class="ns-cta-band ns-cta-band--dark demo-w-full">'
              '<span class="ns-kicker ns-kicker--light ns-kicker--center">Free forever</span>'
              '<h2 class="ns-cta-band__title">Start with the fundamentals</h2>'
              '<p class="ns-cta-band__sub">No card, no trial — the whole beginner track is open.</p>'
              '<div class="ns-cta-band__actions"><a class="ns-btn ns-btn--white" href="#!">Create an account</a>'
              '<a class="ns-btn ns-btn--glass" href="#!">Browse first</a></div></div>', wide=True)),
     note("Band tones: <code>--plain --sunken --dark --brand</code>. Sizes: <code>--sm --lg --flush</code>. "
          "Patterns (<code>--grid --dots</code>) are for dark bands only — on a light ground they are noise."))

page("Components", "breadcrumb", "Breadcrumb",
     "Home / section / current page. One line that NEVER wraps — the current title truncates instead, "
     "because a breadcrumb that reflows pushes the article down on every narrow screen.",
     row(spec(".ns-crumbs",
              '<nav class="ns-crumbs"><a class="ns-crumbs__link" href="#!"><i class="ph ph-house"></i>Home</a>'
              '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
              '<a class="ns-crumbs__link" href="#!"><i class="ph ph-tag"></i>Apex</a>'
              '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
              '<span class="ns-crumbs__current"><i class="ph ph-file-text"></i><span>Governor limits and bulk patterns</span></span></nav>', wide=True)))

page("Components", "pagination", "Pagination",
     "Newer / Older plus a mono page count. Pills are legitimate here — a pager control is a discrete "
     "token, the same family as a tag.",
     row(spec(".ns-pager",
              '<nav class="ns-pager"><a class="ns-pager__link" href="#!"><i class="ph ph-arrow-left"></i>Newer</a>'
              '<span class="ns-pager__count">Page 2 of 7</span>'
              '<a class="ns-pager__link" href="#!">Older<i class="ph ph-arrow-right"></i></a></nav>', wide=True)))

# ── Containers ───────────────────────────────────────────────────────────────
CARD_BODY = ('<div class="ns-card__header"><h3 class="ns-card__title">Apex Programming</h3>'
             '<span class="ns-badge">Paid</span></div>'
             '<p class="ns-card__body demo-type-small">Bulk-safe patterns, governor limits, and tests that mean something.</p>'
             '<div class="ns-card__meta">12 lessons · 6h</div>')

page("Components", "card", "Card",
     "The system's box: a hairline border on a raised surface. The border IS the structure, so there "
     "is no default shadow and no hover lift. Every other box is a preset of this one.",
     head("Base + interactive"),
     row(spec(".ns-card", f'<div class="ns-card demo-w-md">{CARD_BODY}</div>', wide=True),
         spec("--interactive", f'<div class="ns-card ns-card--interactive demo-w-md">{CARD_BODY}</div>', wide=True)),
     note("Hover the second: the border goes brand and an accent line draws across the top. Add "
          "<code>--row</code> and the accent moves to the left edge instead."),
     head("With media and a footer"),
     row(spec("__media + __footer",
              '<div class="ns-card ns-card--interactive demo-w-md">'
              '<div class="ns-card__media demo-media"><i class="ph ph-image"></i>'
              '<span class="ns-card__badge ns-badge ns-badge--solid">New</span></div>'
              '<div class="ns-card__header"><h3 class="ns-card__title">Lightning Web Components</h3></div>'
              '<p class="ns-card__body demo-type-small">Modern web standards on the Salesforce platform.</p>'
              '<div class="ns-card__footer"><span class="ns-card__meta">9 lessons</span>'
              '<a class="ns-btn ns-btn--outline ns-btn--xs" href="#!">View</a></div></div>', wide=True),
         spec("__footer--flush",
              '<div class="ns-card demo-w-md">'
              '<div class="ns-card__media ns-card__media--photo demo-media"><i class="ph ph-image"></i></div>'
              '<h3 class="ns-card__title">Admin Foundations</h3>'
              '<p class="ns-card__body demo-type-small">Objects, fields, users and security.</p>'
              '<div class="ns-card__footer ns-card__footer--flush"><span class="ns-card__meta">Free</span>'
              '<span class="ns-card__meta">9h</span></div></div>', wide=True)),
     head("Surface"),
     row(spec("--sunken", f'<div class="ns-card ns-card--sunken demo-w-sm">{CARD_BODY}</div>', wide=True),
         spec("--dark", f'<div class="ns-card ns-card--dark demo-w-sm">{CARD_BODY}</div>', wide=True),
         spec("--dashed", f'<div class="ns-card ns-card--dashed demo-w-sm">{CARD_BODY}</div>', wide=True)),
     head("Pattern"),
     row(spec("--grid", f'<div class="ns-card ns-card--grid demo-w-sm">{CARD_BODY}</div>', wide=True),
         spec("--dots", f'<div class="ns-card ns-card--dots demo-w-sm">{CARD_BODY}</div>', wide=True),
         spec("--lines", f'<div class="ns-card ns-card--lines demo-w-sm">{CARD_BODY}</div>', wide=True)),
     head("Edge"),
     row(spec("--rail", f'<div class="ns-card ns-card--rail demo-w-sm">{CARD_BODY}</div>', wide=True),
         spec("--strong", f'<div class="ns-card ns-card--strong demo-w-sm">{CARD_BODY}</div>', wide=True)),
     head("Size"),
     row(spec("--xs / --sm / --lg / --xl",
              '<div class="ns-cluster">'
              + "".join(f'<div class="ns-card ns-card--{s} demo-w-xs"><span class="ns-card__meta">{s}</span></div>'
                        for s in ("xs", "sm", "lg", "xl")) + '</div>', wide=True)),
     note("Variants compose: a large interactive card on the grid pattern is "
          "<code>.ns-card .ns-card--lg .ns-card--interactive .ns-card--grid</code> — no new class."))

page("Components", "feature", "Feature",
     "Icon, title, one paragraph. A card preset for the &ldquo;what you get&rdquo; grids.",
     row(spec(".ns-feature",
              '<div class="ns-feature demo-w-md"><span class="ns-chip"><i class="ph-fill ph-graduation-cap"></i></span>'
              '<h3 class="ns-feature__title">Project-led</h3>'
              '<p class="ns-feature__body">Every lesson ends with something you built, not something you watched.</p>'
              '<a class="ns-feature__link" href="#!">Start learning <i class="ph ph-arrow-right"></i></a></div>', wide=True),
         spec("--row",
              '<div class="ns-feature ns-feature--row demo-w-md"><span class="ns-chip ns-chip--sm"><i class="ph-fill ph-users-three"></i></span>'
              '<div><h3 class="ns-feature__title">Community reviewed</h3>'
              '<p class="ns-feature__body">Drafts get a technical review before they go live.</p></div></div>', wide=True)))

TESTI_BODY = ('<div class="ns-testimonial__stars">' + '<i class="ph-fill ph-star"></i>' * 5 + '</div>'
              '<blockquote class="ns-testimonial__body">&ldquo;I went from never having opened Setup to '
              'shipping my first Flow in a fortnight.&rdquo;</blockquote>'
              '<figcaption class="ns-testimonial__author">'
              '<span class="ns-chip ns-chip--sm ns-chip--round"><i class="ph-fill ph-user"></i></span>'
              '<div><p class="ns-testimonial__name">Priya R.</p>'
              '<p class="ns-testimonial__role">Admin, Bengaluru</p></div></figcaption>')

page("Components", "testimonial", "Testimonial",
     "What a learner said, as social proof. Renamed from <code>.ns-quote</code> — the "
     "<a href=\"prose.html\">blockquote element</a> is the different thing, for quotations inside "
     "article content.",
     head("Card + plain"),
     row(spec(".ns-testimonial", f'<figure class="ns-testimonial demo-w-md">{TESTI_BODY}</figure>', wide=True),
         spec("--plain", f'<figure class="ns-testimonial ns-testimonial--plain demo-w-md">{TESTI_BODY}</figure>', wide=True)),
     head("Tones"),
     row(spec("--dark", f'<figure class="ns-testimonial ns-testimonial--dark demo-w-md">{TESTI_BODY}</figure>', wide=True),
         spec("--brand", f'<figure class="ns-testimonial ns-testimonial--brand demo-w-md">{TESTI_BODY}</figure>', wide=True)),
     head("Mark instead of stars"),
     row(spec("--mark", f'<figure class="ns-testimonial ns-testimonial--mark demo-w-md">{TESTI_BODY}</figure>', wide=True)),
     head("Wide — the single pull quote"),
     row(spec("--wide --dark",
              '<figure class="ns-testimonial ns-testimonial--wide ns-testimonial--dark demo-w-full">'
              '<blockquote class="ns-testimonial__body">&ldquo;The governor-limits lesson alone paid for the year.&rdquo;</blockquote>'
              '<figcaption class="ns-testimonial__author">'
              '<span class="ns-chip ns-chip--sm ns-chip--round"><i class="ph-fill ph-user"></i></span>'
              '<div><p class="ns-testimonial__name">Marcus T.</p><p class="ns-testimonial__role">Developer</p></div>'
              '</figcaption></figure>', wide=True)),
     head("A grid of them"),
     row(spec(".ns-testimonial-grid",
              '<div class="ns-testimonial-grid demo-w-full">'
              + f'<figure class="ns-testimonial ns-testimonial--sm">{TESTI_BODY}</figure>' * 3
              + '</div>', wide=True)))

page("Components", "widget", "Widgets",
     "The boxes that stack in a sidebar. One base — a card with a mono heading and a hairline under "
     "it — plus the presets the site actually uses.",
     head("Newsletter + tags"),
     row(spec("--newsletter",
              '<div class="ns-widget ns-widget--newsletter ns-widget--brand demo-w-sm">'
              '<div class="ns-widget__head"><span class="ns-widget__title"><i class="ph ph-envelope-simple"></i>Newsletter</span></div>'
              '<div class="ns-widget__body"><p>One email a fortnight. New lessons, nothing else.</p>'
              '<input class="ns-input ns-input--sm" placeholder="you@email.com">'
              '<button class="ns-btn ns-btn--primary ns-btn--sm ns-btn--block">Subscribe</button>'
              '<span class="ns-widget__note">No spam. Unsubscribe anytime.</span></div></div>', wide=True),
         spec("--tags",
              '<div class="ns-widget ns-widget--tags demo-w-sm">'
              '<div class="ns-widget__head"><span class="ns-widget__title">Topics</span>'
              '<a class="ns-widget__action" href="#!">All</a></div>'
              '<div class="ns-widget__body">'
              + "".join(f'<a class="ns-tagchip ns-tagchip--sm" href="#!">{t} <b>{n}</b></a>'
                        for t, n in (("apex", 12), ("flow", 7), ("lwc", 21), ("data", 5)))
              + '</div></div>', wide=True)),
     head("Author + contents"),
     row(spec("--author",
              '<div class="ns-widget ns-widget--author demo-w-sm">'
              '<div class="ns-widget__head"><span class="ns-widget__title">Written by</span></div>'
              '<div class="ns-widget__body"><span class="ns-avatar ns-avatar--lg demo-avatar-fill"></span>'
              '<div><p class="ns-widget__name">Swarnil Singhai</p>'
              '<p class="ns-widget__role">Salesforce Developer &amp; Architect</p></div></div></div>', wide=True),
         spec("--toc",
              '<div class="ns-widget ns-widget--toc demo-w-sm">'
              '<div class="ns-widget__head"><span class="ns-widget__title">On this page</span></div>'
              '<div class="ns-widget__body"><a class="ns-toc__link" aria-current="true" href="#!">The data model</a>'
              '<a class="ns-toc__link" href="#!">Relationships</a>'
              '<a class="ns-toc__link ns-toc__link--sub" href="#!">Lookup</a></div></div>', wide=True)),
     head("Stats + CTA"),
     row(spec("--stats",
              '<div class="ns-widget ns-widget--stats demo-w-sm">'
              '<div class="ns-widget__head"><span class="ns-widget__title">This course</span></div>'
              '<div class="ns-widget__body">'
              + "".join(f'<div class="ns-widget__row"><span>{l}</span><span class="ns-widget__num">{v}</span></div>'
                        for l, v in (("Lessons", "12"), ("Duration", "6h"), ("Level", "Int.")))
              + '</div></div>', wide=True),
         spec("--cta --dark",
              '<div class="ns-widget ns-widget--cta ns-widget--dark demo-w-sm">'
              '<div class="ns-widget__head"><span class="ns-widget__title">Members</span></div>'
              '<div class="ns-widget__body"><p>Unlock every paid course.</p>'
              '<a class="ns-btn ns-btn--white ns-btn--sm" href="#!">Join</a></div></div>', wide=True)),
     note("Tones: <code>--plain --sunken --brand --dark</code>. <code>--sticky</code> pins a widget "
          "under the header on <code>lg</code> and up."))

page("Components", "note", "Note",
     "The inline callout. Badges may never carry a status wash, but a note is a BLOCK the reader is "
     "meant to stop at — so it gets one tint, held at 4–6%, with the colour carried by the border "
     "and the icon.",
     *[row(spec(f"--{v}" if v else "(brand)",
                f'<div class="ns-note{" ns-note--" + v if v else ""} demo-w-xl">'
                f'<i class="ns-note__icon ph-fill ph-{icon}"></i>'
                f'<div class="ns-note__body"><span class="ns-note__title">{title}</span> — {body}</div></div>', wide=True))
       for v, icon, title, body in (
           ("", "info", "Heads up", "this course assumes you have finished Admin Foundations."),
           ("success", "check-circle", "Section complete", "nice work — the next one unlocks automatically."),
           ("warning", "lock", "Members only", "sign in to read the rest of this lesson."),
           ("danger", "warning-circle", "Deprecated", "this API version retires in Summer 26."),
           ("neutral", "note", "Note", "you can change this later in Setup."))])

page("Components", "empty-state", "Empty state",
     "A dashed hairline says <em>this will fill in</em>, where a solid one would say <em>this is broken</em>.",
     row(spec(".ns-empty",
              '<div class="ns-empty demo-w-xl"><i class="ns-empty__icon ph ph-folder-open"></i>'
              '<p class="ns-empty__title">No lessons yet</p>'
              '<p class="ns-empty__body">Lessons for this section are being written.</p>'
              '<a class="ns-btn ns-btn--outline ns-btn--sm ns-empty__action" href="#!">Browse courses</a></div>', wide=True)),
     row(spec("--sm", '<div class="ns-empty ns-empty--sm demo-w-sm">No results.</div>', wide=True),
         spec("--solid", '<div class="ns-empty ns-empty--solid ns-empty--sm demo-w-sm">Nothing here.</div>', wide=True)))


def acc(cls="", n=3, open_first=True):
    items = [("Why not always Apex?", "Because every line of code is a line somebody has to maintain."),
             ("Can I use Flow for everything?", "Almost. Bulk operations and callouts still want code."),
             ("Do I need a paid org?", "No — a Developer Edition org is free and never expires.")][:n]
    out = [f'<div class="ns-accordion {cls} demo-w-xl">']
    for i, (q, a) in enumerate(items):
        op = " open" if (open_first and i == 0) else ""
        out.append(f'<details class="ns-accordion__item"{op}>'
                   f'<summary class="ns-accordion__summary">'
                   f'<i class="ns-accordion__icon ph ph-caret-right"></i>'
                   f'<span class="ns-accordion__title">{q}</span></summary>'
                   f'<div class="ns-accordion__body"><div><div class="ns-accordion__body-inner">{a}</div></div></div>'
                   f'</details>')
    out.append('</div>')
    return "".join(out)


page("Components", "accordion", "Accordion",
     "Built on <code>&lt;details&gt;</code>, so it works with no JavaScript, is keyboard operable for "
     "free, and is findable by in-page search when open. The panel animates with "
     "<code>grid-template-rows: 0fr → 1fr</code> — the only way to transition to an unknown height "
     "without measuring it in JS.",
     head("Default"),
     row(spec(".ns-accordion", acc(), wide=True)),
     head("Flush — the FAQ shape"),
     row(spec("--flush", acc("ns-accordion--flush"), wide=True)),
     head("Size + tone"),
     row(spec("--sm", acc("ns-accordion--sm", n=2), wide=True)),
     row(spec("--lg --sunken", acc("ns-accordion--lg ns-accordion--sunken", n=2), wide=True)),
     note("The marker rotates rather than swapping glyphs — one element, no flash. Under "
          "<code>prefers-reduced-motion</code> the panel opens instantly and correctly."))

# ── Data ─────────────────────────────────────────────────────────────────────
page("Components", "stat", "Stat",
     "A number and what it counts. The value is ALWAYS mono and tabular so a row of them lines up — "
     "this readout is what makes the site read as a console rather than a brochure.",
     head("Row"),
     row(spec(".ns-stats",
              '<div class="ns-stats">'
              + "".join(f'<div class="ns-stat"><span class="ns-stat__value">{v}</span><span class="ns-stat__label">{l}</span></div>'
                        for v, l in (("24", "courses"), ("312", "lessons"), ("9", "roadmaps"), ("100%", "free")))
              + '</div>', wide=True)),
     head("Divided"),
     row(spec("--divided",
              '<div class="ns-stats ns-stats--divided">'
              + "".join(f'<div class="ns-stat ns-stat--sm"><span class="ns-stat__value">{v}</span><span class="ns-stat__label">{l}</span></div>'
                        for v, l in (("12", "lessons"), ("6h", "duration"), ("Int.", "level")))
              + '</div>', wide=True)),
     head("Cards with a trend"),
     row(spec("--cards",
              '<div class="ns-stats ns-stats--cards demo-w-full">'
              + "".join(f'<div class="ns-stat ns-stat--stacked"><span class="ns-stat__value">{v}</span>'
                        f'<span class="ns-stat__label">{l}</span>'
                        f'<span class="ns-stat__delta ns-stat__delta--{d}">{p}</span></div>'
                        for v, l, d, p in (("312", "lessons", "up", "12 this month"),
                                           ("4.9", "rating", "up", "0.2"),
                                           ("1.2k", "learners", "up", "8%"),
                                           ("3", "open issues", "down", "2")))
              + '</div>', wide=True)),
     head("Size + tone"),
     row(spec("--xl --brand",
              '<div class="ns-stat ns-stat--xl ns-stat--brand"><span class="ns-stat__value">312</span>'
              '<span class="ns-stat__label">lessons</span></div>', wide=True),
         spec("--inline",
              '<div class="ns-stat ns-stat--inline"><i class="ns-stat__icon ph-fill ph-clock"></i>'
              '<span class="ns-stat__value">6h</span><span class="ns-stat__label">total</span></div>', wide=True),
         spec("--light",
              '<div class="ns-stat ns-stat--light"><span class="ns-stat__value">100%</span>'
              '<span class="ns-stat__label">free</span></div>', dark=True)))

page("Components", "progress", "Progress",
     "Course and track completion. A flat brand fill on the sunken track. Pair it with a mono "
     "readout — the number is the information, the bar is just its shape.",
     row(spec(".ns-progress",
              '<div class="demo-w-lg"><div class="ns-progress"><span class="ns-progress__bar" data-demo-width="70"></span></div>'
              '<div class="ns-progress__label demo-mt">7 / 10 · 70%</div></div>', wide=True)),
     head("Size"),
     row(*[spec(f"--{s}" if s else "(default)",
                f'<div class="demo-w-xs"><div class="ns-progress{" ns-progress--" + s if s else ""}">'
                f'<span class="ns-progress__bar" data-demo-width="60"></span></div></div>', wide=True)
           for s in ("xs", "sm", "", "lg")]),
     head("Tone"),
     row(spec("--success", '<div class="demo-w-xs"><div class="ns-progress ns-progress--success"><span class="ns-progress__bar" data-demo-width="100"></span></div></div>', wide=True),
         spec("--warning", '<div class="demo-w-xs"><div class="ns-progress ns-progress--warning"><span class="ns-progress__bar" data-demo-width="35"></span></div></div>', wide=True)))

page("Components", "table", "Table",
     "A table is a spec sheet: hairline rows, mono uppercase headers, tabular numerals, and a faint "
     "brand tint on row hover so the eye can track across. No zebra striping by default — the "
     "hairline already separates the rows.",
     head("Default"),
     row(spec(".ns-table",
              '<div class="ns-table__wrap demo-w-xl"><table class="ns-table">'
              '<caption>Automation tools</caption>'
              '<thead><tr><th>Tool</th><th>Use when</th><th class="ns-table__num">Cost</th></tr></thead>'
              '<tbody>'
              '<tr><td>Flow</td><td>Declarative logic, most of the time</td><td class="ns-table__num">1</td></tr>'
              '<tr><td>Apex</td><td>Bulk, callouts, real tests</td><td class="ns-table__num">12</td></tr>'
              '<tr><td>Nothing</td><td>The requirement is a report</td><td class="ns-table__num">0</td></tr>'
              '</tbody></table></div>', wide=True)),
     head("Bordered"),
     row(spec("--bordered --sm",
              '<div class="ns-table__wrap demo-w-xl"><table class="ns-table ns-table--bordered ns-table--sm">'
              '<thead><tr><th>Field</th><th>Type</th><th>Required</th></tr></thead>'
              '<tbody><tr><td>Name</td><td>Text(80)</td><td>Yes</td></tr>'
              '<tr><td>Stage</td><td>Picklist</td><td>Yes</td></tr>'
              '<tr><td>Amount</td><td>Currency</td><td>No</td></tr></tbody></table></div>', wide=True)),
     head("Striped"),
     row(spec("--striped",
              '<div class="ns-table__wrap demo-w-xl"><table class="ns-table ns-table--striped">'
              '<thead><tr><th>Limit</th><th class="ns-table__num">Sync</th><th class="ns-table__num">Async</th></tr></thead>'
              '<tbody><tr><td>SOQL queries</td><td class="ns-table__num">100</td><td class="ns-table__num">200</td></tr>'
              '<tr><td>DML statements</td><td class="ns-table__num">150</td><td class="ns-table__num">150</td></tr>'
              '<tr><td>CPU time (ms)</td><td class="ns-table__num">10,000</td><td class="ns-table__num">60,000</td></tr></tbody></table></div>', wide=True)),
     note("<code>--cards</code> restacks each row into a labelled card below <code>md</code> (cells carry "
          "<code>data-label</code>) — a wide table on a phone is unreadable any other way."))

page("Components", "list", "List",
     "Lists you build in a template, marked deliberately — as opposed to the bare "
     "<code>&lt;ul&gt;</code>/<code>&lt;ol&gt;</code> element, which styles what an author writes in a post.",
     head("Markers"),
     row(*[spec(f"--{k}",
                f'<ul class="ns-list ns-list--{k} demo-w-sm">'
                + "".join(f'<li class="ns-list__item">{t}</li>' for t in ("First item", "Second item", "Third item"))
                + '</ul>', wide=True)
           for k in ("check", "cross", "dot", "arrow", "num")]),
     head("Forms"),
     row(spec("--boxed",
              '<ul class="ns-list ns-list--boxed demo-w-md">'
              '<li class="ns-list__item"><span class="ns-list__title">Objects and fields</span><span class="ns-list__meta">12m</span></li>'
              '<li class="ns-list__item"><span class="ns-list__title">Users and profiles</span><span class="ns-list__meta">18m</span></li>'
              '<li class="ns-list__item"><span class="ns-list__title">Sharing model</span><span class="ns-list__meta">24m</span></li></ul>', wide=True),
         spec("--divided",
              '<ul class="ns-list ns-list--divided demo-w-md">'
              '<li class="ns-list__item"><span class="ns-list__title">Apex</span><span class="ns-list__meta">12</span></li>'
              '<li class="ns-list__item"><span class="ns-list__title">Flow</span><span class="ns-list__meta">7</span></li></ul>', wide=True)),
     head("Grouped by section"),
     row(spec(".ns-list-group",
              '<div class="ns-list-group demo-w-md">'
              '<div><span class="ns-list-group__title">Getting started</span>'
              '<ul class="ns-list ns-list--arrow ns-list--sm"><li class="ns-list__item">Create your account</li>'
              '<li class="ns-list__item">Find your way around</li></ul></div>'
              '<div><span class="ns-list-group__title">Courses</span>'
              '<ul class="ns-list ns-list--arrow ns-list--sm"><li class="ns-list__item">How a course is structured</li>'
              '<li class="ns-list__item">Free and members-only lessons</li></ul></div></div>', wide=True)),
     note("<code>--inline</code> makes a wrapping row; <code>--grid</code> splits into two columns from "
          "<code>sm</code>; <code>--icon</code> takes a per-item <code>.ns-list__icon</code>."))


def steps_items(marker="", n=3):
    data = [("Create a free org", "5 min"), ("Build your first object", "20 min"), ("Automate it", "35 min")][:n]
    icons = ["ph-cloud", "ph-database", "ph-flow-arrow"]
    out = []
    for i, (t, m) in enumerate(data):
        inner = f'<i class="ph-fill {icons[i]}"></i>' if marker == "icon" else ""
        out.append(f'<div class="ns-steps__item"><span class="ns-steps__marker">{inner}</span>'
                   f'<div class="ns-steps__body"><div class="ns-steps__title">{t}</div>'
                   f'<div class="ns-steps__meta">{m}</div></div></div>')
    return "".join(out)


page("Components", "steps", "Steps",
     "A numbered procedure. The rail is a hairline; the markers sit on it. Steps mark ACTIONS in "
     "order — if you are showing moments rather than actions, use the "
     "<a href=\"timeline.html\">timeline</a>.",
     head("Vertical — number, icon, dot"),
     row(spec("--number", f'<div class="ns-steps ns-steps--number demo-w-md">{steps_items()}</div>', wide=True),
         spec("--icon", f'<div class="ns-steps ns-steps--icon demo-w-md">{steps_items("icon")}</div>', wide=True),
         spec("--dot", f'<div class="ns-steps ns-steps--dot demo-w-md">{steps_items()}</div>', wide=True)),
     head("Horizontal"),
     row(spec("--horizontal --number",
              f'<div class="ns-steps ns-steps--horizontal ns-steps--number demo-w-full">{steps_items()}</div>', wide=True)),
     head("Size + style"),
     row(spec("--sm --quiet", f'<div class="ns-steps ns-steps--sm ns-steps--quiet ns-steps--number demo-w-sm">{steps_items(n=2)}</div>', wide=True),
         spec("--lg --square", f'<div class="ns-steps ns-steps--lg ns-steps--square ns-steps--number demo-w-sm">{steps_items(n=2)}</div>', wide=True)),
     note("<code>--letter</code> counts A, B, C. <code>.is-done</code> and <code>.is-current</code> mark "
          "progress on an item."))


def tl_items():
    data = [("Site launched", "Jan 2026", "is-on"), ("First course", "Mar 2026", "is-on"),
            ("Certificates", "Soon", "is-next")]
    return "".join(
        f'<div class="ns-timeline__item {st}"><span class="ns-timeline__dot"></span>'
        f'<div class="ns-timeline__body"><div class="ns-timeline__title">{t}</div>'
        f'<div class="ns-timeline__meta">{d}</div></div></div>' for t, d, st in data)


page("Components", "timeline", "Timeline",
     "Moments in order: a changelog, a roadmap, a course history. Same rail as the stepper, "
     "different intent — a timeline marks MOMENTS, a stepper marks actions you take.",
     head("Vertical"),
     row(spec(".ns-timeline", f'<div class="ns-timeline demo-w-md">{tl_items()}</div>', wide=True),
         spec("--icon", f'<div class="ns-timeline ns-timeline--icon demo-w-md">{tl_items()}</div>', wide=True)),
     head("Horizontal"),
     row(spec("--horizontal", f'<div class="ns-timeline ns-timeline--horizontal demo-w-full">{tl_items()}</div>', wide=True)),
     head("Rail placement"),
     row(spec("--dashed", f'<div class="ns-timeline ns-timeline--dashed demo-w-sm">{tl_items()}</div>', wide=True),
         spec("--right", f'<div class="ns-timeline ns-timeline--right demo-w-sm">{tl_items()}</div>', wide=True)))

# ── Forms ────────────────────────────────────────────────────────────────────
page("Components", "input", "Input",
     "Sharp geometry, hairline border, a quiet brand focus ring. Works on <code>input</code>, "
     "<code>textarea</code> and <code>select</code> alike.",
     head("Size"),
     row(spec("--sm", '<input class="ns-input ns-input--sm demo-w-sm" placeholder="small">', wide=True),
         spec("(default)", '<input class="ns-input demo-w-sm" placeholder="you@email.com">', wide=True),
         spec("--lg", '<input class="ns-input ns-input--lg demo-w-sm" placeholder="large">', wide=True)),
     head("State"),
     row(spec("--error", '<input class="ns-input ns-input--error demo-w-sm" value="not-an-email">', wide=True),
         spec("--success", '<input class="ns-input ns-input--success demo-w-sm" value="you@email.com">', wide=True),
         spec(":disabled", '<input class="ns-input demo-w-sm" value="Locked" disabled>', wide=True)),
     head("Field + affixes"),
     row(spec(".ns-field",
              '<label class="ns-field demo-w-md"><span class="ns-field__label">Email address</span>'
              '<input class="ns-input" placeholder="you@email.com">'
              '<span class="ns-field__hint">We only use this for the sign-in link.</span></label>', wide=True),
         spec(".ns-input-icon",
              '<label class="ns-input-icon demo-w-md"><i class="ph ph-magnifying-glass"></i>'
              '<input class="ns-input" placeholder="Search lessons…"></label>', wide=True)),
     row(spec(".ns-input-group",
              '<div class="ns-input-group demo-w-md"><span class="ns-input-group__affix">/courses/</span>'
              '<input class="ns-input" placeholder="apex"></div>', wide=True),
         spec("textarea",
              '<textarea class="ns-input demo-w-md" placeholder="Tell us what you are stuck on…"></textarea>', wide=True)))

page("Components", "control", "Checkbox, radio &amp; switch",
     "Native controls, restyled with <code>appearance: none</code> — the thing you see IS the thing "
     "the browser focuses, checks and submits, so keyboard and screen-reader behaviour is the "
     "browser's, not ours. The tick wipes in, the radio dot scales, the switch knob slides.",
     head("Checkbox"),
     row(spec(".ns-checkbox", '<input type="checkbox" class="ns-checkbox" checked>'),
         spec("unchecked", '<input type="checkbox" class="ns-checkbox">'),
         spec("--sm", '<input type="checkbox" class="ns-checkbox ns-checkbox--sm" checked>'),
         spec("--lg", '<input type="checkbox" class="ns-checkbox ns-checkbox--lg" checked>'),
         spec("--success", '<input type="checkbox" class="ns-checkbox ns-checkbox--success" checked>'),
         spec(":disabled", '<input type="checkbox" class="ns-checkbox" checked disabled>')),
     head("Radio"),
     row(spec(".ns-radio", '<input type="radio" name="d1" class="ns-radio" checked>'),
         spec("unchecked", '<input type="radio" name="d2" class="ns-radio">'),
         spec("--sm", '<input type="radio" name="d3" class="ns-radio ns-radio--sm" checked>'),
         spec("--lg", '<input type="radio" name="d4" class="ns-radio ns-radio--lg" checked>')),
     head("Switch"),
     row(spec(".ns-switch", '<input type="checkbox" class="ns-switch" checked>'),
         spec("off", '<input type="checkbox" class="ns-switch">'),
         spec("--sm", '<input type="checkbox" class="ns-switch ns-switch--sm" checked>'),
         spec("--lg", '<input type="checkbox" class="ns-switch ns-switch--lg" checked>')),
     head("Choice rows"),
     row(spec(".ns-choice",
              '<div class="ns-stack-sm demo-w-md">'
              '<label class="ns-choice"><input type="checkbox" class="ns-checkbox" checked>'
              '<span class="ns-choice__label">Video lessons only'
              '<span class="ns-choice__desc">Hide article-based lessons from the list</span></span></label>'
              '<label class="ns-choice"><input type="checkbox" class="ns-checkbox">'
              '<span class="ns-choice__label">Include archived courses</span></label></div>', wide=True),
         spec("--card",
              '<div class="ns-stack-sm demo-w-md">'
              '<label class="ns-choice ns-choice--card"><input type="radio" name="plan" class="ns-radio" checked>'
              '<span class="ns-choice__label">Free<span class="ns-choice__desc">Every free course</span></span></label>'
              '<label class="ns-choice ns-choice--card"><input type="radio" name="plan" class="ns-radio">'
              '<span class="ns-choice__label">Member<span class="ns-choice__desc">Everything, forever</span></span></label></div>', wide=True)),
     head("Segmented control"),
     row(spec(".ns-segment",
              '<div class="ns-segment">'
              + "".join(f'<label class="ns-segment__option"><input type="radio" name="seg"{" checked" if i == 0 else ""}>'
                        f'<span>{t}</span></label>' for i, t in enumerate(("All", "Free", "Paid")))
              + '</div>')))

# ── Media + code ─────────────────────────────────────────────────────────────
page("Components", "media", "Media",
     "Every image and embed the templates place. Media ALWAYS declares an aspect ratio, so the page "
     "never jumps as it loads — the single biggest layout-stability win on a content site.",
     head("Ratios"),
     row(*[spec(f"--{k}", f'<div class="ns-media ns-media--{k} ns-media--frame demo-media demo-w-xs"><i class="ph ph-image"></i></div>', wide=True)
           for k in ("video", "photo", "square", "portrait")]),
     note("A 21:9 band is a letterbox slot on a phone, so <code>--wide</code>, <code>--portrait</code> and "
          "<code>--story</code> all relax their ratio below <code>sm</code>."),
     head("Overlay + labels"),
     row(spec("__overlay + __badge",
              '<div class="ns-media ns-media--frame demo-media demo-w-md"><i class="ph ph-image"></i>'
              '<span class="ns-media__overlay"></span>'
              '<span class="ns-media__badge">12:04</span>'
              '<span class="ns-media__badge ns-media__badge--start ns-media__badge--top">Lesson 3</span></div>', wide=True)),
     head("Fallback"),
     row(spec("__fallback",
              '<div class="ns-media ns-media--frame demo-w-md">'
              '<span class="ns-media__fallback"><i class="ph ph-image"></i></span></div>', wide=True)),
     head("Figure"),
     row(spec(".ns-figure",
              '<figure class="ns-figure demo-w-md"><div class="ns-media ns-media--frame demo-media"><i class="ph ph-image"></i></div>'
              '<figcaption class="ns-figure__caption">The schema builder, mid-refactor</figcaption></figure>', wide=True)),
     head("Gallery"),
     row(spec(".ns-media-grid",
              '<div class="ns-media-grid demo-w-full">'
              + '<div class="ns-media ns-media--square ns-media--frame demo-media"><i class="ph ph-image"></i></div>' * 4
              + '</div>', wide=True)))

page("Components", "video", "Video",
     "Two jobs that are easy to confuse: the POSTER you click to start playback, and the FRAME the "
     "player sits in once it is running.",
     head("Poster"),
     row(spec(".ns-video-poster",
              '<a class="ns-video-poster demo-w-md" href="#!">'
              '<span class="ns-video-poster__fallback"></span>'
              '<span class="ns-video-poster__play"><span><i class="ph-fill ph-play"></i></span></span>'
              '<span class="ns-video-poster__duration">12:04</span></a>', wide=True),
         spec("--sm + __title",
              '<a class="ns-video-poster ns-video-poster--sm demo-w-md" href="#!">'
              '<span class="ns-video-poster__fallback"></span>'
              '<span class="ns-video-poster__play"><span><i class="ph-fill ph-play"></i></span></span>'
              '<span class="ns-video-poster__title">Objects, fields and relationships</span></a>', wide=True)),
     head("Frame"),
     row(spec(".ns-video", '<div class="ns-video demo-w-md demo-media"><i class="ph ph-video"></i></div>', wide=True),
         spec("--square", '<div class="ns-video ns-video--square demo-w-xs demo-media"><i class="ph ph-video"></i></div>', wide=True)),
     head("Embed"),
     row(spec(".ns-embed", '<div class="ns-embed demo-w-md demo-media"><i class="ph ph-video-camera"></i></div>', wide=True)),
     note("<code>.ns-embed</code> wraps a YouTube or Vimeo iframe at a fixed ratio so the page holds its "
          "shape while the embed loads. Ratios: <code>--square</code>, <code>--story</code>."))

SNIP = ('  <span class="ns-tok-com">// bulk-safe: one query, one update</span>\n'
        '  <span class="ns-tok-kw">public static void</span> <span class="ns-tok-fn">setRating</span>'
        '(<span class="ns-tok-type">List</span>&lt;Account&gt; accs) {\n'
        '      <span class="ns-tok-kw">for</span> (Account a : accs) {\n'
        '          a.Rating = a.AnnualRevenue &gt; <span class="ns-tok-num">1000000</span> '
        '? <span class="ns-tok-str">Hot</span> : <span class="ns-tok-str">Warm</span>;\n'
        '      }\n'
        '      <span class="ns-tok-kw">update</span> accs;\n'
        '  }\n')

page("Components", "syntax", "Syntax highlighter",
     "A code block that looks like the tool the reader is learning: a title bar carrying the filename "
     "and language, a copy button that confirms itself, and optional line numbers. "
     "<code>code.js</code> tokenises and injects the <code>.ns-tok-*</code> spans — there is no "
     "highlighting library.",
     head("Default"),
     row(spec(".ns-code",
              '<figure class="ns-code demo-w-xl" data-lang="apex">'
              '<figcaption class="ns-code__bar">'
              '<span class="ns-code__file"><i class="ph ph-code"></i><span>AccountHandler.cls</span></span>'
              '<span class="ns-code__actions"><span class="ns-code__lang">apex</span>'
              '<button type="button" class="ns-code__btn" data-code="copy"><i class="ph ph-copy"></i>'
              '<span class="ns-code__btn-label"><span>Copy</span></span></button></span></figcaption>'
              '<div class="ns-code__body">'
              '<pre class="ns-code__gutter" aria-hidden="true">1\n2\n3\n4\n5\n6\n7</pre>'
              f'<pre class="ns-code__pre"><code>{SNIP}</code></pre>'
              '</div></figure>', wide=True)),
     note("Ghost's editor emits a bare <code>&lt;pre&gt;&lt;code class=\"language-x\"&gt;</code>. "
          "<code>assets/js/code.js</code> upgrades that into this structure and tokenises it; the "
          "copy button is wired by the system's own <code>assets/js/ds/code.js</code> through "
          "<code>[data-code=\"copy\"]</code>. The theme's old <code>.ns-syntax</code> is gone."),
     head("Terminal"),
     row(spec("--terminal",
              '<div class="ns-syntax ns-syntax--terminal demo-w-xl"><div class="ns-syntax__bar">'
              '<span class="ns-syntax__name"><i class="ph ph-terminal-window"></i>zsh</span>'
              '<button class="ns-syntax__copy"><i class="ph ph-stack"></i>'
              '<span class="ns-syntax__copy-label">Copy</span></button></div>'
              '<div class="ns-syntax__body"><pre><code>'
              '<span class="ns-syntax__line">sf org create scratch --alias dev</span>'
              '<span class="ns-syntax__line">sf project deploy start</span>'
              '</code></pre></div></div>', wide=True)),
     head("Plain"),
     row(spec("--plain",
              '<div class="ns-syntax ns-syntax--plain demo-w-xl">'
              f'<div class="ns-syntax__body"><pre><code>{SNIP}</code></pre></div></div>', wide=True)),
     note("<code>--full</code> breaks the block out to the full content width inside an article; "
          "<code>--wrap</code> soft-wraps instead of scrolling; <code>--dark</code> forces the navy "
          "editor surface. The token palette lifts automatically on dark grounds."))

page("Components", "prose", "Prose &amp; text elements",
     "Bare tags inside a reading context — <code>.gh-content</code> (Ghost post content) or "
     "<code>.ns-prose</code>. No classes on any tag below; this is what an author's writing renders as.",
     row(spec("headings, links, lists, quotes, code",
              '<div class="ns-prose demo-w-xl">'
              '<h2>The data model in one sentence</h2>'
              '<p>Objects are tables, fields are columns, records are rows — and <a href="#!">relationships</a> '
              'are what make it a CRM rather than a spreadsheet. Press <kbd>Cmd</kbd> + <kbd>K</kbd> to search, '
              'or run <code>SELECT Id FROM Account</code>. <mark>Highlighted</mark> and an '
              '<abbr title="Salesforce Object Query Language">SOQL</abbr> abbreviation.</p>'
              '<blockquote>A learning site does not need to look like the product it is teaching.'
              '<cite>Namaste Salesforce</cite></blockquote>'
              '<h3>Field types worth knowing</h3>'
              '<ul><li>Picklist — when the set is closed</li><li>Lookup — a soft relationship</li></ul>'
              '<ol><li>Create the object</li><li>Add the fields</li></ol>'
              '<pre><code>update accounts;</code></pre>'
              '<hr>'
              '<p><small>Last reviewed March 2026.</small></p>'
              '</div>', wide=True)),
     note("Two scoping rules keep these defaults from ever fighting template utilities: reading-context "
          "rules use <code>:where(.gh-content, .ns-prose)</code> (zero specificity), and global rules "
          "guard with <code>:not([class])</code>."))

# ── Chrome ───────────────────────────────────────────────────────────────────
page("Components", "nav-link", "Nav link",
     "A navigation row: header bar, mobile menu, sidebars. The faint brand tint on hover is "
     "legitimate here because a nav row is a surface you point at, not a status you read.",
     row(spec(".nav-link / .is-current",
              '<div class="ns-cluster-sm"><a class="nav-link is-current" href="#!"><i class="ph ph-house"></i>Home</a>'
              '<a class="nav-link" href="#!"><i class="ph ph-graduation-cap"></i>Courses</a>'
              '<a class="nav-link" href="#!"><i class="ph ph-flow-arrow"></i>Training</a></div>', wide=True)),
     row(spec("--block + __meta",
              '<div class="demo-w-sm"><a class="nav-link nav-link--block" href="#!"><i class="ph ph-books"></i>Docs'
              '<span class="nav-link__meta">22</span></a></div>', wide=True)))

page("Components", "icon-button", "Icon button",
     "The round, borderless action in the navbar and toolbars. Pairs with the tooltip for its label.",
     head("Tone"),
     row(spec("(default)", '<button class="icon-btn"><i class="ph ph-magnifying-glass"></i></button>'),
         spec("--brand", '<button class="icon-btn icon-btn--brand"><i class="ph ph-arrow-right"></i></button>'),
         spec("--pink", '<button class="icon-btn icon-btn--pink"><i class="ph-fill ph-heart"></i></button>'),
         spec("--danger", '<button class="icon-btn icon-btn--danger"><i class="ph ph-x"></i></button>'),
         spec("--quiet", '<button class="icon-btn icon-btn--quiet"><i class="ph ph-info"></i></button>')),
     head("Shape + state"),
     row(spec("--outline", '<button class="icon-btn icon-btn--outline"><i class="ph ph-gear-six"></i></button>'),
         spec("--square", '<button class="icon-btn icon-btn--square icon-btn--outline"><i class="ph ph-list"></i></button>'),
         spec(".is-active", '<button class="icon-btn is-active"><i class="ph ph-bell-ringing"></i></button>'),
         spec("--sm / --lg", '<button class="icon-btn icon-btn--sm"><i class="ph ph-star"></i></button>'
                             '<button class="icon-btn icon-btn--lg"><i class="ph ph-star"></i></button>')),
     head("With a tooltip"),
     row(spec(".ns-tooltip (hover)",
              '<span class="group demo-relative"><button class="icon-btn"><i class="ph ph-info"></i></button>'
              '<span class="ns-tooltip">Help</span></span>')))

page("Components", "menu", "Menu &amp; share",
     "The dropdown panel: the account menu, the share menu, any Alpine popover. A floating layer "
     "genuinely sits above the page, so this is one of the few places allowed to carry "
     "<code>--shadow-raised</code>.",
     row(spec(".ns-menu",
              '<div class="demo-relative demo-scroll-h demo-w-sm">'
              '<div class="ns-menu demo-static demo-w-sm">'
              '<div class="ns-menu__head"><div class="ns-testimonial__name">Swarnil Singhai</div>'
              '<div class="ns-testimonial__role">member since 2026</div></div>'
              '<div class="ns-menu__group"><a class="ns-menu__item" href="#!"><i class="ph ph-user"></i>Account</a>'
              '<a class="ns-menu__item ns-menu__item--brand" href="#!"><i class="ph ph-user-circle"></i>Become an author</a></div>'
              '<div class="ns-menu__sep"></div>'
              '<a class="ns-menu__item ns-menu__item--quiet" href="#!"><i class="ph ph-x"></i>Sign out</a>'
              '</div></div>', wide=True),
         spec(".ns-share",
              '<div class="ns-share"><button class="ns-btn ns-btn--outline ns-btn--sm">'
              '<i class="ph ph-share-network"></i>Share</button>'
              '<div class="ns-share__menu demo-static demo-mt">'
              '<a href="#!"><i class="ph ph-twitter-logo"></i>Twitter</a>'
              '<a href="#!"><i class="ph ph-linkedin-logo"></i>LinkedIn</a>'
              '<button type="button"><i class="ph ph-link-simple"></i>Copy link</button></div></div>', wide=True)))

page("Components", "toc", "Table of contents",
     "The design system's <code>.ns-toc</code>, filled by <code>toc.js</code> from the headings in "
     "the article. The active heading is marked by the LEFT RAIL going brand — a rail, not a "
     "highlight, because the TOC is a map of the page's structure — and it is carried by "
     "<code>aria-current=&quot;true&quot;</code> rather than a class, so the highlighted item and "
     "the announced item cannot drift apart. Two levels only.",
     row(spec(".ns-toc",
              '<nav class="ns-toc demo-w-sm"><span class="ns-toc__title">On this page</span>'
              '<a class="ns-toc__link" href="#!" aria-current="true">Getting started</a>'
              '<a class="ns-toc__link" href="#!">The data model</a>'
              '<a class="ns-toc__link ns-toc__link--sub" href="#!">Objects</a>'
              '<a class="ns-toc__link ns-toc__link--sub" href="#!">Relationships</a></nav>', wide=True),
         spec("--card",
              '<nav class="ns-toc ns-toc--card demo-w-sm"><span class="ns-toc__title">On this page</span>'
              '<a class="ns-toc__link" href="#!" aria-current="true">Getting started</a>'
              '<a class="ns-toc__link" href="#!">The data model</a></nav>', wide=True)),
     row(spec("--numbered",
              '<nav class="ns-toc ns-toc--numbered demo-w-sm">'
              '<a class="ns-toc__link" href="#!">Create the org</a>'
              '<a class="ns-toc__link" href="#!">Install the package</a>'
              '<a class="ns-toc__link" href="#!">Verify the deploy</a></nav>', wide=True),
         spec("--inline",
              '<nav class="ns-toc ns-toc--inline demo-w-xl">'
              '<a class="ns-toc__link" href="#!" aria-current="true">Getting started</a>'
              '<a class="ns-toc__link" href="#!">The data model</a>'
              '<a class="ns-toc__link" href="#!">Users</a></nav>', wide=True)))

page("Components", "sidebar", "Docs sidebar",
     "Three different &ldquo;active&rdquo; treatments, because they answer three different questions: which "
     "page am I ON, which section am I IN, which heading am I NEAR.",
     row(spec(".doc-nav-link.is-doc-active",
              '<nav class="demo-w-md"><span class="doc-nav-heading">Getting started</span>'
              '<a class="doc-nav-link nav-link nav-link--block nav-link--sm is-doc-active" href="#!">Create your account</a>'
              '<a class="doc-nav-link nav-link nav-link--block nav-link--sm" href="#!">Find your way around</a>'
              '<span class="doc-nav-heading">Courses</span>'
              '<a class="doc-nav-link nav-link nav-link--block nav-link--sm" href="#!">How a course is structured</a></nav>', wide=True)),
     note("The active row uses <code>!important</code> on purpose: the markup's <code>text-muted</code> / "
          "<code>hover:*</code> utilities sit in a later cascade layer and would otherwise wash it out."),
     note("The mobile sub-navbar that used to be documented here is gone with "
          "<code>subnav.css</code>: the lesson list is reached through "
          "<code>.ns-lesson-panel</code> on a phone and the system's rail above lg, so a third "
          "way in had no consumer left."))

page("Components", "site", "Site modules",
     "Styling that only exists on one part of the site — the <code>site-*.css</code> files. They are "
     "part of the component layer but always imported last, because they may lean on anything above "
     "them and nothing above may lean on them.",
     head("Course tags"),
     row(spec(".ns-level", '<span class="ns-level ns-level--beginner">Beginner</span>'
                           '<span class="ns-level ns-level--intermediate">Intermediate</span>'
                           '<span class="ns-level ns-level--advanced">Advanced</span>'),
         spec(".ns-price-tag", '<span class="ns-price-tag ns-price-tag--free">Free</span>'
                               '<span class="ns-price-tag ns-price-tag--paid">Paid</span>'),
         spec(".ns-badge-featured", '<span class="ns-badge-featured"><i class="ph-fill ph-star"></i>Featured</span>')),
     head("Curriculum"),
     row(spec(".ns-curriculum",
              '<div class="ns-curriculum ns-curriculum--flat demo-w-xl">'
              '<div class="ns-curriculum__bar"><span class="ns-curriculum__totals">3 lessons</span></div>'
              + "".join(f'<a class="ns-lesson" href="#!" data-access="{acc}">'
                        f'<span class="ns-lesson__index">{n:02d}</span>'
                        f'<span class="ns-lesson__body"><span class="ns-lesson__title">{t}</span>'
                        f'<span class="ns-lesson__sub">{b}</span></span>'
                        f'<span class="ns-ltype ns-ltype--icon ns-ltype--{kind}">'
                        f'<i class="ph ph-{ic}"></i><span>{kind.title()}</span></span>'
                        f'<span class="ns-lesson__time">{d}</span></a>'
                        for n, ic, kind, t, d, acc, b in (
                            (1, "video", "video", "What Salesforce actually is", "6m", "free",
                             '<span class="ns-laccess ns-laccess--free">Free</span>'),
                            (2, "video", "video", "Objects and fields", "12m", "free",
                             '<span class="ns-laccess ns-laccess--free">Preview</span>'),
                            (3, "article", "article", "Users and permissions", "18m", "members",
                             '<span class="ns-laccess ns-laccess--members">Members</span>')))
              + '</div>', wide=True)),
     head("Lesson"),
     row(spec(".ns-lesson-type", '<span class="ns-lesson-type ns-lesson-type--video"><i class="ph-fill ph-video"></i>Video</span>'
                                 '<span class="ns-lesson-type ns-lesson-type--article"><i class="ph ph-article"></i>Article</span>'),
         spec(".ns-lesson-chip", '<span class="ns-lesson-chip"><i class="ph ph-clock"></i>12 min</span>')),
     note("The rest — the navbar's scroll behaviours, the catalog grid and filters, the training "
          "roadmap and rail — only makes sense at full page width. See it running on the site."))

page("Components", "effects", "Effects &amp; ads",
     "Optional polish. If the JS never runs the page must still read correctly, which is why each "
     "effect's resting state is the visible one wherever possible — and why every one is fully "
     "disabled under <code>prefers-reduced-motion</code>.",
     row(spec(".js-spotlight (hover)",
              '<div class="ns-card ns-card--interactive js-spotlight demo-w-md">'
              '<div class="ns-card__title">Pointer spotlight</div>'
              '<div class="ns-card__meta">a faint brand tint follows the cursor</div></div>', wide=True),
         spec(".ns-underline (hover)", '<a class="ns-underline" href="#!">An underline that wipes in</a>', wide=True)),
     head("Marquee"),
     row(spec(".marquee",
              '<div class="marquee demo-w-xl"><div class="marquee-track ns-cluster">'
              + ("".join(f'<span class="ns-tagchip">{t}</span>'
                         for t in ("Apex", "LWC", "Flow", "Data Cloud", "Agentforce")) * 2)
              + '</div></div>', wide=True)),
     head("Ad slot"),
     row(spec(".ns-ad",
              '<div class="ns-ad demo-w-xl"><div class="ns-ad__ph">'
              '<i class="ns-ad__arrow ph ph-arrow-right"></i>'
              '<span class="ns-ad__label">Your ad here — 728×90</span></div></div>', wide=True)),
     note("Also here: <code>.js-reveal</code>, <code>.js-manifesto</code>, the <code>.js-tl-*</code> "
          "roadmap draw, <code>.ns-aurora</code> and the <code>.ns-ba-*</code> illustration loops."))


# ═════════════════════════════════════════════════════════════════════════════
# HOME — the sections a home page is assembled from
# ═════════════════════════════════════════════════════════════════════════════
def pcard(mod="", title="Why I reach for Flow before Apex", cover=True, badge=None,
          excerpt="Apex is not the senior choice. Choosing the least powerful tool that solves the "
                  "problem is."):
    media = ""
    if cover:
        media = ('<span class="ns-bcard__cover ns-bcard__cover--empty">'
                 '<i class="ph ph-image"></i></span>')
    return (f'<article class="ns-card ns-bcard {mod}">{media}'
            f'<div class="ns-card__body">'
            + (f'<span class="ns-badge ns-badge--solid">{badge}</span>' if badge else "")
            + f'<h3 class="ns-bcard__title"><a class="ns-card__link" href="#!">{title}</a></h3>'
            f'<p class="ns-bcard__excerpt">{excerpt}</p>'
            f'<div class="ns-postmeta ns-postmeta--dotted">'
            f'<span class="ns-postmeta__author">'
            f'<span class="ns-avatar ns-avatar--sm demo-avatar-fill"></span>Swarnil</span>'
            f'<span>6 min</span><span>Mar 2026</span></div>'
            f'</div></article>')


HEADER_DEMO = (
    '<nav class="ns-topnav demo-static" aria-label="Main">'
    '<div class="ns-topnav__inner">'
    '<a class="ns-topnav__brand" href="#!">'
    '<span class="ns-chip ns-chip--sm"><i class="ph ph-terminal-window"></i></span>'
    '<span class="ns-topnav__brand-name">Namaste Salesforce</span></a>'
    '<ul class="ns-topnav__links">'
    '<li><a class="ns-topnav__link" href="#!" aria-current="page"><i class="ph ph-house"></i>Home</a></li>'
    '<li><a class="ns-topnav__link" href="#!"><i class="ph ph-graduation-cap"></i>Courses</a></li>'
    '<li><a class="ns-topnav__link" href="#!"><i class="ph ph-flow-arrow"></i>Training</a></li>'
    '<li><a class="ns-topnav__link" href="#!"><i class="ph ph-books"></i>Docs</a></li>'
    '</ul>'
    '<div class="ns-topnav__actions">'
    '<button type="button" class="ns-navsearch"><i class="ph ph-magnifying-glass"></i>'
    '<span class="ns-navsearch__text">Search…</span><kbd class="ns-navsearch__kbd">&#8984;K</kbd></button>'
    '<a class="ns-navstar" href="#!"><span class="ns-navstar__label"><i class="ph ph-github"></i><span>Star</span></span></a>'
    '<button type="button" class="ns-themeswitch" role="switch" aria-checked="false" aria-label="Dark mode">'
    '<span class="ns-themeswitch__mark"></span></button>'
    '<div class="ns-topnav__auth">'
    '<a class="ns-btn ns-btn--quiet ns-btn--sm" href="#!">Sign in</a>'
    '<a class="ns-btn ns-btn--primary ns-btn--sm" href="#!">Start learning</a></div>'
    '<button type="button" class="ns-burger" aria-label="Menu">'
    '<span class="ns-burger__bar"></span><span class="ns-burger__bar"></span><span class="ns-burger__bar"></span>'
    '</button>'
    '</div></div></nav>')


page("Home", "home", "Home page",
     "The whole page, assembled from the sections below. A home page is nothing but a stack of "
     "bands: one hero, then collections, then proof, then the ask. Every band uses the page measure "
     "and the same vertical rhythm, which is what stops a long landing page feeling improvised.",
     head("The stack"),
     note("<b>1.</b> Header &rarr; <b>2.</b> Hero &rarr; <b>3.</b> Collection: courses &rarr; "
          "<b>4.</b> Feature grid &rarr; <b>5.</b> Collection: latest posts &rarr; <b>6.</b> Metrics "
          "&rarr; <b>7.</b> Testimonials &rarr; <b>8.</b> Closing CTA. Nothing here is new — each is a "
          "component documented on its own page."),
     head("1 · Header"),
     row(spec(".ns-topnav", HEADER_DEMO, wide=True)),
     head("2 · Hero"),
     row(spec(".ns-hero--split",
              '<div class="ns-hero ns-hero--split ns-hero--sm ns-hero--grid">'
              '<div class="ns-hero__inner">'
              '<div><p class="ns-kicker ns-kicker--light">Free forever</p>'
              '<h1 class="ns-hero__title">Learn Salesforce by building it</h1>'
              '<p class="ns-hero__sub">Project-led courses and one guided path from your first login '
              'to your first automation.</p>'
              '<div class="ns-hero__actions"><a class="ns-btn ns-btn--white" href="#!">Start the training</a>'
              '<a class="ns-btn ns-btn--glass" href="#!">Browse courses</a></div>'
              '<div class="ns-hero__meta">'
              '<div class="ns-stat ns-stat--light ns-stat--sm"><span class="ns-stat__value">24</span>'
              '<span class="ns-stat__label">courses</span></div>'
              '<div class="ns-stat ns-stat--light ns-stat--sm"><span class="ns-stat__value">312</span>'
              '<span class="ns-stat__label">lessons</span></div>'
              '<div class="ns-stat ns-stat--light ns-stat--sm"><span class="ns-stat__value">100%</span>'
              '<span class="ns-stat__label">free</span></div></div></div>'
              '<div class="ns-hero__media"><div class="ns-media ns-media--frame demo-media">'
              '<i class="ph ph-image"></i></div></div>'
              '</div></div>', wide=True)),
     head("3 · Collection — courses"),
     row(spec(".ns-collection--rail",
              '<div class="ns-collection ns-collection--sm ns-collection--rail ns-collection--sunken">'
              '<div class="ns-collection__inner">'
              '<div class="ns-collection__head"><div><span class="ns-kicker">Courses</span>'
              '<h2 class="ns-collection__title">Start with the fundamentals</h2>'
              '<p class="ns-collection__sub">Self-contained, one topic each.</p></div>'
              '<a class="ns-btn ns-btn--outline ns-btn--sm ns-collection__action" href="#!">All courses</a></div>'
              '<div class="ns-collection__items">'
              + pcard(badge="Free", title="Admin Foundations",
                      excerpt="Objects, fields, users and security — the groundwork.")
              + pcard(title="Apex Programming", excerpt="Bulk-safe patterns and tests that mean something.")
              + pcard(title="Lightning Web Components", excerpt="Modern web standards, on platform.")
              + '</div></div></div>', wide=True)),
     head("4 · Feature grid"),
     row(spec(".ns-band + .ns-grid",
              '<div class="ns-band ns-band--sm"><div class="ns-band__inner">'
              '<div class="ns-section-head ns-section-head--center"><div>'
              '<span class="ns-kicker ns-kicker--center">Why here</span>'
              '<h2 class="ns-section-head__title">Built for people who want to build</h2></div></div>'
              '<div class="ns-grid ns-grid--3">'
              + "".join('<div class="ns-feature"><span class="ns-chip"><i class="ph-fill ' + ic + '"></i></span>'
                        '<h3 class="ns-feature__title">' + t + '</h3>'
                        '<p class="ns-feature__body">' + b + '</p></div>'
                        for ic, t, b in (
                            ("ph-graduation-cap", "Project-led",
                             "Every lesson ends with something you built, not something you watched."),
                            ("ph-users-three", "Community reviewed",
                             "Drafts get a technical review before they go live."),
                            ("ph-lock-open", "Free forever",
                             "The whole beginner track is open. No card, no trial.")))
              + '</div></div></div>', wide=True)),
     head("5 · Collection — latest posts"),
     row(spec(".ns-collection--feature",
              '<div class="ns-collection ns-collection--sm ns-collection--feature">'
              '<div class="ns-collection__inner">'
              '<div class="ns-collection__head"><div><span class="ns-kicker">Blog</span>'
              '<h2 class="ns-collection__title">Field notes</h2></div>'
              '<a class="ns-btn ns-btn--outline ns-btn--sm ns-collection__action" href="#!">All posts</a></div>'
              '<div class="ns-collection__items">'
              + pcard("ns-bcard--overlay", badge="New")
              + pcard("ns-bcard--row", title="A mental model for governor limits", cover=True,
                      excerpt="Stop memorising the numbers.")
              + pcard("ns-bcard--row", title="Your first 90 days as an admin", cover=True,
                      excerpt="What to do when you inherit an org you did not build.")
              + '</div></div></div>', wide=True)),
     head("6 · Metrics"),
     row(spec(".ns-metrics",
              '<div class="ns-band ns-band--sm ns-band--dark ns-band--grid"><div class="ns-band__inner">'
              '<div class="ns-metrics">'
              + "".join('<div><div class="ns-metrics__value">' + v + '</div>'
                        '<div class="ns-metrics__label">' + l + '</div></div>'
                        for v, l in (("24", "courses"), ("312", "lessons"),
                                     ("9", "roadmaps"), ("1.2k", "learners")))
              + '</div></div></div>', wide=True)),
     head("7 · Testimonials"),
     row(spec(".ns-testimonial-grid",
              '<div class="ns-band ns-band--sm ns-band--sunken"><div class="ns-band__inner">'
              '<div class="ns-testimonial-grid">'
              + f'<figure class="ns-testimonial ns-testimonial--sm">{TESTI_BODY}</figure>' * 3
              + '</div></div></div>', wide=True)),
     head("8 · Closing CTA"),
     row(spec(".ns-cta-band--dark",
              '<div class="ns-band ns-band--sm"><div class="ns-band__inner">'
              '<div class="ns-cta-band ns-cta-band--dark">'
              '<span class="ns-kicker ns-kicker--light ns-kicker--center">Free forever</span>'
              '<h2 class="ns-cta-band__title">Start with the fundamentals</h2>'
              '<p class="ns-cta-band__sub">No card, no trial — the whole beginner track is open.</p>'
              '<div class="ns-cta-band__actions"><a class="ns-btn ns-btn--white" href="#!">Create an account</a>'
              '<a class="ns-btn ns-btn--glass" href="#!">Browse first</a></div></div>'
              '</div></div>', wide=True)))

page("Home", "home-header", "Header",
     "The bar at the top of every page. It is the DESIGN SYSTEM's "
     "<code>.ns-topnav</code> — markup, styling and behaviour all vendored from "
     "NS-Design-System, so the marketing site and the app wear the same bar. "
     "Menus, the mobile sheet and the theme switch are driven by "
     "<code>assets/js/ds/nav.js</code>; the theme writes no navbar JavaScript.",
     head("Default"),
     row(spec(".ns-topnav", HEADER_DEMO, wide=True)),
     note("Nav items come from Ghost (Settings &rarr; Navigation) through the reserved "
          "<code>{{navigation}}</code> helper. The active item carries "
          "<code>aria-current=\"page\"</code> rather than a class, so the highlighted item and the "
          "announced item cannot drift apart."),
     head("Compact"),
     row(spec("--compact",
              HEADER_DEMO.replace('class="ns-topnav demo-static"', 'class="ns-topnav ns-topnav--compact demo-static"'),
              wide=True)),
     head("Sunken"),
     row(spec("--sunken",
              HEADER_DEMO.replace('class="ns-topnav demo-static"', 'class="ns-topnav ns-topnav--sunken demo-static"'),
              wide=True)),
     head("Dark"),
     row(spec("--dark",
              HEADER_DEMO.replace('class="ns-topnav demo-static"', 'class="ns-topnav ns-topnav--dark demo-static"'),
              wide=True)),
     note("<code>@custom.navbar_behavior</code> (Ghost Admin &rarr; Design) selects between these: "
          "Sticky is the base, Fixed-on-scroll maps to <code>--compact</code>, Island to "
          "<code>--floating</code> and Static to <code>--sunken</code>. The old theme-owned "
          "<code>site-navbar.css</code> and <code>navbar.js</code> are deleted."),
     head("Reading chrome"),
     row(spec(".ns-coursenav",
              '<nav class="ns-coursenav demo-static" aria-label="Course">'
              '<a class="ns-coursenav__back" href="#!"><i class="ph ph-arrow-left"></i><span>Salesforce Admin</span></a>'
              '<span class="ns-topnav__divider"></span>'
              '<span class="ns-coursenav__id"><span class="ns-coursenav__title">Objects, fields &amp; relationships</span></span>'
              '<div class="ns-coursenav__progress">'
              '<div class="ns-coursenav__bar demo-p29" role="progressbar" aria-valuenow="29" aria-valuemin="0" aria-valuemax="100"><span></span></div>'
              '<span class="ns-coursenav__pct">7 / 24</span></div>'
              '<div class="ns-coursenav__actions">'
              '<button type="button" class="ns-themeswitch" role="switch" aria-checked="false" aria-label="Dark mode">'
              '<span class="ns-themeswitch__mark"></span></button></div>'
              '</nav>', wide=True)),
     note("A lesson gets this instead of the marketing bar: leave, where-you-are, how-far. No "
          "primary action &mdash; finishing a lesson is the docked prev/next at the foot of it, and "
          "a second solid button up here would compete for the one click a screen is allowed."))

page("Home", "home-post-card", "Post card",
     "One entry in a collection: a blog post, a course, a doc, a resource. The generic card is the "
     "box; this is what goes IN it when the thing being shown is content — so every collection on "
     "the site presents the same shape.",
     head("Default"),
     row(spec(".ns-card .ns-bcard", f'<div class="demo-w-md">{pcard()}</div>', wide=True),
         spec("--sm", f'<div class="demo-w-sm">{pcard("ns-bcard--sm")}</div>', wide=True)),
     head("Row"),
     row(spec("--row", f'<div class="demo-w-xl">{pcard("ns-bcard--row")}</div>', wide=True)),
     head("Wide — the featured item"),
     row(spec("--wide", f'<div class="demo-w-full">{pcard("ns-bcard--wide")}</div>', wide=True)),
     head("Overlay"),
     row(spec("--overlay", f'<div class="demo-w-md">{pcard("ns-bcard--overlay", badge="Featured")}</div>', wide=True)),
     head("Compact + minimal"),
     row(spec("--compact", f'<div class="demo-w-sm">{pcard("ns-bcard--minimal", cover=False)}</div>', wide=True),
         spec("--minimal", f'<div class="demo-w-md">{pcard("ns-bcard--minimal", cover=False)}</div>', wide=True)),
     note("The whole card is clickable through a stretched link on the title, so the title stays the "
          "real anchor — screen readers announce it and middle-click still works."))

page("Home", "home-collection", "Collection",
     "A band that shows part of a collection. It is the unit a home page is built from, and it is "
     "always the same four things in the same order — kicker, title, link, items — so a visitor "
     "learns the shape once.",
     head("Grid — the default"),
     row(spec(".ns-collection",
              '<div class="ns-collection ns-collection--sm"><div class="ns-collection__inner">'
              '<div class="ns-collection__head"><div><span class="ns-kicker">Courses</span>'
              '<h2 class="ns-collection__title">Start with the fundamentals</h2></div>'
              '<a class="ns-btn ns-btn--outline ns-btn--sm ns-collection__action" href="#!">All courses</a></div>'
              '<div class="ns-collection__items">' + pcard() * 3 + '</div>'
              '<div class="ns-collection__footer">'
              '<a class="ns-btn ns-btn--outline ns-btn--sm" href="#!">Load more</a></div>'
              '</div></div>', wide=True)),
     head("Rows — a divided list"),
     row(spec("--rows",
              '<div class="ns-collection ns-collection--sm ns-collection--rows"><div class="ns-collection__inner">'
              '<div class="ns-collection__head"><div><span class="ns-kicker">Docs</span>'
              '<h2 class="ns-collection__title">Recently updated</h2></div></div>'
              '<div class="ns-collection__items">'
              + pcard("ns-bcard--minimal", cover=False, title="Create your account")
              + pcard("ns-bcard--minimal", cover=False, title="How a course is structured")
              + pcard("ns-bcard--minimal", cover=False, title="Cancel or change your plan")
              + '</div></div></div>', wide=True)),
     head("Feature — one big, the rest beside"),
     row(spec("--feature",
              '<div class="ns-collection ns-collection--sm ns-collection--feature ns-collection--sunken">'
              '<div class="ns-collection__inner">'
              '<div class="ns-collection__head"><div><span class="ns-kicker">Blog</span>'
              '<h2 class="ns-collection__title">Field notes</h2></div></div>'
              '<div class="ns-collection__items">'
              + pcard("ns-bcard--overlay")
              + pcard("ns-bcard--row", title="A mental model for governor limits")
              + pcard("ns-bcard--row", title="Your first 90 days as an admin")
              + '</div></div></div>', wide=True)),
     head("Split — standing copy, items beside"),
     row(spec("--split",
              '<div class="ns-collection ns-collection--sm ns-collection--split"><div class="ns-collection__inner">'
              '<div class="ns-collection__head"><div><span class="ns-kicker">Training</span>'
              '<h2 class="ns-collection__title">One guided path</h2>'
              '<p class="ns-collection__sub">Nine sections, in order, from zero.</p>'
              '<a class="ns-btn ns-btn--primary ns-btn--sm" href="#!">Start</a></div></div>'
              '<div class="ns-collection__items">'
              + pcard("ns-bcard--row", title="Start here") + pcard("ns-bcard--row", title="Build your first app")
              + '</div></div></div>', wide=True)),
     note("<code>--rail</code> makes the items swipeable on a phone and a grid from <code>lg</code> — "
          "the right answer when a collection has more items than a phone can show."))



# ═════════════════════════════════════════════════════════════════════════════
# PAGES — the standing pages: about, contact, legal, 404
# ═════════════════════════════════════════════════════════════════════════════
def _toc_rail():
    items = ("Who we are", "What we collect", "How we use it", "Your rights", "Contact us")
    links = "".join(
        '<a class="ns-toc__link"%s href="#!">%s</a>' % (' aria-current="true"' if i == 0 else '', t)
        for i, t in enumerate(items))
    return ('<div class="ns-widget ns-widget--toc ns-widget--sunken">'
            '<div class="ns-widget__head"><span class="ns-widget__title">On this page</span></div>'
            '<div class="ns-widget__body">' + links + '</div></div>')


TOC_RAIL = _toc_rail()

page("Pages", "page-anatomy", "Page anatomy",
     "The standing pages — about, contact, terms, privacy, 404 — are neither collections nor posts, "
     "so they share their own small shell: head, body, optional sticky rail, closing action. Get this "
     "right once and every informational page on the site is the same job.",
     head("The shell"),
     note("<code>.ns-page</code> &rarr; <code>__inner</code> &rarr; <code>__head</code> (kicker, title, "
          "lede, meta) &rarr; <code>__main</code> (<code>__body</code> + optional <code>__aside</code>) "
          "&rarr; <code>__foot</code>. Layouts: <code>--narrow</code> for a single reading column, "
          "<code>--rail</code> for prose plus a contents rail, <code>--rail-start</code> when the "
          "contents should lead."),
     head("Narrow — the default for most pages"),
     row(spec(".ns-page--narrow",
              '<div class="ns-page ns-page--narrow demo-fill"><div class="ns-page__inner">'
              '<div class="ns-page__head"><span class="ns-kicker">About</span>'
              '<h1 class="ns-page__title">Why this exists</h1>'
              '<p class="ns-page__lede">Salesforce learning material is either a sales pitch or a wall '
              'of reference docs. This site is the thing in between.</p></div>'
              '<div class="ns-page__main"><div class="ns-page__body ns-prose">'
              '<p>Objects are tables, fields are columns, records are rows — and relationships are what '
              'make it a CRM rather than a spreadsheet.</p></div></div>'
              '</div></div>', wide=True)),
     head("With a contents rail"),
     row(spec(".ns-page--rail",
              '<div class="ns-page ns-page--rail demo-fill"><div class="ns-page__inner">'
              '<div class="ns-page__head"><span class="ns-kicker">Legal</span>'
              '<h1 class="ns-page__title">Privacy policy</h1>'
              '<div class="ns-page__meta"><span>Last updated 12 March 2026</span>'
              '<span>Effective immediately</span></div></div>'
              '<div class="ns-page__main">'
              '<div class="ns-page__body ns-prose"><p>We collect the minimum needed to run the site, and '
              'we do not sell it. The detail is below.</p></div>'
              '<aside class="ns-page__aside">' + TOC_RAIL + '</aside>'
              '</div></div></div>', wide=True)),
     note("The rail is sticky from <code>lg</code> and scrolls independently; below that it stacks above "
          "the prose, which is the right order — a reader on a phone wants the contents first."))

page("Pages", "page-legal", "Legal pages",
     "Terms, privacy, cookies, refunds. Numbered anchored sections with a generated index, so "
     "re-ordering a section cannot leave a stale &ldquo;4.&rdquo; behind in the copy, and every section has a "
     "stable link to quote in an email.",
     head("Summary first"),
     note("A good policy opens with the short version. <code>.ns-legal__summary</code> is that box — a "
          "brand rail on the sunken surface, not a wall of defensive prose."),
     row(spec(".ns-legal__summary",
              '<div class="ns-legal__summary demo-w-2xl">'
              '<span class="ns-kicker">In short</span>'
              '<p class="demo-mt">We collect your email so you can sign in, and anonymous page counts so '
              'we know which lessons help. We do not sell anything to anyone, ever.</p></div>', wide=True)),
     head("Numbered sections"),
     row(spec(".ns-legal",
              '<div class="ns-legal demo-w-2xl">'
              + "".join('<section><h2 class="ns-legal__title">%s</h2>'
                        '<div class="ns-legal__body ns-prose"><p>%s</p></div></section>' % (t, b)
                        for t, b in (
                            ("Who we are",
                             "Namaste Salesforce is an independent learning site run from Bengaluru, "
                             "India. It is not affiliated with Salesforce, Inc."),
                            ("What we collect",
                             "An email address when you create an account, and anonymous page counts. "
                             "Nothing else — there is no advertising profile here."),
                            ("How we use it",
                             "To send your sign-in link, to send the newsletter if you asked for it, and "
                             "to work out which lessons need rewriting.")))
              + '</div>', wide=True)),
     note("Headings carry <code>scroll-margin-top</code>, so a link from the contents rail lands below "
          "the sticky header rather than underneath it."))

page("Pages", "page-contact", "Contact page",
     "Two columns: how to reach a human on one side, a form on the other. The methods come first in "
     "the source, because most people want the email address rather than the form.",
     head("Methods"),
     row(spec(".ns-contact-method",
              '<div class="ns-contact__methods demo-w-md">'
              + "".join('<a class="ns-contact-method" href="#!">'
                        '<span class="ns-chip ns-chip--sm"><i class="ph-fill %s"></i></span>'
                        '<span class="ns-contact-method__body">'
                        '<span class="ns-contact-method__title">%s</span>'
                        '<span class="ns-contact-method__value">%s</span>'
                        '<span class="ns-contact-method__note">%s</span></span></a>' % (ic, t, v, n)
                        for ic, t, v, n in (
                            ("ph-envelope-simple", "Email", "hello@namastesalesforce.com",
                             "Usually answered within two days"),
                            ("ph-chat-circle-text", "Ask under a lesson", "Comments are open",
                             "The author reads them — fastest route for anything technical"),
                            ("ph-git-branch", "Open an issue", "github.com/imswarnil",
                             "For typos, broken links and code that does not run")))
              + '</div>', wide=True)),
     head("The form"),
     row(spec(".ns-contact__form + .ns-form",
              '<div class="ns-contact__form demo-w-lg"><form class="ns-form">'
              '<div class="ns-form__row ns-form__row--2">'
              '<label class="ns-field"><span class="ns-field__label">Name</span>'
              '<input class="ns-input" placeholder="Priya R."></label>'
              '<label class="ns-field"><span class="ns-field__label">Email</span>'
              '<input class="ns-input" type="email" placeholder="you@email.com"></label></div>'
              '<label class="ns-field"><span class="ns-field__label">Subject</span>'
              '<select class="ns-input"><option>A question about a lesson</option>'
              '<option>Something is broken</option><option>Writing for the site</option>'
              '<option>Sponsorship</option></select></label>'
              '<label class="ns-field"><span class="ns-field__label">Message</span>'
              '<textarea class="ns-input" placeholder="What are you stuck on?"></textarea></label>'
              '<label class="ns-choice"><input type="checkbox" class="ns-checkbox">'
              '<span class="ns-choice__label">Send me the fortnightly newsletter too</span></label>'
              '<div class="ns-form__actions">'
              '<span class="ns-form__note">We only use this to reply.</span>'
              '<button type="submit" class="ns-btn ns-btn--primary">Send message</button></div>'
              '</form></div>', wide=True)),
     head("Together"),
     row(spec(".ns-contact",
              '<div class="ns-contact demo-w-full">'
              '<div class="ns-contact__methods">'
              '<a class="ns-contact-method" href="#!">'
              '<span class="ns-chip ns-chip--sm"><i class="ph-fill ph-envelope-simple"></i></span>'
              '<span class="ns-contact-method__body"><span class="ns-contact-method__title">Email</span>'
              '<span class="ns-contact-method__value">hello@namastesalesforce.com</span></span></a>'
              '<a class="ns-contact-method" href="#!">'
              '<span class="ns-chip ns-chip--sm"><i class="ph-fill ph-git-branch"></i></span>'
              '<span class="ns-contact-method__body"><span class="ns-contact-method__title">Open an issue</span>'
              '<span class="ns-contact-method__value">github.com/imswarnil</span></span></a></div>'
              '<div class="ns-contact__form"><form class="ns-form">'
              '<label class="ns-field"><span class="ns-field__label">Email</span>'
              '<input class="ns-input" type="email" placeholder="you@email.com"></label>'
              '<label class="ns-field"><span class="ns-field__label">Message</span>'
              '<textarea class="ns-input"></textarea></label>'
              '<div class="ns-form__actions"><span class="ns-form__note">We only use this to reply.</span>'
              '<button class="ns-btn ns-btn--primary">Send</button></div></form></div>'
              '</div>', wide=True)),
     note("Add <code>--form-first</code> when the form is the point of the page — a sponsorship enquiry, "
          "say — and the methods become the supporting column."))

page("Pages", "page-about", "About page",
     "Not a legal page and not a collection: a story told in bands. It reuses the marketing sections "
     "wholesale, which is the test of whether those components were general enough.",
     head("Founder"),
     row(spec("split + list + tags",
              '<div class="ns-split demo-w-full">'
              '<div class="ns-split__media"><div class="ns-media ns-media--photo ns-media--frame demo-media">'
              '<i class="ph ph-user"></i></div></div>'
              '<div class="ns-split__body"><span class="ns-kicker">The team</span>'
              '<h2 class="ns-split__title">Hi, I am Swarnil</h2>'
              '<p class="ns-split__lede">I have spent years building on the platform — Apex and LWC '
              'through to data architecture and AI.</p>'
              '<ul class="ns-list ns-list--check ns-list--sm">'
              '<li class="ns-list__item">Writes and reviews every course</li>'
              '<li class="ns-list__item">Ships open-source tooling for the community</li></ul>'
              '<div class="ns-cluster"><a class="ns-tagchip" href="#!">Apex</a>'
              '<a class="ns-tagchip" href="#!">LWC</a><a class="ns-tagchip" href="#!">Flow</a></div>'
              '</div></div>', wide=True)),
     head("Milestones"),
     row(spec(".ns-timeline--icon",
              '<div class="ns-timeline ns-timeline--icon demo-w-md">'
              + "".join('<div class="ns-timeline__item %s">'
                        '<span class="ns-timeline__dot"><i class="ph-fill %s"></i></span>'
                        '<div class="ns-timeline__body"><div class="ns-timeline__title">%s</div>'
                        '<div class="ns-timeline__meta">%s</div></div></div>' % (st, ic, t, d)
                        for t, d, ic, st in (
                            ("Site launched", "Jan 2026", "ph-rocket-launch", "is-on"),
                            ("First course published", "Mar 2026", "ph-graduation-cap", "is-on"),
                            ("Certificates", "Planned", "ph-seal-check", "is-next")))
              + '</div>', wide=True)),
     note("Everything else an about page needs — metrics, testimonials, the closing CTA — is on the "
          "<a href=\"sections.html\">Content sections</a> page. Nothing new was needed here, which is "
          "the point."))

page("Pages", "page-404", "404 &amp; dead ends",
     "The page that says the thing you asked for is not here. A big mono code, one sentence, and the "
     "two or three places a lost visitor actually wants — not a dead end.",
     row(spec(".ns-404",
              '<div class="ns-404 demo-w-full">'
              '<div class="ns-404__code">404</div>'
              '<h1 class="ns-404__title">That page has moved on</h1>'
              '<p class="ns-404__body">The link may be old, or the lesson may have been folded into '
              'another course. Here is where most people were heading:</p>'
              '<div class="ns-404__actions">'
              '<a class="ns-btn ns-btn--primary" href="#!">Browse courses</a>'
              '<a class="ns-btn ns-btn--outline" href="#!">Start the training</a>'
              '<a class="ns-btn ns-btn--outline" href="#!">Search the docs</a></div></div>', wide=True)),
     note("The same shape covers a maintenance page or a members-only wall — swap the code for a glyph "
          "and the actions for a sign-in button."))



# ═════════════════════════════════════════════════════════════════════════════
# TRAINING — /training/, /training/{section}/, /training/{section}/{lesson}/
# ═════════════════════════════════════════════════════════════════════════════
_SECTIONS = (
    ("Start Here", "Get oriented: what the platform is, how this training works, and a free org "
                   "of your own.", 3, "45m", "done"),
    ("Build Your First App", "A custom object, the fields that matter, a layout people can use, "
                             "and one report that proves it.", 4, "1h 20m", "current"),
    ("Automate the Work", "Validation rules, your first Flow, and how to pick the right tool for "
                          "a requirement.", 3, "55m", ""),
    ("Ship and Maintain", "Deployments, sandboxes, and the habits that keep an org healthy.",
     3, "1h", "locked"),
)

_LESSONS = (
    ("What is Salesforce?", "6m", "done"),
    ("Set up a free Developer org", "12m", "done"),
    ("How to use this training", "5m", "current"),
    ("Objects, fields and relationships", "18m", ""),
)


def _sidenav(open_index=1):
    out = ['<nav class="ns-sidenav ns-sidenav--boxed demo-w-sm">',
           '<a class="ns-sidenav__back" href="#!"><i class="ph ph-arrow-left"></i>Back to training</a>',
           '<label class="ns-input-icon demo-mb"><i class="ph ph-magnifying-glass"></i>'
           '<input class="ns-input ns-input--sm" placeholder="Search this training…"></label>']
    for i, (title, _, count, _dur, state) in enumerate(_SECTIONS):
        is_open = " open" if i == open_index else ""
        out.append('<details class="ns-sidenav__group" name="sg-training"%s>' % is_open)
        out.append('<summary class="ns-sidenav__summary">'
                   '<span class="ns-sidenav__icon"><i class="ph-fill ph-stack"></i></span>'
                   '<span class="ns-sidenav__stitle">%s</span>'
                   '<i class="ns-sidenav__caret ph ph-caret-right"></i></summary>' % title)
        out.append('<div class="ns-sidenav__list">')
        out.append('<a class="ns-sidenav__link" href="#!">'
                   '<span class="ns-sidenav__num"><i class="ph ph-squares-four"></i></span>'
                   '<span class="ns-sidenav__text">Overview</span></a>')
        for n, (lt, ld, ls) in enumerate(_LESSONS[:count]):
            cls = " is-current" if ls == "current" else (" is-done" if ls == "done" else "")
            icon = ("ph-play-circle" if n == 0 else
                    "ph-barbell" if n == 2 else "ph-article")
            out.append('<a class="ns-sidenav__link%s" href="#!">'
                       '<span class="ns-sidenav__num"><span>%d</span></span>'
                       '<i class="ns-sidenav__type ph-fill %s"></i>'
                       '<span class="ns-sidenav__text">%s</span>'
                       '<span class="ns-sidenav__meta">%s</span></a>' % (cls, n + 1, icon, lt, ld))
        out.append('</div></details>')
    out.append('<div class="ns-sidenav__foot ns-sidenav__foot--sticky">'
               '<div class="ns-progress ns-progress--xs">'
               '<span class="ns-progress__bar" data-demo-width="35"></span></div>'
               '<div class="ns-sidenav__readout"><span>4 / 13 done</span>'
               '<span>13 lessons</span></div></div>')
    out.append('</nav>')
    return "".join(out)


SUBBAR = ('<div class="ns-subbar ns-subbar--static demo-w-full">'
          '<div class="ns-subbar__inner">'
          '<nav class="ns-crumbs ns-crumbs--sm">'
          '<a class="ns-crumbs__link" href="#!"><i class="ph ph-house"></i></a>'
          '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
          '<a class="ns-crumbs__link" href="#!"><i class="ph ph-graduation-cap"></i>Training</a>'
          '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
          '<a class="ns-crumbs__link" href="#!">Build Your First App</a>'
          '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
          '<span class="ns-crumbs__current"><span>Create a custom object</span></span></nav>'
          '<div class="ns-subbar__progress">'
          '<div class="ns-progress ns-progress--xs"><span class="ns-progress__bar" data-demo-width="35"></span></div>'
          '<span class="ns-subbar__readout">4 / 13 done</span></div>'
          '</div></div>')


def _track_card(i, title, excerpt, count, dur, state):
    cls = {"done": " is-done", "current": " is-current", "locked": " is-locked"}.get(state, "")
    lessons = "".join(
        '<a class="ns-track-card__lesson" href="#!">'
        '<i class="ph-fill %s"></i><span>%s</span>'
        '<span class="ns-track-card__lesson-meta">%s</span></a>'
        % ("ph-play-circle" if n % 2 == 0 else "ph-article", lt, ld)
        for n, (lt, ld, _s) in enumerate(_LESSONS[:min(count, 3)]))
    more = ('<div class="ns-track-card__more">+ %d more</div>' % (count - 3)) if count > 3 else ""
    progress = ""
    if state == "done":
        progress = ('<div class="ns-progress ns-progress--sm ns-progress--success ns-track-card__progress">'
                    '<span class="ns-progress__bar" data-demo-width="100"></span></div>')
    elif state == "current":
        progress = ('<div class="ns-progress ns-progress--sm ns-track-card__progress">'
                    '<span class="ns-progress__bar" data-demo-width="45"></span></div>')
    badge = ""
    if state == "done":
        badge = '<span class="ns-badge ns-badge--dot ns-badge--success">Complete</span>'
    elif state == "current":
        badge = '<span class="ns-badge ns-badge--dot">In progress</span>'
    elif state == "locked":
        badge = '<span class="ns-badge ns-badge--neutral"><i class="ph ph-lock"></i>Soon</span>'
    return ('<article class="ns-track-card%s">'
            '<div class="ns-track-card__index"></div>'
            '<div class="ns-track-card__box">'
            '<div class="ns-track-card__head">'
            '<h3 class="ns-track-card__title"><a href="#!">%s</a></h3>%s</div>'
            '<p class="ns-track-card__excerpt">%s</p>'
            '<div class="ns-track-card__meta"><span>%d lessons</span><span>%s</span></div>'
            '<div class="ns-track-card__lessons">%s</div>%s%s'
            '</div></article>' % (cls, title, badge, excerpt, count, dur, lessons, more, progress))


page("Training", "training-overview", "Training home",
     "The training is ONE ordered path, so the landing page draws it as a path: sections on a single "
     "connected rail, each showing what it covers, how long it takes and where you got to. A grid "
     "would say &ldquo;pick one&rdquo;; a rail says &ldquo;this comes after that&rdquo;, which is the truth.",
     head("Hero"),
     row(spec(".ns-hero--split",
              '<div class="ns-hero ns-hero--split ns-hero--sm ns-hero--grid">'
              '<div class="ns-hero__inner"><div>'
              '<p class="ns-kicker ns-kicker--light">Guided training</p>'
              '<h1 class="ns-hero__title">From your first login to your first automation</h1>'
              '<p class="ns-hero__sub">Four sections, thirteen lessons, in order. Finish one and the '
              'next opens — no prior experience assumed.</p>'
              '<div class="ns-hero__actions">'
              '<a class="ns-btn ns-btn--white" href="#!">Resume section 2</a>'
              '<a class="ns-btn ns-btn--glass" href="#!">Start from the beginning</a></div>'
              '<div class="ns-hero__meta">'
              + "".join('<div class="ns-stat ns-stat--light ns-stat--sm">'
                        '<span class="ns-stat__value">%s</span>'
                        '<span class="ns-stat__label">%s</span></div>' % (v, l)
                        for v, l in (("4", "sections"), ("13", "lessons"), ("4h", "total"), ("100%", "free")))
              + '</div></div>'
              '<div class="ns-hero__media"><article class="ns-card ns-card--interactive">'
              '<div class="ns-card__header"><div><span class="ns-card__meta">Start here</span>'
              '<h2 class="ns-card__title demo-mt">Start Here</h2></div>'
              '<span class="ns-chip ns-chip--sm"><i class="ph-fill ph-stack"></i></span></div>'
              '<p class="ns-clamp-2 demo-type-small demo-mt">Get oriented: what the platform is, how '
              'this training works, and a free org of your own.</p>'
              '<ul class="ns-list ns-list--num ns-list--sm ns-list--divided demo-mt">'
              + "".join('<li class="ns-list__item"><span class="ns-truncate">%s</span>'
                        '<span class="ns-list__meta">%s</span></li>' % (t, d)
                        for t, d, _s in _LESSONS[:3])
              + '</ul>'
              '<div class="ns-card__footer"><span class="ns-card__meta">3 lessons</span>'
              '<span class="ns-btn ns-btn--outline ns-btn--xs">Open section</span></div>'
              '</article></div>'
              '</div></div>', wide=True)),
     note("The media slot shows the FIRST SECTION — what you actually start with, and its lessons. It "
          "replaced a decorative trail illustration that rendered as a faint dotted line and left this "
          "half of the hero empty; showing the real first step is both more useful and more honest."),
     head("Your progress"),
     row(spec(".ns-progress + .ns-stats",
              '<div class="ns-card demo-w-full">'
              '<div class="ns-split"><div>'
              '<span class="ns-kicker">Where you are</span>'
              '<h2 class="ns-card__title demo-mt">Building Your First App</h2>'
              '<p class="ns-card__body demo-type-small">Next up: layouts, list views and a report.</p>'
              '</div><div>'
              '<div class="ns-progress"><span class="ns-progress__bar" data-demo-width="35"></span></div>'
              '<div class="ns-progress__label demo-mt">4 / 13 lessons · 35%</div>'
              '<a class="ns-btn ns-btn--primary ns-btn--sm demo-mt" href="#!">Continue '
              '<i class="ns-btn__icon ns-btn__icon--nudge ph ph-arrow-right"></i></a>'
              '</div></div></div>', wide=True)),
     head("The path"),
     row(spec(".ns-track-list + .ns-track-card",
              '<div class="ns-track-list demo-w-full">'
              + "".join(_track_card(i, *s) for i, s in enumerate(_SECTIONS))
              + '</div>', wide=True)),
     note("States on the card: <code>.is-done</code> turns the disc into a tick, "
          "<code>.is-current</code> rings it in brand and marks the box, <code>.is-locked</code> sinks "
          "it. <code>--compact</code> drops the lesson preview when the list gets long."))

page("Training", "training-nav", "Training navigation",
     "The rail that runs down every training and lesson page — and the answer to the rule you set: "
     "<b>the section you are in stays open, every other one is closed.</b>",
     head("How the behaviour works"),
     note("Each section is a <code>&lt;details&gt;</code> sharing one <code>name</code> attribute. That "
          "is a native HTML exclusive accordion: the browser itself keeps exactly one open and closes "
          "the previous when another is opened. No JavaScript, no flash on load, and it still behaves "
          "if the script never runs. A browser without exclusive-details support just allows more than "
          "one open — which degrades correctly rather than breaking."),
     note("Open section 3 below and section 2 closes on its own."),
     head("The rail"),
     row(spec(".ns-sidenav--boxed", _sidenav(), wide=True)),
     head("What is deliberately NOT in it"),
     note("<b>No lesson count on the section row.</b> The expanded list already shows it, and the "
          "number was the noisiest thing in the rail. <b>No training name or progress</b> — those "
          "belong to the page, not to the navigation, and repeating them above every rail was the "
          "single biggest source of clutter. They live in the sub bar instead."),
     note("<b>No horizontal scroll, ever.</b> Every text cell is <code>min-width: 0</code> with "
          "truncation and the rail clips its x axis — a sidebar you have to scroll sideways is a "
          "sidebar you cannot read."),
     head("Lesson type icons"),
     note("Each lesson row carries what KIND it is — video, exercise, quiz or article. The number says "
          "where you are in the section; the icon says what you are about to open, which is the thing "
          "you actually scan for."),
     row(spec("__type",
              '<nav class="ns-sidenav ns-sidenav--boxed demo-w-sm"><div class="ns-sidenav__list">'
              + "".join('<a class="ns-sidenav__link" href="#!">'
                        '<span class="ns-sidenav__num"><span>%d</span></span>'
                        '<i class="ns-sidenav__type ph-fill %s"></i>'
                        '<span class="ns-sidenav__text">%s</span>'
                        '<span class="ns-sidenav__meta">%s</span></a>' % (n + 1, ic, t, d)
                        for n, (ic, t, d) in enumerate((
                            ("ph-play-circle", "Watch: the data model", "12m"),
                            ("ph-article", "Read: field types", "6m"),
                            ("ph-barbell", "Build: your first object", "20m"),
                            ("ph-exam", "Check what you know", "4m"))))
              + '</div></nav>', wide=True)),
     head("It has to FIT"),
     note("Every level of the rail — group, list, row, text — is <code>min-width: 0</code>, so the "
          "title is what truncates and the duration is never clipped off the edge. The indent under a "
          "section is deliberately small, because every millimetre there comes off the lesson title, "
          "which is the only thing in the row worth reading."),
     head("Section icons"),
     note("The section's own image is its icon: the tag image first (set once, shared everywhere the "
          "section appears), then the post's feature image, then ONE shared fallback glyph. The same "
          "glyph for every section, so a missing image reads as &ldquo;section&rdquo; rather than as a different "
          "kind of thing. The open section's icon goes solid."),
     row(spec("__icon — image",
              '<span class="ns-sidenav__icon"><img src="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 '
              'viewBox=%220 0 40 40%22%3E%3Crect width=%2240%22 height=%2240%22 fill=%22%230176d3%22/%3E%3C/svg%3E" alt=""></span>'),
         spec("__icon — fallback", '<span class="ns-sidenav__icon"><i class="ph-fill ph-stack"></i></span>'),
         spec("__icon — open", '<details class="ns-sidenav__group" open><summary class="ns-sidenav__summary">'
                               '<span class="ns-sidenav__icon"><i class="ph-fill ph-stack"></i></span>'
                               '<span class="ns-sidenav__stitle">Open section</span>'
                               '<i class="ns-sidenav__caret ph ph-caret-right"></i></summary></details>', wide=True)),
     head("Icons in the pager"),
     note("The pager's title slot carries the TYPE glyph of what it points at — a video, an exercise, "
          "a section overview — so it says what you are about to open rather than only naming it. "
          "<code>training-nav.js</code> copies the glyph off the rail row it is already pointing at "
          "rather than working it out a second time, so the rail and the pager can never disagree "
          "about what a lesson is."),
     head("Motion"),
     note("The house rule, applied consistently: 120ms, ease-out, colour and background only — plus a "
          "2px slide toward the reader on hover. That transform is the one allowed here, because it "
          "reads as &ldquo;this is the row under your cursor&rdquo; rather than as decoration. All of it is off "
          "under <code>prefers-reduced-motion</code>."),
     head("A window column"),
     note("The rail runs from the site header to the bottom of the viewport and scrolls inside itself, "
          "so its progress footer sits at the bottom of the SCREEN rather than at the bottom of a list "
          "nobody scrolled to. That is why it is a flex column, not a grid — the last child has to be "
          "pushable to the end."),
     head("Room to scan"),
     note("Rows are taller than the type strictly needs. A rail is SCANNED, not read, and a scannable "
          "list needs air between its items far more than it needs to fit one more row on screen. "
          "Sections carry that further: half a rem of padding either side of the rule, so it reads as "
          "a separation rather than as a line."),
     head("Where things sit"),
     note("<b>Back to training</b> is the FIRST thing in the rail, above the search — a back-path "
          "buried under the navigation is a back-path nobody finds. <b>Progress</b> is the LAST, "
          "pinned to the bottom: it is a status readout you glance at, not somewhere you navigate to, "
          "so it stays in view while a long section scrolls past."),
     head("Sections are ruled, not spaced"),
     note("A hairline separates one section from the next, and an open section is bracketed top and "
          "bottom so its lessons read as belonging to it. Gaps alone would not survive a collapsed "
          "accordion — which is most of the time — where the whole rail becomes one undifferentiated "
          "list. Getting from one section to the next is the pager's job at the foot of the lesson, "
          "not a row inside the navigation."),
     head("A title can never break out"),
     note("Every ancestor of the rail is <code>min-width: 0</code> and every text cell truncates, so a "
          "long section or lesson name shortens rather than widening its container."),
     row(spec("long titles truncate",
              '<nav class="ns-sidenav ns-sidenav--boxed demo-w-sm">'
              '<details class="ns-sidenav__group" open><summary class="ns-sidenav__summary">'
              '<span class="ns-sidenav__icon"><i class="ph-fill ph-stack"></i></span>'
              '<span class="ns-sidenav__stitle">A section with a deliberately very long name</span>'
              '<i class="ns-sidenav__caret ph ph-caret-right"></i></summary>'
              '<div class="ns-sidenav__list">'
              '<a class="ns-sidenav__link" href="#!"><span class="ns-sidenav__num"><span>1</span></span>'
              '<i class="ns-sidenav__type ph-fill ph-play-circle"></i>'
              '<span class="ns-sidenav__text">A lesson title that runs on far past the rail width</span>'
              '<span class="ns-sidenav__meta">12m</span></a></div></details></nav>', wide=True)),
     head("States"),
     note("<code>.is-current</code> is the lesson you are on — solid brand, the same mark the docs rail "
          "uses. <code>.is-done</code> swaps the number for a tick and steps the title back."),
     note("<b>A row is two leading cells, and exactly one thing goes in each.</b> Cell one is the "
          "index — the lesson number, or a tick once it is behind you. Cell two is ONE icon: the lock "
          "if the lesson is members-only, otherwise what kind of lesson it is. Both cells are "
          "fixed-width flex boxes, so every title in the rail starts at the same x no matter which "
          "glyph landed above it."),
     note("<b>Which icon goes in cell two is decided in the TEMPLATE, not by CSS.</b> The row used to "
          "ship both a lock and a type glyph and hide one of them with a rule — and a row like that "
          "shows both the moment the stylesheet is stale, cached or slow to arrive, which is exactly "
          "what kept happening. It cannot overlap if it was never rendered. Prefer not emitting a "
          "thing over emitting it and hiding it, every time."),
     note("<code>.is-locked</code> additionally DIMS the row to 50%. Dimming is the honest signal in "
          "a scanned list: everything you can act on sits at full strength, everything you cannot is "
          "quieter — no warning colour, because &ldquo;you need an account&rdquo; is not an error. Hover "
          "restores it completely, since the row is still a link (it goes to the lesson page, which is "
          "where the sign-up is) and must never look disabled under the cursor. The same rule applies "
          "wherever a locked lesson appears: <code>.ns-list__item.is-locked</code> on a section page "
          "and <code>.ns-track-card__lesson.is-locked</code> in a track card preview."),
     note("What you will NOT find anywhere: a count of how many lessons are free, or a badge naming a "
          "tier. A tally like &ldquo;1 free&rdquo; is noise at best and looks broken at worst, and a section is "
          "a section — not a price. The lock on the individual row is the whole access story."),
     head("Spacing"),
     note("<b>The rail is dense, and that is the point.</b> It is a table of contents, not a menu: "
          "the value of it is seeing where you are in the WHOLE training at once, and every rem of "
          "padding is a lesson pushed off the screen. Rows sit on <code>--space-row-xs</code> and "
          "touch each other; sections sit <code>--space-gap-xs</code> apart. One spacing, essentially, "
          "and it is the smallest the system has."),
     note("<b>Nothing inside the rail is ruled.</b> It used to divide its sections with hairlines and "
          "run a guide line down the side of each lesson list — and with the page rule now drawn "
          "beside the whole column, that was three sets of lines in a space two inches wide. The "
          "section rows are already the heaviest thing in the component (bold, an icon, a caret), so "
          "they read as headings without help, and the indent is enough to say which lessons belong "
          "to them. The one rule the rail spends is the full-height line between this column and the "
          "lesson — one line, doing the dividing at the scale where dividing matters."),
     note("<b>Every row is one line.</b> A row is four things — marker, type, title, duration — and "
          "only the title may take the leftover room: the rest are <code>flex-shrink:0</code> and the "
          "row is <code>nowrap</code>, so a long title shortens rather than pushing its duration onto "
          "a second line. A rail whose rows are sometimes one line and sometimes two cannot be "
          "scanned, because the eye has to re-find the left edge on every row."),
     note("<b>The size variant is the first place to look when rail spacing is wrong.</b> "
          "<code>--sm</code> used to override <code>padding-block</code>, and since <code>--sm</code> "
          "is what every real page uses, that one line silently governed the whole component and beat "
          "every token on the base rule. The size variants now change TYPE only; <code>--lg</code> is "
          "the sole exception and says so explicitly."),
     head("The gate"),
     note("Ghost stops rendering a members-only post partway and leaves the excerpt visible. Without "
          "something in that gap the lesson simply appears to end mid-thought, which reads as a broken "
          "page rather than as a boundary. <code>.ns-lock</code> fills it."),
     note("<b>Full width and centred</b> — every other block in the lesson is capped at the reading "
          "measure and ranged left, because that is what prose wants. This is not prose, it is the END "
          "of it, and breaking both rules at once is what makes it impossible to mistake for another "
          "paragraph. The copy inside still keeps a measure, though: a centred line running the full "
          "width of a 58rem column is unreadable."),
     note("Ghost injects its OWN <code>&lt;aside class=\"gh-post-upgrade-cta\"&gt;</code> into the "
          "content of a post the visitor cannot read, and there is no setting to turn it off — so the "
          "page carried two gates in a row in two different design languages. It is hidden in "
          "<code>lock.css</code>, scoped to the reader: a members-only BLOG post has no gate of its "
          "own, and there Ghost's CTA is the only thing between the reader and a dead end."),
     note("The gate renders on <code>{{#unless access}}</code>, not <code>{{#unless @member}}</code>. A "
          "free member reading a PAID lesson is signed in and still cannot read it — "
          "<code>access</code> is the only value that answers &ldquo;can this visitor see the content&rdquo;, "
          "which is the actual question."),
     note("Quiet otherwise — a hairline, one glyph, one heading, two buttons. No tinted panel, no "
          "gradient, no urgency: the reader is being told &ldquo;not yet&rdquo;, not sold to. The wording "
          "follows Ghost's <code>visibility</code>, so a <code>paid</code> lesson offers plans and a "
          "<code>members</code> lesson offers a free account — promising the wrong thing at a paywall "
          "is worse than saying nothing."),
     row(spec(".ns-lock",
              '<div class="ns-lock"><span class="ns-lock__mark"><i class="ph-fill ph-lock-simple"></i></span>'
              '<h2 class="ns-lock__title">This lesson is for members</h2>'
              '<p class="ns-lock__body">Sign in to read the rest of it. Membership is free, and it '
              'unlocks every members-only lesson in the training.</p>'
              '<div class="ns-lock__actions">'
              '<a class="ns-btn ns-btn--primary" href="#!"><i class="ph-fill ph-lock-simple-open"></i>Create a free account</a>'
              '<a class="ns-btn ns-btn--outline" href="#!">Sign in</a></div></div>', wide=True)),
     head("Flat columns"),
     note("<code>.ns-reader--flat</code>: nothing between the columns but the gutter, and nothing "
          "inside them boxed. There was a full-height hairline in each gutter for a while, and it "
          "went — three columns with a strong line down each side of the middle one reads as a FRAME "
          "around the lesson, and a frame is a heavier claim than &ldquo;these are related columns of one "
          "page&rdquo;. The whitespace was already saying it."),
     note("Neither side column is boxed either: no card around the contents widget, no rule under a "
          "widget head, no line above the progress readout, nothing between sections in the rail. The "
          "lesson is the only thing on the page carrying any weight — which is correct, because it is "
          "the only thing on the page you came to read. Every hairline you remove from a rail is one "
          "less thing the eye has to decide is not a boundary it cares about."),
     head("The floating button"),
     note("Below <code>lg</code> the rail has nowhere to live. It used to be opened by the hamburger "
          "in the site header — which meant the SITE menu icon opened a lesson list, so the most "
          "familiar control on the page did not do what it says. The header is the header again, and "
          "the training carries its own control: <code>.ns-train-fab</code>, floating at the bottom "
          "centre. Bottom, because a lesson is read one-handed and that is where the thumb is; centre, "
          "because it belongs to neither the back gesture on the left nor the system affordances on "
          "the right."),
     note("It is the one elevated thing in a system built on hairlines — the exception that proves the "
          "rule. It genuinely floats above the page rather than sitting in it, so a shadow is an "
          "honest description of where it is rather than decoration. It carries the lesson count, "
          "because &ldquo;3/9&rdquo; answers <i>where am I</i> before anything opens, and it hides itself "
          "while the panel is open and at <code>lg</code>+ where the rail is already on screen."),
     row(spec(".ns-train-fab",
              '<div class="demo-fab-stage">'
              '<span class="ns-train-fab demo-fab-static">'
              '<i class="ph-fill ph-list-checks"></i><span>Contents</span>'
              '<span class="ns-train-fab__count">3/9</span></span></div>', wide=True)),
     note("It opens <code>.ns-lesson-panel--sheet</code>: the shared player panel, restyled for the "
          "training as a FULL-SCREEN sheet that rises from the bottom edge — the edge the button that "
          "summoned it sits on. Full screen because the rail is the contents of an entire training, "
          "so a part-height sheet puts the reader in a scroll-within-a-scroll to answer a question the "
          "full list answers at a glance. It is a mode, not a peek: you left the lesson to look at the "
          "map, and the ✕ pinned in its bar is how you come back."),
     head("Motion"),
     note("A lesson is a full page load, so without motion every navigation is a hard cut. The lesson "
          "ARRIVES instead: title, meta, media, body, then the pager, each 40ms behind the last — the "
          "order you read them in, so the page assembles along the path your eye was going to take "
          "anyway. Steps are 240ms and nothing moves more than <code>0.4rem</code>; the whole sequence "
          "is done inside half a second, because a lesson you have opened before should never feel "
          "performed at you."),
     note("<b>The sidebar does not animate.</b> It used to, and that was wrong: the content is what "
          "CHANGED when you navigated, so animating it tells you what is new — but the rail is the "
          "same list it was a moment ago with one row now marked. Animating it claims otherwise, and "
          "it makes the one fixed thing on the page, the thing you use to keep your place, the most "
          "restless. Only the reading column assembles; the rail is already there."),
     note("Every animation uses <code>both</code>, so if it never runs — reduced motion, an old "
          "engine, a stylesheet that failed — the element is simply there. Motion is never "
          "load-bearing."),
     row(spec("link states",
              '<nav class="ns-sidenav ns-sidenav--boxed demo-w-sm"><div class="ns-sidenav__list">'
              '<a class="ns-sidenav__link is-done" href="#!">'
              '<span class="ns-sidenav__num"><span>1</span></span>'
              '<i class="ns-sidenav__type ph-fill ph-article"></i>'
              '<span class="ns-sidenav__text">What is Salesforce?</span>'
              '<span class="ns-sidenav__meta">6m</span></a>'
              '<a class="ns-sidenav__link is-current" href="#!"><span class="ns-sidenav__num"><span>2</span></span>'
              '<span class="ns-sidenav__text">Set up a free org</span>'
              '<span class="ns-sidenav__meta">12m</span></a>'
              '<a class="ns-sidenav__link" href="#!"><span class="ns-sidenav__num"><span>3</span></span>'
              '<span class="ns-sidenav__text">How to use this training</span>'
              '<span class="ns-sidenav__meta">5m</span></a>'
              '<a class="ns-sidenav__link is-locked" href="#!">'
              '<span class="ns-sidenav__num"><span>4</span></span>'
              '<i class="ns-sidenav__type ns-sidenav__type--lock ph-fill ph-lock-simple"></i>'
              '<span class="ns-sidenav__text">Objects and fields</span>'
              '<span class="ns-sidenav__meta">18m</span></a>'
              '</div></nav>', wide=True)))

page("Training", "training-section", "Training section",
     "A section page is the contents page for that section: what it covers, what you will be able to "
     "do, and the lessons in order. The rail is on the left, breadcrumbs above, and the same "
     "components as everywhere else in between.",
     head("Head — the number IS the hero"),
     note("The section used to announce itself three times over the same two lines: a breadcrumb, a "
          "small numbered disc under it, and a <code>// TRAINING SECTION</code> kicker beside that. "
          "The breadcrumb already says where you are, so the chip and the kicker are gone and the "
          "number became the hero's GROUND — set at the full height of the band, anchored to the left "
          "edge, drawn into the background rather than written on top of it. It is scenery, not a "
          "label: you read the title, and the number is the size of the place you are standing in."),
     note("It is an <code>&lt;svg&gt;</code> rather than a <code>font-size</code>, because &ldquo;as tall as "
          "the hero&rdquo; is a relationship CSS cannot express when the hero's height comes from its own "
          "content. <code>preserveAspectRatio</code> states it exactly, at any content length and any "
          "viewport, with no clamp to keep in sync. Low fill, slightly stronger stroke, "
          "<code>paint-order: stroke fill</code> so the outline keeps an even weight instead of the "
          "fill eating half of it from inside."),
     note("It sits WHOLE in the frame and <code>.ns-hero--numbered</code> indents the copy past it, so "
          "the number and the title share the band rather than stacking. An earlier version ran the "
          "digit off the left edge — at that size a crop reads as a rendering fault, not as a "
          "decision. <code>aria-hidden</code>, since the section is already named twice above it."),
     head("Breadcrumb, title, meta"),
     row(spec(".ns-hero + .ns-track-hero",
              '<div class="ns-hero ns-hero--sm ns-hero--start ns-hero--dots">'
              '<div class="ns-hero__inner">'
              '<nav class="ns-crumbs"><a class="ns-crumbs__link" href="#!">'
              '<i class="ph ph-house"></i>Home</a>'
              '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
              '<a class="ns-crumbs__link" href="#!"><i class="ph ph-graduation-cap"></i>Training</a>'
              '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
              '<span class="ns-crumbs__current"><span>Build Your First App</span></span></nav>'
              '<div class="ns-cluster demo-mt"><span class="ns-track-hero__index">02</span>'
              '<span class="ns-badge ns-badge--glass ns-badge--dot">In progress</span></div>'
              '<h1 class="ns-hero__title">Build Your First App</h1>'
              '<p class="ns-hero__sub">A custom object, the fields that matter, a layout people can '
              'actually use, and one report that proves it works.</p>'
              '<div class="ns-track-hero__meta">'
              + "".join('<div class="ns-stat ns-stat--light ns-stat--sm">'
                        '<span class="ns-stat__value">%s</span><span class="ns-stat__label">%s</span></div>'
                        % (v, l) for v, l in (("4", "lessons"), ("1h 20m", "length"), ("45%", "complete")))
              + '</div>'
              '<div class="ns-hero__actions"><a class="ns-btn ns-btn--white" href="#!">Continue lesson 3</a>'
              '</div></div></div>', wide=True)),
     head("The page — rail, overview, lessons"),
     row(spec(".ns-page--rail-start",
              '<div class="ns-page demo-fill"><div class="ns-page__inner">'
              '<div class="ns-page__main ns-shell ns-shell--sidebar">'
              '<aside class="ns-shell__aside">' + _sidenav() + '</aside>'
              '<div>'
              '<div class="ns-prose demo-w-2xl"><h2>What this section covers</h2>'
              '<p>You will build a small but complete app: a custom object, the fields that matter, a '
              'layout people can use, and a report that answers a question.</p></div>'
              '<h3 class="sg-h3">By the end you can</h3>'
              '<ul class="ns-list ns-list--check demo-w-2xl">'
              '<li class="ns-list__item">Create a custom object and choose its record name</li>'
              '<li class="ns-list__item">Pick field types that will not need reworking</li>'
              '<li class="ns-list__item">Build a layout and a list view people actually use</li></ul>'
              '<h3 class="sg-h3">Lessons</h3>'
              '<ul class="ns-list ns-list--boxed demo-w-2xl">'
              + "".join('<li class="ns-list__item"><span class="ns-list__title">%s</span>'
                        '<span class="ns-list__meta">%s</span></li>' % (t, d)
                        for t, d, _s in _LESSONS)
              + '</ul>'
              '<div class="ns-note ns-note--info demo-w-2xl demo-mt">'
              '<i class="ns-note__icon ph-fill ph-info"></i>'
              '<div class="ns-note__body"><span class="ns-note__title">Before you start</span> — '
              'you need the free Developer org from section 1.</div></div>'
              '</div></div></div></div>', wide=True)),
     note("The rail uses <code>.ns-shell--sidebar</code>, so it is one column below <code>lg</code> "
          "with the navigation stacked above the content — the order a reader on a phone wants."))

page("Training", "training-lesson", "Training lesson",
     "The reading shell. Three columns at the top end: the section rail, the lesson, and an "
     "on-this-page rail. The reading column stays capped at the prose measure whatever the window "
     "does — line length decides whether a lesson gets read.",
     head("The shell"),
     note("<code>.ns-reader--both</code> &rarr; <code>__rail</code> · <code>__main</code> "
          "(<code>__head</code>, <code>__media</code>, <code>__body</code>, <code>__foot</code>) · "
          "<code>__aside</code>. Both rails stick under the header and scroll independently; below "
          "<code>lg</code> they become the bar and a drawer."),
     row(spec(".ns-reader--both",
              SUBBAR + '<div class="ns-reader ns-reader--both demo-fill demo-w-full">'
              '<aside class="ns-reader__rail">' + _sidenav() + '</aside>'
              '<div class="ns-reader__main">'
              '<div class="ns-reader__head">'
              '<nav class="ns-crumbs ns-crumbs--sm"><a class="ns-crumbs__link" href="#!">Training</a>'
              '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
              '<a class="ns-crumbs__link" href="#!">Build Your First App</a>'
              '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
              '<span class="ns-crumbs__current"><span>Create a custom object</span></span></nav>'
              '<h1 class="ns-reader__title">Create a custom object</h1>'
              '<div class="ns-reader__meta">'
              '<span class="ns-lesson-type ns-lesson-type--video"><i class="ph-fill ph-video"></i>Video</span>'
              '<span class="ns-lesson-chip"><i class="ph ph-clock"></i>12 min</span>'
              '<span class="ns-lesson-chip"><i class="ph ph-flag"></i>Lesson 1 of 4</span>'
              '<span class="ns-badge ns-badge--dot ns-badge--success">Free</span>'
              '</div></div>'
              '<div class="ns-reader__media"><div class="ns-video demo-media">'
              '<i class="ph ph-video"></i></div></div>'
              '<div class="ns-reader__body ns-prose">'
              '<p>Naming, the record name field, and the settings that are painful to change later.</p>'
              '<h2>Create the object</h2>'
              '<p>Setup &rarr; Object Manager &rarr; Create. The plural label is what shows in the tab, '
              'so get it right the first time.</p>'
              '<pre><code>Label:        Project\nPlural:       Projects\nRecord Name:  Project Name</code></pre>'
              '</div>'
              '<div class="ns-reader__foot">'
              '<a class="ns-reader__step" href="#!"><span class="ns-reader__step-label">← Previous</span>'
              '<span class="ns-reader__step-title">How to use this training</span></a>'
              '<a class="ns-reader__step ns-reader__step--next" href="#!">'
              '<span class="ns-reader__step-label">Next →</span>'
              '<span class="ns-reader__step-title">Fields that earn their place</span></a>'
              '</div></div>'
              '<aside class="ns-reader__aside">'
              '<div class="ns-widget ns-widget--toc ns-widget--sunken">'
              '<div class="ns-widget__head"><span class="ns-widget__title">On this page</span></div>'
              '<div class="ns-widget__body">'
              '<a class="ns-toc__link" aria-current="true" href="#!">Create the object</a>'
              '<a class="ns-toc__link" href="#!">Name it properly</a>'
              '<a class="ns-toc__link ns-toc__link--sub" href="#!">Record name</a></div></div>'
              '<div class="ns-widget ns-widget--cta ns-widget--brand">'
              '<div class="ns-widget__head"><span class="ns-widget__title">Stuck?</span></div>'
              '<div class="ns-widget__body"><p>Comments are open under every lesson.</p>'
              '<a class="ns-btn ns-btn--outline ns-btn--sm" href="#!">Ask a question</a></div></div>'
              '</aside></div>', wide=True)),
     head("Where the page starts"),
     note("The reader has NO top padding. A page should start at the site header, not float below it, "
          "so whatever runs first — a hero band or the lesson head — supplies its own breathing room "
          "and there is never a dead strip under the navbar. The COLUMNS carry the top space instead, "
          "which is what lets a full-bleed hero sit flush above the reader while the rails still clear "
          "the header."),
     note("Inside, the rhythm is deliberately loose: the column gap scales with the viewport "
          "(<code>clamp(1.75rem, 3.5vw, 3.5rem)</code>), blocks are 2.5rem apart and the rules "
          "between them 3.5rem. Cramped is the failure mode of a three-column layout — the columns "
          "already do the work of separating things, so the content inside them can afford air."),
     head("Full width + rules"),
     note("The reader shell is <code>--fluid</code>: the reading column is already capped at "
          "<code>--container-read</code>, so letting the SHELL fill the window just gives the rails "
          "their natural width on a big screen instead of stranding everything in the middle. Blocks "
          "inside are separated by <code>__sep</code> — a hairline, because that is how this system "
          "divides things, rather than by space alone."),
     row(spec(".ns-reader__sep",
              '<div class="demo-w-full"><p class="demo-type-small">The lesson</p>'
              '<hr class="ns-reader__sep"><p class="demo-type-small">Prev / next</p>'
              '<hr class="ns-reader__sep"><p class="demo-type-small">Comments</p>'
              '<hr class="ns-reader__sep"><p class="demo-type-small">The newsletter band</p></div>', wide=True)),
     head("Access state"),
     note("Free or members-only is stated as a badge in the head AND, when a lesson is locked and you "
          "are signed out, as a note above the content — a chip alone is easy to miss when the article "
          "simply stops."),
     row(spec("locked",
              '<div class="ns-note ns-note--warning demo-w-xl"><i class="ns-note__icon ph-fill ph-lock"></i>'
              '<div class="ns-note__body"><span class="ns-note__title">Members only</span> — sign in to '
              'read the rest of this lesson. Membership is free.</div>'
              '<a class="ns-btn ns-btn--primary ns-btn--sm ns-note__action" href="#!">Sign in</a></div>', wide=True)),
     head("The newsletter band"),
     note("One ask, after everything else is read, with room to explain what subscribing actually "
          "does. It replaced a rail widget that said &ldquo;new lessons by email&rdquo; and nothing more. Medium "
          "height on purpose — tall enough to be a real explanation, short enough not to compete with "
          "the lesson above it."),
     row(spec(".ns-news-band",
              '<div class="ns-news-band ns-news-band--brand demo-w-full">'
              '<div><span class="ns-kicker"><i class="ph-fill ph-envelope-simple"></i>Training newsletter</span>'
              '<h2 class="ns-news-band__title">Get every new lesson as it lands</h2>'
              '<p class="ns-news-band__body">Turn this on and anything added to the training — a new '
              'lesson, a new section, a rewrite of one you have already read — arrives in your inbox. '
              'Nothing else is sent to it.</p>'
              '<ul class="ns-list ns-list--check ns-list--sm ns-news-band__points">'
              '<li class="ns-list__item">New lessons and sections, the day they publish</li>'
              '<li class="ns-list__item">Updates to lessons you have already worked through</li>'
              '<li class="ns-list__item">No marketing, no digest, no third parties</li></ul></div>'
              '<form class="ns-news-band__form">'
              '<label class="ns-field"><span class="ns-field__label">Email address</span>'
              '<input class="ns-input" placeholder="you@example.com"></label>'
              '<button class="ns-btn ns-btn--primary ns-btn--block">Turn on training updates</button>'
              '<span class="ns-news-band__note">Free. One click to unsubscribe.</span></form>'
              '</div>', wide=True)),
     head("Prev / next"),
     row(spec("both — half and half",
              '<div class="ns-reader__foot has-prev demo-w-full">'
              '<a class="ns-reader__step" href="#!">'
              '<span class="ns-reader__step-label">← Previous</span>'
              '<span class="ns-reader__step-title">What is Salesforce?</span></a>'
              '<a class="ns-reader__step ns-reader__step--next" href="#!">'
              '<span class="ns-reader__step-label">Next →</span>'
              '<span class="ns-reader__step-title">Fields that earn their place</span></a></div>', wide=True)),
     row(spec("next only", 
              '<div class="ns-reader__foot demo-w-full">'
              '<span class="ns-reader__step ns-reader__step--empty"></span>'
              '<a class="ns-reader__step ns-reader__step--next" href="#!">'
              '<span class="ns-reader__step-label">Next →</span>'
              '<span class="ns-reader__step-title">Fields that earn their place</span></a></div>', wide=True)),
     note("Prev and next are pinned to explicit grid columns, so the pair always reads half-and-half "
          "on ONE row and a lone &ldquo;next&rdquo; still sits on the right rather than stretching across. The "
          "spacer is only a no-JS fallback — <code>.has-prev</code> removes it once a previous link "
          "exists, which is what stopped &ldquo;next&rdquo; wrapping to a second row."),
     note("The sequence includes section OVERVIEWS, not just lessons: finishing a section lands you on "
          "the next section's overview, because you want to know what it is about before its first "
          "lesson drops you into it. Overview rows carry an explicit label naming their section — "
          "&ldquo;Overview&rdquo; alone tells you nothing in a pager."))



# ═════════════════════════════════════════════════════════════════════════════
# RENDERING
# ═════════════════════════════════════════════════════════════════════════════
# Sidebar order: the vocabulary first, then the pieces, then the pages built
# out of them. Home comes LAST because it is the payoff, not the primer.
GROUPS = ["Foundation", "Components", "Home", "Training", "Pages"]

RULES = [
    ("Hairlines, not shadows",
     "One 1px border is the structuring device. Elevation means the border brightens to brand — "
     "never a floating lift."),
    ("Monospace is a material",
     "Fira Code renders every index, duration, timestamp, status tag and kicker. Inter is for prose "
     "and headings only."),
    ("One signal colour",
     "Brand blue is the only colour that means &ldquo;interactive&rdquo;. Status is a dot plus mono text, never "
     "a background wash."),
    ("Sharp, specific geometry",
     "Cards 6px, buttons and inputs 4px. Pills are reserved for true pills — tags and pager controls."),
    ("Motion is instant",
     "120–180ms plain ease-out. No spring, no bounce, no hover lift. The one exception is the float "
     "loop on illustrations."),
]


def render_block(b):
    kind = b[0]
    if kind == "note":
        return f'<p class="sg-note">{b[1]}</p>'
    if kind == "head":
        return f'<h3 class="sg-h3">{b[1]}</h3>'
    if kind == "swatches":
        cells = "".join(
            f'<div class="sg-swatch"><span class="sg-swatch__chip" data-swatch="{n}"></span>'
            f'<code class="sg-label">{n}</code></div>' for n in b[1])
        return f'<div class="sg-swatches">{cells}</div>'
    if kind == "tokens":
        rows = "".join(f'<tr><td><code>{n}</code></td><td class="sg-token-val" data-token="{n}"></td></tr>'
                       for n in b[1])
        return ('<table class="sg-tokens"><thead><tr><th>Token</th><th>Value</th></tr></thead>'
                f'<tbody>{rows}</tbody></table>')
    out = ['<div class="sg-row">']
    for _, label, markup, wide, dark in b[1]:
        cls = "sg-spec sg-spec--wide" if wide else "sg-spec"
        stage = "sg-stage sg-stage--dark" if dark else "sg-stage"
        out.append(f'<div class="{cls}"><div class="{stage}">{markup}</div>'
                   f'<code class="sg-label">{label}</code></div>')
    out.append("</div>")
    return "".join(out)


def sidebar(current):
    parts = ['<a class="sg-side__home' + (" is-current" if current == "index" else "") +
             '" href="index.html"><i class="ph ph-house"></i>Overview</a>']
    for g in GROUPS:
        parts.append(f'<div class="sg-side__group"><span class="sg-side__title">{g}</span>')
        for grp, slug, title, _, _ in PAGES:
            if grp != g:
                continue
            cur = " is-current" if slug == current else ""
            parts.append(f'<a class="sg-side__link{cur}" href="{slug}.html">{title}</a>')
        parts.append("</div>")
    return "".join(parts)


MOON = ('<svg class="dark:hidden" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" '
        'aria-hidden="true"><path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1-9-9Z"/></svg>')
SUN = ('<svg class="hidden dark:block" width="18" height="18" viewBox="0 0 24 24" fill="none" '
       'stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">'
       '<circle cx="12" cy="12" r="4" fill="currentColor"/>'
       '<path d="M12 2v2m0 16v2M4.2 4.2l1.4 1.4m12.8 12.8 1.4 1.4M2 12h2m16 0h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>')

SHELL = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Developer Console</title>
<!-- The theme's real built CSS, plus the style guide's own chrome. Both are
     generated by `yarn build`. This page carries no embedded CSS of its own —
     see the guard at the foot of scripts/build-styleguide.py. -->
<link rel="stylesheet" href="../assets/built/screen.css">
<link rel="stylesheet" href="../assets/built/styleguide.css">
<script src="styleguide.js" defer></script>
<script>
  try {{ var t = localStorage.getItem('ns-theme');
         if (t) document.documentElement.setAttribute('data-theme', t); }} catch (e) {{}}
</script>
</head>
<body>
<div class="sg-shell">

  <aside class="sg-side">
    <div class="sg-side__brand">
      <span class="ns-chip ns-chip--xs ns-chip--solid"><i class="ph-fill ph-terminal-window"></i></span>
      <span class="sg-side__mark">Developer Console</span>
    </div>
    {sidebar}
  </aside>

  <main class="sg-main">
    <div class="sg-top">
      <span class="ns-kicker ns-kicker--plain">{group}</span>
      <button class="icon-btn ml-auto" data-theme-toggle aria-label="Toggle dark mode">{moon}{sun}</button>
    </div>
    <div class="sg-body">
{content}
    </div>
  </main>
</div>
</body>
</html>
"""

SCRIPT = """/* styleguide.js — generated by scripts/build-styleguide.py.
   Three jobs, each of which would otherwise need an inline attribute:
     1. the dark-mode toggle
     2. printing each token's COMPUTED value, so the tables cannot go stale
     3. applying demo-only widths (progress bars) and swatch colours */
(function () {
  'use strict';

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-theme-toggle]');
    if (!btn) return;
    var h = document.documentElement;
    var next = h.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    h.setAttribute('data-theme', next);
    try { localStorage.setItem('ns-theme', next); } catch (err) {}
  });

  function paint() {
    var cs = getComputedStyle(document.documentElement);
    document.querySelectorAll('.sg-token-val').forEach(function (el) {
      el.textContent = cs.getPropertyValue(el.dataset.token).trim() || '\\u2014';
    });
    document.querySelectorAll('[data-swatch]').forEach(function (el) {
      el.style.background = 'var(' + el.dataset.swatch + ')';
    });
    document.querySelectorAll('[data-demo-width]').forEach(function (el) {
      el.style.width = el.dataset.demoWidth + '%';
    });
  }
  if (document.readyState !== 'loading') paint();
  else document.addEventListener('DOMContentLoaded', paint);
})();
"""


def build():
    OUT.mkdir(exist_ok=True)
    (OUT / "styleguide.js").write_text(SCRIPT)
    order = [(g, s, t) for g, s, t, _, _ in PAGES]

    first = order[0][1]
    rules = "".join(
        f'<div class="ns-card ns-card--sm">'
        f'<span class="ns-index ns-stat__value ns-stat--brand">{i + 1:02d}</span>'
        f'<h3 class="ns-card__title">{t}</h3>'
        f'<p class="ns-card__body demo-type-small">{d}</p></div>'
        for i, (t, d) in enumerate(RULES))

    layers = "".join(
        f'<a class="ns-card ns-card--sm ns-card--interactive" href="{slug}.html">'
        f'<span class="ns-card__meta">Layer {i}</span>'
        f'<h3 class="ns-card__title">{name}</h3>'
        f'<p class="ns-card__body demo-type-small">{desc}</p></a>'
        for i, (name, desc, slug) in enumerate((
            ("Foundation", "Tokens, variables, mixins and helpers. Declares values, paints nothing.", "colors"),
            ("Elements", "Bare HTML — what a tag looks like with no class on it.", "prose"),
            ("Components", "The UI library. One file per component, each with its variants.", "button"))))

    counts = {g: sum(1 for x in PAGES if x[0] == g) for g in GROUPS}
    home = f'''
      <span class="ns-kicker">Design system</span>
      <h1 class="sg-h1">Developer Console</h1>
      <p class="sg-lede">The design language behind Namaste Salesforce. Everything on these pages is
      rendered from the theme's real <code>assets/built/screen.css</code> — if it looks right here,
      it looks right on the site.</p>

      <div class="sg-row ns-cluster">
        <a class="ns-btn ns-btn--primary ns-btn--lg" href="{first}.html">Start
          <i class="ns-btn__icon ns-btn__icon--nudge ph ph-arrow-right"></i></a>
        <a class="ns-btn ns-btn--outline ns-btn--lg" href="button.html">Jump to components</a>
      </div>

      <h3 class="sg-h3">The five rules</h3>
      <div class="ns-grid ns-grid--tight">{rules}</div>

      <h3 class="sg-h3">The layers</h3>
      <p class="sg-note">The CSS is three layers, each with its own <code>index.css</code>. A later
      layer spends what the earlier ones declare, never the other way round. Feature styling lives in
      the component layer as <code>site-*.css</code>, imported last.
      {counts["Foundation"]} foundation pages, {counts["Components"]} component pages.</p>
      <div class="ns-grid ns-grid--tight">{layers}</div>

      <h3 class="sg-h3">Naming</h3>
      <p class="sg-note">Every component follows one contract, so variants compose instead of
      multiplying classes:</p>
      <table class="sg-tokens">
        <thead><tr><th>Pattern</th><th>Means</th></tr></thead>
        <tbody>
          <tr><td><code>.ns-thing</code></td><td>the base — the smallest version that stands alone</td></tr>
          <tr><td><code>.ns-thing--variant</code></td><td>one axis at a time: size, shape, tone or state</td></tr>
          <tr><td><code>.ns-thing__part</code></td><td>a named internal part</td></tr>
          <tr><td><code>.is-state</code></td><td>a runtime state a script toggles</td></tr>
        </tbody>
      </table>
    '''
    (OUT / "index.html").write_text(render_icons(SHELL.format(
        title="Overview", group="Overview", sidebar=sidebar("index"),
        content=home, moon=MOON, sun=SUN)))

    for idx, (group, slug, title, blurb, blocks) in enumerate(PAGES):
        prev_ = order[idx - 1] if idx else None
        next_ = order[idx + 1] if idx + 1 < len(order) else None
        pager = ['<nav class="sg-pager">']
        pager.append(f'<a href="{prev_[1]}.html"><span>← Previous</span><b>{prev_[2]}</b></a>'
                     if prev_ else '<span></span>')
        pager.append(f'<a class="sg-pager__end" href="{next_[1]}.html"><span>Next →</span><b>{next_[2]}</b></a>'
                     if next_ else '<span></span>')
        pager.append("</nav>")

        content = (f'<h1 class="sg-h1">{title}</h1><p class="sg-lede">{blurb}</p>'
                   + "".join(render_block(b) for b in blocks) + "".join(pager))
        (OUT / f"{slug}.html").write_text(render_icons(SHELL.format(
            title=title, group=group, sidebar=sidebar(slug),
            content=content, moon=MOON, sun=SUN)))

    # ── Guards ──────────────────────────────────────────────────────────────
    pages = sorted(OUT.glob("*.html"))
    texts = {f.name: f.read_text() for f in pages}
    html = "".join(texts.values())

    inline = [n for n, t in texts.items() if 'style="' in t or "<style" in t]
    if inline:
        raise SystemExit("INLINE CSS found in: " + ", ".join(inline)
                         + "\n  → move it to assets/css/styleguide.css as a .sg-* or .demo-* class.")

    # No icon font ships any more, so nothing may reach the output still
    # asking for one. render_icons() has already turned every `<i class="ph-*">`
    # specimen into inline SVG (and raised on an unknown name); anything left is
    # a glyph class written somewhere it could not reach, which would render as
    # empty space on the page.
    leftover = sorted(set(re.findall(r"\bph-[a-z0-9-]+", html)))
    drawn = len(re.findall(r'class="ns-icon', html))

    print(f"styleguide/ — {len(pages)} pages, {drawn} inline icons "
          f"from {len(ICONS)} in the set, no inline CSS")
    if leftover:
        raise SystemExit("ICON-FONT CLASSES LEFT IN THE OUTPUT: " + ", ".join(leftover)
                         + "\n  → these render as nothing. Write them as"
                           " <i class=\"ph ph-name\"></i> so render_icons() can convert"
                           " them, or call icon(\"name\") directly.")
    print("every icon resolved against partials/icons.hbs")


if __name__ == "__main__":
    build()
