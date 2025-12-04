# Bohdan Sukhomlinov - CV

**Senior DevOps Engineer | Platform Engineer | SRE**

🌐 **Live Site:** [cv.dnull.systems](https://cv.dnull.systems)

---

## Overview

This repository contains my professional CV/resume, built with an automated template-based generation system. The site combines:

- **Local YAML files** for experience, projects, education (version-controlled)
- **Notion Database** for technical skills (auto-synced)
- **Jinja2 Templates** for HTML generation
- **GitHub Actions** for automated deployment
- **GitHub Pages** for hosting

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate HTML:**
   ```bash
   python scripts/generate_html.py
   ```

3. **Fetch skills from Notion:**
   ```bash
   export NOTION_API_KEY="your_notion_api_key"
   python scripts/fetch_notion_skills.py
   ```

### Making Updates

**To update CV content:**
1. Edit the appropriate YAML file in `data/`
2. Commit and push to `main`
3. Run "Generate HTML" workflow manually OR create a release

**To update technical skills:**
1. Update skills in [Notion database](https://www.notion.so/dnull/ce553f61f831464eb05592124282802f)
2. Run "Update Skills from Notion" workflow manually OR create a release

**To trigger a full build and deployment:**
1. Create a new GitHub release (semantic versioning recommended)
2. Workflows automatically:
   - Update skills from Notion
   - Generate index.html
   - Create PDF
   - Deploy to GitHub Pages
   - Attach PDF to release

## Architecture

```
cv/
├── data/                       # Edit YAML files here to update CV
│   ├── personal.yaml
│   ├── experience.yaml
│   ├── projects.yaml
│   ├── skills.yaml             # Auto-generated from Notion
│   ├── education.yaml
│   ├── languages.yaml
│   └── volunteer.yaml
├── scripts/
│   ├── fetch_notion_skills.py  # Notion → skills.yaml
│   └── generate_html.py        # YAML + Template → index.html
├── templates/
│   └── index.html.j2           # Jinja2 template
├── .github/workflows/
│   ├── update-skills.yml       # Reusable workflow
│   ├── generate-html.yml       # Reusable workflow
│   ├── generate-pdf.yml        # Reusable workflow
│   └── release.yml             # Orchestrator
└── index.html                  # Generated (DO NOT EDIT)
```

## Workflows

### Individual Workflows (Manual Trigger)

- **Update Skills** - Fetch skills from Notion
- **Generate HTML** - Render template with YAML data
- **Generate PDF** - Convert HTML to PDF

### Release Workflow (Automatic)

Triggered on GitHub release creation:
1. Updates skills from Notion
2. Generates index.html
3. Creates PDF
4. Deploys to GitHub Pages
5. Attaches PDF to release

## Features

- **Automated Content Pipeline** - Edit YAML → Generate HTML → Deploy
- **Notion Integration** - Skills auto-sync from Notion database
- **PDF Generation** - Professional PDF attached to releases
- **GitHub Pages Hosting** - Custom domain support
- **Responsive Design** - Mobile-friendly and print-optimized
- **Separation of Concerns** - Modular workflows for maintainability

## Skills System

Technical skills are maintained in a [Notion database](https://www.notion.so/dnull/ce553f61f831464eb05592124282802f) with:
- **Name** - Technology/tool name
- **Category** - Skill grouping
- **Proficiency** - 1-10 rating

The automation fetches the top 10 skills per category (sorted by proficiency) and generates `data/skills.yaml`.

## Technologies Used

- **Template Engine:** Jinja2
- **Data Format:** YAML
- **CI/CD:** GitHub Actions
- **PDF Generation:** Playwright/Chromium
- **Integration:** Notion API
- **Hosting:** GitHub Pages
- **Domain:** cv.dnull.systems

## License

Personal CV repository - all rights reserved.

---

**Last Updated:** December 2024
