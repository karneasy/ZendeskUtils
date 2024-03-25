import os
import csv
from zenpy import Zenpy
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

# Set up Zenpy with your Zendesk credentials
zenpy_client = Zenpy(subdomain=ZENDESK_URL, email=ZENDESK_EMAIL, token=ZENDESK_TOKEN)

# Function to recursively build section hierarchy
def build_section_hierarchy(section_id, hierarchy):
    section = zenpy_client.help_center.section(id=section_id)
    if section.parent_section_id:
        build_section_hierarchy(section.parent_section_id, hierarchy)
    hierarchy.append(section)

# Function to get section hierarchy
def get_section_hierarchy(article):
    hierarchy = []
    build_section_hierarchy(article.section_id, hierarchy)
    return hierarchy

# Write data to CSV file
csv_file_path = os.path.join(DATA_SAVE_PATH, 'output.csv')
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Category Name'] + [f'Section {i+1}' for i in range(10)] + ['Article Title', 'Article Body'])

    # Get all articles
    articles = list(zenpy_client.help_center.articles())

    # Loop through articles
    for article in articles:
        hierarchy = get_section_hierarchy(article)
        category_name = zenpy_client.help_center.category(id=hierarchy[-1].category_id).name
        row_data = [category_name if h.parent_section_id is None else h.name for h in hierarchy]
        row_data += [article.title, article.body]
        writer.writerow(row_data)
