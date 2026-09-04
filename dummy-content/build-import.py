#!/usr/bin/env python3
"""Generates dummy-content/import.json — a Ghost importable data set
that exercises every feature of the theme with realistic content:

  · three courses with numbered lessons ("01 · What is a Salesforce
    org?"), published in order — the course slug EQUALS its public
    tag's slug and every lesson's primary tag is that tag: the whole
    parent/child mechanism
  · three training modules (the module IS a public tag) with
    numbered section posts
  · six blog posts, six library videos (two with a chapters table —
    first column timestamps — which video.js turns into the seeking
    sidebar), four newsletter issues, six changelog entries
  · six snippets with real Apex/SOQL/Flow/LWC code, four prompts,
    six resources, four shop items
  · four slide decks at /slides/ — slides end at divider cards;
    one deck is members-only (the locked cover), one is built
    entirely from editor cards (callout, code, image, button),
    one exercises the sl-* teaching kit (steps, do/don't, stats,
    quiz, flow)
  · six projects — GitHub-style repos at /projects/ — with
    #project-lang-* / #project-stars-* internal tags whose
    DESCRIPTIONS carry the display language and star count
  · the COMPLETE facet taxonomy with chip text in tag DESCRIPTIONS
    (the theme renders descriptions, never parses slugs), including
    the full site-wide duration ramp
  · every data: page.* the routes reference, plus navigation
    settings using the dropdown convention (+Library / -Videos …)

Import in Ghost Admin → Settings → Import/Export, or POST to
/ghost/api/admin/db/. Slugs are all new — safe beside existing
content. The importer dedupes tags by slug.

After importing, run dummy-content/build-thumbnails.py to draw the
branded SVG thumbnails the feature_image URLs already point at.
"""
import json, secrets, datetime

# Deterministic timeline: eighteen months of publishing, oldest
# first, ending shortly before "now". Every post names its own day
# offset — nothing is random, reruns are stable.
START = datetime.datetime(2025, 3, 10, 9, 0, 0)

def oid():
    return secrets.token_hex(12)

def ts(days, hour=9):
    when = START + datetime.timedelta(days=days)
    return when.replace(hour=hour).strftime('%Y-%m-%dT%H:%M:%S.000Z')

# ── lexical builders ────────────────────────────────────────────
def text(t):
    return {"detail": 0, "format": 0, "mode": "normal", "style": "", "text": t, "type": "text", "version": 1}

def para(t):
    return {"children": [text(t)], "direction": "ltr", "format": "", "indent": 0, "type": "paragraph", "version": 1}

def h2(t):
    return {"children": [text(t)], "direction": "ltr", "format": "", "indent": 0, "type": "heading", "tag": "h2", "version": 1}

def li(t):
    return {"children": [text(t)], "direction": "ltr", "format": "", "indent": 0, "type": "listitem", "value": 1, "version": 1}

def ul(*items):
    return {"children": [li(i) for i in items], "direction": "ltr", "format": "", "indent": 0,
            "type": "list", "listType": "bullet", "start": 1, "tag": "ul", "version": 1}

def embed(video_id, caption=""):
    """A YouTube embed card. IDs point at famously stable videos —
    obviously placeholders; swap in real recordings."""
    return {"type": "embed", "version": 1, "embedType": "video",
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "html": (f'<iframe width="480" height="270" '
                     f'src="https://www.youtube.com/embed/{video_id}?feature=oembed" '
                     f'frameborder="0" allow="accelerometer; autoplay; clipboard-write; '
                     f'encrypted-media; gyroscope; picture-in-picture" '
                     f'allowfullscreen title="Video lesson"></iframe>'),
            "metadata": {}, "caption": caption}

def codecard(lang, code, caption=""):
    return {"type": "codeblock", "version": 1, "language": lang, "code": code, "caption": caption}

def htmlcard(markup):
    """A raw HTML card — the slide decks author each slide as one
    of these, separated by divider cards."""
    return {"type": "html", "version": 1, "html": markup}

def hr():
    """A divider card. In a #slides post every divider ENDS a
    slide — deck.js splits the rendered content on them."""
    return {"type": "horizontalrule", "version": 1}

def chapters(rows):
    """A chapters table — FIRST column timestamps. video.js reads
    exactly this shape and builds the seeking sidebar from it."""
    md = "| Time | Chapter |\n|---|---|\n"
    md += "\n".join(f"| {t} | {c} |" for t, c in rows)
    return {"type": "markdown", "version": 1, "markdown": md}

def lexical(*nodes):
    return json.dumps({"root": {"children": list(nodes), "direction": "ltr", "format": "", "indent": 0, "type": "root", "version": 1}})

def body(intro, sections, closing=None):
    """A believable article: a lead paragraph, then h2 sections."""
    nodes = [para(intro)]
    for heading, copy in sections:
        nodes.append(h2(heading))
        nodes.append(para(copy))
    if closing:
        heading, items = closing
        nodes.append(h2(heading))
        nodes.append(ul(*items))
    return lexical(*nodes)

PRACTICE = ("Practice in your org", [
    "Open your Developer Edition org and follow along step by step",
    "Change one thing at a time and note what happens",
    "When something breaks, read the error before searching for it",
])

# ── tags ────────────────────────────────────────────────────────
tags, tag_ids = [], {}

def tag(name, slug, description=None, visibility="internal"):
    """Internal tags follow Ghost's slug convention: #name → hash-name.
    tag_ids is keyed by the BARE slug so call sites stay readable.

    Public tags get a feature image: the branded badge SVG that
    build-thumbnails.py draws into assets/images/tags/{slug}.svg —
    templates use it as the tag's icon everywhere (module badges,
    card eyebrows, chips). __GHOST_URL__ token, as always: a bare
    relative path gets nulled by Ghost's normalisation job."""
    tid = oid()
    tag_ids[slug] = tid
    real_slug = ("hash-" + slug) if visibility == "internal" else slug
    feature_image = (f"__GHOST_URL__/assets/images/tags/{slug}.svg"
                     if visibility == "public" else None)
    tags.append({"id": tid, "name": name, "slug": real_slug,
                 "description": description, "visibility": visibility,
                 "feature_image": feature_image})
    return tid

# THE COLLECTION TAGS — one internal tag per collection, the simple
# vocabulary routes.yaml filters on (tag:hash-course …).
tag("#course", "course", "Marks a post as a course landing page")
tag("#lesson", "lesson", "Marks a post as a course lesson")
tag("#module", "module", "Marks a post as a training module landing page")
tag("#training", "training", "Marks a post as a training module section")
tag("#blog", "blog", "Marks a post as a blog article")
tag("#video", "video", "Marks a post as a library video")
tag("#slides", "slides", "Marks a post as a slide deck")
tag("#newsletter", "newsletter", "Marks a post as a newsletter issue")
tag("#changelog", "changelog", "Marks a post as a changelog entry")
tag("#resource", "resource", "Marks a post as a curated resource")
tag("#shop", "shop", "Marks a post as a shop item")
tag("#snippet", "snippet", "Marks a post as a code snippet")
tag("#prompt", "prompt", "Marks a post as an AI prompt")
tag("#project", "project", "Marks a post as an open-source project")

# facets — the description IS the chip text
tag("#course-level-beginner", "course-level-beginner", "Beginner")
tag("#course-level-intermediate", "course-level-intermediate", "Intermediate")
tag("#course-level-advanced", "course-level-advanced", "Advanced")

# THE DURATION RAMP — one vocabulary for lessons, training pages
# and videos alike: #duration-5m … #duration-55m in five-minute
# steps, then #duration-1h, #duration-1h-15m … for hours. The
# chip text is the DESCRIPTION; templates match the slug prefix
# hash-duration- and never parse it.
for m in range(5, 60, 5):
    tag(f"#duration-{m}m", f"duration-{m}m", f"{m} min")
for h, mins in [(1, 0), (1, 15), (1, 30), (1, 45), (2, 0), (2, 30),
                (3, 0), (4, 0), (5, 0), (6, 0)]:
    slug = f"duration-{h}h" + (f"-{mins}m" if mins else "")
    label = f"{h} hr" + (f" {mins} min" if mins else "")
    tag(f"#{slug}", slug, label)

tag("#lesson-type-video", "lesson-type-video", "Video lesson")
tag("#lesson-type-audio", "lesson-type-audio", "Audio lesson")
tag("#lesson-type-quiz", "lesson-type-quiz", "Quiz")
tag("#video-preview", "video-preview", "Cards play this post's video as a muted preview")

# course layouts — restyle the course hero only (none → classic)
tag("#course-layout-cinema", "course-layout-cinema", "Dark full-bleed hero, image as backdrop")
tag("#course-layout-minimal", "course-layout-minimal", "Centered type, no image")
tag("#course-layout-billboard", "course-layout-billboard", "Wide image banner on top")
tag("#course-layout-boxed", "course-layout-boxed", "Hero framed in a floating card")

# curriculum styles — restyle the course lesson list (none → classic)
tag("#course-curriculum-cards", "course-curriculum-cards", "Curriculum as a tile grid")
tag("#course-curriculum-timeline", "course-curriculum-timeline", "Curriculum as a vertical timeline")
tag("#course-curriculum-compact", "course-curriculum-compact", "Dense curriculum rows, no excerpts")
tag("#course-curriculum-checklist", "course-curriculum-checklist", "Check-marked curriculum rows")

# lesson layouts — restyle the player only (none → classic)
tag("#lesson-layout-right", "lesson-layout-right", "Curriculum rail on the right")
tag("#lesson-layout-focus", "lesson-layout-focus", "No rail — collapsible contents, centered article")
tag("#lesson-layout-cinema", "lesson-layout-cinema", "Dark hero card on the lesson header")
tag("#lesson-layout-wide", "lesson-layout-wide", "Narrow rail, wide article")

# blog options
tag("#blog-layout-magazine", "blog-layout-magazine", "Full-bleed hero layout")
tag("#blog-layout-minimal", "blog-layout-minimal", "Centered, imageless layout")
tag("#blog-layout-split", "blog-layout-split", "Text left, image right")
tag("#blog-layout-wide", "blog-layout-wide", "Breakout image layout")
tag("#blog-sidebar-left", "blog-sidebar-left", "Sidebar on the left")
tag("#blog-sidebar-none", "blog-sidebar-none", "No sidebar, full width")
tag("#blog-toc-hide", "blog-toc-hide", "Hide the table of contents")

# changelog entry types — the badge on /changelog and the entry
# header. The description IS the badge text; the slug suffix is
# the colour class (partials/changelog-badge.hbs).
tag("#changelog-type-feature", "changelog-type-feature", "Feature")
tag("#changelog-type-improvement", "changelog-type-improvement", "Improvement")
tag("#changelog-type-fix", "changelog-type-fix", "Fix")
tag("#changelog-type-content", "changelog-type-content", "Content")

# resource facets — the /resources filter sidebar builds from these;
# the DESCRIPTION is the button label
tag("#resource-type-books", "resource-type-books", "Book")
tag("#resource-type-videos", "resource-type-videos", "Video")
tag("#resource-type-tools", "resource-type-tools", "Tool")
tag("#resource-type-courses", "resource-type-courses", "Course")
tag("#resource-type-podcasts", "resource-type-podcasts", "Podcast")
tag("#resource-type-articles", "resource-type-articles", "Article")
tag("#resource-free", "resource-free", "Free")
tag("#resource-paid", "resource-paid", "Paid")

# shop facets — price is the DESCRIPTION, never the slug
tag("#shop-free", "shop-free", "Free")
tag("#shop-price-9", "shop-price-9", "$9")
tag("#shop-price-19", "shop-price-19", "$19")
tag("#shop-price-29", "shop-price-29", "$29")

# snippet languages
tag("#snippet-lang-apex", "snippet-lang-apex", "Apex")
tag("#snippet-lang-soql", "snippet-lang-soql", "SOQL")
tag("#snippet-lang-flow", "snippet-lang-flow", "Flow")
tag("#snippet-lang-js", "snippet-lang-js", "JavaScript")

# what a prompt is for
tag("#prompt-for-agentforce", "prompt-for-agentforce", "Agentforce")
tag("#prompt-for-claude", "prompt-for-claude", "Claude")
tag("#prompt-for-chatgpt", "prompt-for-chatgpt", "ChatGPT")

# project facets — GitHub grammar: the language dot's label and the
# star count are both tag DESCRIPTIONS (card-project.hbs)
tag("#project-lang-apex", "project-lang-apex", "Apex")
tag("#project-lang-javascript", "project-lang-javascript", "JavaScript")
tag("#project-lang-xml", "project-lang-xml", "XML")
tag("#project-lang-python", "project-lang-python", "Python")

# cross-cutting: any post tagged #now surfaces on /now
tag("#now", "now", "Shows this post on /now while it's being worked on")

