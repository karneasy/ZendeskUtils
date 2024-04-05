import os
import requests
import json
from requests.auth import HTTPBasicAuth
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_API_ENDPOINTS, DATA_SAVE_PATH

def fetch_and_save_endpoint_data(endpoint_config):
    auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    headers = {'Content-Type': 'application/json'}
    response_name = endpoint_config["response_name"]
    pagination = endpoint_config["pagination"]

    all_data = []
    url = f"https://{ZENDESK_URL}.zendesk.com{endpoint}"
    params = {}
    
    if pagination["type"] == "page_number":
        params[pagination["size_param"]] = pagination["size"]
        page = 1

    while True:
        print(f"Querying URL: {url}")
        response = requests.get(url, headers=headers, auth=auth, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            break

        data = response.json()
        batch_data = data.get(response_name, [])
        all_data.extend(batch_data)

        if pagination["type"] == "cursor":
            if not data.get(pagination["meta_key"], {}).get(pagination["has_more"], False):
                break
            params[pagination["param_name"]] = data[pagination["meta_key"]][pagination["cursor_key"]]
        elif pagination["type"] == "page_number":
            if not batch_data:
                break
            page += 1
            params[pagination["param_name"]] = page
        else:
            break  # Unknown pagination type

    output_path = os.path.join(DATA_SAVE_PATH, f"{response_name}.json")
    with open(output_path, 'w') as json_file:
        json.dump(all_data, json_file)
    print(f"Data saved to {output_path}")

if not os.path.exists(DATA_SAVE_PATH):
    os.makedirs(DATA_SAVE_PATH)

for endpoint, config in ZENDESK_API_ENDPOINTS.items():
    fetch_and_save_endpoint_data(config)
