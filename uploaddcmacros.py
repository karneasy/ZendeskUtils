import csv
import requests
import os
from collections import defaultdict
from requests.auth import HTTPBasicAuth
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
headers = {'Content-Type': 'application/json'}
url = f'https://{ZENDESK_URL}.zendesk.com/api/v2/macros.json'

def load_csv_and_group_by_title(csv_file_path):
    """Load CSV and group rows by macro_title."""
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = defaultdict(list)
        for row in reader:
            data[row['macro_title']].append(row)
    return data

def create_macros(grouped_data):
    """Create macros for each macro_title with the collected placeholders."""
    for macro_title, rows in grouped_data.items():
        # Check to ensure there are sufficient rows to process
        if len(rows) < 1:
            print(f"Skipping {macro_title} due to insufficient data.")
            continue

        # Use the dc_title and dc_placeholder from the second row (or first, if only one row)
        action_row = rows[0]  # assuming there's at least one row to process
        dc_title = action_row['dc_title']
        dc_placeholder = action_row['dc_placeholder']

        macro_data = {
            "macro": {
                "actions": [
                    {"field": "subject", "value": dc_title},
                    {"field": "comment_value_html", "value": dc_placeholder}
                ],
                "title": macro_title
            }
        }

        print('Request body to send: ', macro_data)
        print('-----')

        response = requests.post(url, json=macro_data, headers=headers, auth=auth)
        if response.status_code == 201:
            print(f"Macro '{macro_title}' created successfully.")
        else:
            print(f"Failed to create macro for '{macro_title}'. Status: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    csv_file_path = os.path.join(DATA_SAVE_PATH, 'macrostomake_with_placeholders.csv')
    grouped_data = load_csv_and_group_by_title(csv_file_path)
    create_macros(grouped_data)
