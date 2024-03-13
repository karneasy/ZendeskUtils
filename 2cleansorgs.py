import json
import os
from settings import DATA_SAVE_PATH

# Step 1: Load organization memberships and extract unique organization IDs
organization_memberships_file_path = os.path.join(DATA_SAVE_PATH, 'organization_memberships.json')
with open(organization_memberships_file_path, 'r') as file:
    organization_memberships_data = json.load(file)
unique_org_ids_from_memberships = {membership['organization_id'] for membership in organization_memberships_data}

# Step 2: Load organizations and filter those with empty domain names
organizations_file_path = os.path.join(DATA_SAVE_PATH, 'organizations.json')
with open(organizations_file_path, 'r') as file:
    organizations_data = json.load(file)
org_ids_with_empty_domains = {org['id'] for org in organizations_data if not org['domain_names']}

# Step 3: Combine and deduplicate the organization IDs
combined_org_ids = unique_org_ids_from_memberships.union(org_ids_with_empty_domains)

# Step 4: Save the combined list of organization IDs to a new JSON file
combined_orgs_file_path = os.path.join(DATA_SAVE_PATH, 'orgs_without_members_or_domains.json')
with open(combined_orgs_file_path, 'w') as file:
    json.dump(list(combined_org_ids), file)

print(f"IDs of organizations without members or domain names have been saved to {combined_orgs_file_path}")
