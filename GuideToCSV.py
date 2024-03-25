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
    article_data = [{'id': article.id, 'title': article.title} for article in articles]
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

def generate_csv():
    print("Generating CSV file...")
    with open(os.path.join(DATA_SAVE_PATH, 'articles.json')) as json_file:
        articles = json.load(json_file)
    with open(os.path.join(DATA_SAVE_PATH, 'categories.json')) as json_file:
        categories = json.load(json_file)
    with open(os.path.join(DATA_SAVE_PATH, 'sections.json')) as json_file:
        sections = json.load(json_file)
    
    with open(os.path.join(DATA_SAVE_PATH, 'output.csv'), mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Category Name', 'Section Name', 'Article Title'])

        for article in articles:
            article_section_id = next((section['id'] for section in sections if section['id'] == article['section_id']), None)
            if article_section_id:
                article_section = next((section for section in sections if section['id'] == article_section_id), None)
                article_category_id = next((category['id'] for category in categories if category['id'] == article_section['category_id']), None)
                if article_category_id:
                    article_category = next((category for category in categories if category['id'] == article_category_id), None)
                    writer.writerow([article_category['name'], article_section['name'], article['title']])
    print("CSV file generated successfully.")

# Download data
download_articles()
download_categories()
download_sections()

# Generate CSV
generate_csv()
