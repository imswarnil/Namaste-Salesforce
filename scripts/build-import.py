#!/usr/bin/env python3
"""Build dummy-content/import.json — the seed fixture.

This is a FIXTURE GENERATOR, not source material. Regenerating is cheap, and a
stale fixture that no longer matches the templates is worse than none — so the
generator is what is version-controlled and the JSON is an artefact of it.
See abstract/14.

    python3 scripts/build-import.py

Then, IN THIS ORDER — step 1 before step 2, always:
    1. Ghost Admin → Settings → Labs → Routes  → upload routes.yaml
    2. Ghost Admin → Settings → Labs → Import  → dummy-content/import.json

Without routes.yaml the collections do not exist, the posts import with no
URLs, and every page looks broken for reasons that have nothing to do with the
theme.

── The three things that make or break the import (abstract/14) ─────────────

1. `sort_order: 0` IS THE PRIMARY TAG. Ghost has no primary_tag column. For a
   CHILD — a lesson, a docs page — sort_order 0 must be its PARENT's tag, not
   a tag of its own. That inheritance is what makes /courses/{course}/{slug}/
   nest.

2. INTERNAL TAGS ARE WRITTEN `hash-*` HERE, never `#*`. In a template you
   write `#course`; in a filter string and in this file you write `hash-`.

3. A PARENT POST'S SLUG MUST EQUAL ITS OWN TAG'S SLUG. The permalink uses
   {slug} rather than {primary_tag}, because a parent shares its tag with all
   of its children. There is an assertion for this at the bottom, and it has
   to pass before the file is written.
"""

import json, hashlib, pathlib, sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import lexical as L
import bodies
import styleguide

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "dummy-content" / "import.json"
MEDIA = "/assets/media"

def oid(kind, key):
    """Deterministic 24-hex id — deterministic so regenerating does not churn
    every id and make the diff unreadable."""
    return hashlib.sha1(f"{kind}:{key}".encode()).hexdigest()[:24]

BASE = datetime(2026, 1, 6, 9, 0, tzinfo=timezone.utc)
def when(days):
    """Spaced-out dates. Identical timestamps make ordering arbitrary and
    prev/next behave differently on every import (abstract/14 § Ordering)."""
    return (BASE + timedelta(days=days, hours=(days % 7))).strftime("%Y-%m-%dT%H:%M:%S.000Z")

# Bodies come from scripts/bodies.py — one per post where the content matters,
# a short stub otherwise. The first fixture gave every post the SAME three
# paragraphs, and that hid every bug worth finding: a table of contents built
# from two identical headings looks fine, and no card ever tested a long title
# against a short one. A fixture whose rows are all alike only proves the
# template renders once.

TAGS, POSTS, JOINS = [], [], []

def tag(name, slug, description="", visibility="public"):
    t = {"id": oid("tag", slug), "name": name, "slug": slug,
         "description": description, "visibility": visibility}
    TAGS.append(t)
    return t

def internal(name, slug, description=""):
    """An internal tag's NAME carries the # and its SLUG carries hash-."""
    return tag(name, slug, description, "internal")

def post(slug, title, excerpt, tags_in_order, *, day, image=None, type_="post",
         visibility="public", featured=False, body=None):
    """tags_in_order[0] becomes sort_order 0 — the primary tag. That IS the
    URL model, so the order of this list is load-bearing."""
    pid = oid("post", slug)
    POSTS.append({
        "id": pid, "title": title, "slug": slug,
        "lexical": body or bodies.get(slug, excerpt),
        "status": "published", "type": type_, "visibility": visibility,
        "featured": featured,
        "feature_image": f"{MEDIA}/{image}.png" if image else None,
        "custom_excerpt": excerpt,
        "created_at": when(day), "published_at": when(day), "updated_at": when(day),
    })
    for i, t in enumerate(tags_in_order):
        JOINS.append({"post_id": pid, "tag_id": t["id"], "sort_order": i})
    return pid

# ══ STRUCTURAL TAGS — what a post IS (abstract/18) ══════════════════════════
S = {k: internal(f"#{k}", f"hash-{k}") for k in [
    "course", "lesson", "training-module", "training-lesson",
    "docs-section", "docs-page", "blog", "resource", "product"]}

# ══ FACET TAGS — what a post is ABOUT or FOR ═══════════════════════════════
LEVEL = {k: internal(f"#level-{k}", f"hash-level-{k}", k.capitalize())
         for k in ["beginner", "intermediate", "advanced"]}

