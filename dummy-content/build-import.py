#!/usr/bin/env python3
"""Generates dummy-content/import.json — a Ghost importable data set
that exercises every feature of the theme:

  · a course (advanced, 3h) with all four lesson types
  · four more small courses, one per #course-layout-* variant
    (the flagship keeps the classic default)
  · lesson layout variants spread across the flagship's lessons
    (#lesson-layout-cinema / -focus / -right; -wide lives in the
    Apex course; the first lesson keeps the classic default)
  · two training modules with three pages each
  · five blog posts, one per layout, plus sidebar/TOC variants
  · every internal facet tag WITH its description (chips read
    descriptions, never slugs)
  · navigation settings including the dropdown convention
    (+Learn / -Courses / -Training)

Import in Ghost Admin → Settings → Import/Export, or POST to
/ghost/api/admin/db/. Slugs are all new — safe beside existing
content. The importer dedupes tags by slug.
"""
import json, secrets, datetime

BASE = datetime.datetime(2026, 8, 1, 9, 0, 0)

def oid():
    return secrets.token_hex(12)

def ts(offset_hours):
    return (BASE + datetime.timedelta(hours=offset_hours)).strftime('%Y-%m-%dT%H:%M:%S.000Z')

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

def lexical(*nodes):
    return json.dumps({"root": {"children": list(nodes), "direction": "ltr", "format": "", "indent": 0, "type": "root", "version": 1}})

def body(subject, sections):
    """A believable article: intro, then h2 sections with copy."""
    nodes = [para(f"{subject} This page is demo content generated for the theme — replace it with the real thing, keep the tags.")]
    for heading, copy in sections:
        nodes.append(h2(heading))
        nodes.append(para(copy))
    nodes.append(h2("Try it yourself"))
    nodes.append(ul(
        "Open your Developer Edition org and follow along",
        "Change one thing at a time and note what happens",
        "When something breaks, read the error before searching it",
    ))
    return lexical(*nodes)

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

# collections (new vocabulary)
tag("#course-col", "course-col", "Marks a post as a course landing page")
tag("#lesson-col", "lesson-col", "Marks a post as a course lesson")
tag("#training-col", "training-col", "Marks a post as a training module page")
tag("#blog-col", "blog-col", "Marks a post as a blog article")

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
    tag(f"#duration-{m}m", f"duration-{m}m", f"{m}m")
for h, mins in [(1, 0), (1, 15), (1, 30), (1, 45), (2, 0), (2, 30),
                (3, 0), (4, 0), (5, 0), (6, 0)]:
    slug = f"duration-{h}h" + (f"-{mins}m" if mins else "")
    label = f"{h}h" + (f" {mins}m" if mins else "")
    tag(f"#{slug}", slug, label)
tag("#lesson-type-video", "lesson-type-video", "Video lesson")
tag("#video-preview", "video-preview", "Cards play this post's video as a muted preview")
tag("#lesson-type-audio", "lesson-type-audio", "Audio lesson")
tag("#lesson-type-quiz", "lesson-type-quiz", "Quiz")

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

tag("#video-col", "video-col", "Marks a post as a library video")
tag("#newsletter-col", "newsletter-col", "Marks a post as a newsletter issue")
tag("#changelog-col", "changelog-col", "Marks a post as a changelog entry")

# changelog entry types — the badge on /changelog and the entry
# header. The description IS the badge text; the slug suffix is
# the colour class (templates match hash-changelog-type-).
tag("#changelog-type-feature", "changelog-type-feature", "Feature")
tag("#changelog-type-improvement", "changelog-type-improvement", "Improvement")
tag("#changelog-type-fix", "changelog-type-fix", "Fix")
tag("#changelog-type-content", "changelog-type-content", "Content")

# public: the course's own tag, module tags, topics
tag("Flow Automation Masterclass", "flow-automation-masterclass",
    "Everything about Flow, from trigger order to error handling.", "public")
tag("Deployment Basics", "deployment-basics",
    "Ship changes between orgs without fear: metadata, tooling, checklists.", "public")
tag("Security Essentials", "security-essentials",
    "Who sees what, and why — profiles, permission sets, sharing.", "public")
tag("Automation", "automation", "Flows, triggers and the order they run in.", "public")
tag("Architecture", "architecture", "Data models and decisions that age well.", "public")