# public: topics
tag("Apex", "apex", "The platform's language: classes, triggers, tests and limits.", "public")
tag("Flow", "flow", "Declarative automation — from screen flows to platform events.", "public")
tag("LWC", "lwc", "Lightning Web Components: modern JavaScript on-platform.", "public")
tag("Admin", "admin", "Configuration, security, reports — the org, run well.", "public")
tag("Integration", "integration", "APIs, events and middleware: moving data without losing it.", "public")
tag("AI + Agentforce", "ai-agentforce", "Agents, prompts and what actually ships on the platform.", "public")
tag("DevOps", "devops", "Source control, deployments and the pipeline between orgs.", "public")
tag("Careers", "careers", "The Salesforce job market without the hype.", "public")

# ── posts ───────────────────────────────────────────────────────
posts, posts_tags = [], []

THUMB = "__GHOST_URL__/assets/images/thumbs/{}.svg"

def post(title, slug, tag_slugs, excerpt, sections, day, hour=9,
         featured=False, lead=None, closing=None, intro=None, kind="post",
         visibility="public"):
    """feature_image points at the branded SVG thumbnail that
    dummy-content/build-thumbnails.py draws per post into
    assets/images/thumbs/{slug}.svg — run it after importing. The
    __GHOST_URL__ token is mandatory: a bare relative path gets
    nulled by Ghost's URL-normalisation job.

    visibility passes straight through to Ghost ("public",
    "members", "paid") — the theme's member gating is Ghost's
    own post access, nothing more."""
    pid = oid()
    when = ts(day, hour)
    nodes = list(lead) if lead else []
    doc = json.loads(body(intro or excerpt, sections, closing))
    doc["root"]["children"] = nodes + doc["root"]["children"]
    posts.append({
        "id": pid, "title": title, "slug": slug,
        "lexical": json.dumps(doc),
        "feature_image": THUMB.format(slug),
        "featured": 1 if featured else 0,
        "type": kind, "status": "published", "visibility": visibility,
        "custom_excerpt": excerpt,
        "created_at": when, "updated_at": when, "published_at": when,
    })
    for order, ts_slug in enumerate(tag_slugs):
        posts_tags.append({"id": oid(), "post_id": pid,
                           "tag_id": tag_ids[ts_slug], "sort_order": order})

def page(title, slug, excerpt, sections, day, lead=None):
    post(title, slug, [], excerpt, sections, day, kind="page", lead=lead)

# ════════════════════════════════════════════════════════════════
# COURSES — the slug of the course post EQUALS its public tag's
# slug, and every lesson's PRIMARY (first) tag is that tag. That
# single equality is the entire parent/child mechanism.
# ════════════════════════════════════════════════════════════════

# Course 1 · Salesforce Admin Foundations — 6 lessons, classic layout
tag("Salesforce Admin Foundations", "admin-foundations",
    "From your first login to an org you actually understand — objects, users, security and reports.", "public")
post("Salesforce Admin Foundations", "admin-foundations",
     ["admin-foundations", "course", "course-level-beginner", "duration-4h"],
     "From your first login to an org you actually understand. No prior Salesforce experience needed — just a free Developer Edition.",
     [("What this course covers",
       "The data model, users and permissions, page layouts, and reports — the four things every admin touches every week. Each lesson ends with you having changed something real in your own org."),
      ("Who it is for",
       "Career changers, junior admins, and developers who inherited an org. If you can fill in a spreadsheet, you can finish this course.")],
     0, featured=True)

admin_lessons = [
    ("01 · What is a Salesforce org?", "what-is-a-salesforce-org",
     ["duration-15m"],
     "Instance, org, environment — the words everyone uses and nobody defines. Fifteen minutes to a mental model that sticks.",
     [("The org is the unit of everything",
       "Your org is one tenant on shared infrastructure: its own data, its own metadata, its own users. Sandboxes are copies of the metadata; Developer Editions are free standalone orgs — sign up for one now, it is your lab for this whole course."),
      ("Setup is home",
       "Almost everything an admin does starts from the Setup gear. Learn the Quick Find box first: typing beats navigating, every single time.")]),
    ("02 · Objects, fields and records", "objects-fields-and-records",
     ["duration-20m"],
     "The spreadsheet analogy that gets you started, and where it breaks down.",
     [("Objects are tables, until they aren't",
       "An object is a table, a field is a column, a record is a row — that gets you through week one. What the analogy misses: objects carry behaviour, security and relationships that spreadsheets never had."),
      ("Standard first, custom second",
       "Account, Contact and Opportunity solve more than you think. Build a custom object only after you can say why a standard one does not fit — future you will thank present you.")]),
    ("03 · Users, profiles and permission sets", "users-profiles-permission-sets",
     ["lesson-type-video", "duration-25m", "lesson-layout-cinema"],
     "Watch a new user go from created to correctly permissioned — the modern way, with one baseline profile and permission sets on top.",
     [("One profile, many permission sets",
       "Salesforce is retiring profile-based permissions for a reason. Give everyone a minimum-access profile and grant everything else through permission sets — additive, auditable, and stackable."),
      ("The login-as trick",
       "Nothing debugs a permission problem faster than logging in as the user. Enable it in your Developer Edition and see exactly what they see.")]),
    ("04 · Page layouts and Lightning record pages", "page-layouts-and-lightning-record-pages",
     ["duration-20m"],
     "Two systems control what a record looks like, and they overlap just enough to confuse everyone.",
     [("Layouts own the fields, Lightning pages own the page",
       "Page layouts decide which fields and related lists exist; Lightning record pages decide where components sit around them. Change the wrong one and nothing happens — now you know why."),
      ("Dynamic Forms changes the deal",
       "With Dynamic Forms, fields move onto the Lightning page itself with per-field visibility rules. New builds should start there.")]),
    ("05 · Reports and dashboards for humans", "reports-and-dashboards-for-humans",
     ["duration-30m"],
     "From a blank report to a dashboard your manager actually opens — report types, filters, and the three charts that cover most questions.",
     [("The report type decides everything",
       "Pick the wrong report type and no amount of filtering will show the records you need. Learn to read 'Accounts with or without Contacts' before you build anything."),
      ("Dashboards answer questions",
       "Every widget should answer one question a real person actually asks. If you cannot name the person and the question, delete the widget.")]),
    ("06 · Check your understanding: admin foundations", "check-your-understanding-admin-foundations",
     ["lesson-type-quiz", "duration-10m", "lesson-layout-right"],
     "Ten scenarios from real orgs. For each: what would you change, and what would you refuse to change?",
     [("How to take this",
       "Answer before you peek. The scenarios are drawn from real org audits — the wrong answers here are things I have actually found in production."),
      ("If you missed more than three",
       "Revisit lessons 03 and 05 — permissions and report types are where foundations crack first.")]),
]
for i, (title, slug, extra, excerpt, sections) in enumerate(admin_lessons):
    lead = [embed("aqz-KE-bpKQ")] if "lesson-type-video" in extra else None
    post(title, slug, ["admin-foundations", "lesson"] + extra, excerpt, sections,
         3 + i * 3, lead=lead, closing=PRACTICE)

# Course 2 · Apex for Absolute Beginners — 8 lessons, cinema hero
tag("Apex for Absolute Beginners", "apex-beginners",
    "Your first classes, triggers and tests — written slowly, explained completely.", "public")
post("Apex for Absolute Beginners", "apex-beginners",
     ["apex-beginners", "course", "course-level-beginner", "duration-6h",
      "course-layout-cinema", "course-curriculum-cards"],
     "You have never written code, or never written Apex. Eight lessons later you will have a tested trigger running in your own org.",
     [("What this course covers",
       "Classes, variables and collections, SOQL and DML from Apex, your first trigger done safely, governor limits, and the test class that proves it all works."),
      ("Who it is for",
       "Admins ready to cross the line, and developers from other stacks who keep tripping on the platform's rules. We assume zero Apex and explain every line.")],
     70)

apex_lessons = [
    ("01 · Hello, Apex: your first class", "hello-apex-your-first-class",
     ["duration-20m"],
     "Open the Developer Console, write ten lines, run them anonymously — and understand every one of them.",
     [("Where Apex runs",
       "Apex executes on Salesforce's servers, inside a transaction, under limits. That one sentence explains most of what makes it different from JavaScript or Python."),
      ("Execute Anonymous is your REPL",
       "The Developer Console's Execute Anonymous window runs any block instantly. It is how you will test every idea in this course before committing it to a class.")]),
    ("02 · Variables, types and collections", "variables-types-and-collections",
     ["duration-25m"],
     "Lists, Sets and Maps do ninety percent of the work in real Apex. Learn the three of them properly and the rest is syntax.",
     [("Strong types, few surprises",
       "Every variable declares its type. Id is not a String (until it is), Decimal beats Double for money, and null is the value you will meet most often."),
      ("Map<Id, SObject> is the workhorse",
       "Half of all bulk-safe Apex is 'build a map, look things up by Id'. We build three of them in this lesson so the shape becomes reflex.")]),
    ("03 · SOQL: asking the database questions", "soql-asking-the-database-questions",
     ["duration-25m", "lesson-layout-wide"],
     "SELECT is not SQL — no joins, no wildcards, relationship dots instead. Write your first twenty queries in the Query Editor.",
     [("Relationships replace joins",
       "Contact.Account.Name walks up; (SELECT ... FROM Contacts) walks down. Once relationship queries click, you will stop missing joins."),
      ("Query in loops is the cardinal sin",
       "One SOQL query per record is how orgs die at scale. We commit the rule to memory now, two lessons before triggers make it dangerous.")]),
    ("04 · DML and the database", "dml-and-the-database",
     ["duration-20m"],
     "insert, update, upsert, delete — and what happens to the transaction when one record out of two hundred fails.",
     [("All or nothing, unless you ask",
       "Plain DML rolls the whole batch back on one failure; Database.insert(records, false) lets the rest through and hands you the errors. Know which one each situation needs."),
      ("Upsert and external IDs",
       "Upsert against an external ID field is the backbone of every integration you will ever build. We set one up and watch it match.")]),
    ("05 · Triggers, the safe way", "triggers-the-safe-way",
     ["lesson-type-video", "duration-30m"],
     "Watch a before-insert trigger written live: one trigger per object, logic in a handler class, bulk-safe from the first line.",
     [("The pattern before the syntax",
       "One trigger per object, no logic in the trigger body, a handler class with one method per event. Learn the pattern first and you will never untangle spaghetti later."),
      ("Before vs after",
       "Before triggers change the records in flight for free; after triggers see final field values and Ids. Choosing wrong costs you a query or an error.")]),
    ("06 · Governor limits explained", "governor-limits-explained",
     ["duration-25m"],
     "100 queries, 150 DML statements, 10 seconds of CPU — the limits are not obstacles, they are the platform's design language.",
     [("Why limits exist",
       "You share the server with thousands of orgs. Limits are how everyone's code stays fast — and they quietly teach you to write better Apex than you would elsewhere."),
      ("Reading a limit exception",
       "'Too many SOQL queries: 101' tells you exactly what happened: a query inside a loop met 200 records. We trigger the error on purpose and then fix it.")]),
    ("07 · Testing: proving it works", "testing-proving-it-works",
     ["duration-30m"],
     "75% coverage is the law, but coverage is not the point — assertions are. Write a test that would actually catch a bug.",
     [("Tests build their own world",
       "Test methods see no org data. Build every record you need inside the test — it is more work and it is also why your tests still pass in a fresh sandbox."),
      ("Assert like you mean it",
       "A test without assertions is a coverage donation. Assert the field values you changed, the errors you expected, and the records you did not touch.")]),
    ("08 · Quiz: are you ready for production?", "quiz-are-you-ready-for-production",
     ["lesson-type-quiz", "duration-15m", "lesson-layout-focus"],
     "Twelve questions covering the whole course. Pass this and your first real trigger is next week's problem.",
     [("How to take this",
       "Each question is a small piece of code with something wrong: a limit about to blow, a missing bulk pattern, a test that asserts nothing. Find it before reading the answer."),
      ("Where to go next",
       "The Apex Triggers training module goes deeper on everything lesson 05 introduced — order of execution, recursion control, the full handler pattern.")]),
]
for i, (title, slug, extra, excerpt, sections) in enumerate(apex_lessons):
    lead = [embed("aqz-KE-bpKQ")] if "lesson-type-video" in extra else None
    post(title, slug, ["apex-beginners", "lesson"] + extra, excerpt, sections,
         73 + i * 3, lead=lead, closing=PRACTICE)

# Course 3 · Flow Builder Mastery — 5 lessons, billboard hero
tag("Flow Builder Mastery", "flow-mastery",
    "Beyond the happy path: flows that survive production — fault paths, limits and all.", "public")
post("Flow Builder Mastery", "flow-mastery",
     ["flow-mastery", "course", "course-level-advanced", "duration-3h",
      "course-layout-billboard", "course-curriculum-timeline"],
     "You already build flows. This course is about the ones that survive production — entry conditions, fault paths, and knowing when Flow is the wrong answer.",
     [("What this course covers",
       "Record-triggered flows done right, screen flows users finish, error handling that alerts you before the user does, and the async patterns — scheduled paths and platform events."),
      ("Who it is for",
       "Admins and developers who have shipped basic flows and been burned at least once. If you have never seen 'An unhandled fault has occurred', start with Admin Foundations instead.")],
     180)

