import requests
import pandas as pd
import json

# Replace with your Zendesk subdomain, email, and API token
subdomain = 'your_subdomain'
email = 'your_email'
api_token = 'your_api_token'

# Base URL for Zendesk API
base_url = f'https://{subdomain}.zendesk.com/api/v2/help_center/sections.json'

# Set up authentication
auth = (f'{email}/token', api_token)

def get_sections(url, auth):
    sections = []
    while url:
        response = requests.get(url, auth=auth)
        data = response.json()
        sections.extend(data['sections'])
        url = data['next_page']  # This will be None when there are no more pages
    return sections

# Fetch all sections
sections = get_sections(base_url, auth)

# Convert to JSON and save to file
with open('sections.json', 'w') as json_file:
    json.dump(sections, json_file, indent=4)

# Load JSON and convert to CSV
df = pd.DataFrame(sections)
df.to_csv('sections.csv', index=False)

print("Sections have been successfully saved to sections.csv")
