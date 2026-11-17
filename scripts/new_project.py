#!/usr/bin/env python3
"""Create a new project page from a template.

  python scripts/new_project.py my-project "Title as a question or claim" [--repo URL]

Creates content/projects/my-project/index.md marked `draft: true`. Put the figures in
the same folder, write the sections, remove `draft: true`, then build.
"""
import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TEMPLATE = """---
title: {title}
label: {slug}
summary: One sentence that says what the project finds, shown in lists and link previews.
date: {today}
# updated: YYYY-MM-DD
context: ""        # e.g. "MaQI Hackathon 2", "Course project", "Personal"
period: ""         # e.g. "2011–2024" (sample period), optional
repo: {repo}
cover: ""          # file name of the main figure, used as the link-preview image
tags: [Python]
math: false        # true enables $inline$ and $$display$$ LaTeX (KaTeX)
draft: true        # remove this line to publish
---

## The question
one short line, shown in the table of contents

What problem does this project answer, and why does it matter?

## The data
where it comes from, and what was cleaned

- Source, sample, period.

## The method
what was done, in order

- Step one.

## Results
the numbers that answer the question

| Model | Metric |
|-------|-------:|
| Baseline | 0.00 |

![Alt text describing what the figure shows.](figure.png "Caption under the figure.")

## What this teaches
and what it does not show

Takeaways, then limitations.

## References
code and data

- Code: [{slug}]({repo})
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", help="folder / URL name: lowercase letters, digits and dashes")
    ap.add_argument("title", nargs="?", default="Project title")
    ap.add_argument("--repo", default="")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", args.slug):
        print("slug must be lowercase letters, digits and dashes", file=sys.stderr)
        return 1
    folder = ROOT / "content" / "projects" / args.slug
    if folder.exists():
        print(f"{folder.relative_to(ROOT)} already exists", file=sys.stderr)
        return 1
    folder.mkdir(parents=True)
    repo = args.repo or f"https://github.com/gauthierbarre/{args.slug}"
    title = args.title.replace('"', "'")
    (folder / "index.md").write_text(
        TEMPLATE.format(title=f'"{title}"', slug=args.slug, repo=repo, today=dt.date.today().isoformat()),
        encoding="utf-8")
    print(f"Created {folder.relative_to(ROOT)}/index.md (draft). Preview with: make serve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
