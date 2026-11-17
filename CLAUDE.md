# CLAUDE.md

Static portfolio site built by `scripts/build.py` (Markdown + YAML + Jinja2) into `_site/`,
deployed to GitHub Pages by `.github/workflows/deploy.yml`. See README.md for the full layout.

## Rules

- Content lives in `site.yml`, `content/projects/<slug>/index.md` and `content/notes.yml`.
  Do not hand-edit `_site/` (generated, gitignored).
- To add a project from a GitHub repository, use the `add-project` skill
  (`.claude/skills/add-project/SKILL.md`).
- Only publish numbers, claims and figures that appear in the source repository's README or
  executed notebooks. Never invent results, dates or affiliations.
- Site language is English; tone is sober and factual (no marketing adjectives).
- Every figure needs descriptive alt text and a caption.
- After any change: `make build` must pass (it validates fields, figures and internal links),
  then check the page with `make serve` (launch config `portfolio` in `.claude/launch.json`),
  at desktop and mobile width.
- Commit only when asked; pushing to `main` publishes the site.