# Duration. THE TAG'S DESCRIPTION CARRIES THE DISPLAY TEXT — that is what lets
# an author set a duration in Ghost Admin without touching the theme
# (abstract/02). Minutes are 5-minute multiples; an hours-and-minutes value
# separates the units with a hyphen so the slug stays #prefix-value and stays
# readable: #duration-1h-5m is one hour five minutes.
DUR = {v: internal(f"#duration-{v}", f"hash-duration-{v}", label) for v, label in [
    ("5m", "5m"), ("10m", "10m"), ("15m", "15m"), ("20m", "20m"), ("25m", "25m"),
    ("30m", "30m"), ("45m", "45m"), ("1h", "1h"), ("1h-5m", "1h 5m"),
    ("1h-30m", "1h 30m"), ("2h", "2h"), ("2h-15m", "2h 15m"), ("3h", "3h"),
    ("6h-20m", "6h 20m"),
]}

FORMAT = {k: internal(f"#format-{k}", f"hash-format-{k}", k.capitalize())
          for k in ["video", "article", "exercise", "quiz"]}
ACCESS = {k: internal(f"#{k}", f"hash-{k}") for k in ["free", "paid", "preview"]}
CERT = {k: internal(f"#cert-{k}", f"hash-cert-{k}", d) for k, d in
        [("admin", "Salesforce Administrator"), ("pd1", "Platform Developer I")]}
PREREQ = internal("#prereq-apex-basics", "hash-prereq-apex-basics",
                  "You can read a class and a method")
SERIES = internal("#series-apex-perf", "hash-series-apex-perf", "Apex performance")
HERO = {n: internal(f"#hero-{n}", f"hash-hero-{n}") for n in (1, 2, 3)}
RTYPE = {k: internal(f"#resource-type-{k}", f"hash-resource-type-{k}", k.capitalize())
         for k in ["book", "tool", "website"]}

# ══ PUBLIC TOPIC TAGS — what a reader browses. Under 20 (abstract/18) ══════
TOPIC = {s: tag(n, s, d) for s, n, d in [
    ("apex", "Apex", "Salesforce's server-side language."),
    ("flow", "Flow", "Declarative automation."),
    ("lwc", "Lightning Web Components", "The modern component framework."),
    ("security", "Security", "Sharing, permissions and the security model."),
    ("data-modelling", "Data modelling", "Objects, fields and relationships."),
    ("integration", "Integration", "APIs, events and external systems."),
]}

# ══ PARENT TAGS ════════════════════════════════════════════════════════════
# A parent's tag is PUBLIC, and its slug is the parent post's slug. These are
# deliberately distinct from the topic tags above: if a course tag were also
# `apex`, every post about Apex would become a lesson of that course.
COURSE = {s: tag(n, s, d) for s, n, d in [
    ("admin-foundations", "Admin Foundations", "The administrator's first ninety days."),
    ("apex-masterclass", "Apex Masterclass", "Write Apex that survives 200 records and a code review."),
    ("lwc-essentials", "LWC Essentials", "Build, test and ship a Lightning Web Component."),
    ("integration-patterns", "Integration Patterns", "Choosing between the seven integration patterns."),
]}
MODULE = {s: tag(n, s, d) for s, n, d in [
    ("start", "Start", "Get oriented and set up."),
    ("build", "Build", "Model the data and build the screens."),
    ("automate", "Automate", "Make the org do the work."),
]}
DOCS = {s: tag(n, s, d) for s, n, d in [
    ("getting-started", "Getting started", "Install, configure and publish."),
    ("configuration", "Configuration", "Every setting, and what it changes."),
    ("troubleshooting", "Troubleshooting", "When something is not working."),
]}

# ══ CONTENT ════════════════════════════════════════════════════════════════
# Coverage rules (abstract/14): two of a thing proves it renders, three proves
# the LIST renders. So ≥3 per collection, plus at least one of every STATE —
# members-only, preview, featured, no feature image, and a parent with no
# children — because the empty and locked paths are where the bugs hide.

d = 0
def nxt():
    global d
    d += 3
    return d

