#!/usr/bin/env python3
"""build-styleguide.py — generate the Developer Console style guide.

A small static SITE (not one long page) under styleguide/:

    index.html          the home page — the rules, the layers, a Start button
    <page>.html         one page per foundation topic, element family,
                        component and module, each with its own specimens

Every page shares a sidebar, a theme toggle and prev/next paging, and renders
against the theme's real assets/built/screen.css — what you see is what the
site ships. Run it with `yarn styleguide` (or `python3 scripts/build-styleguide.py`
from the theme root), then serve the folder.

Edit THIS file, never the generated HTML.
"""
import pathlib
import re

OUT = pathlib.Path("styleguide")
PAGES = []          # (group, slug, title, blurb, blocks)


# ── Page + block helpers ─────────────────────────────────────────────────────
def page(group, slug, title, blurb, *blocks):
    PAGES.append((group, slug, title, blurb, list(blocks)))


def spec(label, markup, wide=False):
    """One specimen: the rendered thing, with its class string underneath."""
    return ("spec", label, markup, wide)


def row(*specs):
    return ("row", specs)


def note(text):
    return ("note", text)


def head(text):
    return ("head", text)


def swatches(title, names):
    return ("swatches", title, names)


def tokens(title, names, kind="value"):
    return ("tokens", title, names, kind)


def raw(html):
    return ("raw", html)


# ═════════════════════════════════════════════════════════════════════════════
# FOUNDATION
# ═════════════════════════════════════════════════════════════════════════════
page("Foundation", "colors", "Colour",
     "One working blue carries every interactive meaning. Everything else is a "
     "surface, an ink, or a status — and status never becomes a background wash.",
     head("Brand scale"),
     swatches("--color-brand-*", [f"--color-brand-{s}" for s in (50, 100, 200, 300, 400, 500, 600, 700, 800, 900)]),
     note("<code>--color-brand-500</code> is <code>#0176D3</code>, the one signal colour. "
          "600 is the hover step; 900 is the navy that grounds dark mode and every hero."),
     head("Accent scale"),
     swatches("--color-accent-*", [f"--color-accent-{s}" for s in (50, 100, 200, 300, 400, 500, 600, 700, 800, 900)]),
     note("Worth knowing: the accent scale is currently a near-duplicate of brand — "
          "<code>--color-accent-500</code> is the same <code>#0176d3</code>. That is consistent with "
          "&ldquo;one signal colour&rdquo;, but it does mean the <code>--accent</code> variants on buttons, "
          "chips and badges read almost identically to the default. Either give accent a genuinely "
          "different hue, or drop those variants."),
     head("Semantic roles"),
     note("These flip under <code>[data-theme=\"dark\"]</code>. Use the ROLE, not a literal — "
          "that's what makes dark mode work without a single <code>dark:</code> in markup."),
     swatches("surfaces", ["--color-surface", "--color-surface-raised", "--color-surface-sunken"]),
     swatches("ink + lines", ["--color-ink", "--color-muted", "--color-label", "--color-border", "--color-grid"]),
     head("Status"),
     swatches("status", ["--color-success", "--color-warning", "--color-error"]),
     note("Status colours appear as a dot plus mono text, or as a hairline ring — see "
          "<a href=\"badge.html\">Badge</a> and <a href=\"note.html\">Note</a>. The only "
          "tinted blocks in the system are notes, held at 4–6%."))

page("Foundation", "typography", "Typography",
     "Two materials on purpose: Inter for prose and headings, Fira Code for every "
     "index, label, duration and status. That's what makes data read as data without colour.",
     head("Prose scale — Inter"),
     *[row(spec(n, f'<span style="font-size:var({n});font-family:var(--font-heading);'
                   f'font-weight:var(--weight-heading);line-height:1.2">{t}</span>', wide=True))
       for n, t in (("--size-display", "Display"), ("--size-h1", "Heading 1"), ("--size-h2", "Heading 2"),
                    ("--size-h3", "Heading 3"), ("--size-h4", "Heading 4"), ("--size-h5", "Heading 5"))],
     row(spec("--size-lead", '<span style="font-size:var(--size-lead);color:var(--color-muted)">Lead paragraph — the sentence under a title.</span>', wide=True)),
     row(spec("--size-body", '<span style="font-size:var(--size-body)">Body copy at the reading size.</span>', wide=True)),
     row(spec("--size-small", '<span style="font-size:var(--size-small)">Small — metadata and captions.</span>', wide=True)),
     head("Label scale — Fira Code"),
     note("Uppercase, tracked, 700. Every kicker, index, timestamp, column header and status tag."),
     row(spec("ns-label", '<span class="ns-label">Lesson duration</span>'),
         spec("ns-index", '<span class="ns-index" style="font-size:1.5rem">04</span>'),
         spec("--size-mono", '<code style="font-size:var(--size-mono)">SELECT Id FROM Account</code>')),
     head("Weights + leading"),
     tokens("weights", ["--weight-heading", "--weight-semibold", "--weight-medium", "--weight-regular", "--weight-label"]),
     tokens("leading", ["--leading-tight", "--leading-heading", "--leading-body"]),
     tokens("tracking", ["--tracking-label"]))

page("Foundation", "spacing", "Spacing",
     "Named distances that components agree on, so a card is padded like every other "
     "card and sections breathe at one rhythm site-wide.",
     head("Component rhythm"),
     tokens("space", ["--space-card", "--space-card-lg", "--space-gap", "--space-gap-sm", "--space-row"]),
     head("Page rhythm"),
     tokens("space", ["--space-section", "--space-section-sm", "--space-gutter", "--space-navbar"]),
     head("Containers"),
     tokens("width", ["--container-prose", "--container-narrow", "--container-page"]),
     note("Markup usually reaches for the matching <code>max-w-*</code> utility; these exist "
          "for custom CSS, the <a href=\"layout.html\">layout component</a>, and off-site assets."))

page("Foundation", "borders", "Borders &amp; radii",
     "The hairline IS the structuring device. Geometry is sharp and specific — not "
     "&ldquo;12px and pills everywhere&rdquo;.",
     head("Widths"),
     row(spec("--border-hairline", '<div style="width:9rem;height:3rem;border:var(--border-hairline) solid var(--color-border);border-radius:var(--radius-card)"></div>', wide=True),
         spec("--border-strong", '<div style="width:9rem;height:3rem;border:var(--border-strong) solid var(--color-brand-500);border-radius:var(--radius-card)"></div>', wide=True)),
     head("Radii"),
     row(*[spec(n, f'<div style="width:6rem;height:3rem;border:1px solid var(--color-border);'
                   f'background:var(--color-surface-raised);border-radius:var({n})"></div>', wide=True)
           for n in ("--radius-card", "--radius-btn", "--radius-sm", "--radius-pill")]),
     note("Cards 6px, buttons and inputs 4px. <code>--radius-pill</code> is reserved for TRUE pills — "
          "tags, pager controls, avatars — never the default button or card."))

page("Foundation", "elevation", "Elevation",
     "Shadows are near-flat. Depth is expressed by a border going brand, not by a card "
     "floating off the page. Only genuinely floating layers — dropdowns, drawers — lift.",
     row(*[spec(n, f'<div style="width:8rem;height:4rem;border-radius:var(--radius-card);'
                   f'background:var(--color-surface-raised);box-shadow:var({n})"></div>', wide=True)
           for n in ("--shadow-card", "--shadow-raised", "--shadow-brand", "--shadow-focus")]),
     head("The z-index ladder"),
     tokens("z", ["--z-nav", "--z-subnav", "--z-dropdown", "--z-drawer", "--z-tooltip"]),
     note("Never write a raw z-index in a component — take the next rung, or add one here."))

page("Foundation", "motion", "Motion",
     "Fast and literal: state changes resolve in 120–180ms with a plain ease-out. "
     "No spring, no bounce, no hover lift. Everything below is disabled under "
     "<code>prefers-reduced-motion</code>.",
     tokens("duration", ["--duration-fast", "--duration-base"]),
     tokens("easing", ["--ease-out", "--ease-out-strong"]),
     head("In use"),
     row(spec("ns-transition", '<div class="ns-card ns-card--sm ns-transition" style="width:12rem;cursor:pointer">Hover me</div>', wide=True),
         spec(".ns-card--interactive", '<div class="ns-card ns-card--sm ns-card--interactive" style="width:12rem;cursor:pointer">Hover me</div>', wide=True)),
     note("The keyframes the system ships: <code>fade-up</code>, <code>ns-float</code>, "
          "<code>marquee</code>, <code>ns-spin</code>."))

