#!/usr/bin/env python3
"""Theme-styled SVG thumbnails — the CLEAN set.

TWO sources, both light-canvas:

  1. dummy-content/import.json (always): every post/tag whose
     feature_image points into assets/images/thumbs|tags gets its
     SVG drawn, so the demo import never ships broken images.
  2. the local Ghost DB (only if it exists): same treatment plus
     repointing feature_image, for content created in Admin.

Treatments:
  · default    light canvas, blueprint grid, navy icon tile,
               kicker + wrapped title + brand line
  · video      light canvas under a faint tiled icon pattern —
               the card overlays its own play badge

Run from the theme root:  python3 dummy-content/build-thumbnails.py
"""
import json, os, sqlite3, html, textwrap, pathlib, sys

DB = "/Users/swarnil/Namaste Salesforce/ghost/content/data/ghost-local.db"
OUT = pathlib.Path("assets/images/thumbs")
TAG_OUT = pathlib.Path("assets/images/tags")

# stroke paths lifted from partials/icons/ (24-box, drawn at scale)
ICONS = {
    "course":     '<path d="m2.5 9 9.5-4.5L21.5 9 12 13.5 2.5 9z"/><path d="M6.5 11.4v4.4c0 1.4 2.5 2.7 5.5 2.7s5.5-1.3 5.5-2.7v-4.4M21.5 9v5.5"/>',
    "lesson":     '<circle cx="12" cy="12" r="8.6"/><path d="M10 8.8v6.4l5.2-3.2L10 8.8z" fill="rgba(255,255,255,0.9)" stroke="none"/>',
    "training":   '<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3.6 12.7 8.4 4.6 8.4-4.6M3.6 17 12 21.6 20.4 17"/>',
    "blog":       '<path d="M14.5 4.5 19.5 9.5 8 21H3v-5L14.5 4.5z"/><path d="m12.5 6.5 5 5"/>',
    "video":      '<rect x="2.5" y="6" width="13.5" height="12" rx="2.4"/><path d="m16 10.4 4.3-2.6a.8.8 0 0 1 1.2.7v7a.8.8 0 0 1-1.2.7L16 13.6"/>',
    "slides":     '<path d="M3.5 4.5h17M4.5 4.5h15V15a1.5 1.5 0 0 1-1.5 1.5H6A1.5 1.5 0 0 1 4.5 15V4.5z"/><path d="M8 12.5 10.5 10l2 1.8 3.5-3.3M12 16.5v3M9 21.5l3-2 3 2"/>',
    "newsletter": '<path d="M4 5.5h12.5a1.5 1.5 0 0 1 1.5 1.5v11.5H5.5A1.5 1.5 0 0 1 4 17V5.5z"/><path d="M18 8.5h1.2a1.3 1.3 0 0 1 1.3 1.3V17a1.5 1.5 0 0 1-1.5 1.5H18M7 9h5M7 12.2h8M7 15.4h8"/>',
    "changelog":  '<path d="M4 12a8 8 0 1 0 2.3-5.6L4 8.7"/><path d="M4 4.5v4.2h4.2M12 8v4.4l3 1.8"/>',
    "resource":   '<path d="M7 3.5h10a1 1 0 0 1 1 1V21l-6-3.8L6 21V4.5a1 1 0 0 1 1-1z"/>',
    "shop":       '<path d="M4 8.5h16v3H4zM5.5 11.5V20h13v-8.5M12 8.5V20"/><path d="M12 8.5C12 8.5 8 8.7 8 6.2 8 4.3 10.4 4.1 11.3 5.1 12 6 12 8.5 12 8.5zm0 0s0-2.5.7-3.4c.9-1 3.3-.8 3.3 1.1 0 2.5-4 2.3-4 2.3z"/>',
    "snippet":    '<path d="m9 8-4 4 4 4M15 8l4 4-4 4"/>',
    "prompt":     '<path d="M12 3l1.8 4.6L18.5 9l-4.7 1.4L12 15l-1.8-4.6L5.5 9l4.7-1.4L12 3z"/><path d="M18.5 15l.9 2.3 2.3.9-2.3.9-.9 2.3-.9-2.3-2.3-.9 2.3-.9.9-2.3z"/>',
    "project":    '<circle cx="6" cy="5.5" r="2.4"/><circle cx="6" cy="18.5" r="2.4"/><circle cx="18" cy="8" r="2.4"/><path d="M6 8v8M18 10.5c0 4-5.5 3.5-9.4 5.4"/>',
    "module":     '<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3.6 12.7 8.4 4.6 8.4-4.6M3.6 17 12 21.6 20.4 17"/>',
    "page":       '<path d="M7 3.5h7l4 4V20a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V4.5a1 1 0 0 1 1-1z"/><path d="M13.7 3.7V8h4.2M9 12h6M9 15.5h6"/>',
}
KICKERS = {"course": "COURSE", "lesson": "LESSON", "training": "TRAINING",
           "blog": "BLOG", "video": "VIDEO", "slides": "SLIDES",
           "newsletter": "NEWSLETTER",
           "changelog": "CHANGELOG", "resource": "RESOURCE", "shop": "SHOP",
           "snippet": "SNIPPET", "prompt": "PROMPT", "project": "PROJECT",
           "module": "MODULE", "page": "PAGE"}