flow_lessons = [
    ("01 · The anatomy of a flow", "the-anatomy-of-a-flow",
     ["duration-20m"],
     "Elements, resources, connectors — and the two panels in Flow Builder everyone ignores until a debug session forces them to look.",
     [("Resources are variables wearing a costume",
       "Every formula, variable, and record collection is a resource. Name them like code — get_Account, var_SendEmail — and your future debug logs become readable."),
      ("The debug panel tells the truth",
       "Debug runs show every element's inputs and outputs. Learn to read one now; every later lesson assumes you can.")]),
    ("02 · Record-triggered flows done right", "record-triggered-flows-done-right",
     ["lesson-type-video", "duration-30m", "lesson-layout-cinema"],
     "Build one alongside the video: tight entry conditions, before-save vs after-save, and the update that cannot recurse.",
     [("Entry conditions are your governor limit",
       "A flow that fires on every edit of every Account is a tax on the whole org. Entry conditions keep it to the records that matter — set them first, always."),
      ("Before-save when you can",
       "Before-save flows update the triggering record with no extra DML and run an order of magnitude faster. Reach for after-save only when you must touch other records.")]),
    ("03 · Screen flows people actually finish", "screen-flows-people-actually-finish",
     ["duration-25m"],
     "Multi-screen wizards, conditional visibility, and the difference between a form users complete and one they abandon.",
     [("One question per screen beats ten",
       "Users abandon walls of fields. Short screens with visibility rules feel like a conversation — completion rates prove it."),
      ("Validate early, fail kindly",
       "Validate on the screen where the answer lives, not three screens later. An error message should say what to do next, not what went wrong internally.")]),
    ("04 · Fault paths and error handling", "fault-paths-and-error-handling",
     ["duration-25m"],
     "Every element that touches the database can fail. Decide on purpose what happens when it does.",
     [("The fault connector nobody drags",
       "Every Create, Update, Delete and Action element has a fault path waiting. Drag it to a subflow that logs the error and notifies someone — once, centrally, for every flow you own."),
      ("What to tell the user",
       "'An unhandled fault has occurred' is a resignation letter. A caught fault can say: your record was saved, the follow-up email was not, and an admin has been notified.")]),
    ("05 · Scheduled paths and platform events", "scheduled-paths-and-platform-events",
     ["duration-30m", "lesson-layout-right"],
     "The async toolbox: run minutes later, run nightly, or hand off to another system entirely — without a line of Apex.",
     [("Scheduled paths are the gentle async",
       "'Ten minutes after the record meets conditions' covers a surprising share of async needs — reminders, escalations, SLA checks — with none of the ceremony."),
      ("Platform events cross the boundary",
       "Publish an event and anything can subscribe: another flow, Apex, or an external system on CometD. It is the loose coupling your integrations wanted all along.")]),
]
for i, (title, slug, extra, excerpt, sections) in enumerate(flow_lessons):
    lead = [embed("aqz-KE-bpKQ")] if "lesson-type-video" in extra else None
    post(title, slug, ["flow-mastery", "lesson"] + extra, excerpt, sections,
         183 + i * 3, lead=lead, closing=PRACTICE)

# ════════════════════════════════════════════════════════════════
# TRAINING — mirrors the course mechanism. A module is a public
# tag AND a landing post tagged #module whose slug EQUALS the
# tag's slug (/training/{slug}/); the sections are #training
# posts carrying that tag as primary tag
# (/training/{primary_tag}/{slug}/), oldest first.
# ════════════════════════════════════════════════════════════════
tag("Data Model & Schema", "data-model",
    "Objects, relationships and the decisions you cannot cheaply undo.", "public")
tag("Apex Triggers", "apex-triggers",
    "One trigger per object, logic in handlers, bulk-safe by default.", "public")
tag("Integration Patterns", "integration-patterns",
    "Request-reply, events, batch — picking the pattern before the tool.", "public")

# MODULE LANDING POSTS — slug exactly equals the module tag's
# slug; module tag FIRST (primary), then #module. Published just
# before the module's first section.
module_landings = [
    ("Data Model & Schema", "data-model", 34,
     "Objects, relationships and record types — the schema decisions you cannot cheaply undo, made deliberately.",
     [("What you'll learn",
       "How to choose between standard and custom objects, pick the right relationship type with three questions, use record types for the right reasons, read any org's real schema in Schema Builder, and build a many-to-many properly with a junction object."),
      ("Prerequisites",
       "Admin Foundations lessons 01–02, or equivalent comfort with objects, fields and records. A free Developer Edition org to build in."),
      ("How the sections chain",
       "Five sections, oldest first, each building on the last: you start by deciding whether an object should exist at all, then how it relates, then how it varies, then how to read what is already there — and finish by building the trickiest shape, the junction, end to end.")],
     ["Run the reuse test before creating any custom object",
      "Choose lookup vs master-detail with three questions, not habit",
      "Spot the three warning signs of record-type overuse",
      "Audit an inherited org's schema in ten minutes",
      "Model a many-to-many with correct sharing on both sides"]),
    ("Apex Triggers", "apex-triggers", 119,
     "One trigger per object, logic in handlers, bulk-safe by default — the discipline that keeps automation debuggable.",
     [("What you'll learn",
       "The order of execution as a map you can actually navigate, the one-trigger-per-object rule and the handler pattern that enforces it, bulkification as a reflex rather than a review comment, and recursion control that does not break batch two."),
      ("Prerequisites",
       "Apex for Absolute Beginners through lesson 05, or working knowledge of classes, SOQL and DML. Every section assumes you can deploy a class to a Developer Edition."),
      ("How the sections chain",
       "Five sections in publish order: first the map (what runs when you press Save), then the rule, then the pattern that implements the rule, then the discipline that keeps it fast at 200 records — and finally the guard that keeps it from calling itself.")],
     ["Sequence any save's automation from memory",
      "Refactor multi-trigger objects to one trigger + handler",
      "Write collect–query–map–loop–DML without thinking",
      "Test at 200 records, not one",
      "Break recursion with an Id set, not a boolean"]),
    ("Integration Patterns", "integration-patterns", 249,
     "Request-reply, events, batch, middleware — pick the integration pattern before the tool, and design for the failure first.",
     [("What you'll learn",
       "The four patterns that cover nearly every Salesforce integration: synchronous request-reply behind named credentials, fire-and-forget with platform events, nightly batch sync on external IDs, and when the middleware question actually becomes a middleware answer."),
      ("Prerequisites",
       "Comfortable Apex (the Apex Triggers module or equivalent) and a basic grasp of REST. The video section builds a callout live if you have never written one."),
      ("How the sections chain",
       "Four written sections plus a build-along video: synchronous first because it is the default everyone reaches for, then events for when the caller should not wait, then batch for when nobody is waiting at all — closing with the architecture question that decides how the next integration gets built.")],
     ["Stand up a named-credential callout with a tested mock",
      "Design idempotent subscribers for at-least-once delivery",
      "Build reruns-are-safe batch loads on external IDs",
      "Argue middleware vs point-to-point with edge counts",
      "Choose a pattern from latency and ownership, not fashion"]),
]
for name, mslug, day, excerpt, sections, outcomes in module_landings:
    post(name, mslug, [mslug, "module"], excerpt, sections, day,
         closing=("What you'll be able to do", outcomes))

training_modules = [
    ("data-model", 35, [
        ("01 · Standard objects vs custom objects", "standard-vs-custom-objects", "duration-10m",
         "Account, Contact, Opportunity, Case solve more than you think — the checklist to run before you create anything custom.",
         [("The reuse test",
           "Before creating a custom object, ask: does a standard object with a record type cover this? Standard objects come with reports, mobile layouts and AppExchange integrations for free."),
          ("The cost of custom",
           "Every custom object is a permanent resident: permissions, layouts, sharing, API names in code. Creating one is a five-minute job; retiring one is a quarter.")]),
        ("02 · Relationship types, decided with three questions", "relationship-types-three-questions", "duration-15m",
         "Lookup, master-detail or junction — answered by ownership, cascade delete, and roll-ups.",
         [("The three questions",
           "Does the child make sense without the parent? Should deleting the parent delete the child? Do you need roll-up summaries? Master-detail answers no, yes, yes; lookup answers the reverse."),
          ("Converting later is possible, painful",
           "You can switch lookup to master-detail only while every child has a parent, and the switch rewrites sharing. Decide up front; this is a one-way door that pretends not to be.")]),
        ("03 · Record types and when not to use them", "record-types-when-not-to-use-them", "duration-10m",
         "Record types shine for genuinely different processes on one object — and multiply your maintenance everywhere else.",
         [("The right reason",
           "Different sales processes, different page layouts, different picklist values for the same object: that is what record types are for. One object, several shapes."),
          ("The three warning signs",
           "If record types differ only by one field, if users constantly pick the wrong one, or if you have more than five on an object — you probably wanted a field, a flow, or a separate object.")]),
        ("04 · Schema Builder, the honest map", "schema-builder-the-honest-map", "duration-10m",
         "The one Setup tool that shows your data model as it is, not as the ERD on the wiki claims it is.",
         [("Read before you draw",
           "Open Schema Builder on any org you inherit. The orphaned objects and mystery lookups you find in ten minutes would take a week of clicking through Object Manager."),
          ("Draw carefully",
           "Schema Builder can create fields and relationships directly — convenient in a Developer Edition, a footgun in production. Look with it; build through your normal deployment path.")]),
        ("05 · Junction objects in practice", "junction-objects-in-practice", "duration-15m",
         "Many-to-many done properly: two master-details, sharing inherited from both sides, and a real example built end to end.",
         [("The pattern",
           "A Course can have many Students, a Student many Courses: the Enrollment junction object carries two master-detail relationships and any fields that belong to the pair — grade, date, status."),
          ("Sharing rides the master-details",
           "A junction record is visible only to users who can see BOTH parents. That is usually what you want, and it is also the first place to look when someone cannot see an enrollment.")]),
    ]),
    ("apex-triggers", 120, [
        ("01 · Order of execution, the map", "order-of-execution-the-map", "duration-15m",
         "Before triggers, validation, after triggers, assignment rules, flows, roll-ups — what actually runs when you press Save.",
         [("Why the map matters",
           "Half of all 'my field keeps getting overwritten' mysteries are two automations at different steps of the same save. You cannot debug what you cannot sequence."),
          ("The steps that bite",
           "Before-save flows run before before-triggers. Workflow field updates re-fire triggers. Roll-ups run late. Print the diagram and pin it where you debug.")]),
        ("02 · One trigger per object", "one-trigger-per-object", "duration-10m",
         "Two triggers on one object run in an order Salesforce refuses to promise. The fix is a rule, not a framework.",
         [("The rule",
           "One trigger per object, ever. It contains no logic — it delegates every event to a handler class. Order becomes explicit, bypass becomes possible, tests become sane."),
          ("Enforcing it",
           "A naming convention (AccountTrigger, AccountTriggerHandler) plus a code review checklist is enough. Frameworks help at scale, but the rule is what saves you.")]),
        ("03 · The handler pattern", "the-handler-pattern", "duration-15m",
         "One method per event, a static bypass flag, and constructor-free classes your tests will thank you for.",
         [("The shape",
           "beforeInsert(newList), afterUpdate(oldMap, newMap) — the trigger passes context variables straight through. The handler owns every decision; the trigger owns nothing."),
          ("The bypass flag",
           "A public static Boolean lets data migrations and tests switch the handler off without touching metadata. Use sparingly; log every use.")]),
        ("04 · Bulkification: 200 records or bust", "bulkification-200-records-or-bust", "duration-15m",
         "Triggers receive up to 200 records at once. Every query and DML statement inside a loop is a countdown to 'Too many SOQL queries: 101'.",
         [("The discipline",
           "Collect Ids in a loop, query once into a Map, look up inside the loop, collect changes, DML once at the end. Every bulk-safe trigger is that sentence, rearranged."),
          ("Test at 200",
           "A test that inserts one record proves nothing about limits. Insert a List of 200 and your future data-loader migrations stop being surprises.")]),
        ("05 · Recursion control", "recursion-control", "duration-10m",
         "Your after-update updates the record, which fires your after-update. Breaking the loop without breaking legitimate re-entry.",
         [("Why a plain flag is wrong",
           "A static 'hasRun' Boolean blocks the second batch of a 400-record update too — that is legitimate re-entry, not recursion. Track processed record Ids in a static Set instead."),
          ("Better: stop causing it",
           "Most recursion is an after trigger doing a before trigger's job. Assigning field values on the in-flight record in before-save costs no DML and cannot recurse.")]),
    ]),
    ("integration-patterns", 250, [
        ("01 · Request-reply with named credentials", "request-reply-named-credentials", "duration-15m",
         "The synchronous callout, done properly: named credentials for auth, a timeout you chose on purpose, and a mock for the test.",
         [("Named credentials or nothing",
           "Endpoint URLs and secrets do not belong in Apex or custom settings. A named credential moves auth to configuration — and survives the sandbox refresh that would have leaked your token."),
          ("Design for the timeout",
           "Every callout needs an answer to 'what if this takes 30 seconds?' If the user is waiting on the answer, the honest fix is usually to make the integration asynchronous.")]),
        ("02 · Fire-and-forget with platform events", "fire-and-forget-platform-events", "duration-15m",
         "When the caller does not need an answer, publish an event and move on — decoupling, replay, and the delivery guarantees you actually get.",
         [("At-least-once, not exactly-once",
           "Platform events can be delivered more than once and subscribers can fall behind. Design subscribers to be idempotent and the guarantee becomes a feature, not a caveat."),
          ("The replay Id is your safety net",
           "External subscribers can resume from the last replay Id after a disconnect. Store it; the day your middleware restarts mid-stream you will be glad you did.")]),
        ("03 · Batch sync without tears", "batch-sync-without-tears", "duration-15m",
         "Nightly loads still run the world. Upsert on external IDs, order parents before children, and make reruns safe.",
         [("External IDs are the contract",
           "Match on the source system's key, never on Salesforce Ids the source does not know. An indexed external ID field per synced object is the whole trick."),
          ("Idempotency first",
           "Design every load so running it twice changes nothing the second time. When (not if) the 2 a.m. job dies halfway, the fix becomes 'run it again' instead of an archaeology project.")]),
        ("04 · Middleware or point-to-point?", "middleware-or-point-to-point", "duration-10m",
         "Two systems talking directly is simple right up until it is three systems, then five. Where the line actually sits.",
         [("Count the edges",
           "Point-to-point between n systems tends toward n² connections, each with its own auth, retries and error handling. Middleware turns that into n connections to one hub."),
          ("But do not buy a bus for one route",
           "One Salesforce org calling one API does not need an integration platform. Start point-to-point behind a named credential; move to middleware when the third system shows up.")]),
    ]),
]
for module, start_day, sections in training_modules:
    for i, (title, slug, dur, excerpt, body_sections) in enumerate(sections):
        post(title, slug, [module, "training", dur], excerpt, body_sections,
             start_day + i * 3, closing=PRACTICE)