page("Foundation", "mixins", "Mixins",
     "Recurring treatments defined once as Tailwind <code>@utility</code> recipes — usable as a "
     "class in markup AND via <code>@apply</code> inside component CSS.",
     row(spec("ns-label", '<span class="ns-label">Section label</span>'),
         spec("ns-index", '<span class="ns-index" style="font-size:1.25rem">07</span>'),
         spec("ns-dot-marker", '<span class="ns-dot-marker" style="background:var(--color-success)"></span>')),
     row(spec("ns-hairline", '<div class="ns-hairline" style="width:9rem;height:3rem;border-radius:var(--radius-card)"></div>', wide=True),
         spec("ns-transition", '<button class="ns-btn ns-btn--outline ns-transition">Instant hover</button>', wide=True)),
     note("<code>ns-hairline</code> draws its border with an inset shadow, so it never changes "
          "the element's box size — useful on thumbnails and tags."))

# ═════════════════════════════════════════════════════════════════════════════
# ELEMENTS
# ═════════════════════════════════════════════════════════════════════════════
PROSE = '''<div class="ns-prose" style="max-width:38rem">
<h2>The data model in one sentence</h2>
<p>Objects are tables, fields are columns, records are rows — and <a href="#!">relationships</a>
are what make it a CRM rather than a spreadsheet.</p>
<h3>Field types worth knowing</h3>
<p>Press <kbd>Cmd</kbd> + <kbd>K</kbd> to search, or run <code>SELECT Id FROM Account</code>.
<mark>Highlighted</mark> text and an <abbr title="Salesforce Object Query Language">SOQL</abbr>
abbreviation. <small>Last reviewed March 2026.</small></p>
</div>'''

page("Elements", "el-typography", "Text elements",
     "Bare tags inside a reading context — <code>.gh-content</code> (Ghost post content) or "
     "<code>.ns-prose</code>. No classes on any tag below.",
     row(spec("h1 – h6, p, a, code, kbd, mark, abbr, small", PROSE, wide=True)),
     note("Global rules stay minimal — family and weight only — so template utilities keep "
          "control of size. Full sizing applies only inside a reading context."))

page("Elements", "el-lists", "Lists",
     "Bullets take the brand tint; ordered markers run through the mono label scale, so a "
     "numbered list reads like the numbered rows elsewhere in the system.",
     row(spec("ul / ol", '''<div class="ns-prose" style="max-width:22rem">
<ul><li>Picklist — when the set is closed</li><li>Lookup — a soft relationship</li>
<li>Master-detail — ownership and roll-ups</li></ul>
<ol><li>Create the object</li><li>Add the fields</li><li>Build the layout</li></ol></div>''', wide=True),
         spec("dl", '''<div class="ns-prose" style="max-width:22rem">
<dl><dt>Governor limit</dt><dd>A per-transaction ceiling the platform enforces.</dd>
<dt>Bulkification</dt><dd>Writing code that works on sets, not single records.</dd></dl></div>''', wide=True)))

page("Elements", "el-tables", "Tables",
     "A table is a spec sheet: hairline rows, mono uppercase column headers, tabular "
     "numerals, and a faint brand tint on row hover so the eye can track across.",
     row(spec("table", '''<div class="ns-prose" style="max-width:34rem"><table>
<caption>Automation tools</caption>
<thead><tr><th>Tool</th><th>Use when</th><th>Cost</th></tr></thead>
<tbody>
<tr><td>Flow</td><td>Declarative logic, most of the time</td><td>Low</td></tr>
<tr><td>Apex</td><td>Bulk, callouts, real tests</td><td>High</td></tr>
<tr><td>Nothing</td><td>The requirement is a report</td><td>None</td></tr>
</tbody></table></div>''', wide=True)),
     note("No zebra striping — the hairline already separates the rows."))

page("Elements", "el-quotes", "Quotes",
     "A quote is marked by a hairline rail in brand, not by giant quotation marks or "
     "italics. The attribution is a mono label, like every other piece of metadata.",
     row(spec("blockquote + cite", '''<div class="ns-prose" style="max-width:34rem">
<blockquote>A learning site doesn't need to look like the product it's teaching.
<cite>Namaste Salesforce</cite></blockquote></div>''', wide=True)),
     note("Distinct from the <a href=\"quote.html\">Quote component</a>, which is a testimonial CARD you place in a grid."))

page("Elements", "el-code", "Code",
     "Inline code is a hairline-ringed chip on the sunken surface; a bare <code>&lt;pre&gt;</code> "
     "is a quiet navy console. The full window is the "
     "<a href=\"code-window.html\">code window component</a>.",
     row(spec("inline code / kbd / samp", '''<div class="ns-prose" style="max-width:34rem">
<p>Run <code>sfdx force:org:create</code>, then press <kbd>Enter</kbd>. Output: <samp>Successfully created org</samp>.</p></div>''', wide=True)),
     row(spec("pre", '''<div class="ns-prose" style="max-width:34rem"><pre><code>for (Account a : accounts) {
    a.Rating = 'Warm';
}
update accounts;</code></pre></div>''', wide=True)))

page("Elements", "el-forms", "Form elements",
     "Bare controls only — every rule guards with <code>:not([class])</code>, because templates "
     "style their inputs with utilities or the <a href=\"input.html\">input component</a>. "
     "What IS global: the accent colour, so native controls speak the one signal blue.",
     row(spec("input / textarea / select", '''<div style="display:grid;gap:.6rem;max-width:17rem">
<input placeholder="Bare input, no class">
<select><option>Bare select</option></select>
<textarea placeholder="Bare textarea"></textarea></div>''', wide=True),
         spec("checkbox / radio / range", '''<div style="display:grid;gap:.6rem;max-width:15rem">
<label><input type="checkbox" checked> Beginner</label>
<label><input type="radio" name="d" checked> Free</label>
<input type="range" value="60"></div>''', wide=True)),
     row(spec("fieldset / legend", '''<fieldset style="max-width:17rem"><legend>Filters</legend>
<label><input type="checkbox"> Video lessons only</label></fieldset>''', wide=True)))

page("Elements", "el-media", "Media",
     "Media carries the card radius so it sits in the same geometry as everything else, "
     "and captions are mono labels. Nothing here adds a shadow — media is framed by the hairline.",
     row(spec("figure / figcaption", '''<div class="ns-prose" style="max-width:22rem"><figure>
<div style="aspect-ratio:16/9;background:var(--color-surface-sunken);border-radius:var(--radius-card);
display:flex;align-items:center;justify-content:center;color:var(--color-muted)">
<i class="ph ph-image" style="font-size:2rem"></i></div>
<figcaption>The schema builder, mid-refactor</figcaption></figure></div>''', wide=True)))

page("Elements", "el-interactive", "Interactive elements",
     "The native disclosure and feedback elements, dressed in system geometry — so a docs "
     "FAQ or a Ghost toggle card needs no extra markup. Open state is signed by the border "
     "going brand, the same signal a hovered card gives.",
     row(spec("details / summary", '''<div class="ns-prose" style="max-width:30rem">
<details open><summary>Why not always Apex?</summary>
<p>Because every line of code is a line somebody has to maintain.</p></details>
<details><summary>Can I use Flow for everything?</summary>
<p>Almost. Bulk operations and callouts still want code.</p></details></div>''', wide=True)),
     row(spec("progress", '<progress value="70" max="100" style="max-width:20rem"></progress>', wide=True)))