# ── posts ───────────────────────────────────────────────────────
posts, posts_tags = [], []

def post(title, slug, tag_slugs, excerpt, sections, hours,
         featured=False, lead=None, kind="post"):
    """Feature images are intentionally ABSENT: after importing, run
    dummy-content/build-thumbnails.py — it draws a theme-styled SVG
    per post and repoints feature_image at it."""
    pid = oid()
    when = ts(hours)
    nodes = list(lead) if lead else []
    doc = json.loads(body(excerpt, sections))
    doc["root"]["children"] = nodes + doc["root"]["children"]
    posts.append({
        "id": pid, "title": title, "slug": slug,
        "lexical": json.dumps(doc),
        "feature_image": None,
        "featured": 1 if featured else 0,
        "type": kind, "status": "published", "visibility": "public",
        "custom_excerpt": excerpt,
        "created_at": when, "updated_at": when, "published_at": when,
    })
    for order, ts_slug in enumerate(tag_slugs):
        posts_tags.append({"id": oid(), "post_id": pid,
                           "tag_id": tag_ids[ts_slug], "sort_order": order})

def page(title, slug, excerpt, sections, hours):
    post(title, slug, [], excerpt, sections, hours, kind="page")

# THE COURSE — slug equals its public tag's slug; lessons carry
# that tag FIRST (primary), which is the whole nesting mechanism.
post("Flow Automation Masterclass", "flow-automation-masterclass",
     ["flow-automation-masterclass", "course-col", "course-level-advanced", "duration-3h"],
     "Stop writing triggers for things Flow does better — and learn where Flow stops being the answer.",
     [("What this course covers", "Record-triggered flows, scheduled paths, error handling, and the limits you will hit in real orgs."),
      ("Who it is for", "Admins and developers who already build basic flows and want to trust them in production.")],
     0, featured=True)

lessons = [
    # lesson 1 keeps the classic layout; the rest each demo one
    # #lesson-layout-* variant (-wide lives in the Apex course)
    ("Planning your flow before you build", "planning-your-flow-before-you-build",
     ["duration-15m"], "Five questions that prevent ninety percent of flow rewrites."),
    ("Record-triggered flows in practice", "record-triggered-flows-in-practice",
     ["lesson-type-video", "duration-30m", "lesson-layout-cinema"], "Build one alongside the video: entry criteria, paths, and a safe update."),
    ("Flow error handling patterns", "flow-error-handling-patterns",
     ["lesson-type-audio", "duration-15m", "lesson-layout-focus"], "Fault paths, platform events, and what to tell the user when it breaks."),
    ("Check your understanding: flows", "check-your-understanding-flows",
     ["lesson-type-quiz", "duration-10m", "lesson-layout-right"], "Ten scenarios. Decide: flow, trigger, or neither."),
]
for i, (title, slug, extra, excerpt) in enumerate(lessons):
    lead = [embed("aqz-KE-bpKQ")] if "lesson-type-video" in extra else None
    post(title, slug, ["flow-automation-masterclass", "lesson-col"] + extra, excerpt,
         [("The idea", "One concept per lesson, applied immediately in your own org."),
          ("Watch out for", "The mistake everyone makes at this step, and how to notice it early.")],
         1 + i, lead=lead)

