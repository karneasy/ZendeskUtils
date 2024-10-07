import csv
import os
import requests
from requests.auth import HTTPBasicAuth
import json  # Import json to help parse the string of IDs


ZENDESK_URL = '123'
ZENDESK_EMAIL = '123'
ZENDESK_TOKEN = '123'
csv_file = 'transactionarticles.csv'

def create_articles_from_csv(csv_file):
    auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    headers = {'Content-Type': 'application/json'}
    api_url_base = f"https://{ZENDESK_URL}.zendesk.com/api/v2/help_center/en-us"

    all_data = []

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            article_payload = {
                'article': {
                    'title': row['article'],  # Using the 'article' column for the title
                    'body': row['article'],   # Using the 'article' column for the body as well
                    'locale': 'en-us',  # Assuming locale is always 'en-us'
                    'user_segment_id': int(row['user_segment_id']),
                    'permission_group_id': int(row['permission_group_id']),
                },
                'notify_subscribers': False
            }

            # Prepare the URL to create an article in the specified section
            api_url = f"{api_url_base}/sections/{row['section_id']}/articles"

            print(f"Creating article in section {row['section_id']} with title: {row['article']}")
            response = requests.post(api_url, headers=headers, auth=auth, json=article_payload)

            if response.status_code == 201:
                print(f"Successfully created article: {row['article']}")
                all_data.append(response.json())
            else:
                print(f"Failed to create article: {row['article']}, Status Code: {response.status_code}, Response: {response.text}")

    # Save all responses to a JSON file for record-keeping
    output_path = os.path.join('created_articles_responses.json')
    with open(output_path, 'w') as json_file:
        json.dump(all_data, json_file)
    print(f"Data saved to {output_path}")


# Path to the CSV file
csv_file = os.path.join('transactionarticles.csv')
create_articles_from_csv(csv_file)
