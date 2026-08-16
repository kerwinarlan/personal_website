# Personal Website

Portfolio of Kerwin Dio Joseph Arlan - engineering, data, and operations.

Live at: https://kerwinarlan.github.io/personal-website/

## Tech Stack

- **Vanilla HTML5** - semantic markup, no framework
- **Modern CSS** - custom property design tokens, dark/light themes, glassmorphism
- **Vanilla JavaScript** - zero dependencies
- **Zero build step** - the page opens directly in any browser
- **GitHub Pages** - deployed as a static site from the `main` branch

## Key Features

- **Light/Dark theme toggle** - persisted in `localStorage`
- **Ctrl+K command palette** - keyboard-driven navigation to every section and project
- **Liquid-card effects** - pointer-tracked hover glow on glass surfaces
- Scroll-reveal animations with `prefers-reduced-motion` support
- Live Asia/Manila clock and scrollspy navigation
- Accessible: skip link, ARIA labels, focus-visible styles, semantic landmarks
- **Auto-synced projects grid** - long-tail projects render from `projects.json`

## Syncing Projects

The featured cards are hand-authored because they carry trace logs and live
embeds. Everything else renders from `projects.json` at runtime.

Regenerate the data and commit the result:

```bash
python3 build_projects.py
```

The script pulls your public repos from the GitHub API and applies a curated
exclude/allow list. Repo descriptions and topics become card copy, so write
good ones.

## Building the Resume PDF

`resume.pdf` is generated from `resume.html` - never edited by hand:

```bash
./build_resume.sh   # headless Chrome renders resume.html to resume.pdf
```

Run it after any resume.html edit and commit the regenerated PDF.

## Run Locally

```bash
python3 -m http.server 8080
# visit http://localhost:8080
```

## Structure

```
index.html          - single-page portfolio (markup, styles, script)
resume.html         - printable resume page (source of truth)
resume.pdf          - generated from resume.html by build_resume.sh
build_projects.py   - regenerates projects.json from the GitHub API
build_resume.sh     - regenerates resume.pdf from resume.html
projects.json       - project data consumed by the auto-synced grid
assets/             - project preview media
```
