import os
import json
import requests
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN

def split_into_batches(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

def make_put_request(batch_data):
    auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    headers = {'Content-Type': 'application/json'}
    url = f"{ZENDESK_URL}/api/v2/macros/update_many"
    response = requests.put(url, json=batch_data, headers=headers, auth=auth)
    print(response.json())

def main():
    batch_size = 100

    updated_matching_records_file_path = os.path.join(DATA_SAVE_PATH, "updated_matching_records.json")
    with open(updated_matching_records_file_path, "r") as file:
        data = json.load(file)

    batches = list(split_into_batches(data.get("matching_records", []), batch_size))

    for idx, batch_data in enumerate(batches, start=1):
        print(f"Processing Batch {idx}...")
        make_put_request(batch_data)

if __name__ == "__main__":
    main()
