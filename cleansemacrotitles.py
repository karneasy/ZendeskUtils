import csv
import requests
from settings import ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_URL, DATA_FETCH_PATH

auth = (f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
headers = {'Content-Type': 'application/json'}
csv_file_path = f'{DATA_FETCH_PATH}/macrostofilter.csv'

def filter_and_correct_titles(csv_file_path):
    updates_needed = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            original_title = row['title']
            corrected_title = correct_title(original_title)
            if corrected_title != original_title:  # Check if correction was necessary
                updates_needed.append({'id': row['id'], 'title': corrected_title})
                print(f"Title correction needed: '{original_title}' corrected to '{corrected_title}'")
    return updates_needed

def correct_title(title):
    parts = title.split('::')
    corrected_parts = [part.strip() for part in parts]
    return '::'.join(corrected_parts)

def update_macro(macro):
    update_url = f'https://{ZENDESK_URL}/api/v2/macros/{macro["id"]}.json'
    payload = {
        "macro": {
            "title": macro['title']
        }
    }
    response = requests.put(update_url, json=payload, headers=headers, auth=auth)
    if response.status_code == 200:
        print(f"Successfully updated macro with ID {macro['id']}.")
    else:
        print(f"Failed to update macro with ID {macro['id']}. Status: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    updates_needed = filter_and_correct_titles(csv_file_path)
    for macro in updates_needed:
        update_macro(macro)