# FOUR MORE COURSES — one per #course-layout-* variant (the
# flagship above keeps the classic default). Same mechanism:
# public tag slug == course slug, lessons carry that tag first.
more_courses = [
    ("Apex Fundamentals", "apex-fundamentals", ["course-layout-cinema", "course-curriculum-cards"],
     "course-level-intermediate", "duration-2h",
     "Classes, triggers and governor limits — the parts of Apex you will actually write.",
     [("Set up once, run anywhere", "A scratch org, the CLI, and a test class before your first trigger."),
      ("Limits are the language", "Why every Apex decision is really a governor-limit decision.")],
     [("Your first Apex class", "your-first-apex-class",
       ["duration-20m", "lesson-layout-wide"],
       "Write, deploy and test a class in twenty minutes."),
      ("Triggers without tears", "triggers-without-tears",
       ["duration-25m"],
       "One trigger per object, logic in a handler, and why.")]),
    ("Reports and Dashboards Crash Course", "reports-dashboards-crash-course", ["course-layout-minimal", "course-curriculum-compact"],
     "course-level-beginner", "duration-1h",
     "From a blank report to a dashboard your manager actually opens.",
     [("Report types decide everything", "Pick the wrong one and no filter will save you."),
      ("Dashboards are for questions", "Every widget should answer one question someone really asks.")],
     [("Building your first report", "building-your-first-report",
       ["duration-15m"],
       "Rows, columns, filters — and the preview trap."),
      ("Dashboards that get opened", "dashboards-that-get-opened",
       ["duration-15m"],
       "Three widgets, one audience, zero clutter.")]),
    ("Data Modeling Deep Dive", "data-modeling-deep-dive", ["course-layout-billboard", "course-curriculum-timeline"],
     "course-level-intermediate", "duration-2h-30m",
     "Objects, relationships and the decisions you cannot cheaply undo.",
     [("Lookup or master-detail", "The one relationship choice that follows you forever."),
      ("Fields are cheap, objects are not", "When a picklist beats a child object, and when it does not.")],
     [("Choosing the right relationship", "choosing-the-right-relationship",
       ["duration-20m"],
       "Lookup, master-detail, junction — decided with three questions."),
      ("Record types without regret", "record-types-without-regret",
       ["duration-20m"],
       "What record types are for, and the three signs you have too many.")]),
    ("Integration Patterns", "integration-patterns", ["course-layout-boxed", "course-curriculum-checklist"],
     "course-level-advanced", "duration-3h",
     "REST, platform events and middleware — moving data without losing it.",
     [("Sync or async", "The latency question that picks your pattern for you."),
      ("Idempotency first", "Design every integration to survive being run twice.")],
     [("Calling out with REST", "calling-out-with-rest",
       ["duration-25m"],
       "Named credentials, callouts and the test mock you need."),
      ("Platform events in practice", "platform-events-in-practice",
       ["duration-25m"],
       "Publish, subscribe, replay — and when a flow is the subscriber.")]),
]
ch = 80
for name, cslug, styles, level, duration, excerpt, sections, course_lessons in more_courses:
    tag(name, cslug, excerpt, "public")
    post(name, cslug, [cslug, "course-col"] + styles + [level, duration],
         excerpt, sections, ch)
    ch += 1
    for ltitle, lslug, extra, lexcerpt in course_lessons:
        post(ltitle, lslug, [cslug, "lesson-col"] + extra, lexcerpt,
             [("The idea", "One concept per lesson, applied immediately in your own org."),
              ("Watch out for", "The mistake everyone makes at this step, and how to notice it early.")],
             ch)
        ch += 1

# TRAINING — the module IS the primary tag; pages in publish order.
modules = {
    "deployment-basics": [
        ("What counts as metadata", "what-counts-as-metadata",
         "Fields yes, records no — mostly. The line that decides what deploys."),
        ("Change sets versus SFDX", "change-sets-versus-sfdx",
         "Both move metadata. One of them tells you what went wrong."),
        ("Your first deployment checklist", "your-first-deployment-checklist",
         "The eight checks that make Friday deploys boring."),
    ],
    "security-essentials": [
        ("Profiles and permission sets", "profiles-and-permission-sets",
         "One baseline profile, everything else in permission sets. Here is why."),
        ("Sharing rules explained", "sharing-rules-explained",
         "Org-wide defaults set the floor; sharing opens doors on purpose."),
        ("Field-level security audits", "field-level-security-audits",
         "Finding the fields everyone can see and nobody should."),
    ],
}
h = 10
for module, pages in modules.items():
    for title, slug, excerpt in pages:
        post(title, slug, [module, "training-col", "duration-10m"], excerpt,
             [("The rule", "State the convention plainly, then show the one exception worth knowing."),
              ("In practice", "What this looks like in a real org with real users mid-quarter.")],
             h)
        h += 1

