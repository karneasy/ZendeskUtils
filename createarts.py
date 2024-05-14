import csv
import requests
import json  # Import json to help parse the string of IDs
from settings import ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_URL, DATA_FETCH_PATH

zendesk_env = ZENDESK_URL
zendesk_username = ZENDESK_EMAIL + '/token'
zendesk_api_key = ZENDESK_TOKEN
csv_file = DATA_FETCH_PATH + '/articles.csv'

# Assuming zendesk_env is the full subdomain, including ".zendesk.com"
api_url_base = f'https://{zendesk_env}/api/v2/help_center'

auth = (zendesk_username, zendesk_api_key)

with open(csv_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        # Parse the content_tag_ids from a string representation of a list to an actual list of integers
        content_tag_ids = json.loads(row['content_tag_ids'])

        article_payload = {
            'article': {
                'title': row['title'],
                'body': row['body'],
                'locale': row['locale'],
                'user_segment_id': int(row['user_segment_id']),
                'permission_group_id': int(row['permission_group_id']),
                'section_id': int(row['section_id']),
                'label_names': row['labels'].split(),  # Assuming labels are space-separated
                'content_tag_ids': content_tag_ids  # Add content_tag_ids parsed from the string
            }
        }

        # Prepare the URL to create an article in the specified section
        api_url = f"{api_url_base}/sections/{row['section_id']}/articles.json"

        # Send the POST request to create the article
        response = requests.post(api_url, json=article_payload, auth=auth)

        if response.status_code == 201:
            print(f'Successfully created article: {row["title"]}')
        else:
            print(f'Failed to create article: {row["title"]}, Status Code: {response.status_code}, Response: {response.text}')
