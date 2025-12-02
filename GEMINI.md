# Project Overview

This project is an automated CV/resume generation system. It uses YAML files for storing CV data, Jinja2 for templating, and a Python script to generate a static `index.html` file. The system also integrates with the Notion API to fetch and update skills, which are then stored in `data/skills.yaml`.

The project is deployed to GitHub Pages and includes GitHub Actions workflows to automate the entire process, including updating skills from Notion, generating the HTML, and creating a PDF version of the CV upon a new release.

The main technologies used are:
- Python
- Jinja2
- YAML
- Notion API
- GitHub Actions
- GitHub Pages

# Building and Running

## Prerequisites

- Python 3
- `pip`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/shellshock1953/cv.git
   cd cv
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the generator

1. **To generate the HTML file:**
   ```bash
   python scripts/generate_html.py
   ```
   This will create/update the `index.html` file in the root directory.

2. **To fetch skills from Notion:**
   - Set the `NOTION_API_KEY` environment variable:
     ```bash
     export NOTION_API_KEY="your_notion_api_key"
     ```
   - Run the script:
     ```bash
     python scripts/fetch_notion_skills.py
     ```
     This will update the `data/skills.yaml` file with the latest skills from your Notion database.

# Development Conventions

## Data Management

- All CV data is stored in YAML files in the `data/` directory.
- Skills are managed in a Notion database and synced to `data/skills.yaml` using the `fetch_notion_skills.py` script.

## Templating

- The HTML is generated from the `templates/index.html.j2` Jinja2 template.

## Automation

- The entire process of updating skills, generating HTML, and deploying to GitHub Pages is automated using GitHub Actions.
- The workflows are defined in the `.github/workflows/` directory.
- A new release triggers a complete update and deployment, including the generation of a PDF version of the CV.

## Committing

- The GitHub Actions workflows are configured to automatically commit changes to `index.html` and `data/skills.yaml` to the `main` branch.
- The commit messages are standardized and attributed to `github-actions[bot]`.