# BLOG — one post per layout, plus sidebar/TOC variants.
blog = [
    ("Why every admin should learn SOQL", "why-every-admin-should-learn-soql",
     ["blog-col", "automation"],  # classic, right sidebar, TOC on
     "Reports answer questions someone predicted. SOQL answers yours."),
    ("The state of Salesforce careers in 2026", "state-of-salesforce-careers-2026",
     ["blog-col", "automation", "blog-layout-magazine"],
     "Hiring cooled, expectations rose, and the interesting roles moved sideways."),
    ("Ten releases in, what we learned", "ten-releases-in-what-we-learned",
     ["blog-col", "architecture", "blog-layout-minimal", "blog-sidebar-left"],
     "A retrospective on shipping with every Salesforce release since we started."),
    ("Data model reviews that pay off", "data-model-reviews-that-pay-off",
     ["blog-col", "architecture", "blog-layout-split"],
     "An hour of review before the first field beats a quarter of migration after."),
    ("A field guide to sandbox strategies", "field-guide-to-sandbox-strategies",
     ["blog-col", "architecture", "blog-layout-wide", "blog-toc-hide"],
     "Developer, partial, full — and the refresh schedule nobody writes down."),
]
for i, (title, slug, tag_slugs, excerpt) in enumerate(blog):
    post(title, slug, tag_slugs, excerpt,
         [("Where this starts", "The situation as we actually found it, before any best practice applied."),
          ("What changed", "The decision, the trade-off it carried, and the number that moved."),
          ("What we would do differently", "Honest hindsight — the part most write-ups leave out.")],
         20 + i)

# A video walkthrough inside a training module — proves the rail's
# type icons work for training too.
post("Watch: a deployment end to end", "watch-a-deployment-end-to-end",
     ["deployment-basics", "training-col", "lesson-type-video", "duration-15m"],
     "Fifteen minutes from git push to a green deployment, narrated.",
     [("Follow along", "Pause after each step and run the same command in your own project.")],
     16, lead=[embed("aqz-KE-bpKQ")])

# THE VIDEO LIBRARY — standalone videos at /videos/{slug}/.
videos = [
    ("Salesforce in five minutes", "salesforce-in-five-minutes", "jNQXAC9IVRw",
     "The whole platform, one whiteboard, five minutes."),
    ("Data model walkthrough", "data-model-walkthrough", "aqz-KE-bpKQ",
     "Objects, fields and relationships drawn live, with the mistakes left in."),
    ("Debugging a failed flow", "debugging-a-failed-flow", "9bZkp7q19f0",
     "A real flow error, found and fixed on screen."),
    ("Sandbox seeding in practice", "sandbox-seeding-in-practice", "kJQP7kiw5Fk",
     "Getting believable data into a fresh sandbox without a licence."),
]
CHAPTERS = {"type": "markdown", "version": 1, "markdown": (
    "| Time | Chapter |\n|---|---|\n"
    "| 0:00 | Introduction |\n"
    "| 0:45 | The setup |\n"
    "| 2:10 | Building it live |\n"
    "| 3:30 | Where it breaks |\n"
    "| 4:20 | Wrap-up and next steps |")}

video_durations = ["duration-5m", "duration-10m", "duration-15m", "duration-20m"]
for i, (title, slug, vid, excerpt) in enumerate(videos):
    # the first two demo the card video preview (#video-preview)
    preview = ["video-preview"] if i < 2 else []
    post(title, slug, ["video-col", "automation", video_durations[i]] + preview, excerpt,
         [("What you will see", "Screen and narration only — no slides, no intro music."),
          ("Mentioned in this video", "Links and docs referenced on screen, collected for later.")],
         30 + i, lead=[embed(vid), CHAPTERS])

# THE NEWSLETTER — issues at /newsletter/{slug}/.
issues = [
    ("The Weekly Namaste #3 — Flows eat triggers", "weekly-namaste-3",
     "Record-triggered flows keep absorbing trigger use cases. Where the line sits this release."),
    ("The Weekly Namaste #2 — Sandboxes on a budget", "weekly-namaste-2",
     "Partial copies, seeding scripts, and when a Developer Edition is honestly enough."),
    ("The Weekly Namaste #1 — Hello, world", "weekly-namaste-1",
     "Why this newsletter exists and what lands in your inbox every week."),
]
# issues[] lists newest FIRST; publish times must run the other
# way so the newest issue really is the latest.
for i, (title, slug, excerpt) in enumerate(issues):
    post(title, slug, ["newsletter-col"], excerpt,
         [("This week", "The three things worth your attention, each in two sentences."),
          ("Worth a click", "One link we kept coming back to."),
          ("From the courses", "What changed in the curriculum since last issue.")],
         40 + (len(issues) - i))

