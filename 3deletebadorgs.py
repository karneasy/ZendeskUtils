import requests
import json
import os
import time
from requests.auth import HTTPBasicAuth
from settings import ZENDESK_URL, ZENDESK_EMAIL, ZENDESK_TOKEN, DATA_SAVE_PATH

def delete_org_memberships(batch_ids):
    """
    Delete organizations in a batch.
    """
    url = f"{ZENDESK_URL}/api/v2/organizations/destroy_many.json?ids={','.join(map(str, batch_ids))}"
    auth = HTTPBasicAuth(f'{ZENDESK_EMAIL}/token', ZENDESK_TOKEN)
    response = requests.delete(url, auth=auth)
    
    if response.status_code == 429:
        retry_after = int(response.headers.get('Retry-After', 1))
        print(f"Rate limit encountered. Retrying after {retry_after} seconds.")
        time.sleep(retry_after)
        return delete_org_memberships(batch_ids)  # Retry the request after waiting
    
    return response  # Return the response object for further inspection

# Load the organization IDs to remove
orgs_to_remove_file_path = os.path.join(DATA_SAVE_PATH, 'orgs_without_members_or_domains.json')
with open(orgs_to_remove_file_path, 'r') as file:
    org_ids_to_remove = json.load(file)

# Calculate total records and batches
records_to_delete = len(org_ids_to_remove)
total_batches = (records_to_delete + 99) // 100

# Open a file to log the deleted organization memberships
log_file_path = os.path.join(DATA_SAVE_PATH, 'orgsdeleted.txt')
with open(log_file_path, 'w') as log_file:
    for i in range(0, records_to_delete, 100):
        current_batch = (i // 100) + 1
        batch_ids = org_ids_to_remove[i:i+100]
        response = delete_org_memberships(batch_ids)
        
        # Log the response status code
        print(f"Batch {current_batch}/{total_batches} processed with response code: {response.status_code}")
        
        if response and response.status_code in [200, 204]:
            log_file.write(f"Successfully deleted organization memberships: {batch_ids}\n")
        else:
            log_file.write(f"Failed to delete batch. Status code: {response.status_code if response else 'N/A'}\n")

print(f"Completed processing all {records_to_delete} records. Check 'orgsdeleted.txt' for details.")
