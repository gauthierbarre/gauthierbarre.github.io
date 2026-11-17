#!/usr/bin/env python3
"""Create an entry in a lighter section.

  python scripts/new_entry.py hands-on my-slug "Title" [--ipynb path/to/analysis.ipynb]
  python scripts/new_entry.py notes    my-slug "Title" [--press https://article-url]
  python scripts/new_entry.py personal my-slug "Title"

Hands-On: a README-style page; with --ipynb the notebook is copied next to it and rendered
below the text (Markdown cells, code, outputs, figures).
Notes: a short article in Markdown; with --press it comments a press article (shown as a card).
Personal: an essay or text unrelated to finance (philosophy, sport, ...).
The entry is created as a draft: write it, remove `draft: true`, then build.
"""
import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HANDS_ON = """---
title: {title}
summary: One sentence shown in the list.
topic: ""            # short category, e.g. "Time series", "Risk"
date: {today}
# source: "repo · file.ipynb"   # where it comes from
# repo: https://github.com/gauthierbarre/...
{nb_line}# hide_code: true    # show only the notebook's text and outputs
draft: true          # remove this line to publish
---

A few lines of context: what this notebook / README shows and why it is worth reading.
Markdown, tables, figures (`![alt](file.png "caption")`) and $\\LaTeX$ work here.
"""

NOTE = """---
title: {title}
summary: One sentence shown in the list.
topic: ""            # e.g. "Markets", "Quant research", "AI in finance"
date: {today}
{press}draft: true          # remove this line to publish
---

Your text in Markdown. For a press article: a short summary in your own words, then your view —
what it gets right, what it misses, what it means for markets or for quant research.
"""

PERSONAL = """---
title: {title}
summary: One sentence shown in the list.
topic: ""            # e.g. "Philosophy", "Sport"
date: {today}
draft: true          # remove this line to publish
---

Your text in Markdown.
"""

PRESS = """press:               # the article you comment on (shown as a card under the title)
  url: {url}
  title: ""          # article title
  outlet: ""         # e.g. Financial Times, Les Echos, Bloomberg
  date: ""           # e.g. 12 Nov 2026
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("section", choices=["hands-on", "notes", "personal"])
    ap.add_argument("slug")
    ap.add_argument("title", nargs="?", default="Title")
    ap.add_argument("--ipynb", help="hands-on: path to a .ipynb to copy and render")
    ap.add_argument("--press", help="notes: URL of the press article this note comments on")
    args = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.slug):
        print("slug must be lowercase letters, digits and dashes", file=sys.stderr)
        return 1
    folder = ROOT / "content" / args.section / args.slug
    if folder.exists():
        print(f"{folder.relative_to(ROOT)} already exists", file=sys.stderr)
        return 1
    title = '"' + args.title.replace('"', "'") + '"'
    today = dt.date.today().isoformat()
    if args.section == "hands-on":
        nb_line = ""
        if args.ipynb:
            src = Path(args.ipynb).expanduser()
            if src.suffix != ".ipynb" or not src.exists():
                print(f"{src} is not an existing .ipynb file", file=sys.stderr)
                return 1
            folder.mkdir(parents=True)
            shutil.copy2(src, folder / src.name)
            nb_line = f"notebook: {src.name}\n"
        text = HANDS_ON.format(title=title, today=today, nb_line=nb_line)
    elif args.section == "personal":
        text = PERSONAL.format(title=title, today=today)
    else:
        text = NOTE.format(title=title, today=today, press=PRESS.format(url=args.press) if args.press else "")
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "index.md").write_text(text, encoding="utf-8")
    print(f"Created {folder.relative_to(ROOT)}/index.md (draft). Preview with: make serve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
