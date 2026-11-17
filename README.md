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
content/hands-on/<slug>/index.md  Hands-On: a README-style page, optionally rendering a .ipynb
content/notes/<slug>/index.md     Notes: short articles, comments on press articles, opinion
content/<section>/links.yml       optional entries that only link elsewhere
static/                           copied as-is: css/, js/, favicon.svg, cv.pdf
templates/                        page layouts (base, home, projects, project, notes, 404) and icons
scripts/build.py                  builds _site/ and validates it
scripts/new_project.py            scaffolds a new project
.github/workflows/deploy.yml      build on push/PR, deploy main to GitHub Pages
```

Pages: **Home** (About, Projects, latest Hands-On and Notes, Contact) · **Projects** · one page per
project with a contents column · **Hands-On** (notebooks, READMEs) · **Notes** (articles, opinion) · **CV** (the PDF shown in the page, with a
download button). On wide screens every page uses a label column on the left and content on the right.

## Commands

```bash
make install                      # once: .venv + dependencies
make serve                        # build with drafts and serve on http://localhost:8000
make build                        # production build into _site/ (what CI runs)
make new SLUG=my-project TITLE='Does X beat Y?' REPO=https://github.com/gauthierbarre/my-project
make hands-on SLUG=my-entry TITLE='…' NB=~/path/to/analysis.ipynb   # Hands-On entry, NB optional
make note SLUG=my-note TITLE='…' URL=https://press-article           # Notes entry, URL optional
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

## Add a Hands-On entry (notebook / README, lighter than a project)

1. `make hands-on SLUG=my-entry TITLE='…' NB=path/to/file.ipynb` creates
   `content/hands-on/my-entry/index.md` (draft) and copies the notebook next to it. Without `NB`,
   write the page in Markdown (paste a README).
2. Write a few lines of context, set `topic` and `summary`, delete `draft: true`.
3. The entry page shows the text as an abstract, with **View the notebook** (a separate, readable
   page: contents column, foldable code cells, scrollable logs, zoomable figures) and **Download .ipynb**.
   `hide_code: true` shows only text and outputs in the viewer.
4. Make sure the notebook's outputs contain nothing licensed (raw data tables) before publishing.

## Add a Note (article, comment on the press, opinion)

1. `make note SLUG=my-note TITLE='…' URL=https://…` creates `content/notes/my-note/index.md` (draft).
   With `URL`, the note comments a press article: fill `press.title`, `press.outlet`, `press.date`;
   it is shown as a card under the title, linking to the article.
2. Write the text in Markdown: summarise the article in your own words (no long quotes), then your view.
3. Delete `draft: true`, build, push.

Hands-On and Notes sit under the **Collection** menu (a dropdown, and an overview page at `collection/`).
On the home page they appear once they have a published entry. Their names are `collection_title`,
`hands_on_title` and `notes_title` in `site.yml`; the one-line descriptions are `hands_on_blurb` and
`notes_blurb` (defaults in `scripts/build.py`). An entry that only links elsewhere can go
in `content/<section>/links.yml` (fields: date, title, url, topic, summary, source).

## Other edits

- **Home page text, keywords, links:** `site.yml`.
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