# THE CHANGELOG — entries at /changelog/{slug}/. Each carries a
# #changelog-type-* tag: the colour-coded badge on the timeline.
changes = [
    ("Video library launched", "video-library-launched",
     "A new home for standalone walkthroughs, outside any course.",
     "changelog-type-feature"),
    ("Training modules get a full sidebar", "training-modules-full-sidebar",
     "Every module now one click away from any training page.",
     "changelog-type-improvement"),
    ("Course filters shipped", "course-filters-shipped",
     "Filter the catalogue by level and duration.",
     "changelog-type-feature"),
    ("Namaste Salesforce is live", "namaste-salesforce-is-live",
     "First public release: two courses, two modules, and a blog.",
     "changelog-type-content"),
]
for i, (title, slug, excerpt, ctype) in enumerate(changes):
    post(title, slug, ["changelog-col", ctype], excerpt,
         [("What changed", "The user-visible difference, stated without ceremony."),
          ("Why", "The problem this solves, in one honest paragraph.")],
         50 + i)

# EDITOR-CONTROLLED PAGES — everything the routes and the More
# dropdown point at. All plain pages, all editable in Ghost Admin.
page("Namaste Salesforce", "home",
     "Hands-on Salesforce courses, training and writing — from your first login to production.",
     [("About this page", "Supplies the homepage hero copy and metadata via data: page.home.")], 60)
page("The Namaste Blog", "blog",
     "Notes from the ecosystem: releases that matter, decisions explained, careers without the hype.",
     [("About this page", "Supplies the blog hero copy via data: page.blog.")], 61)
page("Courses", "courses",
     "Structured, hands-on tracks. Every course ends with something working in your own org.",
     [("About this page", "Supplies the catalogue hero copy via data: page.courses.")], 62)
page("Video Library", "videos",
     "Standalone walkthroughs — watch one thing get built, start to finish.",
     [("About this page", "Supplies the video library hero via data: page.videos.")], 63)
page("The Weekly Namaste", "newsletter",
     "One email a week: what changed, what matters, what to try. No spam, ever.",
     [("About this page", "Supplies the newsletter hero via data: page.newsletter.")], 64)
page("Changelog", "changelog",
     "What shipped on this site, newest first.",
     [("About this page", "Supplies the changelog hero via data: page.changelog.")], 65)
page("About", "about",
     "Who makes this, and why it is free.",
     [("The short version", "Namaste Salesforce is a hands-on learning platform for the Salesforce ecosystem, built and written by practitioners."),
      ("The longer version", "We believe the best way to learn the platform is to build on it from day one — every course, module and video here follows that rule.")], 66)
page("Contact", "contact",
     "Questions, corrections, ideas — we read everything.",
     [("Email", "Write to hello@namastesalesforce.com and expect a reply within two working days."),
      ("Corrections", "Spotted something wrong in a lesson? Tell us which page and what you expected — fixes ship weekly.")], 67)
page("Terms & Conditions", "terms-and-conditions",
     "The short, readable version of what you agree to by using this site.",
     [("Use of content", "Courses and articles are free for personal learning. Republishing requires written permission."),
      ("No warranty", "Content is provided as-is; verify anything critical against official Salesforce documentation."),
      ("Changes", "These terms may change; the date at the top of this page is authoritative.")], 68)
page("Privacy", "privacy",
     "What we collect (very little), and what we do with it (very little).",
     [("What we store", "Your email address if you subscribe, and standard server logs. Nothing else."),
      ("What we never do", "Sell, rent or share your address. Unsubscribing removes it entirely."),
      ("Analytics", "Aggregate page counts only — no cross-site tracking, no fingerprinting.")], 69)
page("Sign the guestbook", "guestbook",
     "Learners from everywhere leave a line here. Add yours.",
     [("Why a guestbook", "This site is read quietly by a lot of people. The guestbook is where the quiet part ends."),
      ("What to write", "Where are you learning from? What are you building? One line is plenty.")], 71)
page("Welcome to Namaste Salesforce", "welcome",
     "Your account is ready. Here are the three best ways to start.",
     [("You made it", "Take a breath — you are in. The cards below are the three best first steps.")], 72)