# One video section inside a module — proves the rail's type icons
# work for training too.
post("05 · Watch: a callout built end to end", "watch-a-callout-built-end-to-end",
     ["integration-patterns", "training", "lesson-type-video", "duration-20m"],
     "Twenty minutes from a blank class to a tested, mocked, named-credential callout — narrated, mistakes left in.",
     [("Follow along",
       "Pause after each step and run the same code in your own org. The named credential setup happens on screen too — nothing is pre-baked."),
      ("Mentioned in this video",
       "HttpCalloutMock, Test.setMock, and the two-minute trick for inspecting the request your code actually sent.")],
     262, lead=[embed("aqz-KE-bpKQ")])

# ════════════════════════════════════════════════════════════════
# BLOG — six real articles, layouts spread across the variants.
# ════════════════════════════════════════════════════════════════
blog_posts = [
    ("Why your Flow fails silently in production", "why-your-flow-fails-silently-in-production",
     ["blog", "flow"], 25,
     "The flow works in the sandbox, passes UAT, and then quietly stops firing for one profile in production. Here is the checklist that finds it.",
     [("The usual suspects",
       "Nine times out of ten it is one of four things: entry conditions referencing a field the running user cannot see, a paused interview waiting on a time path, an element-level fault swallowed without a fault path, or the flow simply not activated after deployment."),
      ("Field-level security is invisible to Flow",
       "A flow running in user context silently gets null for fields the user cannot read. No error, no debug line — the decision element just takes the other branch. Run system context deliberately or grant the permission deliberately; never leave it to luck."),
      ("Build the alarm before the fire",
       "A one-element subflow on every fault path — log a record, notify a channel — costs ten minutes per flow and turns 'users have been silently affected for three weeks' into 'we knew within the hour'.")]),
    ("Salesforce release notes, decoded: Winter '26", "salesforce-release-notes-decoded-winter-26",
     ["blog", "admin", "blog-layout-magazine"], 100,
     "Six hundred pages of release notes, reduced to the eleven changes that will actually touch your org — and the two that might break it.",
     [("Read the retirements first",
       "The gold is at the back: features entering retirement. Workflow rules and process builder migrations stop being optional the release they go read-only — count backwards from that date, not forwards from today."),
      ("The quiet permission changes",
       "Every release tightens a default somewhere. This one touches guest user access and API versions below 40 — run the release-update checklist in a sandbox on preview weekend, not in production on go-live morning."),
      ("What I am actually excited about",
       "Flow gets reactive screens everywhere, and the new Apex Cursors go GA — pagination over big queries without the offset dance. Both land in the courses here over the next month.")]),
    ("The Apex mistakes I still see in every org", "apex-mistakes-i-still-see-in-every-org",
     ["blog", "apex", "blog-layout-split"], 150,
     "Fifteen years of the same five mistakes: queries in loops, tests without assertions, triggers with opinions, hardcoded Ids, and empty catch blocks.",
     [("Queries in loops, still",
       "The 101st SOQL query has been throwing the same exception since 2008 and it remains the number one production incident I get called about. The fix is a pattern, not a talent — collect, query once, map, loop."),
      ("Tests that assert nothing",
       "Coverage without assertions is a donation to the deployment gods. If the method's behaviour changed completely and the test still passed, it was never a test."),
      ("The empty catch block",
       "catch (Exception e) {} is a decision to find out about failures from your users. Log it, rethrow it, or write the comment explaining why silence is genuinely correct — there is no fourth option.")]),
    ("Agentforce, six months in: what actually works", "agentforce-six-months-in",
     ["blog", "ai-agentforce", "blog-layout-wide", "blog-toc-hide"], 210,
     "Past the keynote demos: where agents genuinely help today, where they embarrass you in front of customers, and how to scope your first one.",
     [("What works today",
       "Narrow, grounded, reversible: case deflection over a curated knowledge base, order status lookups, appointment rescheduling. The common thread — the agent retrieves and drafts, a human or a hard rule commits."),
      ("What does not, yet",
       "Anything requiring the agent to be right about your org's edge cases on the first try. Free-text actions that write to records without review generate the tickets they were meant to deflect."),
      ("Scope your first agent like a junior hire",
       "Give it the job you would give a smart temp on day one: bounded inputs, a script to deviate from, an escalation path, and an audit log. Expand scope the way you would for a human — after it earns it.")]),
    ("How I'd learn Salesforce in 2026, starting from zero", "how-id-learn-salesforce-in-2026",
     ["blog", "careers", "blog-layout-minimal", "blog-sidebar-left"], 280,
     "No certifications-first, no 500 hours of videos. A Developer Edition, one project you care about, and a public log of what you built.",
     [("Build before you badge",
       "Certifications open interviews; projects survive them. A working org that solves a real problem — your club's memberships, your side hustle's invoices — teaches more than any amount of passive watching."),
      ("The weekly loop",
       "Build something small, break it, fix it, write two paragraphs about what you learned, in public. Twelve weeks of that loop beats a year of consuming content — and the log becomes your portfolio."),
      ("Where the jobs moved",
       "Pure point-and-click admin roles are consolidating; admin-plus roles — admin plus Flow, plus data, plus a scripting language — are growing. Learn declarative first, but do not stop there.")]),
    ("Your sandbox strategy is why deploys hurt", "your-sandbox-strategy-is-why-deploys-hurt",
     ["blog", "devops"], 440,
     "If every deploy is a fire drill, the problem started three environments earlier. A sandbox map that actually matches how teams work.",
     [("The minimum viable pipeline",
       "Developer sandboxes per builder, one shared integration sandbox, one UAT that mirrors production data shape, production. Fewer than that and changes collide; more and changes queue."),
      ("Refresh on a calendar, not a crisis",
       "A stale sandbox lies to you about production. Put refreshes on the calendar — after each release lands is the natural rhythm — and script the post-refresh setup you currently do by hand."),
      ("Source of truth means one",
       "The org is the truth or the repo is the truth; pick one and mean it. Half-adopted git where hotfixes go straight to production is how Sunday deploys become Sunday-and-Monday deploys.")]),
]
for title, slug, tag_slugs, day, excerpt, sections in blog_posts:
    post(title, slug, tag_slugs, excerpt, sections, day)

# ════════════════════════════════════════════════════════════════
# VIDEOS — the library at /videos/. A table whose FIRST column is
# timestamps becomes the seeking chapter sidebar (video.js). The
# first two carry #video-preview: cards play them muted.
# ════════════════════════════════════════════════════════════════
videos = [
    ("Build a record-triggered flow in 20 minutes", "build-a-record-triggered-flow-in-20-minutes",
     "aqz-KE-bpKQ", ["flow", "duration-20m", "video-preview"], 55,
     "Entry conditions, a decision, a before-save update and a fault path — a production-shaped flow, built live with no cuts.",
     chapters([("00:00", "What we're building and why"),
               ("01:30", "Object, trigger type, entry conditions"),
               ("05:45", "The decision element done right"),
               ("09:20", "Before-save field updates"),
               ("13:10", "Adding the fault path"),
               ("16:40", "Debug run and activation"),
               ("18:55", "What to build next")]),
     [("What you will see",
       "Screen and narration only — no slides. Every click happens on screen, including the two mistakes and their fixes."),
      ("Mentioned in this video",
       "The Flow Builder Mastery course covers each of these elements in depth, one lesson per element.")]),
    ("Data model walkthrough: a quoting app from scratch", "data-model-walkthrough-quoting-app",
     "jNQXAC9IVRw", ["admin", "duration-30m", "video-preview"], 108,
     "Watch a real data model take shape: objects, relationship choices argued out loud, and the junction object that saves the design.",
     chapters([("00:00", "The requirements, in plain words"),
               ("03:15", "Standard objects we get for free"),
               ("07:40", "Quote and QuoteLine: master-detail, argued"),
               ("14:05", "The pricing junction object"),
               ("21:30", "Roll-up summaries and totals"),
               ("26:10", "What we deliberately did not build")]),
     [("What you will see",
       "Schema Builder open the whole time — the model is drawn live, wrong turns included, because the wrong turns are the lesson."),
      ("Mentioned in this video",
       "The Data Model & Schema training module walks the same decisions as reference pages you can keep open while you design.")]),
    ("Debug a failing deployment, live", "debug-a-failing-deployment-live",
     "9bZkp7q19f0", ["devops", "duration-25m"], 160,
     "A real change set fails with 47 errors. Watch them fall to zero: reading the first error properly, test failures vs missing components, and the retry.",
     [("What you will see",
       "The actual error list, worked top to bottom. Forty-six of the forty-seven trace back to two root causes — which is exactly the point."),
      ("Mentioned in this video",
       "The deployment checklist from the shop, and why 'run local tests' beats 'run all tests' for hotfixes.")]),
    ("Five SOQL queries every admin should know", "five-soql-queries-every-admin-should-know",
     "kJQP7kiw5Fk", ["admin", "duration-15m"], 220,
     "The Developer Console query editor is the fastest answer machine in your org — five queries that replace an hour of report building.",
     [("What you will see",
       "Records modified yesterday, users who never logged in, accounts without contacts, the biggest attachments, and picklist value counts — typed, run, and explained."),
      ("Mentioned in this video",
       "Each query lives in the snippets collection too, ready to copy.")]),
    ("Your first Lightning Web Component, line by line", "your-first-lwc-line-by-line",
     "dQw4w9WgXcQ", ["lwc", "duration-35m"], 300,
     "HTML template, JavaScript class, XML metadata — a working component on a record page in half an hour, every line explained.",
     chapters([("00:00", "What LWC is and is not"),
               ("02:50", "Scaffolding with the CLI"),
               ("08:15", "The template: HTML with directives"),
               ("15:30", "The class: @api, @wire, getters"),
               ("24:00", "Deploying and adding to a record page"),
               ("30:20", "Where to go from here")]),
     [("What you will see",
       "VS Code and an org side by side. We deploy after every change so you see exactly which line caused which pixel."),
      ("Mentioned in this video",
       "The LWC debounce snippet, and the lwc-datatable-plus project this component eventually grew into.")]),
    ("Set up an Agentforce agent, end to end", "set-up-an-agentforce-agent-end-to-end",
     "hY7m5jjJ9mM", ["ai-agentforce", "duration-40m"], 450,
     "Topic, instructions, actions, guardrails, test, deploy — a working service agent grounded on a real knowledge base, in one sitting.",
     [("What you will see",
       "The whole builder flow with nothing skipped: writing instructions that actually constrain, wiring a flow action, and the test bench catching a hallucination before customers do."),
      ("Mentioned in this video",
       "The Agentforce action design rubric from the prompts collection — we score this agent's action against it on screen.")]),
]
for title, slug, vid, extra, day, excerpt, *rest in videos:
    if len(rest) == 2:
        chap, sections = rest
        lead = [embed(vid), chap]
    else:
        (sections,) = rest
        lead = [embed(vid)]
    post(title, slug, ["video"] + extra, excerpt, sections, day, lead=lead)

