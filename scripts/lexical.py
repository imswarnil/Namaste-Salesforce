"""Build Ghost Lexical documents for the seed fixture.

Lexical is Ghost's editor format — a JSON string, not HTML. Hand-writing it is
easy to get subtly wrong and Ghost fails the import WITHOUT saying which post,
so everything goes through these builders and every post takes the same code
path. See abstract/14 in the sibling project.

The node shapes below are Koenig's own. A card is a node with `type` set to
the card's name; a paragraph or heading is a standard Lexical node.
"""
import json

def _t(text, fmt=0):
    return {"detail": 0, "format": fmt, "mode": "normal", "style": "",
            "text": text, "type": "extended-text", "version": 1}

def _block(kind, children, **extra):
    return dict({"children": children, "direction": "ltr", "format": "",
                 "indent": 0, "type": kind, "version": 1}, **extra)

# ── Standard blocks ────────────────────────────────────────────────────────
def p(text):            return _block("paragraph", [_t(text)])
def bold_p(text):       return _block("paragraph", [_t(text, 1)])
def h(text, level=2):   return _block("heading", [_t(text)], tag=f"h{level}")
def quote(text):        return _block("quote", [_t(text)])

def ul(items):
    return _block("list", [
        _block("listitem", [_t(i)], value=n + 1) for n, i in enumerate(items)
    ], listType="bullet", start=1, tag="ul")

def ol(items):
    return _block("list", [
        _block("listitem", [_t(i)], value=n + 1) for n, i in enumerate(items)
    ], listType="number", start=1, tag="ol")

# ── Koenig cards ───────────────────────────────────────────────────────────
# Every one is `type` + the card's own fields. Ghost renders them into the
# .kg-* markup that assets/css/ghost/content.css maps onto NSDS.
def hr():
    return {"type": "horizontalrule", "version": 1}

def code(code_text, language="apex", caption=""):
    return {"type": "codeblock", "version": 1, "code": code_text,
            "language": language, "caption": caption}

def callout(text, emoji="💡", bg="grey"):
    return {"type": "callout", "version": 1, "calloutText": f"<span>{text}</span>",
            "calloutEmoji": emoji, "backgroundColor": bg}

def toggle(heading, content):
    return {"type": "toggle", "version": 1,
            "heading": f"<span>{heading}</span>", "content": f"<p>{content}</p>"}

def button(text, url, alignment="center"):
    return {"type": "button", "version": 1, "buttonText": text,
            "buttonUrl": url, "alignment": alignment}

def image(src, caption="", alt="", width=1200, height=675, card_width=""):
    return {"type": "image", "version": 1, "src": src, "width": width,
            "height": height, "title": "", "alt": alt, "caption": caption,
            "cardWidth": card_width, "href": ""}

def bookmark(url, title, description, author="", publisher="", icon="", thumbnail=""):
    return {"type": "bookmark", "version": 1, "url": url, "caption": "",
            "metadata": {"url": url, "title": title, "description": description,
                         "author": author, "publisher": publisher,
                         "icon": icon, "thumbnail": thumbnail}}

def embed(url, html, title="", provider="YouTube"):
    return {"type": "embed", "version": 1, "url": url, "embedType": "video",
            "html": html, "metadata": {"title": title, "author_name": provider},
            "caption": ""}

def markdown(md):
    return {"type": "markdown", "version": 1, "markdown": md}

def html_card(html):
    return {"type": "html", "version": 1, "html": html}

def divider_header(heading, subheading, size="small", style="dark"):
    return {"type": "header", "version": 2, "size": size, "style": style,
            "buttonEnabled": False, "buttonUrl": "", "buttonText": "",
            "header": f"<span>{heading}</span>",
            "subheader": f"<span>{subheading}</span>",
            "backgroundImageSrc": "", "alignment": "center", "backgroundColor": "#000000",
            "backgroundSize": "cover", "textColor": "#FFFFFF", "buttonColor": "#ffffff",
            "buttonTextColor": "#000000", "layout": "regular", "accentColor": "#FF1A75"}

def gallery(images):
    return {"type": "gallery", "version": 1, "caption": "",
            "images": [{"row": 0, "fileName": s.rsplit("/", 1)[-1], "src": s,
                        "width": 1200, "height": 675, "title": "", "alt": ""}
                       for s in images]}

def signup(header, subheader):
    return {"type": "signup", "version": 1, "alignment": "center",
            "backgroundColor": "accent", "backgroundImageSrc": "",
            "backgroundSize": "cover", "textColor": "#FFFFFF",
            "buttonColor": "#ffffff", "buttonTextColor": "#000000",
            "buttonText": "Subscribe", "disclaimer": "<span>No spam. Unsubscribe anytime.</span>",
            "header": f"<span>{header}</span>", "subheader": f"<span>{subheader}</span>",
            "labels": [], "layout": "wide", "successMessage": "Check your inbox."}

def doc(nodes):
    """Wrap nodes in a Lexical root and serialise. Ghost stores this as a
    STRING in the post's `lexical` column, so it is double-encoded on the way
    into import.json — json.dumps here, then json.dumps again for the file."""
    return json.dumps({"root": {"children": nodes, "direction": "ltr",
                                "format": "", "indent": 0,
                                "type": "root", "version": 1}})
