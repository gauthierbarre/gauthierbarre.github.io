---
name: add-project
description: Add or update a project page on the portfolio from a GitHub repository (or local folder) — reads its README/notebooks, copies figures, writes content/projects/<slug>/index.md, builds and checks it. Use when the user asks to add, import, publish or refresh a project on the portfolio.
---

# Add a project to the portfolio

Input: a repository (`owner/name` or URL) or a local path, optionally a slug and a title.

## 1. Read the source

- `gh repo view <owner/name> --json name,description,createdAt,pushedAt,url` for the date and links.
- Read the README, then the executed notebooks / reports it points to
  (`gh api repos/<owner>/<name>/contents/<path>` or a shallow clone into the scratchpad).
- List figures (`figures/`, `img/`, notebook outputs). Prefer the ones the README itself shows.
- Note every number you intend to publish **with where it comes from**. Nothing else gets published.

## 2. Scaffold

```bash
make new SLUG=<repo-name-lowercase> TITLE='<question or claim>' REPO=<url>
```

Copy the chosen figures (3–5, PNG ≈ 900–1100 px wide) next to `index.md`.

## 3. Write the page

Follow the structure of the existing pages (`content/projects/us-equity-signals/index.md`):

1. **The question** — the problem in plain words.
2. **The data** — source, sample, period, cleaning (say if data is licensed / not redistributed).
3. **The method** — steps, in order.
4. **Results** — a Markdown table of verified numbers + figures.
5. **What this teaches** — takeaways, then limitations and caveats stated honestly.
6. **References** — code, paper, data.

Rename sections when the project calls for it, but keep: one `##` per section, a one-line
lowercase subtitle on the next line, a blank line, then the body. Front matter: `title`,
`summary` (one sentence with the main finding), `date` (repo creation or first result date),
`context`, `period`, `repo`, `cover`, `tags`; `math: true` if formulas are needed. Remove
`draft: true` only when the user wants it published.

Optionally add 1–3 entries to `content/notes.yml` pointing at notebook sections worth reading.

## 4. Check

```bash
make build                      # must print "Built N project(s)…"
```

Then preview (`preview_start` with name `portfolio`), open `/projects/<slug>/`, check the table
of contents, tables, figures and the mobile width (no horizontal scroll). Fix and rebuild.

## 5. Hand back

Summarise what was added and which numbers came from which file; list anything left out or
uncertain. Commit/push only if the user asks (pushing to `main` deploys the site).
