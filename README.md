# portefolio

Personal portfolio of Gauthier Barre — quantitative finance, research and systematic strategies.

**Live site:** https://gauthierbarre.github.io/portefolio/

A small static site generator (Python + Markdown + Jinja2). Each project is one folder with a
Markdown file and its figures; a GitHub Actions workflow builds and publishes the site on every
push to `main`.

## Layout

```
site.yml                          name, headline, status, about, keywords, email, links, CV PDF
content/projects/<slug>/index.md  one project: front matter + sections + figures in the same folder
content/notes.yml                 short technical notes (links to notebook sections, PDFs, …)
static/                           copied as-is: css/, js/, favicon.svg, cv.pdf
templates/                        page layouts (base, home, projects, project, notes, 404) and icons
scripts/build.py                  builds _site/ and validates it
scripts/new_project.py            scaffolds a new project
.github/workflows/deploy.yml      build on push/PR, deploy main to GitHub Pages
```

Pages: **Home** (About, project cards, Contact) · **Projects** · one page per project with a
numbered table of contents · **Notes** · **CV** (the PDF shown in the page, with a download button).

## Commands

```bash
make install                      # once: .venv + dependencies
make serve                        # build with drafts and serve on http://localhost:8000
make build                        # production build into _site/ (what CI runs)
make new SLUG=my-project TITLE='Does X beat Y?' REPO=https://github.com/gauthierbarre/my-project
```

## Add a project

1. `make new SLUG=my-project TITLE='…'` creates `content/projects/my-project/index.md` as a draft.
2. Copy the figures (PNG/JPG/SVG, ≈ 900–1100 px wide) into the same folder.
3. Fill in the front matter and the sections, then delete the `draft: true` line.
4. `make serve` to check, then commit and push. CI builds, validates and deploys.

### Front matter

| Field | Required | Meaning |
|---|---|---|
| `title` | yes | Page title; a question or a claim reads best |
| `summary` | yes | One sentence for lists and link previews |
| `date` | yes | `YYYY-MM-DD`, used for ordering and “Latest” |
| `updated` | | `YYYY-MM-DD`, shown as “updated …” |
| `label` | | Short mono label above the title (defaults to the folder name) |
| `context`, `period` | | e.g. `MaQI Hackathon 1`, `2011–2024` |
| `repo`, `paper` | | Links shown under the title |
| `cover` | | Figure used as the link-preview image |
| `tags` | | Tools, listed at the bottom |
| `math` | | `true` renders `$…$` and `$$…$$` with KaTeX (avoid bare `$` signs in that page) |
| `draft` | | `true` hides the project from the production build |

### Body conventions

- `## Section title` starts a numbered section; the **next line** (optional) is its subtitle,
  shown in the table of contents. Leave a blank line before the body.
- A figure is an image alone on its line:
  `![Alt text describing the figure.](file.png "Caption shown under it.")` — the alt text is required.
- Tables, lists, code blocks and footnotes are standard Markdown.
- Only publish numbers that appear in the project's README or executed notebooks.

## Other edits

- **Home page text, keywords, links:** `site.yml`.
- **Note:** add an entry to `content/notes.yml`.
- **CV:** replace `static/cv.pdf`.
- **Availability line:** `status:` in `site.yml` (empty hides it).
- **Colours and fonts:** variables at the top of `static/css/style.css`.

## Deployment

`.github/workflows/deploy.yml` builds on every push and pull request; on `main` it deploys
`_site/` to GitHub Pages. The build fails — and nothing is deployed — on a missing required field,
a missing figure or a broken internal link.

One-time setting: **Settings → Pages → Build and deployment → Source: GitHub Actions.**

## Content sources

- [US-equity-signals](https://github.com/gauthierbarre/US-equity-signals) — README and executed `02_strategy.ipynb`.
- [sp500-composition](https://github.com/gauthierbarre/sp500-composition) — README and `figures/`.

Underlying data (S&P Global Compustat via the MaQI platform) is licensed and is not included here.
