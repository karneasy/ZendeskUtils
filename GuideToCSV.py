import os
import json
import csv
from zenpy import Zenpy
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

# Set up Zenpy with your Zendesk credentials
zenpy_client = Zenpy(subdomain=ZENDESK_URL, email=ZENDESK_EMAIL, token=ZENDESK_TOKEN)

def download_articles():
    print("Downloading articles...")
    articles = list(zenpy_client.help_center.articles())
    article_data = [{'id': article.id, 'title': article.title, 'section_id': article.section_id} for article in articles]
    with open(os.path.join(DATA_SAVE_PATH, 'articles.json'), 'w') as json_file:
        json.dump(article_data, json_file)
    print("Articles downloaded and saved to 'articles.json'.")

def download_categories():
    print("Downloading categories...")
    categories = list(zenpy_client.help_center.categories())
    category_data = [{'id': category.id, 'name': category.name} for category in categories]
    with open(os.path.join(DATA_SAVE_PATH, 'categories.json'), 'w') as json_file:
        json.dump(category_data, json_file)
    print("Categories downloaded and saved to 'categories.json'.")

def download_sections():
    print("Downloading sections...")
    sections = list(zenpy_client.help_center.sections())
    section_data = [{'id': section.id, 'name': section.name, 'parent_section_id': section.parent_section_id} for section in sections]
    with open(os.path.join(DATA_SAVE_PATH, 'sections.json'), 'w') as json_file:
        json.dump(section_data, json_file)
    print("Sections downloaded and saved to 'sections.json'.")

def build_section_hierarchy(section_id, sections):
    hierarchy = []
    while section_id is not None:
        section = next((section for section in sections if section['id'] == section_id), None)
        if section:
            hierarchy.insert(0, section)
            section_id = section['parent_section_id']
        else:
            section_id = None
    return hierarchy

def generate_csv():
    print("Generating CSV file...")
    with open(os.path.join(DATA_SAVE_PATH, 'articles.json')) as json_file:
        articles = json.load(json_file)
    with open(os.path.join(DATA_SAVE_PATH, 'categories.json')) as json_file:
        categories = json.load(json_file)
    with open(os.path.join(DATA_SAVE_PATH, 'sections.json')) as json_file:
        sections = json.load(json_file)
    
    # Determine maximum depth of section hierarchy
    max_depth = max(len(build_section_hierarchy(article['section_id'], sections)) for article in articles)
    
    with open(os.path.join(DATA_SAVE_PATH, 'output.csv'), mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        # Create header row dynamically based on max depth
        header_row = ['Category Name'] + [f'Section {i+1}' for i in range(max_depth)] + ['Article Title']
        writer.writerow(header_row)

        for article in articles:
            article_section_id = article['section_id']
            if article_section_id:
                article_sections = build_section_hierarchy(article_section_id, sections)
                article_category_id = article_sections[-1]['category_id']
                article_category = next((category for category in categories if category['id'] == article_category_id), None)
                if article_category:
                    row_data = [article_category['name']]
                    row_data += [section['name'] if section else 'null' for section in article_sections[:-1]]
                    # Pad row data with "null" to match max depth
                    row_data += ['null'] * (max_depth - len(article_sections[:-1]))
                    row_data.append(article['title'])
                    writer.writerow(row_data)
    print("CSV file generated successfully.")

# Download data
download_articles()
download_categories()
download_sections()

# Generate CSV
generate_csv()
