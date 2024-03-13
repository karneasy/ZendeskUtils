import requests
import json
import os
import time
from requests.auth import HTTPBasicAuth
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

def delete_organizations(batch):
    """
    Send a DELETE request to remove organizations in a batch.
    """
    ids = ",".join(str(org_id) for org_id in batch)
    url = f"{ZENDESK_URL}/api/v2/organizations/destroy_many.json?ids={ids}"
    auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    response = requests.delete(url, auth=auth)

    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))
        print(f"Rate limit hit. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)
        return delete_organizations(batch)  # Retry the same batch after waiting

    return response

# Assuming you have a JSON file with organization IDs to delete
# For this example, let's say it's structured as a list of IDs: [1, 2, 3, ...]
input_file_path = os.path.join(DATA_SAVE_PATH, 'orgstoremove.json')
with open(input_file_path, 'r') as file:
    org_ids = json.load(file)

total_orgs = len(org_ids)
orgs_deleted = 0

print(f"Total organizations to delete: {total_orgs}")

for i in range(0, total_orgs, 100):
    batch = org_ids[i:i+100]
    response = delete_organizations(batch)
    if response and response.status_code in [200, 204]:
        orgs_deleted += len(batch)
        print(f"{orgs_deleted}/{total_orgs} organizations deleted.")
    else:
        print(f"Failed to delete batch starting with ID {batch[0]}. Status code: {response.status_code if response else 'N/A'}")

print("Organization deletion process completed.")
