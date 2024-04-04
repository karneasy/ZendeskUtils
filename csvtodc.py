import csv
import requests
import os
from requests.auth import HTTPBasicAuth
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_FETCH_PATH

auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
headers = {'Content-Type': 'application/json'}
url = f'https://{ZENDESK_URL}.zendesk.com/api/v2/dynamic_content/items.json'

def create_dynamic_content(csv_file_path):
    """
    Create dynamic content items and variants for specific locales via Zendesk API.
    """
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
                        {"locale_id": 1, "default": True, "content": body},    # Default locale variant
                        {"locale_id": 10, "default": False, "content": body},   # Additional variant
                        {"locale_id": 1176, "default": False, "content": body}  # Additional variant
                    ]
                }
            }

            print('data',data)
            print('ready to send')
            response=requests.post(url, headers=headers, auth=auth)

            if response.status_code == 201:
                print(f"Dynamic content '{title}' created successfully.")
            else:
                print(f"Failed to create dynamic content for '{title}'. Error: {response.text}")

if __name__ == "__main__":
    csv_file_path = os.path.join(DATA_FETCH_PATH, 'dynamic_content.csv')
    create_dynamic_content(csv_file_path)




/////////

{'item': {'name': 'macro_Complaints_External_Update_1_Title', 'default_locale_id': 1, 'variants': [{'locale_id': 1, 'default': True, 'content': 'Re: Complaint {{ticket.id}} - {{ticket.title}}'}, {'locale_id': 10, 'default': False, 'content': 'Re: Complaint {{ticket.id}} - {{ticket.title}}'}, {'locale_id': 1176, 'default': False, 'content': 'Re: Complaint {{ticket.id}} - {{ticket.title}}'}]}}