page("Sponsor us", "sponsor",
     "Put your product in front of people building on Salesforce every week.",
     [("What you get", "A card across the site, a mention in the newsletter, and our genuine thanks."),
      ("What we will not run", "Anything we would not use ourselves. Sponsorship never changes editorial content."),
      ("Get in touch", "Email sponsor@namastesalesforce.com with what you are building.")], 70)

# THE STYLE GUIDE — /style-guide/: one page exercising every
# Koenig card the editor can produce, in the order an author
# meets them. Images reuse the generated thumbs (real assets).
def sg_text(t, fmt=0):
    n = text(t); n["format"] = fmt; return n

def sg_quote(t, kind="quote"):
    return {"children": [text(t)], "direction": "ltr", "format": "",
            "indent": 0, "type": kind, "version": 1}

THUMB = "__GHOST_URL__/assets/images/thumbs/{}.svg"

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
    sg_image("apex-fundamentals", "A regular image sits inside the measure."),
    sg_image("data-modeling-deep-dive", "A wide image steps out of the column.", "wide"),
    sg_image("integration-patterns", "A full-bleed image owns the viewport.", "full"),
    {"type": "gallery", "version": 1, "caption": "A gallery packs a row.",
     "images": [
        {"row": 0, "fileName": "flow-automation-masterclass.svg", "src": THUMB.format("flow-automation-masterclass"), "width": 1200, "height": 675},
        {"row": 0, "fileName": "reports-dashboards-crash-course.svg", "src": THUMB.format("reports-dashboards-crash-course"), "width": 1200, "height": 675},
        {"row": 0, "fileName": "salesforce-in-five-minutes.svg", "src": THUMB.format("salesforce-in-five-minutes"), "width": 1200, "height": 675},
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
    {"type": "codeblock", "version": 1, "language": "apex", "caption": "A code card with a language.",
     "code": "public with sharing class Greeter {\n    public static String greet(String name) {\n        return 'Namaste, ' + name + '!';\n    }\n}"},
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
     "productTitle": "Flow Automation Masterclass",
     "productDescription": "The product card sells one thing: image, stars, pitch, button.",
     "productImageSrc": THUMB.format("flow-automation-masterclass"),
     "productImageWidth": 1200, "productImageHeight": 675},
    {"type": "horizontalrule", "version": 1},
    para("That is the whole vocabulary. If a card renders oddly, fix the theme — never the content."),
]

sg_id = oid(); sg_when = ts(74)
posts.append({
    "id": sg_id, "title": "Style Guide", "slug": "style-guide",
    "lexical": lexical(*style_guide_nodes),
    "feature_image": None, "featured": 0,
    "type": "page", "status": "published", "visibility": "public",
    "custom_excerpt": "Every editor card this theme styles, on one page.",
    "created_at": sg_when, "updated_at": sg_when, "published_at": sg_when,
})

# ── settings: navigation with the dropdown convention ───────────
settings = [
    {"key": "navigation", "value": json.dumps([
        {"label": "Home", "url": "/"},
        {"label": "Courses", "url": "/courses/"},
        {"label": "Training", "url": "/training/"},
        {"label": "Videos", "url": "/videos/"},
        {"label": "Blog", "url": "/blog/"},
        {"label": "+More", "url": "/sitemap/"},
        {"label": "-Newsletter", "url": "/newsletter/"},
        {"label": "-Changelog", "url": "/changelog/"},
        {"label": "-Sponsor us", "url": "/sponsor/"},
        {"label": "-Start project", "url": "https://github.com/imswarnil"},
        {"label": "-Sitemap", "url": "/sitemap/"},
        {"label": "-Guestbook", "url": "/guestbook/"},
        {"label": "-Contact", "url": "/contact/"},
        {"label": "-Terms & Conditions", "url": "/terms-and-conditions/"},
        {"label": "-Privacy", "url": "/privacy/"},
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
    "meta": {"exported_on": int(BASE.timestamp() * 1000), "version": "6.0.0"},
    "data": {"posts": posts, "tags": tags, "posts_tags": posts_tags, "settings": settings},
}]}

with open(__file__.replace('build-import.py', 'import.json'), 'w') as f:
    json.dump(doc, f, indent=2)

print(f"import.json: {len(posts)} posts, {len(tags)} tags, {len(posts_tags)} mappings")