# ── Courses ────────────────────────────────────────────────────────────────
# The parent's slug == its own tag's slug, and its own tag is sort_order 0.
COURSE_LESSONS = {
    "admin-foundations": [
        ("objects-and-fields", "Objects, fields and relationships", "The data model is the product. Get this right and everything after it is easier.", DUR["25m"], LEVEL["beginner"], TOPIC["data-modelling"], FORMAT["article"]),
        ("permissions-that-scale", "Permissions that scale", "Profiles, permission sets and the one rule that keeps them from multiplying.", DUR["30m"], LEVEL["beginner"], TOPIC["security"], FORMAT["article"]),
        ("reports-people-read", "Reports people actually read", "A report nobody opens is a report that does not exist.", DUR["20m"], LEVEL["beginner"], TOPIC["data-modelling"], FORMAT["video"]),
    ],
    "apex-masterclass": [
        ("bulkify-or-die", "Bulkify, or die at 201 records", "The single mistake that fails more code reviews than every other combined.", DUR["45m"], LEVEL["intermediate"], TOPIC["apex"], FORMAT["article"]),
        ("governor-limits", "Governor limits, and how to stop fearing them", "They are a budget, not a punishment. Here is how to read the bill.", DUR["1h-5m"], LEVEL["intermediate"], TOPIC["apex"], FORMAT["article"]),
        ("testing-apex-properly", "Testing Apex properly", "75% coverage is a floor nobody should be proud of clearing.", DUR["1h-30m"], LEVEL["advanced"], TOPIC["apex"], FORMAT["exercise"]),
    ],
    "lwc-essentials": [
        ("your-first-component", "Your first component", "Three files, one decorator, and something on the screen in ten minutes.", DUR["15m"], LEVEL["beginner"], TOPIC["lwc"], FORMAT["video"]),
        ("wire-and-imperative", "@wire, and when not to use it", "The reactive one is not always the right one.", DUR["30m"], LEVEL["intermediate"], TOPIC["lwc"], FORMAT["article"]),
        ("component-communication", "Talking between components", "Events up, properties down, and the message channel for everything else.", DUR["45m"], LEVEL["intermediate"], TOPIC["lwc"], FORMAT["article"]),
    ],
}
for slug, ct in COURSE.items():
    lessons = COURSE_LESSONS.get(slug, [])
    hero = HERO[(len(lessons) % 3) + 1]
    post(slug, ct["name"], ct["description"],
         # sort_order 0 is the course's OWN tag — that is what the course URL
         # and every lesson underneath it hang off.
         [ct, S["course"], LEVEL["beginner"] if slug != "apex-masterclass" else LEVEL["intermediate"],
          DUR["3h"] if lessons else DUR["1h"], hero, ACCESS["free"]],
         day=nxt(), image=f"course-{slug}")

    for i, (lslug, title, exc, dur, lvl, topic, fmt) in enumerate(lessons):
        # A lesson that is members-only, one that is a free preview, and one
        # with no feature image — the three states worth proving.
        vis = "members" if (slug == "apex-masterclass" and i == 2) else "public"
        extra = [ACCESS["preview"]] if (slug == "apex-masterclass" and i == 0) else []
        if slug == "apex-masterclass":
            extra += [SERIES, CERT["pd1"], PREREQ]
        if slug == "admin-foundations":
            extra += [CERT["admin"]]
        post(lslug, title, exc,
             # sort_order 0 is the COURSE's tag, not the lesson's own — the
             # inheritance that makes /courses/{course}/{lesson}/ nest.
             [ct, S["lesson"], lvl, dur, topic, fmt] + extra,
             day=nxt(), visibility=vis,
             image=None if (slug == "lwc-essentials" and i == 1) else f"lesson-generic-{(i % 3) + 1:02d}")