# ═════════════════════════════════════════════════════════════════════════════
# COMPONENTS
# ═════════════════════════════════════════════════════════════════════════════
page("Components", "button", "Button",
     "One solid button per screen, so the one solid thing reads as the one thing to click. "
     "Press is an instant opacity dim — never a lift, never a shadow bloom.",
     head("Tone"),
     row(*[spec(f"--{v}", f'<button class="ns-btn ns-btn--{v}">Enrol now</button>')
           for v in ("primary", "accent", "outline", "ghost")]),
     row(spec("--success", '<button class="ns-btn ns-btn--success">Complete</button>'),
         spec("--warning", '<button class="ns-btn ns-btn--warning">Review</button>'),
         spec("--danger", '<button class="ns-btn ns-btn--danger">Delete</button>')),
     note("<code>--white</code> and <code>--glass</code> are for dark grounds — see "
          "<a href=\"page-header.html\">Page header</a>."),
     head("Size"),
     row(*[spec(f"--{s}" if s else "(default)",
                f'<button class="ns-btn ns-btn--primary{" ns-btn--" + s if s else ""}">Size {s or "md"}</button>')
           for s in ("xs", "sm", "", "lg", "xl")]),
     head("Shape"),
     row(spec("--pill", '<button class="ns-btn ns-btn--outline ns-btn--pill">Pill</button>'),
         spec("--sharp", '<button class="ns-btn ns-btn--outline ns-btn--sharp">Sharp</button>'),
         spec("--square", '<button class="ns-btn ns-btn--outline ns-btn--square"><i class="ph ph-arrow-right"></i></button>'),
         spec("--block", '<button class="ns-btn ns-btn--outline ns-btn--block" style="width:12rem">Full width</button>')),
     head("State"),
     row(spec(":disabled", '<button class="ns-btn ns-btn--primary" disabled>Disabled</button>'),
         spec(".is-loading", '<button class="ns-btn ns-btn--primary is-loading">Saving</button>')),
     head("Group"),
     row(spec(".ns-btn-group",
              '<div class="ns-btn-group"><button class="ns-btn ns-btn--outline ns-btn--sm">Day</button>'
              '<button class="ns-btn ns-btn--outline ns-btn--sm">Week</button>'
              '<button class="ns-btn ns-btn--outline ns-btn--sm">Month</button></div>')))

page("Components", "badge", "Badge",
     "Status as DATA: mono, uppercase, hairline-ringed. Never a filled pastel wash — the "
     "ring carries the colour so the text stays legible on any surface.",
     head("Tone"),
     row(*[spec(f"--{v}" if v else "(brand)",
                f'<span class="ns-badge{" ns-badge--" + v if v else ""}">{v or "brand"}</span>')
           for v in ("", "accent", "success", "warning", "danger", "neutral")]),
     head("Form"),
     row(spec("--dot", '<span class="ns-badge ns-badge--dot ns-badge--success">Live</span>'),
         spec("--solid", '<span class="ns-badge ns-badge--solid">Featured</span>'),
         spec("--glass", '<span class="ns-badge ns-badge--glass" style="background:var(--color-brand-900);padding:.35rem .6rem">On media</span>')),
     head("Size + shape"),
     row(spec("--sm", '<span class="ns-badge ns-badge--sm">sm</span>'),
         spec("(default)", '<span class="ns-badge">md</span>'),
         spec("--lg", '<span class="ns-badge ns-badge--lg">lg</span>'),
         spec("--pill", '<span class="ns-badge ns-badge--pill">Preview</span>')),
     note("The dot form is the house pattern for status: a coloured dot plus mono text."))

page("Components", "chip", "Chip",
     "The icon tile that fronts a feature card or a list row. The one place a faint brand "
     "wash is allowed, because it reads as a surface rather than a status.",
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
     "A tag IS a true pill — the one legitimate pill shape in a system that is otherwise "
     "sharp. Hairline by default; the border goes brand on hover.",
     row(spec(".ns-tagchip", '<a class="ns-tagchip" href="#!">apex <b>12</b></a>'),
         spec("--sm", '<a class="ns-tagchip ns-tagchip--sm" href="#!">flow <b>7</b></a>'),
         spec("--lg", '<a class="ns-tagchip ns-tagchip--lg" href="#!">lwc <b>21</b></a>'),
         spec(".is-active", '<a class="ns-tagchip is-active" href="#!">integration <b>4</b></a>')),
     note("The <code>&lt;b&gt;</code> inside carries the post count in mono, tabular figures."))

page("Components", "kicker", "Kicker",
     "The section eyebrow written as a code comment: <code>// GETTING STARTED</code>. This is "
     "what replaces the pastel eyebrow pill — it says &ldquo;developer&rdquo; without a single decoration.",
     head("Tone"),
     row(spec("(default)", '<span class="ns-kicker">Getting started</span>'),
         spec("--brand", '<span class="ns-kicker ns-kicker--brand">New</span>'),
         spec("--muted", '<span class="ns-kicker ns-kicker--muted">Archive</span>')),
     row(spec("--light", '<span style="background:var(--color-brand-900);padding:.6rem .9rem;border-radius:var(--radius-card);display:inline-block"><span class="ns-kicker ns-kicker--light">On navy</span></span>', wide=True)),
     head("Form"),
     row(spec("--plain", '<span class="ns-kicker ns-kicker--plain">No slashes</span>'),
         spec("--dot", '<span class="ns-kicker ns-kicker--dot">Live now</span>'),
         spec("--sm", '<span class="ns-kicker ns-kicker--sm">small</span>'),
         spec("--lg", '<span class="ns-kicker ns-kicker--lg">large</span>')),
     row(spec("--rule", '<span class="ns-kicker ns-kicker--rule" style="width:min(28rem,100%)">Curriculum</span>', wide=True)))

page("Components", "avatar", "Avatar",
     "A person is round; everything else in the system is sharp. The ring is a solid brand "
     "border — not a gradient halo — and marks an author or instructor, so use it sparingly.",
     head("Size"),
     row(*[spec(f"--{s}" if s else "(default)",
                f'<span class="ns-avatar{" ns-avatar--" + s if s else ""}" style="display:inline-flex;'
                f'align-items:center;justify-content:center"><i class="ph-fill ph-user" style="color:var(--color-muted)"></i></span>')
           for s in ("xs", "sm", "", "lg", "xl")]),
     head("Variants"),
     row(spec(".ns-ring", '<span class="ns-ring"><span class="ns-avatar ns-avatar--lg" style="display:inline-flex;align-items:center;justify-content:center"><i class="ph-fill ph-user" style="color:var(--color-muted)"></i></span></span>'),
         spec("--square", '<span class="ns-avatar ns-avatar--square ns-avatar--lg" style="display:inline-flex;align-items:center;justify-content:center"><i class="ph-fill ph-buildings" style="color:var(--color-muted)"></i></span>'),
         spec(".ns-avatar-stack", '<span class="ns-avatar-stack">'
              + '<span class="ns-avatar ns-avatar--sm" style="background:var(--color-brand-100)"></span>' * 3 + '</span>')))

CARD_BODY = ('<div class="ns-card__header"><h3 class="ns-card__title">Apex Programming</h3>'
             '<span class="ns-badge">Paid</span></div>'
             '<p class="ns-card__body" style="margin-top:.5rem;color:var(--color-muted);font-size:var(--size-small)">'
             'Bulk-safe patterns, governor limits, and tests that mean something.</p>'
             '<div class="ns-card__meta" style="margin-top:.85rem">12 lessons · 6h</div>')

page("Components", "card", "Card",
     "The system's box: a hairline border on a raised surface. The border IS the structure, "
     "so there is no default shadow and no hover lift. Every other box in the system is a "
     "preset of this one.",
     head("Base + interactive"),
     row(spec(".ns-card", f'<div class="ns-card" style="width:19rem">{CARD_BODY}</div>', wide=True),
         spec("--interactive", f'<div class="ns-card ns-card--interactive" style="width:19rem">{CARD_BODY}</div>', wide=True)),
     note("Hover the second one: the border goes brand and an accent line draws across the top. "
          "Add <code>--row</code> and the accent moves to the left edge instead."),
     head("Surface"),
     row(spec("--sunken", f'<div class="ns-card ns-card--sunken" style="width:15rem">{CARD_BODY}</div>', wide=True),
         spec("--dark", f'<div class="ns-card ns-card--dark" style="width:15rem">{CARD_BODY}</div>', wide=True),
         spec("--dashed", f'<div class="ns-card ns-card--dashed" style="width:15rem">{CARD_BODY}</div>', wide=True)),
     head("Pattern"),
     row(spec("--grid", f'<div class="ns-card ns-card--grid" style="width:15rem">{CARD_BODY}</div>', wide=True),
         spec("--dots", f'<div class="ns-card ns-card--dots" style="width:15rem">{CARD_BODY}</div>', wide=True),
         spec("--lines", f'<div class="ns-card ns-card--lines" style="width:15rem">{CARD_BODY}</div>', wide=True)),
     head("Edge"),
     row(spec("--rail", f'<div class="ns-card ns-card--rail" style="width:15rem">{CARD_BODY}</div>', wide=True),
         spec("--strong", f'<div class="ns-card ns-card--strong" style="width:15rem">{CARD_BODY}</div>', wide=True)),
     head("Size"),
     row(spec("--xs / --sm / --lg / --xl",
              "".join(f'<div class="ns-card ns-card--{s}" style="width:8rem"><span class="ns-card__meta">{s}</span></div>'
                      for s in ("xs", "sm", "lg", "xl")), wide=True)),
     note("Variants compose: a large interactive card on the grid pattern is "
          "<code>.ns-card .ns-card--lg .ns-card--interactive .ns-card--grid</code> — no new class."))