NAVY   = "#032d60"   # brand-800 — ink + the icon tile
ACCENT = "#0176d3"   # brand-500 — kicker + accents
LIGHT  = "#f5f9fd"   # the light canvas

def kind_of(slugs):
    for group, members in {
        "course": ("hash-course",),
        "lesson": ("hash-lesson",),
        "module": ("hash-module",),
        "training": ("hash-training",),
        "video": ("hash-video",),
        "slides": ("hash-slides",),
        "newsletter": ("hash-newsletter",),
        "changelog": ("hash-changelog",),
        "resource": ("hash-resource",),
        "shop": ("hash-shop",),
        "snippet": ("hash-snippet",),
        "prompt": ("hash-prompt",),
        "project": ("hash-project",),
        "blog": ("hash-blog",),
    }.items():
        if any(s in slugs for s in members):
            return group
    return "blog"

def svg_video():
    """Video thumb: the LIGHT canvas under a faint dark tiled icon
    pattern — NO centre icon. The video card overlays its own
    play badge; a drawn icon here would double it."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675">
  <defs>
    <pattern id="icons" width="150" height="150" patternUnits="userSpaceOnUse" patternTransform="rotate(-12)">
      <g transform="translate(30,30) scale(2.2)" fill="none" stroke="rgba(3,45,96,0.10)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS["video"]}</g>
      <g transform="translate(105,105) scale(1.4)" fill="none" stroke="rgba(3,45,96,0.07)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS["video"]}</g>
    </pattern>
  </defs>
  <rect width="1200" height="675" fill="{LIGHT}"/>
  <rect width="1200" height="675" fill="url(#icons)"/>
</svg>'''

def svg_clean(title, kind):
    """Default thumb — the LIGHT treatment: near-white canvas, the
    blueprint grid and dot pattern drawn DARK on it, and the
    collection icon dead centre in a navy tile inside a dashed
    ring. Kicker top-left, short title bottom-left in ink, brand
    line bottom-right — all quiet, the icon carries it."""
    lines = textwrap.wrap(title, 34)[:2]
    tspans = "".join(
        f'<tspan x="80" dy="{0 if i == 0 else 46}">{html.escape(line)}</tspan>'
        for i, line in enumerate(lines))
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="2.5"/>'
        for x in range(0, 145, 36) for y in range(0, 109, 36))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" font-family="Figtree,-apple-system,'Segoe UI',Roboto,sans-serif">
  <defs>
    <pattern id="lgrid" width="48" height="48" patternUnits="userSpaceOnUse">
      <path d="M48 0H0v48" fill="none" stroke="rgba(3,45,96,0.09)"/>
    </pattern>
  </defs>
  <rect width="1200" height="675" fill="{LIGHT}"/>
  <rect width="1200" height="675" fill="url(#lgrid)"/>
  <g fill="rgba(3,45,96,0.16)" transform="translate(990,64)">{dots}</g>
  <g fill="rgba(3,45,96,0.16)" transform="translate(66,470)">{dots}</g>
  <circle cx="600" cy="302" r="190" fill="none" stroke="rgba(1,118,211,0.30)" stroke-width="2" stroke-dasharray="2 12" stroke-linecap="round"/>
  <circle cx="986" cy="560" r="10" fill="rgba(1,118,211,0.35)"/>
  <circle cx="180" cy="130" r="34" fill="none" stroke="rgba(3,45,96,0.14)" stroke-width="2"/>
  <rect x="490" y="192" width="220" height="220" rx="48" fill="{NAVY}"/>
  <g transform="translate(534,236) scale(5.5)" fill="none" stroke="#ffffff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[kind]}</g>
  <text x="80" y="92" font-size="24" font-weight="700" letter-spacing="6" fill="{ACCENT}">{KICKERS[kind]}</text>
  <text x="80" y="588" font-size="38" font-weight="800" fill="{NAVY}">{tspans}</text>
  <text x="1120" y="632" font-size="20" font-weight="600" letter-spacing="2" fill="rgba(3,45,96,0.45)" text-anchor="end">NAMASTE SALESFORCE</text>
</svg>'''

def svg_tag_badge(name):
    """Square badge for a PUBLIC tag — templates render it as the
    tag's icon (module badges, card eyebrows, rail icons), usually
    at 2–5rem, so it has to read tiny: the LIGHT canvas, a navy
    tile, the tag's monogram in white."""
    words = [w for w in name.split() if w and w[0].isalnum()]
    mono = html.escape("".join(w[0] for w in words[:2]).upper() or "•")
    size = 200 if len(mono) < 2 else 155
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" font-family="Figtree,-apple-system,'Segoe UI',Roboto,sans-serif">
  <rect width="600" height="600" fill="{LIGHT}"/>
  <circle cx="300" cy="300" r="235" fill="none" stroke="rgba(1,118,211,0.30)" stroke-width="5" stroke-dasharray="3 18" stroke-linecap="round"/>
  <rect x="140" y="140" width="320" height="320" rx="76" fill="{NAVY}"/>
  <text x="300" y="300" font-size="{size}" font-weight="800" fill="#ffffff" text-anchor="middle" dominant-baseline="central">{mono}</text>
