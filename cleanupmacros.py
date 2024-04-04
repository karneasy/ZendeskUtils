import json
import requests
import os
from requests.auth import HTTPBasicAuth
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

def load_macros(json_file_path):
    """Load macros from a JSON file."""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        macros = json.load(file)
    return macros

def find_complaint_macros_ids(macros):
    """Find and return IDs of macros with titles containing 'Complaints::'."""
    return [macro['id'] for macro in macros if 'Complaints::' in macro['title']]

def delete_macros(ids):
    """Delete macros by IDs using Zendesk API."""
    auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    headers = {'Content-Type': 'application/json'}
    ids_param = ','.join(map(str, ids))  # Convert list of IDs to comma-separated string
    url = f'https://{ZENDESK_URL}.zendesk.com/api/v2/macros/destroy_many?ids={ids_param}'

    response = requests.delete(url, headers=headers, auth=auth)
    if response.status_code in [200, 204]:
        print(f"Successfully deleted macros with IDs: {ids_param}")
    else:
        print(f"Failed to delete macros. Status: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    json_file_path = os.path.join(DATA_SAVE_PATH, 'macros.json')
    macros = load_macros(json_file_path)
    complaint_macro_ids = find_complaint_macros_ids(macros['macros'])  # Assuming the JSON structure has a 'macros' key
    if complaint_macro_ids:
        delete_macros(complaint_macro_ids)
    else:
        print("No Complaints:: macros found to delete.")
