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

    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code != 200:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return

    data = response.json()
    if 'count' in data:
        total_count = data['count']
        all_data.extend(data[response_name]) if response_name in data else None
        next_url = data.get('next_page')
    elif 'meta' in data and 'has_more' in data['meta']:
        batch_data = data[response_name] if response_name in data else []
        all_data.extend(batch_data)
        total_count = data['meta'].get('total', 0)
        print(f"Fetched {len(batch_data)}/{total_count} records from {response_name}")
        next_url = data.get('links', {}).get('next')
    else:
        print(f"Unknown pagination type for {response_name}")
        return

    while next_url is not None:
        print(f"Querying URL: {next_url}")
        response = requests.get(next_url, headers=headers, auth=auth)
        if response.status_code != 200:
            print(f"Failed to fetch data from {next_url}. Status code: {response.status_code}")
            break

        data = response.json()
        if 'count' in data:
            total_count = data['count']
            next_url = data.get('next_page')
            all_data.extend(data[response_name]) if response_name in data else None
            print(f"Fetched {len(data[response_name])}/{total_count} records from {response_name}")
        elif 'meta' in data and 'has_more' in data['meta']:
            batch_data = data[response_name] if response_name in data else []
            all_data.extend(batch_data)
            total_count = data['meta'].get('total', 0)
            print(f"Fetched {len(batch_data)}/{total_count} records from {response_name}")
            next_url = data.get('links', {}).get('next')
        else:
            print(f"Unknown pagination type for {response_name}")
            break

    output_path = os.path.join(DATA_SAVE_PATH, f"{response_name}.json")
    with open(output_path, 'w') as json_file:
        json.dump(all_data, json_file)
    print(f"Data saved to {output_path}")

if not os.path.exists(DATA_SAVE_PATH):
    os.makedirs(DATA_SAVE_PATH)

for endpoint, response_name in ZENDESK_API_ENDPOINTS.items():
    fetch_and_save_endpoint_data(endpoint, response_name)