# ── Training ───────────────────────────────────────────────────────────────
MODULE_LESSONS = {
    "start": [("install-the-cli", "Install the CLI", "Ten minutes, and you never touch a browser to deploy again.", DUR["10m"], FORMAT["video"]),
              ("your-first-org", "Your first scratch org", "Disposable, reproducible, and free.", DUR["15m"], FORMAT["exercise"]),
              ("source-control-basics", "Put the org in source control", "The org is not the source of truth. The repo is.", DUR["20m"], FORMAT["article"])],
    "build": [("model-the-data", "Model the data first", "Draw it on paper before you click New Object.", DUR["30m"], FORMAT["article"]),
              ("screens-that-work", "Screens people can use", "Fewer fields, in the order the work actually happens.", DUR["25m"], FORMAT["article"]),
              ("validation-without-anger", "Validation without anger", "A rule that blocks the save must say how to fix it.", DUR["15m"], FORMAT["quiz"])],
    "automate": [("flow-or-apex", "Flow or Apex?", "The honest version: it is about who maintains it, not about performance.", DUR["20m"], FORMAT["article"]),
                 ("record-triggered-flows", "Record-triggered flows", "Before-save, after-save, and why the difference costs you.", DUR["45m"], FORMAT["video"]),
                 ("when-automation-fights", "When two automations fight", "Order of execution, and the debug log that proves it.", DUR["1h"], FORMAT["article"])],
}
for slug, mt in MODULE.items():
    post(slug, mt["name"], mt["description"],
         [mt, S["training-module"], LEVEL["beginner"], DUR["2h"], HERO[2], ACCESS["free"]],
         day=nxt(), image=f"module-{slug}")
    for i, (lslug, title, exc, dur, fmt) in enumerate(MODULE_LESSONS[slug]):
        post(lslug, title, exc,
             [mt, S["training-lesson"], LEVEL["beginner"], dur, fmt],
             day=nxt(), image=f"lesson-generic-{(i % 3) + 1:02d}")

# ── Docs ───────────────────────────────────────────────────────────────────
DOCS_PAGES = {
    "getting-started": [("install", "Install", "Requirements, then three commands."),
                        ("first-publish", "Your first publish", "From empty repo to live site.")],
    "configuration": [("settings-reference", "Settings reference", "Every setting, what it changes, and the default."),
                      ("theme-settings", "Theme settings", "What a publisher can change without touching code.")],
    "troubleshooting": [("common-errors", "Common errors", "The six that account for most support mail."),
                        ("getting-help", "Getting help", "What to include so the first reply is useful.")],
}
for slug, dt in DOCS.items():
    post(slug, dt["name"], dt["description"],
         [dt, S["docs-section"], DUR["10m"], HERO[3]],
         day=nxt(), image=f"docs-{slug}")
    for pslug, title, exc in DOCS_PAGES[slug]:
        post(pslug, title, exc, [dt, S["docs-page"], DUR["5m"], FORMAT["article"]], day=nxt())

# ── Blog ───────────────────────────────────────────────────────────────────
# One featured, and one with a deliberately long title and excerpt — truncation
# and text-wrap bugs only ever appear at length.
post("why-your-org-is-slow", "Why your org is slow", "It is almost never the platform. Here is the order to check things in.",
     [TOPIC["apex"], S["blog"], LEVEL["intermediate"], DUR["10m"], HERO[1]], day=nxt(), image="blog-01", featured=True)
post("the-admin-developer-line",
     "The line between an administrator and a developer is not where you think it is, and pretending otherwise costs teams months",
     "Every org eventually hits the point where clicks stop scaling and code starts. Recognising that moment early is worth more than any certification, and most teams recognise it about a year late — usually after the third rebuild of the same automation.",
     [TOPIC["flow"], S["blog"], LEVEL["beginner"], DUR["15m"], HERO[2]], day=nxt(), image="blog-02")
post("reading-a-debug-log", "Reading a debug log without crying", "Turn off everything, turn on one thing, read the middle.",
     [TOPIC["apex"], S["blog"], LEVEL["advanced"], DUR["20m"], HERO[3]], day=nxt(), image="blog-03")

# ── Resources ──────────────────────────────────────────────────────────────
for i, (slug, title, exc, rt, topic) in enumerate([
    ("apex-recipes", "Apex Recipes", "The reference implementation, maintained by Salesforce.", RTYPE["website"], TOPIC["apex"]),
    ("sfdx-cheatsheet", "SFDX cheat sheet", "The twenty commands worth memorising.", RTYPE["tool"], TOPIC["integration"]),
    ("advanced-apex", "Advanced Apex Programming", "Dan Appleman's book. Still the one to read second.", RTYPE["book"], TOPIC["apex"]),
]):
    post(slug, title, exc, [topic, S["resource"], rt, DUR["5m"]], day=nxt(), image=f"resource-0{i+1}")

# ── Products ───────────────────────────────────────────────────────────────
post("admin-toolkit", "The Admin Toolkit", "Twelve saved reports, a permissions audit sheet and a go-live checklist.",
     [TOPIC["security"], S["product"], ACCESS["paid"], HERO[1]], day=nxt(), image="product-01")
