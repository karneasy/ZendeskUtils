import os
import csv
from zenpy import Zenpy
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

# Set up Zenpy with your Zendesk credentials
zenpy_client = Zenpy(subdomain=ZENDESK_URL, email=ZENDESK_EMAIL, token=ZENDESK_TOKEN)

# Function to recursively build section hierarchy
def build_section_hierarchy(section_id, level, hierarchy):
    children = [section for section in sections if section.parent_section_id == section_id]
    if not children:
        return
    for child in children:
        hierarchy[level].append(child)
        build_section_hierarchy(child.id, level + 1, hierarchy)

# Function to get section hierarchy
def get_section_hierarchy(section_id):
    hierarchy = [[] for _ in range(10)]  # Assuming maximum 10 levels
    build_section_hierarchy(section_id, 0, hierarchy)
    return hierarchy

# Write data to CSV file
csv_file_path = os.path.join(DATA_SAVE_PATH, 'output.csv')
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Category Name', 'Section Name', 'Article Title', 'Article Body'])

    # Get all sections
    sections = list(zenpy_client.help_center.sections())

    # Loop through top-level sections
    for section in sections:
        if section.parent_section_id is None:
            hierarchy = get_section_hierarchy(section.id)
            articles = zenpy_client.help_center.articles(section=section)
            for article in articles:
                for level in hierarchy:
                    for s in level:
                        writer.writerow([section.category().name, s.name, article.title, article.body])
