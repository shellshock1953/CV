# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal CV/resume website for Bohdan Sukhomlinov, hosted on GitHub Pages with a custom domain (cv.dnull.systems). The site uses an automated template-based generation system that pulls technical skills from Notion and combines them with local YAML data files.

## Architecture

**Hybrid Data System:**
- **Local YAML files** (`data/`) - Version-controlled content for experience, projects, education, etc.
- **Notion Database** - Source of truth for technical skills (auto-synced, top 8 per category)
- **Jinja2 Template** (`templates/index.html.j2`) - HTML template with compact styling
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
│   └── volunteer.yaml          # Volunteer work (no nested structure)
├── scripts/
│   ├── fetch_notion_skills.py  # Notion → skills.yaml (excludes 0 proficiency)
│   └── generate_html.py        # YAML + Template → index.html
├── templates/
│   └── index.html.j2           # Jinja2 template (2-column grid, compact)
├── .github/workflows/
│   ├── update-skills.yml       # Fetch skills (uses PAT_TOKEN)
│   ├── generate-html.yml       # Generate HTML (uses PAT_TOKEN)
│   ├── generate-pdf.yml        # Create PDF
│   ├── deploy.yml              # Deploy to GitHub Pages (push to main)
│   └── release.yml             # Orchestrator (runs on release)
├── index.html                  # Generated (DO NOT EDIT)
├── requirements.txt            # Python dependencies
└── CNAME                       # GitHub Pages domain
```

## Development Workflow

**Making Content Updates:**

1. **To update CV content** (experience, projects, etc.):
   - Edit the appropriate YAML file in `data/`
   - Commit and push to `main`
   - Run "Generate HTML" workflow OR create a release

2. **To update technical skills**:
   - Update skills in Notion database: https://www.notion.so/dnull/ce553f61f831464eb05592124282802f
   - Notion property names: `Name` (title), `Class` (select), `Proficiency` (number)
   - Run "Update Skills from Notion" workflow OR create a release

3. **To regenerate HTML locally**:
   ```bash
   pip install -r requirements.txt
   python scripts/generate_html.py
   ```

4. **To fetch skills locally** (requires .env with NOTION_API_KEY):
   ```bash
   export NOTION_API_KEY="your_token"
   python scripts/fetch_notion_skills.py
   ```

## Automated Workflows

**Individual Workflows:**
- `update-skills.yml` - Fetches top 8 skills per category from Notion, excludes 0 proficiency, commits to main
- `generate-html.yml` - Renders Jinja2 template, commits to main
- `generate-pdf.yml` - Converts HTML to PDF using Playwright, attaches to release
- `deploy.yml` - Deploys to GitHub Pages (triggers on push to main when index.html changes)

**Release Workflow** (runs on GitHub release):
1. Update skills from Notion
2. Generate new index.html
3. Generate PDF and attach to release
4. Changes are committed to main → triggers deploy.yml → deployed to GitHub Pages

**Important Notes:**
- Workflows use `PAT_TOKEN` (not GITHUB_TOKEN) to trigger other workflows
- All workflows explicitly checkout `main` branch (not tag) to avoid detached HEAD
- Deploy happens automatically when index.html is pushed to main

## Skills System

**Notion Integration:**
- Database ID: `ce553f61-f831-464e-b055-92124282802f`
- Properties: `Name` (title), `Class` (select), `Proficiency` (number 0-10)
- Fetches top 8 skills per category sorted by proficiency (descending)
- **Excludes skills with 0 proficiency** automatically
- Output: `data/skills.yaml`

**Skills Configuration:**
- `TOP_N_SKILLS = 8` in `fetch_notion_skills.py`
- Skills displayed in 2-column grid (6 rows with 12 categories)
- Compact styling: small fonts (0.75em), tight spacing (3px margins), narrow bars (80px)

**Category Names and Emojis:**
```python
"AI Tools": "🤖"
"CI/CD": "🔄"
"Cloud Providers and Services": "☁️"
"Configuration Templating and Init": "📝"
"Data Storage and Databases": "💾"
"Hardware": "🖥️"
"Infrastructure as Code": "🏗️"
"Monitoring and Logging": "📊"
"Networking and Security": "🔐"
"Orchestration and Cluster Management": "⚙️"
"Programming Languages and Frameworks": "💻"
"Utils": "🛠️"
```

## Data File Structure

**YAML Format Guidelines:**

- `personal.yaml` - Flat structure: name, title, contact, summary
- `experience.yaml` - List under `jobs:` key
- `projects.yaml` - List under `projects:` key
- `skills.yaml` - Auto-generated, list under `skill_categories:` key
- `education.yaml` - List under `degrees:` key
- `languages.yaml` - List under `languages:` key
- `volunteer.yaml` - **Flat structure** (NOT nested): emoji, description at root level

**Important:** `volunteer.yaml` must have data at root level, not nested under `volunteer:` key.

## Deployment

**GitHub Pages:**
- Deployed from `main` branch via GitHub Actions
- Custom domain: cv.dnull.systems (configured via CNAME)
- Deployment triggers when `index.html` is pushed to main

**PDF Generation:**
- Uses Playwright/Chromium for rendering
- Attached to GitHub releases as `cv_bohdan_sukhomlinov.pdf`
- Latest PDF always available at: `https://github.com/shellshock1953/cv/releases/latest/download/cv_bohdan_sukhomlinov.pdf`

**Environment Protection:**
- GitHub Pages environment only allows deployments from `main` branch (not tags)
- Solution: Deploy workflow triggers on push to main, not from release context

## GitHub Secrets

Required secrets:
- `NOTION_API_KEY` - Notion integration token for fetching skills
- `PAT_TOKEN` - Personal Access Token with `repo` and `workflow` scopes (allows workflows to trigger other workflows)

## Design Decisions

**Skills Section:**
- 2-column grid layout (not 3 or 4) for readability
- Top 8 skills per category (balanced between detail and compactness)
- Excludes 0 proficiency skills (only show actual experience)
- Compact styling: 0.75em fonts, 3px spacing, 80px bars, 5px bar height
- 2-column responsive: desktop (2 cols) → tablet (2 cols) → mobile (1 col)

**Template Styling:**
- Inline CSS (no external stylesheets)
- Responsive design with breakpoints at 900px, 600px
- Print-optimized with `@media print`
- Color scheme: Blue tones (#1e40af, #2563eb)
- Skills use text-overflow ellipsis for long names

## Troubleshooting

**Detached HEAD errors:**
- Ensure workflows use `ref: main` in checkout steps
- Use `git push origin main` (not just `git push`)

**Deployment blocked by environment protection:**
- Deploy from main branch context, never from tag/release context
- Use separate deploy workflow triggered by push to main

**Workflows not triggering:**
- Use PAT_TOKEN instead of GITHUB_TOKEN in checkout
- GITHUB_TOKEN doesn't trigger other workflows (security feature)

## Important Notes

- `index.html` is auto-generated - DO NOT edit directly
- Edit YAML files in `data/` instead
- Skills come from Notion - update there, not in YAML manually
- Notion database uses "Class" property (not "Category")
- Volunteer YAML must be flat structure (common mistake)
- Use semantic versioning with `v` prefix (e.g., v0.0.1)
- Responsive design with mobile breakpoints at 600px
- Print-optimized styles using `@media print`
