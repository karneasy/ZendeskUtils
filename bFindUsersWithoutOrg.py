import os
import json
import math
from settings import DATA_SAVE_PATH

# Load the users json file
users_file_path = os.path.join(DATA_SAVE_PATH, 'users.json')
with open(users_file_path, 'r') as file:
    users_data = json.load(file)

# Search the users for those without an organization
users_without_org = [user for user in users_data if not user.get('organization_id')]
print(f"Found {len(users_without_org)} users without an organization")

# Prepare data with only user_id and email for each user
filtered_users_data = [{'user_id': user['id'], 'email': user['email']} for user in users_without_org]

# Save the filtered list of users without an organization to a new JSON file
users_without_org_file_path = os.path.join(DATA_SAVE_PATH, 'users_without_org_filtered.json')
with open(users_without_org_file_path, 'w') as file:
    json.dump(filtered_users_data, file)

# Corrected the print statement to properly format the file path
print(f"Data saved to {users_without_org_file_path}")

# Extract the domain from the users' email and add it to users_without_org
for user in users_without_org:
    # Use a default value of '' if email is None or not present
    email = user.get('email') or ''  # This ensures email is a string, even if it's empty
    # Now, it's safe to check if '@' is in email and to split it
    user['domain'] = email.split('@')[1] if '@' in email else 'No email'

# Save the updated list of users without an organization to the same JSON file
with open(users_without_org_file_path, 'w') as file:
    json.dump(users_without_org, file)
    # Print statement after updating the file
    print(f"Data including the domain saved to {users_without_org_file_path}")

#Load the organizations json file
organizations_file_path = os.path.join(DATA_SAVE_PATH, 'organizations.json')
with open(organizations_file_path, 'r') as file:
    organizations_data = json.load(file)
    print(f"Data loaded from {organizations_file_path}")

# Get the org_id and domain name and pass it to a new list
org_domain_data = [{'org_id': org['id'], 'domain_names': org['domain_names']} for org in organizations_data]

# Compare the domains in org_domain_data with the domain in users_without_org and when it matches add the org_id to the users_without_org json
for user in users_without_org:
    for org in org_domain_data:
        if user['domain'] in org['domain_names']:
            user['organization_id'] = org['org_id']
            print(f"Added organization_id {org['org_id']} to user {user['id']}")
            break
    else:
        user['organization_id'] = None

# Save the updated list of users without an organization to the same JSON file
with open(users_without_org_file_path, 'w') as file:
    json.dump(users_without_org, file)
    # Print statement after updating the file
    print(f"Data including the organization_id saved to {users_without_org_file_path}")
    