page("Components", "feature", "Feature",
     "Icon, title, one paragraph. A card preset for the &ldquo;what you get&rdquo; grids, with the "
     "chip and copy rhythm already set.",
     row(spec(".ns-feature",
              '<div class="ns-feature" style="width:17rem"><span class="ns-chip"><i class="ph-fill ph-graduation-cap"></i></span>'
              '<h3 class="ns-feature__title">Project-led</h3>'
              '<p class="ns-feature__body">Every lesson ends with something you built, not something you watched.</p>'
              '<a class="ns-feature__link" href="#!">Start learning <i class="ph ph-arrow-right"></i></a></div>', wide=True),
         spec("--row",
              '<div class="ns-feature ns-feature--row" style="width:19rem"><span class="ns-chip ns-chip--sm"><i class="ph-fill ph-users-three"></i></span>'
              '<div><h3 class="ns-feature__title">Community reviewed</h3>'
              '<p class="ns-feature__body">Drafts get a technical review before they go live.</p></div></div>', wide=True)))

page("Components", "quote", "Quote",
     "A learner testimonial: stars, the quote, then who said it. Distinct from the "
     "<a href=\"el-quotes.html\">blockquote element</a>, which styles quotes inside article content.",
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
              '<div><p class="ns-quote__name">Marcus T.</p><p class="ns-quote__role">Developer</p></div></figcaption></figure>', wide=True)))

page("Components", "widget", "Widget",
     "The boxes that stack in a sidebar — a card with a mono heading and a hairline under "
     "it, so a column of them reads as one rail.",
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
              '<a class="ns-tagchip ns-tagchip--sm" href="#!">lwc</a></div></div>', wide=True)))

page("Components", "note", "Note",
     "The inline callout. Badges may never carry a status wash, but a note is a BLOCK the "
     "reader is meant to stop at — so it gets one tint, held at 4–6%, with the colour "
     "carried by the border and the icon.",
     *[row(spec(f"--{v}" if v else "(brand)",
                f'<div class="ns-note{" ns-note--" + v if v else ""}" style="width:min(34rem,100%)">'
                f'<i class="ns-note__icon ph-fill ph-{icon}"></i>'
                f'<div class="ns-note__body"><span class="ns-note__title">{title}</span> — {body}</div></div>', wide=True))
       for v, icon, title, body in (
           ("", "info", "Heads up", "this course assumes you've finished Admin Foundations."),
           ("success", "check-circle", "Section complete", "nice work — the next one unlocks automatically."),
           ("warning", "lock", "Members only", "sign in to read the rest of this lesson."),
           ("danger", "warning-circle", "Deprecated", "this API version retires in Summer '26."),
           ("neutral", "note", "Note", "you can change this later in Setup."))],
     head("Size"),
     row(spec("--sm", '<div class="ns-note ns-note--sm" style="width:min(24rem,100%)"><i class="ns-note__icon ph-fill ph-info"></i><div class="ns-note__body">Compact.</div></div>', wide=True)))

page("Components", "empty-state", "Empty state",
     "&ldquo;No lessons yet&rdquo;, &ldquo;nothing matched your search&rdquo;. A dashed hairline says "
     "<em>this will fill in</em>, where a solid one would say <em>this is broken</em>.",
     row(spec(".ns-empty",
              '<div class="ns-empty" style="width:min(34rem,100%)"><i class="ns-empty__icon ph ph-folder-open"></i>'
              '<p class="ns-empty__title">No lessons yet</p>'
              '<p class="ns-empty__body">Lessons for this section are being written.</p>'
              '<a class="ns-btn ns-btn--outline ns-btn--sm ns-empty__action" href="#!">Browse courses</a></div>', wide=True)),
     row(spec("--sm", '<div class="ns-empty ns-empty--sm" style="width:min(20rem,100%)">No results.</div>', wide=True),
         spec("--solid", '<div class="ns-empty ns-empty--solid ns-empty--sm" style="width:min(20rem,100%)">Nothing here.</div>', wide=True)))

page("Components", "stat", "Stat",
     "A number and what it counts. The value is ALWAYS mono and tabular so a row of them "
     "lines up — this readout is what makes the site feel like a console rather than a brochure.",
     row(spec(".ns-stats",
              '<div class="ns-stats">'
              + "".join(f'<div class="ns-stat"><span class="ns-stat__value">{v}</span><span class="ns-stat__label">{l}</span></div>'
                        for v, l in (("24", "courses"), ("312", "lessons"), ("9", "roadmaps"), ("100%", "free"))) +
              '</div>', wide=True)),
     head("Size + tone"),
     row(spec("--lg --brand",
              '<div class="ns-stat ns-stat--lg ns-stat--brand"><span class="ns-stat__value">312</span>'
              '<span class="ns-stat__label">lessons</span></div>', wide=True),
         spec("--inline",
              '<div class="ns-stat ns-stat--inline"><i class="ns-stat__icon ph-fill ph-clock"></i>'
              '<b class="ns-stat__value" style="font-size:1.15rem">6h</b><span class="ns-stat__label">total</span></div>', wide=True)),
     note("<code>--light</code> is for dark grounds — that's the course hero readout."))

page("Components", "progress", "Progress",
     "Course and track completion. A flat brand fill on the sunken track — no stripes, no "
     "gradient. Pair it with a mono readout, because the number is the information and the "
     "bar is just its shape.",
     row(spec(".ns-progress",
              '<div style="width:min(24rem,100%)"><div class="ns-progress"><span class="ns-progress__bar" style="width:70%"></span></div>'
              '<div class="ns-progress__label" style="margin-top:.4rem">7 / 10 · 70%</div></div>', wide=True)),
     head("Size"),
     row(*[spec(f"--{s}" if s else "(default)",
                f'<div style="width:9rem"><div class="ns-progress{" ns-progress--" + s if s else ""}">'
                f'<span class="ns-progress__bar" style="width:60%"></span></div></div>', wide=True)
           for s in ("xs", "sm", "", "lg")]),
     head("Tone"),
     row(spec("--success", '<div style="width:9rem"><div class="ns-progress ns-progress--success"><span class="ns-progress__bar" style="width:100%"></span></div></div>', wide=True),
         spec("--warning", '<div style="width:9rem"><div class="ns-progress ns-progress--warning"><span class="ns-progress__bar" style="width:35%"></span></div></div>', wide=True)))

page("Components", "input", "Input",
     "Sharp geometry, hairline border, a quiet brand focus ring. Works on "
     "<code>input</code>, <code>textarea</code> and <code>select</code> alike.",
     head("Size"),
     row(spec("--sm", '<input class="ns-input ns-input--sm" placeholder="small" style="width:11rem">', wide=True),
         spec("(default)", '<input class="ns-input" placeholder="you@email.com" style="width:15rem">', wide=True),
         spec("--lg", '<input class="ns-input ns-input--lg" placeholder="large" style="width:15rem">', wide=True)),
     head("State"),
     row(spec("--error", '<input class="ns-input ns-input--error" value="not-an-email" style="width:15rem">', wide=True),
         spec("--success", '<input class="ns-input ns-input--success" value="you@email.com" style="width:15rem">', wide=True),
         spec(":disabled", '<input class="ns-input" value="Locked" disabled style="width:15rem">', wide=True)),
     head("Field + affixes"),
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
              '<label class="ns-check"><input type="checkbox"> Advanced</label>', wide=True)))

page("Components", "code-window", "Code window",
     "The Salesforce Developer Console rebuilt in CSS: a navy bar with a white file tab and "
     "a copy button, a white editor surface with the code fully flush, and an all-blue token "
     "palette. No highlighting library — <code>code.js</code> adds the <code>.tok-*</code> spans.",
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
     note("Variants: <code>--plain</code> drops the bar, <code>--dark</code> uses the navy editor surface."))

page("Components", "video-poster", "Video poster",
     "A click-to-play cover. Media is the ONE exception to the no-transform rule — a poster "
     "that doesn't respond feels broken — and the motion is on the image, not on the box.",
     row(spec(".ns-video-poster",
              '<a class="ns-video-poster" href="#!" style="width:20rem;display:block">'
              '<span class="ns-video-poster__fallback"></span>'
              '<span class="ns-video-poster__play"><i class="ph-fill ph-play"></i></span></a>', wide=True)),
     note("<code>--lesson</code> switches the box from 4:3 to 16:9."))