# ════════════════════════════════════════════════════════════════
# NEWSLETTER — four weekly issues, published ascending so the
# newest issue really is the latest.
# ════════════════════════════════════════════════════════════════
issues = [
    ("The Weekly Namaste #01 — Hello, world", "the-weekly-namaste-01", 490,
     "Why this newsletter exists, what lands in your inbox every Sunday, and the one link to start with.",
     [("This week",
       "Issue one is a promise, not a digest: every Sunday, the three things from the Salesforce world worth your attention, each in two sentences, plus what changed on this site. No sponsor slots, no filler."),
      ("Worth a click",
       "The Admin Foundations course is complete and free — six lessons from first login to a dashboard someone actually opens."),
      ("From the courses",
       "Apex for Absolute Beginners is in progress; the trigger lesson is being filmed this week.")]),
    ("The Weekly Namaste #02 — The fault path issue", "the-weekly-namaste-02", 497,
     "One theme this week: errors you have decided to handle versus errors that are handling you.",
     [("This week",
       "A reader's production incident (shared with permission) traced to a single missing fault path; the new Flow error-handler pattern now in the projects collection; and why 'it works in the sandbox' is a sentence about permissions."),
      ("Worth a click",
       "The 'Why your Flow fails silently in production' post is this newsletter's origin story — read it before your next deploy."),
      ("From the courses",
       "Flow Builder Mastery lesson 04 covers the same ground with a build-along.")]),
    ("The Weekly Namaste #03 — Release week survival", "the-weekly-namaste-03", 504,
     "Preview weekend is here. What to test first, what to ignore, and the release-notes reading order that saves an afternoon.",
     [("This week",
       "Read retirements first, release updates second, your clouds third, everything else never. Plus: the two Winter '26 permission tightenings most likely to page you, and how to check them in ten minutes."),
      ("Worth a click",
       "The full decoded release notes post is on the blog — six hundred pages down to eleven changes."),
      ("From the courses",
       "Admin Foundations lesson 05 gets a refresh for the new report builder this week.")]),
    ("The Weekly Namaste #04 — Agents, honestly", "the-weekly-namaste-04", 511,
     "Six months of Agentforce in real orgs: the wins are real, the demos are still demos, and scoping is everything.",
     [("This week",
       "What separates the agent deployments that stuck from the ones that got quietly turned off — narrow scope, grounded answers, reversible actions. The long version is on the blog; the rubric is in the prompts collection."),
      ("Worth a click",
       "The new end-to-end Agentforce setup video: forty minutes, nothing skipped, one hallucination caught on camera."),
      ("From the courses",
       "Next up: a short course on prompt design for platform work. Reply if you want early access.")]),
]
for title, slug, day, excerpt, sections in issues:
    post(title, slug, ["newsletter"], excerpt, sections, day)

# ════════════════════════════════════════════════════════════════
# CHANGELOG — entries carrying #changelog-type-*: the badge text
# is the tag DESCRIPTION, the slug picks colour + icon.
# ════════════════════════════════════════════════════════════════
changes = [
    ("Namaste Salesforce is live", "namaste-salesforce-is-live", "changelog-type-content", 10,
     "First public release: the Admin Foundations course, the Data Model training module, and a blog.",
     [("What shipped",
       "The site opens with one complete course, one training module, and the first article. Everything is free; the newsletter starts once there is enough here to summarise."),
      ("Why",
       "Learning in public needs a public. This site is the log of everything I build and teach on the platform, structured so you can actually follow along.")]),
    ("Video library launched", "video-library-launched", "changelog-type-feature", 112,
     "Standalone walkthroughs get their own home at /videos/ — with chapter navigation on longer recordings.",
     [("What shipped",
       "Videos no longer hide inside courses. The library lists every walkthrough with its duration; long recordings carry a chapters sidebar that seeks the player when you click a section."),
      ("Why",
       "Half of you watch one specific segment, not the whole recording. Chapters make the twenty-minute videos as skimmable as the five-minute ones.")]),
    ("Duration chips unified site-wide", "duration-chips-unified-site-wide", "changelog-type-improvement", 170,
     "One duration vocabulary now covers lessons, training pages and videos alike — chips read the tag description everywhere.",
     [("What changed",
       "Courses said '2h', videos said '25 minutes', training said nothing. Every duration now comes from one site-wide ramp, rendered identically wherever it appears."),
      ("Why",
       "You should be able to glance at any card anywhere and know the time commitment. Consistency is a feature.")]),
    ("Three courses now complete", "three-courses-now-complete", "changelog-type-content", 240,
     "Flow Builder Mastery joins Admin Foundations and Apex for Absolute Beginners — nineteen lessons across the three tracks.",
     [("What shipped",
       "The advanced Flow track is finished: five lessons from anatomy to platform events, with build-along videos. All three launch courses are now complete and free."),
      ("Why",
       "The three tracks cover the three doors into the platform — admin, code, automation. Everything published next builds on one of them.")]),
    ("Fixed: code blocks in dark mode", "fixed-code-blocks-in-dark-mode", "changelog-type-fix", 320,
     "Snippet syntax colours were unreadable against the dark canvas on some screens. Contrast rebuilt from tokens.",
     [("What changed",
       "Code blocks now derive their palette from the theme's semantic tokens in both modes, instead of shipping one hardcoded scheme. Copy buttons stop overlapping line numbers on narrow screens too."),
      ("Why",
       "Half of all snippet views happen in dark mode after 9 p.m. Reading code should not require switching themes.")]),
    ("Projects collection launched", "projects-collection-launched", "changelog-type-feature", 460,
     "The open-source work gets a proper shelf: /projects/, GitHub-styled, with language and star metadata on every repo.",
     [("What shipped",
       "Six repositories, each with its readme rendered as the post and a real 'View on GitHub' button. Cards show the language dot and star count the way your muscle memory expects."),
      ("Why",
       "The code behind the courses was scattered across gists and repo links in lesson footers. Now everything installable lives in one place.")]),
]
for title, slug, ctype, day, excerpt, sections in changes:
    post(title, slug, ["changelog", ctype], excerpt, sections, day)

# ════════════════════════════════════════════════════════════════
# SNIPPETS — real code in a code card; language on the chip.
# ════════════════════════════════════════════════════════════════
snippets = [
    ("Bulk-safe trigger handler skeleton", "bulk-safe-trigger-handler",
     ["snippet-lang-apex", "apex"], 410,
     "The five-method handler shape that survives 200-record batches — collect, query once, map, loop, DML once.",
     "apex",
     "public with sharing class AccountTriggerHandler {\n"
     "    public static Boolean bypass = false;\n\n"
     "    public static void beforeInsert(List<Account> records) {\n"
     "        if (bypass) return;\n"
     "        for (Account acc : records) {\n"
     "            // never SOQL/DML inside this loop\n"
     "            acc.Rating = acc.AnnualRevenue > 1000000 ? 'Hot' : 'Warm';\n"
     "        }\n"
     "    }\n\n"
     "    public static void afterUpdate(Map<Id, Account> oldMap,\n"
     "                                   Map<Id, Account> newMap) {\n"
     "        List<Account> changed = new List<Account>();\n"
     "        for (Account acc : newMap.values()) {\n"
     "            if (acc.OwnerId != oldMap.get(acc.Id).OwnerId) {\n"
     "                changed.add(acc);\n"
     "            }\n"
     "        }\n"
     "        if (!changed.isEmpty()) OwnerSync.enqueue(changed);\n"
     "    }\n"
     "}",
     [("Gotchas",
       "The bypass flag is for data migrations and tests only — every production use deserves a code comment explaining itself. And afterUpdate compares old to new before doing anything: change detection is what keeps recursion away.")]),
    ("Test data factory, the minimal version", "test-data-factory-minimal",
     ["snippet-lang-apex", "apex"], 411,
     "One class, builder-style defaults, no framework — the 80% of a test factory most orgs actually need.",
     "apex",
     "@isTest\n"
     "public class TestFactory {\n"
     "    public static Account account() { return account('Acme ' + counter()); }\n\n"
     "    public static Account account(String name) {\n"
     "        return new Account(Name = name, Industry = 'Technology');\n"
     "    }\n\n"
     "    public static Contact contact(Id accountId) {\n"
     "        return new Contact(FirstName = 'Test', LastName = 'Person ' + counter(),\n"
     "                           AccountId = accountId,\n"
     "                           Email = 'test' + counter() + '@example.com');\n"
     "    }\n\n"
     "    public static List<Account> accounts(Integer n) {\n"
     "        List<Account> out = new List<Account>();\n"
     "        for (Integer i = 0; i < n; i++) out.add(account());\n"
     "        return out;\n"
     "    }\n\n"
     "    static Integer seq = 0;\n"
     "    static Integer counter() { return ++seq; }\n"
     "}",
     [("Gotchas",
       "Return unsaved records and let the test decide when to insert — tests that need Ids call insert themselves, tests that don't stay fast. The counter keeps unique fields unique across a 200-record build.")]),
    ("SOQL: records modified since yesterday", "soql-modified-since-yesterday",
     ["snippet-lang-soql", "admin"], 412,
     "Relative date literals beat hand-built timestamps every time — and they respect the user's time zone.",
     "sql",
     "SELECT Id, Name, LastModifiedBy.Name, LastModifiedDate\n"
     "FROM Account\n"
     "WHERE LastModifiedDate = YESTERDAY\n"
     "   OR LastModifiedDate = TODAY\n"
     "ORDER BY LastModifiedDate DESC\n"
     "LIMIT 200",
     [("Gotchas",
       "YESTERDAY is the user's calendar yesterday, not 'the last 24 hours' — for a rolling window use LastModifiedDate >= :DateTime.now().addHours(-24) from Apex instead.")]),
    ("SOQL: accounts with no contacts", "soql-accounts-with-no-contacts",
     ["snippet-lang-soql", "admin"], 413,
     "The anti-join: records missing children, without a report type gymnastics session.",
     "sql",
     "SELECT Id, Name, Owner.Name, CreatedDate\n"
     "FROM Account\n"
     "WHERE Id NOT IN (SELECT AccountId FROM Contact)\n"
     "  AND CreatedDate = LAST_N_DAYS:90\n"
     "ORDER BY CreatedDate DESC",
     [("Gotchas",
       "NOT IN with a subquery is limited to one level and can be slow on very large orgs — for millions of accounts, run it in batches or flip it into a report with a cross filter.")]),
    ("Flow formula: business days between dates", "flow-business-days-formula",
     ["snippet-lang-flow", "flow"], 414,
     "No Apex, no loops — one formula resource that counts weekdays between two dates.",
     "text",
     "/* Formula (Number) — business days from {!startDate} to {!endDate} */\n"
     "(5 * FLOOR(({!endDate} - DATE(1900, 1, 8)) / 7)\n"
     "  + MIN(5, MOD({!endDate} - DATE(1900, 1, 8), 7) + 1))\n"
     "-\n"
     "(5 * FLOOR(({!startDate} - DATE(1900, 1, 8)) / 7)\n"
     "  + MIN(5, MOD({!startDate} - DATE(1900, 1, 8), 7) + 1))",
     [("Gotchas",
       "DATE(1900, 1, 8) is a Monday — that anchor is what makes the modulo arithmetic work. Holidays are not weekends: if you need them excluded, that is a custom metadata lookup, not a formula.")]),
    ("LWC: debounce a lightning-input", "lwc-debounce-input",
     ["snippet-lang-js", "lwc"], 415,
     "Stop hammering the server on every keystroke — 300 milliseconds of patience per search box.",
     "javascript",
     "import { LightningElement } from 'lwc';\n\n"
     "const DELAY = 300;\n\n"
     "export default class ContactSearch extends LightningElement {\n"
     "    delayTimeout;\n\n"
     "    handleKeyChange(event) {\n"
     "        window.clearTimeout(this.delayTimeout);\n"
     "        const searchKey = event.target.value;\n"
     "        this.delayTimeout = window.setTimeout(() => {\n"
     "            this.dispatchEvent(\n"
     "                new CustomEvent('search', { detail: { searchKey } })\n"
     "            );\n"
     "        }, DELAY);\n"
     "    }\n"
     "}",
     [("Gotchas",
       "Read event.target.value BEFORE the timeout — the event is recycled by the time the callback runs. Clear the timeout in disconnectedCallback too if the component can unmount mid-typing.")]),
]
for title, slug, tag_slugs, day, excerpt, lang, code, sections in snippets:
    post(title, slug, ["snippet"] + tag_slugs, excerpt, sections, day,
         lead=[codecard(lang, code)])

