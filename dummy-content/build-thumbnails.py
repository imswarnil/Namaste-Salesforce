#!/usr/bin/env python3
"""Theme-styled SVG thumbnails — the CLEAN set.

Reads every post whose feature_image is a picsum placeholder, one of
our own generated thumbs, or missing, and draws a clean 1200x675 SVG
into assets/images/thumbs/{slug}.svg, then repoints the post's
feature_image at it.

Two treatments:
  · default    flat navy canvas, kicker, wrapped title, brand line —
               no grid, no glow, no gradient
  · video      posts in the video library or tagged #lesson-type-video:
               a solid colour and a centered video icon, nothing else

Run from the theme root:  python3 dummy-content/build-thumbnails.py
"""
import sqlite3, html, textwrap, pathlib, sys

DB = "/Users/swarnil/Namaste Salesforce/ghost/content/data/ghost-local.db"
OUT = pathlib.Path("assets/images/thumbs")

# stroke paths lifted from partials/icons/ (24-box, drawn at scale)
ICONS = {
    "course":     '<path d="m2.5 9 9.5-4.5L21.5 9 12 13.5 2.5 9z"/><path d="M6.5 11.4v4.4c0 1.4 2.5 2.7 5.5 2.7s5.5-1.3 5.5-2.7v-4.4M21.5 9v5.5"/>',
    "lesson":     '<circle cx="12" cy="12" r="8.6"/><path d="M10 8.8v6.4l5.2-3.2L10 8.8z" fill="rgba(255,255,255,0.9)" stroke="none"/>',
    "training":   '<path d="m12 3 9 5-9 5-9-5 9-5z"/><path d="m3.6 12.7 8.4 4.6 8.4-4.6M3.6 17 12 21.6 20.4 17"/>',
    "blog":       '<path d="M14.5 4.5 19.5 9.5 8 21H3v-5L14.5 4.5z"/><path d="m12.5 6.5 5 5"/>',
    "video":      '<rect x="2.5" y="6" width="13.5" height="12" rx="2.4"/><path d="m16 10.4 4.3-2.6a.8.8 0 0 1 1.2.7v7a.8.8 0 0 1-1.2.7L16 13.6"/>',
    "newsletter": '<path d="M4 5.5h12.5a1.5 1.5 0 0 1 1.5 1.5v11.5H5.5A1.5 1.5 0 0 1 4 17V5.5z"/><path d="M18 8.5h1.2a1.3 1.3 0 0 1 1.3 1.3V17a1.5 1.5 0 0 1-1.5 1.5H18M7 9h5M7 12.2h8M7 15.4h8"/>',
    "changelog":  '<path d="M4 12a8 8 0 1 0 2.3-5.6L4 8.7"/><path d="M4 4.5v4.2h4.2M12 8v4.4l3 1.8"/>',
}
KICKERS = {"course": "COURSE", "lesson": "LESSON", "training": "TRAINING",
           "blog": "BLOG", "video": "VIDEO", "newsletter": "NEWSLETTER",
           "changelog": "CHANGELOG"}

NAVY   = "#032d60"   # brand-800 — the flat canvas
ACCENT = "#1b96ff"   # brand-400 — kicker + rule

def kind_of(slugs):
    for group, members in {
        "course": ("hash-course-col", "hash-courses-col"),
        "lesson": ("hash-lesson-col", "hash-lessons-col"),
        "training": ("hash-training-col", "hash-docs-col"),
        "video": ("hash-video-col",),
        "newsletter": ("hash-newsletter-col",),
        "changelog": ("hash-changelog-col", "hash-feed-col"),
        "blog": ("hash-blog-col",),
    }.items():
        if any(s in slugs for s in members):
            return group
    return "blog"

def svg_video():
    """Video thumb: one solid colour under a faint tiled icon
    pattern — NO centre icon. The video card overlays its own
    play badge; a drawn icon here would double it."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675">
  <defs>
    <pattern id="icons" width="150" height="150" patternUnits="userSpaceOnUse" patternTransform="rotate(-12)">
      <g transform="translate(30,30) scale(2.2)" fill="none" stroke="rgba(255,255,255,0.07)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS["video"]}</g>
      <g transform="translate(105,105) scale(1.4)" fill="none" stroke="rgba(255,255,255,0.055)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS["video"]}</g>
    </pattern>
  </defs>
  <rect width="1200" height="675" fill="{NAVY}"/>
  <rect width="1200" height="675" fill="url(#icons)"/>
</svg>'''

def svg_clean(title, kind):
    """Default thumb: flat navy, kicker + wrapped title + brand
    line on the left, a geometric illustration on the right —
    glow circle, ring, dot grid, and the collection icon in a
    rounded tile."""
    lines = textwrap.wrap(title, 24)[:3]
    tspans = "".join(
        f'<tspan x="80" dy="{0 if i == 0 else 76}">{html.escape(line)}</tspan>'
        for i, line in enumerate(lines))
    dots = "".join(
        f'<circle cx="{x}" cy="{y}" r="3"/>'
        for x in range(0, 145, 36) for y in range(0, 109, 36))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 675" font-family="Figtree,-apple-system,'Segoe UI',Roboto,sans-serif">
  <defs>
    <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
      <stop offset="0" stop-color="rgba(27,150,255,0.35)"/><stop offset="1" stop-color="rgba(27,150,255,0)"/>
    </radialGradient>
    <clipPath id="frame"><rect width="1200" height="675"/></clipPath>
  </defs>
  <rect width="1200" height="675" fill="{NAVY}"/>
  <g clip-path="url(#frame)">
    <circle cx="985" cy="300" r="290" fill="url(#glow)"/>
    <circle cx="985" cy="300" r="180" fill="none" stroke="rgba(27,150,255,0.35)" stroke-width="2" stroke-dasharray="2 10" stroke-linecap="round"/>
    <circle cx="1140" cy="118" r="46" fill="none" stroke="rgba(255,255,255,0.14)" stroke-width="2"/>
    <circle cx="822" cy="510" r="14" fill="rgba(27,150,255,0.45)"/>
    <g fill="rgba(255,255,255,0.12)" transform="translate(1042,470)">{dots}</g>
    <rect x="895" y="210" width="180" height="180" rx="36" fill="rgba(27,150,255,0.16)" stroke="rgba(27,150,255,0.55)" stroke-width="2"/>
    <g transform="translate(931,246) scale(4.5)" fill="none" stroke="rgba(255,255,255,0.92)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[kind]}</g>
  </g>
  <text x="80" y="120" font-size="26" font-weight="700" letter-spacing="6" fill="{ACCENT}">{KICKERS[kind]}</text>
  <text x="80" y="330" font-size="64" font-weight="800" fill="#ffffff">{tspans}</text>
  <rect x="80" y="560" width="120" height="6" rx="3" fill="{ACCENT}"/>
  <text x="80" y="612" font-size="24" font-weight="600" letter-spacing="2" fill="rgba(244,246,248,0.75)">NAMASTE SALESFORCE</text>
</svg>'''

def main():
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
    db.commit()
    print(f"generated + repointed {changed} thumbnails")

if __name__ == "__main__":
    main()
