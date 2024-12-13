import os
import requests
import json
from requests.auth import HTTPBasicAuth
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_API_ENDPOINTS, DATA_SAVE_PATH

def fetch_and_save_endpoint_data(endpoint, endpoint_config):
    auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    headers = {'Content-Type': 'application/json'}
    url = f"https://{ZENDESK_URL}.zendesk.com/api/v2/macros/active{endpoint}"  # Use the key as part of the URL
    all_data = []

    while True:
        response = requests.get(url, headers=headers, auth=auth, verify=False)
        if response.status_code != 200:
            print(f"Failed to fetch data from {url}, status code: {response.status_code}")
            break

        data = response.json()
        all_data.append(data)

        # Check for the next page cursor
        meta = data.get("meta", {})
        if not meta.get("has_more", False):
            print("Reached the last page.")
            break

        # Update the URL with the next cursor
        after_cursor = meta.get("after_cursor")
        if after_cursor:
            url = f"https://{ZENDESK_URL}.zendesk.com/api/v2/macros/active{endpoint}&page[after]={after_cursor}"
        else:
            print("No cursor found for the next page.")
            break

    # Save the complete JSON data to a file
    output_path = os.path.join(DATA_SAVE_PATH, f"{endpoint_config['response_name']}.json")
    with open(output_path, 'w') as json_file:
        json.dump(all_data, json_file, indent=4)
    print(f"Complete JSON data saved to {output_path}")

if not os.path.exists(DATA_SAVE_PATH):
    os.makedirs(DATA_SAVE_PATH)

# Iterate over the endpoints and configurations
for endpoint, config in ZENDESK_API_ENDPOINTS.items():
    fetch_and_save_endpoint_data(endpoint, config)
