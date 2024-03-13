import os
import requests
import json
import time
from requests.auth import HTTPBasicAuth
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_API_ENDPOINTS, DATA_SAVE_PATH

def fetch_and_save_endpoint_data(endpoint, response_name):
    auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    headers = {'Content-Type': 'application/json'}
    url = f"{ZENDESK_URL}{endpoint}.json?page[size]=100"
    all_data = []
    total_count = 0

    while url:
        response = requests.get(url, headers=headers, auth=auth)
        if response.status_code == 200:
            data = response.json()
            if 'count' in data:
                total_count = data['count']
                next_url = data.get('next_page')
            elif 'meta' in data and 'has_more' in data['meta']:
                batch_data = data[response_name]
                all_data.extend(batch_data)
                batch_count = len(batch_data)
                total_count = data['meta'].get('total', 0)
                print(f"Fetched {batch_count}/{total_count} records from {response_name}")
                next_url = data.get('links', {}).get('next')
            else:
                print(f"Unknown pagination type for {response_name}")
                break

            url = next_url
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 60))
            print(f"Rate limit hit. Waiting for {retry_after} seconds before retrying...")
            time.sleep(retry_after)
        else:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            break

    output_path = os.path.join(DATA_SAVE_PATH, f"{response_name}.json")
    with open(output_path, 'w') as json_file:
        json.dump(all_data, json_file)
    print(f"Data saved to {output_path}")

if not os.path.exists(DATA_SAVE_PATH):
    os.makedirs(DATA_SAVE_PATH)

for endpoint, response_name in ZENDESK_API_ENDPOINTS.items():
    fetch_and_save_endpoint_data(endpoint, response_name)
