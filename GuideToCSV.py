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
    writer.writerow(['Category Name'] + [f'Section Level {i+1}' for i in range(10)] + ['Article Title', 'Article Body'])

    # Get all sections
    sections = list(zenpy_client.help_center.sections())

#iterate through sections, any section with no parent_section_id is a top level section, then create columns for each level beneath, based on parent_section_id
    for section in sections:
        if section.parent_section_id is None:
            section_hierarchy = get_section_hierarchy(section.id)
            for i in range(10):
                if not section_hierarchy[i]:
                    break
                writer.writerow([section.category.name] + [section.name for section in section_hierarchy[i]] + ['', ''])
                for article in zenpy_client.help_center.articles(section_id=section.id):
                    writer.writerow([''] * (i + 2) + [article.title, article.body])
        else:
            continue
print(f"Data saved to {csv_file_path}")
