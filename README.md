# portefolio

Personal portfolio of Gauthier Barre — quantitative finance, research and systematic strategies.

**Live site:** https://gauthierbarre.github.io/portefolio/

Plain HTML, CSS and a few lines of JavaScript: no build step, no framework, no backend.

## Structure

```
index.html                  the whole site (Home, Projects, Notes, Skills, About)
404.html                    not-found page (absolute /portefolio/ paths)
assets/css/style.css        styles; colours and fonts are CSS variables at the top
assets/js/main.js           mobile menu, active nav link, reveal animation, figure lightbox
assets/img/<project>/       figures, copied from each project's repository or notebook outputs
assets/favicon.svg
robots.txt, sitemap.xml     basic SEO
.nojekyll                   serve files as-is (no Jekyll processing)
```

All paths in `index.html` are **relative** (`assets/...`), so the site works both locally and under
the `/portefolio/` sub-path on GitHub Pages. Only `404.html` uses absolute `/portefolio/...` paths,
because GitHub serves it from any URL depth.

## Preview locally

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000/.

## Common edits

### Add or update a project

1. Put its figures in `assets/img/<project-name>/` (PNG, ideally ≤ 1100 px wide).
2. In `index.html`, copy an existing `<article class="project">` block inside `#projects` and edit:
   - `project-meta` (domain · context · period) and the `<h3>` title;
   - the repository link;
   - **Problem**, **Methodology**, **Verified results** (a `<table>` or the `.kpis` cards), **Takeaways**;
   - the `.tags` list (technologies);
   - the `<figure>` blocks: set `src`, a descriptive `alt`, and the image `width`/`height`.
3. Only publish numbers that appear in the project's README or executed notebooks.

### Add a technical note

Copy an `<li class="note">` in `#notes`. Set the topic, title, link (a notebook section, a PDF in
`assets/`, or a new HTML page next to `index.html`), a one-line summary and the source line.

### Add LinkedIn, e-mail or a CV

- **CV:** add `assets/cv.pdf`, then add a button in `.hero-actions`:
  `<a class="btn" href="assets/cv.pdf">CV</a>`
- **LinkedIn / e-mail:** add a button in `.hero-actions` and an `<li>` in the `.contact` list
  (placeholders are marked with HTML comments). Remember to add the LinkedIn URL to `sameAs`
  in the JSON-LD block of `<head>`.

### Change colours or fonts

Edit the variables in `:root` at the top of `assets/css/style.css`.

## Deployment

GitHub Pages is set to **Deploy from a branch → `main` / `(root)`** (Settings → Pages).
Every push to `main` republishes the site automatically; progress is visible in the repository's
**Actions** tab ("pages build and deployment") and the site updates about a minute later.
`.nojekyll` makes GitHub serve the files as they are.

## Content sources

- [US-equity-signals](https://github.com/gauthierbarre/US-equity-signals) — README and executed `02_strategy.ipynb`.
- [sp500-composition](https://github.com/gauthierbarre/sp500-composition) — README and `figures/`.

Underlying data (S&P Global Compustat via the MaQI platform) is licensed and is not included here.