# ════════════════════════════════════════════════════════════════
# PROMPTS — the AI-era toolbox, each with the full prompt text.
# ════════════════════════════════════════════════════════════════
prompts = [
    ("Explain this Flow like a code review", "explain-flow-code-review",
     ["prompt-for-claude", "flow"], 420,
     "Paste flow metadata, get back risks, misfires and the order-of-execution traps — ranked by blast radius.",
     "You are a senior Salesforce architect reviewing a Flow like a"
     " pull request.\n\nHere is the flow metadata:\n[PASTE FLOW XML]\n\n"
     "Review it for:\n1. Order-of-execution traps (same-record updates,"
     " recursion)\n2. Bulk safety — what happens at 200 records?\n"
     "3. Fault paths — every element that can fail, and what catches it\n"
     "4. Anything Apex would do better, and why\n\nBe blunt."
     " Rank findings by blast radius.",
     [("Why it works",
       "Framing it as a pull request review borrows a discipline the model knows deeply. The numbered rubric stops it from writing a summary instead of a review, and 'rank by blast radius' forces prioritisation over completeness.")]),
    ("Write the test class for this Apex", "write-the-test-class-for-this-apex",
     ["prompt-for-claude", "apex"], 421,
     "Not coverage — assertions. This prompt produces tests that would actually catch the bug you will write next month.",
     "Write an Apex test class for the code below.\n\n[PASTE APEX"
     " CLASS]\n\nRules:\n- Build ALL data in the test; assume an empty"
     " org. Use @testSetup.\n- One test method per behaviour, named"
     " test_<method>_<scenario>_<expected>\n- Include: the happy path, a"
     " 200-record bulk case, the null/empty case, and the failure path"
     " with a try/catch asserting the exception\n- Every test method"
     " must contain at least one Assert with a failure message\n- Do"
     " NOT use SeeAllData, hardcoded Ids, or Test.isRunningTest"
     " branches\n\nAfter the code, list the behaviours you could NOT"
     " test and why.",
     [("Why it works",
       "The rules encode the review checklist most teams enforce by hand, so the output arrives pre-reviewed. The closing instruction — list what you could not test — surfaces the seams (callouts, async) that need mocks before you discover it in the deploy.")]),
    ("Draft release notes from a diff", "release-notes-from-diff",
     ["prompt-for-chatgpt", "devops"], 422,
     "Turns a messy changeset description into release notes humans read — grouped, jargon-free, action-flagged.",
     "Turn this changeset description into release notes humans"
     " read.\n\n[PASTE DIFF / CHANGESET]\n\nRules:\n- Lead with what the"
     " USER can now do, never with what changed internally\n- One line"
     " per change, grouped: New / Improved / Fixed\n- No jargon, no"
     " ticket numbers, no 'various improvements'\n- If a change needs"
     " action from admins, flag it with ACTION:",
     [("Why it works",
       "Each rule kills one specific failure mode of AI release notes: leading with internals, wall-of-text formatting, jargon, and buried breaking changes. The ACTION: flag turns the output into a checklist.")]),
    ("Agentforce action design rubric", "agentforce-action-rubric",
     ["prompt-for-agentforce", "ai-agentforce"], 423,
     "Score a proposed agent action for safety, scope and rollback before anyone builds it.",
     "Score this proposed Agentforce action before anyone builds"
     " it.\n\nAction: [DESCRIBE THE ACTION]\n\nScore 1-5 on:\n-"
     " Blast radius: what is the worst record this can touch?\n-"
     " Reversibility: can a human undo the result in one step?\n-"
     " Scope creep: does it do ONE thing?\n- Auditability: will the"
     " log explain WHY it acted?\n\nBelow 16/20 → redesign before"
     " building.",
     [("Why it works",
       "Four axes with a numeric floor turns 'should we build this?' from a meeting into a score. The blast-radius question in particular forces naming the worst case before the demo, not after it.")]),
]
for title, slug, tag_slugs, day, excerpt, prompt_text, sections in prompts:
    post(title, slug, ["prompt"] + tag_slugs, excerpt, sections, day,
         lead=[codecard("markdown", prompt_text)])

# ════════════════════════════════════════════════════════════════
# RESOURCES — curated links, typed + free/paid for the sidebar.
# ════════════════════════════════════════════════════════════════
resources = [
    ("Advanced Apex Programming", "advanced-apex-programming",
     ["resource-type-books", "resource-paid", "apex"], 390,
     "Dan Appleman's book is still the deepest treatment of Apex patterns in print — read it after your first triggers, not before.",
     [("Why it's here",
       "Everything else teaches you Apex syntax; this book teaches you Apex judgment — limits as a design constraint, asynchronous patterns, and managed package realities nobody blogs about."),
      ("Where to start",
       "Chapter 3 (limits) and chapter 6 (triggers) pay for the book on their own. Skim the rest, return when the topics find you.")]),
    ("Salesforce Developer Documentation", "salesforce-developer-docs",
     ["resource-type-articles", "resource-free", "apex"], 391,
     "The primary source. Learn to read it before any course — including mine.",
     [("Why it's here",
       "Every course, video and blog post is an interpretation; the docs are the contract. The Apex Developer Guide and the SOQL reference answer questions precisely that tutorials answer approximately."),
      ("Where to start",
       "Bookmark the Apex Reference and the Object Reference. When a method behaves oddly, the reference page's fine print usually predicted it.")]),
    ("Workbench", "workbench-tool",
     ["resource-type-tools", "resource-free", "admin"], 392,
     "The Swiss-army knife for SOQL, metadata and REST exploring — free, ancient, and still unmatched for quick answers.",
     [("Why it's here",
       "Query any object, describe any metadata, call any REST endpoint, all from a browser with your existing session. For 'what does the API actually return here?' nothing is faster."),
      ("Where to start",
       "Queries → SOQL Query for data questions; Info → Standard & Custom Objects to read an object's true shape, defaults and all.")]),
    ("Apex Hours", "apex-hours",
     ["resource-type-videos", "resource-free", "apex"], 393,
     "Community-run sessions on everything platform — the archive alone is a curriculum.",
     [("Why it's here",
       "Practitioners presenting to practitioners, for free, for years. The sessions on asynchronous Apex and integration architecture are better than most paid courses on the same topics."),
      ("Where to start",
       "Search the archive for the topic currently hurting you; watch the newest session on it first — the platform moves, and so do the recommendations.")]),
    ("Trailhead", "trailhead",
     ["resource-type-courses", "resource-free", "admin"], 394,
     "Salesforce's own hands-on learning — badges are not skills, but the practice orgs and guided projects are genuinely good.",
     [("Why it's here",
       "The hands-on challenges verify your work in a real org, which beats watching videos by a mile. Use it for breadth; use projects of your own for depth."),
      ("Where to start",
       "The Admin Beginner and Developer Beginner trails pair well with the courses here — do the trail's challenges in the same org you use for my lessons.")]),
    ("Good Day, Sir!", "good-day-sir",
     ["resource-type-podcasts", "resource-free", "careers"], 395,
     "The podcast that keeps the ecosystem honest — opinionated, funny, technical, and unafraid of the word 'no'.",
     [("Why it's here",
       "Two developers who say what consultants will not: which features are ready, which acquisitions matter, and when the emperor's new cloud has no clothes. Listening is how you calibrate the hype."),
      ("Where to start",
       "Any release-week episode — their release-notes reactions are the fastest honest summary you will find anywhere.")]),
]
for title, slug, tag_slugs, day, excerpt, sections in resources:
    post(title, slug, ["resource"] + tag_slugs, excerpt, sections, day)

# ════════════════════════════════════════════════════════════════
# SHOP — digital assets; the price is the tag's DESCRIPTION.
# ════════════════════════════════════════════════════════════════
shop_items = [
    ("Flow Error-Handling Playbook (ebook)", "flow-error-handling-playbook",
     ["shop-price-19", "flow"], 400,
     "Forty pages of fault paths, retry patterns and the alerts worth waking up for — the missing chapter of every Flow course.",
     [("What you get",
       "A 40-page PDF: the central error-logging subflow (with install steps), fault-path patterns per element type, alert routing that respects on-call hours, and the postmortem template we use for automation incidents."),
      ("Who it's for",
       "Teams running ten or more record-triggered flows in production. If you have three flows and one admin, the free blog post covers you — genuinely, save the money.")]),
    ("Admin's Release Readiness Template", "admin-release-readiness-template",
     ["shop-free", "admin"], 401,
     "The Notion + Sheets template I use to digest every Salesforce release in about an hour — retirements first, updates second, hype never.",
     [("What you get",
       "A Notion board with the reading-order checklist, a Sheets tracker for release updates with owner and deadline columns, and the sandbox test script for preview weekend."),
      ("Who it's for",
       "Anyone who owns an org through three releases a year. It is free because everyone should have a system for this — pay with a newsletter subscription if it helps.")]),
    ("Org Health Check Notes", "org-health-check-notes",
     ["shop-price-9", "admin"], 402,
     "My raw working notes from twenty org audits — what to look at, in what order, and the numbers that usually mean trouble.",
     [("What you get",
       "A 15-page working document: the query pack (unused fields, silent automations, permission sprawl), the interview questions for the team, and thresholds with the reasoning behind each one."),
      ("Who it's for",
       "Consultants and new-in-seat admins inheriting an org. It is notes, not a book — you are paying for the order of operations, not the prose.")]),
    ("Namaste Salesforce Ghost Theme", "namaste-salesforce-ghost-theme",
     ["shop-price-29", "devops"], 403,
     "This very site's theme — courses with a lesson player, training trails, video library, snippets, the lot.",
     [("What you get",
       "The theme zip plus the routes file, a setup guide covering the tag conventions that drive everything, and the demo-content generator so you start from a working site."),
      ("Who it's for",
       "Anyone building a learning site on Ghost. Requires comfort editing routes.yaml and Ghost's navigation settings — the setup guide assumes no code beyond that.")]),
]
for title, slug, tag_slugs, day, excerpt, sections in shop_items:
    post(title, slug, ["shop"] + tag_slugs, excerpt, sections, day)

# ════════════════════════════════════════════════════════════════
# PROJECTS — GitHub-style repos at /projects/. Topic tag FIRST
# (the card's topic chip is primary_tag); language and stars ride
# as internal tag DESCRIPTIONS.
# ════════════════════════════════════════════════════════════════
def stars_tag(n):
    slug = f"project-stars-{n}"
    if slug not in tag_ids:
        tag(f"#{slug}", slug, str(n))
    return slug

projects = [
    ("sf-trigger-framework", ["apex"], "project-lang-apex", 312, 330, True,
     "Minimal trigger framework for Salesforce: one trigger per object, handler interface, per-object bypass, recursion guard. No dependencies.",
     [("Why another trigger framework",
       "Most frameworks solve org-scale problems with library-scale complexity. This one is four classes: a handler interface, a dispatcher, a bypass registry, and a recursion guard keyed on record Ids — read all of it in ten minutes."),
      ("Install",
       "Deploy the four classes, create one trigger per object that calls TriggerDispatcher.run(new AccountTriggerHandler()), and delete your old triggers one at a time as their logic moves into handlers."),
      ("Design notes",
       "The recursion guard tracks processed Ids per event, not a global boolean — batch two of a 400-record update still runs. Bypass is per-object and logged, because silent bypasses become permanent bypasses.")]),
    ("lwc-datatable-plus", ["lwc"], "project-lang-javascript", 204, 340, False,
     "lightning-datatable with the missing pieces: server-side pagination, column filters, saved views and CSV export — as one drop-in component.",
     [("What it adds",
       "The standard datatable stops at sorting. This wraps it with cursor-based pagination against your Apex, per-column filter inputs, view definitions users can save, and a client-side CSV export that respects the current filters."),
      ("Install",
       "Deploy the component and its Apex controller interface, implement one method returning a page of rows, and replace your lightning-datatable tag. The README walks a working Account table in fifteen minutes."),
      ("Design notes",
       "Pagination is cursor-based (keyset on Id) rather than OFFSET, so page 40 of a million rows costs the same as page one. Saved views serialise to a custom object, one record per user per table.")]),
    ("apex-test-factory", ["apex"], "project-lang-apex", 128, 350, False,
     "Builder-pattern test data factory for Apex: sensible defaults, relationship wiring, bulk builders — tests that read like specifications.",
     [("Why",
       "Test setup is where Apex tests go to die: forty lines of record building before one line of behaviour. The factory gives every object a builder with working defaults, so a test states only what it cares about."),
      ("Usage",
       "Account acc = TF.account().withIndustry('Banking').insertRecord(); Contact c = TF.contact(acc).build(); — bulk variants (.list(200)) cover the governor-limit cases in one call."),
      ("Design notes",
       "Defaults live in one class per object, so an org's required-field quirks are handled exactly once. Nothing inserts unless you ask — pure-build tests stay database-free and fast.")]),
    ("flow-error-handler", ["flow"], "project-lang-xml", 86, 360, False,
     "Drop-in error handling for Flow: a logging subflow, a platform event, and a notifier — every fault path in your org pointed at one place.",
     [("What it is",
       "An unmanaged package: the FlowError__e platform event, a logging subflow you wire every fault connector to, a subscriber flow that writes Flow_Error_Log__c records, and a notifier with quiet hours."),
      ("Install",
       "Deploy the package, then drag each existing fault connector to the Log Flow Error subflow — the README includes the audit query that lists every unhandled fault path in the org."),
      ("Design notes",
       "Logging goes through a platform event so the log survives the transaction rollback that just destroyed everything else — the whole reason most homegrown error logging silently loses the errors that matter.")]),
    ("sfdx-org-snapshot", ["devops"], "project-lang-python", 57, 370, False,
     "CLI that snapshots an org's metadata and sample data into versioned JSON — diff two snapshots to see what actually changed between refreshes.",
     [("What it does",
       "sfdx-org-snapshot pull captures metadata plus a configurable sample of records per object into a content-addressed JSON tree; diff renders what changed between any two snapshots as a readable report."),
      ("Install",
       "pipx install sfdx-org-snapshot, authenticate with your existing sf CLI session, and add the pull to your post-refresh script. Snapshots are plain files — commit them, diff them, grep them."),
      ("Design notes",
       "Records are sampled deterministically (newest N per object, IDs redacted on request) so two pulls of an unchanged org produce identical trees — which is what makes the diffs mean something.")]),
    ("namaste-salesforce-theme", ["devops"], "project-lang-javascript", 41, 380, False,
     "The Ghost theme powering this site: courses with a lesson player, tag-driven training modules, video chapters, snippets, prompts and a projects shelf.",
     [("What it is",
       "A Ghost theme where one internal tag decides a post's collection, URL and layout — courses nest lessons through a single slug equality, training modules are public tags, and a timestamp table becomes video chapters."),
      ("Install",
       "Upload the theme zip, mirror routes.yaml into Ghost's settings, import the demo content, run the thumbnail generator. The README's conventions section is the part to actually read."),
      ("Design notes",
       "Handlebars and CSS carry everything they can — prev/next inside a course is in=\"primary_tag\", the mobile drawer is a checkbox, the changelog's two views are radio inputs. JavaScript is the last resort, four small files.")]),
]
for title, topic, lang, stars, day, featured, excerpt, sections in projects:
    post(title, title, topic + ["project", lang, stars_tag(stars)],
         excerpt, sections, day, featured=featured)

