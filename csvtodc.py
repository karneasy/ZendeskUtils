import csv
import requests
import os
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

def create_dynamic_content(csv_file_path):
    """
    Create dynamic content items and variants for specific locales via Zendesk API.
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ZENDESK_TOKEN}'
    }

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            title = row['dc_title']
            body = row['dc_body']

            # Construct the payload for dynamic content creation
            data = {
                "item": {
                    "name": title,
                    "default_locale_id": 1,
                    "variants": [
                        {"locale_id": 1, "content": body},    # Default locale variant
                        {"locale_id": 10, "content": body},   # Additional variant
                        {"locale_id": 1176, "content": body}  # Additional variant
                    ]
                }
            }

            response = requests.post(f'https://{ZENDESK_URL}/api/v2/dynamic_content/items.json',
                                     json=data, headers=headers)

            if response.status_code == 201:
                print(f"Dynamic content '{title}' created successfully.")
            else:
                print(f"Failed to create dynamic content for '{title}'. Error: {response.text}")

if __name__ == "__main__":
    csv_file_path = os.path.join(DATA_SAVE_PATH, 'dynamic_content.csv')
    create_dynamic_content(csv_file_path)
