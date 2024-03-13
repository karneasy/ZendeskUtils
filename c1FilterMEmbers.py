import os
import json
import math
from settings import DATA_SAVE_PATH

# Load the users json file
users_file_path = os.path.join(DATA_SAVE_PATH, 'users_without_org_filtered.json')
with open(users_file_path, 'r') as file:
    users_data = json.load(file)

#get each org_id and count how many users there are
org_user_count = {}
for user in users_data:
    org_id = user['organization_id']
    if org_id in org_user_count:
        org_user_count[org_id] += 1
    else:
        org_user_count[org_id] = 1

#Remove users with no domain down to user_id, email, and organization_id then pass to a new json file
filtered_users_data = [{'user_id': user['id'], 'email': user['email'], 'organization_id': user['organization_id']} for user in users_data]

# Save the filtered list of users without an organization to a new JSON file
users_without_org_file_path = os.path.join(DATA_SAVE_PATH, 'list_of_users.json')
with open(users_without_org_file_path, 'w') as file:
    json.dump(filtered_users_data, file)
    print(f"Data saved to {users_without_org_file_path}")