page("Components", "steps", "Steps",
     "A numbered procedure: a hairline rail behind solid brand discs. The disc carries a "
     "surface-coloured ring, so the rail appears to pass behind it.",
     row(spec(".ns-steps",
              '<div class="ns-steps" style="width:min(26rem,100%);display:grid;gap:1rem">'
              + "".join(f'<div style="display:flex;gap:1rem;align-items:center"><span class="ns-step-num">{n}</span>'
                        f'<div><div style="font-weight:600">{t}</div>'
                        f'<div class="ns-card__meta">{m}</div></div></div>'
                        for n, t, m in ((1, "Create a free org", "5 min"), (2, "Build your first object", "20 min"),
                                        (3, "Automate it", "35 min"))) +
              '</div>', wide=True)),
     note("<code>--quiet</code> gives hairline discs with ink numerals, for long lists; "
          "<code>.is-done</code> fills one in."))

page("Components", "timeline", "Timeline",
     "A vertical hairline rail behind milestone dots. Same idea as Steps, without the "
     "numbered discs — a timeline marks moments, a stepper marks actions.",
     row(spec(".ns-timeline",
              '<div class="ns-timeline" style="width:min(22rem,100%);display:grid;gap:1.1rem">'
              + "".join(f'<div style="display:flex;gap:1rem;align-items:center"><span class="ns-timeline__dot{on}"></span>'
                        f'<div><div style="font-weight:600;font-size:var(--size-small)">{t}</div>'
                        f'<div class="ns-card__meta">{d}</div></div></div>'
                        for t, d, on in (("Site launched", "Jan 2026", " is-on"), ("First course", "Mar 2026", " is-on"),
                                         ("Certificates", "Soon", ""))) +
              '</div>', wide=True)))

page("Components", "layout", "Layout",
     "The two measurements every page agrees on: how wide the content column is, and how "
     "much air sits between bands.",
     row(spec(".ns-container--prose", '<div class="ns-container ns-container--prose" style="background:var(--color-surface-sunken);border-radius:var(--radius-card);padding-block:1rem"><span class="ns-label">45rem — the reading column</span></div>', wide=True)),
     row(spec(".ns-container--narrow", '<div class="ns-container ns-container--narrow" style="background:var(--color-surface-sunken);border-radius:var(--radius-card);padding-block:1rem"><span class="ns-label">34rem — centred CTAs</span></div>', wide=True)),
     row(spec(".ns-container", '<div class="ns-container" style="background:var(--color-surface-sunken);border-radius:var(--radius-card);padding-block:1rem"><span class="ns-label">80rem — the page shell</span></div>', wide=True)),
     note("<code>.ns-section</code> supplies the vertical rhythm: <code>--sm</code>, <code>--lg</code>, "
          "<code>--flush</code>, plus <code>--sunken</code> / <code>--dark</code> grounds."))

page("Components", "page-header", "Page header",
     "The band at the top of a collection or landing page. Solid navy ground — never a "
     "gradient — with the pattern layer behind it.",
     row(spec(".ns-page-header",
              '<div class="ns-page-header" style="border-radius:var(--radius-card)">'
              '<div class="ns-page-header__inner" style="padding-block:2.5rem">'
              '<p class="ns-kicker ns-kicker--light ns-kicker--center"><i class="ph-fill ph-graduation-cap"></i>Courses</p>'
              '<h1 class="ns-page-header__title" style="font-size:2rem">Learn Salesforce properly</h1>'
              '<p class="ns-page-header__sub">Project-led courses, free forever.</p>'
              '<div class="ns-page-header__actions"><a class="ns-btn ns-btn--white" href="#!">Browse courses</a>'
              '<a class="ns-btn ns-btn--glass" href="#!">See the roadmap</a></div></div></div>', wide=True)),
     note("Tones: <code>--plain</code> and <code>--sunken</code> for light grounds; "
          "<code>--left</code> to un-centre; <code>--sm</code> / <code>--lg</code> for height."))

page("Components", "section-head", "Section head",
     "The kicker + title + &ldquo;see all&rdquo; row that opens every band. One component, so the "
     "spacing above a section is identical everywhere — inconsistent section rhythm is the "
     "fastest way for a page to feel assembled rather than designed.",
     row(spec(".ns-section-head",
              '<div style="width:min(38rem,100%)"><div class="ns-section-head">'
              '<div><span class="ns-kicker">Catalog</span><h2 class="ns-section-head__title">Latest courses</h2>'
              '<p class="ns-section-head__sub">Everything published so far, newest first.</p></div>'
              '<a class="ns-btn ns-btn--outline ns-btn--sm ns-section-head__action" href="#!">See all</a></div></div>', wide=True)),
     row(spec("--center",
              '<div style="width:min(38rem,100%)"><div class="ns-section-head ns-section-head--center">'
              '<div><span class="ns-kicker ns-kicker--center">How it works</span>'
              '<h2 class="ns-section-head__title">Three steps to your first app</h2></div></div></div>', wide=True)))

page("Components", "breadcrumb", "Breadcrumb",
     "Home / section / current page. One line that NEVER wraps — the current title truncates "
     "instead, because a breadcrumb that reflows pushes the article down on every narrow screen.",
     row(spec(".ns-crumbs",
              '<nav class="ns-crumbs"><a class="ns-crumbs__link" href="#!"><i class="ph ph-house"></i>Home</a>'
              '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
              '<a class="ns-crumbs__link" href="#!"><i class="ph ph-tag"></i>Apex</a>'
              '<i class="ns-crumbs__sep ph ph-caret-right"></i>'
              '<span class="ns-crumbs__current"><i class="ph ph-file-text"></i><span>Governor limits and bulk patterns</span></span></nav>', wide=True)))

page("Components", "pagination", "Pagination",
     "Newer / Older plus a mono page count. Pills are legitimate here — a pager control is a "
     "discrete token, the same family as a tag.",
     row(spec(".ns-pager",
              '<nav class="ns-pager"><a class="ns-pager__link" href="#!"><i class="ph ph-arrow-left"></i>Newer</a>'
              '<span class="ns-pager__count">Page 2 of 7</span>'
              '<a class="ns-pager__link" href="#!">Older<i class="ph ph-arrow-right"></i></a></nav>', wide=True)))

page("Components", "nav-link", "Nav link",
     "A navigation row: header bar, mobile menu, sidebars. The faint brand tint on hover is "
     "legitimate here because a nav row is a surface you point at, not a status you read.",
     row(spec(".nav-link / .is-current",
              '<div style="display:flex;gap:.25rem"><a class="nav-link is-current" href="#!"><i class="ph ph-house"></i>Home</a>'
              '<a class="nav-link" href="#!"><i class="ph ph-graduation-cap"></i>Courses</a>'
              '<a class="nav-link" href="#!"><i class="ph ph-flow-arrow"></i>Training</a></div>', wide=True)),
     row(spec("--block + __meta",
              '<div style="width:15rem"><a class="nav-link nav-link--block" href="#!"><i class="ph ph-books"></i>Docs'
              '<span class="nav-link__meta">22</span></a></div>', wide=True)))

page("Components", "icon-button", "Icon button",
     "The round, borderless action in the navbar and toolbars. Pairs with "
     "<a href=\"tooltip.html\">the tooltip</a> for its label.",
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
                             '<button class="icon-btn icon-btn--lg"><i class="ph ph-star"></i></button>')))

page("Components", "menu", "Menu",
     "The dropdown panel: the account menu, the share menu, any Alpine popover. A floating "
     "layer genuinely sits above the page, so this is one of the few places allowed to carry "
     "<code>--shadow-raised</code>.",
     row(spec(".ns-menu",
              '<div class="ns-menu" style="position:static;width:15rem">'
              '<div class="ns-menu__head"><div style="font-weight:700;font-size:var(--size-small)">Swarnil Singhai</div>'
              '<div style="font-size:.75rem;color:var(--color-muted)">member since 2026</div></div>'
              '<div class="ns-menu__group"><a class="ns-menu__item" href="#!"><i class="ph ph-user"></i>Account</a>'
              '<a class="ns-menu__item ns-menu__item--brand" href="#!"><i class="ph ph-user-circle"></i>Become an author</a></div>'
              '<div class="ns-menu__sep"></div>'
              '<a class="ns-menu__item ns-menu__item--quiet" href="#!"><i class="ph ph-x"></i>Sign out</a>'
              '</div>', wide=True)),
     note("Placement: <code>--end</code> aligns right, <code>--up</code> opens upwards. "
          "Widths: <code>--sm</code>, <code>--lg</code>, <code>--wide</code>."))

