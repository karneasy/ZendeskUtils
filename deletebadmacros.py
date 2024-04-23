import csv
import requests
from settings import ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_URL, DATA_FETCH_PATH

auth = (f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
headers = {'Content-Type': 'application/json'}
csv_file_path = f'{DATA_FETCH_PATH}/macrostofilter.csv'
delete_url_base = f'https://{ZENDESK_URL}/api/v2/macros/destroy_many.json?ids='

def filter_macros_for_deletion(csv_file_path):
    ids_to_delete = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['title'].startswith("Transfer::External::"):
                ids_to_delete.append(row['id'])
    return ids_to_delete

def delete_macros_in_batches(ids_to_delete, batch_size=100):
    # Process deletion in batches
    for start in range(0, len(ids_to_delete), batch_size):
        batch_ids = ids_to_delete[start:start + batch_size]
        ids_string = ','.join(batch_ids)
        delete_url = delete_url_base + ids_string
        response = requests.delete(delete_url, auth=auth, headers=headers)
        if response.status_code == 200:
            print(f"Successfully deleted batch of macros starting with ID {batch_ids[0]}.")
        else:
            print(f"Failed to delete batch of macros. Status: {response.status_code}, Error: {response.text}")

if __name__ == "__main__":
    ids_to_delete = filter_macros_for_deletion(csv_file_path)
    delete_macros_in_batches(ids_to_delete)
