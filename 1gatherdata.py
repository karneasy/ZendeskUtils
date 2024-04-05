import os
import requests
import json
from requests.auth import HTTPBasicAuth
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_API_ENDPOINTS, DATA_SAVE_PATH

def fetch_and_save_endpoint_data(endpoint, response_name):
    auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    headers = {'Content-Type': 'application/json'}
    url = f"https://{ZENDESK_URL}.zendesk.com{endpoint}"
    all_data = []
    params = {"page[size]": 100}  # Adjust page size as needed

    while url:
        print(f"Querying URL: {url}")
        response = requests.get(url, headers=headers, auth=auth, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            break

        data = response.json()
        batch_data = data.get(response_name, [])
        all_data.extend(batch_data)
        next_url = data.get('links', {}).get('next')  # Adjust based on the actual API response format for cursor links
        print(f"Fetched {len(batch_data)} records from {response_name}")
        url = next_url

    output_path = os.path.join(DATA_SAVE_PATH, f"{response_name}.json")
    with open(output_path, 'w') as json_file:
        json.dump(all_data, json_file)
    print(f"Data saved to {output_path}")

if not os.path.exists(DATA_SAVE_PATH):
    os.makedirs(DATA_SAVE_PATH)

for endpoint, response_name in ZENDESK_API_ENDPOINTS.items():
    fetch_and_save_endpoint_data(endpoint, response_name)