page("Components", "tooltip", "Tooltip",
     "The label that appears under an icon button on hover. Inverted and mono, so it reads "
     "as a system hint rather than content. Needs a positioned <code>.group</code> parent.",
     row(spec(".nav-tip (hover me)",
              '<span class="group" style="position:relative;display:inline-flex"><button class="icon-btn"><i class="ph ph-info"></i></button>'
              '<span class="nav-tip">Help</span></span>', wide=True)),
     note("Placements: <code>--top</code>, <code>--left</code>, <code>--right</code>. "
          "Keyboard focus reveals it too."))

page("Components", "toc", "Table of contents",
     "Built by <code>toc.js</code> from the headings in the article. The active heading is "
     "marked by the LEFT RAIL going brand — a rail, not a highlight, because the TOC is a map "
     "of the page's structure.",
     row(spec(".toc-link",
              '<nav style="width:15rem"><a class="toc-link is-active" href="#!">Getting started</a>'
              '<a class="toc-link" href="#!">The data model</a>'
              '<a class="toc-link is-h3" href="#!">Objects</a>'
              '<a class="toc-link is-h3" href="#!">Relationships</a>'
              '<a class="toc-link is-h4" href="#!">Lookup vs master-detail</a></nav>', wide=True)))

page("Components", "sidebar", "Docs sidebar",
     "Three different &ldquo;active&rdquo; treatments, because they answer three different questions: "
     "which page am I ON, which section am I IN, which heading am I NEAR.",
     row(spec(".doc-nav-link.is-doc-active",
              '<nav style="width:16rem"><span class="doc-nav-heading">Getting started</span>'
              '<a class="doc-nav-link nav-link nav-link--block nav-link--sm is-doc-active" href="#!">Create your account</a>'
              '<a class="doc-nav-link nav-link nav-link--block nav-link--sm" href="#!">Find your way around</a></nav>', wide=True)),
     note("The active row uses <code>!important</code> on purpose: the markup's "
          "<code>text-muted</code> / <code>hover:*</code> utilities sit in a later cascade layer "
          "and would otherwise wash it out."))

page("Components", "subnav", "Mobile sub-navbar",
     "The &ldquo;tap to open the lesson list&rdquo; pattern used by course, lesson, training and docs "
     "pages: a sticky bar under the header on small screens that becomes a plain static "
     "sidebar from <code>lg</code> up — same markup, two completely different shapes.",
     row(spec(".subnav-bar",
              '<div style="width:min(24rem,100%)"><div class="subnav-bar" style="position:static;display:flex">'
              '<span>Course lessons</span><i class="ph ph-caret-down"></i></div>'
              '<div class="subnav-panel" style="max-height:none">'
              '<a class="nav-link nav-link--block nav-link--sm" href="#!">1 · What Salesforce actually is</a>'
              '<a class="nav-link nav-link--block nav-link--sm" href="#!">2 · Objects and fields</a></div></div>', wide=True)),
     note("Shown here forced open; on a real page it is <code>lg:hidden</code> and Alpine toggles the panel."))

page("Components", "share", "Share menu",
     "A reveal menu anchored above its trigger. Rows are plain until hovered, where they "
     "take the same faint brand tint as every other menu row.",
     row(spec(".ns-share",
              '<div class="ns-share"><button class="ns-btn ns-btn--outline ns-btn--sm">'
              '<i class="ph ph-share-network"></i>Share</button>'
              '<div class="ns-share__menu" style="position:static;margin-top:.5rem">'
              '<a href="#!"><i class="ph ph-twitter-logo"></i>Twitter</a>'
              '<a href="#!"><i class="ph ph-linkedin-logo"></i>LinkedIn</a>'
              '<button type="button"><i class="ph ph-link-simple"></i>Copy link</button></div></div>', wide=True)))

page("Components", "ad", "Ad slot",
     "The placeholder is deliberately a WHITE creative surface whatever the site theme is "
     "doing: real ad units render on white, so a themed slot would lie about what the page "
     "will look like once a campaign is live.",
     row(spec(".ns-ad",
              '<div class="ns-ad" style="width:min(34rem,100%)"><div class="ns-ad__ph" style="height:6rem">'
              '<i class="ns-ad__arrow ph ph-arrow-right"></i>'
              '<span class="ns-ad__label">Your ad here — 728×90</span></div></div>', wide=True)))

page("Components", "marquee", "Marquee",
     "The infinite logo strip. The track is DUPLICATED in markup and the keyframe travels "
     "-50%, which is what makes the loop seamless. Edges fade via a mask so items enter and "
     "leave instead of popping.",
     row(spec(".marquee",
              '<div class="marquee" style="width:min(34rem,100%);overflow:hidden">'
              '<div class="marquee-track" style="display:flex;gap:1rem;width:max-content;animation:marquee 24s linear infinite">'
              + ("".join(f'<span class="ns-tagchip">{t}</span>' for t in ("Apex", "LWC", "Flow", "Data Cloud", "Agentforce")) * 2)
              + '</div></div>', wide=True)),
     note("Hover pauses it; <code>prefers-reduced-motion</code> stops it entirely."))

page("Components", "effects", "Effects",
     "Optional polish. If the JS never runs the page must still read correctly, which is why "
     "each effect's resting state is the visible one wherever possible — and why every one is "
     "fully disabled under <code>prefers-reduced-motion</code>.",
     row(spec(".js-spotlight (hover)",
              '<div class="ns-card ns-card--interactive js-spotlight" style="width:17rem">'
              '<div class="ns-card__title">Pointer spotlight</div>'
              '<div class="ns-card__meta" style="margin-top:.35rem">a faint brand tint follows the cursor</div></div>', wide=True),
         spec(".ns-underline (hover)",
              '<a class="ns-underline" href="#!" style="font-weight:600">An underline that wipes in</a>', wide=True)),
     note("Also here: <code>.js-reveal</code> (scroll reveal), <code>.js-manifesto</code>, "
          "the <code>.js-tl-*</code> roadmap draw, <code>.ns-aurora</code> and the "
          "<code>.ns-ba-*</code> illustration loops."))

# ═════════════════════════════════════════════════════════════════════════════
# MODULES
# ═════════════════════════════════════════════════════════════════════════════
page("Modules", "modules", "Modules",
     "Layer 3 — styling that only makes sense on one part of the site. Nothing in layers 0–2 "
     "may depend on any of it. When a piece here proves reusable it gets promoted into the "
     "component library with a proper variant set; that's how "
     "<a href=\"video-poster.html\">video poster</a>, <a href=\"ad.html\">ad</a> and "
     "<a href=\"share.html\">share</a> arrived there.",
     head("Course tags"),
     row(spec(".ns-level", '<span class="ns-level ns-level--beginner">Beginner</span>'
                           '<span class="ns-level ns-level--intermediate">Intermediate</span>'
                           '<span class="ns-level ns-level--advanced">Advanced</span>'),
         spec(".ns-price-tag", '<span class="ns-price-tag ns-price-tag--free">Free</span>'
                               '<span class="ns-price-tag ns-price-tag--paid">Paid</span>'),
         spec(".ns-badge-featured", '<span class="ns-badge-featured"><i class="ph-fill ph-star"></i>Featured</span>')),
     head("Curriculum"),
     row(spec(".ns-curriculum",
              '<div class="ns-curriculum" style="width:min(34rem,100%)">'
              + "".join(f'<a class="ns-curriculum__item" href="#!"><span class="ns-curriculum__num">{n:02d}</span>'
                        f'<i class="ns-curriculum__icon ph-fill ph-{ic}"></i>'
                        f'<span class="ns-curriculum__body"><span class="ns-curriculum__title">{t}</span></span>'
                        f'<span class="ns-curriculum__meta"><span class="ns-curriculum__dur">{d}</span>{badge}</span></a>'
                        for n, ic, t, d, badge in (
                            (1, "play-circle", "What Salesforce actually is", "6m",
                             '<span class="ns-curriculum__badge ns-curriculum__badge--free">Free</span>'),
                            (2, "play-circle", "Objects and fields", "12m",
                             '<span class="ns-curriculum__badge ns-curriculum__badge--preview">Preview</span>'),
                            (3, "article", "Users and permissions", "18m",
                             '<span class="ns-curriculum__badge ns-curriculum__badge--members">Members</span>')))
              + '</div>', wide=True)),
     note("Four styles via <code>data-style</code>: <code>list</code> (default), <code>cards</code>, "
          "<code>detailed</code>, <code>timeline</code>. Badges follow Ghost visibility."),
     head("Lesson"),
     row(spec(".ns-lesson-type", '<span class="ns-lesson-type ns-lesson-type--video"><i class="ph-fill ph-video"></i>Video</span>'
                                 '<span class="ns-lesson-type ns-lesson-type--article"><i class="ph ph-article"></i>Article</span>'),
         spec(".ns-lesson-chip", '<span class="ns-lesson-chip"><i class="ph ph-clock"></i>12 min</span>')),
     note("The rest of layer 3 — the navbar's scroll behaviours, the catalog grid and filters, "
          "the training roadmap and rail — only makes sense at full page width. See it running "
          "on the site itself."))


