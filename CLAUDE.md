# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal CV/resume website for Bohdan Sukhomlinov, hosted on GitHub Pages with a custom domain (cv.dnull.systems). The site uses an automated template-based generation system that pulls technical skills from Notion and combines them with local YAML data files.

## Architecture

**Hybrid Data System:**
- **Local YAML files** (`data/`) - Version-controlled content for experience, projects, education, etc.
- **Notion Database** - Source of truth for technical skills (auto-synced)
- **Jinja2 Template** (`templates/index.html.j2`) - HTML template with styling
- **Generated Output** (`index.html`) - Deployed to GitHub Pages

**Directory Structure:**
```
cv/
├── data/                       # YAML data files (edit these to update CV)
│   ├── personal.yaml           # Name, contact, summary
│   ├── experience.yaml         # Job history
│   ├── projects.yaml           # Projects with tech stacks
│   ├── skills.yaml             # Auto-generated from Notion
│   ├── education.yaml          # Degrees
│   ├── languages.yaml          # Language proficiencies
│   └── volunteer.yaml          # Volunteer work
├── scripts/                    # Python generation scripts
│   ├── fetch_notion_skills.py  # Pull skills from Notion → skills.yaml
│   └── generate_html.py        # Render template → index.html
├── templates/
│   └── index.html.j2           # Jinja2 template
├── .github/workflows/          # CI/CD automation
│   ├── update-skills.yml       # Fetch skills from Notion
│   ├── generate-html.yml       # Generate index.html
│   ├── generate-pdf.yml        # Create PDF from HTML
│   └── release.yml             # Orchestrator (runs on release)
├── index.html                  # Generated output (deployed)
├── requirements.txt            # Python dependencies
└── CNAME                       # GitHub Pages domain config
```

## Development Workflow

**Making Content Updates:**

1. **To update CV content** (experience, projects, etc.):
   - Edit the appropriate YAML file in `data/`
   - Commit and push to `main`
   - Manually run "Generate HTML" workflow OR create a release

2. **To update technical skills**:
   - Update skills in Notion database: https://www.notion.so/dnull/ce553f61f831464eb05592124282802f
   - Manually run "Update Skills from Notion" workflow OR create a release
   - Skills are fetched, `data/skills.yaml` is auto-generated and committed

3. **To regenerate HTML locally**:
   ```bash
   pip install -r requirements.txt
   python scripts/generate_html.py
   ```

4. **To fetch skills locally**:
   ```bash
   export NOTION_API_KEY="your_token"
   python scripts/fetch_notion_skills.py
   ```

## Automated Workflows

**Individual Workflows** (can be run manually or called by release):
- `update-skills.yml` - Fetches skills from Notion, commits `skills.yaml`
- `generate-html.yml` - Renders Jinja2 template, commits `index.html`
- `generate-pdf.yml` - Converts HTML to PDF, attaches to release

**Release Workflow** (runs on GitHub release):
1. Update skills from Notion
2. Generate new index.html
3. Generate PDF
4. Deploy to GitHub Pages
5. Attach PDF to release

**Triggering a Full Build:**
- Create a new GitHub release (uses semantic versioning)
- All workflows run automatically in sequence
- PDF is attached to the release
- Site is deployed to cv.dnull.systems

## Data File Structure

**YAML Format Guidelines:**

- `personal.yaml` - Contact info and professional summary
- `experience.yaml` - List of jobs with responsibilities
- `projects.yaml` - Projects with emoji, technologies, and description
- `skills.yaml` - Auto-generated from Notion (top 10 per category by proficiency)
- `education.yaml` - Degrees and institutions
- `languages.yaml` - Languages with proficiency levels
- `volunteer.yaml` - Volunteer work description

See existing files for structure examples.

## Skills System

**Notion Integration:**
- Technical skills are maintained in Notion database (ID: ce553f61f831464eb05592124282802f)
- Skills have: Name, Category, Proficiency (1-10)
- Script fetches top 10 skills per category sorted by proficiency
- Output is written to `data/skills.yaml`

**Skills Rating Scale:**
- 1-10 numeric scale (displayed as X/10)
- Visual progress bars at 10% width per point
- Categories include: Cloud Platforms, Orchestration, IaC, CI/CD, Monitoring, etc.

## Deployment

**GitHub Pages:**
- Deployed from `main` branch
- Custom domain: cv.dnull.systems (configured via CNAME)
- Automatic deployment on release via `release.yml` workflow

**PDF Generation:**
- Uses Playwright/Chromium for rendering
- Preserves print styles from template
- Attached to GitHub releases for easy download
- Professional format for recruiters

## Important Notes

- `index.html` is auto-generated - DO NOT edit directly
- Edit YAML files in `data/` instead
- Skills come from Notion - update there, not in YAML
- Notion API key stored in GitHub Secrets as `NOTION_API_KEY`
- Template preserves original design with inline CSS
- Responsive design with mobile breakpoints at 600px
- Print-optimized styles using `@media print`
