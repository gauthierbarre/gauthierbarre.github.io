#!/usr/bin/env python3
"""Build the portfolio into _site/.

Sources
  site.yml                          identity, about, keywords, social links
  content/projects/<slug>/index.md  one project = front matter + Markdown + its figures
  content/notes.yml                 short technical notes
  static/                           copied as-is (css, js, favicon, cv.pdf)
  templates/                        Jinja2 templates

Usage
  python scripts/build.py             build into _site/
  python scripts/build.py --drafts    also build projects marked `draft: true`
  python scripts/build.py --serve     build, then serve on http://localhost:8000

The build stops with a list of errors (missing fields, missing figures, broken
internal links) instead of publishing a broken site.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import re
import shutil
import struct
import sys
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
CONTENT = ROOT / "content"
PROJECTS = CONTENT / "projects"
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"

REQUIRED_PROJECT_FIELDS = ("title", "summary", "date")
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}


class BuildError(Exception):
    pass


errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


# --------------------------------------------------------------------------- helpers

def to_date(value, where: str) -> dt.date | None:
    if value in (None, ""):
        return None
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        err(f"{where}: date '{value}' is not YYYY-MM-DD")
        return None


def fmt_date(d: dt.date | None) -> str:
    return f"{d.day} {d.strftime('%b')} {d.year}" if d else ""


def image_size(path: Path) -> tuple[int, int] | None:
    """Width/height of PNG, GIF or JPEG without Pillow (sets width/height to avoid layout shift)."""
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return struct.unpack("<HH", data[6:10])
    if data[:2] == b"\xff\xd8":
        i = 2
        while i < len(data) - 9:
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5:i + 9])
                return w, h
            i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    return None


def split_front_matter(text: str, where: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.S)
    if not m:
        err(f"{where}: missing front matter (a block between two '---' lines at the top)")
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        err(f"{where}: invalid front matter: {e}")
        meta = {}
    return meta, m.group(2)


def slugify(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_]+", "-", text).strip("-") or "section"


# --------------------------------------------------------------------------- markdown

MD_EXTENSIONS = ["tables", "attr_list", "md_in_html", "fenced_code", "footnotes", "sane_lists", "smarty"]


def render_markdown(text: str) -> str:
    return markdown.markdown(text, extensions=MD_EXTENSIONS, output_format="html")


MATH_RE = re.compile(r"(\$\$.+?\$\$|(?<![\\$])\$(?!\s)[^$\n]+?(?<!\s)\$)", re.S)


def protect_math(text: str) -> tuple[str, list[str]]:
    """Keep $...$ and $$...$$ away from Markdown (underscores, asterisks); KaTeX renders them."""
    stash: list[str] = []

    def keep(m):
        stash.append(html.escape(m.group(0)))
        return f"MATHPH{len(stash) - 1}HPMATH"

    return MATH_RE.sub(keep, text), stash


def restore_math(text: str, stash: list[str]) -> str:
    return re.sub(r"MATHPH(\d+)HPMATH", lambda m: stash[int(m.group(1))], text)


def parse_sections(body: str) -> tuple[list[dict], str]:
    """`## Heading` + optional one-line subtitle on the very next line.

    Returns the table of contents and the Markdown with numbered, anchored headings.
    """
    lines = body.splitlines()
    toc, out, used = [], [], set()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m and not line.startswith("###"):
            title = m.group(1)
            sub = ""
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if nxt.strip() and not re.match(r"^\s*([#>|!\-*+`]|\d+\.)", nxt):
                sub = nxt.strip()
                i += 1
            anchor = slugify(title)
            while anchor in used:
                anchor += "-1"
            used.add(anchor)
            n = len(toc) + 1
            toc.append({"n": n, "title": render_inline(title), "sub": render_inline(sub), "id": anchor})
            out.append(f'<h2 id="{anchor}"><span class="num">{n}.</span> {render_inline(title)}</h2>')
            if sub:
                out.append(f'<p class="section-sub">{render_inline(sub)}</p>')
            out.append("")
        else:
            out.append(line)
        i += 1
    return toc, "\n".join(out)


def render_inline(text: str) -> str:
    rendered = render_markdown(text)
    return re.sub(r"^<p>(.*)</p>$", r"\1", rendered.strip(), flags=re.S)


FIG_RE = re.compile(r'<p>\s*<img alt="([^"]*)" src="([^"]+)"(?: title="([^"]*)")?\s*/?>\s*</p>')


def figures(html_text: str, src_dir: Path, where: str) -> str:
    """A paragraph holding only an image becomes a <figure>; the image title is its caption."""

    def repl(m):
        alt, src, cap = m.group(1), m.group(2), m.group(3)
        attrs = ""
        if not re.match(r"^(https?:)?//", src):
            p = src_dir / src
            if not p.exists():
                err(f"{where}: figure '{src}' not found next to index.md")
            else:
                size = image_size(p)
                if size:
                    attrs = f' width="{size[0]}" height="{size[1]}"'
        if not alt:
            err(f"{where}: figure '{src}' has no alt text (![alt text](file.png \"caption\"))")
        img = f'<img src="{src}" alt="{alt}"{attrs} loading="lazy">'
        figcap = f"<figcaption>{cap}</figcaption>" if cap else ""
        return (f'<figure><button class="zoomable" type="button" aria-label="Enlarge figure">'
                f"{img}</button>{figcap}</figure>")

    return FIG_RE.sub(repl, html_text)


def wrap_tables(html_text: str) -> str:
    return html_text.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")


# --------------------------------------------------------------------------- content

def load_site() -> dict:
    site = yaml.safe_load((ROOT / "site.yml").read_text(encoding="utf-8")) or {}
    for key in ("name", "url", "base_path"):
        if not site.get(key):
            err(f"site.yml: '{key}' is required")
    site["about_html"] = render_markdown(site.get("about") or "")
    site["social"] = site.get("social") or []
    site["keywords"] = site.get("keywords") or []
    for key in ("cv", "photo"):
        if site.get(key) and not (STATIC / site[key]).exists():
            err(f"site.yml: {key} '{site[key]}' not found in static/")
    return site


def load_projects(include_drafts: bool) -> list[dict]:
    projects = []
    for md in sorted(PROJECTS.glob("*/index.md")):
        slug = md.parent.name
        where = f"content/projects/{slug}/index.md"
        meta, body = split_front_matter(md.read_text(encoding="utf-8"), where)
        if meta.get("draft") and not include_drafts:
            continue
        for f in REQUIRED_PROJECT_FIELDS:
            if not meta.get(f):
                err(f"{where}: front matter field '{f}' is required")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug):
            err(f"{where}: folder name must be lowercase letters, digits and dashes")
        stash: list[str] = []
        if meta.get("math"):
            body, stash = protect_math(body)
        toc, body_md = parse_sections(body)
        body_html = wrap_tables(figures(render_markdown(body_md), md.parent, where))
        body_html = restore_math(body_html, stash)
        for item in toc:
            item["title"] = restore_math(item["title"], stash)
            item["sub"] = restore_math(item["sub"], stash)
        cover = meta.get("cover")
        if cover and not (md.parent / cover).exists():
            err(f"{where}: cover '{cover}' not found")
        projects.append({
            "slug": slug,
            "url": f"projects/{slug}/",
            "kind": "Project",
            "title": meta.get("title", slug),
            "label": meta.get("label", slug),
            "summary": meta.get("summary", ""),
            "date": to_date(meta.get("date"), where),
            "updated": to_date(meta.get("updated"), where),
            "context": meta.get("context", ""),
            "period": meta.get("period", ""),
            "repo": meta.get("repo", ""),
            "paper": meta.get("paper", ""),
            "tags": meta.get("tags") or [],
            "cover": cover,
            "math": bool(meta.get("math")),
            "draft": bool(meta.get("draft")),
            "toc": toc,
            "html": body_html,
            "dir": md.parent,
        })
    projects.sort(key=lambda p: p["date"] or dt.date.min, reverse=True)
    return projects


def load_notes() -> list[dict]:
    path = CONTENT / "notes.yml"
    if not path.exists():
        return []
    notes = yaml.safe_load(path.read_text(encoding="utf-8")) or []
    out = []
    for i, n in enumerate(notes, 1):
        where = f"content/notes.yml entry {i}"
        for f in ("title", "url", "date"):
            if not n.get(f):
                err(f"{where}: '{f}' is required")
        out.append({**n, "kind": "Note", "date": to_date(n.get("date"), where),
                    "updated": None, "external": bool(re.match(r"^https?://", str(n.get("url", ""))))})
    out.sort(key=lambda n: n["date"] or dt.date.min, reverse=True)
    return out


# --------------------------------------------------------------------------- render

def check_internal_links(out_dir: Path) -> None:
    for page in out_dir.rglob("*.html"):
        if page.name == "404.html":
            continue
        text = page.read_text(encoding="utf-8")
        for ref in re.findall(r'(?:href|src)="([^"#?]+)', text):
            if re.match(r"^(https?:|mailto:|data:|//)", ref):
                continue
            target = (page.parent / ref).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.exists():
                err(f"{page.relative_to(out_dir)}: broken link '{ref}'")


def build(include_drafts: bool = False) -> None:
    errors.clear()
    site = load_site()
    projects = load_projects(include_drafts)
    notes = load_notes()
    if errors:
        raise BuildError()

    env = Environment(loader=FileSystemLoader(TEMPLATES), autoescape=True,
                      trim_blocks=True, lstrip_blocks=True)
    env.filters["date"] = fmt_date

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(STATIC, OUT)
    (OUT / ".nojekyll").write_text("")

    today = dt.date.today()
    has_notes = bool(notes)
    nav = [("Home", "index.html", "home"), ("Projects", "projects.html", "projects")]
    if has_notes:
        nav.append(("Notes", "notes.html", "notes"))
    if site.get("cv"):
        nav.append(("CV", "cv.html", "cv"))

    def render(template: str, dest: str, **ctx) -> None:
        depth = dest.count("/")
        root = "../" * depth
        page = env.get_template(template).render(site=site, nav=nav, root=root, year=today.year, **ctx)
        path = OUT / dest
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page, encoding="utf-8")

    latest = sorted(projects + notes, key=lambda e: e["updated"] or e["date"] or dt.date.min,
                    reverse=True)[: int(site.get("latest") or 4)]

    render("home.html", "index.html", active="home", latest=latest, projects=projects, notes=notes, title=None)
    if site.get("cv"):
        render("cv.html", "cv.html", active="cv", title="CV")
    render("projects.html", "projects.html", active="projects", projects=projects, title="Projects")
    if has_notes:
        render("notes.html", "notes.html", active="notes", notes=notes, title="Notes")
    render("404.html", "404.html", active="", title="Page not found")

    for p in projects:
        dest_dir = OUT / "projects" / p["slug"]
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in p["dir"].iterdir():
            if f.name != "index.md" and not f.name.startswith("."):
                (shutil.copytree if f.is_dir() else shutil.copy2)(f, dest_dir / f.name)
        render("project.html", f"projects/{p['slug']}/index.html", active="projects", p=p, title=p["title"])

    urls = ["", "projects.html"] + (["notes.html"] if has_notes else []) + (["cv.html"] if site.get("cv") else []) + [p["url"] for p in projects]
    sitemap = "\n".join(f"  <url><loc>{html.escape(site['url'] + u)}</loc></url>" for u in urls)
    (OUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + sitemap + "\n</urlset>\n")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {site['url']}sitemap.xml\n")

    check_internal_links(OUT)
    if errors:
        raise BuildError()
    print(f"Built {len(projects)} project(s), {len(notes)} note(s) into {OUT.relative_to(ROOT)}/")


def serve(port: int) -> None:
    import functools
    import http.server

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
    print(f"Serving on http://localhost:{port}/  (Ctrl+C to stop; re-run the build after edits)")
    http.server.ThreadingHTTPServer(("", port), handler).serve_forever()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--drafts", action="store_true", help="include projects marked draft: true")
    ap.add_argument("--serve", action="store_true", help="serve _site/ after building")
    ap.add_argument("--port", type=int, default=8000)
    args = ap.parse_args()
    try:
        build(include_drafts=args.drafts)
    except BuildError:
        print("Build failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    if args.serve:
        serve(args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