# ═════════════════════════════════════════════════════════════════════════════
# RENDERING
# ═════════════════════════════════════════════════════════════════════════════
GROUPS = ["Foundation", "Elements", "Components", "Modules"]

RULES = [
    ("Hairlines, not shadows",
     "One 1px border is the structuring device. Elevation means the border brightens to "
     "brand — never a floating lift."),
    ("Monospace is a material",
     "Fira Code renders every index, duration, timestamp, status tag and kicker. Inter is "
     "for prose and headings only."),
    ("One signal colour",
     "Brand blue is the only colour that means &ldquo;interactive&rdquo;. Status is a dot plus mono "
     "text, never a background wash."),
    ("Sharp, specific geometry",
     "Cards 6px, buttons and inputs 4px. Pills are reserved for true pills — tags and pager "
     "controls."),
    ("Motion is instant",
     "120–180ms plain ease-out. No spring, no bounce, no hover lift. The one exception is "
     "the float loop on illustrations."),
]


def render_block(b):
    kind = b[0]
    if kind == "note":
        return f'<p class="sg-note">{b[1]}</p>'
    if kind == "head":
        return f'<h3 class="sg-h3">{b[1]}</h3>'
    if kind == "raw":
        return b[1]
    if kind == "swatches":
        cells = "".join(
            f'<div class="sg-swatch"><span class="sg-swatch__chip" style="background:var({n})"></span>'
            f'<code class="sg-label">{n}</code></div>' for n in b[2])
        return f'<div class="sg-swatches">{cells}</div>'
    if kind == "tokens":
        rows = "".join(
            f'<tr><td><code>{n}</code></td><td class="sg-token-val" data-token="{n}"></td></tr>' for n in b[2])
        return ('<table class="sg-tokens"><thead><tr><th>Token</th><th>Value</th></tr></thead>'
                f'<tbody>{rows}</tbody></table>')
    out = ['<div class="sg-row">']
    for _, label, markup, wide in b[1]:
        cls = "sg-spec sg-spec--wide" if wide else "sg-spec"
        out.append(f'<div class="{cls}"><div class="sg-stage">{markup}</div>'
                   f'<code class="sg-label">{label}</code></div>')
    out.append("</div>")
    return "".join(out)


def sidebar(current):
    parts = ['<a class="sg-side__home' + (" is-current" if current == "index" else "") +
             '" href="index.html"><i class="ph ph-house"></i>Overview</a>']
    for g in GROUPS:
        items = [(s, t) for grp, s, t, _, _ in PAGES if grp == g]
        parts.append(f'<div class="sg-side__group"><span class="sg-side__title">{g}</span>')
        for slug, title in items:
            cur = " is-current" if slug == current else ""
            parts.append(f'<a class="sg-side__link{cur}" href="{slug}.html">{title}</a>')
        parts.append("</div>")
    return "".join(parts)


SHELL = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Developer Console</title>
<!-- The theme's real built CSS. Run `yarn build` to refresh it. -->
<link rel="stylesheet" href="../assets/built/screen.css">
<script>
  try {{ var t = localStorage.getItem('ns-theme');
         if (t) document.documentElement.setAttribute('data-theme', t); }} catch (e) {{}}
</script>
<style>
  /* Style-guide chrome only — none of this ships with the theme. */
  .sg-shell {{ display: grid; grid-template-columns: 16rem minmax(0,1fr); min-height: 100vh; }}
  @media (max-width: 900px) {{ .sg-shell {{ grid-template-columns: 1fr; }} .sg-side {{ position: static !important; height: auto !important; }} }}

  .sg-side {{ position: sticky; top: 0; height: 100vh; overflow-y: auto;
              border-right: 1px solid var(--color-border); background: var(--color-surface-sunken);
              padding: 1.25rem 1rem 3rem; }}
  .sg-side__brand {{ display: flex; align-items: center; gap: .6rem; margin-bottom: 1.25rem; }}
  .sg-side__mark {{ font-family: var(--font-mono); font-size: .72rem; font-weight: 700;
                    letter-spacing: .08em; text-transform: uppercase; }}
  .sg-side__home, .sg-side__link {{ display: flex; align-items: center; gap: .5rem;
        padding: .35rem .6rem; border-radius: var(--radius-btn); font-size: .875rem;
        color: var(--color-muted); }}
  .sg-side__home:hover, .sg-side__link:hover {{ color: var(--color-brand-600);
        background: color-mix(in srgb, var(--color-brand-500) 8%, transparent); }}
  .sg-side__home.is-current, .sg-side__link.is-current {{ color: var(--color-brand-600);
        background: color-mix(in srgb, var(--color-brand-500) 12%, transparent); font-weight: 600; }}
  [data-theme="dark"] .sg-side__home:hover, [data-theme="dark"] .sg-side__link:hover,
  [data-theme="dark"] .sg-side__home.is-current, [data-theme="dark"] .sg-side__link.is-current {{ color: var(--color-brand-300); }}
  .sg-side__group {{ margin-top: 1.25rem; }}
  .sg-side__title {{ display: block; padding: 0 .6rem .4rem; font-family: var(--font-mono);
        font-size: var(--size-label); font-weight: 700; letter-spacing: var(--tracking-label);
        text-transform: uppercase; color: var(--color-label); }}

  .sg-main {{ min-width: 0; }}
  .sg-top {{ position: sticky; top: 0; z-index: 20; display: flex; align-items: center; gap: .75rem;
             border-bottom: 1px solid var(--color-border); padding: .7rem 2rem;
             background: color-mix(in srgb, var(--color-surface) 90%, transparent);
             backdrop-filter: blur(10px); }}
  .sg-body {{ padding: 2.5rem 2rem 5rem; max-width: 60rem; }}
  @media (max-width: 640px) {{ .sg-body, .sg-top {{ padding-inline: 1.1rem; }} }}

  .sg-h1 {{ font-family: var(--font-heading); font-size: 2.25rem; font-weight: 800; letter-spacing: -.02em; }}
  .sg-h3 {{ margin-top: 2.5rem; font-family: var(--font-mono); font-size: var(--size-label);
            font-weight: 700; letter-spacing: var(--tracking-label); text-transform: uppercase;
            color: var(--color-label); }}
  .sg-lede {{ margin-top: .75rem; max-width: 44rem; color: var(--color-muted);
              font-size: var(--size-lead); line-height: var(--leading-body); }}
  .sg-note {{ margin-top: .9rem; max-width: 44rem; font-size: var(--size-small); color: var(--color-muted); }}
  .sg-row {{ display: flex; flex-wrap: wrap; gap: 1.25rem 1.5rem; margin-top: 1.1rem; align-items: flex-end; }}
  .sg-spec {{ display: flex; flex-direction: column; gap: .5rem; }}
  .sg-stage {{ display: flex; align-items: center; gap: .5rem; flex-wrap: wrap; min-height: 2.5rem; }}
  .sg-spec--wide .sg-stage {{ display: block; }}
  .sg-label {{ font-family: var(--font-mono); font-size: .65rem; letter-spacing: .05em; color: var(--color-label); }}

  .sg-swatches {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(7rem, 1fr));
                  gap: .75rem; margin-top: 1.1rem; }}
  .sg-swatch {{ display: flex; flex-direction: column; gap: .4rem; }}
  .sg-swatch__chip {{ height: 3.25rem; border-radius: var(--radius-card);
                      box-shadow: inset 0 0 0 1px var(--color-border); }}

  .sg-tokens {{ margin-top: 1.1rem; border-collapse: collapse; font-size: var(--size-small); }}
  .sg-tokens th {{ text-align: left; padding: .4rem .8rem .4rem 0; font-family: var(--font-mono);
        font-size: var(--size-label); letter-spacing: var(--tracking-label); text-transform: uppercase;
        color: var(--color-label); border-bottom: 1px solid var(--color-border); }}
  .sg-tokens td {{ padding: .4rem .8rem .4rem 0; border-bottom: 1px solid var(--color-border); }}
  .sg-token-val {{ font-family: var(--font-mono); color: var(--color-muted); }}

  .sg-pager {{ display: flex; justify-content: space-between; gap: 1rem; margin-top: 4rem;
               padding-top: 1.5rem; border-top: 1px solid var(--color-border); }}
  .sg-pager a {{ display: flex; flex-direction: column; gap: .2rem; }}
  .sg-pager span {{ font-family: var(--font-mono); font-size: var(--size-label);
                    letter-spacing: var(--tracking-label); text-transform: uppercase; color: var(--color-label); }}
  .sg-pager b {{ font-weight: 600; color: var(--color-ink); }}
