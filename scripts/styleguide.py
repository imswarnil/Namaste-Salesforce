"""The styleguide post — every Koenig card and every prose element, once.

WHY IT EXISTS. A theme is judged on what happens when a writer uses a card the
developer never tried. Ghost's editor can emit two dozen card types and a full
range of prose elements, and a theme that only styles the four its author
happened to use looks broken the first time somebody drops in a bookmark.

This post is the check. Open it after any CSS change; if something here looks
wrong, it is wrong on somebody's real post too.

It is also the answer to "does dark mode work" — every card below has to be
readable in both schemes, and Ghost's own cards.min.css hard-codes light-mode
colours for several of them (see the unlayered block in ghost/content.css).
"""
import lexical as L

MEDIA = "/assets/media"

def build():
    return L.doc([
        L.p("Everything Ghost's editor can produce, on one page. If a card here looks wrong, it is wrong on a real post too — that is the entire purpose of this page."),

        # ── Prose ──────────────────────────────────────────────────────────
        L.h("Headings and prose", 2),
        L.p("Body copy sits at the reading size with the reading leading, on a measure of about 68 characters. The paragraph you are reading is the baseline everything else is judged against."),
        L.h("A third-level heading", 3),
        L.p("Third-level headings are one step down and keep the same tight tracking. Below them, a fourth level exists and is deliberately close to body size — if you need it often, the page wants splitting."),
        L.h("A fourth-level heading", 4),
        L.p("Inline styles: this sentence contains bold, italic and a link to prove each one survives the prose layer."),

        L.h("Lists", 2),
        L.ul(["An unordered item, kept short.",
              "A second item that runs long enough to wrap onto a second line, so the hanging indent and the marker alignment can both be checked at once.",
              "A third, to prove the spacing between items is even."]),
        L.ol(["Ordered lists use the mono face for their markers.",
              "That is what makes a numbered list read as a sequence.",
              "Three items is the minimum that proves it."]),

        L.h("Quotations", 2),
        L.quote("A pull-quote is a change of voice, not an alert. It gets a rule down the side and nothing else."),

        # ── Koenig cards ───────────────────────────────────────────────────
        L.h("Callouts", 2),
        L.p("Ghost offers callouts in several colours. The theme re-tints them from the current surface so they stay legible in dark mode instead of staying pastel on a navy page."),
        L.callout("A plain note, on the sunken surface.", "ℹ️", "grey"),
        L.callout("A warning. Amber means you are about to do something you cannot undo.", "⚠️", "yellow"),
        L.callout("An accent callout — the one signal colour, used once.", "✅", "accent"),

        L.h("Code", 2),
        L.p("Code blocks scroll themselves rather than the page, and carry a copy button from assets/js/code.js."),
        L.code(
            "public with sharing class CaseRouter {\n"
            "    public static void route(List<Case> cases) {\n"
            "        Map<String, Id> queues = queueMap();\n"
            "        for (Case c : cases) {\n"
            "            c.OwnerId = queues.get(c.Origin);\n"
            "        }\n"
            "    }\n"
            "}",
            "apex", "CaseRouter.cls"),
        L.p("A shorter one, in a different language, to prove the label is not hard-coded:"),
        L.code("SELECT Id, Name FROM Account\nWHERE CreatedDate = LAST_N_DAYS:30\nORDER BY Name", "sql", "recent-accounts.soql"),

        L.h("Images", 2),
        L.p("A standard image sits on the reading measure."),
        L.image(f"{MEDIA}/blog-01.png", caption="A standard image, on the reading measure.", alt="Abstract geometric pattern"),
        L.p("A wide image breaks out to the page container."),
        L.image(f"{MEDIA}/blog-02.png", caption="Wide — breaks out of the reading column.", alt="Abstract geometric pattern", card_width="wide"),
        L.p("A full-bleed image takes the whole viewport and drops its corner radius, because a rounded corner against the viewport edge reads as a mistake."),
        L.image(f"{MEDIA}/course-apex-masterclass.png", caption="Full width.", alt="Abstract geometric pattern", card_width="full"),

        L.h("Gallery", 2),
        L.gallery([f"{MEDIA}/module-start.png", f"{MEDIA}/module-build.png", f"{MEDIA}/module-automate.png"]),

        L.h("Bookmark", 2),
        L.p("A bookmark card is a link with its metadata fetched. Ghost hard-codes white-on-white for it, so the theme restates every colour."),
        L.bookmark("https://developer.salesforce.com/docs",
                   "Salesforce Developer Documentation",
                   "The official reference for the platform — Apex, SOQL, LWC and the APIs.",
                   author="Salesforce", publisher="developer.salesforce.com"),

        L.h("Toggle", 2),
        L.toggle("Does this expand?", "It does, and the chevron rotates. The heading is a real button and the content is real markup, so it is searchable and printable."),

        L.h("Button", 2),
        L.button("A primary action", "/courses/", "center"),

        L.h("Divider", 2),
        L.hr(),
        L.p("A horizontal rule separates sections inside an article and gets more air than a rule between blocks."),

        L.h("Embed", 2),
        L.p("An embed arrives as an iframe of unknown aspect ratio; the theme pins video embeds to 16:9 so they do not letterbox."),
        L.embed("https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                '<iframe width="200" height="113" src="https://www.youtube.com/embed/dQw4w9WgXcQ" frameborder="0" allowfullscreen title="Embedded video"></iframe>',
                title="An embedded video"),

        L.h("Markdown and raw HTML", 2),
        L.p("Both are escape hatches, and both have to be styled because writers use them."),
        L.markdown("A **markdown** card, with a [link](/blog/) and `inline code`.\n\n> And a blockquote inside it."),
        L.html_card('<p>A raw HTML card. It gets the prose layer like everything else.</p>'),

        L.h("Tables", 2),
        L.markdown("| Limit | Synchronous | Asynchronous |\n|---|---|---|\n| SOQL queries | 100 | 200 |\n| DML statements | 150 | 150 |\n| CPU time | 10s | 60s |\n| Heap | 6 MB | 12 MB |"),

        L.hr(),
        L.p("End of the styleguide. Anything the editor can produce that is not on this page is untested."),
    ])
