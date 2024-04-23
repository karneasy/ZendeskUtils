import csv
import requests
from settings import ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_URL, DATA_FETCH_PATH

auth = (f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
headers = {'Content-Type': 'application/json'}
csv_file_path = f'{DATA_FETCH_PATH}/macrostofilter.csv'
update_url_base = f'https://{ZENDESK_URL}/api/v2/macros/update_many.json'

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

def update_macros_in_batches(updates_needed, batch_size=100):
    # Process updates in batches
    for start in range(0, len(updates_needed), batch_size):
        batch_updates = updates_needed[start:start + batch_size]
        payload = {
            'macros': [
                {'id': macro['id'], 'macro': {'title': macro['title']}}
                for macro in batch_updates
            ]
        }
        print(f"Sending the following payload for update: {payload}")  # Print the body of the request
        response = requests.put(update_url_base, json=payload, headers=headers, auth=auth)
        if response.status_code == 200:
            print(f"Successfully updated batch of macros starting with ID {batch_updates[0]['id']}.")
        else:
            print(f"Failed to update batch of macros. Status: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    updates_needed = filter_and_correct_titles(csv_file_path)
    if updates_needed:
        update_macros_in_batches(updates_needed)
    else:
        print("No titles require correction.")