</style>
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
      <button class="icon-btn" style="margin-left:auto" aria-label="Toggle dark mode" onclick="
        var h=document.documentElement, n=h.getAttribute('data-theme')==='dark'?'light':'dark';
        h.setAttribute('data-theme',n); try{{localStorage.setItem('ns-theme',n)}}catch(e){{}}">
        <svg class="dark:hidden" width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 3a9 9 0 1 0 9 9 7 7 0 0 1-9-9Z"/></svg>
        <svg class="hidden dark:block" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4" fill="currentColor"/><path d="M12 2v2m0 16v2M4.2 4.2l1.4 1.4m12.8 12.8 1.4 1.4M2 12h2m16 0h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/></svg>
      </button>
    </div>
    <div class="sg-body">
{content}
    </div>
  </main>
</div>
<script>
  // Print the computed value of each token row, so the tables never go stale.
  var cs = getComputedStyle(document.documentElement);
  document.querySelectorAll('.sg-token-val').forEach(function (el) {{
    el.textContent = cs.getPropertyValue(el.dataset.token).trim() || '—';
  }});
</script>
</body>
</html>
"""


def build():
    OUT.mkdir(exist_ok=True)
    order = [(g, s, t) for g, s, t, _, _ in PAGES]

    # ── Home ────────────────────────────────────────────────────────────────
    first = order[0][1]
    rules = "".join(
        f'<div class="ns-card ns-card--sm"><span class="ns-index" style="color:var(--color-brand-500);'
        f'font-size:1.1rem">{i + 1:02d}</span>'
        f'<h3 style="margin-top:.4rem;font-family:var(--font-heading);font-weight:700">{t}</h3>'
        f'<p style="margin-top:.3rem;font-size:var(--size-small);color:var(--color-muted);'
        f'line-height:var(--leading-body)">{d}</p></div>'
        for i, (t, d) in enumerate(RULES))

    layers = "".join(
        f'<a class="ns-card ns-card--sm ns-card--interactive" href="{slug}.html" style="text-decoration:none">'
        f'<span class="ns-card__meta">Layer {i}</span>'
        f'<h3 style="margin-top:.3rem;font-family:var(--font-heading);font-weight:700">{name}</h3>'
        f'<p style="margin-top:.3rem;font-size:var(--size-small);color:var(--color-muted)">{desc}</p></a>'
        for i, (name, desc, slug) in enumerate((
            ("Foundation", "Tokens, variables and mixins. Declares values, paints nothing.", "colors"),
            ("Elements", "Bare HTML — what a tag looks like with no class on it.", "el-typography"),
            ("Components", "The UI library. One file per component, each with its variants.", "button"),
            ("Modules", "Per-feature styling: navbar, curriculum, course, catalog, training.", "modules"))))

    counts = {g: sum(1 for x in PAGES if x[0] == g) for g in GROUPS}
    home = f'''
      <span class="ns-kicker">Design system</span>
      <h1 class="sg-h1" style="margin-top:.5rem">Developer Console</h1>
      <p class="sg-lede">The design language behind Namaste Salesforce. Everything on these
      pages is rendered from the theme's real <code>assets/built/screen.css</code> — if it
      looks right here, it looks right on the site.</p>

      <div style="margin-top:1.75rem;display:flex;flex-wrap:wrap;gap:.75rem">
        <a class="ns-btn ns-btn--primary ns-btn--lg" href="{first}.html">Start <i class="ph ph-arrow-right"></i></a>
        <a class="ns-btn ns-btn--outline ns-btn--lg" href="button.html">Jump to components</a>
      </div>

      <div class="ns-stats" style="margin-top:2rem">
        <div class="ns-stat"><span class="ns-stat__value">4</span><span class="ns-stat__label">layers</span></div>
        <div class="ns-stat"><span class="ns-stat__value">{counts["Foundation"]}</span><span class="ns-stat__label">foundation pages</span></div>
        <div class="ns-stat"><span class="ns-stat__value">{counts["Components"]}</span><span class="ns-stat__label">components</span></div>
        <div class="ns-stat"><span class="ns-stat__value">1</span><span class="ns-stat__label">signal colour</span></div>
      </div>

      <h3 class="sg-h3">The five rules</h3>
      <div style="margin-top:1rem;display:grid;gap:.75rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr))">{rules}</div>

      <h3 class="sg-h3">The layers</h3>
      <p class="sg-note">The CSS is four numbered layers, each with its own <code>index.css</code>.
      A later layer spends what the earlier ones declare, never the other way round.</p>
      <div style="margin-top:1rem;display:grid;gap:.75rem;grid-template-columns:repeat(auto-fit,minmax(15rem,1fr))">{layers}</div>

      <h3 class="sg-h3">Naming</h3>
      <p class="sg-note">Every component follows one contract, so variants compose instead of
      multiplying classes:</p>
      <table class="sg-tokens" style="margin-top:.75rem">
        <thead><tr><th>Pattern</th><th>Means</th></tr></thead>
        <tbody>
          <tr><td><code>.ns-thing</code></td><td>the base — the smallest version that stands alone</td></tr>
          <tr><td><code>.ns-thing--variant</code></td><td>one axis at a time: size, shape, tone or state</td></tr>
          <tr><td><code>.ns-thing__part</code></td><td>a named internal part</td></tr>
          <tr><td><code>.is-state</code></td><td>a runtime state a script toggles</td></tr>
        </tbody>
      </table>
    '''
    (OUT / "index.html").write_text(SHELL.format(
        title="Overview", group="Overview", sidebar=sidebar("index"), content=home))

    # ── Content pages ───────────────────────────────────────────────────────
    for idx, (group, slug, title, blurb, blocks) in enumerate(PAGES):
        prev_ = order[idx - 1] if idx else None
        next_ = order[idx + 1] if idx + 1 < len(order) else None
        pager = ['<nav class="sg-pager">']
        pager.append(f'<a href="{prev_[1]}.html"><span>← Previous</span><b>{prev_[2]}</b></a>'
                     if prev_ else '<span></span>')
        pager.append(f'<a href="{next_[1]}.html" style="text-align:right"><span>Next →</span><b>{next_[2]}</b></a>'
                     if next_ else '<span></span>')
        pager.append("</nav>")

        content = (f'<h1 class="sg-h1">{title}</h1><p class="sg-lede">{blurb}</p>'
                   + "".join(render_block(b) for b in blocks) + "".join(pager))
        (OUT / f"{slug}.html").write_text(SHELL.format(
            title=title, group=group, sidebar=sidebar(slug), content=content))

    # ── Guard: every ph-* glyph must exist in the SUBSETTED icon font, or it
    #    silently renders as a blank box (see CLAUDE.md, "Icon font").
    subset = set(re.findall(r"\.(ph-[a-z0-9-]+)",
                            pathlib.Path("assets/css/0-foundation/icons.css").read_text()))
    used = set()
    for f in OUT.glob("*.html"):
        used |= set(re.findall(r"\b(ph-[a-z0-9-]+)", f.read_text()))
    missing = sorted(used - subset - {"ph-fill"})
    print(f"styleguide/ — {len(PAGES) + 1} pages, {len(used)} glyphs")
    if missing:
        raise SystemExit("NOT IN THE ICON SUBSET (would render blank): " + ", ".join(missing)
                         + "\n  → pick another glyph, or add it to CONTENT_SAFELIST in"
                           " scripts/subset-icons.py and re-run it.")
    print("all glyphs present in the subset")


if __name__ == "__main__":
    build()
