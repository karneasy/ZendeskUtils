import csv
import requests
import time
from settings import ZENDESK_EMAIL, ZENDESK_TOKEN, ZENDESK_URL, DATA_FETCH_PATH, RECIPIENT_COMPANY_CUSTOM_FIELD_ID

zendesk_env = ZENDESK_URL
zendesk_username = ZENDESK_EMAIL + '/token'
zendesk_api_key = ZENDESK_TOKEN
ticket_field_id = RECIPIENT_COMPANY_CUSTOM_FIELD_ID
csv_file = DATA_FETCH_PATH + '/dependent.csv'

# Assuming zendesk_env is the full subdomain, including ".zendesk.com"
api_url_base = f'https://{zendesk_env}.zendesk.com/api/v2/ticket_fields/{ticket_field_id}/options'

auth = (zendesk_username, zendesk_api_key)

with open(csv_file, 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        option_payload = {
            'custom_field_option': {
                'name': row['name'],
                'value': row['value']
            }
        }
        
        response = requests.post(api_url_base, json=option_payload, auth=auth)

        if response.status_code == 200 or response.status_code == 201:
            print(f'Successfully updated/created option: {row["name"]}')
        else:
            print(f'Failed to update/create option: {row["name"]}, Status Code: {response.status_code}, Response: {response.text}')
        
        # Basic rate limit handling
        if 'Retry-After' in response.headers:
            retry_after = int(response.headers['Retry-After'])
            print(f'Rate limit reached. Waiting for {retry_after} seconds.')
            time.sleep(retry_after + 1)  # Waiting a bit longer just to be safe
        else:
            # Adjust this sleep time based on your API's rate limit policies
            time.sleep(1)
