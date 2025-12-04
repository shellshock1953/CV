# Bohdan Sukhomlinov - CV

**Senior DevOps Engineer | Platform Engineer | SRE**

🌐 **Live Site:** [cv.dnull.systems](https://cv.dnull.systems)
📄 **Latest PDF:** [Download CV](https://github.com/shellshock1953/cv/releases/latest/download/cv_bohdan_sukhomlinov.pdf)

---

## Overview

Automated CV/resume system with Notion integration for skills and GitHub Actions for deployment.

**Stack:** YAML + Jinja2 + Notion API + GitHub Actions + GitHub Pages

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate HTML
python scripts/generate_html.py

# Fetch skills from Notion
export NOTION_API_KEY="your_token"
python scripts/fetch_notion_skills.py
```

## Making Updates

**Update content:** Edit YAML files in `data/` → Commit to main → Run "Generate HTML" workflow

**Update skills:** Modify [Notion database](https://www.notion.so/dnull/ce553f61f831464eb05592124282802f) → Run "Update Skills" workflow

**Full deployment:** Create GitHub release (`v0.0.x`) → Automated pipeline:
1. Fetches skills from Notion (top 8/category, excludes 0 proficiency)
2. Generates index.html
3. Creates PDF (attached to release)
4. Deploys to GitHub Pages

## Architecture

```
Notion DB + Local YAML → Jinja2 Template → index.html → GitHub Pages
                                         ↓
                                   PDF (release asset)
```

**Key Files:**
- `data/*.yaml` - CV content (edit these)
- `data/skills.yaml` - Auto-generated from Notion
- `templates/index.html.j2` - Jinja2 template (2-column compact grid)
- `scripts/fetch_notion_skills.py` - Notion sync (top 8 per category)
- `scripts/generate_html.py` - HTML generator
- `.github/workflows/*.yml` - Automated workflows

## Features

✅ Notion integration for skills (auto-sync, excludes 0 proficiency)
✅ PDF generation via Playwright (attached to releases)
✅ Compact 2-column grid design (0.75em fonts, tight spacing)
✅ Responsive layout (breakpoints: 900px, 600px)
✅ Modular GitHub Actions workflows
✅ Custom domain (cv.dnull.systems)

## Required Secrets

- `NOTION_API_KEY` - Notion integration token
- `PAT_TOKEN` - Personal Access Token (repo + workflow scopes)

## Tech Stack

Jinja2 • YAML • Notion API • GitHub Actions • Playwright • GitHub Pages

---

**Last Updated:** December 2024
