#!/usr/bin/env python3
"""
Generate index.html from YAML data and Jinja2 template.
Loads all data files and renders the CV HTML.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader


# Paths
DATA_DIR = Path("data")
TEMPLATE_DIR = Path("templates")
TEMPLATE_FILE = "index.html.j2"
OUTPUT_FILE = "index.html"

# Data files to load
DATA_FILES = {
    "personal": "personal.yaml",
    "experience": "experience.yaml",
    "projects": "projects.yaml",
    "opensource": "opensource.yaml",
    "presentations": "presentations.yaml",
    "skills": "skills.yaml",
    "education": "education.yaml",
    "languages": "languages.yaml",
    "volunteer": "volunteer.yaml",
}


def load_yaml_file(file_path):
    """Load YAML file and return parsed data."""
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)


def load_all_data():
    """Load all YAML data files."""
    data = {}

    print("Loading data files:")
    for key, filename in DATA_FILES.items():
        file_path = DATA_DIR / filename
        print(f"  - {filename}")
        data[key] = load_yaml_file(file_path)

    return data


def render_template(data):
    """Render the Jinja2 template with data."""
    # Set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(TEMPLATE_DIR),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Load template
    try:
        template = env.get_template(TEMPLATE_FILE)
    except Exception as e:
        print(f"Error loading template {TEMPLATE_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    # Add current date for "Last updated"
    data["updated_date"] = datetime.now().strftime("%B %Y")

    # Render template
    try:
        html_content = template.render(**data)
        return html_content
    except Exception as e:
        print(f"Error rendering template: {e}", file=sys.stderr)
        sys.exit(1)


def write_output(content):
    """Write rendered HTML to output file."""
    try:
        with open(OUTPUT_FILE, "w") as f:
            f.write(content)
        print(f"\n✅ Generated {OUTPUT_FILE}")
    except Exception as e:
        print(f"Error writing output file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main execution function."""
    print("=" * 60)
    print("CV HTML Generator")
    print("=" * 60)

    # Load data
    data = load_all_data()

    # Render template
    print(f"\nRendering template: {TEMPLATE_FILE}")
    html_content = render_template(data)

    # Write output
    write_output(html_content)

    print("=" * 60)
    print("✅ HTML generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
