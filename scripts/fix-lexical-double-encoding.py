#!/usr/bin/env python3
"""
Repair double-encoded Lexical documents in Ghost dummy-content import files.

Background
----------
dummy-content/training.json (and friends) are hand-authored Ghost content-import
fixtures. Each post's `lexical` field must be a JSON *string* containing a
Lexical doc whose `root.children` is an *array* of top-level nodes, e.g.:

    "lexical": "{\"root\": {\"children\": [ ... array of nodes ... ], ...}}"

A previous edit of training.json (commit 40387bc, "Regenerate training dummy
data for the section-as-post model") introduced posts where `root.children`
was itself set to *another fully-stringified Lexical document* instead of an
array of nodes, i.e. the real content got wrapped in an extra layer of
`json.dumps`/`JSON.stringify`:

    "lexical": "{\"root\": {\"children\": \"{\\\"root\\\": {\\\"children\\\": [...] ...}}\", ...}}"

Ghost's Lexical validator rejects this as "Invalid lexical structure" because
`children` must be an array, not a string.

This script scans every dummy-content/*.json file, finds posts whose lexical
`root.children` is a string rather than a list, unwraps the inner stringified
doc (which holds the real array of nodes) and replaces the outer doc with it,
then re-serialises `lexical` back to a single JSON string as Ghost expects.

Usage:
    python3 scripts/fix-lexical-double-encoding.py [--check]

`--check` only reports problems (exit code 1 if any found) without writing.
"""
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DUMMY_CONTENT_DIR = REPO_ROOT / "dummy-content"


def unwrap_lexical(lexical_str):
    """Return (fixed_lexical_str, was_fixed) for a single post's lexical field."""
    doc = json.loads(lexical_str)
    root = doc.get("root", {})
    children = root.get("children")

    if isinstance(children, list):
        return lexical_str, False

    if not isinstance(children, str):
        # Not a recognised shape; leave untouched (validation step will flag it).
        return lexical_str, False

    # `children` holds a fully stringified Lexical doc (double-encoding bug).
    # Unwrap repeatedly in case of triple+ nesting, then use that doc as the
    # real lexical document.
    inner_str = children
    while True:
        inner_doc = json.loads(inner_str)
        inner_children = inner_doc.get("root", {}).get("children")
        if isinstance(inner_children, list):
            return json.dumps(inner_doc), True
        if isinstance(inner_children, str):
            inner_str = inner_children
            continue
        # Give up unwrapping further; return what we have.
        return json.dumps(inner_doc), True


def process_file(path, check_only):
    data = json.loads(path.read_text())
    posts = data.get("data", {}).get("posts", [])
    fixed_count = 0
    still_bad = []

    for post in posts:
        lexical = post.get("lexical")
        if lexical is None:
            continue
        fixed_lexical, was_fixed = unwrap_lexical(lexical)
        if was_fixed:
            post["lexical"] = fixed_lexical
            fixed_count += 1

        # Verify post-fix shape.
        doc = json.loads(post["lexical"])
        children = doc.get("root", {}).get("children")
        if not isinstance(children, list):
            still_bad.append((post.get("id"), post.get("slug")))

    if fixed_count and not check_only:
        # dummy-content/*.json fixtures use a 1-space indent; match it so the
        # diff is limited to the actually-changed lexical fields.
        path.write_text(json.dumps(data, indent=1) + "\n")

    return len(posts), fixed_count, still_bad


def main():
    check_only = "--check" in sys.argv
    total_posts = 0
    total_fixed = 0
    total_bad = []

    for path in sorted(DUMMY_CONTENT_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        if "data" not in data or "posts" not in data.get("data", {}):
            continue

        count, fixed, bad = process_file(path, check_only)
        total_posts += count
        total_fixed += fixed
        total_bad.extend((path.name, pid, slug) for pid, slug in bad)

        if fixed:
            action = "would fix" if check_only else "fixed"
            print(f"{path.name}: {action} {fixed}/{count} post(s) with double-encoded lexical")

    print(f"\nChecked {total_posts} posts across dummy-content/*.json")
    print(f"{'Would fix' if check_only else 'Fixed'}: {total_fixed}")
    if total_bad:
        print(f"Still invalid after fix: {len(total_bad)}")
        for fname, pid, slug in total_bad:
            print(f"  {fname}: {pid} ({slug})")
        sys.exit(1)
    else:
        print("All posts have root.children as a proper array.")


if __name__ == "__main__":
    main()
