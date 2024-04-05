import requests
import json
import os
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

def fetch_content_tags():
    # Setup the endpoint
    endpoint = f"https://{ZENDESK_URL}.zendesk.com/api/v2/guide/content_tags"
    headers = {'Content-Type': 'application/json'}
    auth = (f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    
    all_tags = []
    while endpoint:
        response = requests.get(endpoint, headers=headers, auth=auth)
        if response.status_code != 200:
            print(f"Failed to fetch data from {endpoint}. Status code: {response.status_code}")
            return []
        
        data = response.json()
        tags = data.get('content_tags', [])
        all_tags.extend(tags)

        # Cursor-based pagination: look for 'next_page' link
        endpoint = data.get('next_page')

    return all_tags

if __name__ == "__main__":
    content_tags = fetch_content_tags()

    # Ensure the DATA_SAVE_PATH exists
    if not os.path.exists(DATA_SAVE_PATH):
        os.makedirs(DATA_SAVE_PATH)

    # Save the fetched content tags to a JSON file
    file_path = os.path.join(DATA_SAVE_PATH, "content_tags.json")
    with open(file_path, 'w') as file:
        json.dump(content_tags, file)
    
    print(f"Content tags saved to {file_path}")