# A live-demo link is an internal tag whose DESCRIPTION is the
# URL (#project-live-*) — post-project.hbs surfaces it at the top
# of the About rail. One demo project carries it.
tag("#project-live-lwc-datatable-plus", "project-live-lwc-datatable-plus",
    "https://demo.namastesalesforce.com/lwc-datatable-plus")
for p in posts:
    if p["slug"] == "lwc-datatable-plus":
        posts_tags.append({"id": oid(), "post_id": p["id"],
                           "tag_id": tag_ids["project-live-lwc-datatable-plus"],
                           "sort_order": 50})

# ════════════════════════════════════════════════════════════════
# SLIDES — teaching decks at /slides/. Each slide is ONE html
# card; every divider card ends a slide (deck.js splits on <hr>).
# The members-only deck demonstrates Ghost's own post access
# gating the player (post-slides.hbs shows the locked cover).
# ════════════════════════════════════════════════════════════════
def deck(title, slug, tag_slugs, excerpt, slides_src, day,
         visibility="public"):
    """Each entry in slides_src is ONE slide: an HTML string (one
    html card) or a LIST of lexical nodes — any Koenig cards the
    editor can produce. Divider cards go between slides."""
    nodes = []
    for i, s in enumerate(slides_src):
        if i:
            nodes.append(hr())
        if isinstance(s, str):
            nodes.append(htmlcard(s))
        else:
            nodes.extend(s)
    pid = oid()
    when = ts(day)
    posts.append({
        "id": pid, "title": title, "slug": slug,
        "lexical": lexical(*nodes),
        "feature_image": THUMB.format(slug), "featured": 0,
        "type": "post", "status": "published", "visibility": visibility,
        "custom_excerpt": excerpt,
        "created_at": when, "updated_at": when, "published_at": when,
    })
    for order, s in enumerate(tag_slugs):
        posts_tags.append({"id": oid(), "post_id": pid,
                           "tag_id": tag_ids[s], "sort_order": order})

deck("The Salesforce Org in 3 Slides", "the-salesforce-org-in-3-slides",
     ["slides", "admin", "duration-10m"],
     "The whole mental model on three slides — org, metadata, security. The deck I open in every intro session.",
     ["<h2>One org, everything in it</h2>"
      "<p>Your org is one tenant on shared infrastructure — its own data, its own metadata, its own users.</p>"
      "<ul><li>Sandboxes are copies of the <strong>metadata</strong>, not the data</li>"
      "<li>A Developer Edition is a free standalone org — your lab</li>"
      "<li>Almost everything starts from Setup: learn the Quick Find box first</li></ul>",

      "<h2>Metadata is the product</h2>"
      "<p>Objects, fields, layouts, flows, classes — everything you build is metadata, and metadata can move between orgs.</p>"
      "<ul><li>Data lives in records; behaviour lives in metadata</li>"
      "<li>Deployments move metadata, never (normally) data</li>"
      "<li>If you can't retrieve it with the CLI, ask what it really is</li></ul>",

      "<h2>Security decides what the table shows</h2>"
      "<p>Two users open the same list view and see different worlds — by design.</p>"
      "<ul><li>Profiles + permission sets: what you can <em>do</em></li>"
      "<li>Org-wide defaults + sharing: which <em>records</em> you can see</li>"
      "<li>Field-level security: which <em>columns</em> exist for you</li></ul>"
      "<p>Next step: open your own org and check all three for one user.</p>"],
     385)

deck("Governor Limits Survival Deck", "governor-limits-survival-deck",
     ["slides", "apex", "duration-15m"],
     "Members only: the four limits that actually stop real orgs, one slide each — and the reflexes that keep you clear of them.",
     ["<h2>Limits are the platform's contract</h2>"
      "<p>Shared infrastructure means every transaction runs inside hard budgets. The good news: only a handful matter day to day.</p>",

      "<h2>100 SOQL queries</h2>"
      "<p>The one that catches everyone. A query inside a loop over 200 trigger records is 200 queries.</p>"
      "<ul><li>Query <strong>before</strong> the loop, into a Map by Id</li>"
      "<li>Let the trigger handler own the queries, not the helpers</li></ul>",

      "<h2>150 DML statements</h2>"
      "<p>Same shape, same fix: collect records into a list, one insert or update at the end.</p>",

      "<h2>CPU time: 10 seconds</h2>"
      "<p>The quiet one — it accumulates across every trigger, flow and process in the transaction.</p>"
      "<ul><li>Measure with debug logs before optimising anything</li>"
      "<li>Move heavy work async: Queueable beats @future</li></ul>"],
     390, visibility="members")

# The third deck is built from EDITOR CARDS, not html — callout,
# code, image, button — proving any Koenig card works on a slide.
deck("Slides with Editor Cards", "slides-with-editor-cards",
     ["slides", "devops", "duration-10m"],
     "A deck made only of Ghost editor cards — callout, code, image, button — one per slide. Copy this pattern for your own decks.",
     [[h2("Slides are just editor cards"),
       para("Write a deck the way you write a post. Any card the editor produces works on a slide — the theme restyles it for the canvas."),
       {"type": "callout", "version": 1, "calloutEmoji": "💡",
        "calloutText": "End a slide with a divider card. That's the whole authoring model.",
        "backgroundColor": "blue"}],

      [h2("Show real code"),
       codecard("apex",
                "trigger AccountTrigger on Account (before insert, before update) {\n"
                "    TriggerDispatcher.run(new AccountTriggerHandler());\n"
                "}",
                "One trigger per object — the logic lives in the handler.")],

      [h2("Drop in an image"),
       {"type": "image", "version": 1, "src": THUMB.format("admin-foundations"),
        "width": 1200, "height": 675, "title": "", "alt": "Course cover",
        "caption": "Images centre themselves and keep the projector honest.",
        "cardWidth": "regular", "href": ""}],

      [h2("Close with a call to action"),
       para("A deck should end with the next step, not a thank-you slide."),
       {"type": "button", "version": 1, "buttonText": "Browse the courses",
        "alignment": "center", "buttonUrl": "__GHOST_URL__/courses/"}]],
     392)

# The fourth deck exercises THE TEACHING KIT — the sl-* slide
# components (slides/_surface.css): steps, do/don't, stats,
# quiz, flow. Each slide is one HTML card using the classes.
deck("The Teaching Kit", "the-teaching-kit",
     ["slides", "admin", "duration-15m"],
     "Every sl-* slide component on one deck — title, steps, do/don't, big numbers, a quiz and a process flow. Steal these slides.",
     ["<div class=\"sl-center\">"
      "<p class=\"sl-kicker\">The teaching kit</p>"
      "<h1>Slides built to teach</h1>"
      "<p>Numbered steps, do/don't panels, big numbers, quizzes and process flows — plain HTML cards with a class.</p>"
      "<p><span class=\"sl-badge\">.sl-steps</span><span class=\"sl-badge\">.sl-compare</span><span class=\"sl-badge\">.sl-stat</span><span class=\"sl-badge\">.sl-quiz</span><span class=\"sl-badge\">.sl-flow</span></p>"
      "</div>",

      "<h2>Deploy a change, safely</h2>"
      "<ol class=\"sl-steps\">"
      "<li>Pull the latest metadata from the sandbox</li>"
      "<li>Run the full test suite locally first</li>"
      "<li>Validate against production — deploy nothing yet</li>"
      "<li>Deploy in a window, with the rollback ready</li>"
      "</ol>",

      "<h2>Triggers, judged</h2>"
      "<div class=\"sl-compare\">"
      "<div class=\"sl-do\"><ul><li>One trigger per object</li><li>Logic in a handler class</li><li>Bulk-safe from line one</li></ul></div>"
      "<div class=\"sl-dont\"><ul><li>SOQL inside loops</li><li>Logic in the trigger body</li><li>A global boolean as a recursion guard</li></ul></div>"
      "</div>",

      "<h2>Why bulk-safety matters</h2>"
      "<div class=\"sl-stats\">"
      "<div class=\"sl-stat\"><b>200</b><span>records per trigger batch</span></div>"
      "<div class=\"sl-stat\"><b>100</b><span>SOQL queries per transaction</span></div>"
      "<div class=\"sl-stat\"><b>1</b><span>query you actually need</span></div>"
      "</div>"
      "<p class=\"sl-foot\">Numbers from the governor limits every org shares.</p>",

      "<h2>Check yourself</h2>"
      "<div class=\"sl-quiz\">"
      "<p class=\"sl-quiz-q\">A trigger queries Contacts inside a for-loop over 200 Accounts. What happens?</p>"
      "<ol><li>Nothing — Salesforce optimises it away</li>"
      "<li>It works in the sandbox, then dies in production</li>"
      "<li>LimitException: Too many SOQL queries — at scale</li></ol>"
      "</div>",

      "<h2>The path every change takes</h2>"
      "<div class=\"sl-flow\"><span>Sandbox</span><span>Tests</span><span>Validate</span><span>Deploy</span><span>Monitor</span></div>"
      "<p class=\"sl-foot\">Same five boxes, whatever the tooling — the kit's .sl-flow draws the arrows.</p>"],
     394)

# #now — a few in-flight things surface on /now (tag any post with
# #now in Admin and it appears there; untag when it ships).
def add_now(slug):
    for p in posts:
        if p["slug"] == slug:
            posts_tags.append({"id": oid(), "post_id": p["id"],
                               "tag_id": tag_ids["now"], "sort_order": 99})
            return
add_now("set-up-an-agentforce-agent-end-to-end")
add_now("your-sandbox-strategy-is-why-deploys-hurt")
add_now("lwc-datatable-plus")

# ════════════════════════════════════════════════════════════════
# EDITOR-CONTROLLED PAGES — every data: page.* the routes
# reference, plus the pages navigation points at. All editable
# in Ghost Admin.
# ════════════════════════════════════════════════════════════════
page("Namaste Salesforce", "home",
     "Hands-on Salesforce courses, training and writing by Swarnil Singhai — from your first login to production.",
     [("About this page", "Supplies the homepage hero copy and metadata via data: page.home.")], 500)
page("The Namaste Blog", "blog",
     "Notes from the ecosystem: releases that matter, decisions explained, careers without the hype.",
     [("About this page", "Supplies the blog hero copy via data: page.blog.")], 500)
page("Courses", "courses",
     "Structured, hands-on tracks. Every course ends with something working in your own org.",
     [("About this page", "Supplies the catalogue hero copy via data: page.courses.")], 500)
page("Video Library", "videos",
     "Standalone walkthroughs — watch one thing get built, start to finish, mistakes left in.",
     [("About this page", "Supplies the video library hero via data: page.videos.")], 500)
page("Slides", "slides",
     "Teaching decks — the whiteboard version of a topic, one idea per slide.",
     [("About this page", "Supplies the slides hero via data: page.slides.")], 500)
page("The Weekly Namaste", "newsletter",
     "One email every Sunday: what changed, what matters, what to try. No sponsors, no filler.",
     [("About this page", "Supplies the newsletter hero via data: page.newsletter.")], 500)
page("Changelog", "changelog",
     "What shipped on this site, newest first.",
     [("About this page", "Supplies the changelog hero via data: page.changelog.")], 500)
