"""Builds the site. Run: python build.py   Then open docs/index.html
Articles: Markdown files in posts/.  About page: about.md."""
import re, html, shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
SITE_NAME = "Jack"                 # change to your full name
HEADLINE = "Writing about what I am <i>learning</i> and what I can't stop thinking about."
SUBLINE = "Reading poems until they start talking back."


# ---------- markdown ----------
def slugify(t):
    return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-") or "section"


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
    return t


def md(text, poem=False):
    out, para, items, oitems, quote, heads = [], [], [], [], [], []

    def flush():
        nonlocal para, items, oitems, quote
        if para:
            if poem:
                out.append('<p class="stanza">' + "<br>\n".join(inline(l) for l in para) + "</p>")
            else:
                out.append("<p>" + inline(" ".join(para)) + "</p>")
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
        if oitems:
            out.append("<ol>" + "".join(f"<li>{inline(i)}</li>" for i in oitems) + "</ol>")
        if quote:
            out.append("<blockquote><p>" + inline(" ".join(quote)) + "</p></blockquote>")
        para, items, oitems, quote = [], [], [], []

    for line in text.splitlines():
        s = line.strip()
        if not s:
            flush()
            continue
        im = re.match(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)$', s)
        if im:
            flush()
            src = im.group(2)
            if not re.match(r"(https?:)?//|\.\./", src):
                src = "../" + src      # images/x.jpg is written relative to the site folder
            cap = f"<figcaption>{html.escape(im.group(3))}</figcaption>" if im.group(3) else ""
            out.append(f'<figure><img src="{html.escape(src)}" alt="{html.escape(im.group(1))}" loading="lazy">{cap}</figure>')
            continue
        m = re.match(r"(#{1,3})\s+(.*)", s)
        if m:
            flush()
            n = max(2, len(m.group(1)))
            sid = slugify(m.group(2))
            heads.append((n, m.group(2), sid))
            out.append(f'<h{n} id="{sid}">{inline(m.group(2))}</h{n}>')
            continue
        if s.startswith("- "):
            if para or quote or oitems:
                flush()
            items.append(s[2:])
            continue
        mo = re.match(r"\d+\.\s+(.*)", s)
        if mo:
            if para or quote or items:
                flush()
            oitems.append(mo.group(1))
            continue
        if s.startswith("> "):
            if para or items or oitems:
                flush()
            quote.append(s[2:])
            continue
        if items or oitems or quote:
            flush()
        para.append(s)
    flush()
    return "\n".join(out), heads


def parse(path):
    raw = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    meta, body = {}, raw
    m = re.match(r"---\n(.*?)\n---\n(.*)", raw, re.S)
    if m:
        for l in m.group(1).splitlines():
            if ":" in l:
                k, v = l.split(":", 1)
                meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body


def nice_date(d):
    try:
        dt = datetime.strptime(d, "%Y-%m-%d")
        return f"{dt.day} {dt.strftime('%b %Y')}"
    except ValueError:
        return d


# ---------- page shell ----------
def layout(title, body, depth=0, active="", progress=False):
    up = "../" * depth

    def nav(href, label, key):
        on = ' class="on"' if active == key else ""
        return f'<a href="{up}{href}"{on}>{label}</a>'

    bar = '<div id="progress"></div>' if progress else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,600;1,9..144,400&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css">
