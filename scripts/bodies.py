"""Real, varied post bodies for the fixture.

WHY THIS FILE EXISTS. The first fixture gave every post the same three
paragraphs, and that hid every bug worth finding: a table of contents built
from two identical headings looks fine, a card grid of identical excerpts
never wraps differently, and no card ever tested a long title against a short
one. A fixture whose rows are all the same only proves the template renders
once.

So each body below is different in the ways that matter to a TEMPLATE —
heading count and depth, list vs code vs quote, short vs long — rather than
different in prose for its own sake.
"""
import lexical as L

def _body(intro, sections):
    """intro + [(heading, [nodes])] → a document with a real outline."""
    nodes = [L.p(intro)]
    for heading, inner in sections:
        nodes.append(L.h(heading, 2))
        nodes.extend(inner)
    return L.doc(nodes)

BODIES = {}

BODIES["bulkify-or-die"] = _body(
    "Every Apex developer meets this bug once: the trigger that worked all through development, then failed the first time somebody imported a spreadsheet.",
    [("The limit is the transaction", [
        L.p("Governor limits are counted per transaction, not per record. A trigger that runs one query per record does not use one query — it uses as many as the load has rows, and the platform stops it at 101."),
        L.callout("The 101 is not a typo. The hundredth query succeeds; the hundred-and-first raises the exception.", "ℹ️", "blue"),
     ]),
     ("The fix is a pattern", [
        L.p("Collect the ids, query once, put the results in a map, then loop. Three lines longer, and it does not care whether the load is one record or two hundred."),
        L.code("Map<String, Id> queues = queueMap();\nfor (Case c : cases) {\n    c.OwnerId = queues.get(c.Origin);\n}", "apex", "CaseRouter.cls"),
     ]),
     ("Testing it honestly", [
        L.p("A test that inserts one record proves nothing about the case that broke. Insert two hundred."),
        L.ol(["Build the data in a factory, not inline.",
              "Insert 200, not 1.",
              "Assert the limit, not just the outcome."]),
     ])])

BODIES["governor-limits"] = _body(
    "Limits are a budget, not a punishment. Once you can read the bill, most of the fear goes.",
    [("What actually counts", [
        L.p("Statements count. Records mostly do not. The exception is DML rows, and that exception is where people get caught."),
        L.ul(["SOQL queries — 100 synchronous",
              "DML statements — 150",
              "DML rows — 10,000",
              "CPU time — 10 seconds synchronous"]),
     ]),
     ("Reading the log", [
        L.p("Turn everything off, turn one thing on, read the middle. A log at full verbosity is a wall; a log with only the limit events is a receipt."),
        L.quote("The debug log is not a stack trace. It is an itemised bill."),
     ])])

BODIES["testing-apex-properly"] = _body(
    "Seventy-five percent coverage is a floor nobody should be proud of clearing.",
    [("Coverage is not correctness", [
        L.p("A test that calls a method and asserts nothing raises coverage and proves nothing. The number the platform reports is a deployment gate, not a quality measure."),
     ]),
     ("What a real test looks like", [
        L.code("@isTest\nstatic void routesByOrigin() {\n    List<Case> cases = CaseFactory.build(200);\n    Test.startTest();\n    insert cases;\n    Test.stopTest();\n    System.assertEquals(200, [SELECT COUNT() FROM Case WHERE OwnerId != null]);\n}", "apex", "CaseRouterTest.cls"),
        L.callout("Assert the thing that broke in production. If you cannot name it, you do not have a test — you have coverage.", "⚠️", "yellow"),
     ])])

BODIES["why-your-org-is-slow"] = _body(
    "It is almost never the platform. Here is the order to check things in, and why that order matters more than the checks.",
    [("Start with the query, not the code", [
        L.p("Selectivity decides everything. A report that times out at fifty thousand rows is usually one unindexed filter away from being instant."),
     ]),
     ("Then the automation", [
        L.p("Count how many things fire on save. Two flows and a trigger on the same object is three chances to do the same work twice."),
        L.ul(["Record-triggered flows, before and after save",
              "Apex triggers",
              "Workflow rules that nobody has migrated yet"]),
     ]),
     ("Only then the data model", [
        L.p("If the first two came back clean, the shape is wrong, and that is a longer conversation."),
        L.quote("Every automation problem I have been called in to fix was a schema problem wearing a costume."),
     ])])

BODIES["the-admin-developer-line"] = _body(
    "Every org eventually hits the point where clicks stop scaling and code starts. Recognising that moment early is worth more than any certification.",
    [("The symptom", [
        L.p("You are maintaining the same logic in three places and none of them is the source of truth."),
     ]),
     ("The test", [
        L.ol(["Can you describe the rule in one sentence?",
              "Does it live in exactly one place?",
              "Would a new admin find it without being told?"]),
        L.p("Two noes mean the answer is code, whoever writes it."),
     ])])

BODIES["reading-a-debug-log"] = _body(
    "Turn off everything, turn on one thing, read the middle.",
    [("Levels, not logs", [
        L.p("The default trace flags produce a file nobody reads. Set everything to NONE, then raise the one category you are investigating."),
     ]),
     ("The middle is the answer", [
        L.p("The top is setup and the bottom is teardown. The thing that broke is almost always between the first LIMIT_USAGE line and the last."),
     ])])

def get(slug, fallback_excerpt):
    """A varied body if one is written, otherwise a short, honest stub.

    The stub is deliberately SHORT. A fixture full of identical long bodies
    makes every reading page look the same and hides exactly the wrapping and
    outline bugs the fixture exists to expose."""
    if slug in BODIES:
        return BODIES[slug]
    return _body(fallback_excerpt, [
        ("What you will learn", [L.p("Three or four practical steps, each small enough to finish in one sitting.")]),
        ("Before you start", [L.p("Nothing here assumes you have read the previous page, but it will go faster if you have.")]),
    ])
