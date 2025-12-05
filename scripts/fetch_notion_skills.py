#!/usr/bin/env python3
"""
Fetch technical skills from Notion database and generate skills.yaml
Queries the Tools database and extracts top 10 skills per category by proficiency.
"""

import os
import sys
from collections import defaultdict
from notion_client import Client
import yaml


# Configuration
NOTION_TOKEN = os.getenv("NOTION_API_KEY")
DATABASE_ID = "ce553f61-f831-464e-b055-92124282802f"
OUTPUT_FILE = "data/skills.yaml"
TOP_N_SKILLS = 10

# Emoji mapping for skill categories
CATEGORY_EMOJIS = {
    "AI Tools": "🤖",
    "CI/CD": "🔄",
    "Cloud Providers and Services": "☁️",
    "Configuration Templating and Init": "📝",
    "Data Storage and Databases": "💾",
    "Hardware": "🖥️",
    "Infrastructure as Code": "🏗️",
    "Monitoring and Logging": "📊",
    "Networking and Security": "🔐",
    "Orchestration and Cluster Management": "⚙️",
    "Programming Languages and Frameworks": "💻",
    "Utils": "🛠️",
}


def fetch_skills_from_notion():
    """Fetch all skills from Notion database."""
    if not NOTION_TOKEN:
        print("Error: NOTION_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    notion = Client(auth=NOTION_TOKEN)

    print(f"Fetching skills from Notion database: {DATABASE_ID}")

    try:
        # Query the database with pagination
        all_results = []
        has_more = True
        start_cursor = None

        while has_more:
            query_params = {"database_id": DATABASE_ID}
            if start_cursor:
                query_params["start_cursor"] = start_cursor

            results = notion.databases.query(**query_params)
            all_results.extend(results.get("results", []))
            has_more = results.get("has_more", False)
            start_cursor = results.get("next_cursor")

        print(f"Total pages fetched from Notion: {len(all_results)}")

        # Debug: Print available properties from first page
        if all_results:
            first_page = all_results[0]
            available_props = list(first_page.get("properties", {}).keys())
            print(f"Available properties in Notion: {available_props}")

        skills = []
        terraform_pages = []  # Debug: Track Terraform pages
        for page in all_results:
            properties = page.get("properties", {})

            # Extract skill data (adjust property names based on your Notion schema)
            name = extract_title(properties.get("Name", {}))
            category = extract_select(properties.get("Class", {}))  # Using "Class" property
            proficiency = extract_number(properties.get("Proficiency", {}))

            # Debug: Track Terraform
            if name and "terraform" in name.lower():
                terraform_pages.append({
                    "name": name,
                    "category": category or "NO CATEGORY",
                    "proficiency": proficiency if proficiency is not None else "NO PROFICIENCY"
                })

            # Skip skills with proficiency <= 4
            if name and category and proficiency is not None and proficiency >= 4:
                skills.append({
                    "name": name,
                    "category": category,
                    "proficiency": proficiency
                })

        # Debug: Report on Terraform
        if terraform_pages:
            print(f"\nDEBUG - Found {len(terraform_pages)} Terraform page(s) in Notion:")
            for t in terraform_pages:
                print(f"  - {t['name']}: category={t['category']}, proficiency={t['proficiency']}")
        else:
            print(f"\nDEBUG - No Terraform found. Showing all pages from Notion:")
            for page in all_results:
                properties = page.get("properties", {})
                n = extract_title(properties.get("Name", {}))
                c = extract_select(properties.get("Class", {}))
                p = extract_number(properties.get("Proficiency", {}))
                if n:  # Only show pages with names
                    status = "FILTERED OUT" if (not c or p is None or p <= 4) else "INCLUDED"
                    print(f"  [{status}] {n}: class={c or 'NONE'}, prof={p if p is not None else 'NONE'}")

        print(f"\nFetched {len(skills)} skills from Notion (after filtering)")

        # Debug: Look for Terraform
        terraform_found = [s for s in skills if "terraform" in s["name"].lower()]
        if terraform_found:
            print(f"\nDEBUG - Found Terraform entries:")
            for t in terraform_found:
                print(f"  - {t['name']}: category={t['category']}, proficiency={t['proficiency']}")
        else:
            print(f"\nDEBUG - No Terraform found in fetched skills (proficiency > 4)")
            print(f"DEBUG - This means Terraform either:")
            print(f"  1. Doesn't exist in Notion database")
            print(f"  2. Has proficiency <= 4")
            print(f"  3. Doesn't have 'Class' property set")

        return skills

    except Exception as e:
        print(f"Error fetching from Notion: {e}", file=sys.stderr)
        sys.exit(1)


def extract_title(prop):
    """Extract text from Notion title property."""
    if prop.get("type") == "title" and prop.get("title"):
        return prop["title"][0].get("plain_text", "")
    return None


def extract_select(prop):
    """Extract value from Notion select property."""
    if prop.get("type") == "select" and prop.get("select"):
        return prop["select"].get("name", "")
    return None


def extract_number(prop):
    """Extract number from Notion number property."""
    if prop.get("type") == "number":
        return prop.get("number")
    return None


def group_and_filter_skills(skills):
    """Group skills by category and get top N by proficiency."""
    grouped = defaultdict(list)

    for skill in skills:
        grouped[skill["category"]].append(skill)

    # Sort each category by proficiency (descending) and take top N
    top_skills = {}
    for category, category_skills in grouped.items():
        sorted_skills = sorted(
            category_skills,
            key=lambda x: x["proficiency"],
            reverse=True
        )[:TOP_N_SKILLS]

        # Debug: Print all skills for Infrastructure as Code
        if category == "Infrastructure as Code":
            print(f"\nDEBUG - {category} - All skills before filtering:")
            for s in sorted(category_skills, key=lambda x: x["proficiency"], reverse=True):
                print(f"  - {s['name']}: {s['proficiency']}")
            print(f"DEBUG - After taking top {TOP_N_SKILLS}:")
            for s in sorted_skills:
                print(f"  - {s['name']}: {s['proficiency']}")

        top_skills[category] = [
            {"name": s["name"], "proficiency": s["proficiency"]}
            for s in sorted_skills
        ]

    return top_skills


def generate_skills_yaml(skills_by_category):
    """Generate YAML structure with skills organized by category."""
    categories = []

    for category_name, skills in sorted(skills_by_category.items()):
        category = {
            "name": category_name,
            "emoji": CATEGORY_EMOJIS.get(category_name, "📌"),
            "skills": skills
        }
        categories.append(category)

    output = {"skill_categories": categories}

    # Write to file
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        yaml.dump(output, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"Generated {OUTPUT_FILE} with {len(categories)} categories")

    # Print summary
    for category in categories:
        print(f"  {category['emoji']} {category['name']}: {len(category['skills'])} skills")


def main():
    """Main execution function."""
    print("=" * 60)
    print("Notion Skills Fetcher")
    print("=" * 60)

    skills = fetch_skills_from_notion()
    skills_by_category = group_and_filter_skills(skills)
    generate_skills_yaml(skills_by_category)

    print("=" * 60)
    print("✅ Skills successfully fetched and saved!")
    print("=" * 60)


if __name__ == "__main__":
    main()