post("interview-pack", "Interview pack", "Forty questions, with the answers an interviewer is actually listening for.",
     [TOPIC["apex"], S["product"], ACCESS["paid"], HERO[2]], day=nxt(), image="product-02")

# ── Pages ──────────────────────────────────────────────────────────────────
# type "page", so Ghost serves them at /{slug}/ via page.hbs. The `home`,
# `training` and `docs` pages back the content-less routes: each template forks
# on {{#page}} and uses the page's title and excerpt when one exists.
for slug, title, exc in [
    ("home", "Say Namaste to Salesforce", "Beginner-friendly courses, hands-on training and a weekly newsletter for people learning Salesforce properly."),
    ("about", "About", "Who writes this, and why it is free."),
    ("training", "Training", "A guided path from a fresh org to a working one."),
    ("docs", "Documentation", "Reference for the theme and the tooling."),
    ("contact", "Contact", "The fastest way to reach a human."),
]:
    post(slug, title, exc, [], day=nxt(), type_="page",
         image="course-admin-foundations" if slug == "home" else None)

# ── The styleguide ─────────────────────────────────────────────────────────
# Every Koenig card and every prose element, once. A theme is judged on what
# happens when a writer uses a card its author never tried, and Ghost's editor
# emits two dozen of them. Open this page after any CSS change.
post("styleguide", "Styleguide: every card, every element",
     "Everything Ghost's editor can produce, on one page. If a card here looks wrong, it is wrong on a real post too.",
     [TOPIC["apex"], S["blog"], DUR["10m"], HERO[1]],
     day=nxt(), image="blog-01", body=styleguide.build())

# ══ ASSERTIONS — these run before anything is written ═══════════════════════
by_id = {t["id"]: t for t in TAGS}
posts_by_id = {p["id"]: p for p in POSTS}
first = {}
for j in JOINS:
    if j["sort_order"] == 0:
        first[j["post_id"]] = by_id[j["tag_id"]]

PARENT_STRUCTURAL = {"hash-course", "hash-training-module", "hash-docs-section"}
parent_ids = {j["post_id"] for j in JOINS if by_id[j["tag_id"]]["slug"] in PARENT_STRUCTURAL}

problems = []
for pid in parent_ids:
    p, t = posts_by_id[pid], first.get(pid)
    # THE ONE RULE: a parent's slug must equal its own primary tag's slug, or
    # every child underneath it 301s to the wrong parent.
    if not t or t["slug"] != p["slug"]:
        problems.append(f"parent slug != primary tag: {p['slug']} vs {t and t['slug']}")

for pid, t in first.items():
    if t["visibility"] == "internal":
        problems.append(f"primary tag is INTERNAL for {posts_by_id[pid]['slug']} ({t['slug']}) "
                        f"— sort_order 0 must be the public parent/topic tag")

slugs = [p["slug"] for p in POSTS]
dupes = {s for s in slugs if slugs.count(s) > 1}
if dupes:
    problems.append(f"duplicate post slugs: {sorted(dupes)}")

for p in POSTS:
    json.loads(p["lexical"])          # every body must be valid JSON

if problems:
    raise SystemExit("FIXTURE INVALID:\n  " + "\n  ".join(problems))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({
    "meta": {"exported_on": int(BASE.timestamp() * 1000), "version": "5.0.0"},
    "data": {"tags": TAGS, "posts": POSTS, "posts_tags": JOINS},
}, indent=2) + "\n")

kinds = {}
for j in JOINS:
    s = by_id[j["tag_id"]]["slug"]
    if s.startswith("hash-") and s.count("-") == 1 or s in ("hash-training-module", "hash-training-lesson", "hash-docs-section", "hash-docs-page"):
        kinds[s] = kinds.get(s, 0) + 1

print(f"wrote {OUT.relative_to(ROOT)}")
print(f"  {len(POSTS)} posts · {len(TAGS)} tags · {len(JOINS)} joins · {OUT.stat().st_size/1024:.0f} KB")
print("  " + " · ".join(f"{k.replace('hash-','')}:{v}" for k, v in sorted(kinds.items()) if v))
print(f"  members-only: {sum(1 for p in POSTS if p['visibility']=='members')} · "
      f"featured: {sum(1 for p in POSTS if p['featured'])} · "
      f"no image: {sum(1 for p in POSTS if not p['feature_image'])} · "
      f"pages: {sum(1 for p in POSTS if p['type']=='page')}")
print("  all assertions passed")
