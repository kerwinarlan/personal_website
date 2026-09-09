# Personal Website

Portfolio of Kerwin Dio Joseph Arlan — Civil Engineering candidate at UP Diliman specializing in GIS, hydrodynamic modeling, data analysis, and AI operations.

Live at: https://kerwinarlan.github.io/personal_website/

## Tech Stack & Design System

- **Vanilla HTML5 & Modern CSS3** — custom property design tokens, dark/light theme switching, glassmorphism surfaces
- **Interactive macOS Terminal** — interactive shell window with live prompt commands (`whoami`, `status`, `stack`, `projects`, `contact`)
- **Vanilla JavaScript** — zero framework dependencies, fast load time
- **GitHub Pages & Actions** — automated deployment workflow (`.github/workflows/deploy-gh-pages.yml`) deploying on every push to `main`

## Key Features

- **Interactive Terminal Hero Component** — run commands directly in the embedded shell or click quick prompt pills
- **Light/Dark theme toggle** — persisted in `localStorage`
- **⌘K / Ctrl+K command palette** — keyboard-driven modal navigation
- **Liquid-card spotlight effects** — pointer-tracked hover glow and subtle 3D tilt
- **Live Asia/Manila Clock** — real-time PHT clock with pulse status dot
- **Filterable Repositories Showcase** — category tabs (Python & ML, Civil & Hydro, Web & Tools) and live search
- **WCAG Accessibility & Motion Safeguards** — skip links, explicit `:focus-visible` rings, `@media (prefers-reduced-motion: reduce)` fallback

## Syncing Projects

`projects.json` is regenerated automatically every Monday (03:17 UTC) and on demand by the `sync-projects` GitHub Action.

To force a sync manually:

```bash
python3 build_projects.py --verbose   # then commit projects.json
```

## Building the Resume PDF

`resume.pdf` is generated from `resume.html` via headless Chrome/Chromium:

```bash
./build_resume.sh
```

## Run Locally

```bash
python3 -m http.server 8080
# visit http://localhost:8080
```

## Repository Structure

```
index.html          - single-page portfolio (markup, styles, script)
resume.html         - printable resume source page
resume.pdf          - generated resume PDF artifact
build_projects.py   - CLI tool syncing repositories from GitHub API
build_resume.sh     - cross-platform script building resume.pdf
projects.json       - project data payload consumed by the showcase
.github/workflows/  - GitHub Actions deployment & sync workflows
```