page("Resources", "resources",
     "Everything worth your time in one place — books, tools, videos and courses, each with an honest reason it made the list.",
     [("About this page", "Supplies the resources hero via data: page.resources.")], 500)
page("Shop", "shop",
     "Digital things I made and use — playbooks, templates, working notes and this theme.",
     [("About this page", "Supplies the shop hero via data: page.shop.")], 500)
page("Snippets", "snippets",
     "Small pieces of code I reach for again and again — copy, paste, read the gotcha first.",
     [("About this page", "Supplies the snippets hero via data: page.snippets.")], 500)
page("Prompts", "prompts",
     "Prompts I actually reuse — tested on real platform work, with notes on why each line is there.",
     [("About this page", "Supplies the prompts hero via data: page.prompts.")], 500)
page("Projects", "projects",
     "Open-source work: frameworks, components and tooling that run in real orgs — everything here is installable today.",
     [("About this page", "Supplies the projects hero via data: page.projects.")], 500)

page("About", "about",
     "Who makes this, and why it is free.",
     [("The short version",
       "Namaste Salesforce is a hands-on Salesforce learning platform built and written by Swarnil Singhai — 7+ years in IT, learning in public, building first and sharing how."),
      ("The longer version",
       "The best way to learn this platform is to build on it from day one. Every course, module and video here follows that rule: you leave each one having changed something real in your own org.")], 502)
page("Contact", "contact",
     "Questions, corrections, ideas — I read everything.",
     [("Email", "Write to hello@namastesalesforce.com and expect a reply within two working days."),
      ("Corrections", "Spotted something wrong in a lesson? Tell me which page and what you expected — fixes ship weekly.")], 503)
page("Now", "now",
     "What I'm actually working on right now.",
     [("How this page works", "Anything on the site tagged #now shows up here automatically, labelled by what it is — and leaves the moment it ships.")], 504)
page("Products I Use", "products-i-use",
     "Every product, tool and service I actually use to build, teach and ship.",
     [("Hardware", "The desk, the mic, the camera — what I record and build on, with one honest line each."),
      ("Software", "Editors, terminals, design tools and the automations between them."),
      ("Salesforce tooling", "The extensions, CLIs and inspectors open in every working session.")], 505)
page("My Schedule", "my-schedule",
     "When I go live, publish and send — so you know exactly when to look.",
     [("Recurring", "The weekly rhythm above is the promise; changes land in the newsletter first."),
      ("One-off sessions", "Special builds and live deep-dives get announced a week ahead.")], 506,
     lead=[{"type": "html", "version": 1, "html":
            "<table><thead><tr><th>Day</th><th>Time (IST)</th><th>What</th><th>Where</th></tr></thead>"
            "<tbody>"
            "<tr><td>Monday</td><td>9:00 PM</td><td>\U0001F534 Live build stream</td><td>YouTube</td></tr>"
            "<tr><td>Wednesday</td><td>8:00 AM</td><td>New blog post</td><td>/blog/</td></tr>"
            "<tr><td>Friday</td><td>9:00 PM</td><td>New video drops</td><td>/videos/ + YouTube</td></tr>"
            "<tr><td>Sunday</td><td>10:00 AM</td><td>The Weekly Namaste</td><td>Your inbox</td></tr>"
            "</tbody></table>"}])
page("Terms & Conditions", "terms-and-conditions",
     "The short, readable version of what you agree to by using this site.",
     [("Use of content", "Courses and articles are free for personal learning. Republishing requires written permission."),
      ("No warranty", "Content is provided as-is; verify anything critical against official Salesforce documentation."),
      ("Changes", "These terms may change; the date at the top of this page is authoritative.")], 507)
page("Privacy", "privacy",
     "What we collect (very little), and what we do with it (very little).",
     [("What we store", "Your email address if you subscribe, and standard server logs. Nothing else."),
      ("What we never do", "Sell, rent or share your address. Unsubscribing removes it entirely."),
      ("Analytics", "Aggregate page counts only — no cross-site tracking, no fingerprinting.")], 508)
page("Sign the guestbook", "guestbook",
     "Learners from everywhere leave a line here. Add yours.",
     [("Why a guestbook", "This site is read quietly by a lot of people. The guestbook is where the quiet part ends."),
      ("What to write", "Where are you learning from? What are you building? One line is plenty.")], 509)
page("Welcome to Namaste Salesforce", "welcome",
     "Your account is ready. Here are the three best ways to start.",
     [("You made it", "Take a breath — you are in. The cards below are the three best first steps.")], 510)
page("Sponsor us", "sponsor",
     "Put your product in front of people building on Salesforce every week.",
     [("What you get", "A card across the site, a mention in the newsletter, and our genuine thanks."),
      ("What we will not run", "Anything we would not use ourselves. Sponsorship never changes editorial content."),
      ("Get in touch", "Email sponsor@namastesalesforce.com with what you are building.")], 511)

# ════════════════════════════════════════════════════════════════
# THE STYLE GUIDE — /style-guide/: one page exercising every
# Koenig card the editor can produce, in the order an author
# meets them. Images reuse the generated thumbs (real assets).
# ════════════════════════════════════════════════════════════════
def sg_text(t, fmt=0):
    n = text(t); n["format"] = fmt; return n

def sg_quote(t, kind="quote"):
    return {"children": [text(t)], "direction": "ltr", "format": "",
            "indent": 0, "type": kind, "version": 1}

def sg_image(slug, caption, width="regular"):
    return {"type": "image", "version": 1, "src": THUMB.format(slug),
            "width": 1200, "height": 675, "title": "", "alt": caption,
            "caption": caption, "cardWidth": width, "href": ""}

style_guide_nodes = [
    para("Every block the Ghost editor can produce, on one page. "
         "Write with anything below — the theme has it covered."),

    h2("Text"),
    para("Paragraphs carry the reading rhythm. Bold, italics, links and inline code are set inline; everything else on this page is a card."),
    {"children": [sg_text("Bold pulls weight", 1), text(", "), sg_text("italics lean in", 2),
                  text(", and "), sg_text("inline code sits in a chip", 16), text(".")],
     "direction": "ltr", "format": "", "indent": 0, "type": "paragraph", "version": 1},
    ul("Bulleted lists get accent markers",
       "Keep items parallel in shape",
       "Three is a good number"),
    sg_quote("A quote card: one strong sentence beats three careful ones."),
    sg_quote("The alternate quote stands centered, for the line the whole piece hangs on.", "aside"),

    h2("Images"),
    sg_image("admin-foundations", "A regular image sits inside the measure."),
    sg_image("apex-beginners", "A wide image steps out of the column.", "wide"),
    sg_image("flow-mastery", "A full-bleed image owns the viewport.", "full"),
    {"type": "gallery", "version": 1, "caption": "A gallery packs a row.",
     "images": [
        {"row": 0, "fileName": "sf-trigger-framework.svg", "src": THUMB.format("sf-trigger-framework"), "width": 1200, "height": 675},
        {"row": 0, "fileName": "build-a-record-triggered-flow-in-20-minutes.svg", "src": THUMB.format("build-a-record-triggered-flow-in-20-minutes"), "width": 1200, "height": 675},
        {"row": 0, "fileName": "namaste-salesforce-is-live.svg", "src": THUMB.format("namaste-salesforce-is-live"), "width": 1200, "height": 675},
     ]},

    h2("Callouts"),
    {"type": "callout", "version": 1, "calloutEmoji": "💡",
     "calloutText": "The default callout carries a tip worth stopping for.", "backgroundColor": "grey"},
    {"type": "callout", "version": 1, "calloutEmoji": "⚠️",
     "calloutText": "The red callout warns before the step that bites.", "backgroundColor": "red"},
    {"type": "callout", "version": 1, "calloutEmoji": "🚀",
     "calloutText": "The accent callout announces something shipped.", "backgroundColor": "accent"},

    h2("Interactive"),
    {"type": "toggle", "version": 1, "heading": "A toggle hides the long answer",
     "content": "<p>Readers who need the detail open it; everyone else keeps their place. Perfect for FAQs and asides that would break the flow.</p>"},
    {"type": "button", "version": 1, "buttonText": "A button card",
     "alignment": "center", "buttonUrl": "__GHOST_URL__/courses/"},
    {"type": "bookmark", "version": 1, "url": "https://ghost.org/",
     "metadata": {"url": "https://ghost.org/", "title": "Ghost: The best open source blog & newsletter platform",
                  "description": "Beautiful, modern publishing with email newsletters and paid subscriptions built-in.",
                  "author": None, "publisher": "Ghost", "thumbnail": THUMB.format("namaste-salesforce-is-live"),
                  "icon": "https://ghost.org/favicon.ico"}, "caption": ""},

    h2("Media"),
    embed("jNQXAC9IVRw", "An embed card — paste a URL, get a player."),
    codecard("apex",
             "public with sharing class Greeter {\n    public static String greet(String name) {\n        return 'Namaste, ' + name + '!';\n    }\n}",
             "A code card with a language."),
    {"type": "markdown", "version": 1, "markdown":
     "| Helper | Does |\n|---|---|\n| `{{#get}}` | Queries the API |\n| `{{#match}}` | Compares values |\n| `{{#foreach}}` | Iterates with @first/@last |"},
    {"type": "html", "version": 1, "html":
     '<p style="text-align:center"><em>An HTML card renders exactly what you give it.</em></p>'},

    h2("Big furniture"),
    {"type": "header", "version": 2, "size": "small", "style": "dark",
     "backgroundColor": "#032d60", "backgroundImageEnabled": False,
     "textColor": "#FFFFFF", "buttonColor": "#1b96ff", "buttonTextColor": "#FFFFFF",
     "buttonEnabled": True, "buttonText": "Browse courses", "buttonUrl": "__GHOST_URL__/courses/",
     "header": "A header card breaks the page", "subheader": "Use one to open a chapter or close with a call to action.",
     "layout": "wide", "alignment": "center", "swapped": False},
    {"type": "product", "version": 1, "productButtonEnabled": True,
     "productRatingEnabled": True, "productStarRating": 5,
     "productButton": "Start learning", "productUrl": "__GHOST_URL__/courses/",
     "productTitle": "Salesforce Admin Foundations",
     "productDescription": "The product card sells one thing: image, stars, pitch, button.",
     "productImageSrc": THUMB.format("admin-foundations"),
     "productImageWidth": 1200, "productImageHeight": 675},
    {"type": "horizontalrule", "version": 1},
    para("That is the whole vocabulary. If a card renders oddly, fix the theme — never the content."),
]

sg_id = oid(); sg_when = ts(512)
posts.append({
    "id": sg_id, "title": "Style Guide", "slug": "style-guide",
    "lexical": lexical(*style_guide_nodes),
    "feature_image": THUMB.format("style-guide"), "featured": 0,
    "type": "page", "status": "published", "visibility": "public",
    "custom_excerpt": "Every editor card this theme styles, on one page.",
    "created_at": sg_when, "updated_at": sg_when, "published_at": sg_when,
})

# ── settings: navigation with the dropdown convention ───────────
# +Parent opens a pure-CSS dropdown; the -Child run after it are
# its items; the first unprefixed label ends the run.
settings = [
    {"key": "navigation", "value": json.dumps([
        {"label": "Home", "url": "/"},
        {"label": "Courses", "url": "/courses/"},
        {"label": "Training", "url": "/training/"},
        {"label": "+Library", "url": "/resources/"},
        {"label": "-Videos", "url": "/videos/"},
        {"label": "-Slides", "url": "/slides/"},
        {"label": "-Snippets", "url": "/snippets/"},
        {"label": "-Prompts", "url": "/prompts/"},
        {"label": "-Resources", "url": "/resources/"},
        {"label": "-Projects", "url": "/projects/"},
        {"label": "Blog", "url": "/blog/"},
        {"label": "+More", "url": "/sitemap/"},
        {"label": "-Newsletter", "url": "/newsletter/"},
        {"label": "-Changelog", "url": "/changelog/"},
        {"label": "-Shop", "url": "/shop/"},
        {"label": "-About", "url": "/about/"},
    ])},
    {"key": "secondary_navigation", "value": json.dumps([
        {"label": "About", "url": "/about/"},
        {"label": "Contact", "url": "/contact/"},
        {"label": "Sponsor us", "url": "/sponsor/"},
        {"label": "Terms & Conditions", "url": "/terms-and-conditions/"},
        {"label": "Privacy", "url": "/privacy/"},
        {"label": "Sitemap", "url": "/sitemap/"},
    ])},
]

doc = {"db": [{
    "meta": {"exported_on": int(START.timestamp() * 1000), "version": "6.0.0"},
    "data": {"posts": posts, "tags": tags, "posts_tags": posts_tags, "settings": settings},
}]}

with open(__file__.replace('build-import.py', 'import.json'), 'w') as f:
    json.dump(doc, f, indent=2)

n_posts = sum(1 for p in posts if p["type"] == "post")
n_pages = sum(1 for p in posts if p["type"] == "page")
print(f"import.json: {n_posts} posts + {n_pages} pages, {len(tags)} tags, {len(posts_tags)} mappings")