<script>try{{var t=localStorage.getItem("theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
</head><body>
{bar}
<header class="top"><a class="logo" href="{up}index.html">{html.escape(SITE_NAME)}</a>
<nav>{nav("index.html", "Articles", "home")}{nav("about.html", "About", "about")}
<button id="theme" aria-label="Switch light or dark theme">Dark</button></nav></header>
{body}
<footer>&copy; {html.escape(SITE_NAME)}</footer>
<script src="{up}site.js"></script>
</body></html>"""


def main():
    docs = ROOT / "docs"
    if docs.exists():
        shutil.rmtree(docs)
    (docs / "posts").mkdir(parents=True)
    shutil.copy(ROOT / "style.css", docs / "style.css")
    shutil.copy(ROOT / "site.js", docs / "site.js")
    if (ROOT / "images").exists():
        shutil.copytree(ROOT / "images", docs / "images")

    posts = []
    for p in sorted((ROOT / "posts").glob("*.md")):
        meta, body = parse(p)
        title = meta.get("title", p.stem)
        date = meta.get("date", "")
        tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]
        poem = meta.get("type", "").lower() == "poem"
        content, heads = md(body, poem)
        words = len(re.findall(r"\w+", body))
        mins = max(1, round(words / 220))
        toc = toc_inline = ""
        if not poem and len([h for h in heads if h[0] == 2]) >= 2:
            links = "".join(f'<a class="l{n}" href="#{sid}">{html.escape(t)}</a>' for n, t, sid in heads)
            toc = f'<aside class="toc"><div class="toc-h">On this page</div>{links}</aside>'
            toc_inline = f'<details class="toc toc-inline"><summary>On this page</summary>{links}</details>'
        tagline = " · ".join(html.escape(t) for t in tags)
        cls = " poem" if poem else ""
        wrap = " has-toc" if toc else ""
        art = f"""<div class="post-wrap{wrap}">
<article class="post{cls}">
<div class="tag">{tagline}</div>
<h1>{html.escape(title)}</h1>
<div class="meta">{nice_date(date)} · {mins} min read</div>
{toc_inline}
<div class="body">{content}</div>
<p class="back"><a href="../index.html">&larr; All articles</a></p>
</article>{toc}</div>"""
        (docs / "posts" / f"{p.stem}.html").write_text(
            layout(f"{title} | {SITE_NAME}", art, 1, progress=True), encoding="utf-8")
        posts.append(dict(date=date, title=title, slug=p.stem, tags=tags, mins=mins,
                          summary=meta.get("summary", "")))
    posts.sort(key=lambda x: x["date"], reverse=True)

    alltags = sorted({t for x in posts for t in x["tags"]})
    chips = '<button class="chip on" data-tag="">All</button>' + "".join(
        f'<button class="chip" data-tag="{html.escape(t)}">{html.escape(t)}</button>' for t in alltags)
    cards = ""
    for x in posts:
        text = html.escape((x["title"] + " " + x["summary"] + " " + " ".join(x["tags"])).lower())
        summ = f'<p class="sum">{html.escape(x["summary"])}</p>' if x["summary"] else ""
        cards += (
            f'<a class="card" href="posts/{x["slug"]}.html" data-tags="{html.escape("|".join(x["tags"]))}" data-text="{text}">'
            f'<div class="tag">{html.escape(" · ".join(x["tags"]))}</div><h3>{html.escape(x["title"])}</h3>{summ}'
            f'<div class="meta">{x["mins"]} min read · {nice_date(x["date"])}</div></a>')
    if not cards:
        cards = '<p class="none">No articles yet.</p>'
    home = f"""<main class="home">
<h1 class="hero">{HEADLINE}</h1><p class="sub">{html.escape(SUBLINE)}</p>
<input id="q" type="search" placeholder="Search articles" aria-label="Search articles">
<div class="chips">{chips}</div>
<div class="grid" id="grid">{cards}</div>
<p class="none" id="none" hidden>Nothing matches that.</p></main>"""
    (docs / "index.html").write_text(layout(SITE_NAME, home, 0, "home"), encoding="utf-8")

    am, ab = parse(ROOT / "about.md")
    acontent, _ = md(ab)
    about = (f'<main class="home"><article class="post"><h1>{html.escape(am.get("title", "About"))}</h1>'
             f'<div class="body">{acontent}</div></article></main>')
    (docs / "about.html").write_text(layout(f"About | {SITE_NAME}", about, 0, "about"), encoding="utf-8")
    print(f"Built {len(posts)} article(s) into {docs}")


main()