</svg>'''

def tag_badges(c):
    """Every public tag gets its badge; only images the editor set
    by hand (anything not ours, not empty) are left alone."""
    TAG_OUT.mkdir(parents=True, exist_ok=True)
    changed = 0
    for tid, slug, name, image in c.execute(
            "select id, slug, name, feature_image from tags "
            "where visibility = 'public'").fetchall():
        if image and '/assets/images/tags/' not in image:
            continue
        (TAG_OUT / f"{slug}.svg").write_text(svg_tag_badge(name))
        c.execute("update tags set feature_image=? where id=?",
                  (f"__GHOST_URL__/assets/images/tags/{slug}.svg", tid))
        changed += 1
    return changed

def from_import():
    """Draw every SVG the demo import references, straight from
    import.json — no Ghost install needed. The import already
    stamps the __GHOST_URL__ paths; this makes the files real."""
    src = pathlib.Path(__file__).parent / "import.json"
    if not src.exists():
        return 0, 0
    data = json.loads(src.read_text())["db"][0]["data"]
    tags_by_id = {t["id"]: t for t in data["tags"]}
    post_tags = {}
    for m in data["posts_tags"]:
        post_tags.setdefault(m["post_id"], []).append(m["tag_id"])

    OUT.mkdir(parents=True, exist_ok=True)
    TAG_OUT.mkdir(parents=True, exist_ok=True)

    thumbs = 0
    for p in data["posts"]:
        image = p.get("feature_image") or ""
        if "/assets/images/thumbs/" not in image:
            continue
        name = image.rsplit("/", 1)[-1]
        slugs = " ".join(
            tags_by_id[tid]["slug"] for tid in post_tags.get(p["id"], [])
            if tid in tags_by_id)
        kind = "page" if p.get("type") == "page" else kind_of(slugs)
        videoish = kind == "video" or "hash-lesson-type-video" in slugs
        art = svg_video() if videoish else svg_clean(p["title"], kind)
        (OUT / name).write_text(art)
        thumbs += 1

    badges = 0
    for t in data["tags"]:
        image = t.get("feature_image") or ""
        if "/assets/images/tags/" not in image:
            continue
        (TAG_OUT / image.rsplit("/", 1)[-1]).write_text(svg_tag_badge(t["name"]))
        badges += 1
    return thumbs, badges

def main():
    it, ib = from_import()
    print(f"import.json: generated {it} thumbnails, {ib} tag badges")
    if not os.path.exists(DB):
        print("no local Ghost DB — skipped the live-site pass")
        return
    OUT.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB)
    c = db.cursor()
    rows = c.execute("""
        select p.id, p.slug, p.title, p.feature_image,
               group_concat(t.slug, ' ')
        from posts p
        left join posts_tags pt on pt.post_id = p.id
        left join tags t on t.id = pt.tag_id
        where p.type = 'post'
        group by p.id
    """).fetchall()

    changed = 0
    for pid, slug, title, image, tag_slugs in rows:
        # regenerating our own thumbs is the point — only images the
        # editor chose by hand are left alone
        needs = (not image or 'picsum.photos' in image
                 or '/assets/images/thumbs/' in image)
        if not needs:
            continue
        slugs = tag_slugs or ""
        kind = kind_of(slugs)
        videoish = kind == "video" or "hash-lesson-type-video" in slugs
        art = svg_video() if videoish else svg_clean(title, kind)
        (OUT / f"{slug}.svg").write_text(art)
        # Ghost stores internal URLs with the __GHOST_URL__ token and
        # substitutes the site URL when serving. A bare relative path
        # gets nulled by its URL-normalisation job — learned live.
        c.execute("update posts set feature_image=? where id=?",
                  (f"__GHOST_URL__/assets/images/thumbs/{slug}.svg", pid))
        changed += 1
    badges = tag_badges(c)
    db.commit()
    print(f"generated + repointed {changed} thumbnails, {badges} tag badges")

if __name__ == "__main__":
    main()
